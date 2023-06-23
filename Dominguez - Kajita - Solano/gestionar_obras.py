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
        print("Datos extraidos...")
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
        print("Datos limpios...")
        return cleaned_df


    @classmethod
    def cargar_datos(cls):
        datos = cls.extraer_datos()
        df = cls.limpiar_datos(datos)
        # Persistir los datos de las obras en la base de datos
        for _, row in datos.iterrows():
            tipo_obra = TipoObra.get_or_create(nombre=row['tipo'])[0]
            area_responsable = AreaResponsable.get_or_create(nombre=row['area_responsable'])[0]
            etapa = Etapa.get_or_create(nombre=row['etapa'])[0]
            Obra.create(
                entorno = row["entorno"],
                nombre = row["nombre"],
                etapa = etapa,
                tipo = tipo_obra,
                area_responsable = area_responsable,
                descripcion = row["descripcion"],
                monto_contrato = row["monto_contrato"],
                comuna = row["comuna"],
                barrio = row["barrio"],
                direccion = row["direccion"],
                lat = row["lat"],
                lng = row["lng"],
                fecha_inicio = row["fecha_inicio"],
                fecha_fin_inicial = row["fecha_fin_inicial"],
                plazo_meses = row["plazo_meses"],
                porcentaje_avance = row["porcentaje_avance"],
                imagen_1 = row["imagen_1"],
                imagen_2 = row["imagen_2"],
                imagen_3 = row["imagen_3"],
                imagen_4 = row["imagen_4"],
                licitacion_oferta_empresa = row["licitacion_oferta_empresa"],
                licitacion_anio = row["licitacion_anio"],
                contratacion_tipo = row["contratacion_tipo"],
                nro_contratacion = row["nro_contratacion"],
                cuit_contratista = row["cuit_contratista"],
                beneficiarios = row["beneficiarios"],
                mano_obra = row["mano_obra"],
                compromiso = row["compromiso"],
                destacada = row["destacada"],
                ba_elige = row["ba_elige"],
                link_interno = row["link_interno"],
                pliego_descarga = row["pliego_descarga"],
                expediente_numero = row["expediente-numero"],
                estudio_ambiental_descarga = row["estudio_ambiental_descarga"],
                financiamiento = row["financiamiento"]
            ).save()

    @classmethod
    def nueva_obra(cls):
        entorno = "Casas"# input("Ingrese el entorno de la obra: ")
        nombre = "casuchas"# input("Ingrese el nombre de la obra: ")
        tipo = "Vivienda"# input("Ingrese el tipo de obra: ")
        tipo_obra = TipoObra.get_or_none(nombre=tipo)
        while tipo_obra is None:
            print("El tipo de obra ingresado no existe. Intente nuevamente.")
            TipoObra.imprimir_lista()
            tipo = input("Ingrese el nombre del tipo de obra: ")
            tipo_obra = TipoObra.get_or_none(nombre=tipo)
        area = "Instituto de la Vivienda"# input("Ingrese el area responsable de la obra: ")
        a_resp = AreaResponsable.get_or_none(nombre=area)
        while a_resp is None:
            print("El area responsable ingresada no existe. Intente nuevamente.")
            AreaResponsable.imprimir_lista()
            area = input("Ingrese el area responsable de la obra: ")
            a_resp = AreaResponsable.get_or_none(nombre=area)
        descripcion = "Cualquier cosa"# input("Ingrese una descripcion de la obra: ")
        monto = "12345"# input("Ingrese el monto expresado en pesos: ")
        direccion = "Sin calle 123"# input("Ingrese el domicilio de la obra: ")
        comuna = "3"# input("Ingrese la comuna: ")
        barrio = "Otro"# input("Ingrese el barrio: ")
        nueva_obra = Obra.nuevo_proyecto(entorno=entorno, nombre=nombre, etapa='En Licitación', tipo=tipo_obra, a_responsable=a_resp, descripcion=descripcion, monto=monto, comuna=comuna, barrio=barrio, direccion=direccion)
        nueva_obra.save()
        data_base.close()
        return nueva_obra

    @classmethod
    def obtener_indicadores(cls):
        cantidad_obras = Obra.select().count()
        monto_total = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()
        promedio_monto = Obra.select(fn.AVG(Obra.monto_contrato)).scalar()
        print(f"Hay un total de {cantidad_obras} obras. ")
        print(f"El monto total de todas las obras es de {monto_total}$. ")
        print(f"La media del monto contratado por cada una de estas obras es {promedio_monto}$. ")
        return cantidad_obras, monto_total, promedio_monto

if __name__== "__main__" :
    GestionarObra.mapear_orm()
    #GestionarObra.cargar_datos()
    #GestionarObra.obtener_indicadores()

    obra1 = GestionarObra.nueva_obra()
    #obra3 = GestionarObra.nueva_obra()
    obra1.iniciar_contratacion()



