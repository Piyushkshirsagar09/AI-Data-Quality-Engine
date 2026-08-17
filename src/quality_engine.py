import pandas as pd
import re


def calculate_completeness(df):
    """Measure how many dataset cells contain values."""

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 100.0

    missing_cells = int(df.isnull().sum().sum())

    score = (
        1 - (missing_cells / total_cells)
    ) * 100

    return round(max(0, score), 2)


def calculate_uniqueness(df):
    """Measure how many rows are non-duplicate."""

    total_rows = len(df)

    if total_rows == 0:
        return 100.0

    duplicate_rows = int(
        df.duplicated().sum()
    )

    score = (
        1 - (duplicate_rows / total_rows)
    ) * 100

    return round(max(0, score), 2)


def calculate_validity(df):
    """
    Check basic validity of numeric and
    common email fields.
    """

    total_checks = 0
    failed_checks = 0

    for column in df.columns:

        series = df[column]
        column_name = str(column).lower()

        # Numeric validation
        if pd.api.types.is_numeric_dtype(series):

            valid_values = series.dropna()

            if len(valid_values) > 0:

                total_checks += len(valid_values)

                # Age validation
                if "age" in column_name:

                    invalid = (
                        (valid_values < 0)
                        | (valid_values > 120)
                    )

                    failed_checks += int(
                        invalid.sum()
                    )

                # Salary validation
                elif "salary" in column_name:

                    invalid = (
                        valid_values < 0
                    )

                    failed_checks += int(
                        invalid.sum()
                    )

        # Email validation
        if "email" in column_name:

            values = series.dropna().astype(str)

            pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

            if len(values) > 0:

                total_checks += len(values)

                invalid = ~values.str.match(
                    pattern
                )

                failed_checks += int(
                    invalid.sum()
                )

    if total_checks == 0:
        return 100.0

    score = (
        1 - (failed_checks / total_checks)
    ) * 100

    return round(max(0, score), 2)


def calculate_consistency(df):
    """
    Check basic consistency of categorical/text data.
    """

    total_checks = 0
    inconsistent_checks = 0

    for column in df.select_dtypes(
        include=["object", "category"]
    ).columns:

        values = df[column].dropna().astype(str)

        if len(values) == 0:
            continue

        # Check whitespace inconsistencies
        stripped_values = values.str.strip()

        inconsistent_checks += int(
            (values != stripped_values).sum()
        )

        total_checks += len(values)

        # Check values differing only by case
        normalized = values.str.strip().str.lower()

        duplicate_normalized = (
            normalized.duplicated().sum()
        )

        inconsistent_checks += int(
            duplicate_normalized
        )

    if total_checks == 0:
        return 100.0

    score = (
        1 - (
            inconsistent_checks
            / total_checks
        )
    ) * 100

    return round(max(0, score), 2)


def calculate_overall_quality(df):
    """
    Calculate the final overall data-quality score.
    """

    completeness = calculate_completeness(df)

    uniqueness = calculate_uniqueness(df)

    validity = calculate_validity(df)

    consistency = calculate_consistency(df)

    overall_score = (
        completeness * 0.30
        + uniqueness * 0.20
        + validity * 0.30
        + consistency * 0.20
    )

    overall_score = round(
        overall_score,
        2
    )

    summary = pd.DataFrame({
        "Dimension": [
            "Completeness",
            "Uniqueness",
            "Validity",
            "Consistency"
        ],
        "Score": [
            completeness,
            uniqueness,
            validity,
            consistency
        ],
        "Weight": [
            "30%",
            "20%",
            "30%",
            "20%"
        ]
    })

    return overall_score, summary