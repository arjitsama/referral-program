# Data Engineer Referral Pipeline  
Python ETL pipeline that profiles referral data, applies fraud-detection rules, and outputs a validated referral rewards report.

---

## 📁 Project Structure
- `main.py` — main pipeline script (load, clean, process, fraud detection, output)  
- `requirements.txt` — dependencies  
- `Dockerfile` — containerization setup  
- `data/` — input CSVs (mounted at runtime, not baked into image)  
- `output/` — final report (mounted at runtime)  
- `profiling/` — profiling reports (mounted at runtime)  
- `docs/` — documentation, including Data Dictionary  

---

## ⚙️ Setup (Local Run)

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline:
   ```bash
   python main.py --input_dir data --output_dir output --profile_dir profiling
   ```

## 🐳 Setup with Docker
1. Install Dependencies:
   ```bash
   docker build -t referral-app .
   ```
2. Run the pipeline:
   ```bash
   docker run --rm \
      -v "$PWD/data":/app/data:ro \
      -v "$PWD/output":/app/output \
      -v "$PWD/profiling":/app/profiling \
      referral-app
   ```
  

## 📊 Outputs
   - `profiling/*.csv` — profiling reports (null counts, distinct values, dtypes)
   - `output/referral_report.csv` — final report with 46 rows and columns:
      - referral details, referrer/referee info, status, reward/transaction info, validity flag
