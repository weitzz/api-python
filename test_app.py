import pytest
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_medicamento():
    # Caso de teste para a rota de criação de medicamento
    data = {
        "id": 1,
        "nome": "Medicamento Teste",
        "preco": 10.0,
        "data_validade": "2023-12-31",
        "imagem": "imagem_teste.jpg"
    }
    response = client.post("/medicamento", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Medicamento inserido com sucesso"}

def test_get_medicamento():
    # Caso de teste para a rota de consulta de medicamento por ID
    response = client.get("/medicamentos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Medicamento Teste"

def test_update_medicamento():
    # Caso de teste para a rota de atualização de medicamento
    data = {
        "nome": "Medicamento Atualizado",
        "preco": 20.0,
        "data_validade": "2024-12-31",
        "imagem": "nova_imagem.jpg"
    }
    response = client.put("/medicamentos/1", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Medicamento atualizado com sucesso"}


