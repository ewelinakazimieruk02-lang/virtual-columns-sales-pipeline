import pandas as pd
from pipeline import clean_sales_data, run_pipeline


def test_clean_sales_data_fixes_issues():
    raw = pd.DataFrame({
        "Order ID": ["SO-1", "SO-1", "Order ID", "SO-2", "TOTAL"],
        "Region": [" south ", " south ", "Region", "EAST", ""],
        "Product": ["Mouse", "Mouse", "Product", "Mouse", ""],
        "Quantity ": ["1 000", "1 000", "Quantity ", "-2", "998"],
        "Unit Price": ["29,50", "29,50", "Unit Price", "", ""],
        "Discount": ["", "", "Discount", "5.00", "5.00"],
        "Order Date": ["2026-01-01", "2026-01-01", "Order Date", "2026-01-02", ""],
    })

    clean = clean_sales_data(raw)

    assert len(clean) == 2
    assert list(clean["region"]) == ["South", "East"]
    assert list(clean["quantity"]) == [1000, -2]
    assert list(clean["unit_price"]) == [29.5, 29.5]
    assert list(clean["discount"]) == [0.0, 5.0]


def test_run_pipeline_returns_five_regions():
    result = run_pipeline()
    assert list(result["region"]) == ["Central", "East", "North", "South", "West"]
    assert result["revenue"].isna().sum() == 0