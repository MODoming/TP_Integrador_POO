# Instituto de Formación Técnica Superior Nro 18 - Profesor Eduardo Iberti 
# CARRERA de TÉCNICO SUPERIOR en DESARROLLO DE SOFTWARE - Trabajo Práctico Final Integrador
# Integrantes Dominguez Maximiliano, Kajita Lucas, Solano Santiago
# Tema: Sistema de gestión de obras públicas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

'''3. Crear el módulo “modelo_orm.py” que contenga la definición de las clases y sus atributos correspondientes que considere necesarios, siguiendo el modelo ORM de Peewee para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite llamada “obras_urbanas.db”, ubicada en la misma carpeta solución del proyecto. Aquí se debe incluir además la clase BaseModel heredando de peewee.Model.'''

from peewee import *

data_base = SqliteDatabase('obras_urbanas.db')
class BaseModel(Model):
    class Meta:
        database = data_base

'''5. La clase “Obra”, que es una de las clases que debe formar parte del modelo ORM, debe incluir los siguientes métodos de instancia con el objetivo de definir las diferentes etapas de avance de obra:'''

class Obra(BaseModel):
    id = AutoField()
    nombre = CharField()
    tipo = CharField()
    ubicacion = CharField()
    fecha_inicio = DateField()
    fecha_fin = DateField(null=True)
    costo = IntegerField()


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

