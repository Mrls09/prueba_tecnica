import json
import pymysql
from db import get_connection
from utils import headers_open

def delete_customer(event, context):
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
        phone = data.get('telefono')
        if not phone:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Telefono es requerido'}),
                'headers': headers_open
            }

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

        # Delete customer data from the customer table
        cursor.execute("DELETE FROM customer WHERE phone = %s", (phone,))

        # Delete data from the name_customer table if there are no references
        cursor.execute("""
            DELETE FROM name_customer 
            WHERE id NOT IN (SELECT name_customer_id FROM customer)
            AND id = (
                SELECT name_customer_id FROM customer WHERE phone = %s
            )
        """, (phone,))

        # Confirm changes
        connection.commit()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Cliente eliminado correctamente'}),
            'headers': headers_open
        }

    except pymysql.MySQLError as err:
        connection.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Database error: {err}'}),
            'headers': headers_open
        }

    finally:
        cursor.close()
        connection.close()
