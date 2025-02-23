# dataset_inteligente  ( Para ajudar nos estudo )

resumo do  código  é um script Python que gera um dataset fictício de clientes e suas compras, e então salva esses dados em um arquivo CSV. Vou detalhar cada parte do código para que você possa entender melhor o que está acontecendo.

1. Importações de Bibliotecas
python
Copy
import pandas as pd
import random
from datetime import datetime, timedelta
import requests
pandas: Biblioteca para manipulação de dados, especialmente útil para trabalhar com DataFrames.

random: Biblioteca para geração de números aleatórios.

datetime e timedelta: Bibliotecas para manipulação de datas e tempos.

requests: Biblioteca para fazer requisições HTTP, usada para obter dados de APIs.

2. Configurações Gerais do Dataset
python
Copy
n_linhas = 45000  # Definindo o número de linhas
ids = list(range(1,1 + n_linhas))
n_linhas: Define o número de linhas (ou registros) que o dataset terá.

ids: Cria uma lista de IDs únicos para cada cliente, começando de 1 até n_linhas.

3. Função para Obter Cidades e Estados do Brasil via API do IBGE
python
Copy
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
obter_cidades_e_estados: Esta função faz uma requisição à API do IBGE para obter uma lista de municípios e seus respectivos estados.

url: Endpoint da API do IBGE que retorna os municípios.

response: Faz a requisição GET à API.

municipios: Converte a resposta da API em um formato JSON.

cidades: Extrai os nomes das cidades.

estados: Extrai as siglas dos estados.

return: Retorna duas listas, uma com os nomes das cidades e outra com as siglas dos estados.

4. Função para Obter Nomes Aleatórios do IBGE
python
Copy
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
obter_nomes: Esta função faz uma requisição à API do IBGE para obter uma lista de nomes populares no Brasil.

url: Endpoint da API do IBGE que retorna os nomes mais comuns.

response: Faz a requisição GET à API.

dados: Converte a resposta da API em um formato JSON.

return: Retorna uma lista de nomes.

5. Carregar Cidades, Estados e Nomes
python
Copy
cidades_lista, estados_lista = obter_cidades_e_estados()
nomes_lista = obter_nomes()
cidades_lista: Lista de cidades obtidas da API do IBGE.

estados_lista: Lista de estados obtidos da API do IBGE.

nomes_lista: Lista de nomes obtidos da API do IBGE.

6. Geração de Dados Aleatórios
python
Copy
idades = [random.randint(18, 60) for _ in range(n_linhas)]
generos = random.choices(["Feminino", "Masculino"], weights=[60, 40], k=n_linhas)
cidades_selecionadas = random.choices(cidades_lista, k=n_linhas)
estados_selecionados = [estados_lista[cidades_lista.index(cidade)] for cidade in cidades_selecionadas]
nomes_clientes = [f"{random.choice(nomes_lista)} {random.choice(nomes_lista)}" for _ in range(n_linhas)]
idades: Gera uma lista de idades aleatórias entre 18 e 60 anos.

generos: Gera uma lista de gêneros, com uma probabilidade de 60% para "Feminino" e 40% para "Masculino".

cidades_selecionadas: Seleciona aleatoriamente cidades da lista de cidades.

estados_selecionados: Para cada cidade selecionada, obtém o estado correspondente.

nomes_clientes: Gera nomes completos combinando dois nomes aleatórios da lista de nomes.

7. Lista de Produtos e Suas Categorias
python
Copy
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
produtos_pesos = {"Eletrônicos": 20, "Vestuário": 30, "Acessórios": 15, "Livros e Cultura": 10, "Beleza e Saúde": 10,
                  "Casa e Decoração": 5, "Serviços": 5, "Brinquedos": 3, "Eletrodomésticos": 2}
produtos_variados: Um dicionário onde as chaves são categorias de produtos e os valores são listas de produtos.

produtos_pesos: Um dicionário que define a probabilidade de cada categoria ser escolhida.

8. Avaliações e Métodos de Pagamento
python
Copy
avaliacoes = ["Excelente", "Boa", "Neutra", "Ruim", "Péssimo"]
avaliacoes_pesos = [30, 40, 20, 7, 3]
pagamentos = ["Pix", "Crédito", "Débito", "Dinheiro"]
pagamentos_pesos = [40, 30, 20, 10]
avaliacoes: Lista de possíveis avaliações que um cliente pode dar.

avaliacoes_pesos: Probabilidades associadas a cada avaliação.

pagamentos: Lista de métodos de pagamento.

pagamentos_pesos: Probabilidades associadas a cada método de pagamento.

9. Expansão dos Dados
python
Copy
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
    categorias_escolhidas = random.choices(list(produtos_variados.keys()),
                                           weights=[produtos_pesos[cat] for cat in produtos_variados.keys()],
                                           k=num_produtos)
    produtos_comprados = [random.choice(produtos_variados[categoria]) for categoria in categorias_escolhidas]
    valores = [round(random.uniform(10, 1000), 2) for _ in produtos_comprados]
    data_inicial = datetime(2023, 1, 1)
    datas_compras = [data_inicial + timedelta(days=random.randint(0, 365)) for _ in produtos_comprados]
    avaliacoes_aleatorias = random.choices(avaliacoes, weights=avaliacoes_pesos, k=len(produtos_comprados))
    pagamentos_aleatorios = random.choices(pagamentos, weights=pagamentos_pesos, k=len(produtos_comprados))

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
expanded_data: Lista que armazenará todos os dados expandidos.

ticket_medio: Dicionário que armazenará o ticket médio (valor médio gasto) por cliente.

for i in range(n_linhas): Loop que itera sobre cada cliente.

cliente_id, nome, idade, genero, cidade, estado: Atributos do cliente.

num_produtos: Número aleatório de produtos comprados pelo cliente (entre 1 e 6).

categorias_escolhidas: Seleciona categorias de produtos com base nos pesos definidos.

produtos_comprados: Seleciona produtos aleatórios dentro das categorias escolhidas.

valores: Gera valores aleatórios para cada produto.

datas_compras: Gera datas aleatórias para as compras.

avaliacoes_aleatorias: Gera avaliações aleatórias para cada produto.

pagamentos_aleatorios: Gera métodos de pagamento aleatórios para cada produto.

ticket_medio[cliente_id]: Calcula o ticket médio para o cliente.

expanded_data.append: Adiciona os dados do cliente e suas compras à lista expanded_data.

10. Criação do DataFrame e Salvamento do CSV
python
Copy
df_expanded = pd.DataFrame(expanded_data)
file_path = "dataset_clientes_final.csv"
df_expanded.to_csv(file_path, index=False, encoding="utf-8")
print(f"Arquivo CSV salvo em: {file_path}")
df_expanded: Cria um DataFrame a partir da lista expanded_data.

file_path: Define o caminho e o nome do arquivo CSV.

df_expanded.to_csv: Salva o DataFrame em um arquivo CSV.

print: Informa ao usuário que o arquivo foi salvo.

Resumo
O código gera um dataset fictício de clientes e suas compras, utilizando dados reais de cidades, estados e nomes obtidos da API do IBGE. Ele cria um arquivo CSV com informações como nome do cliente, idade, gênero, cidade, estado, produtos comprados, valores, datas de compra, avaliações, métodos de pagamento e ticket médio. O dataset é gerado de forma aleatória, mas com base em probabilidades definidas para categorias de produtos, avaliações e métodos de pagamento.
