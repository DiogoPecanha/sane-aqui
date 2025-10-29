import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }
    
    def get_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            return conn
        except Error as e:
            print(f"Erro ao conectar: {e}")
            return None
    
    def create_table(self):
        """Cria tabela se não existir"""
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pesquisas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cpf VARCHAR(14) NOT NULL,
                    endereco VARCHAR(255) NOT NULL,
                    bairro VARCHAR(100),
                    cidade VARCHAR(100),
                    estado CHAR(2),
                    moradores INT,
                    rede_esgoto BOOLEAN,
                    agua_tratada BOOLEAN,
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_cidade (cidade),
                    INDEX idx_estado (estado)
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
    
    def insert_pesquisa(self, data):
        """Insere nova pesquisa"""
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO pesquisas 
                (cpf, endereco, bairro, cidade, estado, moradores, rede_esgoto, agua_tratada)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['cpf'], data['endereco'], data['bairro'],
                data['cidade'], data['estado'], data['moradores'],
                data['rede_esgoto'], data['agua_tratada']
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        return False
    
    def get_statistics(self):
        """Retorna estatísticas agregadas"""
        conn = self.get_connection()
        if conn:
            import pandas as pd
            
            # Total de registros
            total = pd.read_sql("SELECT COUNT(*) as total FROM pesquisas", conn)
            
            # Por estado
            por_estado = pd.read_sql("""
                SELECT estado, COUNT(*) as total 
                FROM pesquisas 
                GROUP BY estado 
                ORDER BY total DESC
            """, conn)
            
            # Por cidade (top 10)
            por_cidade = pd.read_sql("""
                SELECT cidade, COUNT(*) as total 
                FROM pesquisas 
                GROUP BY cidade 
                ORDER BY total DESC 
                LIMIT 10
            """, conn)
            
            # Infraestrutura
            infra = pd.read_sql("""
                SELECT 
                    SUM(rede_esgoto) as com_esgoto,
                    SUM(agua_tratada) as com_agua,
                    COUNT(*) as total
                FROM pesquisas
            """, conn)
            
            # Média de moradores
            moradores = pd.read_sql("""
                SELECT AVG(moradores) as media_moradores
                FROM pesquisas
            """, conn)
            
            conn.close()
            
            return {
                'total': total,
                'por_estado': por_estado,
                'por_cidade': por_cidade,
                'infra': infra,
                'moradores': moradores
            }
        return None
