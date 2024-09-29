from PyQt6.QtWidgets import QMessageBox
import mysql.connector
import hashlib

def connect_to_database():
  connection = mysql.connector.connect(
      host="localhost",         
      user="root",        
      password="root", 
      database="password_manager"  
  )
  return connection


def get_data():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT username, motive, created_at FROM passwords"
        cursor.execute(query)
        result = cursor.fetchall() 

        if result:
            return result
        else:
            return None
        
    except mysql.connector.Error as e:
        show_message_box("Error", f"Ocurrió un error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_password_data(username, password):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT salt, hash_password FROM passwords WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone() 

        if result:
            stored_salt_hex, stored_hash_password = result
            stored_salt = bytes.fromhex(stored_salt_hex)
            password_hash = hashlib.sha256(stored_salt + password.encode('utf-8')).hexdigest()
            if password_hash == stored_hash_password:
                return True
            else:
                return False
        else:
            return False
        
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            show_message_box("Error", f"El nombre de usuario '{username}' ya está en uso. Por favor, elija otro.")
        else:
            show_message_box("Error", f"Ocurrió un error al almacenar la clave: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
 
def store_password(salt_hex, hashed_password, username, motive):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        insert_query = """INSERT INTO passwords (username, motive, salt, hash_password) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_query, (username, motive, salt_hex, hashed_password))
        connection.commit()
        show_message_box("Éxito", "La clave se almacenó correctamente.")
        
        return True

    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            show_message_box("Error", f"El nombre de usuario '{username}' ya está en uso. Por favor, elija otro.")
        else:
            show_message_box("Error", f"Ocurrió un error al almacenar la clave: {e}")
            
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
            
def show_message_box(title, message):
	msg_box = QMessageBox()
	msg_box.setWindowTitle(title)
	msg_box.setText(message)
	msg_box.exec()
