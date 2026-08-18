# Source Data Dictionary

## Dataset

Walmart Store Sales Dataset

## Source

Kaggle

## File

Walmart.csv

## Dataset Size

- Rows: 6,435
- Columns: 8
- Stores: 45
- Missing values: 0
- Duplicate rows: 0

## Grain

One record represents weekly sales for a store on a specific date.

Candidate natural key:

`Store + Date`

## Columns

| Column | Source Type | Description | Nullable | Notes |
|---|---|---|---|---|
| Store | integer | Unique store identifier | No | 1–45 |
| Date | string | Week associated with the sales record | No | Will be standardized in Silver |
| Weekly_Sales | decimal | Weekly sales amount | No | Primary measure |
| Holiday_Flag | integer | Indicates whether the week is a holiday week | No | 0 = No, 1 = Yes |
| Temperature | decimal | Temperature during the week | No | External factor |
| Fuel_Price | decimal | Fuel price during the week | No | External factor |
| CPI | decimal | Consumer Price Index | No | Economic indicator |
| Unemployment | decimal | Unemployment rate | No | Economic indicator |

## Data Quality Observations

### Missing Values

No missing values were found across the eight columns.

### Duplicate Records

No completely duplicated records were found.

### Duplicate Store + Date

To be validated during profiling.

### Data Type Observations

The `Date` column is currently represented as a string and should be converted to a proper date type in the Silver layer.

### Potential Business Key

`Store + Date`