import json
import pymysql
from db import get_connection
from utils import headers_open


def validate_update_data(nombre_cliente_data, telefono, edad):
    # Validaciones
    if not nombre_cliente_data or telefono is None or edad is None:
        return {'statusCode': 400, 'body': {'message': 'Datos incompletos'}}

    nombre = nombre_cliente_data.get('nombre')
    apellido = nombre_cliente_data.get('apellido')

    if not nombre or not apellido:
        return {'statusCode': 400, 'body': {'message': 'Datos del nombre del cliente incompletos'}}

    if not isinstance(nombre, str) or not isinstance(apellido, str):
        return {'statusCode': 400, 'body': {'message': 'Nombre y apellido deben ser cadenas de texto'}}

    if not isinstance(telefono, int) or not (1000000000 <= telefono <= 9999999999):
        return {'statusCode': 400, 'body': {'message': 'Teléfono debe ser un número entero de 10 dígitos'}}

    if not isinstance(edad, int) or edad <= 18:
        return {'statusCode': 400, 'body': {'message': 'Edad debe ser un número mayor de 18 años'}}

    return None

def update_customer(event, context):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        body = event.get('body')
        if body is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'El cuerpo de la solicitud está vacío'}),
                'headers': headers_open
            }

        data = json.loads(body)
        name_customer_data = data.get('nombreCliente')
        phone = data.get('telefono')
        age = data.get('edad')

        # Asegurarse de que telefono y edad sean enteros
        if phone is not None:
            phone = int(phone)
        if age is not None:
            age = int(age)

        # Validar los datos
        validation_result = validate_update_data(name_customer_data, phone, age)
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
        if exist is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Cliente no encontrado'}),
                'headers': headers_open
            }

        # Actualizar datos en la tabla nombre_cliente
        cursor.execute("""
            UPDATE name_customer
            SET name = %s, lastname = %s
            WHERE id = (SELECT name_customer_id FROM customer WHERE phone = %s)
        """, (name, lastname, phone))

        # Actualizar datos en la tabla cliente
        cursor.execute("""
            UPDATE customer
            SET age = %s
            WHERE phone = %s
        """, (age, phone))

        # Confirmar cambios
        connection.commit()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Cliente actualizado exitosamente'}),
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
