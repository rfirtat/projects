import pandas as pd
import re

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def validate_duplicates(df):

    duplicates = df.duplicated(subset="transaction_id")

    print("Duplicate rows removed:", duplicates.sum())

    df = df.drop_duplicates(subset="transaction_id")

    return df


def validate_quantity(df):

    intial_row_count = len(df)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df = df[df["quantity"] > 0]

    resulting_row_count = len(df)
    print("Invalid quantities removed:", intial_row_count-resulting_row_count)

    return df


def validate_email(df):

    intial_row_count = len(df)

    df = df[df["email"].str.match(EMAIL_PATTERN)]

    resulting_row_count = len(df)
    print("Invalid emails removed:", intial_row_count-resulting_row_count)

    return df


def validate_dates(df):

    intial_row_count = len(df)

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    df = df[~df["order_date"].isna()]

    resulting_row_count = len(df)
    print("Invalid dates removed:", intial_row_count-resulting_row_count)

    return df


def main():

    df = pd.read_csv("data/raw_sales_data.csv")

    print("Rows processed:", len(df))
    print("\nValidation Summary")
    print("-------------------")

    df = validate_duplicates(df)
    df = validate_quantity(df)
    df = validate_email(df)
    df = validate_dates(df)

    df.to_csv("output/cleaned_sales_data.csv", index=False)


if __name__ == "__main__":
    main()

