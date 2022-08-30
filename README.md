# pony_orm_2022
Un repo donde hay un Pony orm galopando por acá o por alla.

## Comentarios previos a las clases:

1. Qué pensaba yo que era programar durante mi vida acádemica y que pienso ahora qué es programar (por si me olvide: lo de siempre + saber de frameworks + testear).
2. Usen la documentación oficial. Siempre va a estar ahí.
3. Un buen equipo de desarrollo es previsible. Si digo "Voy a hacer A", entonces A se hace. Si se va a ir todo al caño, avisen con tiempo, es bueno saberlo para manejar las expectativas.
4. Participen en comunidades. Mirense videos de charlas en eventos. Cuando se acabe la pandemia, busquen ampliar sus circulos sociales.
5. Lean libros.
6. Escriban "código bonito" siempre, en todo contexto.


## Generemos un diagrama de clases del ejercicio "Reservas de habitaciones" del práctico 2:

Se desea desarrollar un sistema informático para la gestión de las reservas de las habitaciones de un hotel. Cada reserva estará a nombre de un cliente, que proporcionará un número de tarjeta de crédito para efectuar el pago.

El número de tarjeta de crédito es indispensable para poder realizar la reserva. Se podría reservar habitación para cierto número de días consecutivos.

Cuando el cliente se presenta para aprovechar la reserva en la fecha de comienzo indicada, el sistema pasa la reserva a la situación de ocupada. Cuando llega la fecha de terminación de la reserva, o si el cliente solicita la terminación anticipada, el sistema pasa la reserva a la situación de terminada y tramita la creación de una factura,
que se cobrará en general automáticamente de la tarjeta de crédito del cliente.

El cliente tiene sin embargo la opción de otras formas de pago al finalizar la reserva (contado, tarjeta de crédito alternativa, etc.).

El cliente puede cancelar una reserva hasta una semana antes de la fecha inicial, en cuyo caso no se le pasaría al cobro factura alguna. En caso de cancelar la reserva con menos de 7 días de anticipación, se le cobrará de su tarjeta de crédito el valor correspondiente a un día de hospedaje


Vamos a hacer un [diseño usando la herramienta de Pony](https://editor.ponyorm.com/user/chun/ReservasHotel2022/designer).


## Instalación

1. Descargar el repo.
2. Entrar a la carpeta descagada
3. Crear un entorno virtual con python3.
4. Levantar el entorno virtual
5. Instalar los requerimientos

```
$ git clone https://github.com/matiaslee/pony_orm_2022.git
$ cd pony_orm_2022/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Explorando el archivo `entities.py`

En el archivo `entities.py` vamos a encontrar la como se crean "entidades" (clases de python que guardan datos en una base de dato) y y la configuración de la base de datos.

Las entidades de ese archivo están basadas en la [sección primeros pasos de la documentación de Pony](https://docs.ponyorm.org/firststeps.html)

  - Cosas feas: La versión actual no soporta migraciones. :(  (al menos no durante 2021...)

## Jugando con Pony!

Dentro del virtual env, levantemos python y juguemos con la entidad `Pasajero`.

```
(venv) $ python
Python 3.6.9 (default, Jul 17 2020, 12:50:27)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from entities import Pasajero
>>> p = Pasajero(nombre='Matias Lee')
>>> p
Person[new:1]
>>> p.nombre
'Matias Lee'
```
En otra consola, hagamos un `cat` al archivo `example.sqlite`

```
$ cat example.sqlite
```

Deberíamos ver la estructura de la base de datos peeeeero ningun dato, pues los datos que escribimos todavia no fuerom "commiteados".  Commitemoslos, en la consola de python:

```
>>> from pony.orm import commit
>>> commit()
```

Si volvemos a ejecutar `cat example.sqlite` en la otra consola deberíamos ver que no está vacia.

## Funciones que se conectan a la base de dato.

Veamos el archivo `some_functions.py`.

   - `cargar_datos_con_decoradores`: carga algunos datos usando el decorador/decorator `db_session`.
   - `cargar_datos_con_with` usa el with statement (con `db_session`) para cargar datos. Esto permite conexiones dentro de funciones.

Corramos las funciones
```
>>> from some_functions import *
>>> cargar_datos_con_decoradores()
>>> cargar_datos_con_with()

```
Veamos que tenemos datos datos para acceder:
```
>>> Pasajero.select().show()
id|nombre|edad
--+------+----
1 |John  |20
2 |Mary  |30
3 |Bob   |40
4 |Juan  |20
5 |Maria |30
6 |Bobito|40
>>>

```

No nos muestra data de la tarjeta porque eso es una relación

## Queries

Las queryes se construyen usando `generadores`.  Por ejemplo

```
>>> select(p for p in Pasajero if p.edad > 31)
<pony.orm.core.Query object at 0x7f167c08b130>
```

El resultado es un objeto `Query` que nos dice mucho. Podermos usar el método `show` para ver mejor esto:

```
>>> select(p for p in Pasajero if p.edad > 31).show()
id|nombre|edad
--+------+----
3 |Bob   |40
6 |Bobito|40
```

Podemos ver que query de sql se realiza si activamos el modo debug:

```
>>> from pony.orm import set_sql_debug
>>> set_sql_debug(True)
>>> select(p for p in Pasajero if p.edad > 31).show()

SELECT "p"."id", "p"."nombre", "p"."edad"
FROM "Pasajero" "p"
WHERE "p"."edad" > 31

id|nombre|edad
--+------+----
3 |Bob   |40
6 |Bobito|40

>>> set_sql_debug(False)
>>>
```

Dada una consulta, podemos devolver una lista con
  - todos los objetos,
  - solo los primeros N objetos,
  - pero no podemos tomar los últimos N objetos

Por ejemplo:

```
>>> select(p for p in Pasajero if p.edad > 20)[:]
[Pasajero[2], Pasajero[3], Pasajero[5], Pasajero[6]]
>>> select(p for p in Pasajero if p.edad > 20)[:2]
[Pasajero[2], Pasajero[3]]
>>> select(p for p in Pasajero if p.edad > 20)[-2:]
...
TypeError: Parameter 'start' of slice object cannot be negative
```

En vez de construir una lista con entidades se puede construir una lista con atributos de las entidads:

```
>>> select(p.nombre for p in Pasajero if p.edad > 20)[:]
['Mary', 'Bob', 'Maria', 'Bobito']
```

Se pueden devolver tb listas mas complejas

```
>>> from pony.orm import count
>>> select((p, count(p.tarjeta_de_creditos)) for p in Pasajero)[:3]
[(Pasajero[1], 1), (Pasajero[2], 1), (Pasajero[3], 1)]
```

##  Manipulando entidades:

Obtener un objeto directamente por su id:

```
>>> Pasajero[1]    # Tenemos el objeto
Pasajero[1]
>>> Pasajero[1].nombre  # Lo podemos acceder directamente
'John'
>>> Pasajero[100]  # el id no existe, error.
...
pony.orm.core.ObjectNotFound: Pasajero[100]
```

Con el método `get` sobre una entidad podemos buscar por atributo. Si existe más de una entidad que satisface el criterio habrá un error. Si no existe estidad la función no devulve nada:

```
>>> Pasajero.get(nombre="Bobito") # Solo existe un Bobito
Pasajero[6]
>>> Pasajero.get(edad=30) # Hay más de una persona con 30 años.
Traceback (most recent call last):
...
pony.orm.core.MultipleObjectsFoundError: Multiple objects were found. Use Person.select(...) to retrieve them

>>> Pasajero.get(name='Chun')  # Chun no existis.
>>>
```

Los entidades pueden ser asignadas a variables, manipuladas modificadas y luego guardadas en la base de datos.

```
>>> bobito = Pasajero.get(nombre="Bobito")
>>> bobito.edad
40
>>> bobito.edad = 25
>>> commit()
>>> bobito = Pasajero.get(nombre="Bobito")
>>> bobito.edad
25

```



##  Relaciones

```
class Alumno(db.Entity):
    nota_evaluacion = Set('NotaEvaluacion')

class NotaEvaluacion(db.Entity):
    alumno = Required(Alumno)
    nota = Required(int)
```

 - Declaración explicita: ambos objetos tiene que establecer la relación
 - Tres tipos de relación one-to-one, one-to-many y many-to-many.

### One-to-one

Ejemplos:

- "Una persana puede tener un pasaporte y ningun pasaporte es compartido por dos personas"


```

class Person(db.Entity):
    passport = Optional("Passport") # "puede tener pasaporte" es optativo.
    ...

class Passport(db.Entity):
    person = Required("Person") # Un pasaporte no puede existir sin una persona
    ...

```

- "Toda persona tiene un DNI y ningún DNI es compartido por dos personas"


```

class Person(db.Entity):
    passport = Required("Passport") # "puede tener pasaporte" es optativo.
    ...


class Dni(db.Entity):
    person = Required("Person") # Un pasaporte no puede existir sin una persona
    ...

```



```
class Order(db.Entity):
    items = Set("OrderItem")

class OrderItem(db.Entity):
    order = Optional(Order)

```

### one-to-many

El ejemplo que vimos: "Los alumnos tienen notas"

```
class Alumno(db.Entity):
    nota_evaluacion = Set('NotaEvaluacion')

class NotaEvaluacion(db.Entity):
    alumno = Required(Alumno)
    nota = Required(int)
```


### many-to-many

```
class Materia(db.Entity):
    nombre = Required(str)
    profesores = Set("Profesor")


class Profesor(db.Entity):
    nombre = Required(str)
    materias = Set(Materia)
```

### Jugando con las relaciones!

La última relacion está en el archivo relations.py. Carguemolo.

Vamos a crear un profesor y una materia con ese profesor.

```
>>> from relations import *
>>> matias = Profesor(nombre='Matias')
>>> matias.materias.select().show()
id|nombre
--+------

>>> ingenieria = Materia(nombre="Ingenieria", profesores=[matias])
>>> matias.materias.select().show()
id|nombre
--+------
2 |Ingenieria
```

Vamos a crear ahora a una profesora  y agregarla como docente de la materia que creamos.

```
>>> laura = Profesor(nombre='Laura')
>>> ingenieria.profesores.select().show()
id|nombre
--+------
1 |Matias

>>> ingenieria.profesores.add(laura)
>>> ingenieria.profesores.select().show()
id|nombre
--+------
1 |Matias
2 |Laura
```

Como el primer profesor estaba flojo de papeles, lo sacaron de la materia.

```
>>> ingenieria.profesores.remove(matias)
>>> ingenieria.profesores.select().show()

id|nombre
--+------
2 |Laura
>>> commit()
```

La función `show`, te muestra las relaciones "to-one":

```
>>> TarjetaDeCredito.select().show()
id|numero |vencimiento|pasajero
--+-------+-----------+-----------
1 |1234   |None       |Pasajero[1]
2 |1234555|None       |Pasajero[2]
3 |323232 |None       |Pasajero[3]
4 |777777 |None       |Pasajero[4]
5 |88888  |None       |Pasajero[5]
6 |999999 |None       |Pasajero[6]
>>>
```

Pero no te muestra las relaciones "to many":

```
>>> Pasajero.select().show()
id|nombre|edad
--+------+----
1 |John  |20
2 |Mary  |30
3 |Bob   |40
4 |Juan  |20
5 |Maria |30
6 |Bobito|25
```

Podemos hacer queries de objetos en función de atributos de low objetos a los que se relaciona. Por ejemplo, podemos seleccionar los tarjetas con dueños mayores a 25 años:

```
>>> select(tarjeta for tarjeta in TarjetaDeCredito if tarjeta.pasajero.edad > 25).show()
id|numero |vencimiento|pasajero
--+-------+-----------+-----------
2 |1234555|None       |Pasajero[2]
3 |323232 |None       |Pasajero[3]
5 |88888  |None       |Pasajero[5]
```

O seleccionar directamente objectos de la relacion, por ejemplo, los dueños de autos mayores a 30:

```
>>> select(tarjeta.pasajero for tarjeta in TarjetaDeCredito if tarjeta.pasajero.edad > 25).show()
id|nombre|edad
--+------+----
2 |Mary  |30
3 |Bob   |40
5 |Maria |30
```



Fin!

## Agregaciones!

Se pueden realizar otras operaciones como contar, sumar, sacar el máximo, mínimo, promedio y agrupar en funcion de condiciones para despues volver a operar. Vean esta [sección](https://docs.ponyorm.org/aggregations.html) de la documentación.
