![Economic Forecast Dashboard](https://github.com/remiyeku/Maverick-gold/blob/main/Data/dashboard.JPG)

## Introduction

The Economic Forecast Dashboard is a Streamlit application designed to fetch economic data from a MySQL database, process the data, and visualize the forecasted economic indicators using SARIMA (Seasonal Autoregressive Integrated Moving Average) modeling. This project is a tool for forecasting and analyzing key economic indicators such as Inflation, Interest Rates, and GDP Growth.

## Table of Contents

1. [Dependencies](#dependencies)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Contributing](#contributing)

## Dependencies

The following Python libraries are used in this project:

- [`streamlit`](https://streamlit.io/)
- [`mysql-connector`](https://dev.mysql.com/doc/connector-python/en/)
- [`pandas`](https://pandas.pydata.org/)
- [`plotly`](https://plotly.com/)
- [`statsmodels`](https://www.statsmodels.org/stable/index.html)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/remiyeku/Maverick-gold.git
cd Maverick-gold/Jupyter_Notebook/Economic_Indicators_Forecast
```



### 2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure the MySQL database:

Set up your MySQL database with the appropriate credentials and schema. Update the database connection details in the script:

```python
# Update the following lines in EconomicForecastDashboard class
mydb = sql.connect(host='localhost', user='root', port=3306, database='maverick', use_pure=True)
```

## Configuration

Before running the application, ensure that the MySQL database is properly configured and accessible. Review the script (`Economic_Indicators_Forecast.py`) and update the connection details as necessary.

## Usage

Run the Streamlit app:

```bash
streamlit run Economic_Indicators_Forecast.py
```

Visit the provided URL in your web browser to interact with the Economic Forecast Dashboard.

## Contributing

Feel free to contribute to the development of this project. Create a fork, make your changes, and submit a pull request.
