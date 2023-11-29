from datetime import date, datetime

import metrics
import ops
import pandas as pd
import plotly.io as pio
import plots
import sidebar
import streamlit as st
from models import Granularity


def filters(
    df: pd.DataFrame,
) -> tuple[date, date, Granularity, list[str], list[str], list[str]]:
    st.subheader("Filters")

    from_col, to_col, granularity_col = st.columns(3)
    date_from = from_col.date_input(
        "Date From",
        help="Date from which data will be rendered",
        value=ops.earliest_date(df),
    )
    date_to = to_col.date_input(
        "Date To", help="Date to which data will be rendered", value=ops.latest_date(df)
    )

    # Granularity selector
    granularity = Granularity(
        granularity_col.selectbox("Granularity", [grain for grain in Granularity])
    )

    with st.expander("Extended Filters"):
        categories = st.multiselect(
            "Aggregate data only on the following categories",
            ops.choices(df, "category"),
            ops.choices(df, "category"),
        )

        subcategories = st.multiselect(
            "Aggregate data only on the following subcategories",
            ops.choices(df, "subcategory"),
            ops.choices(df, "subcategory"),
        )

        operations = st.multiselect(
            "Aggregate data only on the following operations",
            ops.choices(df, "operation"),
            ops.choices(df, "operation"),
        )

    return date_from, date_to, granularity, categories, subcategories, operations


def main():
    st.set_page_config(layout="wide", page_title="Transaction Dashboard")
    st.title("Transaction Dashboard")

    pio.templates.default = "plotly"

    df, plot_height = sidebar.render()

    st.divider()

    if df is None:
        return

    date_from, date_to, granularity, categories, subcategories, operations = filters(df)

    df = ops.within_period(df, date_from, date_to)

    if not len(df):
        return

    df = ops.filter_choices(df, "category", categories)
    df = ops.filter_choices(df, "subcategory", subcategories)
    df = ops.filter_choices(df, "operation", operations)

    tot_earnings, tot_expenses, tot_income = st.columns(3)

    tot_earnings.metric("Total Earnings", f'{metrics.total(df, "earning")} Euro')
    tot_expenses.metric("Total Expenses", f'{metrics.total(df, "expense")} Euro')
    tot_income.metric(
        "Total Savings / Losses",
        f'{metrics.total(df, "earning") - metrics.total(df, "expense")} Euro',
    )

    st.plotly_chart(
        plots.profit_loss_line(df, granularity, plot_height), use_container_width=True
    )
    st.plotly_chart(
        plots.earnings_expenses_bar(df, granularity, plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.bar(df, granularity, "category", "expense", plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.bar(df, granularity, "subcategory", "expense", plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.bar(df, granularity, "category", "earning", plot_height),
        use_container_width=True,
    )

    cat_expenses_pie, sub_cat_earnings_pie = st.columns(2)
    cat_expenses_pie.plotly_chart(
        plots.pie(df, "expense", "category"),
        use_container_width=True,
    )
    sub_cat_earnings_pie.plotly_chart(
        plots.pie(df, "expense", "subcategory"),
        use_container_width=True,
    )

    operation_expenses_pie, cat_earnings_pie = st.columns(2)
    operation_expenses_pie.plotly_chart(
        plots.operation_pie(df, "expense"), use_container_width=True
    )
    cat_earnings_pie.plotly_chart(
        plots.pie(df, "earning", "category"),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.top_k_transactors(df, k=20, height=plot_height),
        use_container_width=True,
    )

    inbound, outbound = st.columns(2)

    inbound.plotly_chart(
        plots.top_k_euros(df, k=20, kind="expense", height=plot_height),
        use_container_width=True,
    )

    outbound.plotly_chart(
        plots.top_k_euros(df, k=20, kind="earning", height=plot_height),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.flow_heatmap(df, granularity, "expense", "category", plot_height),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.flow_heatmap(df, granularity, "expense", "subcategory", plot_height),
        use_container_width=True,
    )

    st.subheader("Transactions")

    df


if __name__ == "__main__":
    main()
