import pandas as pd

from src.quality_engine import (
    calculate_completeness,
    calculate_uniqueness,
    calculate_validity,
    calculate_consistency,
    calculate_overall_quality
)


def create_test_dataset():

    return pd.DataFrame({
        "ID": [1, 2, 3, 3, 5],
        "Age": [20, 25, None, 30, 150],
        "Salary": [25000, 30000, 35000, 40000, -5000],
        "Email": [
            "a@gmail.com",
            "b@gmail.com",
            "invalid-email",
            "d@gmail.com",
            None
        ]
    })


def test_completeness():

    df = create_test_dataset()

    score = calculate_completeness(df)

    assert 0 <= score <= 100


def test_uniqueness():

    df = create_test_dataset()

    score = calculate_uniqueness(df)

    assert 0 <= score <= 100


def test_validity():

    df = create_test_dataset()

    score = calculate_validity(df)

    assert 0 <= score <= 100


def test_consistency():

    df = create_test_dataset()

    score = calculate_consistency(df)

    assert 0 <= score <= 100


def test_overall_quality():

    df = create_test_dataset()

    score, quality_df = calculate_overall_quality(df)

    assert 0 <= score <= 100

    assert not quality_df.empty

    assert "Dimension" in quality_df.columns

    assert "Score" in quality_df.columns

    assert "Weight" in quality_df.columns