# Instituto de Formación Técnica Superior Nro 18 - Profesor Eduardo Iberti 
# CARRERA de TÉCNICO SUPERIOR en DESARROLLO DE SOFTWARE - Trabajo Práctico Final Integrador
# Integrantes Dominguez Maximiliano, Kajita Lucas, Solano Santiago
# Tema: Sistema de gestión de obras públicas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

'''3. Crear el módulo “modelo_orm.py” que contenga la definición de las clases y sus atributos correspondientes que considere necesarios, siguiendo el modelo ORM de Peewee para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite llamada “obras_urbanas.db”, ubicada en la misma carpeta solución del proyecto. Aquí se debe incluir además la clase BaseModel heredando de peewee.Model.'''

from peewee import *
import gestionar_obras

data_base = gestionar_obras.data_base

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
        self.etapa = Etapa.get_or_create(nombre='En Licitación')[0]
        self.save()

    def iniciar_contratacion(self, tipo_contratacion, nro_contratacion):
        self.contratacion_tipo = tipo_contratacion
        self.nro_contratacion = nro_contratacion
        self.save()

    def adjudicar_obra(self, empresa, nro_expediente):
        self.licitacion_oferta_empresa = empresa
        self.expediente_numero = nro_expediente
        self.save()

    def iniciar_obra(self, destacada, fecha_inicio, fecha_fin_inicial, fuente_financiamiento, mano_obra):
        self.etapa = Etapa.get_or_create(nombre='En Ejecución')[0]
        self.destacada = destacada
        self.fecha_inicio = fecha_inicio
        self.fecha_fin_inicial = fecha_fin_inicial
        self.financiamiento = fuente_financiamiento
        self.mano_obra = mano_obra
        self.save()

    def actualizar_porcentaje_avance(self):
        self.porcentaje_avance = input(int("Ingrese el nuevo porcentaje de la obra: "))
        self.save()
        print("Porcentaje actualizado. ")

    def incrementar_plazo(self):
        try:
            plazo_meses = input(int("Ingrese la cantidad de meses que quiere incrementar (solo nueros): "))
            self.plazo_meses += plazo_meses
            self.save()
        except Exception as e:
            print("Se ha generado un error ingresando los datos.", e)
            print("Vuelva a intentarlo.")

    def incrementar_mano_obra(self, mano_obra):
        self.mano_obra += mano_obra
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
