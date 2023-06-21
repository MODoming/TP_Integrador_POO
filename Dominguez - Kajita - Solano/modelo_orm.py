# Instituto de Formación Técnica Superior Nro 18 - Profesor Eduardo Iberti 
# CARRERA de TÉCNICO SUPERIOR en DESARROLLO DE SOFTWARE - Trabajo Práctico Final Integrador
# Integrantes Dominguez Maximiliano, Kajita Lucas, Solano Santiago
# Tema: Sistema de gestión de obras públicas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

'''3. Crear el módulo “modelo_orm.py” que contenga la definición de las clases y sus atributos correspondientes que considere necesarios, siguiendo el modelo ORM de Peewee para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite llamada “obras_urbanas.db”, ubicada en la misma carpeta solución del proyecto. Aquí se debe incluir además la clase BaseModel heredando de peewee.Model.'''
from peewee import *
import gestionar_obras
import datetime

data_base = gestionar_obras.data_base

class BaseModel(Model):
    class Meta:
        database = data_base

class Etapa(BaseModel):
    nombre = CharField(unique=True)
    lista = [
        ("En Licitación",),
        ("En Ejecución",),
        ("Finalizada",),
        ("Desestimada",),
        ("Pausada",),
    ]

    @classmethod
    def cargar_lista(cls):
        with data_base.atomic():
            cls.insert_many(cls.lista, fields=[cls.nombre]).execute()

    @classmethod
    def imprimir_lista(cls):
        print("Lista de ingreso para elegir: ")
        for item in cls.lista:
            print(f"\t{item[0]}")

class TipoObra(BaseModel):
    nombre = CharField(unique=True)
    lista = [
        ("Arquitectura",),
        ("Escuela",),
        ("Espacio Público",),
        ("Hidráulica",),
        ("Salud",),
        ("Transporte",),
        ("Vivienda",),
    ]

    @classmethod
    def cargar_lista(cls):
        with data_base.atomic():
            cls.insert_many(cls.lista, fields=[cls.nombre]).execute()

    @classmethod
    def imprimir_lista(cls):
        print("Lista de ingreso para elegir: ")
        for item in cls.lista:
            print(f"\t{item[0]}")

class AreaResponsable(BaseModel):
    nombre = CharField(unique=True)
    lista = [
        ("Corporación Buenos Aires Sur",),
        ("Instituto de la Vivienda",),
        ("Ministerio de Cultura",),
        ("Ministerio de Desarrollo Humano y Hábitat",),
        ("Ministerio de Educación",),
        ("Ministerio de Espacio Público e Higiene Urbana",),
        ("Ministerio de Justicia y Seguridad",),
        ("Ministerio de Salud",),
        ("Secretarí­a de Transporte y Obras Públicas",),
        ("Subsecretarí­a de Gestión Comunal",),
    ]

    @classmethod
    def cargar_lista(cls):
        with data_base.atomic():
            cls.insert_many(cls.lista, fields=[cls.nombre]).execute()

    @classmethod
    def imprimir_lista(cls):
        print("Lista de ingreso para elegir: ")
        for item in cls.lista:
            print(f"\t{item[0]}")

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

    def nuevo_proyecto(self, entorno, nombre, tipo, a_responsable, descripcion, monto="", comuna="", barrio="", direccion=""):
        '''etapa_proyecto, _ = Etapa.get_or_create(nombre='En Licitación')
        self.etapa = etapa_proyecto'''
        self.entorno = entorno
        self.nombre = nombre
        self.tipo = tipo
        self.area_responsable = a_responsable
        self.descripcion = descripcion
        self.monto_contrato = monto
        self.comuna = comuna
        self.barrio = barrio
        self.direccion = direccion
        self.save()

    def iniciar_contratacion(self):
        tipo_contratacion = input("Ingrese el tipo de contratacion: ")
        nro_contratacion = input("Ingrese el numero de contratacion: ")
        self.contratacion_tipo = tipo_contratacion
        self.nro_contratacion = nro_contratacion
        self.save()

    def adjudicar_obra(self):
        empresa = input("Ingrese el nombre de la empresa adjudicatoria: ")
        nro_expediente = input("Ingrese el numero de expediente: ")
        self.licitacion_oferta_empresa = empresa
        self.expediente_numero = nro_expediente
        self.save()

    def iniciar_obra(self):
        try:
            print("Para inicializar la obra hacen falta unos datos que solicitaremos a continuación: ")
            fecha_inicial = input("Ingresa la fecha de inicio de obra (dd/mm/aaaa): ")
            fecha_final = input("Ingresa la fecha de finalización de obra (dd/mm/aaaa): ")
            m_obra = input("Ingrese la cantidad de mano de obra contratada: ")
            destacada = input("Desea destacar la obra? si/no: ")
            f_inicial = datetime.datetime.strptime(fecha_inicial, "%d/%m/%Y")
            f_final = datetime.datetime.strptime(fecha_final, "%d/%m/%Y")
            diferencia = (f_final.date() - f_inicial.date()).days
            meses = diferencia // 30
            etapa_ejecucion, _ = Etapa.get_or_create(nombre='En Ejecución')
            self.etapa = etapa_ejecucion
            self.destacada = destacada
            self.fecha_inicio = f_inicial.date()
            self.fecha_fin_inicial = f_final.date()
            self.mano_obra = m_obra
            self.plazo_meses = meses
            self.save()
        except Exception as e:
            print("Se ha generado un error ingresando los datos:", e)
            print("Vuelva a intentarlo.")

    def actualizar_porcentaje_avance(self):
        try:
            porcentaje = input("Ingrese el nuevo porcentaje de la obra: ")
            self.porcentaje_avance = porcentaje
            self.save()
            print("Porcentaje actualizado.")
        except Exception as e:
            print("Se ha generado un error ingresando los datos:", e)
            print("Vuelva a intentarlo.")

    def incrementar_plazo(self):
        try:
            plazo_meses = input("Ingrese la cantidad de meses que quiere incrementar (solo números): ")
            self.plazo_meses += int(plazo_meses)
            self.save()
        except Exception as e:
            print("Se ha generado un error ingresando los datos:", e)
            print("Vuelva a intentarlo.")

    def incrementar_mano_obra(self):
        try:
            mano_obra = input("Ingrese la cantidad de mano de obra que va a incrementar: ")
            self.mano_obra += int(mano_obra)
            self.save()
        except Exception as e:
            print("Se ha generado un error ingresando los datos:", e)
            print("Vuelva a intentarlo.")

    def finalizar_obra(self):
        etapa_finalizada, _ = Etapa.get_or_create(nombre='Finalizada')
        self.etapa = etapa_finalizada
        self.porcentaje_avance = 100
        self.save()

    def rescindir_obra(self):
        etapa_desestimada, _ = Etapa.get_or_create(nombre='Desestimada')
        self.etapa = etapa_desestimada
        self.save()
