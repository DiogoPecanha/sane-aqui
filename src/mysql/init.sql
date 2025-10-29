USE pesquisa_db;

CREATE TABLE IF NOT EXISTS pesquisas (
    id CHAR(36) PRIMARY KEY,  -- UUID
    cpf VARCHAR(14) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    bairro VARCHAR(100),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    moradores INT NOT NULL CHECK (moradores >= 1 AND moradores <= 50),
    rede_esgoto BOOLEAN NOT NULL DEFAULT FALSE,
    agua_tratada BOOLEAN NOT NULL DEFAULT FALSE,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_cpf (cpf),
    INDEX idx_cidade (cidade),
    INDEX idx_estado (estado),
    INDEX idx_data_envio (data_envio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserir dados de exemplo (opcional)
INSERT INTO pesquisas (cpf, endereco, bairro, cidade, estado, moradores, rede_esgoto, agua_tratada) VALUES
('12345678901', 'Rua das Flores, 123', 'Centro', 'São Paulo', 'SP', 4, TRUE, TRUE),
('98765432109', 'Av. Brasil, 456', 'Jardim América', 'Rio de Janeiro', 'RJ', 3, TRUE, TRUE),
('11122233344', 'Rua da Paz, 789', 'Boa Vista', 'Recife', 'PE', 5, FALSE, TRUE),
('55566677788', 'Travessa do Sol, 321', 'Aldeota', 'Fortaleza', 'CE', 2, FALSE, FALSE),
('99988877766', 'Rua Amazonas, 654', 'Adrianópolis', 'Manaus', 'AM', 6, TRUE, FALSE);

-- Criar usuário adicional (se necessário)
-- CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin_password';
-- GRANT ALL PRIVILEGES ON pesquisa_db.* TO 'admin'@'%';
-- FLUSH PRIVILEGES;

-- Exibir tabelas criadas
SHOW TABLES;