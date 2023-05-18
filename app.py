from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'data'


# Define a function to execute MySQL queries
def run_query(query):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/', methods=['GET', 'POST'])
def air_quality():
    # Define the available dates
    if request.method == 'POST':
        selected_date = request.form['date']
        # Define the query to get the data for the selected date
        query = f"SELECT * FROM `{selected_date}`"
        try:
            # Execute the query and get the data
            data = run_query(query)
            # Render the template with the selected date and the data
            return render_template('crop-details.html', selected_date=selected_date, data=data)
        except:
            # If there is an error executing the query, render the template with an error message
            error_message = f"Could not find data for the selected date: {selected_date}"
            return render_template('crop-details.html', error_message=error_message)
    else:
        # If a GET request is made, render the template with no data
        return render_template('crop-details.html')

if __name__ == '__main__':
    app.run(debug=True)
