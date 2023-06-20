# Instituto de Formación Técnica Superior Nro 18 - Profesor Eduardo Iberti 
# CARRERA de TÉCNICO SUPERIOR en DESARROLLO DE SOFTWARE - Trabajo Práctico Final Integrador
# Integrantes Dominguez Maximiliano, Kajita Lucas, Solano Santiago
# Tema: Sistema de gestión de obras públicas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

'''3. Crear el módulo “modelo_orm.py” que contenga la definición de las clases y sus atributos correspondientes que considere necesarios, siguiendo el modelo ORM de Peewee para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite llamada “obras_urbanas.db”, ubicada en la misma carpeta solución del proyecto. Aquí se debe incluir además la clase BaseModel heredando de peewee.Model.'''

from peewee import *

data_base = SqliteDatabase('./Dominguez - Kajita - Solano/obras_urbanas.db', pragmas={'journal_mode': 'wal'})
try:
    data_base.connect()
    print("Base de datos conectada con exito. ")
except OperationalError as e:
    print("Se ha generado un error en la conexion a la BD.", e)
    exit()

class BaseModel(Model):
    class Meta:
        database = data_base

class Etapa(BaseModel):
    nombre = CharField(unique=True)

class TipoObra(BaseModel):
    nombre = CharField(unique=True)

class AreaResponsable(BaseModel):
    nombre = CharField(unique=True)

class Obra(BaseModel): 
    # ID,entorno,nombre,etapa,tipo,area_responsable,descripcion,monto_contrato,comuna,barrio,direccion,lat,lng,fecha_inicio,fecha_fin_inicial,plazo_meses,porcentaje_avance,imagen_1,imagen_2,imagen_3,imagen_4,licitacion_oferta_empresa,licitacion_anio,contratacion_tipo,nro_contratacion,cuit_contratista,beneficiarios,mano_obra,compromiso,destacada,ba_elige,link_interno,pliego_descarga,expediente-numero,estudio_ambiental_descarga,financiamiento

    id = AutoField()
    entorno = CharField()
    nombre = CharField()
    etapa = ForeignKeyField(Etapa)
    tipo = ForeignKeyField(TipoObra)
    area_responsable = ForeignKeyField(AreaResponsable)
    descripcion = TextField()
    monto_contrato = DecimalField(max_digits=10, decimal_places=2)
    comuna = CharField()
    barrio = CharField()
    direccion = CharField()
    lat = FloatField()
    lng = FloatField()
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
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
    
    def nuevo_proyecto(self):
        self.etapa = Etapa.get_or_create(nombre='Proyecto')[0]
        self.save()

    def iniciar_contratacion(self, tipo_contratacion, nro_contratacion):
        self.etapa = Etapa.get_or_create(nombre='Contratación')[0]
        self.tipo_contratacion = tipo_contratacion
        self.nro_contratacion = nro_contratacion
        self.save()

    def adjudicar_obra(self, empresa, nro_expediente):
        self.etapa = Etapa.get_or_create(nombre='Adjudicada')[0]
        self.empresa = empresa
        self.nro_expediente = nro_expediente
        self.save()

    def iniciar_obra(self, destacada, fecha_inicio, fecha_fin_inicial, fuente_financiamiento, mano_obra):
        self.etapa = Etapa.get_or_create(nombre='En Progreso')[0]
        self.destacada = destacada
        self.fecha_inicio = fecha_inicio
        self.fecha_fin_inicial = fecha_fin_inicial
        self.fuente_financiamiento = fuente_financiamiento
        self.mano_obra = mano_obra
        self.save()

    def actualizar_porcentaje_avance(self, porcentaje):
        self.porcentaje_avance = porcentaje
        self.save()

    def incrementar_plazo(self, meses):
        self.plazo_meses += meses
        self.save()

    def incrementar_mano_obra(self, cantidad):
        self.mano_obra += cantidad
        self.save()

    def finalizar_obra(self):
        self.etapa = Etapa.get_or_create(nombre='Finalizada')[0]
        self.porcentaje_avance = 100
        self.save()

    def rescindir_obra(self):
        self.etapa = Etapa.get_or_create(nombre='Rescindida')[0]
        self.save()

def crear_tablas():
    with data_base:
        data_base.create_tables([Etapa, TipoObra, AreaResponsable, Obra])
