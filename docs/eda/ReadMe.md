# Exploratory Data Analysis

## Dataset Overview

The ML dataset contains 6,435 weekly sales records across 45 stores from February 5, 2010 through October 26, 2012.

The dataset contains 16 features including:

- Store information
- Sales information
- Calendar features
- Holiday indicators
- Economic variables
- Historical sales features

## Key Findings

### Store-Level Sales

Weekly sales vary significantly between stores.

Store 20 has the highest average weekly sales, followed by stores 4, 14, 13, and 2.

Store-level behavior is therefore an important consideration for predictive modeling.

### Seasonality

Sales demonstrate noticeable seasonal behavior.

December has the highest average weekly sales, while January has the lowest.

This indicates that calendar features such as month, quarter, and week of year may provide useful predictive information.

### Holiday Impact

Holiday weeks have higher average sales than non-holiday weeks.

- Non-holiday average: approximately $1.04M
- Holiday average: approximately $1.12M

Holiday indicators will therefore be retained as model features.

### Historical Sales

Historical sales features have the strongest relationships with the target variable.

| Feature | Correlation |
|---|---:|
| Previous year sales | 0.986 |
| Previous week sales | 0.951 |
| Previous 2 weeks sales | 0.941 |
| Previous 4 weeks sales | 0.937 |

These features will be important candidates for the predictive model.

### Economic Variables

The linear correlations between weekly sales and economic variables are relatively weak.

However, these variables will initially be retained because nonlinear machine learning models may identify relationships that correlation analysis does not capture.

### Data Quality

No duplicate Store + Date records were found.

The missing historical lag values are expected because historical observations do not exist for the earliest records of each store.

These values should not automatically be replaced with zero.

## Modeling Considerations

Based on the EDA:

1. Store should be treated as a categorical variable.
2. Calendar features should be retained.
3. Historical sales features should be retained.
4. Holiday information should be retained.
5. Economic variables will initially be retained.
6. The dataset must be split chronologically to prevent future information from leaking into training data.
7. Lag features must be handled carefully during preprocessing.

## EDA Visualizations

The following visualizations were generated:

- `weekly_sales_trend.png`
- `monthly_sales.png`
- `store_sales.png`
- `previous_week_vs_current.png`
- `correlation_matrix.png`