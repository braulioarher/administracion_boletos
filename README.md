# Prueba de sistema de administracion de boletos para eventos

## Recursos de events

Dentro de los recurso de event tenemos dos rutas:

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

## Recursos de tickets

Dentro de los recurso de tickets tenemos dos rutas:

        - Ruta: /ticket/sell/<ticket_id>
                    De tipo POST:
                    (Require un argumento que es el ticket_id)
                        - Al usar este recurso la API evaluea que el evento no haya sido vendido y si es asi modifica el valor de is_sold en la base de datos
                        - Al vender un boleto la API regresa la informacion del boleto
        - Ruta /ticket/redeem/<ticket_id>
                    De tipo POST:
                    (Require un argumento que es el ticket_id)
                        - Al usar este recurso la API evalua los rangos de inicio y final del evento y que el boleto no haya sido canjeado en caso de que todo este en orden se actualiza en la base de datos y regresa los detalles del boleto
