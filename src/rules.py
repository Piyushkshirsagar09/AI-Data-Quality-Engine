import pandas as pd
import re


def check_numeric_range(df, column, minimum=None, maximum=None):
    """
    Check whether numeric values are within an allowed range.
    """

    if column not in df.columns:
        return {
            "Rule": f"{column} numeric range",
            "Status": "FAILED",
            "Violations": 0,
            "Message": "Column not found."
        }

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    violations = pd.Series(False, index=df.index)

    if minimum is not None:
        violations = violations | (series < minimum)

    if maximum is not None:
        violations = violations | (series > maximum)

    count = int(violations.sum())

    return {
        "Rule": f"{column} must be within valid range",
        "Status": "PASSED" if count == 0 else "FAILED",
        "Violations": count,
        "Message": (
            "All values are valid."
            if count == 0
            else f"{count} values are outside the allowed range."
        )
    }


def check_unique(df, column):
    """
    Check whether values in a column are unique.
    """

    if column not in df.columns:
        return {
            "Rule": f"{column} uniqueness",
            "Status": "FAILED",
            "Violations": 0,
            "Message": "Column not found."
        }

    duplicate_count = int(
        df[column].duplicated().sum()
    )

    return {
        "Rule": f"{column} must be unique",
        "Status": "PASSED" if duplicate_count == 0 else "FAILED",
        "Violations": duplicate_count,
        "Message": (
            "All values are unique."
            if duplicate_count == 0
            else f"{duplicate_count} duplicate values found."
        )
    }


def check_email_format(df, column):
    """
    Check email values using a basic email format rule.
    """

    if column not in df.columns:
        return {
            "Rule": f"{column} email format",
            "Status": "FAILED",
            "Violations": 0,
            "Message": "Column not found."
        }

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    values = df[column].dropna().astype(str)

    invalid_count = int(
        (~values.str.match(pattern)).sum()
    )

    return {
        "Rule": f"{column} must contain valid emails",
        "Status": "PASSED" if invalid_count == 0 else "FAILED",
        "Violations": invalid_count,
        "Message": (
            "All email values appear valid."
            if invalid_count == 0
            else f"{invalid_count} invalid email values found."
        )
    }


def run_default_rules(df):
    """
    Run automatically selected rules based on
    available column names and data types.
    """

    results = []

    # Check ID-like columns for uniqueness
    for column in df.columns:

        column_name = str(column).lower()

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.endswith("id")
        ):

            results.append(
                check_unique(
                    df,
                    column
                )
            )

    # Check likely age columns
    for column in df.columns:

        column_name = str(column).lower()

        if column_name == "age" or "age" in column_name:

            if pd.api.types.is_numeric_dtype(df[column]):

                results.append(
                    check_numeric_range(
                        df,
                        column,
                        minimum=0,
                        maximum=120
                    )
                )

    # Check likely salary columns
    for column in df.columns:

        column_name = str(column).lower()

        if "salary" in column_name:

            if pd.api.types.is_numeric_dtype(df[column]):

                results.append(
                    check_numeric_range(
                        df,
                        column,
                        minimum=0
                    )
                )

    # Check likely email columns
    for column in df.columns:

        column_name = str(column).lower()

        if "email" in column_name:

            results.append(
                check_email_format(
                    df,
                    column
                )
            )

    return results