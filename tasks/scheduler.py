import time
import mysql.connector
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QMessageBox, QApplication

conn = None

def connect_to_database():
  connection = mysql.connector.connect(
      host="localhost",         
      user="root",       
      password="rootPass06", 
      database="password_manager"  
  )
  return connection

def connect_db():
    global conn
    conn = connect_to_database() 
    return conn


def check_passwords():
    global conn
    cursor = conn.cursor()
    six_months_ago = datetime.now() - timedelta(days=6*30)
    warning_date = six_months_ago + timedelta(days=3)
    cursor.execute("SELECT motive, created_at FROM passwords WHERE created_at <= %s", (warning_date,))
    results = cursor.fetchall()
    if results:
        for motive, created_at in results:
            created_at = created_at.strftime("%d/%m/%Y") 
            display_alert(motive, created_at)


def display_alert(motive, created_at):
    app = QApplication([]) 
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Clave por vencer")
    msg.setText(f"La clave para {motive} está por vencer.\nFecha de creación: {created_at}")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec() 
    app.quit() 
    

if __name__ == "__main__":
    connect_db()
    check_passwords()