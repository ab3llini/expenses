import metrics
import ops
import plotly.io as pio
import plots
import sidebar
import streamlit as st
from models import CashFlow, CategoryLevel


def main():
    st.set_page_config(layout="wide")
    st.title("Transaction Dashboard")

    pio.templates.default = "plotly"

    uploaded_file, date_from, date_to, granularity, plot_height = sidebar.render()

    df = ops.load_df(uploaded_file)
    if df is None:
        return

    df = ops.transform(df)
    # df = ops.normalize(df)
    df = ops.focus(df, date_from, date_to)

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
