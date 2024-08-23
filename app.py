from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Define the path for the CSV file
CSV_FILE = 'service_records.csv'

# Create the CSV file with headers if it does not exist
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'machine', 'component', 'parameter', 'value'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    machine = request.form.get('machine')
    component = request.form.get('component')
    parameter = request.form.get('parameter')
    value = request.form.get('value')
    
    # Determine the next ID based on the current contents of the CSV file
    next_id = 1
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) > 1:  # Skip header
                last_id = int(rows[-1][0])
                next_id = last_id + 1
    
    # Create a new record
    new_record = [next_id, machine, component, parameter, value]
    
    # Append the new record to the CSV file
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_record)

    return f"Record submitted: Machine={machine}, Component={component}, Parameter={parameter}, Value={value}"

if __name__ == "__main__":
    app.run(debug=True)
