# Smart E-Commerce AI

An English-language Streamlit analytics project built around the DataCo Smart Supply Chain dataset. It includes delivery-risk classification and ensembles, weekly sales-value forecasting, customer segmentation, category association rules, and an explicitly simulated inventory-control exercise. It is an analytics demo, not an online store or production decision system.

## Dataset

This project uses **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS**, Version 5, hosted on [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cite the dataset authors/source and retain attribution when sharing derived work.

The supplied archive `8gx2fvg2k6-5.zip` contains the source CSV. Extract `DataCoSupplyChainDataset.csv` to `data/raw/DataCoSupplyChainDataset.csv`. `DescriptionDataCoSupplyChain.csv` is documentation only; `tokenized_access_logs.csv` is not used by this project. This complete project repository includes the source CSV, processed data, model artifacts, and generated reports for reproducibility. The raw source contains customer names, street addresses, and postal codes, so keep the GitHub repository private. Those fields are excluded from every processed table.

The dataset has 180,519 line-item rows, 65,752 unique orders, and spans 2015-01-01 through 2018-01-31. The validator checks those facts from the actual file each run rather than assuming fixed results. Processed artifacts exclude customer names, email, password, street address, and postal code. Delivery models exclude delivery outcome, actual shipping time, shipment date, and order status from predictors. Revenue uses DataCo's native numeric units; this project does not assert a currency.

## Windows installation

Use Python 3.11 and PowerShell. From this project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, invoke the venv interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Alternatively run `powershell -ExecutionPolicy Bypass -File .\setup.ps1` to create the environment and install dependencies. If `py -3.11` is not registered, install Python 3.11 from python.org, enable the Python Launcher, or edit `setup.ps1` to point to your interpreter.

## Prepare real data

After putting the CSV in `data/raw/`, run:

```powershell
python scripts/validate_data.py
python scripts/prepare_data.py
```

Validation writes `reports/data_quality.json`; preparation writes privacy-safe Parquet files to `data/processed/` plus `reports/dataset_profile.json` and `reports/prepare_quality.json`. Preparation keeps one row per order in the order table, one row per product line in the item table, and excludes canceled shipments from booked sales and baskets. No synthetic example data is generated.

## Train, evaluate, and launch

```powershell
python scripts/train_all.py --mode full
python scripts/evaluate_all.py
python -m pytest -q --basetemp=reports\pytest-tmp
python scripts/smoke_test.py
python -m streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`). `--mode quick` is for troubleshooting and reduces the delivery model set and simulation episodes; use `full` for the full model comparison. Training writes a real-data run manifest and records per-model errors instead of substituting fake scores.

## Dashboard and evidence

- **Delivery Predictor / Model Arena:** chronological train, validation, and test periods; logistic and tree models; regularized regression; bagging, voting, boosting, stacking, and optional XGBoost; metrics include average precision, ROC AUC, precision, recall, F1, balanced accuracy, Brier score, and fit/inference time.
- **Revenue Forecast Lab:** compares linear regression, polynomial Ridge, Ridge, Lasso, Elastic Net, Random Forest, Gradient Boosting, and naive baselines on later weeks. The target is weekly `Order Item Total` in native dataset units, excluding freight.
- **Customer Segmentation:** RFM, PCA, sampled LLE, and a reported DBSCAN parameter grid. Clusters are descriptive; noise is not churn or fraud.
- **Market Basket Explorer:** mines co-occurring product categories and reports support, confidence, and lift.
- **RL Inventory Simulator:** `SIMULATION — NOT HISTORICAL ACTION DATA`. DataCo provides no historical inventory, reorder actions, or rewards. The Q-learning agent and baseline policies run against a demand distribution estimated from the data and explicitly chosen reward assumptions.
- **Data Quality & About:** displays the observed source profile, preparation checks, and training manifest.

Reports and plots are written under `reports/`; trained inference pipelines and metadata are written under `artifacts/`. Important evidence includes `classification_metrics.csv`, `regression_metrics.csv`, `delivery_test_predictions.csv`, `revenue_test_predictions.csv`, `segmentation_summary.json`, `association_rules.csv`, and `rl_policy_comparison.csv`.

## Limitations

This dataset is historical and cannot establish current market behavior. Delivery classification is conditional on eligible shipment records and the source's `Late_delivery_risk` label. Predictive scores are associations, not causal claims. Weekly holdout performance does not guarantee future performance. RL results are simulated, not observed operating outcomes. See `docs/DATA_DICTIONARY.md`, `docs/LIMITATIONS.md`, model cards, and the dataset's own documentation for details.
