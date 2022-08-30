from datetime import datetime
from pony.orm import *

db = Database()

class Pasajero(db.Entity):
    id = PrimaryKey(int, auto=True)
    nombre = Required(str)
    edad = Required(int)
    reservas = Set('Reserva')
    tarjeta_de_creditos = Set('TarjetaDeCredito')


class Habitacion(db.Entity):
    id = PrimaryKey(int, auto=True)
    Pax = Required(int)
    reservas = Set('Reserva')


class Reserva(db.Entity):
    id = PrimaryKey(int, auto=True)
    habitacion = Required(Habitacion)
    pasajero = Required(Pasajero)
    estado = Required(str)
    ingreso = Required(datetime)
    egreso = Required(datetime)
    fecha_cancelacion = Optional(datetime)
    factura = Optional('Factura')


class TarjetaDeCredito(db.Entity):
    id = PrimaryKey(int, auto=True)
    numero = Required(int)
    vencimiento = Optional(datetime)
    pasajero = Required(Pasajero)


class Factura(db.Entity):
    id = PrimaryKey(int, auto=True)
    reserva = Required(Reserva)
    monto = Optional(float)



#db.generate_mapping()
# Configuramos la base de datos.
# Más info: https://docs.ponyorm.org/database.html

db.bind('sqlite', 'example.sqlite', create_db=True)  # Conectamos el objeto `db` con la base de dato.
db.generate_mapping(create_tables=True)  # Generamos las base de datos.
