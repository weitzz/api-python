CREATE DATABASE pharmadb;

CREATE TABLE IF NOT EXISTS `pharmadb`.`medicamentos` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(256),
    preco FLOAT,
    data_de_validade VARCHAR(256),
    imagem VARCHAR,
    estoque BOOLEAN,
    quantidade VARCHAR(256)
);