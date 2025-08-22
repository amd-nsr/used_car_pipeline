# Used Car Price Prediction Pipeline

This project is a data pipeline for predicting the price of used cars. It includes data wrangling, model training, and a web-based interface for predictions. The pipeline is implemented using Python, Apache Airflow, and Streamlit.

---

## Features

- **Data Wrangling**: Cleans and preprocesses raw car data.
- **Model Training**: Trains a linear regression model to predict car prices.
- **Web Interface**: Provides a user-friendly interface for price prediction.
- **ETL Pipeline**: Automates data processing and model training using Apache Airflow.

---

## Project Structure

```
used_car_pipeline/
├── dags/                  # Airflow DAGs for ETL pipeline
│   ├── etl_pipeline.py    # ETL pipeline definition
├── data/                  # Data directory
│   ├── raw/               # Raw data files
│   ├── processed/         # Processed data files
├── models/                # Trained models and schema files
├── notebooks/             # Jupyter notebooks for EDA
├── scripts/               # Python scripts for data processing and training
│   ├── wrangle_data.py    # Data wrangling script
│   ├── train_model.py     # Model training script
│   ├── predict.py         # Streamlit app for predictions
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore file
```

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/used_car_pipeline.git
    cd used_car_pipeline
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### 1. Data Wrangling and Model Training
Run the ETL pipeline using Apache Airflow:
1. Start the Airflow scheduler and webserver:
    ```bash
    airflow db init
    airflow scheduler
    airflow webserver
    ```
2. Access the Airflow UI at `http://localhost:8080` and trigger the `used_car_etl_pipeline` DAG.

### 2. Streamlit App
Launch the Streamlit app for predictions:
```bash
streamlit run scripts/predict.py
```

---

## How It Works

1. **Data Wrangling**:
    - Cleans raw data by removing irrelevant columns, handling missing values, and encoding categorical features.
    - Saves the processed data to `data/processed/cars_clean.csv`.

2. **Model Training**:
    - Trains a linear regression model using the processed data.
    - Saves the trained model and schema to the `models/` directory.

3. **Prediction**:
    - The Streamlit app allows users to input car features and predicts the price using the trained model.

---

## Dependencies

- Python 3.10+
- Pandas
- Scikit-learn
- Joblib
- Apache Airflow
- Streamlit

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

[Your Name](https://github.com/your-profile)