import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
import streamlit as st
import pandas as pd
import plotly.express as px

from src.cleaning import clean_dataset
from src.rules import run_default_rules
from src.anomaly import detect_anomalies
from src.recommendations import generate_recommendations
from src.comparison import calculate_quality_metrics
from src.report import create_quality_report
from src.quality_engine import calculate_overall_quality
from src.pdf_report import generate_pdf_report

# --------------------------------
# Intelligent Column Validation
# --------------------------------

def analyze_column(df, column):

    series = df[column]

    missing = int(series.isna().sum())

    unique_values = int(series.nunique(dropna=True))

    data_type = str(series.dtype)

    recommendations = []

    # Missing value check
    if missing > 0:
        recommendations.append(
            f"{missing} missing values detected. "
            "Consider appropriate imputation."
        )

    # Duplicate value check
    if unique_values < len(series.dropna()):
        recommendations.append(
            "Repeated values detected. "
            "Check whether duplicates are expected."
        )

    # Numeric validation
    if pd.api.types.is_numeric_dtype(series):

        negative_values = int(
            (series < 0).sum()
        )

        if negative_values > 0:
            recommendations.append(
                f"{negative_values} negative values detected. "
                "Check whether negative values are valid."
            )

    # Text validation
    if pd.api.types.is_string_dtype(series):

        empty_values = int(
            series.astype(str).str.strip().eq("").sum()
        )

        if empty_values > 0:
            recommendations.append(
                f"{empty_values} empty text values detected."
            )

    # No problems
    if len(recommendations) == 0:
        recommendations.append(
            "No obvious quality issue detected."
        )

    return {
        "Column": column,
        "Data Type": data_type,
        "Missing Values": missing,
        "Unique Values": unique_values,
        "Recommendations": " ".join(recommendations)
    }
# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="AI Data Quality Engine",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Custom CSS
# --------------------------------
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #1f77b4;
}

.sub-title {
    font-size: 20px;
    text-align: center;
    color: gray;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# Header
# --------------------------------
st.markdown(
    "<h1 class='main-title'>📊 AI Data Quality Engine</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Intelligent Platform for Automated Data Quality Assessment & Cleaning</p>",
    unsafe_allow_html=True
)

st.divider()


# --------------------------------
# Project Information
# --------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🚀 Project Features

    ✔ Upload CSV or Excel Dataset

    ✔ Detect Missing Values

    ✔ Detect Duplicate Records

    ✔ Check Data Types

    ✔ Data Quality Score

    ✔ AI-Based Data Cleaning

    ✔ Download Cleaned Dataset

    ✔ Generate PDF Report
    """)

with col2:
    st.info("📌 Final Year BE Project")
    st.success("Department: AI & Data Science")
    st.warning("Technology: Python + Streamlit")


st.divider()


# --------------------------------
# Dataset Upload
# --------------------------------
st.subheader("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV or Excel File",
    type=["csv", "xlsx"]
)


# --------------------------------
# Dataset Processing
# --------------------------------
if uploaded_file is not None:

    # Read Dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Dataset Uploaded Successfully!")


    # --------------------------------
    # Basic Dataset Information
    # --------------------------------

    total_rows = df.shape[0]
    total_columns = df.shape[1]

    total_cells = total_rows * total_columns

    missing_values = int(df.isnull().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).shape[1]

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).shape[1]


    # --------------------------------
    # Data Quality Score
    # --------------------------------

    # Completeness
    if total_cells > 0:
        missing_percentage = (
            missing_values / total_cells
        ) * 100
    else:
        missing_percentage = 0

    completeness_score = max(
        0,
        100 - missing_percentage
    )


    # Uniqueness
    if total_rows > 0:
        duplicate_percentage = (
            duplicate_rows / total_rows
        ) * 100
    else:
        duplicate_percentage = 0

    uniqueness_score = max(
        0,
        100 - duplicate_percentage
    )


    # Validity
    # First version:
    # missing values are considered invalid values.
    invalid_values = missing_values

    if total_cells > 0:
        invalid_percentage = (
            invalid_values / total_cells
        ) * 100
    else:
        invalid_percentage = 0

    validity_score = max(
        0,
        100 - invalid_percentage
    )


    # Consistency
    # We will implement real consistency rules later.
    consistency_score = 100


    # Overall Quality Score
    quality_score = (
        completeness_score
        + uniqueness_score
        + validity_score
        + consistency_score
    ) / 4


    # --------------------------------
    # Dataset Summary
    # --------------------------------
    st.subheader("📊 Dataset Summary")


    # First KPI Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📏 Total Rows",
            total_rows
        )

    with col2:
        st.metric(
            "📋 Total Columns",
            total_columns
        )

    with col3:
        st.metric(
            "❌ Missing Values",
            missing_values
        )

    with col4:
        st.metric(
            "🔁 Duplicate Rows",
            duplicate_rows
        )


    # Second KPI Row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🔢 Numeric Columns",
            numeric_columns
        )

    with col2:
        st.metric(
            "🔤 Categorical Columns",
            categorical_columns
        )

    with col3:

        memory_usage = (
            df.memory_usage(deep=True).sum()
            / 1024
        )

        st.metric(
            "💾 Memory Usage",
            f"{memory_usage:.2f} KB"
        )


    st.divider()


    # --------------------------------
    # Data Quality Score
    # --------------------------------
    st.subheader("⭐ Data Quality Score")

    st.metric(
        "Overall Quality Score",
        f"{quality_score:.2f} / 100"
    )


    # --------------------------------
    # Quality Dimensions
    # --------------------------------
    quality_data = pd.DataFrame({
        "Quality Dimension": [
            "Completeness",
            "Uniqueness",
            "Validity",
            "Consistency"
        ],
        "Score": [
            completeness_score,
            uniqueness_score,
            validity_score,
            consistency_score
        ]
    })


    st.write("### Quality Dimensions")

    st.dataframe(
        quality_data,
        use_container_width=True
    )


    # --------------------------------
    # Quality Score Chart
    # --------------------------------
    st.write("### 📊 Data Quality by Dimension")

    fig_quality = px.bar(
        quality_data,
        x="Quality Dimension",
        y="Score",
        range_y=[0, 100],
        text="Score"
    )

    fig_quality.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_quality,
        use_container_width=True
    )


    # --------------------------------
    # Dataset Preview
    # --------------------------------
    st.subheader("👀 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )


    # --------------------------------
    # Data Types
    # --------------------------------
    st.subheader("🔤 Data Types")

    data_types = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(
        data_types,
        use_container_width=True
    )


    # --------------------------------
    # Missing Values
    # --------------------------------
    st.subheader("❌ Missing Values by Column")

    missing_data = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        missing_data,
        use_container_width=True
    )


    # --------------------------------
    # Missing Values Chart
    # --------------------------------
    st.write("### 📊 Missing Values by Column")

    fig_missing = px.bar(
        missing_data,
        x="Column",
        y="Missing Values",
        text="Missing Values"
    )

    fig_missing.update_layout(
        xaxis_title="Columns",
        yaxis_title="Number of Missing Values"
    )

    st.plotly_chart(
        fig_missing,
        use_container_width=True
    )


    # --------------------------------
    # Column Type Distribution
    # --------------------------------
    st.write("### 🥧 Column Type Distribution")

    type_data = pd.DataFrame({
        "Type": [
            "Numeric",
            "Categorical"
        ],
        "Count": [
            numeric_columns,
            categorical_columns
        ]
    })

    fig_types = px.pie(
        type_data,
        names="Type",
        values="Count"
    )

    st.plotly_chart(
        fig_types,
        use_container_width=True
    )

    # --------------------------------
    # Intelligent Data Validation
    # --------------------------------

    st.divider()

    st.subheader("🤖 Intelligent Data Validation")

    validation_results = []

    for column in df.columns:

        result = analyze_column(df, column)

        validation_results.append(result)

    validation_df = pd.DataFrame(
        validation_results
    )

    st.dataframe(
        validation_df,
        use_container_width=True
    )


    # --------------------------------
    # Duplicate Records
    # --------------------------------

    st.subheader("🔁 Duplicate Records")

    if duplicate_rows == 0:

        st.success(
            "✅ No duplicate records found."
        )

    else:

        st.warning(
            f"⚠️ {duplicate_rows} duplicate records found."
        )

        duplicate_data = df[
            df.duplicated(keep=False)
        ]

        st.dataframe(
            duplicate_data,
            use_container_width=True
        )

    # --------------------------------
    # Automated Data Cleaning
    # --------------------------------

    st.divider()

    st.subheader("🧹 Automated Data Cleaning")

    st.write(
        "Automatically handle duplicate records "
        "and missing values."
    )

    if st.button("🧹 Clean Dataset"):

        cleaned_df, duplicate_count = clean_dataset(df)

        st.success(
            "✅ Dataset cleaned successfully!"
        )

        st.write("### Before Cleaning")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Rows",
                df.shape[0]
            )

        with col2:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        with col3:
            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )


        st.write("### After Cleaning")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Rows",
                cleaned_df.shape[0]
            )

        with col2:
            st.metric(
                "Missing Values",
                int(cleaned_df.isnull().sum().sum())
            )

        with col3:
            st.metric(
                "Duplicate Rows",
                int(cleaned_df.duplicated().sum())
            )


        st.write("### Cleaned Dataset")

        st.dataframe(
            cleaned_df,
            use_container_width=True
        )


        # --------------------------------
        # Download Cleaned Dataset
        # --------------------------------

        csv_data = cleaned_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned Dataset",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

        # --------------------------------
    # Data Quality Rules Engine
    # --------------------------------

    st.divider()

    st.subheader("🛡️ Data Quality Rules Engine")

    st.write(
        "Automatically validate important columns "
        "using predefined data-quality rules."
    )

    if st.button("🔍 Run Quality Rules"):

        rule_results = run_default_rules(df)

        if len(rule_results) == 0:

            st.info(
                "No automatic rules were applicable "
                "to this dataset."
            )

        else:

            rules_df = pd.DataFrame(
                rule_results
            )

            st.dataframe(
                rules_df,
                use_container_width=True
            )

            passed_rules = sum(
                rules_df["Status"] == "PASSED"
            )

            failed_rules = sum(
                rules_df["Status"] == "FAILED"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "✅ Passed Rules",
                    passed_rules
                )

            with col2:
                st.metric(
                    "❌ Failed Rules",
                    failed_rules
                )

        # --------------------------------
    # ML-Based Anomaly Detection
    # --------------------------------

    st.divider()

    st.subheader("🤖 ML-Based Anomaly Detection")

    st.write(
        "Uses Isolation Forest to identify "
        "unusual records in numeric data."
    )

    if st.button("🔍 Detect Anomalies"):

        anomaly_result, error_message = detect_anomalies(df)

        if error_message is not None:

            st.warning(error_message)

        else:

            anomaly_df = anomaly_result["data"]

            numeric_columns = anomaly_result[
                "numeric_columns"
            ]

            anomaly_count = anomaly_result[
                "anomaly_count"
            ]

            st.success(
                "✅ Anomaly detection completed."
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🔢 Numeric Columns Used",
                    len(numeric_columns)
                )

            with col2:
                st.metric(
                    "🚨 Anomalies Detected",
                    anomaly_count
                )

            st.write("### Numeric Columns Used")

            st.write(
                ", ".join(numeric_columns)
            )

            st.write("### 🚨 Detected Records")

            detected_anomalies = anomaly_df[
                anomaly_df["Anomaly"] == -1
            ]

            if detected_anomalies.empty:

                st.success(
                    "🎉 No unusual records detected."
                )

            else:

                st.warning(
                    f"{anomaly_count} unusual "
                    "records detected."
                )

                st.dataframe(
                    detected_anomalies,
                    use_container_width=True
                )

        # --------------------------------
    # Automatic Recommendations
    # --------------------------------

    st.divider()

    st.subheader("💡 Automatic Data Quality Recommendations")

    st.write(
        "The system analyzes detected quality problems "
        "and recommends appropriate actions."
    )

    if st.button("💡 Generate Recommendations"):

        recommendations = generate_recommendations(
            df
        )

        if len(recommendations) == 0:

            st.success(
                "🎉 No major data quality issues "
                "were detected."
            )

        else:

            recommendations_df = pd.DataFrame(
                recommendations
            )

            st.dataframe(
                recommendations_df,
                use_container_width=True
            )

            # --------------------------------
            # Recommendation Summary
            # --------------------------------

            high_count = sum(
                recommendations_df["Severity"] == "High"
            )

            medium_count = sum(
                recommendations_df["Severity"] == "Medium"
            )

            low_count = sum(
                recommendations_df["Severity"] == "Low"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🔴 High Priority",
                    high_count
                )

            with col2:
                st.metric(
                    "🟠 Medium Priority",
                    medium_count
                )

            with col3:
                st.metric(
                    "🟢 Low Priority",
                    low_count
                )

        # --------------------------------
    # Before vs After Comparison
    # --------------------------------

    st.divider()

    st.subheader("📊 Before vs After Quality Comparison")

    st.write(
        "Compare the dataset before and after "
        "automatic cleaning."
    )

    if st.button("📈 Compare Dataset Quality"):

        # Original dataset metrics
        before_metrics = calculate_quality_metrics(
            df
        )

        # Clean the dataset
        cleaned_df, duplicate_count = clean_dataset(
            df
        )

        # Cleaned dataset metrics
        after_metrics = calculate_quality_metrics(
            cleaned_df
        )


        # --------------------------------
        # Quality Score Comparison
        # --------------------------------

        comparison_data = pd.DataFrame({
            "Stage": [
                "Before Cleaning",
                "After Cleaning"
            ],
            "Quality Score": [
                before_metrics["Quality Score"],
                after_metrics["Quality Score"]
            ]
        })


        st.write("### ⭐ Quality Score Improvement")


        fig_comparison = px.bar(
            comparison_data,
            x="Stage",
            y="Quality Score",
            range_y=[0, 100],
            text="Quality Score",
            title="Data Quality Before vs After Cleaning"
        )


        fig_comparison.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )


        st.plotly_chart(
            fig_comparison,
            use_container_width=True
        )


        # --------------------------------
        # Before Metrics
        # --------------------------------

        st.write("### 🔴 Before Cleaning")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                before_metrics["Rows"]
            )

        with col2:
            st.metric(
                "Missing Values",
                before_metrics["Missing Values"]
            )

        with col3:
            st.metric(
                "Duplicate Rows",
                before_metrics["Duplicate Rows"]
            )

        with col4:
            st.metric(
                "Quality Score",
                f'{before_metrics["Quality Score"]:.2f}'
            )


        # --------------------------------
        # After Metrics
        # --------------------------------

        st.write("### 🟢 After Cleaning")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                after_metrics["Rows"]
            )

        with col2:
            st.metric(
                "Missing Values",
                after_metrics["Missing Values"]
            )

        with col3:
            st.metric(
                "Duplicate Rows",
                after_metrics["Duplicate Rows"]
            )

        with col4:
            st.metric(
                "Quality Score",
                f'{after_metrics["Quality Score"]:.2f}'
            )


        # --------------------------------
        # Improvement
        # --------------------------------

        improvement = (
            after_metrics["Quality Score"]
            - before_metrics["Quality Score"]
        )


        if improvement > 0:

            st.success(
                f"📈 Quality improved by "
                f"{improvement:.2f} points."
            )

        elif improvement == 0:

            st.info(
                "ℹ️ No measurable quality "
                "improvement was detected."
            )

        else:

            st.warning(
                f"⚠️ Quality decreased by "
                f"{abs(improvement):.2f} points."
            )

        # --------------------------------
    # Quality Report
    # --------------------------------

    st.divider()

    st.subheader("📄 Data Quality Report")

    st.write(
        "Generate a downloadable report containing "
        "the main quality metrics of the uploaded dataset."
    )

    if st.button("📄 Generate Quality Report"):

        report_df = create_quality_report(df)

        st.success(
            "✅ Quality report generated successfully!"
        )

        st.dataframe(
            report_df,
            use_container_width=True
        )

        report_csv = report_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Quality Report",
            data=report_csv,
            file_name="data_quality_report.csv",
            mime="text/csv"
        )
        # --------------------------------
    # Advanced Data Quality Intelligence
    # --------------------------------

    st.divider()

    st.subheader(
        "🧠 Advanced Data Quality Intelligence"
    )

    st.write(
        "Calculate the overall dataset quality "
        "using completeness, uniqueness, validity "
        "and consistency."
    )

    if st.button(
        "🧠 Analyze Data Quality"
    ):

        overall_score, quality_df = (
            calculate_overall_quality(df)
        )

        st.metric(
            "⭐ Overall Data Quality Score",
            f"{overall_score:.2f} / 100"
        )

        st.write(
            "### 📊 Quality Dimensions"
        )

        st.dataframe(
            quality_df,
            use_container_width=True
        )

        # --------------------------------
        # Quality Dimension Chart
        # --------------------------------

        fig_quality = px.bar(
            quality_df,
            x="Dimension",
            y="Score",
            range_y=[0, 100],
            text="Score",
            title="Data Quality Dimensions"
        )

        fig_quality.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside"
        )

        st.plotly_chart(
            fig_quality,
            use_container_width=True
        )

        # --------------------------------
        # Quality Status
        # --------------------------------

        if overall_score >= 90:

            st.success(
                "🟢 Excellent Data Quality"
            )

        elif overall_score >= 75:

            st.info(
                "🟡 Good Data Quality"
            )

        elif overall_score >= 50:

            st.warning(
                "🟠 Data Quality Needs Improvement"
            )

        else:

            st.error(
                "🔴 Poor Data Quality"
            )
        # --------------------------------
    # PDF Quality Report
    # --------------------------------

    st.divider()

    st.subheader("📄 Professional PDF Report")

    st.write(
        "Generate a PDF containing the "
        "dataset quality assessment."
    )

    if st.button("📄 Generate PDF Report"):

        overall_score, quality_df = (
            calculate_overall_quality(df)
        )

        pdf_file = generate_pdf_report(
            dataset_name=uploaded_file.name,
            overall_score=overall_score,
            quality_df=quality_df,
            rows=df.shape[0],
            columns=df.shape[1],
            missing_values=int(
                df.isnull().sum().sum()
            ),
            duplicate_rows=int(
                df.duplicated().sum()
            )
        )

        st.success(
            "✅ PDF report generated successfully!"
        )

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_file,
            file_name="AI_Data_Quality_Report.pdf",
            mime="application/pdf"
        )