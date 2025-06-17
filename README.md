## 📁 Data Format Requirements

For theThis project expects input data in the following format:

- A separate `.csv` file for each asset (e.g., `META_Data.csv`, `GOOG_Data.csv`)
- Each file must contain at least the following columns:
  - `Date` — format: `YYYY-MM-DD`
  - `Close/Last` — daily adjusted close price

Files must be stored in a local path (modify this in `src/Get_Market_Data.py`):
