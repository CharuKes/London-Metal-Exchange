import streamlit as st
import mysql.connector as sql
import pandas as pd
import csv
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Function to create a table in the database
def create_table(cursor, table_name, columns):
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        create_table_query = f"CREATE TABLE {table_name} ({columns})"
        cursor.execute(create_table_query)
    except sql.Error as e:
        raise Exception(f"Error creating table: {e}")

# Function to insert data into a table in the database
def insert_data(cursor, table_name, columns, data):
    try:
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['%s' for _ in range(len(data[0]))])})"
        cursor.executemany(insert_query, data)
    except sql.Error as e:
        raise Exception(f"Error inserting data: {e}")

# Function to execute a SQL query and return the result
def execute_query(cursor, query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sql.Error as e:
        raise Exception(f"Error executing query: {e}")

# Function to predict prices using a machine learning model
def predict_prices(model, features):
    try:
        return model.predict(features)
    except Exception as e:
        raise Exception(f"Error predicting prices: {e}")

# Function to get the latest values of precious metals from the database
def get_latest_metal_values(cursor):
    query = "SELECT Gold, Silver, Platinum, Palladium, Date FROM precious_metals ORDER BY Year DESC, Month DESC LIMIT 1"
    cursor.execute(query)
    latest_values = cursor.fetchone()
    latest_values = list(latest_values)
    latest_values[-1] = pd.to_datetime(latest_values[-1])
    return tuple(latest_values)

# Function to print the current values of precious metals to the sidebar
def print_current_values(cursor):
    current_values = get_latest_metal_values(cursor)
    st.sidebar.write("Current values of precious metals:")
    st.sidebar.write(f"Gold: {current_values[0]:.2f}")
    st.sidebar.write(f"Silver: {current_values[1]:.2f}")
    st.sidebar.write(f"Platinum: {current_values[2]:.2f}")
    st.sidebar.write(f"Palladium: {current_values[3]:.2f}\n")
    return current_values

# Function to plot a chart of precious metals prices over time
def plot_chart(metal_data, future_dates):
    st.title('Precious Metals Prices Over Time')
    fig = go.Figure()

    for metal_name, metal_prices in metal_data.items():
        fig.add_trace(go.Scatter(x=metal_prices.index, y=metal_prices.values, mode='lines+markers', name=metal_name))

    fig.update_layout(xaxis_title='Year', yaxis_title='Price', template='plotly_dark', legend=dict(title='Metal'))
    st.plotly_chart(fig)

# Function to analyze the investment for each metal
def analyse_investment(cursor, table_name, metal_columns, investment_duration, seed_money, current_values):
    future_predictions_dict = {}
    try:
        query = f"SELECT * FROM {table_name}"
        data = execute_query(cursor, query)
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

        if investment_duration > 0:
            future_dates = pd.date_range(df['Date'].max() + timedelta(days=1), periods=investment_duration, freq='M')
            future_data = pd.DataFrame({'Year': future_dates.year, 'Month': future_dates.month})

            metal_data = {}
            for metal_column in metal_columns:
                features = df[['Year', 'Month']]
                target_column = metal_column
                X_train = features
                y_train = df[target_column]
                model = LinearRegression()
                model.fit(X_train, y_train)

                future_predictions = predict_prices(model, future_data[['Year', 'Month']])
                future_predictions_dict[metal_column] = future_predictions[-1]

                st.write(f"Predicted {target_column} price at the end of investment period: {future_predictions[-1]:.2f}")

                metal_data[metal_column] = pd.Series(future_predictions, index=future_dates)

            multiplier1 = (1 + ((future_predictions_dict['Gold'] - float(current_values[0])) / float(current_values[0])))
            multiplier2 = (1 + ((future_predictions_dict['Silver'] - float(current_values[1])) / float(current_values[1])))
            multiplier3 = (1 + ((future_predictions_dict['Platinum'] - float(current_values[2])) / float(current_values[2])))
            multiplier4 = (1 + ((future_predictions_dict['Palladium'] - float(current_values[3])) / float(current_values[3])))

            gold_return = seed_money * multiplier1
            silver_return = seed_money * multiplier2
            platinum_return = seed_money * multiplier3
            palladium_return = seed_money * multiplier4

            investment_months = investment_duration % 12
            investment_years = int(investment_duration / 12)

            st.write(f"\nYour ${seed_money} investment in {investment_years} Years and {investment_months} Months will result in:")
            st.write(f"${int(gold_return)} if invested in gold.")
            st.write(f"${int(silver_return)} if invested in silver.")
            st.write(f"${int(platinum_return)} if invested in platinum.")
            st.write(f"${int(palladium_return)} if invested in palladium.")

            plot_chart(metal_data, future_dates)

    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

# Function to get user input for the initial investment amount
def get_seed_money():
    try:
        return int(st.sidebar.text_input("What is your initial investment: "))
    except ValueError:
        st.sidebar.error("Invalid input. Please enter a valid number.")
        return 0

# Function to get user input for the investment duration
def get_investment_duration():
    try:
        investment_type = st.sidebar.radio("Do you want to invest in Months or Years?", options=['Months', 'Years'])
        if investment_type == 'Months':
            months = st.sidebar.number_input("Enter the number of Months you want to invest:", value=1, min_value=1)
            return months
        elif investment_type == 'Years':
            years = st.sidebar.number_input("Enter the number of Years you want to invest:", value=1, min_value=1)
            return int(years * 12)
    except ValueError:
        st.sidebar.error("Invalid input. Please enter a valid number.")
        return 0

# Main function to run the Streamlit app
def main():
    st.title("Metal Investment Analysis")

    try:
        # Connect to the MySQL database
        mydb = sql.connect(host='localhost', user='root', password='', port=3306, database='maverick', use_pure=True)
        mycursor = mydb.cursor()

        # Define columns for the precious_metals table
        precious_metals_columns = """
            Year INT,
            Month INT,
            Date DATE,
            Gold DECIMAL(10, 2),
            Silver DECIMAL(10, 2),
            Platinum DECIMAL(10, 2),
            Palladium DECIMAL(10, 2)
        """

        # Create the precious_metals table and insert data
        create_table(mycursor, 'precious_metals', precious_metals_columns)

        with open('Metal_Prices.csv', 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            next(csv_data)
            data_to_insert = [row for row in csv_data]

        insert_data(mycursor, 'precious_metals', 'Year, Month, Date, Gold, Silver, Platinum, Palladium', data_to_insert)

        metal_columns_to_predict = ['Gold', 'Silver', 'Platinum', 'Palladium']

        # Get user inputs for investment duration and initial investment amount
        investment_duration = get_investment_duration()
        current_values = print_current_values(mycursor)
        seed_money = get_seed_money()

        # Analyze the investment and display results
        analyse_investment(mycursor, 'precious_metals', metal_columns_to_predict, investment_duration, seed_money, current_values)

    except Exception as e:
        st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
