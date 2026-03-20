import pandas as pd
import logging

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"

STATE_MAP = {
    "CALIFORNIA": "CA",
    "TEXAS": "TX",
    "NEVADA": "NV"
}

VALID_STATES = set(STATE_MAP.values())

logging.basicConfig(
    filename="logs/errors.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def validate_duplicates(df):

    duplicates = df.duplicated(subset="transaction_id")

    for tid in set(df["transaction_id"][duplicates]):
        logging.info(f"Duplicate record removed | transaction_id={tid}")

    print(f"Duplicate rows removed: {duplicates.sum()}")

    df = df.drop_duplicates(subset="transaction_id", keep="first")

    return df


def validate_quantity(df):

    initial_row_count = len(df)

    invalid_rows = df[pd.to_numeric(df["quantity"], errors="coerce").isna()]

    for quantity, tid in zip(invalid_rows["quantity"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid quantity removed | quantity={quantity} | transaction_id={tid}")

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df = df[df["quantity"] > 0]

    removed_rows = initial_row_count - len(df)
    print(f"Invalid quantities removed: {removed_rows}")

    return df


def validate_price(df):

    initial_row_count = len(df)

    invalid_rows = df[pd.to_numeric(df["price"], errors="coerce").isna()]

    for price, tid in zip(invalid_rows["price"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid price removed | price={price} | transaction_id={tid}")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df = df[df["price"] > 0]

    removed_rows = initial_row_count - len(df)
    print(f"Invalid prices removed: {removed_rows}")

    return df


def validate_email(df):

    initial_row_count = len(df)

    invalid_rows = df[~df["email"].str.match(EMAIL_PATTERN)]

    for email, tid in zip(invalid_rows["email"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid email removed | email={email} | transaction_id={tid}")

    df = df[df["email"].str.match(EMAIL_PATTERN)]

    removed_rows = initial_row_count - len(df)
    print(f"Invalid email removed: {removed_rows}")

    return df


def validate_dates(df):

    initial_row_count = len(df)

    invalid_rows = df[pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce").isna()]

    for date, tid in zip(invalid_rows["order_date"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid date removed | date={date} | transaction_id={tid}")

    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    
    df = df[df["order_date"].notna()]

    removed_rows = initial_row_count - len(df)
    print(f"Invalid dates removed: {removed_rows}")

    return df


def validate_product(df, products_pd):

    initial_row_count = len(df)

    valid_products = set(products_pd["product"].str.strip().str.lower())

    invalid_rows = df[~df["product"].str.strip().str.lower().isin(valid_products)]

    for product, tid in zip(invalid_rows["product"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid product removed | product={product} | transaction_id={tid}")

    df["product"] = df["product"].str.strip().str.lower()
    df = df[df["product"].isin(valid_products)]

    removed_rows = initial_row_count - len(df)
    print(f"Invalid products removed: {removed_rows}")

    return df


def standardize_state(df):

    initial_row_count = len(df)

    invalid_rows = df[~df["state"].str.strip().str.upper().replace(STATE_MAP).isin(VALID_STATES)]

    for state, tid in zip(invalid_rows["state"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid state removed | state={state} | transaction_id={tid}")

    df["state"] = df["state"].str.strip().str.upper().replace(STATE_MAP)
    df = df[df["state"].isin(VALID_STATES)]

    removed_rows = initial_row_count - len(df)
    print(f"Invalid states removed: {removed_rows}")

    return df


def main():

    print("\nStarting validation pipeline:\n")

    df = pd.read_csv("data/raw_sales_data.csv")
    products_pd = pd.read_csv("data/valid_products.csv")

    print("Rows processed:", len(df))
    print("\nValidation Summary")
    print("-------------------")

    df = validate_duplicates(df)
    df = validate_quantity(df)
    df = validate_price(df)
    df = validate_product(df, products_pd)
    df = validate_email(df)
    df = validate_dates(df)
    df = standardize_state(df)

    df.to_csv("output/cleaned_sales_data.csv", index=False)

    print("\nClean data written to output/cleaned_sales_data.csv\n")


if __name__ == "__main__":
    main()

