import mysql.connector
from mysql.connector import Error
# Replace with your MySQL database connection details

def insert_presensi(nip, name, category, date):
    try:
        connection = mysql.connector.connect(
            host='192.168.10.223',
            database='face_recognition',
            user='admin',
            password='itbekasioke'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = (
                "INSERT INTO presensi (nip, name, category, date) "
                "VALUES (%s, %s, %s, %s)"
            )
            data = (nip, name, category, date)
            cursor.execute(query, data)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        else:
            return False
    except Error as e:
        return False

def read_presensi():
    try:
        connection = mysql.connector.connect(
            host='192.168.10.223',
            database='face_recognition',
            user='admin',
            password='itbekasioke'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = (
                "SELECT name, category, date "
                "FROM `presensi` "
                "ORDER BY `date` "
                "DESC LIMIT 3"
            )
            cursor.execute(query)
            records = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            result = []
            for row in records:
                result.append([row[0], row[1], row[2]])
            
            return result
        else:
            return False
    except Error as e:
        return False
    
# if __name__ == "__main__":
#     nip = 2
#     name = 'Sastra'
#     category = 'IN'
#     date = '2023-05-01 10:00:00'
#     data = insert_presensi(nip, name, category, date)
#     print(data)