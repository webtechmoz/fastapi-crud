# FASTAPI - PYTHON

Aprenda a criar uma API com fastAPI e consumir com um crud basico feito em mysql e o client side feito usando a biblioteca flet.

## Instalação das bibliotecas necessárias
Para instalar as biblitoecas rode os domandos abaixo
```bash
pip install --upgrade manage-sql fastapi uvicorn flet httpx
```

## Clone do projecto
Pode clonar este projecto usando a tag abaixo
```bash
git clone https:/github.com/webtechmoz/fastapi.git
```

## Configurações da API
Edite  as conexões com o banco de dados no arquivo FastAPI/api.py
```python
db = MYSQL(
    host='nome_do_host',
    user='nome_do_user',
    password='pass_do_user',
    database='nome_do_banco',
    port=3306 #altere se for diferente
)

# Caso não tenha o mysql e queira usar o SQLITE, use a conexão abaixo
from manage_sql import SQLITE #para substituir o MYSQL

db = SQLITE(
    nomebanco='nome_do_banco'
)
```

## Rodar o servidor
Para rodar a api no servidor local use a tag abaixo
```bash
uvicorn api:app --reload
```

## Rodar o flet app
Para rodar o flet app use a tag abaixo
```bash
flet -r main.py
```
