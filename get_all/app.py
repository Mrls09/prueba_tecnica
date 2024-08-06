import json

import pymysql

from db import get_connection
from utils import headers_open

def get_all(event, context):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Recuperar todos los registros
        cursor.execute("""
            SELECT c.phone, c.age, nc.name, nc.lastname
            FROM customer c
            JOIN name_customer nc ON c.name_customer_id = nc.id
        """)

        # Obtener los resultados
        rows = cursor.fetchall()

        # Formatear los resultados
        customers = []
        for row in rows:
            customer = {
                "nombreCliente": {
                    "nombre": row['name'],
                    "apellido": row['lastname']
                },
                "telefono": row['phone'],
                "edad": row['age']
            }
            customers.append(customer)

        return {
            'statusCode': 200,
            'body': json.dumps(customers),
            'headers': headers_open
        }

    except pymysql.MySQLError as err:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error en la base de datos: {err}'}),
            'headers': headers_open
        }

    finally:
        cursor.close()
        connection.close()
