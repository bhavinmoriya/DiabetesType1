# CGM + Insulin Dashboard (Polars Version)

A Python tool for simulating, analyzing, and visualizing Continuous Glucose Monitoring (CGM) and insulin pump data using **Polars** for efficient data manipulation.

---

## **Features**

- Simulate or load real-world CGM and insulin data.
- Merge datasets using **as-of joins** to align glucose readings with insulin doses.
- Detect hypoglycemia (`HYPO`) and hyperglycemia (`HYPER`) events.
- Predict next glucose value using a rolling average.
- Visualize glucose trends and alerts with `matplotlib`.
- Command-line interface for easy use.

---

## **Installation**

### **Prerequisites**

- Python 3.8+
- `polars`, `numpy`, `matplotlib`

### **Install Dependencies**

```bash
uv add polars numpy matplotlib
```

---

## **Usage**

### **1. Run with Demo Data**

```bash
python unified_cgm_insulin_polars.py
```

This will generate demo data for both CGM and insulin, merge them, detect alerts, predict the next glucose value, and plot the results.

### **2. Run with Your Own Data**

```bash
python unified_cgm_insulin_polars.py --cgm path/to/cgm_data.csv --insulin path/to/insulin_data.csv
```

- `--cgm`: Path to your CGM data CSV file.
- `--insulin`: Path to your insulin data CSV file.

### **3. Expected CSV Format**

- **CGM Data**: Columns `timestamp` and `glucose_mg_dl`.
- **Insulin Data**: Columns `timestamp` and `insulin_units`.

---

## **Example Output**

- **Terminal Output**:
  ```
  Predicted glucose in 5 minutes: 125.3 mg/dL
  ```
- **Plot**:  
Glucose and Insulin Dashboard
  - Green: Normal glucose levels.
  - Red: Hypoglycemia (`HYPO`).
  - Orange: Hyperglycemia (`HYPER`).

---

## **Code Overview**

### **1. Data Loading**

- `load_cgm_data()`: Loads or simulates CGM data (288 data points/day).
- `load_insulin_data()`: Loads or simulates insulin data (24 data points/day).

### **2. Data Merging**

- `merge_data()`: Uses Polars' `join_asof` to align CGM and insulin data by timestamp.

### **3. Analytics**

- `generate_alerts()`: Detects `HYPO` and `HYPER` events.
- `predict_next_glucose()`: Predicts the next glucose value using a rolling average.

### **4. Visualization**

- `plot_glucose()`: Plots glucose trends and alerts.

---

## **Customization**

- **Alert Thresholds**: Modify `HYPO_THRESHOLD` and `HYPER_THRESHOLD` in the script.
- **Prediction Window**: Adjust the `window` parameter in `predict_next_glucose()`.
- **Plot Styling**: Customize the `matplotlib` plot in `plot_glucose()`.

---

## **Why Polars?**

- **Performance**: Polars is optimized for speed and memory efficiency, making it ideal for large datasets.
- **Ease of Use**: Polars' API is intuitive and similar to Pandas, but with better performance.

---

## Running with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t diabetes-app .
   ```
2. **Run the container:**
	```bash
	docker run -p 8501:8501 diabetes-app
	``` 
	
---

## **License**

This project is open-source and available under the [MIT License](LICENSE).

---

## **Contributing**

Contributions are welcome! Open an issue or submit a pull request.

---

## **Contact**

For questions or feedback, contact [bhavinmoriya58@gmail.com] or open an issue on GitHub.
