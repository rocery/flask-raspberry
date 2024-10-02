from flask import Flask, render_template, Response, jsonify, request, redirect, url_for, flash
from facerec import predict, show_labels_on_image
import face_recognition
from read_data import *
import schedule
from uploads import *
from mysql_process import *
import cv2
import csv
import os
import time

app = Flask(__name__)
app.secret_key = 'itbekasioke'  # Necessary for using flash messages
app.config['UPLOAD_FOLDER'] = 'uploads/train'

# Path to the CSV file
CSV_FILE_PATH = 'static/data/data.csv'
CSV_FILE_PATH_GROUP = 'static/data/group_data.csv'
CSV_FILE_PATH_AUTOMATE = 'static/data/data__.csv'
CSV_TEMP__ = 'static/data/temp__.csv'

# Ensure the CSV file exists and has the correct headers
if not os.path.exists(CSV_FILE_PATH):
    with open(CSV_FILE_PATH, mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Category', 'Time'])

if not os.path.exists(CSV_FILE_PATH_GROUP):
    with open(CSV_FILE_PATH_GROUP, mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Time'])

if not os.path.exists(CSV_FILE_PATH_AUTOMATE):
    with open(CSV_FILE_PATH_GROUP, mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['NIP', 'Name', 'Time'])

if not os.path.exists(CSV_TEMP__):
    with open(CSV_TEMP__, mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['NIP', 'Name', 'Time'])

# Root index       
@app.route('/')
def index():
    return render_template('index.html')

# OCR Route
@app.route('/ocr')
def ocr():
    return render_template('ocr/index.html')

@app.route('/ocr/plat_number')
def plat_number():
    return render_template('ocr/index.html')

# Route Face_Recognition Index
@app.route('/face_recognition')
def face_recognition_home():
    return render_template('face_recognition/index.html')

#Route Single Facerec
@app.route('/face_recognition/facerec')
def facerec():
    data_csv = read_csv(CSV_FILE_PATH)
    return render_template('face_recognition/facerec.html', data_csv = data_csv)

@app.route('/face_recognition/facerec_')
def facerec_():
    # data_csv = read_csv(CSV_FILE_PATH)
    ip_address = get_external_ip()
    
    # read_data_from_db
    data = read_presensi()
    if data == False:
        data = read_csv(CSV_FILE_PATH)
    
    return render_template('face_recognition/facerec_.html', data_csv=data, ip_address=ip_address)

@app.route('/face_recognition/facerec__')
def facerec__():
    # data_csv = read_csv(CSV_FILE_PATH)
    last_index = []
    try:
        with open(CSV_FILE_PATH_AUTOMATE, 'r') as file:
            reader = reversed(list(csv.reader(file)))
            last_row = next(reader)
            last_index = last_row[1]
    except:
        pass
    ip_address = get_external_ip()
    
    # read_data_from_db
    # Disable for local test
    # data = read_presensi()
    # if data == False:
    data = read_csv(CSV_FILE_PATH_AUTOMATE)
    #last_index = "-"
    return render_template('face_recognition/facerec__.html', data_csv=data, ip_address=ip_address, last_index=last_index)

#Route Group Facerec
@app.route('/face_recognition/facerec_group')
def facerec_group():
    with open(CSV_FILE_PATH_GROUP, 'r') as file:
        reader = reversed(list(csv.reader(file)))
        last_row = next(reader)
        last_index = last_row[0]
    data_csv = read_csv_group(CSV_FILE_PATH_GROUP)
    return render_template('face_recognition/facerec_group.html', data_csv = data_csv, last_index = last_index)

@app.route('/submit_facerec', methods=['POST'])
def submit_facerec():
    if request.method == 'POST':
        # Get data from the form
        time_category = request.form.get('time_category')
        name_input = request.form.get('name_input')
        time_str = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        
        if name_input in ['-', '', 'Tidak Dikenali', 'Tidak Terdeteksi', 'Palsu', 'Lebih dari Satu Wajah'] or 'Palsu' in name_input:
            flash(f"Data terdeteksi salah")
            return redirect(url_for('facerec'))           
        else:
            # Save data to CSV
            with open(CSV_FILE_PATH, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name_input, time_category, time_str])
            flash(f"Berhasil! Nama: {name_input}, Kategori: {time_category}, Waktu: {time_str}")
            return redirect(url_for('facerec'))
        
    else:
        flash("Error, data terdeteksi tidak ada, silahkan ulangi proses Face Recognition")
        return redirect(url_for('facerec'))
    
@app.route('/submit_facerec_', methods=['POST'])
def submit_facerec_():
    if request.method == 'POST':
        # Get data from the form
        time_category = request.form.get('time_category')
        name_input = request.form.get('name_input')
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        if name_input in ['-', '', 'Tidak Dikenali', 'Tidak Terdeteksi', 'Palsu', 'Lebih dari Satu Wajah', 'Face Recognition'] or 'Palsu' in name_input:
            flash(f"Data terdeteksi salah", "danger")
            return redirect(url_for('facerec_'))
            
        else:
            # Save data to CSV
            with open(CSV_FILE_PATH, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name_input, time_category, time_str])
            
            # Save data to MySQL
            nip = "-"
            data = insert_presensi(nip, name_input, time_category, time_str)
            if data:
                flash(f"Berhasil! Nama: {name_input}, Kategori: {time_category}, Waktu: {time_str}")
            else:
                flash("Data Gagal Disimpan ke Database. Mohon Hubungi IT")
                
            return redirect(url_for('facerec_'))
        
    else:
        flash("Error, data terdeteksi tidak ada, silahkan ulangi proses Face Recognition")
        return redirect(url_for('facerec_'))

@app.route('/submit_facerec__', methods=['POST'])
def submit_facerec__():
    if request.method == 'POST':
        # Get data from the form
        # time_category = request.form.get('time_category')
        name_input = request.form.get('name_input')
        nip = request.form.get('nip_input')
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time_category = "-"
        
        # save_image()
        
        if name_input in ['-', '', 'Tidak Dikenali', 'Tidak Terdeteksi', 'Palsu', 'Lebih dari Satu Wajah', 'Face Recognition'] or 'Palsu' in nip:
            flash("Data terdeteksi salah", "danger")
            return redirect(url_for('facerec__'))
            
        else:
            try:
                # Save data to CSV
                with open(CSV_FILE_PATH_AUTOMATE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nip, name_input, time_str])
                
                with open(CSV_TEMP__, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nip, name_input, time_str])
                
                flash(f"Berhasil! Nama: {name_input}, Kategori: {time_category}, Waktu: {time_str}", "success")
            except:
                flash("Data Gagal Disimpan ke Database. Mohon Hubungi IT", "danger")
                
            # # Save data to MySQL
            # data = insert_presensi(nip, name_input, time_category, time_str)
            # if data:
            #     flash(f"Berhasil! Nama: {name_input}, Kategori: {time_category}, Waktu: {time_str}", "success")
            # else:
            #     flash("Data Gagal Disimpan ke Database. Mohon Hubungi IT", "danger")
            
            return redirect(url_for('facerec__'))
        
    else:
        flash("Error, data terdeteksi tidak ada, silahkan ulangi proses Face Recognition")
        return redirect(url_for('facerec__'))
    
def insert_facerec_automatic():
    with open(CSV_TEMP__, mode='r') as file:
        reader = csv.reader(file)
    

@app.route('/group_submit_facerec', methods=['POST'])
def group_submit_facerec():
    if request.method == 'POST':
        # Get data from the form
        name_input = request.form.get('name_input')
        time_str = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        
        # Save data to CSV
        with open(CSV_FILE_PATH_GROUP, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name_input, time_str])
        return redirect(url_for('facerec_group'))
        
    else:
        flash("Error, data terdeteksi tidak ada, silahkan ulangi proses Face Recognition")

# in Raspberry Pi, use index camera won't work
camera = '/dev/video0'
# dev/video0
cap = cv2.VideoCapture(camera)
predictions = []
def generate_frames():
    process_this_frame = 14
    while True:
        # Baca frame dari webcam
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode frame ke format JPEG
            img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            process_this_frame = process_this_frame + 1
            
            if process_this_frame % 15 == 0:
                faceloc = face_recognition.face_locations(img)
                if len(faceloc) > 0:
                    time.sleep(0.5)
                global predictions
                predictions = predict(img, model_path="static/clf/trained_knn_model.clf")
                print(predictions)
            frame = show_labels_on_image(frame, predictions)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Hasilkan frame sebagai aliran byte
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Rute untuk streaming video dengan deteksi wajah
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pred')
def pred():
    # Initialize name_ to a default value
    name_ = "Face Recognition"
    nip_ = "NIP"
    # Initialize name_ outside the loop
    for name, _, _, _ in predictions:
        if name:
            try:
                name_, nip_ = name.rsplit('_', 1)
            except:
                name_ = name
        # If you want to break after the first non-empty name, you can use:
        # if name:
        #     name_ = name
        #     break

    return jsonify({'name_': name_, 'nip_': nip_})

@app.route('/group_pred')
def group_pred():
    names = []
    for name, _ in predictions:
        if name is not None:
            names.append(name)
    return jsonify({'names': names})

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        images = request.files.getlist('images')
        
        # Validasi input
        if not name or not id or not images:
            flash('Semua form harus diisi', 'danger')
            return redirect(request.url)
        
        if not "".join(name.split()).isalpha():
            flash('Nama harus berupa huruf alfabet. Nama yang diinput: {}'.format(name), 'danger')
            return redirect(request.url)

        if not id.isdigit():
            flash('ID harus berupa angka. ID yang diinput: {}'.format(id), 'danger')
            return redirect(request.url)

        # Validasi format gambar
        for image in images:
            if not allowed_file(image.filename):
                flash('Format gambar yang diinput harus JPG, JPEG, atau PNG', 'danger')
                return redirect(request.url)

        formatted_name = format_name(name)
        folder_name = f"{formatted_name}_{id}"
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        
        save_image(images, folder_path)
        flash('Data {} berhasil disimpan'.format(folder_name), 'success')
        return redirect(url_for('uploads'))
    
    folders_info = get_folders_info(app.config['UPLOAD_FOLDER'])
    return render_template('uploads.html', folders_info=folders_info)

def insert_data_to_db():
    try:
        # MySQL connection setup
        db_connection = mysql.connector.connect(
            host="192.168.15.223",
            user="admin",
            password="itbekasioke",
            database="face_recognition"
        )
        cursor = db_connection.cursor()

        # Read CSV file
        with open(CSV_TEMP__, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                nip = row['NIP']
                name = row['Name']
                date = row['Time']

                # Insert data into MySQL
                cursor.execute(
                    "INSERT INTO presensi (nip, name, date) VALUES (%s, %s, %s)",
                    (nip, name, date)
                )
            db_connection.commit()

        # Close the database connection
        cursor.close()
        db_connection.close()

        # If successful, remove the CSV file
        os.remove(CSV_TEMP__)
        print("Data inserted successfully and CSV file deleted.")
        
        if not os.path.exists(CSV_TEMP__):
            with open(CSV_TEMP__, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerow(['NIP', 'Name', 'Time'])

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
# Schedule the task to run every hour
schedule.every(1).minutes.do(insert_data_to_db)


# @app.route('/button_status', methods=['GET'])
# def button_status():
#     button_login_status = GPIO.input(BUTTON_LOGIN)
#     button_logout_status = GPIO.input(BUTTON_LOGOUT)
#     return jsonify({
#         'button_login': 'HIGH' if button_login_status == GPIO.HIGH else 'LOW',
#         'button_logout': 'HIGH' if button_logout_status == GPIO.HIGH else 'LOW'
#     })

if __name__ == '__main__':
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)
        
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    app.run(host='0.0.0.0', port=5000, threaded=True)
