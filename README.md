# JJ Flow

This project implements a robust two-pipeline system designed to streamline financial data ingestion, storage, and predictive modeling for making informed investment decisions. The repository includes utilities and scripts for managing the entire workflow, from fetching external data to generating predictions.

---

## Overview

The project is divided into two main pipelines:

### 1. **Data Pipeline**
- Fetches financial data from external sources (e.g., APIs, CSV files).
- Processes and transforms the raw data into a structured format.
- Stores the cleaned data in a **PostgreSQL database** for efficient querying and analysis.

### 2. **Model Pipeline**
- Pulls data from the PostgreSQL database for preprocessing.
- Trains predictive models using the preprocessed financial data.
- Generates predictions to assist in making investment decisions.

---

## External sources and usage:
- EDGAR: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
  - Company facts and SEC filings
- Alpaca Market Data API: https://docs.alpaca.markets/docs/about-market-data-api
  - Historical stock price data
  - (maybe some other things from other endpoints)

---

## Project Structure

The repository is organized as follows:

### Project Root

---

### Configuration Files
- **`config/`**  
  Default database configuration to connect to the database
  - `db_default_config.yaml` — Database configuration settings.

### Model Storage
- **`models/`**  
  Directory to store trained models for inference and evaluation

### Exploration Notebooks
- **`notebooks/`**  
  Notebooks for data exploration, analysis, and experimentation.

### Pipelines
- **`pipelines/`**  
  Pipeline logic for data management and model inference workflows.

  - **`data_pipeline/`**  
    Handles data collection, storage, and retrieval:
    - `tasks/`
      - `fetch_data.py` — Fetch data from external sources.
      - `store_data.py` — Store data into the database.
      - `retrieve_data.py` — Retrieve data from the database.
    - `pipeline.py` — Runs the complete data pipeline.

  - **`model_pipeline/`**  
    Manages model inference and prediction workflows:
    - `tasks/`
      - `preprocess_data.py` — Preprocess data for inference.
      - `load_model.py` — Load trained models for inference.
      - `inference.py` — Perform inference on new data.
    - `pipeline.py` — Runs the complete model inference pipeline.

### Scripts
- **`scripts/`**  
  High-level scripts for running pipelines and training models.
  - `run_pipeline.py` — Executes the entire pipeline workflow.
  - `train_models.py` — Trains models using processed data.

### Source Code
- **`src/`**  
  Reusable utility functions and modules organized by functionality:
  - `data_fetching/` — Functions for fetching data from APIs or other sources.
  - `database/` — Functions for managing database connections and queries.
  - `preprocessing/` — Data preprocessing utilities.
  - `models/` — Model management and manipulation utilities.
  - `utils/` — Miscellaneous utility functions

### Tests
- **`tests/`**  
  Unit tests:
  - `db_tests.py` — Tests for database functionality.
  - `data_pipeline.py` — Tests for data pipeline.
  - `model_pipeline.py` — Tests for model pipeline.

### Other Files
- **`TEMPLATES/`** — Templates for .env files and documenting code for developers.
- **`Pipfile`** — Project dependency management.
- **`README.md`**
- **`Requirements.txt`**
- **`setup.py`** — Configuration for packaging and installing project modules.
- **`.gitignore`**