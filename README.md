# Prueba Técnica
# Servicio de Gestión de Clientes

Este proyecto proporciona un servicio python(Lambda) para gestionar clientes. Incluye operaciones para crear, leer, actualizar y eliminar información de clientes.

## Esquema de la Base de Datos

El esquema de la base de datos está definido en el archivo `prueba_tecnica_bd.sql`.

## Endpoints de la API

### Crear Cliente

- **Endpoint:** `https://tw5h0n9tfj.execute-api.us-east-1.amazonaws.com/Prod/customer/`
- **Método:** `POST`
- **Cuerpo de la Solicitud:**
    ```json
    {
        "nombreCliente": {
            "nombre": "John",
            "apellido": "Doe"
        },
        "telefono": 1234567890,
        "edad": 30
    }
    ```
- **Respuesta:**
    - **Éxito:**
        ```json
        {
            "message": "Cliente creado exitosamente"
        }
        ```
    - **Error:**
        ```json
        {
            "message": "Mensaje de error"
        }
        ```

### Obtener Todos los Clientes

- **Endpoint:** `https://tw5h0n9tfj.execute-api.us-east-1.amazonaws.com/Prod/customer/get-all/`
- **Método:** `GET`
- **Respuesta:**
    - **Éxito:**
        ```json
        [
            {
                "id": 1,
                "nombre": "John",
                "apellido": "Doe",
                "telefono": 1234567890,
                "edad": 30
            },
            ...
        ]
        ```
    - **Error:**
        ```json
        {
            "message": "Mensaje de error"
        }
        ```

### Actualizar Cliente

- **Endpoint:** `https://tw5h0n9tfj.execute-api.us-east-1.amazonaws.com/Prod/customer/`
- **Método:** `PUT`
- **Cuerpo de la Solicitud:**
    ```json
    {
        "nombreCliente": {
            "nombre": "Jane",
            "apellido": "Doe"
        },
        "telefono": 1234567890,
        "edad": 29
    }
    ```
- **Respuesta:**
    - **Éxito:**
        ```json
        {
            "message": "Cliente actualizado exitosamente"
        }
        ```
    - **Error:**
        ```json
        {
            "message": "Mensaje de error"
        }
        ```

### Eliminar Cliente

- **Endpoint:** `https://tw5h0n9tfj.execute-api.us-east-1.amazonaws.com/Prod/customer/`
- **Método:** `DELETE`
- **Cuerpo de la Solicitud:**
    ```json
    {
        "telefono": 1234567890
    }
    ```
- **Respuesta:**
    - **Éxito:**
        ```json
        {
            "message": "Cliente eliminado correctamente"
        }
        ```
    - **Error:**
        ```json
        {
            "message": "Mensaje de error"
        }
        ```

