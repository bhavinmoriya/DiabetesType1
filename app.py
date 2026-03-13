import streamlit as st
import polars as pl
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(page_title="Prediction of the glucose", layout="wide")

#Constants

HYPO_THRESHOLD = 70
HYPER_THRESHOLD = 180
DEFAULT_GLUCOSE_MEAN = 120
DEFAULT_GLUCOSE_STD = 20

#--- Helper Functions ---

def load_cgm_data(file_path: str = None) -> pl.DataFrame:
    if file_path:
        try:
            return pl.read_csv(file_path, try_parse_dates=True)
        except Exception as e:
            st.error(f"Error loading CGM data: {e}")
            raise
    else:
        timestamps = [datetime.now() - timedelta(minutes=5*i) for i in range(288)][::-1]
        glucose = np.random.normal(loc=DEFAULT_GLUCOSE_MEAN, scale=DEFAULT_GLUCOSE_STD, size=288)
        return pl.DataFrame({
            'timestamp': timestamps,
            'glucose_mg_dl': glucose
        })

def load_insulin_data(file_path: str = None) -> pl.DataFrame:
    if file_path:
        try:
            return pl.read_csv(file_path, try_parse_dates=True)
        except Exception as e:
            st.error(f"Error loading insulin data: {e}")
            raise
    else:
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(24)][::-1]
        insulin_units = np.random.choice([0, 1, 2, 3], size=24)
        return pl.DataFrame({
            'timestamp': timestamps,
            'insulin_units': insulin_units
        })

def merge_data(cgm_df: pl.DataFrame, insulin_df: pl.DataFrame) -> pl.DataFrame:
    merged = cgm_df.join_asof(insulin_df, on='timestamp', strategy='backward')
    return merged.with_columns(pl.col("insulin_units").fill_null(0))

def generate_alerts(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.when(pl.col('glucose_mg_dl') < HYPO_THRESHOLD).then(pl.lit('HYPO'))
          .when(pl.col('glucose_mg_dl') > HYPER_THRESHOLD).then(pl.lit('HYPER'))
          .otherwise(pl.lit('NORMAL')).alias('alert')
    )

def predict_next_glucose(df: pl.DataFrame, window: int = 5) -> float:
    y = df['glucose_mg_dl'].to_numpy()
    if len(y) < window:
        return y[-1]
    rolling_avg = np.convolve(y, np.ones(window)/window, mode='valid')
    return rolling_avg[-1]

#--- Streamlit UI ---

st.title("Glucose Prediction Dashboard")
st.write("Upload your CGM and insulin data, or use demo data to predict the next glucose value.")

cgm_file = st.file_uploader("Upload CGM Data (CSV)", type="csv")
insulin_file = st.file_uploader("Upload Insulin Data (CSV)", type="csv")

if st.button("Run Prediction"):
    with st.spinner("Processing data..."):
        cgm = load_cgm_data(cgm_file if cgm_file else None)
        insulin = load_insulin_data(insulin_file if insulin_file else None)
        merged = merge_data(cgm, insulin)
        merged = generate_alerts(merged)
        next_glucose = predict_next_glucose(merged)

    st.success(f"Predicted glucose in 5 minutes: **{next_glucose:.1f} mg/dL**")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    df_pd = merged.to_pandas()
    colors = np.where(df_pd['alert']=='HYPO', 'red',
                     np.where(df_pd['alert']=='HYPER', 'orange', 'green'))
    ax.plot(df_pd['timestamp'], df_pd['glucose_mg_dl'], label='Glucose (mg/dL)')
    ax.scatter(df_pd['timestamp'], df_pd['glucose_mg_dl'], c=colors, label='Alerts')
    ax.set_xlabel('Time')
    ax.set_ylabel('Glucose (mg/dL)')
    ax.set_title('Glucose Trend with Alerts')
    ax.legend()
    st.pyplot(fig)

# Link to download demo files
st.markdown("""
---
**Download demo files for Glucose and Insulin data:**
[Demo Files (GitHub)](https://github.com/bhavinmoriya/DiabetesType1/tree/main/DemoFiles)
""")
