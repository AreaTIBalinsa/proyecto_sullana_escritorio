# Importación de Librerias
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime
from PyQt5.QtGui import QPixmap
import time
import serial
import psutil
import win32print
from datetime import datetime
import socket
from PyQt5.QtGui import QMovie
import threading
import json

# Importación de los Layout
from View.Ui_sistemaVentas import Ui_MainWindow # La clase Ui_MainWindow del archivo ui_Principal.py 

# Importación de Base de Datos
import DataBase.database_conexion # El archivo database_conexion.py

# Puertos COM
COMAR = ""

# BalanzaSeleccionada
balanzaSeleccionada = 1

# Contraseña para eliminar
passwordEliminar = ""

# Variables para selección de Clientes
listCodCliente = []
listGrupoCliente = []
listEstadoCliente = []
indexLista = 0

# Variables para las luces de las Balanzas
pesoBalanza1 = False
pesoBalanza2 = False

# Id de cada Especie
primerEspecie = 0
segundaEspecie = 0
terceraEspecie = 0
cuartaEspecie = 0
quintaEspecie = 0
sextaEspecie = 0
septimaEspecie = 0
octavaEspecie = 0
novenaEspecie = 0
decimaEspecie = 0
decimaPrimeraEspecie = 0
decimaSegundaEspecie = 0
decimaTerceraEspecie = 0
decimaCuartaEspecie = 0
decimaQuintaOtrasEspecies = 0

# Nombre de cada Especie
nombrePrimerEspecie = ""
nombreSegundaEspecie = ""
nombreTerceraEspecie = ""
nombreCuartaEspecie = ""
nombreQuintaEspecie = ""
nombreSextaEspecie = ""
nombreSeptimaEspecie = ""
nombreOctavaEspecie = ""
nombreNovenaEspecie = ""
nombreDecimaEspecie = ""
nombreDecimaPrimeraEspecie = ""
nombreDecimaSegundaEspecie = ""
nombreDecimaTerceraEspecie = ""
nombreDecimaCuartaEspecie = ""
nombreDecimaQuintaOtrasEspecies = ""

# Variables de Clientes por Balanza
codCliente1 = 0
codCliente2 = 0
especieCli1 = 0
especieCli2 = 0
especieDesCli1 = 0
especieDesCli2 = 0

# Variables de Precio
precioPrimerEspecie = 0
precioSegundaEspecie = 0
precioTerceraEspecie = 0
precioCuartaEspecie = 0
precioQuintaEspecie = 0
precioSextaEspecie = 0
precioSeptimaEspecie = 0
precioOctavaEspecie = 0
precioNovenaEspecie = 0
precioDecimaEspecie = 0
precioDecimaPrimeraEspecie = 0
precioDecimaSegundaEspecie = 0
precioDecimaTerceraEspecie = 0
precioDecimaCuartaEspecie = 0
precioDecimaQuintaOtrasEspecies = 0

# Variables de Nombres de Cliente por Balanza
nombresCliBalanza = ""
nombresCliBalanza1 = ""
nombresCliBalanza2 = ""

# Variables bandera
frmRegistrarCantidad = False
frmAlertaEliminarPeso = False
frmEliminarPeso = False
frmAlerta = False
frmRegistrarDescuento = False
frmEditarCantidad = False
frmInicioProceso = False
frmRegistrarJabas = False
frmRegistrarDescuentoCan = False
frmEditarCantidadTara = False
frmEditarCantidadDescuento = False

# Variables para la Base de Datos
codCliente = 0
numProceso = 0
precioCliente = 0
pesoNetoJabas = 0
taraCliente = 0
idEspecie = 0
pesoNeto = 0
horaPeso = datetime.now().strftime('%H:%M:%S')
fechaPeso = datetime.now().strftime('%Y-%m-%d')
cantidadRegistro = 0
numJabas = 0
estadoPeso = 1
estadoWebPeso = 1
coloresJabas = ""

# Variantes de las variables para la Base de datos pero para Descuento
precioClienteDesc = 0
idEspecieDesc = 0

# Variable que indica si esta listo para realizar acciones 
listoParaAccionar = False
btnActualizar = True
contadorActualizar = 30

# Variables de rutas de imagenes para alerta
correcto = "imagenes/correcto.png"
error = "imagenes/error.png"
descuento = "imagenes/seleccionado.png"
loading = "imagenes/loading.gif"

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
                    """ #self.conexion.actualizar_datos_servidor_procesos()
                    #self.conexion.actualizar_datos_servidor_pesadas() """
                except Exception as e:
                    print(f"Error al interactuar con la base de datos: {e}")
                else:
                    s.close()
            time.sleep(120)

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

""" Creamos hilo para la ejecución en segundo plano de la Fecha y Hora, de esta forma
evitamos que la aplicación se detenga por la lectura constante  """

class WorkerThreadFechaHora(QThread):
    # Tarea a ejecutarse cada determinado tiempo.
    update_fecha = pyqtSignal(str)
    update_hora = pyqtSignal(str)
    def run(self):
        try:
            while True:
                hora_actual = datetime.now().time()
                hora = int(hora_actual.strftime("%H"))
                minutos = hora_actual.strftime("%M")
                segundos = hora_actual.strftime("%S")
                periodo = "AM" if hora < 12 else "PM"
                hora = hora if hora <= 12 else hora - 12
                hora_formateada = "{:02d} : {:02d} : {:02d} {}".format(hora, int(minutos), int(segundos), periodo)
                self.update_hora.emit(hora_formateada)

                fecha_actual = datetime.now().date()
                año = fecha_actual.year
                mes = fecha_actual.month
                dia = fecha_actual.day
                dia_semana = fecha_actual.weekday()
                dia_semana = ["Lunes", 
                            "Martes", 
                            "Miércoles", 
                            "Jueves", 
                            "Viernes", 
                            "Sábado", 
                            "Domingo"][int(dia_semana)]
                meses = {
                    1: "Enero",
                    2: "Febrero",
                    3: "Marzo",
                    4: "Abril",
                    5: "Mayo",
                    6: "Junio",
                    7: "Julio",
                    8: "Agosto",
                    9: "Septiembre",
                    10: "Octubre",
                    11: "Noviembre",
                    12: "Diciembre"
                }
                fecha_formateada = "{} {} de {} del {}".format(dia_semana, dia, meses[mes], año)

                self.update_fecha.emit(fecha_formateada)
                time.sleep(1)
        except Exception as e:
            print("WT FH"+str(e))  
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()

# ===============================
# Creación de la Clase Principal
# ===============================

class Inicio(QMainWindow):
    
    def __init__(self):
        super(Inicio, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conexion = DataBase.database_conexion.Conectar()
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.workerFechaHora = WorkerThreadFechaHora() # Hilo de Fecha y Hora
        self.workerFechaHora.start() # Iniciamos el hilo
        self.workerFechaHora.update_fecha.connect(self.mostrar_fecha) # Llamamos a la función mostrar_fecha
        self.workerFechaHora.update_hora.connect(self.mostrar_hora) # Llamamos a la función mostrar_hora
        
        self.fn_declararPuertoArduino()
        self.workerAR = WorkerThreadAR() # Hilo de Arduino
        self.workerAR.start() # Iniciamos el hilo
        
        self.fn_declararApiURL()
        self.fn_traerDatosServidor() 
        self.workerBase = WorkerThreadSubirDatosBase() # Actualización Base de Datos de Local a Servidor
        self.workerBase.start()
        threadBtn = threading.Thread(target=self.fn_temporizadorBtn)
        threadBtn.start()

        self.ui.imgLogo.setPixmap(QPixmap("Imagenes/iconoPC.png"))
        self.ui.imgImpresora.setPixmap(QPixmap("Imagenes/impresora.png"))
        
        #self.fn_declaraEspecie()
        self.fn_declaraPassword()
        
        tablaDePesos = self.ui.tblDetallePesadas
        tablaDePesos.setColumnWidth(0, 80)
        tablaDePesos.setColumnWidth(1, 320)
        tablaDePesos.setColumnWidth(2, 120)
        tablaDePesos.setColumnWidth(3, 180)
        tablaDePesos.setColumnWidth(4, 150)
        tablaDePesos.setColumnWidth(5, 100)
        tablaDePesos.setColumnWidth(6, 100)
        tablaDePesos.setColumnWidth(7, 180)
        tablaDePesos.setColumnWidth(8, 150)
        tablaDePesos.setColumnWidth(9, 120)
        tablaDePesos.setAlternatingRowColors(True)

        self.ui.txtCodigoCliente.setEnabled(True)
        self.ui.txtCodigoCliente.setFocus(True)
        self.ui.txtCodigoCliente.textChanged.connect(self.fn_recepcionaCodigoTrabajador)
        self.ui.lblPesoIndicador.setText("10.00")
        
        self.ui.frmIngresarCantidad.setHidden(True)
        self.ui.frmAlerta.setHidden(True)
        self.ui.frmAplicarDescuento.setHidden(True)
        self.ui.frmIngresarPassword.setHidden(True)
        self.ui.frmAlertaEliminar.setHidden(True)
        self.ui.txtCantJabasTotales.setHidden(True)
        self.ui.txtCantidadDeJabas.setHidden(True)
        self.ui.frmColores.setHidden(True)
        self.ui.frmIngresarCantidadJabas.setHidden(True)
        
        self.ui.txtCantidadParaIngresar.textChanged.connect(self.fn_validarEntradaNumerica)
        self.ui.txtCantidadDescuento.textChanged.connect(self.fn_validarEntradaNumerica)
        self.ui.btnCerrarFrmAlerta.clicked.connect(self.fn_btnCerrarFrmAlerta)
        
    # ======================== Funciones llamadas por los Hilos ========================
    
    def evt_actualizar_peso(self, val):
        global pesoBalanza1
        global user_input_arduino
        
        if (balanzaSeleccionada == 1) :
            try:
                signo = val[0:1]
                val = float(val[1:9])
                
                if (signo == "-") and val != 0:
                    self.ui.lblPesoIndicador.setText("-"+str(format(val, ".2f")))
                else:
                    self.ui.lblPesoIndicador.setText(format(val, ".2f"))
            except ValueError:
                self.ui.lblPesoIndicador.setText("0.00")

    def evt_actualizar_baliza(self, val):    
        global pesoBalanza1
        global user_input_arduino

        try:

            val = float(val[1:9])

            if (pesoBalanza1 == False and float(val)> 0.5):
                user_input_arduino = "c"
            else:
                user_input_arduino = "g"
            
            if (pesoBalanza1 == True and float(val) < 0.5):
                pesoBalanza1 = False
                user_input_arduino = "e"
           
        except ValueError:
           pass

    def evt_actualizar_estado(self, val):
        if (balanzaSeleccionada == 1) :
            if (val == "0"):
                self.ui.lblEstadoBalanzas.setText("FUERA DE LINEA")
                self.ui.lblPesoIndicador.setText("0.00")
                self.ui.lblEstadoBalanzas.setStyleSheet("background-color: rgb(234, 29, 49);color: rgb(255, 255, 255);")
            elif (val == "1"):
                self.ui.lblEstadoBalanzas.setText("EN LINEA")
                self.ui.lblEstadoBalanzas.setStyleSheet("background-color: rgb(32, 176, 20);color: rgb(255, 255, 255);")
            
    def evt_actualizar_peso2(self, val):
        global pesoBalanza2
        global user_input_arduino
        
        if (balanzaSeleccionada == 2) :
            try:
                signo = val[0:1]
                val = float(val[1:9])
                
                if (signo == "-") and val != 0:
                    self.ui.lblPesoIndicador.setText("-"+str(format(val, ".2f")))
                else:
                    self.ui.lblPesoIndicador.setText(format(val, ".2f"))
            except ValueError:
                self.ui.lblPesoIndicador.setText("0.00")

    def evt_actualizar_estado2(self, val):
        if (balanzaSeleccionada == 2) :
            if (val == "0"):
                self.ui.lblEstadoBalanzas.setText("FUERA DE LINEA")
                self.ui.lblPesoIndicador.setText("0.00")
                self.ui.lblEstadoBalanzas.setStyleSheet("background-color: rgb(234, 29, 49);color: rgb(255, 255, 255);")
            elif (val == "1"):
                self.ui.lblEstadoBalanzas.setText("EN LINEA")
                self.ui.lblEstadoBalanzas.setStyleSheet("background-color: rgb(32, 176, 20);color: rgb(255, 255, 255);")

    def evt_actualizar_baliza2(self, val):    
        global pesoBalanza2
        global user_input_arduino

        try:

            val = float(val[1:9])

            if (pesoBalanza2 == False and float(val)> 0.5):
                user_input_arduino = "d"
            else:
                user_input_arduino = "h"
            
            if (pesoBalanza2 == True and float(val) < 0.5):
                pesoBalanza2 = False
                user_input_arduino = "f"
           
        except ValueError:
           pass
        
    def mostrar_hora(self,val):
        self.ui.lblHora.setText(val)
        
    def mostrar_fecha(self,val):
        self.ui.lblFecha.setText(val)
        
    # ======================== Termina funciones llamadas por los Hilos ========================
    
    # ======================== Eventos con el Teclado ========================
    
    def condiciones_base(self):
        return (
            not frmRegistrarCantidad and
            not frmAlertaEliminarPeso and
            not frmEliminarPeso and
            not frmAlerta and
            not frmRegistrarDescuento and
            not frmEditarCantidad and
            not frmRegistrarJabas and 
            not frmRegistrarDescuentoCan
        )
        
    def condiciones_alertas(self):
        return (
            not self.ui.frmIngresarCantidad.isVisible() and
            not self.ui.frmAlerta.isVisible() and
            not self.ui.frmAplicarDescuento.isVisible() and
            not self.ui.frmIngresarPassword.isVisible() and
            not self.ui.frmAlertaEliminar.isVisible()
        )
        
    def keyPressEvent(self,event):
        global balanzaSeleccionada
        global frmRegistrarCantidad
        global frmAlertaEliminarPeso
        global frmEliminarPeso
        global frmAlerta
        global frmRegistrarDescuento
        global frmInicioProceso
        global frmEditarCantidad
        global frmRegistrarJabas
        global frmRegistrarDescuentoCan
        global frmEditarCantidadTara
        global frmEditarCantidadDescuento
        global btnActualizar
        
        if event.key() == Qt.Key_Escape:
            self.close()
    
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.condiciones_base() and frmInicioProceso == True and self.condiciones_alertas() and float(self.ui.lblPesoIndicador.text()) > 0:
            
            self.ui.txtCantidadParaIngresar.setText("")
            self.fn_alertaCantidad("Ingresar cantidad de Pollos")
            frmRegistrarCantidad = True
            self.ui.txtCantidadParaIngresar.setFocus(True)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.lwListaClientes.isVisible():
            if (len(listCodCliente)):
                indice = self.ui.lwListaClientes.currentIndex().row()
                estadoDelCliente = listEstadoCliente[indice]
                if (estadoDelCliente == 1):
                    self.fn_seleccionarCliente()
                    if balanzaSeleccionada == 1:
                        self.fn_traerPreciosCliente(codCliente1)
                        self.fn_seleccionarEspecie(idEspecie)
                        self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                    elif balanzaSeleccionada == 2:
                        self.fn_traerPreciosCliente(codCliente2)
                        self.fn_seleccionarEspecie(idEspecie)
                        self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                        
                    self.fn_verificarProceso()
                    self.fn_listarVenta()
                else:
                    self.fn_cambiarCliente()
                    self.ui.btnCerrarFrmAlerta.setHidden(False)
                    self.ui.lblAlertaTitulo.setStyleSheet("color: #EA1D31")
                    self.ui.lblAlertaTexto.setStyleSheet("font-size:16pt;")
                    self.ui.frmAlerta.setHidden(False)
                    self.ui.lblAlertaTitulo.setText("¡ADVERTENCIA!")
                    self.ui.imgIconAlerta.setPixmap(QPixmap(error))
                    self.ui.lblAlertaTexto.setText("El cliente se encuentra INHABILITADO. Seleccione otro cliente por favor.")
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmRegistrarCantidad == True and frmInicioProceso == True and self.ui.frmIngresarCantidad.isVisible() and self.ui.txtCantidadParaIngresar.text() != "":
            if float(self.ui.lblPesoIndicador.text()) > 0.05 :
                self.fn_registrarPesada()
                self.ui.frmIngresarCantidad.setHidden(True)
                self.fn_alerta("¡REGISTRO EXITOSO!",correcto,"El registro se realizo correctamente.")
                frmRegistrarCantidad = False
            else:
                self.fn_alerta("¡ADVERTENCIA!",error,"El peso es demasiado bajo.")
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmEditarCantidad == True and frmInicioProceso == True and self.ui.frmIngresarCantidad.isVisible() and self.ui.txtCantidadParaIngresar.text() != "":
            self.fn_editarCantidad()
            self.ui.frmIngresarCantidad.setHidden(True)
            self.fn_alerta("¡EDITADO EXITOSO!",correcto,"El registro se edito correctamente.")
            frmEditarCantidad = False
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmEditarCantidadTara == True and frmInicioProceso == True and self.ui.frmIngresarCantidad.isVisible() and self.ui.txtCantidadParaIngresar.text() != "":
            self.fn_editarCantidadTara()
            self.ui.frmIngresarCantidad.setHidden(True)
            self.fn_alerta("¡EDITADO EXITOSO!",correcto,"El registro se edito correctamente.")
            frmEditarCantidadTara = False
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmEditarCantidadDescuento == True and frmInicioProceso == True and self.ui.frmIngresarCantidad.isVisible() and self.ui.txtCantidadParaIngresar.text() != "":
            self.fn_editarCantidadDescuento()
            self.ui.frmIngresarCantidad.setHidden(True)
            self.fn_alerta("¡EDITADO EXITOSO!",correcto,"El registro se edito correctamente.")
            frmEditarCantidadDescuento = False
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmRegistrarJabas == True and frmInicioProceso == True and self.ui.frmIngresarCantidad.isVisible() and self.ui.txtCantidadParaIngresar.text() != "":
            self.fn_registrarTara()
            self.ui.frmIngresarCantidad.setHidden(True)
            self.fn_alerta("¡REGISTRO EXITOSO!",correcto,"El registro se realizo correctamente.")
            frmRegistrarJabas = False 
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmRegistrarDescuento == True and frmInicioProceso == True and self.ui.frmAplicarDescuento.isVisible() and idEspecieDesc != 0:
            self.ui.txtCantidadDescuento.setEnabled(True)
            self.ui.imgIconDesc.setPixmap(QPixmap(descuento))
            frmRegistrarDescuento = False
            frmRegistrarDescuentoCan = True
            self.ui.txtCantidadDescuento.setFocus(True)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmRegistrarDescuento == False and frmRegistrarDescuentoCan == True and frmInicioProceso == True and self.ui.frmAplicarDescuento.isVisible() and self.ui.txtCantidadDescuento.text() != "":
            if idEspecieDesc == primerEspecie and int(self.ui.txtCantPolloYugo.text().split()[0].strip()) <= int(self.ui.txtCantidadDescuento.text()):
                self.fn_alerta("¡ADVERTENCIA!",error,"La cantidad de descuento no puede ser mayor a la registrada.",2000)
            elif idEspecieDesc == segundaEspecie and int(self.ui.txtCantPolloPerla.text().split()[0].strip()) <= int(self.ui.txtCantidadDescuento.text()):
                self.fn_alerta("¡ADVERTENCIA!",error,"La cantidad de descuento no puede ser mayor a la registrada.",2000)
            elif idEspecieDesc == terceraEspecie and int(self.ui.txtCantPolloChimu.text().split()[0].strip()) <= int(self.ui.txtCantidadDescuento.text()):
                self.fn_alerta("¡ADVERTENCIA!",error,"La cantidad de descuento no puede ser mayor a la registrada.",2000)
            elif idEspecieDesc == cuartaEspecie and int(self.ui.txtCantPolloXX.text().split()[0].strip()) <= int(self.ui.txtCantidadDescuento.text()):
                self.fn_alerta("¡ADVERTENCIA!",error,"La cantidad de descuento no puede ser mayor a la registrada.",2000)
            else:
                self.fn_registrarDescuento()
                self.ui.frmAplicarDescuento.setHidden(True)
                self.fn_alerta("¡REGISTRO EXITOSO!",correcto,"El descuento se realizo correctamente.")
                frmRegistrarDescuentoCan = False
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmAlertaEliminarPeso == True and frmInicioProceso == True and self.ui.frmAlertaEliminar.isVisible():
            self.ui.txtPasswordEliminar.setFocus(True)
            self.ui.frmAlertaEliminar.setHidden(True)
            self.ui.frmIngresarPassword.setHidden(False)
            frmAlertaEliminarPeso = False
            frmEliminarPeso = True
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and frmAlertaEliminarPeso == False and frmEliminarPeso == True and frmInicioProceso == True and self.ui.frmIngresarPassword.isVisible() and self.ui.txtPasswordEliminar.text() != "":
            passwordExtraido = self.ui.txtPasswordEliminar.text()
            if str(passwordEliminar) == str(passwordExtraido):
                self.fn_eliminarUltimaCantidad()
                self.fn_alerta("¡ELIMINADO EXITOSO!",correcto,"El registro se elimino correctamente.",2000)
                self.ui.frmIngresarPassword.setHidden(True)
                frmEliminarPeso = False
            else:
                self.fn_alerta("¡CONTRASEÑA INCORRECTA!",error,"La contraseña no coincide con la contraseña declara para eliminar.")
            
    def keyReleaseEvent(self, event):
        global balanzaSeleccionada
        global frmRegistrarCantidad
        global frmAlertaEliminarPeso
        global frmEliminarPeso
        global frmAlerta
        global frmRegistrarDescuento
        global frmInicioProceso
        global frmEditarCantidad
        global frmRegistrarJabas
        global frmRegistrarDescuentoCan
        global idEspecieDesc
        global frmEditarCantidadTara
        global frmEditarCantidadDescuento
        global btnActualizar
        global contadorActualizar
        
        if (event.key() == Qt.Key_Right) and self.condiciones_base():
            balanzaSeleccionada = 1
            self.fn_seleccionaBalanza()
            self.fn_seleccionarEspecie(idEspecie)
            self.fn_seleccionarEspecieDescuento(idEspecieDesc)
            self.fn_verificarProceso()
            self.fn_listarVenta()
        
        if (event.key() == Qt.Key_Left) and self.condiciones_base():
            balanzaSeleccionada = 2
            self.fn_seleccionaBalanza()
            self.fn_seleccionarEspecie(idEspecie)
            self.fn_seleccionarEspecieDescuento(idEspecieDesc)
            self.fn_verificarProceso()
            self.fn_listarVenta()
            
        if event.key() == Qt.Key_Up and self.ui.lwListaClientes.isVisible():
            self.fn_ArribaLista()
        elif event.key() == Qt.Key_Down and self.ui.lwListaClientes.isVisible():
            self.fn_AbajoLista()
            
        if (event.key() == Qt.Key_6) and self.condiciones_base() and not self.ui.lwListaClientes.isVisible():
            self.fn_cambiarCliente()
            
        if (event.key() == Qt.Key_1) and not self.ui.lwListaClientes.isVisible() and self.condiciones_base() and self.condiciones_alertas():
            self.fn_seleccionarEspecie(primerEspecie)
        elif (event.key() == Qt.Key_2) and not self.ui.lwListaClientes.isVisible() and self.condiciones_base() and self.condiciones_alertas():
            self.fn_seleccionarEspecie(segundaEspecie)
        elif (event.key() == Qt.Key_3) and not self.ui.lwListaClientes.isVisible() and self.condiciones_base() and self.condiciones_alertas():
            self.fn_seleccionarEspecie(terceraEspecie)
        elif (event.key() == Qt.Key_4) and not self.ui.lwListaClientes.isVisible() and self.condiciones_base() and self.condiciones_alertas():
            self.fn_seleccionarEspecie(cuartaEspecie)
            
        if (event.key() == Qt.Key_1) and not self.ui.lwListaClientes.isVisible() and self.ui.frmAplicarDescuento.isVisible() and frmRegistrarDescuento == True and frmRegistrarDescuentoCan == False:
            if int(self.ui.txtCantPolloYugo.text().split()[0].strip()) > 0 :
                self.fn_seleccionarEspecieDescuento(primerEspecie)
            else:
                idEspecieDesc = 0
                self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                self.fn_alerta("¡ADVERTENCIA!",error,"No puede seleccionar la especie {} porque la cantidad es 0.".format(nombrePrimerEspecie),1500)
        elif (event.key() == Qt.Key_2) and not self.ui.lwListaClientes.isVisible() and self.ui.frmAplicarDescuento.isVisible() and frmRegistrarDescuento == True and frmRegistrarDescuentoCan == False:
            if int(self.ui.txtCantPolloPerla.text().split()[0].strip()) > 0 :
                self.fn_seleccionarEspecieDescuento(segundaEspecie)
            else:
                idEspecieDesc = 0
                self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                self.fn_alerta("¡ADVERTENCIA!",error,"No puede seleccionar la especie {} porque la cantidad es 0.".format(nombreSegundaEspecie),1500)
        elif (event.key() == Qt.Key_3) and not self.ui.lwListaClientes.isVisible() and self.ui.frmAplicarDescuento.isVisible() and frmRegistrarDescuento == True and frmRegistrarDescuentoCan == False:
            if int(self.ui.txtCantPolloChimu.text().split()[0].strip()) > 0 :
                self.fn_seleccionarEspecieDescuento(terceraEspecie)
            else:
                idEspecieDesc = 0
                self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                self.fn_alerta("¡ADVERTENCIA!",error,"No puede seleccionar la especie {} porque la cantidad es 0.".format(nombreTerceraEspecie),1500)
        elif (event.key() == Qt.Key_4) and not self.ui.lwListaClientes.isVisible() and self.ui.frmAplicarDescuento.isVisible() and frmRegistrarDescuento == True and frmRegistrarDescuentoCan == False:
            if int(self.ui.txtCantPolloXX.text().split()[0].strip()) > 0 :
                self.fn_seleccionarEspecieDescuento(cuartaEspecie)
            else:
                idEspecieDesc = 0
                self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                self.fn_alerta("¡ADVERTENCIA!",error,"No puede seleccionar la especie {} porque la cantidad es 0.".format(nombreCuartaEspecie),1500)
            
        if (event.key() == Qt.Key_8) and self.condiciones_base() and self.condiciones_alertas() and not self.ui.lwListaClientes.isVisible():
            if listoParaAccionar == True :
                self.ui.imgIconDesc.setPixmap(QPixmap(""))
                self.ui.txtCantidadDescuento.setText("")
                self.fn_seleccionarEspecieDescuento(idEspecieDesc)
                self.ui.txtCantidadDescuento.setEnabled(False)
                self.ui.frmAplicarDescuento.setHidden(False)
                frmRegistrarDescuento = True
            else:
                self.fn_alerta("¡ADVERTENCIA!",error,"En este momento no puedes realizar un descuento por que no hay registros.",2500)
            
        if (event.key() == Qt.Key_9) and self.condiciones_base() and self.condiciones_alertas() and not self.ui.lwListaClientes.isVisible():
            if listoParaAccionar == True :
                self.ui.txtPasswordEliminar.setText("")
                self.ui.frmAlertaEliminar.setHidden(False)
                frmAlertaEliminarPeso = True
            else:
                self.fn_alerta("¡ADVERTENCIA!",error,"En este momento no puedes eliminar por que no hay registros.",2500)
            
        if (event.key() == Qt.Key_Asterisk) and self.condiciones_base() and frmInicioProceso == True and self.condiciones_alertas() and not self.ui.lwListaClientes.isVisible():
            if listoParaAccionar == True :
                columna = 5
                item = self.ui.tblDetallePesadas.item(0, columna)  # Obtener el item de la primera fila y columna 5
                valor = item.text()
                if valor.endswith('T'):
                    self.ui.txtCantidadParaIngresar.setText("")
                    self.fn_alertaCantidad("Ingresar cantidad nueva de Tara")
                    frmEditarCantidadTara = True
                    self.ui.txtCantidadParaIngresar.setFocus(True)
                elif valor.startswith("-"):
                    self.ui.txtCantidadParaIngresar.setText("")
                    self.fn_alertaCantidad("Ingresar cantidad nueva de Descuento")
                    frmEditarCantidadDescuento = True
                    self.ui.txtCantidadParaIngresar.setFocus(True)
                else:
                    self.ui.txtCantidadParaIngresar.setText("")
                    self.fn_alertaCantidad("Ingresar cantidad nueva de Pollos")
                    frmEditarCantidad = True
                    self.ui.txtCantidadParaIngresar.setFocus(True)
            else:
                self.fn_alerta("¡ADVERTENCIA!",error,"En este momento no puedes editar por que no hay registros.",3000)
            
        if (event.key() == Qt.Key_7) and self.condiciones_base() and frmInicioProceso == True and self.condiciones_alertas() and not self.ui.lwListaClientes.isVisible():
            self.ui.txtCantidadParaIngresar.setText("")
            self.fn_alertaCantidad("Ingresar cantidad de Jabas")
            frmRegistrarJabas = True
            self.ui.txtCantidadParaIngresar.setFocus(True)
            
        if (event.key() == Qt.Key_0) and self.condiciones_base() and self.condiciones_alertas() and not self.ui.lwListaClientes.isVisible():
            self.fn_imprimirReporte()
            
        if event.key() == Qt.Key_Minus and frmInicioProceso == True:
            if (self.ui.frmIngresarCantidad.isVisible()):
                self.ui.frmIngresarCantidad.setHidden(True)
                frmRegistrarCantidad = False
                frmEditarCantidad = False
                frmRegistrarJabas = False
                frmEditarCantidadTara = False
                frmEditarCantidadDescuento = False
            elif (self.ui.frmAplicarDescuento.isVisible()):
                self.ui.frmAplicarDescuento.setHidden(True)
                frmRegistrarDescuento = False
                frmRegistrarDescuentoCan = False
            elif (self.ui.frmAlertaEliminar.isVisible()):
                self.ui.frmAlertaEliminar.setHidden(True)
                frmAlertaEliminarPeso = False
            elif (self.ui.frmIngresarPassword.isVisible()):
                self.ui.frmIngresarPassword.setHidden(True)
                frmEliminarPeso = False
                
        if event.key() == Qt.Key_F5 and not self.ui.frmAlerta.isVisible():
            if not btnActualizar and contadorActualizar == 0:
                btnActualizar = True
                contadorActualizar = 30
                threadBtn = threading.Thread(target=self.fn_temporizadorBtn)
                threadBtn.start()
                self.fn_abrirAnimacion()
            else:
                self.fn_alerta("ADVERTENCIA", error, "Debe esperar {} segundos antes de volver a actualizar.".format(contadorActualizar), 1000)
            
    # ======================== Termina eventos con el Teclado ========================
    
    def fn_temporizadorBtn(self):
        global btnActualizar
        global contadorActualizar

        # Contar desde 30 hasta 0 segundos
        for i in range(30, -1, -1):
            contadorActualizar = i
            time.sleep(1)

        btnActualizar = False
    
    def fn_abrirAnimacion(self):
        self.ui.lblAlertaTitulo.setStyleSheet("color: #3A93B3")
        self.ui.frmAlerta.setHidden(False)
        self.ui.lblAlertaTitulo.setText("Actualizando Datos")
        
        movie = QMovie(loading)  # Crea una instancia de QMovie
        self.ui.imgIconAlerta.setMovie(movie)  # Asocia la QMovie con el QLabel
        movie.start()  # Inicia la animación
        self.ui.lblAlertaTexto.setStyleSheet("font-size:14pt;")
        self.ui.lblAlertaTexto.setText("Espere por favor los datos se están actualizando. Recuerda que debes esperar 30 segundos para volver a actualizar.")
        
        # Llama a fn_traerDatosServidor en un hilo para evitar bloquear la interfaz de usuario
        thread = threading.Thread(target=self.fn_traerDatosServidor)
        thread.start()
    
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
                """ #self.conexion.actualizar_datos_servidor_a_local_clientes()
                #self.conexion.actualizar_datos_servidor_a_local_precios()
                #self.conexion.actualizar_datos_servidor_a_local_password() """
                print("Exito al interactuar con la base de datos")
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
            else:
                s2.close()
    
    def fn_declaraEspecie(self):
        global primerEspecie
        global segundaEspecie
        global terceraEspecie
        global cuartaEspecie
        global nombrePrimerEspecie
        global nombreSegundaEspecie
        global nombreTerceraEspecie
        global nombreCuartaEspecie
        
        nombresEspecies = self.conexion.db_buscaEspecies()
        primerEspecie = nombresEspecies[0][0]
        nombrePrimerEspecie = nombresEspecies[0][1]
        
        segundaEspecie = nombresEspecies[1][0]
        nombreSegundaEspecie = nombresEspecies[1][1]
        
        terceraEspecie = nombresEspecies[2][0]
        nombreTerceraEspecie = nombresEspecies[2][1]
        
        cuartaEspecie = nombresEspecies[3][0]
        nombreCuartaEspecie = nombresEspecies[3][1]
        
        self.ui.btnYugoVivo.setText("{} (1)".format(nombrePrimerEspecie))
        self.ui.btnYugoPelado.setText("{} (2)".format(nombreSegundaEspecie))
        self.ui.btnTecnicoVivo.setText("{} (3)".format(nombreTerceraEspecie))
        self.ui.btnTecnicoPelado.setText("{} (4)".format(nombreCuartaEspecie))
        
        self.ui.btnDescYugoVivo.setText("{} (1)".format(nombrePrimerEspecie))
        self.ui.btnDescYugoPelado.setText("{} (2)".format(nombreSegundaEspecie))
        self.ui.btnDescTecnicoVivo.setText("{} (3)".format(nombreTerceraEspecie))
        self.ui.btnDescTecnicoPelado.setText("{} (4)".format(nombreCuartaEspecie))
        
    def fn_declararPuertoArduino(self):
        global COMAR
        global HOST
        
        puertoArduino = self.conexion.db_seleccionaPuertoArduino()
        COMAR = str(puertoArduino[0])
        
    def fn_declararApiURL(self):
        
        apiURL = self.conexion.db_seleccionaApiURL()
        DataBase.database_conexion.URLSERVIDOR = str(apiURL[0][0])
        DataBase.database_conexion.URLLOCAL = str(apiURL[0][1])        
        
    def fn_declaraPassword(self):
        global passwordEliminar
        
        passwordBase = self.conexion.db_declaraPassword()
        passwordEliminar = str(passwordBase[0])
        
        
    def fn_alerta(self,titulo,imagen,mensaje,tiempo = 500):
        self.ui.btnCerrarFrmAlerta.setHidden(True)
        if imagen == correcto:
            self.ui.lblAlertaTitulo.setStyleSheet("color: #24D315")
            self.ui.lblAlertaTexto.setStyleSheet("font-size:16pt;")
        elif imagen == error:
            self.ui.lblAlertaTitulo.setStyleSheet("color: #EA1D31")
            self.ui.lblAlertaTexto.setStyleSheet("font-size:16pt;")
        self.ui.frmAlerta.setHidden(False)
        self.ui.lblAlertaTitulo.setText(titulo)
        self.ui.imgIconAlerta.setPixmap(QPixmap(imagen))
        self.ui.lblAlertaTexto.setText(mensaje)

        timer = QtCore.QTimer()
        timer.singleShot(tiempo, lambda: self.ui.frmAlerta.setHidden(True))
        
    def fn_alertaCantidad(self,titulo):
        self.ui.frmIngresarCantidad.setHidden(False)
        self.ui.lblTextoIngresarCantidad.setText(titulo)
        
    def fn_validarEntradaNumerica(self):
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(filter(str.isdigit, texto))

            sender.setText(texto_valido)
    
    def fn_recepcionaCodigoTrabajador(self):
        global listCodCliente
        global listGrupoCliente
        global listEstadoCliente
        
        self.ui.lwListaClientes.clear()
        listCodCliente.clear()
        listGrupoCliente.clear()
        listEstadoCliente.clear()
        valor = self.ui.txtCodigoCliente.text()

        if (valor != "" and len(valor) >= 1):

            nombreClienteSeleccionar = self.conexion.db_buscaCliente(valor)

            if (len(nombreClienteSeleccionar) > 0):
                self.ui.lwListaClientes.setHidden(False)
                for item in nombreClienteSeleccionar:
                    self.ui.lwListaClientes.addItem(item[0])
                    listCodCliente.append(item[1])
                    listGrupoCliente.append(item[2])
                    listEstadoCliente.append(item[3])
                self.ui.lwListaClientes.setCurrentRow(0)
                           
    def fn_ArribaLista(self):
        global indexLista
        
        if (indexLista != 0):
            indexLista -= 1
            self.ui.lwListaClientes.setCurrentRow(indexLista)

    def fn_AbajoLista(self):
        global indexLista
        
        numClientes = self.ui.lwListaClientes.count()
        if (indexLista < numClientes-1):
            indexLista += 1
            self.ui.lwListaClientes.setCurrentRow(indexLista)
            
    def fn_seleccionarCliente(self):
        global codCliente
        global codCliente1
        global codCliente2
        global nombresCliBalanza1
        global nombresCliBalanza2
        global precioCliente
        global idEspecie
        global idEspecieDesc
        global especieCli1
        global especieCli2
        global nombresCliBalanza
        global especieDesCli1
        global especieDesCli2
        global idGrupoCli1
        global idGrupoCli2
        global idGrupoCli
        
        if (balanzaSeleccionada == 1):
            indice = self.ui.lwListaClientes.currentIndex().row()
            codCliente1 = listCodCliente[indice]
            idGrupoCli1 = listGrupoCliente[indice]

            item = QListWidgetItem(self.ui.lwListaClientes.currentItem())
            self.ui.txtNombreCliente.setText(str(item.text()))
            self.ui.lwListaClientes.setHidden(True)
            self.ui.txtCodigoCliente.setHidden(True)
            nombresCliBalanza1 = str(item.text())
            codCliente = codCliente1
            idGrupoCli = idGrupoCli1
            especieCli1 = primerEspecie
            especieDesCli1 = 0
            idEspecie = especieCli1
            idEspecieDesc = especieDesCli1
            nombresCliBalanza = nombresCliBalanza1
            
        elif (balanzaSeleccionada == 2):
            indice = self.ui.lwListaClientes.currentIndex().row()
            codCliente2 = listCodCliente[indice]
            idGrupoCli2 = listGrupoCliente[indice]

            item = QListWidgetItem(self.ui.lwListaClientes.currentItem())
            self.ui.txtNombreCliente.setText(str(item.text()))
            self.ui.lwListaClientes.setHidden(True)
            self.ui.txtCodigoCliente.setHidden(True)
            nombresCliBalanza2 = str(item.text())
            codCliente = codCliente2
            idGrupoCli = idGrupoCli2
            especieCli2 = primerEspecie
            especieDesCli2 = 0
            idEspecie = especieCli2
            idEspecieDesc = especieDesCli2
            nombresCliBalanza = nombresCliBalanza2
            
    def fn_btnCerrarFrmAlerta(self):
        self.ui.frmAlerta.setHidden(True)
        self.ui.txtCodigoCliente.setFocus(True)
            
    def fn_seleccionaBalanza(self):
        global codCliente
        global balanzaSeleccionada
        global nombresCliBalanza
        global idEspecie
        global precioCliente
        global frmInicioProceso
        global idEspecieDesc
        global precioClienteDesc
        global valorDeConversion
        global valorDeConversionDesc
        global idGrupoCli
        
        codCliente = 0
        idGrupoCli = 0
        nombresCliBalanza = ""
        precioCliente = 0
        valorDeConversion = 0
        valorDeConversionDesc = 0
        precioClienteDesc = 0
        idEspecie = 0
        idEspecieDesc = 0
        self.ui.lblNumReporte.setText(str(0))
        
        self.ui.lblEstadoBalanzas.setText("FUERA DE LINEA")
        self.ui.lblEstadoBalanzas.setStyleSheet("background-color: rgb(234, 29, 49);color: rgb(255, 255, 255);")
        
        if (balanzaSeleccionada == 1):
            self.ui.lblNumBalanza.setText("Balanza N° 1")
            if codCliente1 != 0:
                frmInicioProceso = True
                codCliente = codCliente1
                idGrupoCli = idGrupoCli1
                nombresCliBalanza = nombresCliBalanza1
                idEspecie = especieCli1
                idEspecieDesc = especieDesCli1
                self.fn_traerPreciosCliente(codCliente)
                self.ui.txtNombreCliente.setText(nombresCliBalanza1)
                self.ui.txtCodigoCliente.setHidden(True)
                self.ui.lwListaClientes.setHidden(True)
            else:
                self.ui.txtCodigoCliente.setHidden(False)
                self.ui.txtCodigoCliente.setText("")
                self.ui.txtCodigoCliente.setFocus(True)
                self.ui.lwListaClientes.setHidden(False)
                
        elif (balanzaSeleccionada == 2):
            self.ui.lblNumBalanza.setText("Balanza N° 2")
            if codCliente2 != 0:
                frmInicioProceso = True
                codCliente = codCliente2
                idGrupoCli = idGrupoCli2
                nombresCliBalanza = nombresCliBalanza2
                idEspecie = especieCli2
                idEspecieDesc = especieDesCli2
                self.fn_traerPreciosCliente(codCliente)
                self.ui.txtNombreCliente.setText(nombresCliBalanza2)
                self.ui.txtCodigoCliente.setHidden(True)
                self.ui.lwListaClientes.setHidden(True)
            else:
                self.ui.txtCodigoCliente.setHidden(False)
                self.ui.txtCodigoCliente.setText("")
                self.ui.txtCodigoCliente.setFocus(True)
                self.ui.lwListaClientes.setHidden(False)
            
    def fn_traerPreciosCliente(self, codCliente):
        global precioPrimerEspecie
        global precioSegundaEspecie
        global precioTerceraEspecie
        global precioCuartaEspecie
        global valorDeConversionPrimerEspecie
        global valorDeConversionSegundaEspecie
        global valorDeConversionTerceraEspecie
        global valorDeConversionCuartaEspecie
        global valorDeConversion
        global precioCliente
        global precioClienteDesc
        
        try:
            self.preciosCliente = self.conexion.db_traerPreciosCliente(codCliente)
            
            (precioPrimerEspecie, precioSegundaEspecie, precioTerceraEspecie, precioCuartaEspecie, valorDeConversionPrimerEspecie,valorDeConversionSegundaEspecie,valorDeConversionTerceraEspecie,valorDeConversionCuartaEspecie) = self.preciosCliente[0]
        except Exception as e:
            self.fn_alerta("¡ERROR!",error,"No se pudieron obtener los precios del cliente.", 2000)
            self.fn_cambiarCliente()
        
    def fn_cambiarCliente(self):
        global precioPrimerEspecie
        global precioSegundaEspecie
        global precioTerceraEspecie
        global precioCuartaEspecie
        global valorDeConversion
        global codCliente1
        global codCliente2
        global nombresCliBalanza1
        global nombresCliBalanza2
        global codCliente
        global frmInicioProceso
        global idGrupoCli
        global idGrupoCli1
        global idGrupoCli2
        
        precioPrimerEspecie = 0
        precioSegundaEspecie = 0
        precioTerceraEspecie = 0
        precioCuartaEspecie = 0
        valorDeConversion = 0
        codCliente = 0
        idGrupoCli = 0
        
        self.ui.txtCantYugoVivo.setText("{} Uds.".format(0))
        self.ui.txtCantYugoPelado.setText("{} Uds.".format(0))
        self.ui.txtCantTecnicoVivo.setText("{} Uds.".format(0))
        self.ui.txtCantTecnicoPelado.setText("{} Uds.".format(0))
        self.ui.txtCantPolloTotales.setText("{} Uds.".format(0))
        
        self.ui.lblKgYugoVivo.setText("{:.2f} Kg".format(0))
        self.ui.lblKgYugoPelado.setText("{:.2f} Kg".format(0))
        self.ui.lblKgTecnicoVivo.setText("{:.2f} Kg".format(0))
        self.ui.lblKgTecnicoPelado.setText("{:.2f} Kg".format(0))
        
        self.ui.txtCantJabasTotales.setHidden(True)
        self.ui.txtCantidadDeJabas.setHidden(True)
        
        tablaDePesos = self.ui.tblDetallePesadas
        tablaDePesos.clearContents()
        tablaDePesos.setRowCount(0)
        
        frmInicioProceso = False
        
        self.ui.lblNumReporte.setText(str(0))
        
        if balanzaSeleccionada == 1:
            codCliente1 = 0
            idGrupoCli1 = 0
            nombresCliBalanza1 = ""
        elif balanzaSeleccionada == 2:
            codCliente2 = 0
            idGrupoCli2 = 0
            nombresCliBalanza2 = ""
            
        self.ui.txtCodigoCliente.setHidden(False)
        self.ui.txtCodigoCliente.setText("")
        self.ui.txtCodigoCliente.setFocus(True)
        self.ui.lwListaClientes.setHidden(False)
        
    def fn_seleccionarEspecie(self,especie):
        global idEspecie
        global precioCliente
        global especieCli1
        global especieCli2
        global especieDesCli1
        global especieDesCli2
        global valorDeConversion
        
        self.ui.btnPolloYugo.setStyleSheet("background-color: #FFF; color: #000")
        self.ui.btnPolloPerla.setStyleSheet("background-color: #FFF; color: #000")
        self.ui.btnPolloChimu.setStyleSheet("background-color: #FFF; color: #000")
        self.ui.btnPolloXX.setStyleSheet("background-color: #FFF; color: #000")
        
        if especie == 1:
            self.ui.btnPolloYugo.setStyleSheet("background-color: #2ABF4E; color: #fff")
            precioCliente = precioPrimerEspecie
            valorDeConversion = valorDeConversionPrimerEspecie
            idEspecie = primerEspecie
        elif especie == 2:
            self.ui.btnPolloPerla.setStyleSheet("background-color: #2ABF4E; color: #fff")
            precioCliente = precioSegundaEspecie
            valorDeConversion = valorDeConversionSegundaEspecie
            idEspecie = segundaEspecie
        elif especie == 3:
            self.ui.btnPolloChimu.setStyleSheet("background-color: #2ABF4E; color: #fff")
            precioCliente = precioTerceraEspecie
            valorDeConversion = valorDeConversionTerceraEspecie
            idEspecie = terceraEspecie
        elif especie == 4:
            self.ui.btnPolloXX.setStyleSheet("background-color: #2ABF4E; color: #fff")
            precioCliente = precioCuartaEspecie
            valorDeConversion = valorDeConversionCuartaEspecie
            idEspecie = cuartaEspecie
            
        if balanzaSeleccionada == 1:
            especieCli1 = idEspecie
            especieDesCli1 = idEspecieDesc
        elif balanzaSeleccionada == 2:
            especieCli2 = idEspecie
            especieDesCli2 = idEspecieDesc
            
    def fn_seleccionarEspecieDescuento(self,especieDesc):
        global idEspecieDesc
        global precioClienteDesc
        global especieDesCli1
        global especieDesCli2
        global valorDeConversionDesc
        
        self.ui.btnDescPolloYugo.setStyleSheet("background-color: #FFF; color: #000; border: 2px solid black; border-radius: 15px;")
        self.ui.btnDescPolloPerla.setStyleSheet("background-color: #FFF; color: #000; border: 2px solid black; border-radius: 15px;")
        self.ui.btnDescPolloChimu.setStyleSheet("background-color: #FFF; color: #000; border: 2px solid black; border-radius: 15px;")
        self.ui.btnDescPolloXX.setStyleSheet("background-color: #FFF; color: #000; border: 2px solid black; border-radius: 15px;")
        
        if especieDesc == 1:
            self.ui.btnDescPolloYugo.setStyleSheet("background-color: #2ABF4E; color: #fff; border: 2px solid black; border-radius: 15px;")
            precioClienteDesc = precioPrimerEspecie
            valorDeConversionDesc = valorDeConversionPrimerEspecie
            idEspecieDesc = primerEspecie
        elif especieDesc == 2:
            self.ui.btnDescPolloPerla.setStyleSheet("background-color: #2ABF4E; color: #fff; border: 2px solid black; border-radius: 15px;")
            precioClienteDesc = precioSegundaEspecie
            valorDeConversionDesc = valorDeConversionSegundaEspecie
            idEspecieDesc = segundaEspecie
        elif especieDesc == 3:
            self.ui.btnDescPolloChimu.setStyleSheet("background-color: #2ABF4E; color: #fff; border: 2px solid black; border-radius: 15px;")
            precioClienteDesc = precioTerceraEspecie
            valorDeConversionDesc = valorDeConversionTerceraEspecie
            idEspecieDesc = terceraEspecie
        elif especieDesc == 4:
            self.ui.btnDescPolloXX.setStyleSheet("background-color: #2ABF4E; color: #fff; border: 2px solid black; border-radius: 15px;")
            precioClienteDesc = precioCuartaEspecie
            valorDeConversionDesc = valorDeConversionCuartaEspecie
            idEspecieDesc = cuartaEspecie
            
        if balanzaSeleccionada == 1:
            especieDesCli1 = idEspecieDesc
        elif balanzaSeleccionada == 2:
            especieDesCli2 = idEspecieDesc
        
    def fn_verificarProceso(self):
        global numProceso
        
        numProceso = 0
        
        procesoActual = self.conexion.db_verificarProceso(codCliente)
            
        if(len(procesoActual) > 0 and codCliente != 0):
            numProceso = procesoActual[0][0]
        else:          
            if codCliente != 0 :  
                self.conexion.db_registrarProceso(codCliente)
                numVentaBase = self.conexion.db_obtieneUltimoIdProcesoRegistrado()
                numProceso = numVentaBase[0]
            
        self.ui.lblNumReporte.setText(str(numProceso))
        
    def fn_registrarPesada(self):
        global pesoNeto
        global cantidadRegistro
        global user_input_arduino
        global pesoBalanza1
        global pesoBalanza2
        global horaPeso
        global fechaPeso
        
        horaPeso = datetime.now().strftime('%H:%M:%S')
        fechaPeso = datetime.now().strftime('%Y-%m-%d')
        
        pesoNeto = float(self.ui.lblPesoIndicador.text())
        cantidadRegistro = int(self.ui.txtCantidadParaIngresar.text())
        self.conexion.db_registrarPesadas(numProceso,idEspecie,pesoNeto,horaPeso,codCliente,fechaPeso,cantidadRegistro,precioCliente,balanzaSeleccionada,numJabas,valorDeConversion,estadoPeso,estadoWebPeso)
        
        if balanzaSeleccionada == 1:
            user_input_arduino = "agi"
            time.sleep(1)
            user_input_arduino = "k"
            pesoBalanza1 = True
            
        elif balanzaSeleccionada == 2:
            user_input_arduino = "bhj"
            time.sleep(1)
            user_input_arduino = "l"
            pesoBalanza2 = True  
                  
        self.fn_listarVenta()
        
    def fn_registrarDescuento(self):
        global pesoNeto
        global cantidadRegistro
        global user_input_arduino
        global pesoBalanza1
        global pesoBalanza2
        global horaPeso
        global fechaPeso
        
        horaPeso = datetime.now().strftime('%H:%M:%S')
        fechaPeso = datetime.now().strftime('%Y-%m-%d')
        
        pesoNeto = float(self.ui.lblPesoIndicador.text())*-1
        cantidadRegistro = int(self.ui.txtCantidadDescuento.text())*-1
        self.conexion.db_registrarPesadas(numProceso,idEspecieDesc,pesoNeto,horaPeso,codCliente,fechaPeso,cantidadRegistro,precioClienteDesc,balanzaSeleccionada,numJabas,valorDeConversionDesc,estadoPeso,estadoWebPeso)
        
        if balanzaSeleccionada == 1:
            user_input_arduino = "agi"
            time.sleep(1)
            user_input_arduino = "k"
            pesoBalanza1 = True
            
        elif balanzaSeleccionada == 2:
            user_input_arduino = "bhj"
            time.sleep(1)
            user_input_arduino = "l"
            pesoBalanza2 = True 
        
        self.fn_listarVenta()
        
    def fn_registrarTara(self):
        global pesoNeto
        global cantidadRegistro
        global numJabas
        global user_input_arduino
        global pesoBalanza1
        global pesoBalanza2
        global horaPeso
        global fechaPeso
        
        horaPeso = datetime.now().strftime('%H:%M:%S')
        fechaPeso = datetime.now().strftime('%Y-%m-%d')
        
        pesoNeto = float(self.ui.lblPesoIndicador.text())*-1
        cantidadRegistro = int(self.ui.txtCantidadParaIngresar.text())
        self.conexion.db_registrarPesadas(numProceso,idEspecie,pesoNeto,horaPeso,codCliente,fechaPeso,numJabas,precioCliente,balanzaSeleccionada,cantidadRegistro,valorDeConversion,estadoPeso,estadoWebPeso)
        
        if balanzaSeleccionada == 1:
            user_input_arduino = "agi"
            time.sleep(1)
            user_input_arduino = "k"
            pesoBalanza1 = True
            
        elif balanzaSeleccionada == 2:
            user_input_arduino = "bhj"
            time.sleep(1)
            user_input_arduino = "l"
            pesoBalanza2 = True 
        
        numJabas = 0
        
        self.fn_listarVenta()
        
    def fn_editarCantidad(self):
        cantidadNueva = int(self.ui.txtCantidadParaIngresar.text())
        self.conexion.db_editarCantidadNueva(cantidadNueva,codCliente)
        self.fn_listarVenta()
        
    def fn_editarCantidadTara(self):
        cantidadNueva = int(self.ui.txtCantidadParaIngresar.text())   
        self.conexion.db_editarCantidadTaraNueva(cantidadNueva,codCliente)
        self.fn_listarVenta()
        
    def fn_editarCantidadDescuento(self):
        cantidadNueva = int(self.ui.txtCantidadParaIngresar.text())*-1   
        self.conexion.db_editarCantidadDescuentoNueva(cantidadNueva,codCliente)
        self.fn_listarVenta()
        
    def fn_eliminarUltimaCantidad(self):
        self.conexion.db_eliminarUltimaCantidad(codCliente)
        self.fn_listarVenta()
        
    def fn_listarVenta(self):
        global frmInicioProceso
        global listoParaAccionar
        
        tablaDePesos = self.ui.tblDetallePesadas
        tablaDePesos.clearContents()
        tablaDePesos.setRowCount(0)
        
        totalPesoPrimerEspecie = 0
        totalPesoSegundaEspecie = 0
        totalPesoTerceraEspecie = 0
        totalPesoCuartaEspecie = 0
        
        totalCantidadTotalEspecies = 0
        
        totalCantidadPrimerEspecie = 0
        totalCantidadSegundaEspecie = 0
        totalCantidadTerceraEspecie = 0
        totalCantidadCuartaEspecie = 0
        
        totalCantidadDescPrimerEspecie = 0
        totalCantidadDescSegundaEspecie = 0
        totalCantidadDescTerceraEspecie = 0
        totalCantidadDescCuartaEspecie = 0
        totalDeJabas = 0
        
        frmInicioProceso = False
        listoParaAccionar = False
        
        self.ui.txtCantJabasTotales.setHidden(True)
        self.ui.txtCantidadDeJabas.setHidden(True)
        
        if codCliente != 0:
            pesosListarTabla = self.conexion.db_listarPesosTabla(numProceso,codCliente)
            
            frmInicioProceso = True
            
            if len(pesosListarTabla) > 0:
                
                listoParaAccionar = True
            
                for row_number, row_data in enumerate(pesosListarTabla):
                    
                        tablaDePesos.insertRow(row_number)
                        
                        for column_number, data in enumerate(row_data):
                            
                            if column_number == 0:  # Columna de "correlativo"
                                data = (row_number - len(pesosListarTabla))*-1
                            if column_number == 4:  # Columna de "pesoNetoPes"
                                data = "{:.2f} Kg".format(data)
                            if column_number == 8 :  # Columna de "horaPes"
                                hours, remainder = divmod(data.seconds, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                data = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
                            
                            if column_number == 2 and row_data[2] is None and row_data[8] > 0: # Columna de "Promedio"
                                data = (row_data[4] / row_data[8])*-1
                                
                            if column_number == 3 and row_data[9] == 1: # Columna de "idEspecie" y columna de "estadoPes"
                                if data == nombrePrimerEspecie:
                                    totalPesoPrimerEspecie += row_data[4] # Columna de "pesoNetoPes" 
                                    totalCantidadPrimerEspecie += row_data[5] # Columna de "cantidadPes"
                                elif data == nombreSegundaEspecie:
                                    totalPesoSegundaEspecie += row_data[4]
                                    totalCantidadSegundaEspecie += row_data[5]
                                elif data == nombreTerceraEspecie:
                                    totalPesoTerceraEspecie += row_data[4]
                                    totalCantidadTerceraEspecie += row_data[5]
                                elif data == nombreCuartaEspecie:
                                    totalPesoCuartaEspecie += row_data[4]
                                    totalCantidadCuartaEspecie += row_data[5]
                                
                                totalCantidadTotalEspecies += row_data[5]
                                
                            if row_data[5] < 0 :
                                if data == nombrePrimerEspecie:
                                    totalCantidadDescPrimerEspecie += row_data[5] # Columna de "cantidadPes"
                                elif data == nombreSegundaEspecie:
                                    totalCantidadDescSegundaEspecie += row_data[5]
                                elif data == nombreTerceraEspecie:
                                    totalCantidadDescTerceraEspecie += row_data[5]
                                elif data == nombreCuartaEspecie:
                                    totalCantidadDescCuartaEspecie += row_data[5]
                                
                            item = QTableWidgetItem(str(data))
                            item.setTextAlignment(Qt.AlignCenter)
                            tablaDePesos.setItem(row_number, column_number, item)
                            
                        if (row_data[7] == 0):
                            self.fn_pintarCeldasRegistrosEliminados(row_number)
        
        self.ui.txtCantidadDeJabas.setHidden(False)
        self.ui.txtCantJabasTotales.setHidden(False)
        self.ui.txtCantJabasTotales.setText("{} {}".format(totalDeJabas, "Ud." if totalDeJabas == 1 else "Uds."))
                            
        self.ui.lblKgPolloYugo.setText("{:.2f} Kg".format(totalPesoPrimerEspecie))
        self.ui.lblKgPolloPerla.setText("{:.2f} Kg".format(totalPesoSegundaEspecie))
        self.ui.lblKgPolloChimu.setText("{:.2f} Kg".format(totalPesoTerceraEspecie))
        self.ui.lblKgPolloXX.setText("{:.2f} Kg".format(totalPesoCuartaEspecie))
        
        self.ui.txtCantPolloTotales.setText("{} {}".format(totalCantidadTotalEspecies, "Ud." if totalCantidadTotalEspecies == 1 else "Uds."))
        
        self.ui.txtCantPolloYugo.setText("{} {}".format(totalCantidadPrimerEspecie, "Ud." if totalCantidadPrimerEspecie == 1 else "Uds."))
        self.ui.txtCantPolloPerla.setText("{} {}".format(totalCantidadSegundaEspecie, "Ud." if totalCantidadSegundaEspecie == 1 else "Uds."))
        self.ui.txtCantPolloChimu.setText("{} {}".format(totalCantidadTerceraEspecie, "Ud." if totalCantidadTerceraEspecie == 1 else "Uds."))
        self.ui.txtCantPolloXX.setText("{} {}".format(totalCantidadCuartaEspecie, "Ud." if totalCantidadCuartaEspecie == 1 else "Uds."))
        
        self.ui.txtCantDescPolloYugo.setText("{} {}".format(totalCantidadDescPrimerEspecie, "Ud." if totalCantidadDescPrimerEspecie == 1 else "Uds."))
        self.ui.txtCantDescPolloPerla.setText("{} {}".format(totalCantidadDescSegundaEspecie, "Ud." if totalCantidadDescSegundaEspecie == 1 else "Uds."))
        self.ui.txtCantDescPolloChimu.setText("{} {}".format(totalCantidadDescTerceraEspecie, "Ud." if totalCantidadDescTerceraEspecie == 1 else "Uds."))
        self.ui.txtCantDescPolloXX.setText("{} {}".format(totalCantidadDescCuartaEspecie, "Ud." if totalCantidadDescCuartaEspecie == 1 else "Uds."))
                            
    def fn_pintarCeldasRegistrosEliminados(self, row):
        tablaDePesos = self.ui.tblDetallePesadas
        for e in range(tablaDePesos.columnCount()):
            item = tablaDePesos.item(row, e)
            item.setBackground(QColor(255, 51, 51))
            item.setForeground(QColor(255, 255, 255))
            
    def fn_imprimirReporte(self):

        datosTicket = self.conexion.db_traerDatosReporte(numProceso,codCliente)
        
        reporteTotalCantidadPrimerEspecie = 0
        reporteTotalCantidadSegundaEspecie = 0
        reporteTotalCantidadTerceraEspecie = 0
        reporteTotalCantidadCuartaEspecie = 0
        
        reporteTotalPesoPrimerEspecie = 0
        reporteTotalPesoSegundaEspecie = 0
        reporteTotalPesoTerceraEspecie = 0
        reporteTotalPesoCuartaEspecie = 0
        
        contarDescuentos = 0
        contarJabas = 0
        
        file = open("ArchivosDeTexto/reporte.txt", "w") 
        file.write("\n")
        file.write(" FECHA : "+fechaPeso+"     HORA : "+horaPeso+"\n")
        file.write(" CLIENTE :  "+str(self.ui.txtNombreCliente.text())+" \n")
        file.write("\n")
        file.write(" {:<13}{:<10}{:<7}{:<9}\n".format("PRODUCTO", "Kg", "CANT.", "HORA"))
        file.write("========================================\n")
        
        for item in datosTicket:
            reporteEspecie = item[0]
            reportePeso = item[1]
            reporteCantidad = item[2]
            reporteHora = "{:02}:{:02}:{:02}".format(item[3].seconds // 3600, (item[3].seconds // 60) % 60, item[3].seconds % 60)
            reporteJabas = item[4]
            
            if reportePeso < 0:
                contarDescuentos += 1
                
            if reporteJabas > 0:
                contarJabas += 1
            
            if (reporteEspecie == nombrePrimerEspecie) and reportePeso > 0 :
                reporteTotalCantidadPrimerEspecie += reporteCantidad
                reporteTotalPesoPrimerEspecie += reportePeso
                file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
            elif (reporteEspecie == nombreSegundaEspecie) and reportePeso > 0 :
                reporteTotalCantidadSegundaEspecie += reporteCantidad
                reporteTotalPesoSegundaEspecie += reportePeso
                file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
            elif (reporteEspecie == nombreTerceraEspecie) and reportePeso > 0 :
                reporteTotalCantidadTerceraEspecie += reporteCantidad
                reporteTotalPesoTerceraEspecie += reportePeso
                file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
            elif (reporteEspecie == nombreCuartaEspecie) and reportePeso > 0 :
                reporteTotalCantidadCuartaEspecie += reporteCantidad
                reporteTotalPesoCuartaEspecie += reportePeso
                file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
                
        if contarDescuentos > 0 :
            
            file.write("\n")
            file.write(" DESCUENTOS :\n")
            file.write("========================================\n")
            
            for item in datosTicket:
                reporteEspecie = item[0]
                reportePeso = item[1]
                reporteCantidad = item[2]
                reporteHora = "{:02}:{:02}:{:02}".format(item[3].seconds // 3600, (item[3].seconds // 60) % 60, item[3].seconds % 60)
                reporteJabas = item[4]
                
                if (reporteEspecie == nombrePrimerEspecie) and reportePeso < 0 and reporteJabas == 0:
                    reporteTotalCantidadPrimerEspecie += reporteCantidad
                    reporteTotalPesoPrimerEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
                elif (reporteEspecie == nombreSegundaEspecie) and reportePeso < 0 and reporteJabas == 0:
                    reporteTotalCantidadSegundaEspecie += reporteCantidad
                    reporteTotalPesoSegundaEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
                elif (reporteEspecie == nombreTerceraEspecie) and reportePeso < 0 and reporteJabas == 0:
                    reporteTotalCantidadTerceraEspecie += reporteCantidad
                    reporteTotalPesoTerceraEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
                elif (reporteEspecie == nombreCuartaEspecie) and reportePeso < 0 and reporteJabas == 0:
                    reporteTotalCantidadCuartaEspecie += reporteCantidad
                    reporteTotalPesoCuartaEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteCantidad, reporteHora))
                    
        if contarJabas > 0 :
            
            file.write("\n")
            file.write(" JABAS :\n")
            file.write("========================================\n")
            
            for item in datosTicket:
                reporteEspecie = item[0]
                reportePeso = item[1]
                reporteCantidad = item[2]
                reporteHora = "{:02}:{:02}:{:02}".format(item[3].seconds // 3600, (item[3].seconds // 60) % 60, item[3].seconds % 60)
                reporteJabas = item[4]
                
                if (reporteEspecie == nombrePrimerEspecie) and reportePeso < 0 and reporteJabas != 0:
                    reporteTotalCantidadPrimerEspecie += reporteCantidad
                    reporteTotalPesoPrimerEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteJabas, reporteHora))
                elif (reporteEspecie == nombreSegundaEspecie) and reportePeso < 0 and reporteJabas != 0:
                    reporteTotalCantidadSegundaEspecie += reporteCantidad
                    reporteTotalPesoSegundaEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteJabas, reporteHora))
                elif (reporteEspecie == nombreTerceraEspecie) and reportePeso < 0 and reporteJabas != 0:
                    reporteTotalCantidadTerceraEspecie += reporteCantidad
                    reporteTotalPesoTerceraEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteJabas, reporteHora))
                elif (reporteEspecie == nombreCuartaEspecie) and reportePeso < 0 and reporteJabas != 0:
                    reporteTotalCantidadCuartaEspecie += reporteCantidad
                    reporteTotalPesoCuartaEspecie += reportePeso
                    file.write(" {:<13}{:<10}{:<7}{:<9}\n".format(reporteEspecie, reportePeso, reporteJabas, reporteHora))
        
        file.write("\n")
        file.write(" TOTALES :           \n")
        file.write("========================================\n")
        file.write(" PRODUCTO        Kg.       CANTIDAD     \n")
        file.write("========================================\n")
        file.write(" {:<16}{:<10.1f}{:<9}\n".format(nombrePrimerEspecie, reporteTotalPesoPrimerEspecie, reporteTotalCantidadPrimerEspecie))
        file.write(" {:<16}{:<10.1f}{:<9}\n".format(nombreSegundaEspecie, reporteTotalPesoSegundaEspecie, reporteTotalCantidadSegundaEspecie))
        file.write(" {:<16}{:<10.1f}{:<9}\n".format(nombreTerceraEspecie, reporteTotalPesoTerceraEspecie, reporteTotalCantidadTerceraEspecie))
        file.write(" {:<16}{:<10.1f}{:<9}\n".format(nombreCuartaEspecie, reporteTotalPesoCuartaEspecie, reporteTotalCantidadCuartaEspecie))
        file.write("========================================\n")
        file.write("===       GRACIAS POR SU COMPRA      ===\n")
        file.write("========================================\n")
        file.write("\n")
        file.close()
        
        if  reporteTotalCantidadPrimerEspecie == 0 and reporteTotalCantidadSegundaEspecie == 0 and reporteTotalCantidadTerceraEspecie == 0 and reporteTotalCantidadCuartaEspecie == 0:
            self.fn_alerta("¡REPORTE NO ENVIDO!",error,"El reporte no se puede imprimir por valores nulos.", 2000)
        else:
            self.imprimirTicketWindows()
            self.fn_alerta("¡REPORTE ENVIADO!",correcto,"El reporte sera impreso en estos momentos.")
    
    def imprimirTicketWindows(self):
        # Obtener la impresora predeterminada
        impresora = win32print.GetDefaultPrinter()

        # Ruta al archivo que deseas imprimir
        ruta_archivo = r"ArchivosDeTexto/reporte.txt"
        # Abrir el archivo en modo lectura
        with open(ruta_archivo, "r") as f:
            # Leer el contenido del archivo
            contenido = f.read()

        # Imprimir el contenido del archivo en la impresora predeterminada
        hPrinter = win32print.OpenPrinter(impresora)
        try:
            win32print.StartDocPrinter(hPrinter, 1, ("documento", None, "RAW"))
            try:
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, bytes(contenido, "utf-8"))
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    
# DISEÑADO Y DESARROLLADO POR SANTOS VILCHEZ EDINSON PASCUAL
# LA UNIÓN - PIURA - PERU ; 2023