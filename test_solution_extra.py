import pandas as pd
from solution import add_virtual_column


def test_multiple_operations_and_order():
    df = pd.DataFrame({
        "quantity": [2, 3],
        "unit_price": [10.0, 5.0],
        "discount": [1.5, 0.0],
    })
    result = add_virtual_column(df, "quantity * unit_price - discount", "revenue")
    assert list(result["revenue"]) == [18.5, 15.0]


def test_original_dataframe_is_not_modified():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    add_virtual_column(df, "a + b", "c")
    assert list(df.columns) == ["a", "b"]


def test_invalid_existing_column_name():
    df = pd.DataFrame({"col_1": [1, 2], "col_two": [3, 4]})
    result = add_virtual_column(df, "col_two + col_two", "result")
    assert result.empty


def test_division_is_not_allowed():
    df = pd.DataFrame({"a": [10, 20], "b": [2, 5]})
    result = add_virtual_column(df, "a / b", "result")
    assert result.empty


def test_empty_or_incomplete_role():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    assert add_virtual_column(df, "", "result").empty
    assert add_virtual_column(df, "a + ", "result").empty