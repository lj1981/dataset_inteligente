import pandas as pd
import random
from datetime import datetime, timedelta
import requests

# Configurações gerais do dataset
n_linhas = 45000  # Definindo o número de linhas
ids = list(range(1,1 + n_linhas))


# Função para obter cidades e estados do Brasil via API do IBGE
def obter_cidades_e_estados():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url)
    if response.status_code == 200:
        municipios = response.json()
        cidades = [municipio['nome'] for municipio in municipios]
        estados = [municipio['microrregiao']['mesorregiao']['UF']['sigla'] for municipio in municipios]
        return cidades, estados
    else:
        print("Erro ao obter dados dos municípios.")
        return [], []


# Função para obter nomes aleatórios do IBGE
def obter_nomes():
    url = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking?localidade=br"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            dados = response.json()
            if isinstance(dados, list) and len(dados) > 0 and "res" in dados[0]:
                return [nome["nome"] for nome in dados[0]["res"]]
            else:
                print("Formato inesperado da resposta da API do IBGE.")
                return []
        except Exception as e:
            print(f"Erro ao processar JSON da API do IBGE: {e}")
            return []
    else:
        print("Erro ao obter nomes do IBGE.")
        return []


# Carregar cidades, estados e nomes
cidades_lista, estados_lista = obter_cidades_e_estados()
nomes_lista = obter_nomes()

# Geração de probabilidades dinâmicas
prob_genero = [random.randint(50, 70), 100 - random.randint(50, 70)]
prob_pagamento = [random.randint(30, 50), random.randint(20, 40), random.randint(10, 30), random.randint(5, 15)]
prob_avaliacao = [random.randint(20, 40), random.randint(30, 50), random.randint(10, 30), random.randint(5, 15),
                  random.randint(1, 10)]

# Geração de dados aleatórios
idades = [random.randint(18, 60) for _ in range(n_linhas)]
generos = random.choices(["Feminino", "Masculino"], weights=prob_genero, k=n_linhas)
cidades_selecionadas = random.choices(cidades_lista, k=n_linhas)
estados_selecionados = [estados_lista[cidades_lista.index(cidade)] for cidade in cidades_selecionadas]
nomes_clientes = [f"{random.choice(nomes_lista)} {random.choice(nomes_lista)}" for _ in range(n_linhas)]

# Lista de produtos e suas categorias
produtos_variados = {
    "Eletrônicos": ["Smartphone", "Notebook", "Tablet", "Fone de Ouvido", "Câmera Digital", "Smartwatch"],
    "Vestuário": ["Tênis", "Meia", "Camiseta", "Jaqueta", "Calça", "Boné", "Chinelo", "Vestido", "Blusa"],
    "Acessórios": ["Relógio", "Óculos", "Mochila", "Carteira", "Pulseira", "Colar", "Anel"],
    "Livros e Cultura": ["Livro de Ficção", "Livro de Não-Ficção", "Revista", "Quadrinho"],
    "Beleza e Saúde": ["Shampoo", "Condicionador", "Maquiagem", "Perfume", "Suplemento"],
    "Casa e Decoração": ["Sofá", "Mesa", "Luminária", "Cortina", "Tapete"],
    "Serviços": ["Assinatura", "Transporte", "Curso Online"],
    "Brinquedos": ["Boneca", "Carrinho", "Jogo de Tabuleiro", "Quebra-Cabeça"],
    "Eletrodomésticos": ["Liquidificador", "Micro-ondas", "Aspirador de Pó", "Máquina de Café"]
}

avaliacoes = ["Excelente", "Boa", "Neutra", "Ruim", "Péssimo"]
pagamentos = ["Pix", "Crédito", "Débito", "Dinheiro"]

# Expandir os dados
expanded_data = []
ticket_medio = {}

for i in range(n_linhas):
    cliente_id = ids[i]
    nome = nomes_clientes[i]
    idade = idades[i]
    genero = generos[i]
    cidade = cidades_selecionadas[i]
    estado = estados_selecionados[i]

    num_produtos = random.randint(1, 6)
    produtos_comprados = random.choices(list(produtos_variados.values()), k=num_produtos)
    valores = [round(random.uniform(10, 1000), 2) for _ in produtos_comprados]
    data_inicial = datetime(2023, 1, 1)
    datas_compras = [data_inicial + timedelta(days=random.randint(0, 365)) for _ in produtos_comprados]
    avaliacoes_aleatorias = random.choices(avaliacoes, weights=prob_avaliacao, k=len(produtos_comprados))
    pagamentos_aleatorios = random.choices(pagamentos, weights=prob_pagamento, k=len(produtos_comprados))

    ticket_medio[cliente_id] = sum(valores) / num_produtos

    for produto, valor, data_compra, avaliacao, pagamento in zip(produtos_comprados, valores, datas_compras,
                                                                 avaliacoes_aleatorias, pagamentos_aleatorios):
        expanded_data.append({
            "Nome": nome,
            "ID": cliente_id,
            "Idade": idade,
            "Gênero": genero,
            "Cidade": cidade,
            "Estado": estado,
            "Produto": produto,
            "Valor": f"R${valor:.2f}",
            "Data_Compra": data_compra.strftime("%Y-%m-%d"),
            "Avaliacao": avaliacao,
            "Pagamento": pagamento,
            "Ticket_Medio": f"R${ticket_medio[cliente_id]:.2f}"
        })

# Criar DataFrame e salvar CSV
df_expanded = pd.DataFrame(expanded_data)
file_path = "dataset_clientes_final.csv"
df_expanded.to_csv(file_path, index=False, encoding="utf-8")
print(f"Arquivo CSV salvo em: {file_path}")
