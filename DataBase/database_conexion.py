import mysql.connector
import requests
import json

URLSERVIDOR=""
URLLOCAL = ""

class Conectar():
    def __init__(self):
        # Conexion para MySql
        self.conexionsql = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='',
                                        database='bd_proyectosullana',
                                        port='3306')
        
    def db_seleccionaApiURL(self):
        cursor = self.conexionsql.cursor()
        sql = "SELECT puerto_ApiURLSERVIDOR,puerto_ApiURLLOCAL FROM tb_puertos"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
        
    def db_buscaEspecies(self):
        cursor = self.conexionsql.cursor()
        sql = "SELECT idEspecie,nombreEspecie FROM tb_especies_venta"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_seleccionaPuertoIndicadores(self):
        cursor = self.conexionsql.cursor()
        sql = "SELECT puerto_indicador1, puerto_indicador2 FROM tb_puertos"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_seleccionaPuertoArduino(self):
        cursor = self.conexionsql.cursor()
        sql = "SELECT puerto_indicadorArduino FROM tb_puertos"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def db_declaraPassword(self):
        cursor = self.conexionsql.cursor()
        sql = "SELECT passwordEliminar FROM tb_password"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
        
    def db_buscaCliente(self, valor):
        cursor = self.conexionsql.cursor()
        sql = "SELECT IFNULL(CONCAT_WS(' ', nombresCli, apellidoPaternoCli), '') AS nombre_completo, codigoCli, idEstadoCli FROM tb_clientes WHERE estadoEliminadoCli = 1 AND (CONCAT_WS(' ', nombresCli, apellidoPaternoCli) LIKE %s OR codigoCli LIKE %s)"
        cursor.execute(sql, ('%' + valor + '%', '%' + valor + '%'))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_traerPreciosCliente(self,codigoCli):
        cursor = self.conexionsql.cursor()
        sql = "SELECT primerEspecie,segundaEspecie,terceraEspecie,cuartaEspecie,quintaEspecie, sextaEspecie, septimaEspecie, octavaEspecie, novenaEspecie, decimaEspecie, decimaPrimeraEspecie, decimaSegundaEspecie, decimaTerceraEspecie, decimaCuartaEspecie, decimaQuintaOtrasEspecies FROM tb_precio_x_presentacion WHERE codigoCli = %s"
        cursor.execute(sql,(codigoCli,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_verificarProceso(self,codigoCli):
        cursor = self.conexionsql.cursor()    
        sql = "SELECT idProceso,codigoCli FROM tb_procesos WHERE codigoCli = %s AND fechaInicioPro = DATE(NOW())"
        cursor.execute(sql, (codigoCli,))        
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_registrarProceso(self, cliente):
        cursor = self.conexionsql.cursor()
        sql = "INSERT INTO tb_procesos(fechaInicioPro,horaInicioPro,codigoCli) VALUES (DATE(NOW()),TIME(NOW()), %s)"
        cursor.execute(sql,(cliente,))
        self.conexionsql.commit()
        cursor.close()
    
    def db_obtieneUltimoIdProcesoRegistrado(self):
        cursor = self.conexionsql.cursor()
        sql = "SELECT MAX(idProceso) AS idProceso FROM tb_procesos"
        cursor.execute(sql)        
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def db_registrarPesadas(self,numProceso,idEspecie,pesoNeto,horaPeso,codCliente,fechaPeso,cantidadRegistro,precioCliente,pesoNetoJabas,numeroJabasPes,numeroCubetasPes,estadoPeso,estadoWebPeso,tipoCubetas,coloresJabas,observacionPes):
        cursor = self.conexionsql.cursor()
        sql = """INSERT INTO tb_pesadas
                    (idProceso, idEspecie, pesoNetoPes, horaPes, codigoCli, fechaRegistroPes, cantidadPes, precioPes, pesoNetoJabas, numeroJabasPes, numeroCubetasPes, estadoPes, estadoWebPes, tipoCubetas, coloresJabas, observacionPes) 
                VALUES 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(numProceso,idEspecie,pesoNeto,horaPeso,codCliente,fechaPeso,cantidadRegistro,precioCliente,pesoNetoJabas,numeroJabasPes,numeroCubetasPes,estadoPeso,estadoWebPeso,tipoCubetas,coloresJabas,observacionPes))
        self.conexionsql.commit()
        cursor.close()
        
    def db_listarPesosTabla(self,numProceso,codigoCli):
        cursor = self.conexionsql.cursor()
        sql = """SELECT
                    CAST((@rownum:=@rownum-1) as INT) as num,
                    IFNULL(CONCAT_WS(' ', nombresCli, apellidoPaternoCli), '') AS cliente,
                    (SELECT TRUNCATE(pesoNetoPes / cantidadPes, 2) FROM tb_pesadas WHERE idPesada = p.idPesada) AS promedioPesoNetoCantidad,
                    nombreEspecie, TRUNCATE(pesoNetoPes, 2), cantidadPes, numeroJabasPes, coloresJabas, pesoNetoJabas, horaPes, estadoPes, idPesada
                FROM
                    (SELECT @rownum:=(SELECT COUNT(idPesada) FROM tb_pesadas WHERE fechaRegistroPes = DATE(NOW()) AND tb_pesadas.codigoCli = %s) + 1) r,
                    tb_pesadas p
                    INNER JOIN tb_clientes ON p.codigoCli = tb_clientes.codigoCli
                    INNER JOIN tb_procesos ON p.idProceso = tb_procesos.idProceso
                    INNER JOIN tb_especies_venta ON p.idEspecie = tb_especies_venta.idEspecie
                WHERE
                    p.fechaRegistroPes = DATE(NOW()) AND p.idProceso = %s AND p.codigoCli = %s AND p.estadoPes = 1
                ORDER BY
                    p.idPesada desc"""
        cursor.execute(sql,(codigoCli, numProceso, codigoCli))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_editarCantidadNueva(self, cantidadNueva, idPesadaEditarOEliminar):
        cursor = self.conexionsql.cursor()
        sql = "UPDATE tb_pesadas SET cantidadPes = %s WHERE idPesada = %s"
        cursor.execute(sql, (cantidadNueva, idPesadaEditarOEliminar))
        self.conexionsql.commit()
        cursor.close()
        
    def db_editarCantidadTaraNueva(self, cantidadNueva, idPesadaEditarOEliminar):
        cursor = self.conexionsql.cursor()
        sql = "UPDATE tb_pesadas SET numeroJabasPes = %s WHERE idPesada = %s"
        cursor.execute(sql, (cantidadNueva, idPesadaEditarOEliminar))
        self.conexionsql.commit()
        cursor.close()
        
    def db_editarCantidadDescuentoNueva(self, cantidadNueva, idPesadaEditarOEliminar):
        cursor = self.conexionsql.cursor()
        sql = "UPDATE tb_pesadas SET cantidadPes = %s WHERE idPesada = %s"
        cursor.execute(sql, (cantidadNueva, idPesadaEditarOEliminar))
        self.conexionsql.commit()
        cursor.close()
        
    def db_eliminarUltimaCantidad(self, idPesadaEditarOEliminar):
        cursor = self.conexionsql.cursor()
        sql = "UPDATE tb_pesadas SET estadoPes = 0 WHERE idPesada = %s"
        cursor.execute(sql, (idPesadaEditarOEliminar,))
        self.conexionsql.commit()
        cursor.close()
        
    def db_traerDatosReporte(self,numProceso,codigoCli):
        cursor = self.conexionsql.cursor()
        sql = """SELECT
                    nombreEspecie, TRUNCATE(pesoNetoPes, 2), cantidadPes, horaPes,numeroJabasPes
                FROM
                    tb_pesadas p
                    INNER JOIN tb_procesos ON p.idProceso = tb_procesos.idProceso
                    INNER JOIN tb_especies_venta ON p.idEspecie = tb_especies_venta.idEspecie
                WHERE
                    p.fechaRegistroPes = DATE(NOW()) AND p.idProceso = %s AND p.codigoCli = %s AND estadoPes = 1
                ORDER BY
                    p.idPesada asc"""
        cursor.execute(sql,(numProceso, codigoCli))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def db_verificarProveedor(self,codCliente):
        cursor = self.conexionsql.cursor()
        sql = """SELECT codigoCli FROM tb_clientes WHERE codigoCli = %s"""
        cursor.execute(sql, (codCliente, ))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def db_verificaridGrupoCli(self,codCliente):
        cursor = self.conexionsql.cursor()
        sql = """SELECT idGrupo FROM tb_clientes WHERE codigoCli = %s"""
        cursor.execute(sql, (codCliente, ))
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    
    def db_verificarPrecios(self,codCliente):
        cursor = self.conexionsql.cursor()
        sql = """SELECT primerEspecie,segundaEspecie,terceraEspecie,cuartaEspecie,valorConversionPrimerEspecie,valorConversionSegundaEspecie,valorConversionTerceraEspecie,valorConversionCuartaEspecie FROM tb_precio_x_presentacion WHERE codigoCli = %s"""
        cursor.execute(sql, (codCliente, ))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    ######################################################################################################
    ###################################### CONSULTAS A SERVIDOR WEB ######################################
    ######################################################################################################
        
# DISEÑADO Y DESARROLLADO POR SANTOS VILCHEZ EDINSON PASCUAL
# LA UNIÓN - PIURA - PERU ; 2023