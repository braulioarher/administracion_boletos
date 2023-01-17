import pytest
from app import create_app
from flask import Flask
from models import EventModel, TicketModel
from datetime import datetime, timedelta
import json

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

# ---- Pruebas a /events/<event_id> ----
def test_detalles_del_evento(client):
    url = "/events"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Queen", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 5}}'
    response = client.post(url, headers=headers, data=payload)
    ans = response.get_data(as_text=True).strip()

    url1 = "/event/1"
    headers = {'Content-Type': "application/json"}
    response = client.get(url1, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict['name'] == 'Queen'

def test_update_event(client):
    url = "/event/1"
    headers = {'Content-Type': "application/json"}
    start_date = format(datetime.now() + timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    end_date = format(datetime.now() + timedelta(hours=2), '%Y-%m-%d %H:%M:%S')
    payload = f'{{"name": "Cream", "start_date": "{start_date}", "end_date": "{end_date}", "tickets_num": 8}}'
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
    assert ans_dict1["boletos_totales"] == 8

# ---- Pruebas a /ticket/<ticket_id> ----
def test_vender_boleto(client):
    url = "/ticket/sell/10"
    headers = {'Content-Type': "application/json"}
    response = client.put(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict["is_sold"] == True

    # Caso si el boleto fue vendido
    url = "/ticket/sell/10"
    headers = {'Content-Type': "application/json"}
    response = client.put(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict["message"] == "Este boleto ya ha sido vendido"

def test_canjear_boleto(client):
    url = "/ticket/redeem/10"
    headers = {'Content-Type': "application/json"}
    response = client.put(url, headers=headers)
    ans = response.get_data(as_text=True).strip()
    ans_dict = json.loads(ans)
    assert ans_dict["code"] == 500