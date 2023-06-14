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
        {CashFlow.Earning.value: "sum", CashFlow.Expense.value: "sum"}
    )
    group_df = group_df.reset_index().melt(
        id_vars=granularity.lower(),
        value_vars=[CashFlow.Earning.value, CashFlow.Expense.value],
        var_name="cash flow",
        value_name="euro",
    )
    group_df = group_df[group_df["euro"] > 0]
    return px.bar(
        group_df,
        x=granularity.lower(),
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
        df[~pd.isna(df[flow.value])]
        .groupby([granularity.lower(), level.value])
        .agg({flow.value: "sum"})
    )
    group_df = group_df[group_df[flow.value] > 0]

    title = f"{'Expenses' if flow == CashFlow.Expense else 'Earnings'} by {'Category' if level == CategoryLevel.Large else 'Subcategory'}"

    return px.bar(
        group_df.reset_index(),
        x=granularity.lower(),
        y=flow.value,
        color=level.value,
        title=title,
        height=height,
    )


@st.cache_data
def flow_pie(df: pd.DataFrame, flow: CashFlow, level: CategoryLevel):
    group_df = df.groupby([level.value])[flow.value].sum().reset_index()
    group_df = group_df[group_df[flow.value] > 0]

    title = f"{flow.value.capitalize()} Pie for {'Category' if level == CategoryLevel.Large else 'Subcategory'}"
    fig = px.pie(group_df, values=flow.value, names=level.value, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


@st.cache_data
def operation_pie(df: pd.DataFrame, flow: CashFlow):
    group_df = df.groupby(["operation"])[flow.value].sum().reset_index()
    group_df = group_df[group_df[flow.value] > 0]
    title = f"{flow.value.capitalize()} Pie for Operations"
    fig = px.pie(group_df, values=flow.value, names="operation", title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


@st.cache_data
def profit_loss_line(df: pd.DataFrame, granularity: str, height: int) -> go.Figure:
    group_df = (
        df.groupby([granularity.lower()])
        .agg({CashFlow.Earning.value: "sum", CashFlow.Expense.value: "sum"})
        .reset_index()
    )
    group_df = group_df.fillna(0)
    group_df["profit / loss"] = (
        group_df[CashFlow.Earning.value].cumsum()
        - group_df[CashFlow.Expense.value].cumsum()
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
        x=data_pos[granularity.lower()],
        y=data_pos["profit / loss"],
        mode="lines+markers",
        fill="tozeroy",
        name="Earnings",
    )
    trace_neg = go.Scatter(
        x=data_neg[granularity.lower()],
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
    heatmap_df = df[~pd.isna(df[flow.value])].pivot_table(
        index=level.value, columns=granularity.lower(), values=flow.value, aggfunc="sum"
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
