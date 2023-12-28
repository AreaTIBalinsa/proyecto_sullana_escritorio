from View.Ui_inicioSistema import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *      
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import sistemaVentasVivo
import sistemaVentasBeneficiado
import serial
import time
import socket

# Importación de Base de Datos
import DataBase.database_conexion # El archivo database_conexion.py

# Puertos COM
COMAR = ""
COM1 = ""
COM2 = ""

appVentaBeneficiado = False
appVentaVivo = False
user_input_arduino = ""

""" Creamos hilo para la ejecución en segundo plano del Indicador , de esta forma
evitamos que la aplicación se detenga por la lectura constante """

class WorkerThread(QThread):
    update_peso = pyqtSignal(str)
    update_estado = pyqtSignal(str)
    update_baliza = pyqtSignal(str)
    def run(self):
        try:
            COMINDICADOR1 = "COM"+ COM1
            serialIndicador = serial.Serial(COMINDICADOR1, baudrate=9600, timeout=1)
            
            while True:
                result = serialIndicador.readline().decode('utf-8')
                if not result:
                    self.update_peso.emit("0.00")
                    self.update_estado.emit("0")   
                else:
                    #self.update_peso.emit(result[6:14])
                    self.update_peso.emit(result[2:10])
                    self.update_baliza.emit(result[2:10])
                    self.update_estado.emit("1")
        except Exception as e:
            print("WT IN"+str(e))
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()

""" Creamos hilo para la ejecución en segundo plano del Indicador, de esta forma
evitamos que la aplicación se detenga por la lectura constante """

class WorkerThread2(QThread):
    update_peso2 = pyqtSignal(str)
    update_estado2 = pyqtSignal(str)
    update_baliza2 = pyqtSignal(str)
    def run(self):
        try:
            COMINDICADOR2 = "COM"+ COM2
            serialIndicador2 = serial.Serial(COMINDICADOR2, baudrate=9600, timeout=1)
            
            while True:
                result2 = serialIndicador2.readline().decode('utf-8')
                print(result2)
                if not result2:
                    self.update_peso2.emit("0.00")
                    self.update_estado2.emit("0")   
                else:
                    #self.update_peso2.emit(result2[6:14])
                    self.update_peso2.emit(result2[2:10])
                    self.update_baliza2.emit(result2[2:10])
                    self.update_estado2.emit("1")
        except Exception as e:
            print("WT IN2"+str(e))  
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()   
        
""" Creamos hilo para la ejecución en segundo plano del Arduino, de esta forma
evitamos que la aplicación se detenga por la lectura constante  """

user_input_arduino = ""
            
class WorkerThreadAR(QThread):
    def run(self):
        try:
            COMARDUINO = "COM"+COMAR
            serialArduino = serial.Serial(COMARDUINO, baudrate=9600, timeout=1)
            
            while True:
                if user_input_arduino != "":
                    serialArduino.write(str(user_input_arduino).encode('utf8'))
        except Exception as e:
            print("WT AR"+str(e))
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()
        
""" Creamos hilo para la ejecución en segundo plano para subir los datos al servidor """

class WorkerThreadSubirDatosBase(QThread):
    # Tarea a ejecutarse cada determinado tiempo.
    def run(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            try:
                s.connect(("www.google.com", 80))
            except (socket.gaierror, socket.timeout):
                print("Sin conexión a internet")
            else:
                print("Con conexión a internet")
                try:
                    self.conexion = DataBase.database_conexion.Conectar()
                except Exception as e:
                    print(f"Error al interactuar con la base de datos: {e}")
                else:
                    s.close()
            time.sleep(12000)

# ===============================
# Creación de la Clase Principal
# ===============================

class InicioSistema(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.conexion = DataBase.database_conexion.Conectar()
        
        self.moduloVentasVivo = sistemaVentasVivo.Inicio()
        self.moduloVentasBeneficiado = sistemaVentasBeneficiado.Inicio()
        
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.ui.imgVentaBeneficiado.setPixmap(QPixmap("Imagenes/Pollo_Beneficiado.png"))
        self.ui.imgVentaVivo.setPixmap(QPixmap("Imagenes/Pollo_Vivo.png"))
        self.ui.lblmimizar.setPixmap(QPixmap("Imagenes/minimizar.png"))
        self.ui.lblcerrar.setPixmap(QPixmap("Imagenes/cerrar.png"))
        
        self.ui.btnCerrar.clicked.connect(self.fn_cerrarPrograma)
        self.ui.btnminimizar.clicked.connect(self.fn_minimizarPrograma)
        
        self.fn_declararPuertoIndicadores()
        
        self.worker = WorkerThread() # Hilo Balanza 1
        self.worker.start()
        self.worker.update_peso.connect(self.moduloVentasVivo.evt_actualizar_peso)
        self.worker.update_estado.connect(self.moduloVentasVivo.evt_actualizar_estado)
        self.worker.update_baliza.connect(self.moduloVentasVivo.evt_actualizar_baliza)
        
        self.worker.update_peso.connect(self.moduloVentasBeneficiado.evt_actualizar_peso)
        self.worker.update_estado.connect(self.moduloVentasBeneficiado.evt_actualizar_estado)
        self.worker.update_baliza.connect(self.moduloVentasBeneficiado.evt_actualizar_baliza)
        
        self.worker2 = WorkerThread2() # Hilo Balanza 2
        self.worker2.start()
        self.worker2.update_peso2.connect(self.moduloVentasVivo.evt_actualizar_peso2)
        self.worker2.update_estado2.connect(self.moduloVentasVivo.evt_actualizar_estado2)
        self.worker2.update_baliza2.connect(self.moduloVentasVivo.evt_actualizar_baliza2)
        
        self.worker2.update_peso2.connect(self.moduloVentasBeneficiado.evt_actualizar_peso2)
        self.worker2.update_estado2.connect(self.moduloVentasBeneficiado.evt_actualizar_estado2)
        self.worker2.update_baliza2.connect(self.moduloVentasBeneficiado.evt_actualizar_baliza2)
        
        self.fn_declararPuertoArduino()
        self.workerAR = WorkerThreadAR() # Hilo de Arduino
        self.workerAR.start() # Iniciamos el hilo
        
        self.fn_declararApiURL()
        self.fn_traerDatosServidor() 
        self.workerBase = WorkerThreadSubirDatosBase() # Actualización Base de Datos de Local a Servidor
        self.workerBase.start()
        
    def fn_traerDatosServidor(self):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.settimeout(5)
        try:
            s2.connect(("www.google.com", 80))
        except (socket.gaierror, socket.timeout):
            print("Sin conexión a internet")
        else:
            print("Con conexión a internet")
            try:
                time.sleep(3)
                print("Exito al interactuar con la base de datos")
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
            else:
                s2.close()
            
    def fn_declararApiURL(self):
        
        apiURL = self.conexion.db_seleccionaApiURL()
        DataBase.database_conexion.URLSERVIDOR = str(apiURL[0][0])
        DataBase.database_conexion.URLLOCAL = str(apiURL[0][1])  
        
    def fn_declararPuertoArduino(self):
        global COMAR
        
        puertoArduino = self.conexion.db_seleccionaPuertoArduino()
        COMAR = str(puertoArduino[0])
    
    def fn_declararPuertoIndicadores(self):
        global COM1
        global COM2
        
        puertoIndicadores = self.conexion.db_seleccionaPuertoIndicadores()
        COM1 = str(puertoIndicadores[0][0])
        COM2 = str(puertoIndicadores[0][1])
        
    def fn_cerrarPrograma(self):
        # Cerrar la instancia de Ventas en Vivo si existe
        if self.moduloVentasVivo and self.moduloVentasVivo.isVisible():
            self.moduloVentasVivo.close()

        # Cerrar la instancia de Ventas Beneficiado si existe
        if self.moduloVentasBeneficiado and self.moduloVentasBeneficiado.isVisible():
            self.moduloVentasBeneficiado.close()

        # Cerrar la ventana principal
        self.close()
    
    def fn_minimizarPrograma(self):
        self.showMinimized()

    # ======================== Eventos con el Teclado ========================
    
    def keyPressEvent(self, event):
              
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and appVentaVivo == True and appVentaBeneficiado == False:
            if not self.moduloVentasVivo:
                self.moduloVentasVivo = sistemaVentasVivo.Inicio()
            elif not self.moduloVentasVivo.isVisible():
                self.moduloVentasVivo.show()
            else:
                self.moduloVentasVivo.showNormal()
                self.moduloVentasVivo.activateWindow()
                
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and appVentaBeneficiado == True and appVentaVivo == False:
            if not self.moduloVentasBeneficiado:
                self.moduloVentasBeneficiado = sistemaVentasBeneficiado.Inicio()
            elif not self.moduloVentasBeneficiado.isVisible():
                self.moduloVentasBeneficiado.show()
            else:
                self.moduloVentasBeneficiado.showNormal()
                self.moduloVentasBeneficiado.activateWindow()
                
    def keyReleaseEvent(self, event):
        global appVentaBeneficiado
        global appVentaVivo
        
        if (event.key() == Qt.Key_Left):
            appVentaBeneficiado = True
            appVentaVivo = False
            self.ui.imgVentaBeneficiado.setStyleSheet("background-color: rgb(36, 211, 21);border-radius: 15px;border: 2px solid black;border-color: rgb(0, 0, 0);")
            self.ui.imgVentaVivo.setStyleSheet("background-color: transparent;border-radius: 15px;border: 2px solid black;border-color: rgb(0, 0, 0);")
            
        if (event.key() == Qt.Key_Right):
            appVentaVivo = True
            appVentaBeneficiado = False
            self.ui.imgVentaVivo.setStyleSheet("background-color: rgb(36, 211, 21);border-radius: 15px;border: 2px solid black;border-color: rgb(0, 0, 0);")
            self.ui.imgVentaBeneficiado.setStyleSheet("background-color: transparent;border-radius: 15px;border: 2px solid black;border-color: rgb(0, 0, 0);")
    
    # ======================== Termina eventos con el Teclado ========================
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = InicioSistema()
    gui.show()
    sys.exit(app.exec_())