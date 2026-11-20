import pandas as pd
from solution import add_virtual_column


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Porządkujemy nazwy kolumn: małe litery, bez spacji na brzegach, spacje zamieniamy na '_'
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # 2. Usuwamy powtórzony nagłówek w środku pliku oraz wiersz podsumowania TOTAL
    df = df[df["order_id"] != "Order ID"]
    df = df[df["order_id"] != "TOTAL"]

    # 3. Usuwamy dokładne duplikaty wierszy
    df = df.drop_duplicates()

    # 4. Porządkujemy nazwy regionów (usuwamy spacje i robimy pierwszą literę wielką)
    df["region"] = df["region"].str.strip().str.title()

    # 5. Naprawiamy kolumnę quantity (usuwamy spacje ze środka liczb, np. '1 762' -> 1762)
    df["quantity"] = df["quantity"].astype(str).str.replace(" ", "", regex=False).astype(int)

    # 6. Naprawiamy kolumnę unit_price (zamieniamy przecinki na kropki i zmieniamy na liczby)
    df["unit_price"] = df["unit_price"].astype(str).str.replace(",", ".", regex=False)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # 7. Uzupełniamy brakujące ceny na podstawie ceny tego samego produktu z innych wierszy
    price_per_product = df.groupby("product")["unit_price"].transform("first")
    df["unit_price"] = df["unit_price"].fillna(price_per_product)

    # 8. Puste rabaty zamieniamy na 0.0
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)

    return df.reset_index(drop=True)


def run_pipeline(input_path: str = "sales.csv", output_path: str = "revenue_by_region.csv") -> pd.DataFrame:
    # Wczytujemy plik jako tekst (dtype=str), żeby samemu bezpiecznie wyczyścić liczby
    df_raw = pd.read_csv(input_path, dtype=str)

    # Czyścimy dane
    df_clean = clean_sales_data(df_raw)

    # Dodajemy kolumnę revenue za pomocą Twojej funkcji z Etapu 1
    df_with_revenue = add_virtual_column(
        df_clean, "quantity * unit_price - discount", "revenue"
    )

    # Sumujemy przychód dla każdego regionu i zaokrąglamy do 2 miejsc po przecinku
    revenue_by_region = (
        df_with_revenue.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("region")
    )
    revenue_by_region["revenue"] = revenue_by_region["revenue"].round(2)

    # Zapisujemy gotowy plik CSV (bez kolumny z numerami wierszy 0, 1, 2...)
    revenue_by_region.to_csv(output_path, index=False)
    return revenue_by_region


if __name__ == "__main__":
    run_pipeline()