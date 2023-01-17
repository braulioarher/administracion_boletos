import json

from flask import Flask
import pytest

from app import create_app
from models import EventModel, TicketModel
from datetime import datetime, timedelta


@pytest.fixture(autouse=True)
def app():
    app = create_app()
    app.config.update({
        'TESTING' : True
    })
    client = app.test_client()

    yield app
    

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

# ---- Pruebas a /events ----
def test_eventos_vacio(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    response = client.get(url)
    ans = response.get_data(as_text=True).strip()
    check_ans = '[]'
    assert ans == check_ans
    assert response.status_code == 200

def test_agregar_evento(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Queen", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 5}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['name'] == 'Queen'
    assert response.status_code == 201

def test_agregar_evento_en_fecha_pasada(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() - timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "AC/DC", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 5}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['message'] == 'La fecha del evento no puede ser menor a la de hoy'
    assert response.status_code == 403

def test_agregar_evento_en_fecha_inicio_mayor(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "AC/DC", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 5}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['message'] == 'La fecha de inicio del evento no puede ser mayor a la del final'
    assert response.status_code == 403

def test_agregar_evento_con_boletos_fuera_de_rango(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "AC/DC", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 301}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict["message"] == "El rango de boletos a crear debe ser entre 1 y 300"
    assert response.status_code == 403

    url1 = "/events"
    headers1 = {'Content-Type': "application/json"}
    start_date1 = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date1 = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload1 = f'{{"name": "AC/DC", "start_date": "{start_date1}", "end_date": "{end_date1}", "tickets_num": 0}}'
    response1 = client.post(url1, headers=headers1, data=payload1)
    ans1 = response1.get_data(as_text=True).strip()
    ans_dict1 = json.loads(ans1)
    assert ans_dict1["message"] == "El rango de boletos a crear debe ser entre 1 y 300"
    assert response.status_code == 403

def test_agregar_evento_existente(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=3), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Queen", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 5}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict["message"] == "Un error ocurrio al insertar el evento"
    assert response.status_code == 500

# ---- Pruebas a /event/<event_id> ----
def test_detalles_del_evento(client):
    url1 = "/event/1"
    headers = {'Content-Type': "application/json"}
    response = client.get(url1, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['name'] == 'Queen'
    assert response.status_code == 200

def test_update_event(client):
    url = "/event/1"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Cream", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 10}}'
    response = client.put(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['name'] == 'Cream'
    assert response.status_code == 200

    url1 = "/event/1"
    headers1 = {'Content-Type': "application/json"}
    response1 = client.get(url1, headers=headers1)
    ans1 = response1.get_data(as_text=True).strip()
    ans_dict1 = json.loads(ans1)
    assert ans_dict1["boletos_totales"] == 10

def test_update_event_con_fechas_incoherentes(client):
    url = "/event/1"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() - timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Cream", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 10}}'
    response = client.put(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['message'] == 'La fecha del evento no puede ser menor a la de actual'
    assert response.status_code == 403

    url1 = "/event/1"
    headers1 = {'Content-Type': "application/json"}
    start_date1 = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    end_date1 = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    payload1 = f'{{"name": "Cream", "start_date": "{start_date1}", "end_date": "{end_date1}", "tickets_num": 10}}'
    response1 = client.put(url1, headers=headers1, data=payload1)
    ans1 = response1.get_data(as_text=True).strip()
    ans_dict1 = json.loads(ans1)
    assert ans_dict1['message'] == 'La fecha de inicio del evento no puede ser mayor a la del final'
    assert response1.status_code == 403

# ---- Pruebas a /ticket/sell/<ticket_id> ----
def test_vender_boleto(client):
    url = "/ticket/sell/10"
    headers = {'Content-Type': "application/json"}
    response = client.put(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert response.status_code == 201
    assert ans_dict["is_sold"] == True
    

    # Caso si el boleto fue vendido
    url = "/ticket/sell/10"
    headers = {'Content-Type': "application/json"}
    response = client.put(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert response.status_code == 403
    assert ans_dict["message"] == "Este boleto ya ha sido vendido"

    url1 = "/ticket/sell/11"
    headers1 = {'Content-Type': "application/json"}
    response1 = client.put(url1, headers=headers1)
    ans1 = response1.get_data(as_text=True).strip()
    ans_dict1 = json.loads(ans1)
    assert response1.status_code == 201
    assert ans_dict1["is_sold"] == True


# ---- Pruebas a /event/<event_id> despues de vender boletos----
def test_delete_evento(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Muse", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 5}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['name'] == 'Muse'
    assert response.status_code == 201

    # Delete event
    url1 = "/event/2"
    headers1 = {'Content-Type': "application/json"}
    response1 = client.delete(url1, headers=headers1)
    ans1 = response1.get_data(as_text=True).strip()
    assert ans1 == '{"message":"Evento borrado"}'
    assert response.status_code == 201

def test_delete_evento_con_boletos_vendido(client):
    url = "/event/1"
    headers = {'Content-Type': "application/json"}
    response = client.delete(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert response.status_code == 403
    assert ans_dict['message'] == 'Error, no puedes borrar evento ya que tiene boletos vendidos'


# ---- Prueba a /ticket/redeem/<ticket_id> ----
def test_canjear_boleto(client):
    url = "/ticket/redeem/10"
    headers = {'Content-Type': "application/json"}
    response = client.put(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict["code"] == 403