from enum import StrEnum


class Granularity(StrEnum):
    MONTH = "Month"
    WEEK = "Week"


class CategoryLevel(StrEnum):
    Large = "category"
    Small = "subcategory"


class CashFlow(StrEnum):
    Expense = "expense"
    Earning = "earning"
