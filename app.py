from flask import Flask, render_template, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def get_average_moisture():
    data = get_sensor_data()
    moistureSum = 0
    count = 0
    for record in data:
        if 'soil_moisture' in record:
            moistureSum += record['soil_moisture']
            count += 1
    if count == 0:
        return 0  # Avoid division by zero
    print(moistureSum)
    return moistureSum / count

    
def get_average_temperature():
    data = get_sensor_data()
    temperatureSum = 0
    count = 0
    for record in data:
        if 'temperature' in record:
            temperatureSum += record['temperature']
            count += 1
    if count == 0:
        return 0  # Avoid division by zero
    return round((temperatureSum / count), 2)

def get_average_humidity():
    data = get_sensor_data()
    humiditySum = 0
    count = 0
    for record in data:
        if 'humidity' in record:
            humiditySum += record['humidity']
            count += 1
    if count == 0:
        return 0  # Avoid division by zero
    return round((humiditySum / count), 2)

def get_sensor_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="drip_irrigation"
    )
    cursor = conn.cursor(dictionary=True)
    # cursor.execute("SELECT * FROM sensor_data")
    # cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 20")
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 20")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# @app.route('/sensor_data')
# def sensor_data():
#     # data = get_sensor_data()
#     # return jsonify(data)
#     data = get_sensor_data()
#     for record in data:
#         i = 1
#         record['created_at'] = i
#         record['temperature'] = round(record['temperature'], 2)
#         i += 1
#     return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/dashboard')
def dashboard():
    data = get_sensor_data()
    avg_moisture = get_average_moisture()
    avg_temperature = get_average_temperature()
    avg_humidity = get_average_humidity()

    for i in range(20):
        data[i]['timestamp'] = datetime.strftime(data[i]['timestamp'], '%Y-%m-%d %H:%M:%S')

    print(data[0])
    data1 = []
    for i in range(20):
        data1.append((data[i]['timestamp'], data[i]['soil_moisture']))

    labels1 = []
    values1 = []
    values2 = []
    values3 = []

    for i in range(20):
        labels1.append(data[i]['timestamp'])
        values1.append(data[i]['soil_moisture'])
        values2.append(data[i]['temperature'])
        values3.append(data[i]['humidity'])

    return render_template(template_name_or_list='dashboard.html', data=data, avg_moisture=avg_moisture, avg_temperature=avg_temperature, avg_humidity=avg_humidity, labels1=labels1, values1=values1, values2=values2, values3=values3)

if __name__ == '__main__':
    app.run(debug=True)