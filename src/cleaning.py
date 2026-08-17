import pandas as pd


def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    """
    cleaned_df = df.drop_duplicates()

    removed = len(df) - len(cleaned_df)

    return cleaned_df, removed


def fill_missing_numeric(df, method="median"):
    """
    Fill missing values in numeric columns.
    """

    cleaned_df = df.copy()

    numeric_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns

    for column in numeric_columns:

        if method == "median":
            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].median()
            )

        elif method == "mean":
            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].mean()
            )

    return cleaned_df


def fill_missing_categorical(df):
    """
    Fill missing values in categorical/text columns
    using the most frequent value.
    """

    cleaned_df = df.copy()

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        if cleaned_df[column].isnull().any():

            mode = cleaned_df[column].mode()

            if not mode.empty:
                cleaned_df[column] = cleaned_df[column].fillna(
                    mode.iloc[0]
                )

    return cleaned_df


def clean_dataset(df):
    """
    Apply the basic automated cleaning pipeline.
    """

    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df, duplicate_count = remove_duplicates(
        cleaned_df
    )

    # Fill numeric missing values
    cleaned_df = fill_missing_numeric(
        cleaned_df,
        method="median"
    )

    # Fill categorical missing values
    cleaned_df = fill_missing_categorical(
        cleaned_df
    )

    return cleaned_df, duplicate_count