from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf_report(
    dataset_name,
    overall_score,
    quality_df,
    rows,
    columns,
    missing_values,
    duplicate_rows
):
    """
    Generate a PDF data-quality report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    # --------------------------------
    # Title
    # --------------------------------

    story.append(
        Paragraph(
            "AI Data Quality Engine",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Automated Data Quality Assessment Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    # --------------------------------
    # Dataset Information
    # --------------------------------

    story.append(
        Paragraph(
            "Dataset Information",
            styles["Heading2"]
        )
    )

    dataset_table = [
        ["Metric", "Value"],
        ["Dataset", dataset_name],
        ["Rows", str(rows)],
        ["Columns", str(columns)],
        ["Missing Values", str(missing_values)],
        ["Duplicate Rows", str(duplicate_rows)],
        [
            "Overall Quality Score",
            f"{overall_score:.2f} / 100"
        ]
    ]

    table = Table(
        dataset_table,
        colWidths=[220, 220]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            )
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # --------------------------------
    # Quality Dimensions
    # --------------------------------

    story.append(
        Paragraph(
            "Quality Dimensions",
            styles["Heading2"]
        )
    )

    quality_table = [
        [
            "Dimension",
            "Score",
            "Weight"
        ]
    ]

    for _, row in quality_df.iterrows():

        quality_table.append([
            str(row["Dimension"]),
            f'{float(row["Score"]):.2f}',
            str(row["Weight"])
        ])

    table = Table(
        quality_table,
        colWidths=[180, 130, 130]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # --------------------------------
    # Conclusion
    # --------------------------------

    story.append(
        Paragraph(
            "Conclusion",
            styles["Heading2"]
        )
    )

    if overall_score >= 90:
        status = "Excellent"

    elif overall_score >= 75:
        status = "Good"

    elif overall_score >= 50:
        status = "Needs Improvement"

    else:
        status = "Poor"

    story.append(
        Paragraph(
            f"The dataset received an overall quality "
            f"score of {overall_score:.2f}/100 and is "
            f"classified as {status}. The report provides "
            f"a summary of the major data-quality "
            f"dimensions used by the AI Data Quality Engine.",
            styles["BodyText"]
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer