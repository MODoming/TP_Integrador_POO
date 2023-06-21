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
        ("Null",),
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
        ("Null",),
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
        ("Null",),
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
    entorno = CharField(null=True)
    nombre = CharField(null=True)
    etapa = ForeignKeyField(Etapa)
    tipo = ForeignKeyField(TipoObra)
    area_responsable = ForeignKeyField(AreaResponsable)
    descripcion = TextField(null=True)
    monto_contrato = DecimalField(null=True)
    comuna = CharField(null=True)
    barrio = CharField(null=True)
    direccion = CharField(null=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje_avance = IntegerField(null=True)
    imagen_1 = CharField(null=True)
    imagen_2 = CharField(null=True)
    imagen_3 = CharField(null=True)
    imagen_4 = CharField(null=True)
    licitacion_oferta_empresa = CharField(null=True)
    licitacion_anio = IntegerField(null=True)
    contratacion_tipo = CharField(null=True)
    nro_contratacion = CharField(null=True)
    cuit_contratista = CharField(null=True)
    beneficiarios = IntegerField(null=True)
    mano_obra = IntegerField(null=True)
    compromiso = CharField(null=True)
    destacada = BooleanField(null=True)
    ba_elige = BooleanField(null=True)
    link_interno = CharField(null=True)
    pliego_descarga = CharField(null=True)
    expediente_numero = CharField(null=True)
    estudio_ambiental_descarga = CharField(null=True)
    financiamiento = CharField(null=True)

    class Meta:
        db_table = 'obras'

    @classmethod
    def nuevo_proyecto(cls, entorno, nombre, etapa, tipo, a_responsable, descripcion, monto, comuna, barrio, direccion):
        nueva_obra = cls.create(entorno=entorno, nombre=nombre, etapa=etapa, tipo=tipo, area_responsable=a_responsable, descripcion=descripcion, monto=monto, comuna=comuna, barrio=barrio, direccion=direccion)
        return nueva_obra
    
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
