from pony.orm import db_session

from entities import TarjetaDeCredito, Pasajero

#
# The db_session() decorator performs the following actions on exiting function:
#
#  - Performs rollback of transaction if the function raises an exception
#  - Commits transaction if data was changed and no exceptions occurred
#  - Returns the database connection to the connection pool
#  - Clears the database session cache
#

@db_session
def cargar_datos_con_decoradores():
    pasajeros = [
        ('John', 20, 1234),
        ('Mary', 30, 1234555),
        ('Bob' , 40, 323232),
    ]
    for nombre, edad, numero in pasajeros:
        pasajero = Pasajero(nombre=nombre, edad=edad)
        TarjetaDeCredito(numero=numero, pasajero=pasajero)


def cargar_datos_con_with():
    pasajeros = [
        ('Juan', 20, 777777),
        ('Maria', 30, 88888),
        ('Bobito', 40, 999999),
    ]

    # Esta forma permite tener commits dentro de la misma función.
    with db_session:
        for nombre, edad, numero in pasajeros:
            pasajero = Pasajero(nombre=nombre, edad=edad)
            TarjetaDeCredito(numero=numero, pasajero=pasajero)
