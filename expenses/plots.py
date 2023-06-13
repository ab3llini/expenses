from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from expenses.models import Granularity, CategoryLevel, CashFlow


@st.cache_data
def earnings_expenses_bar(
        df: pd.DataFrame, granularity: Granularity, height: int
) -> go.Figure:
    group_df = df.groupby([granularity.lower()]).agg({CashFlow.Earning.value: "sum", CashFlow.Expense.value: "sum"})
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
def bar(df: pd.DataFrame, granularity: Granularity, level: CategoryLevel, flow: CashFlow, height: int):
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
        height=height
    )


@st.cache_data
def flow_pie(df: pd.DataFrame, flow: CashFlow, level: CategoryLevel):
    group_df = df.groupby([level.value])[flow.value].sum().reset_index()
    group_df = group_df[group_df[flow.value] > 0]

    title = f"{flow.value.capitalize()} Pie for {'Category' if level == CategoryLevel.Large else 'Subcategory'}"
    fig = px.pie(group_df, values=flow.value, names=level.value, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

@st.cache_data
def operation_pie(df: pd.DataFrame, flow: CashFlow):
    group_df = df.groupby(["operation"])[flow.value].sum().reset_index()
    group_df = group_df[group_df[flow.value] > 0]
    title = f"{flow.value.capitalize()} Pie for Operations"
    fig = px.pie(group_df, values=flow.value, names="operation", title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

@st.cache_data
def cumulative_line(
        df: pd.DataFrame, granularity: Granularity, height: int
) -> go.Figure:
    group_df = df.groupby([granularity.lower()]).agg({CashFlow.Earning.value: "sum", CashFlow.Expense.value: "sum"}).reset_index()
    group_df = group_df.fillna(0)
    group_df['cumulative'] = group_df[CashFlow.Earning.value].cumsum() - group_df[CashFlow.Expense.value].cumsum()
    return px.area(group_df, x=granularity.lower(), y='cumulative', title='Savings Over Time', markers=True, height=height)
