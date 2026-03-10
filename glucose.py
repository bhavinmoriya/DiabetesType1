import polars as pl
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import argparse
from typing import Optional, Tuple

# Constants
HYPO_THRESHOLD = 70
HYPER_THRESHOLD = 180
DEFAULT_GLUCOSE_MEAN = 120
DEFAULT_GLUCOSE_STD = 20

def load_cgm_data(file_path: Optional[str] = None) -> pl.DataFrame:
    """
    Load CGM data from CSV or generate demo data.

    Args:
        file_path (Optional[str]): Path to CSV file. If None, generates demo data.

    Returns:
        pl.DataFrame: DataFrame with columns 'timestamp' and 'glucose_mg_dl'.
    """
    if file_path:
        try:
            return pl.read_csv(file_path, parse_dates=True)
        except Exception as e:
            print(f"Error loading CGM data: {e}")
            raise
    else:
        timestamps = [datetime.now() - timedelta(minutes=5*i) for i in range(288)][::-1]
        glucose = np.random.normal(loc=DEFAULT_GLUCOSE_MEAN, scale=DEFAULT_GLUCOSE_STD, size=288)
        return pl.DataFrame({
            'timestamp': timestamps,
            'glucose_mg_dl': glucose
        })

def load_insulin_data(file_path: Optional[str] = None) -> pl.DataFrame:
    """
    Load insulin pump data from CSV or simulate.

    Args:
        file_path (Optional[str]): Path to CSV file. If None, generates demo data.

    Returns:
        pl.DataFrame: DataFrame with columns 'timestamp' and 'insulin_units'.
    """
    if file_path:
        try:
            return pl.read_csv(file_path, parse_dates=True)
        except Exception as e:
            print(f"Error loading insulin data: {e}")
            raise
    else:
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(24)][::-1]
        insulin_units = np.random.choice([0, 1, 2, 3], size=24)
        return pl.DataFrame({
            'timestamp': timestamps,
            'insulin_units': insulin_units
        })

def merge_data(cgm_df: pl.DataFrame, insulin_df: pl.DataFrame) -> pl.DataFrame:
    """
    Merge CGM and insulin data on timestamp using asof join.

    Args:
        cgm_df (pl.DataFrame): CGM data.
        insulin_df (pl.DataFrame): Insulin data.

    Returns:
        pl.DataFrame: Merged DataFrame.
    """
    merged = cgm_df.join_asof(insulin_df, on='timestamp', strategy='backward')
    return merged.with_columns([
        pl.col("insulin_units").fill_null(0)
    ])

def generate_alerts(df: pl.DataFrame, hypo_threshold: int = HYPO_THRESHOLD, hyper_threshold: int = HYPER_THRESHOLD) -> pl.DataFrame:
    """
    Detect hypo/hyperglycemia events.

    Args:
        df (pl.DataFrame): Input DataFrame.
        hypo_threshold (int): Hypoglycemia threshold.
        hyper_threshold (int): Hyperglycemia threshold.

    Returns:
        pl.DataFrame: DataFrame with 'alert' column.
    """
    return df.with_columns([
        pl.when(pl.col('glucose_mg_dl') < hypo_threshold).then(pl.lit('HYPO'))
          .when(pl.col('glucose_mg_dl') > hyper_threshold).then(pl.lit('HYPER'))
          .otherwise(pl.lit('NORMAL')).alias('alert')
    ])

def predict_next_glucose(df: pl.DataFrame, window: int = 5) -> float:
    """
    Predict next glucose value using rolling average.

    Args:
        df (pl.DataFrame): Input DataFrame.
        window (int): Rolling window size.

    Returns:
        float: Predicted glucose value.
    """
    y = df['glucose_mg_dl'].to_numpy()
    if len(y) < window:
        return y[-1]  # Fallback if not enough data
    rolling_avg = np.convolve(y, np.ones(window)/window, mode='valid')
    return rolling_avg[-1]

def plot_glucose(df: pl.DataFrame) -> None:
    """
    Plot glucose data with alerts.

    Args:
        df (pl.DataFrame): Input DataFrame.
    """
    df_pd = df.to_pandas()
    colors = np.where(df_pd['alert']=='HYPO', 'red',
                     np.where(df_pd['alert']=='HYPER', 'orange', 'green'))

    plt.figure(figsize=(12,6))
    plt.plot(df_pd['timestamp'], df_pd['glucose_mg_dl'], label='Glucose (mg/dL)')
    plt.scatter(df_pd['timestamp'], df_pd['glucose_mg_dl'], c=colors, label='Alerts')
    plt.xlabel('Time')
    plt.ylabel('Glucose (mg/dL)')
    plt.title('CGM + Insulin Dashboard (Polars Version)')
    plt.legend()
    plt.show()

def main(cgm_file: Optional[str] = None, insulin_file: Optional[str] = None) -> None:
    """
    Main function to run the demo.

    Args:
        cgm_file (Optional[str]): Path to CGM data file.
        insulin_file (Optional[str]): Path to insulin data file.
    """
    cgm = load_cgm_data(cgm_file)
    insulin = load_insulin_data(insulin_file)
    merged = merge_data(cgm, insulin)
    merged = generate_alerts(merged)
    next_glucose = predict_next_glucose(merged)

    print(f"Predicted glucose in 5 minutes: {next_glucose:.1f} mg/dL")
    plot_glucose(merged)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CGM + Insulin Dashboard")
    parser.add_argument("--cgm", help="Path to CGM data file", default=None)
    parser.add_argument("--insulin", help="Path to insulin data file", default=None)
    args = parser.parse_args()

    main(args.cgm, args.insulin)
