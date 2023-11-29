import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go
import streamlit as st
from models import Granularity


@st.cache_data
def earnings_expenses_bar(
    df: pd.DataFrame, granularity: Granularity, height: int
) -> go.Figure | None:
    if not len(df):
        return None

    group_df = (
        df.groupby([granularity.lower(), "kind"]).agg({"euro": "sum"}).reset_index()
    )
    group_df = group_df.sort_values(by=[granularity.lower(), "kind"], ascending=True)
    plot = px.bar(
        group_df,
        x=granularity.lower(),
        y="euro",
        color="kind",
        barmode="group",
        height=height,
        title="Earnings vs Expenses",
    )

    return plot


@st.cache_data
def bar(
    df: pd.DataFrame,
    granularity: Granularity,
    level: str,
    kind: str,
    height: int,
) -> go.Figure | None:
    if not len(df):
        return None

    group_df = (
        df[df["kind"] == kind]
        .groupby([granularity.lower(), level])
        .agg({"euro": "sum"})
    ).reset_index()

    group_df = group_df.sort_values(by=granularity.lower(), ascending=True)
    title = f"{kind.capitalize()}s by {level.capitalize()}"

    return px.bar(
        group_df,
        x=granularity.lower(),
        y="euro",
        color=level,
        title=title,
        height=height,
    )


@st.cache_data
def pie(df: pd.DataFrame, kind: str, level: str):
    group_df = (
        df[df["kind"] == kind].groupby([level]).agg({"euro": "sum"}).reset_index()
    )

    title = f"{kind.capitalize()} Pie for {'Category' if level == 'category' else 'Subcategory'}"
    fig = px.pie(group_df, values="euro", names=level, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


@st.cache_data
def operation_pie(df: pd.DataFrame, kind: str):
    group_df = (
        df[df["kind"] == kind].groupby(["operation"]).agg({"euro": "sum"}).reset_index()
    )
    group_df = group_df[group_df["euro"] > 0]
    title = f"{kind.capitalize()} Pie for Operations"
    fig = px.pie(group_df, values="euro", names="operation", title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


@st.cache_data
def profit_loss_line(
    df: pd.DataFrame, granularity: Granularity, height: int
) -> go.Figure | None:
    if not len(df):
        return None

    group_df = (
        df.groupby([granularity.lower(), "kind"]).agg({"euro": "sum"}).unstack("kind")
    )
    group_df = group_df.fillna(0)
    group_df.columns = group_df.columns.droplevel()
    group_df["profit / loss"] = (
        group_df["earning"].cumsum() - group_df["expense"].cumsum()
    )
    group_df = group_df.reset_index()

    line = go.Scatter(
        x=group_df[Granularity.WEEK.lower()]
        if granularity == Granularity.WEEK
        else group_df[Granularity.MONTH.lower()].dt.strftime("%B %Y"),
        y=group_df["profit / loss"],
        name="Line",
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(101, 110, 242, 0.2)",
        line=dict(color="rgba(101, 110, 242, 0.3)"),
        showlegend=False,
    )
    bars = go.Bar(
        x=group_df[Granularity.WEEK.lower()]
        if granularity == Granularity.WEEK
        else group_df[Granularity.MONTH.lower()].dt.strftime("%B %Y"),
        y=group_df["profit / loss"],
        name="Euros",
        # Remove legend
        showlegend=False,
    )

    # Create a layout and return a go.Figure
    layout = go.Layout(
        title="Profit / Loss Over Time",
        xaxis_title=granularity.capitalize(),
        yaxis_title="Profit / Loss",
        height=height,
    )

    return go.Figure(data=[bars, line], layout=layout)


@st.cache_data
def flow_heatmap(
    df: pd.DataFrame,
    granularity: Granularity,
    kind: str,
    level: str,
    height: int,
):
    heatmap_df = df[df["kind"] == kind].pivot_table(
        index=level, columns=granularity.lower(), values="euro", aggfunc="sum"
    )

    heatmap_df.fillna(0, inplace=True)

    title = f"{'Expenses' if kind == 'expense' else 'Earnings'} Heatmap by {'Category' if level == 'category' else 'Subcategory'}"

    fig = px.imshow(
        heatmap_df,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        labels=dict(color="euro"),
        title=title,
        height=height,
    )
    return fig


@st.cache_data
def top_k_transactors(df: pd.DataFrame, k: int, height: int) -> go.Figure | None:
    """
    This function is used to plot the top k transactors.
    """
    plot_df = df.copy()
    plot_df.loc[:, "description"] = plot_df["description"].apply(
        lambda s: s[:25] + ".." if len(s) > 25 else s
    )
    plot_df = plot_df.groupby(["description", "operation"]).size().reset_index()
    plot_df.rename(columns={0: "transactions", "description": "vendor"}, inplace=True)
    plot_df.sort_values(by="transactions", ascending=True, inplace=True)

    scale = px.colors.sequential.Plotly3

    # Same plot as above but I want to render based on log and on hover i want to show the actual value
    fig = px.bar(
        plot_df.tail(k),
        x="transactions",
        y="vendor",
        title=f"Top {k} Transactors",
        height=height,
    )

    return fig


@st.cache_data
def top_k_euros(
    df: pd.DataFrame, k: int, kind: str, height: int, operation: str | None = None
) -> go.Figure | None:
    """
    This function is used to plot the top k vendors by euros spent or earned.
    """
    plot_df = df.copy()

    if operation is not None:
        plot_df = plot_df[plot_df["operation"] == operation]

    plot_df.loc[:, "description"] = plot_df["description"].apply(
        lambda s: s[:25] + ".." if len(s) > 25 else s
    )
    plot_df = (
        plot_df[plot_df["kind"] == kind]
        .groupby(["description", "operation"])
        .agg({"euro": "sum"})
        .reset_index()
    )
    plot_df.rename(columns={"description": "vendor"}, inplace=True)
    plot_df.sort_values(by="euro", ascending=True, inplace=True)
    plot_df["log_euro"] = np.log(plot_df["euro"])

    fig = px.bar(
        plot_df.tail(k),
        x="log_euro",
        y="vendor",
        title=f'{"Outbound" if kind == "expense" else "Inbound"} Money - Top {k} {" - " + operation if operation else ""} (Log Scale)',
        height=height,
        hover_data=["euro"],
    )
    return fig
