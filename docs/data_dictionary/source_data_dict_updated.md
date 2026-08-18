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
- Records per store: 143
- Missing values: 0
- Duplicate rows: 0
- Duplicate Store + Date keys: 0

## Date Coverage

- Start Date: 2010-02-05
- End Date: 2012-10-26

## Grain

One record represents the weekly sales for one store on a specific date.

### Natural Key

`Store + Date`

The combination of Store and Date uniquely identifies each record.

## Columns

| Column | Source Type | Description | Nullable | Notes |
|---|---|---|---|---|
| Store | integer | Unique store identifier | No | 45 stores, IDs 1–45 |
| Date | string | Week associated with the sales record | No | Converted to DATE in Silver |
| Weekly_Sales | decimal | Weekly sales amount | No | Primary business measure |
| Holiday_Flag | integer | Indicates whether the week is a holiday week | No | 0 = No, 1 = Yes |
| Temperature | decimal | Temperature during the week | No | External factor |
| Fuel_Price | decimal | Fuel price during the week | No | External factor |
| CPI | decimal | Consumer Price Index | No | Economic indicator |
| Unemployment | decimal | Unemployment rate | No | Economic indicator |

## Data Quality Findings

### Missing Values

No missing values were found.

### Duplicate Records

No completely duplicated records were found.

### Duplicate Store + Date Keys

No duplicate Store + Date combinations were found.

### Record Distribution

All 45 stores contain exactly 143 weekly records.

This confirms a consistent record distribution across stores.

### Data Type Observations

The `Date` column is currently represented as a string and will be converted to a proper DATE type in the Silver layer.