# Metal Investment Database Setup

This script sets up a MySQL database for metal investment analysis, creating three tables: `precious_metals`, `inflation_years`, and `metals_with_inflation`. It also populates these tables with data from CSV files and provides example queries.

## Introduction

Managing data for metal investment analysis involves creating a MySQL database with specific tables and populating them with relevant data. This script automates this process, ensuring a seamless setup for subsequent analysis and queries.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Example Queries](#example-queries)
6. [Dependencies](#dependencies)
7. [Contributing](#contributing)

## Prerequisites

Ensure you have the required Python modules installed:

- [mysql-connector](https://dev.mysql.com/doc/connector-python/en/)
- [pandas](https://pandas.pydata.org/)
- [csv](https://docs.python.org/3/library/csv.html)

```bash
pip install mysql-connector pandas
```

## Usage

1. **Clone the Repository:**

```bash
git clone https://github.com/remiyeku/Maverick-gold.git
cd Maverick-gold/Jupyter_Notebook/Economic_Indicators_Forecast
```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL Database:**

   Update the connection details in the script (`your_script.py`):

   ```python
   mydb = sql.connect(host='localhost', user='root', password='', port=3306, database='maverick', use_pure=True)
   ```

4. **Run the Script:**

   Execute the script to create tables and add data:

   ```bash
   python your_script.py
   ```

   The script will create the following tables:

   - `precious_metals`
   - `inflation_years`
   - `metals_with_inflation`

5. **Example Queries:**

   View sample queries to check the database:

   ```python
   # Example query to check precious_metals and inflation_years tables
   sqlquery = "SELECT p.date, p.year, p.gold, i.inflation FROM precious_metals AS p LEFT JOIN inflation_years AS i ON p.month = i.month LIMIT 5"
   mycursor.execute(sqlquery)
   result = mycursor.fetchall()
   for i in result:
       print(i)
   ```

   ```python
   # Example query to check metals_with_inflation table
   sqlquery = "SELECT p.year, p.gold, p.inflation FROM metals_with_inflation AS p LIMIT 10"
   mycursor.execute(sqlquery)
   result = mycursor.fetchall()
   for i in result:
       print(i)
   ```

## Dependencies

- [mysql-connector](https://dev.mysql.com/doc/connector-python/en/)
- [pandas](https://pandas.pydata.org/)

## Contributing

Feel free to contribute to the development of this project. Create a fork, make your changes, and submit a pull request.
