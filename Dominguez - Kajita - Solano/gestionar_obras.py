# Instituto de Formación Técnica Superior Nro 18 - Profesor Eduardo Iberti 
# CARRERA de TÉCNICO SUPERIOR en DESARROLLO DE SOFTWARE - Trabajo Práctico Final Integrador
# Integrantes Dominguez Maximiliano, Kajita Lucas, Solano Santiago
# Tema: Sistema de gestión de obras públicas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

from abc import ABC, abstractmethod
import pandas as pd
from peewee import *
from modelo_orm import *

data_base = SqliteDatabase('./Dominguez - Kajita - Solano/obras_urbanas.db', pragmas={'journal_mode': 'wal'})

class GestionarObra(ABC):    
    @classmethod
    def extraer_datos(cls):
        # Cargar el archivo CSV en un objeto DataFrame
        dataset = pd.read_csv('.\Dominguez - Kajita - Solano\observatorio-de-obras-urbanas.csv')
        return dataset
    
    @classmethod
    def conectar_db(cls): # que debe incluir las sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”.
        try:
            data_base.connect()
            print("Base de datos conectada con exito. ")
        except OperationalError as e:
            print("Se ha generado un error en la conexion a la BD.", e)
            exit()
        return data_base

    @classmethod
    def mapear_orm(cls):
        try:
            db = cls.conectar_db()
            db.create_tables([TipoObra, AreaResponsable, Etapa, Obra])
            try:
                Etapa.cargar_lista()
                TipoObra.cargar_lista()
                AreaResponsable.cargar_lista()
            except:
                print("Los datos ya existen.")
        except Exception as e:
            print(e)

    @classmethod
    def limpiar_datos(cls, df):
        cleaned_df = df.dropna()  # Eliminar filas con valores nulos
        cleaned_df = cleaned_df.drop_duplicates()  # Eliminar filas duplicadas
        return cleaned_df


    @classmethod
    def cargar_datos(cls): # que debe incluir las sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de datos relacional SQLite. Para ello se debe utilizar el método de clase Model create() en cada una de las clase del modelo ORM definido.
        pass

    @classmethod
    def nueva_obra(cls):
        entorno = "casa" #input("Ingrese el entorno de la obra: ")
        nombre = "Casita" #input("Ingrese el nombre de la obra: ")
        tipo = "Vivienda" #input("Ingrese el tipo de obra: ")
        tipo_obra = TipoObra.get_or_none(nombre=tipo)
        while tipo_obra is None:
            print("El tipo de obra ingresado no existe. Intente nuevamente.")
            TipoObra.imprimir_lista()
            tipo = input("Ingrese el nombre del tipo de obra: ")
            tipo_obra = TipoObra.get_or_none(nombre=tipo)
        area = "Instituto de la Vivienda" #input("Ingrese el area responsable de la obra: ")
        a_resp = AreaResponsable.get_or_none(nombre=area)
        while a_resp is None:
            print("El area responsable ingresada no existe. Intente nuevamente.")
            AreaResponsable.imprimir_lista()
            area = input("Ingrese el area responsable de la obra: ")
            a_resp = AreaResponsable.get_or_none(nombre=area)
        descripcion = "Casas" # input("Ingrese una descripcion de la obra: ")
        monto = "12345678" #input("Ingrese el monto expresado en pesos: ")
        direccion = "Calle Falsa 1234" #input("Ingrese el domicilio de la obra: ")
        comuna = "15" #input("Ingrese la comuna: ")
        barrio = input("Ingrese el barrio: ")
        nueva_obra = Obra.nuevo_proyecto(entorno=entorno, nombre=nombre, etapa='En Licitación', tipo=tipo, a_responsable=a_resp, descripcion=descripcion, monto=monto, comuna=comuna, barrio=barrio, direccion=direccion)
        nueva_obra.save()
        data_base.close()
        return nueva_obra

    @classmethod
    def obtener_indicadores(cls): # que debe incluir las sentencias necesarias para obtener información de las obras existentes en la base de datos SQLite a través de sentencias ORM.'''
        pass

if __name__== "__main__" :
    GestionarObra.mapear_orm()

    obra1 = GestionarObra.nueva_obra()
    obra2 = GestionarObra.nueva_obra()



