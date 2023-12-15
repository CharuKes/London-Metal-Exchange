# Precious Metals SQL Analysis

How to Use
Open SQL Workbench or your preferred SQL client.
Load the dataset (metals_with_inflation, inflation_years, etc.).
Open and execute the desired SQL file from this repository.

This repository contains SQL queries used to analyze historical data on precious metals including gold, silver, platinum, and palladium. The queries cover calculations for monthly percentage changes, inflation analysis, and volatility calculations.

## Query 1: Calculating Monthly Percentage Change

```sql
-- Monthly percentage change for each metal
SELECT 
    Year, 
    Month, 
    Gold, 
    Silver, 
    Platinum, 
    Palladium, 
    -- Percentage change calculations for each metal
FROM metals_with_inflation_interest_GDP;
```

## Query 2: Handling Initial Null Percentage Changes

```sql
-- CTE to handle initial null percentage changes
WITH PercentageChanges AS (
    -- Above Query Results as a CTE
)

-- Handling initial null values in percentage changes
SELECT 
    Year, 
    Month, 
    Gold, 
    Silver, 
    Platinum, 
    Palladium, 
    -- Coalesce and average calculations for initial null values
FROM PercentageChanges;
```

## Inflation Analysis

### Query 3: Calculating Average Inflation

```sql
-- Calculating average inflation
SELECT AVG(inflation) AS average_inflation 
FROM metals_with_inflation;
```

### Query 4: Selecting High and Low Inflation Years

```sql
-- Selecting years with inflation higher than average
SELECT * 
FROM inflation_years 
WHERE inflation > (SELECT AVG(inflation) FROM inflation_years);

-- Selecting years with inflation lower than average
SELECT * 
FROM inflation_years 
WHERE inflation < (SELECT AVG(inflation) FROM inflation_years);
```

## Volatility Calculations (1990-2023)

### Query 5: Calculating Volatility for Metals

```sql
-- Calculating monthly returns for each metal
SELECT 
    Year, 
    Month, 
    Date, 
    Gold, 
    Silver, 
    Platinum, 
    Palladium, 
    -- Calculating returns for each metal
FROM precious_metals;

-- Calculating standard deviation of returns for each metal
SELECT 
    STDDEV_POP(Gold_Return) AS Gold_Return_StdDev, 
    STDDEV_POP(Silver_Return) AS Silver_Return_StdDev, 
    STDDEV_POP(Platinum_Return) AS Platinum_Return_StdDev, 
    STDDEV_POP(Palladium_Return) AS Palladium_Return_StdDev 
FROM (
    -- Subquery to calculate returns for each metal
) subquery 
WHERE Gold_Return IS NOT NULL 
    AND Silver_Return IS NOT NULL 
    AND Platinum_Return IS NOT NULL 
    AND Palladium_Return IS NOT NULL;
