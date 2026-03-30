import pandas as pd
import logging

# Basic email regex pattern for email recognition
EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# Dictionary -> set of valid states (FULL NAME: STATE CODE)
STATE_MAP = {"CALIFORNIA": "CA", "TEXAS": "TX", "NEVADA": "NV"}
VALID_STATES = set(STATE_MAP.values())

# Date format for data standardiation
DATE_FORMAT = "%Y-%m-%d"

# Local file paths for reading/writing data
RAW_DATA_PATH = "data/raw_sales_data.csv"
PRODUCTS_PATH = "data/valid_products.csv"
OUTPUT_PATH = "output/cleaned_sales_data.csv"
LOG_PATH = "logs/errors.log"

# Configure logger name, file path, and message format
logging.basicConfig(
    filename=LOG_PATH, level=logging.INFO, format="%(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)


def validate_duplicates(df):
    # Create series of boolean values from dataframe
    # Duplicate (transaction_id) -> TRUE
    duplicates = df.duplicated(subset="transaction_id")

    # Loop through duplicates to log each duplicate transaction_id
    for tid in df["transaction_id"][duplicates]:
        # Log message showing which record(s) were removed
        logger.info(f"Duplicate record removed | transaction_id={tid}")
    # Print # of duplicates removed
    print(f"Duplicate rows removed: {duplicates.sum()}")

    # Remove duplicates from dataframe
    df = df.drop_duplicates(subset="transaction_id", keep="first")

    return df


def validate_quantity(df):
    # Track initial row count for summary
    initial_row_count = len(df)

    # Pandas function to convert str to int; errors marked as "NaN"
    # Input series of str; returns series of int/NaN
    converted_quantity = pd.to_numeric(df["quantity"], errors="coerce")
    # Rows where quantity is NaN or <= 0
    invalid_rows = df[converted_quantity.isna() | (converted_quantity <= 0)]
    # Loop for logging invalid rows
    for quantity, tid in zip(invalid_rows["quantity"], invalid_rows["transaction_id"]):
        logger.info(
            f"Invalid quantity removed | quantity={quantity} | transaction_id={tid}"
        )

    # Replace "quantity" column with cleaned version
    df["quantity"] = converted_quantity
    df = df[df["quantity"] > 0]

    # Calculate and print # of rows removed
    removed_rows = initial_row_count - len(df)
    print(f"Invalid quantities removed: {removed_rows}")

    return df


def validate_price(df):
    initial_row_count = len(df)

    # Pandas function to convert str to int; errors converted to "NaN"
    # Input series of str; returns series of int/NaN
    converted_price = pd.to_numeric(df["price"], errors="coerce")
    # Rows where price is NaN or <= 0
    invalid_rows = df[converted_price.isna() | (converted_price <= 0)]
    # Loop for logging invalid rows
    for price, tid in zip(invalid_rows["price"], invalid_rows["transaction_id"]):
        logger.info(f"Invalid price removed | price={price} | transaction_id={tid}")

    # Replace "price" column with cleaned version
    df["price"] = converted_price
    df = df[df["price"] > 0]

    # Calculate and print # of rows removed for summary
    removed_rows = initial_row_count - len(df)
    print(f"Invalid prices removed: {removed_rows}")

    return df


def validate_email(df):
    initial_row_count = len(df)

    # Rows containing invalid emails
    # [boolean series] created to filter where regex matches -> FALSE (~TRUE)
    invalid_rows = df[~df["email"].str.match(EMAIL_PATTERN)]
    # Loop for logging invalid rows
    for email, tid in zip(invalid_rows["email"], invalid_rows["transaction_id"]):
        logger.info(f"Invalid email removed | email={email} | transaction_id={tid}")

    # Remove rows containing invalid emails
    df = df[df["email"].str.match(EMAIL_PATTERN)]

    # Calculate and print # of rows removed for summary
    removed_rows = initial_row_count - len(df)
    print(f"Invalid emails removed: {removed_rows}")

    return df


def validate_dates(df):
    initial_row_count = len(df)

    # Rows containing invalid dates
    # [boolean series] created to filter where date format failed to convert (NaT)
    invalid_rows = df[
        pd.to_datetime(df["order_date"], format=DATE_FORMAT, errors="coerce").isna()
    ]
    # Loop for logging invalid rows
    for date, tid in zip(invalid_rows["order_date"], invalid_rows["transaction_id"]):
        logger.info(f"Invalid date removed | date={date} | transaction_id={tid}")

    # Remove rows containing invalid dates
    df["order_date"] = pd.to_datetime(
        df["order_date"], format=DATE_FORMAT, errors="coerce"
    )
    df = df[df["order_date"].notna()]

    # Calculate and print # of rows removed for summary
    removed_rows = initial_row_count - len(df)
    print(f"Invalid dates removed: {removed_rows}")

    return df


def validate_product(df, products_pd):
    initial_row_count = len(df)

    # Create set of standardized valid products for reference
    valid_products = set(products_pd["product"].str.strip().str.lower())
    # Rows containing invalid products
    # [boolean series] created to filter if "product" is not in valid_products
    invalid_rows = df[~df["product"].str.strip().str.lower().isin(valid_products)]
    # Loop for logging invalid rows
    for product, tid in zip(invalid_rows["product"], invalid_rows["transaction_id"]):
        logger.info(
            f"Invalid product removed | product={product} | transaction_id={tid}"
        )
    
    # Remove rows containing invalid products
    df["product"] = df["product"].str.strip().str.lower()
    df = df[df["product"].isin(valid_products)]

    # Calculate and print # of rows removed for summary
    removed_rows = initial_row_count - len(df)
    print(f"Invalid products removed: {removed_rows}")

    return df


def standardize_state(df):
    initial_row_count = len(df)

    # Rows containing invalid states
    # [boolean series] created to filter if "state" is not in VALID_STATES
    invalid_rows = df[
        ~df["state"].str.strip().str.upper().replace(STATE_MAP).isin(VALID_STATES)
    ]
    # Loop for logging invalid rows
    for state, tid in zip(invalid_rows["state"], invalid_rows["transaction_id"]):
        logging.info(f"Invalid state removed | state={state} | transaction_id={tid}")

    # Remove rows containing invalid states
    df["state"] = df["state"].str.strip().str.upper().replace(STATE_MAP)
    df = df[df["state"].isin(VALID_STATES)]
    
    # Calculate and print # of rows removed for summary
    removed_rows = initial_row_count - len(df)
    print(f"Invalid states removed: {removed_rows}")

    return df


def main():

    print("\nStarting validation pipeline:\n")

    # Generate dataframes from csv files
    df = pd.read_csv(RAW_DATA_PATH)
    products_pd = pd.read_csv(PRODUCTS_PATH)

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

    # Output cleaned dataframe to csv
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nClean data written to {OUTPUT_PATH}\n")


if __name__ == "__main__":
    main()
