import plotly.express as px  # Ploty é uma biblioteca para criação de gráficos
# Dash é uma biblioteca para criar servidor Web
import dash
import dash_core_components as dcc  # Components do Core
import dash_html_components as html  # Elementos HTML
import dash_bootstrap_components as dbc
import pandas as pd  # Vai fazer a leitura do arquivo

from dash.dependencies import Input, Output  # Utilizar isso para utilizar a callback
# print(df.columns) - Imprimir as colunas do arquivo CSV

df_rec_desp = pd.read_csv('ExcelReceitasDespesasMes.csv')  # Dados de Receitas e Despesas
df_comissao_vend = pd.read_csv('ComissaoVendedor.csv')  # Dados de Comissao dos Vendedores
df_prods = pd.read_csv('ProdutosSafra.csv')  # Dados de Saida de Produtos por Safra
df_map_clientes = pd.read_csv('MapaClientes.csv')  # Dados de Localização dos Clientes
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv") # Dataframe online
df = pd.read_csv('MapaClientes.csv')

# Comissão de Vendedores
df_comissao_vend.rename(columns={'valor': 'VALOR', 'vendedor': 'VENDEDOR'}, inplace=True)
fig_comissao_vend = px.bar(df_comissao_vend, y='VALOR', x='VENDEDOR', text='VALOR', title='Comissão de Vendedores')
fig_comissao_vend.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_comissao_vend.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# HISTOGRAMA - PRODUTOS POR SAFRA
df_prods.rename(columns={'safra': 'SAFRA'}, inplace=True)
fig_prods_safra = px.line(df_prods, x='SAFRA', y=df_prods.columns, labels={'x':'SAFRA', 'y': 'TOTAL VENDA'}, title='Venda de Produtos')


app = dash.Dash()
app.layout = html.Div(
    [
        dcc.Dropdown(
            id='dd_receita_despesa',
            options=[
                {'label': 'Receitas', 'value': 'RECEITAS'},
                {'label': 'Despesas', 'value': 'DESPESAS'}
            ],
            value=['RECEITAS','DESPESAS'],
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
        dcc.Graph(figure=fig_comissao_vend),
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
                {'label': 'Mineiros', 'value': 'Mineiros'}
            ],
            value='Rondonopolis', # Aqui poderia ser passado uma lista de cidades
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
    dfc2 = dfc.loc[dfc.Cidade == dd_mapa_clientes]
    #  dfc2 = df.loc[df['Cidade'].isin(dd_mapa_clientes)]  # Fazer assim para quando for uma lista de cidades
    fig_mapa_clientes = px.scatter_mapbox(dfc2, lat="lat", lon="lon", hover_name="Cidade",
                                         hover_data=["Estado", "Populacao", "Cliente"],
                                         color_discrete_sequence=["fuchsia"], zoom=5, height=500)
    fig_mapa_clientes.update_layout(mapbox_style="open-street-map")
    fig_mapa_clientes.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mapa_clientes.update_layout(title="Localização dos Clientes")
    return fig_mapa_clientes

#Filtro de Vendedores - Comissao
@app.callback(
    Output(component_id='fig_comissao_vendedores', component_property='figure'),
    [Input(component_id='dd_comissao_vend', component_property='value')]
)
def graf_mapa_vendedores(dd_comissao_vend):
    df_comissao_vend.rename(columns={'valor': 'VALOR', 'vendedor': 'VENDEDOR'}, inplace=True)
    dfc = df_comissao_vend.filter(items=['VENDEDOR', 'VALOR', 'mes', 'produto'])
    if(dd_comissao_vend != 'Todos'):
        # dfc = df_comissao_vend.filter(items=['VENDEDOR', 'VALOR', 'mes', 'produto'])
        dfc2 = dfc.loc[dfc.VENDEDOR == dd_comissao_vend]
    else:
        dfc2 = df_comissao_vend
    fig_comissao_vendedores = px.bar(dfc2, y='VALOR', x='VENDEDOR', text='VALOR', title='Comissão de Vendedores')
    fig_comissao_vendedores.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_comissao_vendedores.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig_comissao_vendedores

app.run_server(debug=True, use_reloader=True)

