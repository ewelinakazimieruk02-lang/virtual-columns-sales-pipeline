import pandas as pd

ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"


def is_valid_column_name(name):
    if type(name) != str or name == "":
        return False
    for char in name:
        if char not in ALLOWED_CHARS:
            return False
    return True


def add_virtual_column(
    df: pd.DataFrame, role: str, new_column: str
) -> pd.DataFrame:
    if not is_valid_column_name(new_column):
        return pd.DataFrame([])

    for col in df.columns:
        if not is_valid_column_name(col):
            return pd.DataFrame([])

    if type(role) != str:
        return pd.DataFrame([])
    role_with_spaces = role.replace("+", " + ").replace("-", " - ").replace("*", " * ")
    parts = role_with_spaces.split()

    if len(parts) == 0:
        return pd.DataFrame([])

    expect_column = True
    for part in parts:
        if expect_column:
            if part not in df.columns:
                return pd.DataFrame([])
            expect_column = False
        else:
            if part not in ["+", "-", "*"]:
                return pd.DataFrame([])
            expect_column = True

    if expect_column:
        return pd.DataFrame([])

    result = df.copy()
    result[new_column] = result.eval(role)
    return result