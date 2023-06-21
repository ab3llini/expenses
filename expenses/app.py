from datetime import date, datetime

import metrics
import ops
import pandas as pd
import plotly.io as pio
import plots
import sidebar
import streamlit as st
from models import CashFlow, CategoryLevel, Granularity


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
            ops.choices(df, CategoryLevel.Large),
            ops.choices(df, CategoryLevel.Large),
        )

        subcategories = st.multiselect(
            "Aggregate data only on the following subcategories",
            ops.choices(df, CategoryLevel.Small),
            ops.choices(df, CategoryLevel.Small),
        )

        operations = st.multiselect(
            "Aggregate data only on the following operations",
            ops.choices(df, "operation"),
            ops.choices(df, "operation"),
        )

    return date_from, date_to, granularity, categories, subcategories, operations

# wrute the same function from above, but improved
# def filters(


def main():
    st.set_page_config(layout="wide", page_title="Transaction Dashboard")
    st.title("Transaction Dashboard")

    pio.templates.default = "plotly"

    uploaded_file, plot_height = sidebar.render()

    st.divider()

    df = ops.load_df(uploaded_file)
    if df is None:
        return

    df = ops.transform(df)

    date_from, date_to, granularity, categories, subcategories, operations = filters(df)

    df = ops.within_period(df, date_from, date_to)
    df = ops.filter_choices(df, CategoryLevel.Large, categories)
    df = ops.filter_choices(df, CategoryLevel.Small, subcategories)
    df = ops.filter_choices(df, "operation", operations)

    tot_earnings, tot_expenses, tot_income = st.columns(3)

    tot_earnings.metric("Total Earnings", f"{metrics.total(df, CashFlow.Earning)} Euro")
    tot_expenses.metric("Total Expenses", f"{metrics.total(df, CashFlow.Expense)} Euro")
    tot_income.metric(
        "Total Savings / Losses",
        f"{metrics.total(df, CashFlow.Earning) - metrics.total(df, CashFlow.Expense)} Euro",
    )

    st.plotly_chart(
        plots.profit_loss_line(df, granularity, plot_height), use_container_width=True
    )
    st.plotly_chart(
        plots.earnings_expenses_bar(df, granularity, plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.bar(df, granularity, CategoryLevel.Large, CashFlow.Expense, plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.bar(df, granularity, CategoryLevel.Small, CashFlow.Expense, plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.bar(df, granularity, CategoryLevel.Large, CashFlow.Earning, plot_height),
        use_container_width=True,
    )

    cat_expenses_pie, sub_cat_earnings_pie = st.columns(2)
    cat_expenses_pie.plotly_chart(
        plots.flow_pie(df, CashFlow.Expense, CategoryLevel.Large),
        use_container_width=True,
    )
    sub_cat_earnings_pie.plotly_chart(
        plots.flow_pie(df, CashFlow.Expense, CategoryLevel.Small),
        use_container_width=True,
    )

    operation_expenses_pie, cat_earnings_pie = st.columns(2)
    operation_expenses_pie.plotly_chart(
        plots.operation_pie(df, CashFlow.Expense), use_container_width=True
    )
    cat_earnings_pie.plotly_chart(
        plots.flow_pie(df, CashFlow.Earning, CategoryLevel.Large),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.top_k_vendor_transactions(df, k=20, height=plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.top_k_vendor_flow(df, k=20, flow=CashFlow.Expense, height=plot_height),
        use_container_width=True,
    )
    st.plotly_chart(
        plots.top_k_vendor_flow(
            df,
            k=20,
            flow=CashFlow.Expense,
            operation="Pagamento POS",
            height=plot_height,
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.top_k_vendor_flow(
            df,
            k=20,
            flow=CashFlow.Expense,
            operation="Pagamenti OnLine",
            height=plot_height,
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.flow_heatmap(
            df, granularity, CashFlow.Expense, CategoryLevel.Large, plot_height
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        plots.flow_heatmap(
            df, granularity, CashFlow.Expense, CategoryLevel.Small, plot_height
        ),
        use_container_width=True,
    )

    st.subheader("Transactions")

    df





if __name__ == "__main__":
    main()
