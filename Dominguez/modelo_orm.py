# Instituto de Formación Técnica Superior Nro 18 - Profesor Eduardo Iberti 
# CARRERA de TÉCNICO SUPERIOR en DESARROLLO DE SOFTWARE - Trabajo Práctico Final Integrador
# Integrantes Dominguez Maximiliano, Kajita Lucas, Solano Santiago
# Tema: Sistema de gestión de obras públicas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

'''3. Crear el módulo “modelo_orm.py” que contenga la definición de las clases y sus atributos correspondientes que considere necesarios, siguiendo el modelo ORM de Peewee para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite llamada “obras_urbanas.db”, ubicada en la misma carpeta solución del proyecto. Aquí se debe incluir además la clase BaseModel heredando de peewee.Model.'''

from peewee import *

data_base = SqliteDatabase('./Dominguez/obras_urbanas.db', pragmas={'journal_mode': 'wal'})
try:
    data_base.connect()
    print("Base de datos conectada con exito. ")
except OperationalError as e:
    print("Se ha generado un error en la conexion a la BD.", e)
    exit()

class BaseModel(Model):
    class Meta:
        database = data_base

'''5. La clase “Obra”, que es una de las clases que debe formar parte del modelo ORM, debe incluir los siguientes métodos de instancia con el objetivo de definir las diferentes etapas de avance de obra:'''

class Obra(BaseModel): 

    id = AutoField()
    entorno = CharField()
    nombre = CharField()
    etapa = CharField()
    tipo = CharField()
    area_responsable = CharField()
    descripcion = TextField()
    monto_contrato = DecimalField(max_digits=10, decimal_places=2)
    comuna = CharField()
    barrio = CharField()
    direccion = CharField()
    lat = FloatField()
    lng = FloatField()
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = IntegerField()
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()
    beneficiarios = IntegerField()
    mano_obra = IntegerField()
    compromiso = CharField()
    destacada = BooleanField()
    ba_elige = BooleanField()
    link_interno = CharField()
    pliego_descarga = CharField()
    expediente_numero = CharField()
    estudio_ambiental_descarga = CharField()
    financiamiento = CharField()

    class Meta:
        db_table = 'obras'

    def nuevo_proyecto():
        pass
    def iniciar_contratacion():
        pass
    def adjudicar_obra():
        pass
    def iniciar_obra():
        pass
    def actualizar_porcentaje_avance():
        pass
    def incrementar_plazo():
        pass
    def incrementar_mano_obra():
        pass
    def finalizar_obra():
        pass
    def rescindir_obra():
        pass

