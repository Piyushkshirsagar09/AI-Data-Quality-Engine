import pandas as pd


def calculate_quality_metrics(df):
    """
    Calculate basic data-quality metrics
    for a dataset.
    """

    total_rows = len(df)
    total_columns = len(df.columns)

    total_cells = total_rows * total_columns

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    if total_cells > 0:

        completeness = (
            1 - (missing_values / total_cells)
        ) * 100

    else:

        completeness = 100


    if total_rows > 0:

        uniqueness = (
            1 - (duplicate_rows / total_rows)
        ) * 100

    else:

        uniqueness = 100


    # Keep the same first-version scoring
    # approach used in the main application.
    validity = completeness

    consistency = 100


    overall_score = (
        completeness
        + uniqueness
        + validity
        + consistency
    ) / 4


    return {
        "Rows": total_rows,
        "Columns": total_columns,
        "Missing Values": missing_values,
        "Duplicate Rows": duplicate_rows,
        "Completeness": completeness,
        "Uniqueness": uniqueness,
        "Validity": validity,
        "Consistency": consistency,
        "Quality Score": overall_score
    }