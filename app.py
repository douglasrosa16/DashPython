import plotly.express as px  # Ploty é uma biblioteca para criação de gráficos
# Dash é uma biblioteca para criar servidor Web
import dash
import dash_core_components as dcc  # Components do Core
import dash_html_components as html  # Elementos HTML
import dash_bootstrap_components as dbc
import pandas as pd  # Vai fazer a leitura do arquivo
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.datasets import load_boston
from sklearn.model_selection import cross_val_score
import io
import base64
from dash.dependencies import Input, Output  # Utilizar isso para utilizar a callback
# print(df.columns) - Imprimir as colunas do arquivo CSV

# Carregar os datasets
df_rec_desp = pd.read_csv('ExcelReceitasDespesasMes.csv')  # Dados de Receitas e Despesas
df_comissao_vend = pd.read_csv('ComissaoVendedor.csv')  # Dados de Comissao dos Vendedores
df_prods = pd.read_csv('ProdutosSafra.csv')  # Dados de Saida de Produtos por Safra
df_map_clientes = pd.read_csv('MapaClientes.csv')  # Dados de Localização dos Clientes
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")  # df online
df = pd.read_csv('MapaClientes.csv')
df_cli_pagador = pd.read_csv('cliente-pagador.csv')

# Comissão de Vendedores
df_comissao_vend.rename(columns={'valor': 'VALOR', 'vendedor': 'VENDEDOR'}, inplace=True)
fig_comissao_vend = px.bar(df_comissao_vend, y='VALOR', x='VENDEDOR', text='VALOR', title='Comissão de Vendedores')
fig_comissao_vend.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_comissao_vend.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# HISTOGRAMA - PRODUTOS POR SAFRA
df_prods.rename(columns={'safra': 'SAFRA'}, inplace=True)
fig_prods_safra = px.line(df_prods, x='SAFRA', y=df_prods.columns, labels={'x': 'SAFRA', 'y': 'TOTAL VENDA'},
                          title='Venda de Produtos por Safra')

# Arvore de Decisão
atributos = ['Contratado','Prazo','Pagador']
# valorContratado[1],prazo[2],classificacaoY[3]
# Critérios: Bom = valor baixo(1000) e varios dias (60)
# Critérios: Regular = valor medio e varios dias
# Critérios: Ruim = valor alto e poucos dias

X_arvore_dados=[[2024,2],[6292,39],[3414,54],[5260,60],[3058,12],[5385,47],[7236,43],[5932,28],[4573,23],[3385,40],
                [3520,46],[9469,57],[1100,11],[8560,52],[2732,11],[3014,25],[8647,0],[9280,20],[8388,48],[5967,19],
                [6250,38],[6647,44],[4096,20],[6641,52],[2235,18],[8529,57],[202,76],[7981,10],[9160,49],[817,76],
                [8791,47],[7752,38],[4670,23],[6655,60],[7128,50],[527,96],[215,72],[6525,19],[8260,36],[5932,26],
                [4804,32],[2885,55],[6356,30],[457,62],[7750,16],[3521,34],[4654,49],[577,116],[8971,17],[9377,26],
                [6916,20],[6308,6],[4027,41],[1390,24],[7861,32],[8186,11],[5659,21],[9671,54],[8103,51],[7801,26],
                [2249,58],[4616,4],[8246,28],[4105,14],[9837,35],[3082,12],[628,92],[8042,30],[9805,24],[1683,29],
                [2248,54],[371,66],[7703,26],[4310,2],[7946,36],[7765,52],[6931,11],[1883,50],[6995,12],[3826,6],
                [4573,1],[9939,52],[5445,52],[4023,22],[4779,26],[5174,29],[5408,54],[8377,27],[7711,56],[2557,14],
                [3738,25],[2384,40],[1155,31],[967,78]]
Y_arvore_classe = ['regular','ruim','regular','ruim','regular','ruim','ruim','ruim','ruim','regular','regular','ruim',
                   'regular','ruim','regular','regular','ruim','ruim','ruim','ruim','ruim','ruim','ruim','ruim','regular',
                   'ruim','bom','ruim','ruim','bom','ruim','ruim','ruim','ruim','ruim','bom','bom','ruim','ruim','ruim',
                   'ruim','regular','ruim','bom','ruim','regular','ruim','bom','ruim','ruim','ruim','ruim','ruim','regular',
                   'ruim','ruim','ruim','ruim','ruim','ruim','regular','ruim','ruim','ruim','ruim','regular','bom','ruim',
                   'ruim','regular','regular','bom','ruim','ruim','ruim','ruim','ruim','regular','ruim','regular','ruim',
                   'ruim','ruim','ruim','ruim','ruim','ruim','ruim','ruim','regular','regular','regular','regular','bom']

previsores = ['valorContratado','prazo']
# Arvore de Decisão
arvore_check_pagador = DecisionTreeClassifier(criterion='entropy')
# Treinamento
arvore_check_pagador.fit(X_arvore_dados, Y_arvore_classe)
figure, eixos = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
print(tree.plot_tree(arvore_check_pagador, feature_names=previsores, class_names=arvore_check_pagador.classes_, filled=True))

scores = cross_val_score(arvore_check_pagador, X_arvore_dados, Y_arvore_classe, cv=10)
# Irá retornar um array com 10 posições
scores.mean() # Media do score
plt.show()
app = dash.Dash()

app.layout = html.Div(
    [
        html.H1(
            'Dashboard BI - Financeiro'
        ),

        html.Br(),
        dcc.Dropdown(
            id='dd_receita_despesa',
            options=[
                {'label': 'Receitas', 'value': 'RECEITAS'},
                {'label': 'Despesas', 'value': 'DESPESAS'}
            ],
            value=['RECEITAS', 'DESPESAS'],
            placeholder='Selecione uma opção',
            multi=True
        ),
        dcc.Graph(
            id='fig_receita_despesa'
        ),
        html.Br(),
        dcc.Dropdown(
            id='dd_comissao_vend',
            options=[
                {'label': 'Todos', 'value': 'Todos'},
                {'label': 'Wellen', 'value': 'Wellen'},
                {'label': 'Douglas', 'value': 'Douglas'},
                {'label': 'Adao', 'value': 'Adao'},
                {'label': 'Janice', 'value': 'Janice'},
                {'label': 'Gabriel', 'value': 'Gabriel'}
            ],
            value='Todos',
            placeholder='Informe um Vendedor',
            multi=False
        ),
        dcc.Graph(
            id='fig_comissao_vendedores'
        ),
        html.Br(),
        dcc.Graph(figure=fig_prods_safra),
        html.Br(),
        dcc.Dropdown(
            id='dd_mapa_clientes',
            options=[
                {'label': 'Itiquira', 'value': 'Itiquira'},
                {'label': 'Rondonopolis', 'value': 'Rondonopolis'},
                {'label': 'Pedra Preta', 'value': 'Pedra Preta'},
                {'label': 'Juscimeira', 'value': 'Juscimeira'},
                {'label': 'Alto Garças', 'value': 'Alto Garças'},
                {'label': 'Itiquira', 'value': 'Itiquira'},
                {'label': 'Cuiaba', 'value': 'Cuiaba'},
                {'label': 'Caceres', 'value': 'Caceres'},
                {'label': 'Lucas do Rio Verde', 'value': 'Lucas do Rio Verde'},
                {'label': 'Sorriso', 'value': 'Sorriso'},
                {'label': 'Sinop', 'value': 'Sinop'},
                {'label': 'Brasnorte', 'value': 'Brasnorte'},
                {'label': 'Juina', 'value': 'Juina'},
                {'label': 'Castanheira', 'value': 'Castanheira'},
                {'label': 'Tangara da Serra', 'value': 'Tangara da Serra'},
                {'label': 'Sonora', 'value': 'Sonora'},
                {'label': 'Mineiros', 'value': 'Mineiros'},
                {'label': 'Todos', 'value': 'Todos'}
            ],
            value='Todos',  # Aqui poderia ser passado uma lista de cidades
            placeholder='Seleciona um Estado',
            multi=False
        ),
        dcc.Graph(
            id='fig_mapa_clientes'
        )
    ]
)


# Filtro de Receita e Despesas
@app.callback(
    Output(component_id='fig_receita_despesa', component_property='figure'),
    [Input(component_id='dd_receita_despesa', component_property='value')]
)
def graf_receita_desp(dd_receita_despesa):
    df_rec_desp.rename(columns={'data': 'PERIODO', 'receita': 'RECEITAS', 'despesa': 'DESPESAS'}, inplace=True)
    return px.line(df_rec_desp, x='PERIODO', y=dd_receita_despesa, title='Receitas e Despesas')


# Filtro de Localição de Clientes
@app.callback(
    Output(component_id='fig_mapa_clientes', component_property='figure'),
    [Input(component_id='dd_mapa_clientes', component_property='value')]
)
def graf_mapa_clientes(dd_mapa_clientes):
    dfc = df.filter(items=['Cidade', 'Estado', 'Populacao', 'Cliente', 'lat', 'lon'])
    if dd_mapa_clientes != 'Todos':
        # dfc = df_comissao_vend.filter(items=['VENDEDOR', 'VALOR', 'mes', 'produto'])
        dfc2 = dfc.loc[dfc.Cidade == dd_mapa_clientes]
    else:
        dfc2 = dfc
    #  dfc2 = df.loc[df['Cidade'].isin(dd_mapa_clientes)]  # Fazer assim para quando for uma lista de cidades
    fig_mapa_clientes = px.scatter_mapbox(dfc2, lat="lat", lon="lon", hover_name="Cidade",
                                          hover_data=["Estado", "Populacao", "Cliente"],
                                         color_discrete_sequence=["fuchsia"], zoom=5, height=500)
    fig_mapa_clientes.update_layout(mapbox_style="open-street-map")
    fig_mapa_clientes.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mapa_clientes.update_layout(title="Localização dos Clientes")
    return fig_mapa_clientes

# Filtro de Vendedores - Comissao
@app.callback(
    Output(component_id='fig_comissao_vendedores', component_property='figure'),
    [Input(component_id='dd_comissao_vend', component_property='value')]
)
def graf_mapa_vendedores(dd_comissao_vend):
    df_comissao_vend.rename(columns={'valor': 'VALOR', 'vendedor': 'VENDEDOR'}, inplace=True)
    dfc = df_comissao_vend.filter(items=['VENDEDOR', 'VALOR', 'mes', 'produto'])
    if dd_comissao_vend != 'Todos':
        # dfc = df_comissao_vend.filter(items=['VENDEDOR', 'VALOR', 'mes', 'produto'])
        dfc2 = dfc.loc[dfc.VENDEDOR == dd_comissao_vend]
    else:
        dfc2 = df_comissao_vend
    fig_comissao_vendedores = px.bar(dfc2, y='VALOR', x='VENDEDOR', text='VALOR', title='Comissão de Vendedores')
    fig_comissao_vendedores.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_comissao_vendedores.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig_comissao_vendedores

app.run_server(debug=True, use_reloader=True)
