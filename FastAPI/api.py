# Importar a biblioteca FastAPI
from fastapi import FastAPI
from manage_sql import MYSQL
from pydantic import BaseModel

# Criar uma instância do FastAPI
app = FastAPI()

# Criando as principais variáveis do banco de dados
db = MYSQL(
    host='localhost', #especifique o host em que está a rodar a conexão do banco
    user='', # preencha o user correcto
    password='', # preencha a senha correcta
    database='usuarios', # indique o nome do banco de dados da sua preferencia
    port=3306
)
nometabela = 'usuarios'
colunas = ['nome', 'username', 'email', 'senha']

# HOME - API
@app.get('/')
def home():
    return {'Bem vindo': 'CRUD COM FASTAPI'}

#READ
@app.get('/usuarios')
def usuarios():
    # Vai criar a tabeala se não existir
    db.criarTabela(
        nomeTabela=nometabela,
        Colunas=colunas,
        ColunasTipo=['varchar(255)','varchar(255)','varchar(255)','varchar(255)']
    )

    #Consultar os dados na tabela
    dados = db.verDados(
        nomeTabela=nometabela,
        colunas='id,nome,username,email,senha'
    )

    if len(dados) > 0:
        return {'usuarios': dados}
    
    else:
        return {'Messagem': 'Nenhum usuário encontrado'}

# CREATE
class Dados(BaseModel):
    nome: str
    username: str
    email: str
    senha: str

@app.post('/usuarios/inserir')
def inserir_usuario(dados: Dados):
    db.inserirDados(
        nomeTabela=nometabela,
        Colunas=colunas,
        dados=[dados.nome, dados.username, dados.email, db.encriptarValor(dados.senha)]
    )

    return {'Messagem': f'O usuário {dados.nome} foi inserido'}

# DELETE
@app.delete('/usuarios/apagar/{id}')
def apagar_usuario(id: int):
    dados = db.verDados(
        nomeTabela=nometabela,
        conditions=f'id = {id}',
        colunas='nome'
    )

    if len(dados) > 0:
        db.apagarDados(
            nomeTabela=nometabela,
            conditions=f'id = {id}'
        )

        return {'Messagem': f'Usuário {dados[0][0]} foi apagado com sucesso'}
    
    else:
        return {'Messagem': f'O usuário nº {id} não existe'}

# UPDATE - email
class Email(BaseModel):
    email: str

@app.put('/usuarios/editar_email/{id}')
def editar_usuario(id: int, email: Email):
    dados = db.verDados(
        nomeTabela=nometabela,
        conditions=f'id = {id}',
    )

    if len(dados) > 0:
        db.editarDados(
            nomeTabela=nometabela,
            conditions=f'id = {id}',
            colunas_valores={colunas[2]: email.email}
        )

        return {'Messagem': f'O email do usuario nº {id} for editado'}

    else:
        {'Messagem': f'O usuário nº {id} não existe'}

# UPDATE -senha
class Senha(BaseModel):
    senha: str

@app.put('/usuarios/editar_senha/{id}')
def editar_usuario(id: int, senha: Senha):
    dados = db.verDados(
        nomeTabela=nometabela,
        conditions=f'id = {id}',
    )

    if len(dados) > 0:
        db.editarDados(
            nomeTabela=nometabela,
            conditions=f'id = {id}',
            colunas_valores={colunas[3]: db.encriptarValor(senha.senha)}
        )

        return {'Messagem': f'A senha do usuario nº {id} for editado'}

    else:
        {'Messagem': f'O usuário nº {id} não existe'}