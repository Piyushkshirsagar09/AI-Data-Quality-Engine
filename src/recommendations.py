import pandas as pd


def generate_recommendations(df):

    recommendations = []

    total_rows = len(df)

    if total_rows == 0:
        return recommendations

    # --------------------------------
    # Missing Value Analysis
    # --------------------------------

    for column in df.columns:

        missing_count = int(
            df[column].isnull().sum()
        )

        if missing_count > 0:

            missing_percentage = (
                missing_count / total_rows
            ) * 100

            if missing_percentage >= 30:
                severity = "High"

            elif missing_percentage >= 10:
                severity = "Medium"

            else:
                severity = "Low"

            if pd.api.types.is_numeric_dtype(
                df[column]
            ):
                action = (
                    "Consider median or mean "
                    "imputation."
                )
            else:
                action = (
                    "Consider mode imputation "
                    "or an explicit 'Unknown' category."
                )

            recommendations.append({
                "Column": column,
                "Issue": "Missing Values",
                "Count": missing_count,
                "Severity": severity,
                "Recommendation": action
            })


    # --------------------------------
    # Duplicate Row Analysis
    # --------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        duplicate_percentage = (
            duplicate_count / total_rows
        ) * 100

        if duplicate_percentage >= 10:
            severity = "High"

        elif duplicate_percentage >= 5:
            severity = "Medium"

        else:
            severity = "Low"

        recommendations.append({
            "Column": "Entire Dataset",
            "Issue": "Duplicate Rows",
            "Count": duplicate_count,
            "Severity": severity,
            "Recommendation":
                "Review and remove duplicate records "
                "if they are not legitimate repeated events."
        })


    # --------------------------------
    # Negative Numeric Values
    # --------------------------------

    for column in df.select_dtypes(
        include=["number"]
    ).columns:

        negative_count = int(
            (df[column] < 0).sum()
        )

        if negative_count > 0:

            recommendations.append({
                "Column": column,
                "Issue": "Negative Values",
                "Count": negative_count,
                "Severity": "Medium",
                "Recommendation":
                    "Verify whether negative values "
                    "are logically valid for this column."
            })


    # --------------------------------
    # Constant Columns
    # --------------------------------

    for column in df.columns:

        unique_count = df[column].nunique(
            dropna=False
        )

        if unique_count <= 1:

            recommendations.append({
                "Column": column,
                "Issue": "Constant Column",
                "Count": unique_count,
                "Severity": "Low",
                "Recommendation":
                    "Consider removing the column "
                    "if it provides no useful information."
            })


    return recommendations