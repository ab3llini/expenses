import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go
import streamlit as st
from models import CashFlow, CategoryLevel, Granularity


@st.cache_data
def earnings_expenses_bar(
    df: pd.DataFrame, granularity: Granularity, height: int
) -> go.Figure:
    group_df = df.groupby([granularity.lower()]).agg(
        {CashFlow.Earning: "sum", CashFlow.Expense: "sum"}
    )
    group_df = group_df.reset_index().melt(
        id_vars=granularity.lower(),
        value_vars=[CashFlow.Earning, CashFlow.Expense],
        var_name="cash flow",
        value_name="euro",
    )
    group_df = group_df[group_df["euro"] > 0]
    return px.bar(
        group_df,
        x=granularity.lower()
        if granularity == Granularity.WEEK
        else group_df[Granularity.MONTH.lower()].dt.strftime("%B %Y"),
        y="euro",
        color="cash flow",
        barmode="group",
        height=height,
        title="Earnings vs Expenses",
    )


@st.cache_data
def bar(
    df: pd.DataFrame,
    granularity: Granularity,
    level: CategoryLevel,
    flow: CashFlow,
    height: int,
):
    group_df = (
        df[~pd.isna(df[flow])].groupby([granularity.lower(), level]).agg({flow: "sum"})
    ).reset_index()
    group_df = group_df[group_df[flow] > 0]

    title = f"{'Expenses' if flow == CashFlow.Expense else 'Earnings'} by {'Category' if level == CategoryLevel.Large else 'Subcategory'}"

    return px.bar(
        group_df,
        x=granularity.lower()
        if granularity == Granularity.WEEK
        else group_df[Granularity.MONTH.lower()].dt.strftime("%B %Y"),
        y=flow,
        color=level,
        title=title,
        height=height,
    )


@st.cache_data
def flow_pie(df: pd.DataFrame, flow: CashFlow, level: CategoryLevel):
    group_df = df.groupby([level])[flow].sum().reset_index()
    group_df = group_df[group_df[flow] > 0]

    title = f"{flow.capitalize()} Pie for {'Category' if level == CategoryLevel.Large else 'Subcategory'}"
    fig = px.pie(group_df, values=flow, names=level, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


@st.cache_data
def operation_pie(df: pd.DataFrame, flow: CashFlow):
    group_df = df.groupby(["operation"])[flow].sum().reset_index()
    group_df = group_df[group_df[flow] > 0]
    title = f"{flow.capitalize()} Pie for Operations"
    fig = px.pie(group_df, values=flow, names="operation", title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


@st.cache_data
def profit_loss_line(df: pd.DataFrame, granularity: str, height: int) -> go.Figure:
    group_df = (
        df.groupby([granularity.lower()])
        .agg({CashFlow.Earning: "sum", CashFlow.Expense: "sum"})
        .reset_index()
    )
    group_df = group_df.fillna(0)
    group_df["profit / loss"] = (
        group_df[CashFlow.Earning].cumsum() - group_df[CashFlow.Expense].cumsum()
    )

    # Separate data into positive and negative earnings
    data_pos = group_df.copy()
    data_neg = group_df.copy()
    data_pos["profit / loss"] = np.where(
        data_pos["profit / loss"] > 0, data_pos["profit / loss"], 0
    )
    data_neg["profit / loss"] = np.where(
        data_neg["profit / loss"] < 0, data_neg["profit / loss"], 0
    )

    # Create Plotly graph objects
    trace_pos = go.Scatter(
        x=granularity.lower()
        if granularity == Granularity.WEEK
        else group_df[Granularity.MONTH.lower()].dt.strftime("%B %Y"),
        y=data_pos["profit / loss"],
        mode="lines+markers",
        fill="tozeroy",
        name="Earnings",
    )
    trace_neg = go.Scatter(
        x=granularity.lower()
        if granularity == Granularity.WEEK
        else group_df[Granularity.MONTH.lower()].dt.strftime("%B %Y"),
        y=data_neg["profit / loss"],
        mode="lines+markers",
        fill="tozeroy",
        name="Losses",
    )

    # Create a layout and return a go.Figure
    layout = go.Layout(
        title="Profit / Loss Over Time",
        xaxis_title=granularity.capitalize(),
        yaxis_title="Profit / Loss",
        height=height,
    )

    return go.Figure(data=[trace_pos, trace_neg], layout=layout)


@st.cache_data
def flow_heatmap(
    df: pd.DataFrame,
    granularity: Granularity,
    flow: CashFlow,
    level: CategoryLevel,
    height: int,
):
    heatmap_df = df[~pd.isna(df[flow])].pivot_table(
        index=level, columns=granularity.lower(), values=flow, aggfunc="sum"
    )

    heatmap_df.fillna(0, inplace=True)

    title = f"{'Expenses' if flow == CashFlow.Expense else 'Earnings'} Heatmap by {'Category' if level == CategoryLevel.Large else 'Subcategory'}"

    fig = px.imshow(
        heatmap_df,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        labels=dict(color="euro"),
        title=title,
        height=height,
    )
    return fig


import plotly.express as px


@st.cache_data
def top_k_vendor_transactions(df: pd.DataFrame, k: int, height: int) -> go.Figure:
    plot_df = df.copy()
    plot_df.loc[:, "description"] = plot_df["description"].apply(
        lambda s: s[:25] + ".." if len(s) > 25 else s
    )
    plot_df = plot_df.groupby(["description", "operation"]).size().reset_index()
    plot_df.rename(columns={0: "transactions", "description": "vendor"}, inplace=True)
    plot_df.sort_values(by="transactions", ascending=False, inplace=True)
    plot_df = plot_df[:k]

    fig = px.bar(
        plot_df,
        x="transactions",
        y="vendor",
        color="operation",
        title=f"Top {k} Transactors",
        height=height,
    )
    return fig


@st.cache_data
def top_k_vendor_flow(
    df: pd.DataFrame, k: int, flow: CashFlow, height: int, operation: str | None = None
) -> go.Figure:
    plot_df = df.copy()

    if operation is not None:
        plot_df = plot_df[plot_df["operation"] == operation]

    plot_df.loc[:, "description"] = plot_df["description"].apply(
        lambda s: s[:25] + ".." if len(s) > 25 else s
    )
    plot_df = (
        plot_df[~plot_df[flow].isna()]
        .groupby(["description", "operation"])
        .agg({flow: "sum"})
        .reset_index()
    )
    plot_df.rename(columns={"description": "vendor"}, inplace=True)
    plot_df.sort_values(by=flow, ascending=False, inplace=True)

    fig = px.bar(
        plot_df[:k],
        x=flow,
        y="vendor",
        color="operation" if not operation else None,
        title=f'Top {k} {"Vendors" if flow == CashFlow.Expense else "Payers"}{" - "+ operation if operation else ""}',
        height=height,
    )
    return fig
