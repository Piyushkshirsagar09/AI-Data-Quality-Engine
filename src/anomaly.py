import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer


def detect_anomalies(df):
    """
    Detect unusual records using Isolation Forest.

    Only numeric columns are used for the first version.
    """

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    # No numeric columns
    if len(numeric_columns) == 0:

        return None, (
            "No numeric columns available "
            "for anomaly detection."
        )

    numeric_data = df[numeric_columns].copy()

    # Replace missing numeric values with median
    imputer = SimpleImputer(
        strategy="median"
    )

    processed_data = imputer.fit_transform(
        numeric_data
    )

    # Create Isolation Forest model
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    # Train model and predict
    predictions = model.fit_predict(
        processed_data
    )

    # -1 = anomaly
    #  1 = normal
    anomaly_mask = predictions == -1

    result_df = df.copy()

    result_df["Anomaly"] = predictions

    result_df["Anomaly Status"] = result_df[
        "Anomaly"
    ].map({
        1: "Normal",
        -1: "Anomaly"
    })

    anomaly_count = int(
        anomaly_mask.sum()
    )

    return {
        "data": result_df,
        "numeric_columns": numeric_columns,
        "anomaly_count": anomaly_count
    }, None