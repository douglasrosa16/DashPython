import plotly.express as px
import pandas as pd

# df = recebe os dados que vem do pacote express e dados Iris
# Nesse caso o DataFrame recebe o Dataset de iris
df = pd.read_csv('VendasProdutos.csv')


# 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species', 'species_id'
# Aqui no PX pode ser passado parâmetros que vai influenciar no Gráfico
# Index(['idProduto', 'DescProduto', 'QuantidadeVendas', 'data'], dtype='object')
# Fazer agrupamento pelo nome do produto e somar as linhas das colunas

df_produto = df.groupby(['DescProduto']).sum()
print(df_produto.head())