from flask import Blueprint, render_template, jsonify, request, make_response
from flask_login import login_required, current_user
from . import db
import sqlite3
import project.log as log

ts = log.dato()
DATABASE = 'data.db'
main = Blueprint('main', __name__)


@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)

@main.route('/list')
@login_required
def list():
    return render_template('list.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@main.route('/get_configurations', methods=['GET'])
def get_configurations():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM indeks")
    rows = c.fetchall()
    configurations = [{'deviceID': row[0], 'address': row[1]} for row in rows]
    conn.close()
    return jsonify(configurations)



@main.route('/add_device', methods=['POST'])
def add_device():
    device_id = request.form['deviceID']
    address = request.form['address']
    log.create_table(device_id)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO indeks (Device_ID, Address) VALUES (?, ?)", (device_id, address))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.Error as e:
        print("Failed to add device configuration:", e)
        conn.rollback()
        conn.close()
        return jsonify({'success': False})
    


@main.route('/delete_device', methods=['POST'])
def delete_device():
    device_id = request.form['deviceID']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM indeks WHERE Device_ID=?", (device_id,))
        c.execute(f'DROP TABLE IF EXISTS {device_id}')
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.Error as e:
        print("Failed to delete device configuration:", e)
        conn.rollback()
        conn.close()
        return jsonify({'success': False})
    


@main.route('/edit_device', methods=['POST'])
def edit_device():
    device_id = request.form['deviceID']
    new_device_id = request.form['newDeviceID']
    address = request.form['address']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("UPDATE indeks SET Device_ID=?, Address=? WHERE Device_ID=?", (new_device_id, address, device_id))
        c.execute(f"ALTER TABLE {device_id} RENAME TO {new_device_id}")
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.Error as e:
        print("Failed to edit device configuration:", e)
        conn.rollback()
        conn.close()
        return jsonify({'success': False})
    



@main.route('/get_latest_percentage_data')
def get_latest_percentage_data():
    bin_id = request.args.get('bin')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT percentage FROM {} ORDER BY id DESC LIMIT 1".format(bin_id))
    percentage_data = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify(percentage_data)




@main.route('/get_percentage_data')
def get_percentage_data():
    bin_id = request.args.get('bin')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT percentage FROM {} ORDER BY id DESC LIMIT 1".format(bin_id))
    percentage_data = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    response = make_response(jsonify(float(percentage_data)))

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response




@main.route('/api/data', methods=['POST'])
def receive_data():
	data = request.get_json()
	if 'sensor_id' in data and 'percentage' in data:
		sensor_id = data['sensor_id']
		percentage = data ['percentage']

		if isinstance(sensor_id, str) and isinstance(percentage, int) and 0 <= percentage <=100:
			print('hej')
			log.logdata(sensor_id, ts, percentage)
		else:
			return 'invalid data format or values', 400
	else:
		return 'missing required fields', 400

	return 'Data received successfully'
def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS indeks (Device_ID TEXT PRIMARY KEY, Address TEXT)')
    conn.commit()
    conn.close()