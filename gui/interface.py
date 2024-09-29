from utils.password_utils import *
import datetime
from storage.db_manager import *
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QLineEdit, QDialog

# Sintaxis de herencia ->  subclase(superclase)
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.password = ""
        
        self.setWindowTitle("Gestor de Claves")
        self.setGeometry(300, 300, 400, 300)

        self.buttonCreate = QPushButton("Generar Clave", self) 
        self.buttonCreate.clicked.connect(self.on_generate_password)
        self.buttonHash = QPushButton("Guardar clave", self)
        self.buttonHash.clicked.connect(self.on_password_to_hash) 
        self.buttonRecover = QPushButton("Comprobar clave", self)
        self.buttonRecover.clicked.connect(self.on_recover_password) 
        self.buttonGetData = QPushButton("Ver datos", self)
        self.buttonGetData.clicked.connect(self.on_get_data) 
        
        self.text_area_password = QTextEdit(self)
        self.text_area_password.setReadOnly(True)
        
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Usuario', 'Motivo', 'Creado'])
        self.table_widget.setVisible(False)  # La tabla está oculta al principio
        
        layout = QVBoxLayout()
        layout.addWidget(self.buttonGetData)
        layout.addWidget(self.buttonCreate)
        layout.addWidget(self.buttonHash)
        layout.addWidget(self.buttonRecover)
        layout.addWidget(self.text_area_password)
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_generate_password(self):
        self.password = generate_password()
        self.text_area_password.setText(self.password)


    def on_get_data(self):
        data = get_data()
        
        if data != None:
            self.table_widget.setVisible(True) 
            self.table_widget.setRowCount(len(data)) 
            
            for row_index, row in enumerate(data):
                if len(row) >= 3:
                    username = row[0]
                    motive = row[1]
                    created_at = row[2].strftime("%d/%m/%Y") 

                    self.table_widget.setItem(row_index, 0, QTableWidgetItem(username))
                    self.table_widget.setItem(row_index, 1, QTableWidgetItem(motive))
                    self.table_widget.setItem(row_index, 2, QTableWidgetItem(created_at))
        else:
            show_message_box("Sin datos", "No hay claves almacenadas para mostrar")


    def on_password_to_hash(self):
        if self.password:
            salt_hex, hashed_password = password_to_hash(self.password)  
            username_dialog = Username(self)
            if username_dialog.exec() == QDialog.DialogCode.Accepted:
                username, motive = username_dialog.get_data()
                if(store_password(salt_hex, hashed_password, username, motive)):
                    self.table_widget.clearContents() 
                    self.table_widget.setRowCount(0) 
                    self.text_area_password.clear()


    def on_recover_password(self):
        self.input_window = VerifyPassword()  
        self.input_window.show()

       

# QDialog permite que la ventana se comporte como un cuadro de diálogo modal y que se pueda esperar el resultado antes de continuar
class Username(QDialog): 
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Usuario")
        self.setGeometry(200, 200, 400, 200)

        self.username_label = QLabel("Ingrese un nombre de usuario: ", self)
        self.text_input_username = QLineEdit(self)
        
        self.motive_label = QLabel("Ingrese el destino de la clave (Por ejemplo, 'Banco Galicia'): ", self)
        self.text_input_motive = QLineEdit(self)

        self.button = QPushButton("Guardar", self)
        self.button.clicked.connect(self.on_save)

        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;") 

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.text_input_username)
        layout.addWidget(self.motive_label)
        layout.addWidget(self.text_input_motive)
        layout.addWidget(self.error_label)  
        layout.addWidget(self.button)

        self.setLayout(layout)


    def on_save(self):
        username = self.text_input_username.text()
        motive = self.text_input_motive.text()

        # Limpiar cualquier mensaje de error previo
        self.error_label.setText("")

        if username and motive:
            self.accept() 
        else:
            # Mostrar un mensaje de error si el campo está vacío
            self.error_label.setText("Este campo es obligatorio.")


    def get_data(self):
        return self.text_input_username.text(), self.text_input_motive.text()
            
              
class VerifyPassword(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscar contraseña")
        self.setGeometry(300, 300, 400, 200)

        self.label_user = QLabel("Ingrese el usuario:", self)
        self.text_input_user = QLineEdit(self)
        
        self.label_password = QLabel("Ingrese la clave:", self)
        self.text_input_password = QLineEdit(self)
        # self.text_input_user.setEchoMode(QLineEdit.EchoMode.Password)  # Para ocultar la entrada

        self.button = QPushButton("Enviar", self)
        self.button.clicked.connect(self.on_check_password)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.text_input_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.text_input_password)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    

    def on_check_password(self):
        username = self.text_input_user.text()
        password = self.text_input_password.text()
        
        if(get_password_data(username, password)):
            show_message_box("Aceptado", "Los datos son correctos")
        else:
            show_message_box("Error", "Alguno de los datos no es correcto")
            
        self.close()
