# Sane Aqui

**Sane Aqui** é um sistema web para coleta e análise de dados sobre saneamento básico. Ele permite que usuários preencham um formulário de pesquisa e visualizem estatísticas em tempo real sobre o acesso à rede de esgoto e água tratada em diferentes regiões do Brasil.

---

## Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Banco de Dados](#banco-de-dados)
- [Screenshots](#screenshots)
- [Licença](#licença)

---

## Funcionalidades

- Formulário para coleta de dados sobre saneamento básico (CPF, endereço, cidade, estado, número de moradores, acesso à rede de esgoto e água tratada).
- Validação de CPF e campos obrigatórios.
- Armazenamento dos dados em banco MySQL.
- Dashboard estatístico com:
  - Total de pesquisas realizadas
  - Média de moradores por residência
  - Percentual de acesso à rede de esgoto e água tratada
  - Gráficos por estado e cidades
  - Visualização de infraestrutura de saneamento

---

## Tecnologias Utilizadas

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) (interface web)
- [Pandas](https://pandas.pydata.org/) (análise de dados)
- [Plotly](https://plotly.com/python/) (gráficos)
- [validate-docbr](https://pypi.org/project/validate-docbr/) (validação de CPF)
- [MySQL](https://www.mysql.com/) (banco de dados relacional)

---

## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sane-aqui.git
cd sane-aqui
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados

- Instale e inicie o MySQL.
- Crie o banco e a tabela usando o script `src/mysql/init.sql`:

```bash
mysql -u root -p < src/mysql/init.sql
```

- Configure as variáveis de conexão no arquivo `database.py` (usuário, senha, host, banco).

### 4. Execute a aplicação

```bash
streamlit run src/app.py
```

Acesse [http://localhost:8501](http://localhost:8501) no navegador.

---

## Estrutura do Projeto

```plaintext
sane-aqui/
│
├── src/
│   ├── app.py           # Aplicação principal Streamlit
│   ├── database.py      # Classe de acesso ao banco de dados
│   └── mysql/
│       └── init.sql     # Script de criação do banco e tabela
├── requirements.txt     # Dependências Python
└── README.md            # Este arquivo
```

---

## Banco de Dados

O banco utiliza uma tabela `pesquisas` com os seguintes campos:

- `id` (UUID, chave primária)
- `cpf` (VARCHAR, obrigatório)
- `endereco` (VARCHAR, obrigatório)
- `bairro` (VARCHAR)
- `cidade` (VARCHAR, obrigatório)
- `estado` (CHAR(2), obrigatório)
- `moradores` (INT, obrigatório, 1-50)
- `rede_esgoto` (BOOLEAN)
- `agua_tratada` (BOOLEAN)
- `data_envio` (TIMESTAMP)

Veja o script completo em [`src/mysql/init.sql`](src/mysql/init.sql).

---

## Screenshots

### Formulário de Pesquisa

![Formulário de Pesquisa](img/formulario.png)

### Dashboard Estatístico

![Dashboard Estatístico](img/dashboard.png)

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvido por [Matheus Dias/Diogo Dias]**

Para dúvidas ou sugestões, abra uma issue no repositório.