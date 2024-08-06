import json

import pymysql

from db import get_connection
from utils import headers_open


def validate_data(name_customer_data, phone, age):
    if not name_customer_data or phone is None or age is None:
        return {'statusCode': 400, 'body': {'message': 'Datos incompletos'}}

    name = name_customer_data.get('nombre')
    lastname = name_customer_data.get('apellido')

    if not name or not lastname:
        return {'statusCode': 400, 'body': {'message': 'Datos del nombre del cliente incompletos'}}

    if not isinstance(name, str) or not isinstance(lastname, str):
        return {'statusCode': 400, 'body': {'message': 'Nombre y apellido deben ser cadenas de texto'}}

    if not isinstance(phone, int) or not (1000000000 <= phone <= 9999999999):
        return {'statusCode': 400, 'body': {'message': 'Teléfono debe ser un número entero de 10 dígitos'}}

    if not isinstance(age, int) or age <= 18:
        return {'statusCode': 400, 'body': {'message': 'Edad debe ser un número mayor de 18 años'}}

    return None


def create_customer(event, context):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Extraer datos del evento
        data = json.loads(event['body'])
        name_customer_data = data.get('nombreCliente')
        phone = data.get('telefono')
        age = data.get('edad')

        # Asegurarse de que telefono y edad sean enteros
        if phone is not None:
            phone = int(phone)
        if age is not None:
            age = int(age)

        # Validar los datos
        validation_result = validate_data(name_customer_data, phone, age)
        if validation_result:
            return {
                'statusCode': validation_result['statusCode'],
                'body': json.dumps(validation_result['body']),
                'headers': headers_open
            }

        name = name_customer_data.get('nombre')
        lastname = name_customer_data.get('apellido')

        # Ejecutar consulta para verificar si el cliente existe
        cursor.execute("SELECT phone FROM customer WHERE phone = %s", (phone,))
        exist = cursor.fetchone()
        # Verificar si el cliente existe
        if exist is not None:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Cliente ya existente' }),
                'headers': headers_open
            }

        # Insertar datos en la tabla nombre_cliente
        cursor.execute("""
            INSERT INTO name_customer (name, lastname)
            VALUES (%s, %s)
        """, (name, lastname))

        # Obtener el ID del nuevo nombre_cliente
        name_customer_id = cursor.lastrowid

        # Insertar datos en la tabla cliente
        cursor.execute("""
            INSERT INTO customer (phone, age, name_customer_id)
            VALUES (%s, %s, %s)
        """, (phone, age, name_customer_id))

        #Confirmar cambios
        connection.commit()

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Cliente creado exitosamente'}),
            'headers': headers_open
        }

    except pymysql.MySQLError as err:
        connection.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error en la base de datos: {err}'}),
            'headers': headers_open
        }

    finally:
        cursor.close()
        connection.close()
