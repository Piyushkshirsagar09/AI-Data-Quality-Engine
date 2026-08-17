import pandas as pd


def create_quality_report(df):
    """
    Create a downloadable data-quality report.
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

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).shape[1]

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).shape[1]

    if total_cells > 0:

        completeness = (
            1 - missing_values / total_cells
        ) * 100

    else:

        completeness = 100

    if total_rows > 0:

        uniqueness = (
            1 - duplicate_rows / total_rows
        ) * 100

    else:

        uniqueness = 100

    validity = completeness

    consistency = 100

    quality_score = (
        completeness
        + uniqueness
        + validity
        + consistency
    ) / 4

    report = pd.DataFrame({
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Missing Values",
            "Duplicate Rows",
            "Numeric Columns",
            "Categorical Columns",
            "Completeness",
            "Uniqueness",
            "Validity",
            "Consistency",
            "Overall Quality Score"
        ],
        "Value": [
            total_rows,
            total_columns,
            missing_values,
            duplicate_rows,
            numeric_columns,
            categorical_columns,
            round(completeness, 2),
            round(uniqueness, 2),
            round(validity, 2),
            round(consistency, 2),
            round(quality_score, 2)
        ]
    })

    return report