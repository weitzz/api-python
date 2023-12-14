import pytest
from fastapi.testclient import TestClient
from sqlalchemy import true

from main import app

client = TestClient(app)


def test_post_medicamento():
    medicamento_data = {
        "nome": "cetoprofeno",
        "preco": 25.99,
        "data_de_validade": "10-05-2040",
        "estoque": True,
        "quantidade": "500"
    }
    files = {'imagem': ('test_image.jpg', open('medicamentos/images/test_image.jpg', 'rb'), 'image/jpeg')}







    response = client.post("/api/medicamentos", data=medicamento_data, files=files)

    assert response.status_code == 201
    assert response.json()["nome"] == medicamento_data["nome"]
    assert response.json()["preco"] == medicamento_data["preco"]


def test_get_medicamentos():
    response = client.get("/api/medicamentos")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_medicamento():
    response = client.get("/medicamentos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Medicamento Teste"


def test_put_medicamento():
    medicamento_id = 1
    medicamento_data = {
        "nome": "novo_nome",
        "preco": 30.99,
        "data_de_validade": "2023-08-20",
        "imagem": "nova_imagem3.png"
    }

    response = client.put(f"/api/medicamentos/{medicamento_id}", json=medicamento_data)

    assert response.status_code == 202
    assert response.json()["nome"] == medicamento_data["nome"]
    assert response.json()["preco"] == medicamento_data["preco"]


def test_delete_medicamento():
    medicamento_id = 1
    response = client.delete(f"/api/medicamentos/{medicamento_id}")

    assert response.status_code == 204


