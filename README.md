# Prueba de sistema de administracion de boletos para eventos

## Recursos de events

Dentro de los recurso de event tenemos:

    - Ruta: /events :
                    POST 
                    (Crea un evento) requiere:
                        - name: string
                        - start_date: Date formato "YYYY-MM-DD HH-MM:SS"
                        - end_date: Date formato "YYYY-MM-DD HH-MM:SS"
                        - tickets_num : int
                    Se puede usar el siguiente JSON de referencia:
                        {
                            "name": "Queen",
                            "start_date": "2023-01-14 22:07:00",
                            "end_date": "2023-01-14 22:08:00",
                            "tickets_num": 100
                        }

                    GET
                    (Regresa todos los eventos):
                        Al usar este recurso la API regresara un JSON con toda la informacion almacenada en DB ejemplo:
                         [
                            {
                                "id": 1,
                                "name": "Queen",
                                "start_date": "2023-01-14T22:07:00",
                                "end_date": "2023-01-14T22:08:00",
                                "tickets": [
                                    {
                                        "is_redeemed": false,
                                        "is_sold": false,
                                        "id": 10
                                    },
                                    ...]
                         ]

        - Ruta: /event/<event_id>:
                    GET:
                    (Regresa solamenre el evento solicitado)
                        Al usar este recurso la API regresa detalles del evento como nombre, fechas, boletos vendidos y canjeados
                    DELETE:
                    (Elimina el boleto solicitado)
                    PUT:
                    (Modifica detalles del evento)
                        Al usar este metodo puedes modificar el nombre del evento, fechas y opcionalmente el numero de boletos
                        {
                            "name": "Queen",
                            "start_date": "2023-01-14 22:07:00",
                            "end_date": "2023-01-14 22:08:00",
                            "tickets_num": 15
                        }