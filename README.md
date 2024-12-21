# TradePulse

## Repository Structure: Tradepulse

Below is an overview of the directory structure for the **Tradepulse** project.

### Project Root

---

### Configuration Files
- **`config/`**  
  Configuration files for managing database settings
  - `db_default_config.yaml` — Database configuration settings.

---

### Model Storage
- **`models/`**  
  Directory to store trained models for inference and evaluation

---

### Exploration Notebooks
- **`notebooks/`**  
  Notebooks for data exploration, analysis, and experimentation.

---

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

---

### Scripts
- **`scripts/`**  
  High-level scripts for running pipelines and training models.
  - `run_pipeline.py` — Executes the entire pipeline workflow.
  - `train_models.py` — Trains models using processed data.

---

### Source Code
- **`src/`**  
  Reusable utility functions and modules organized by functionality:
  - `data_fetching/` — Functions for fetching data from APIs or other sources.
  - `database/` — Functions for managing database connections and queries.
  - `preprocessing/` — Data preprocessing utilities.
  - `models/` — Model management and manipulatino utilities.
  - `utils/`
    - `env_utils.py` — Handles environment variables and project root utilities.

---

### Tests
- **`tests/`**  
  Unit tests:
  - `db_tests.py` — Tests for database functionality.
  - `data_pipeline.py` — Tests for data pipeline.
  - `model_pipeline.py` — Tests for model pipeline.

---

### Other Files
- **`.gitignore`**
- **`Pipfile`** — Manage project dependencies using Pipenv.
- **`README.md`** — Project overiew.
- **`setup.py`** — Configuration for packaging and installing project modules.