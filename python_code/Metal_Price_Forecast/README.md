 ## Metal Investment Forecast

![Metal Investment Forecast](https://github.com/remiyeku/Maverick-gold/blob/main/Data/Python_dashboad2.JPG)

## Introduction

The Metal Investment Analysis is a Streamlit application designed to analyze potential returns on investment for precious metals. It connects to a MySQL database, fetches historical metal prices, and uses a linear regression model to predict future prices. This tool helps users make informed investment decisions by providing insights into the expected returns on investments in Gold, Silver, Platinum, and Palladium.

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
- [`scikit-learn`](https://scikit-learn.org/)

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
# Update the following lines in main function
mydb = sql.connect(host='localhost', user='root', password='', port=3306, database='maverick', use_pure=True)
```

## Configuration

Before running the application, ensure that the MySQL database is properly configured and accessible. Review the script (`metal_investment_analysis.py`) and update the connection details as necessary.

## Usage

Run the Streamlit app:

```bash
streamlit run Metal_Prediction.py
```

Visit the provided URL in your web browser to interact with the Metal_Prediction.py.

## Contributing

Feel free to contribute to the development of this project. Create a fork, make your changes, and submit a pull request.

