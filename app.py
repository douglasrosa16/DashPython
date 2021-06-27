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

# Comissão de Vendedores
df_comissao_vend.rename(columns={'valor': 'VALOR', 'vendedor': 'VENDEDOR'}, inplace=True)
fig_comissao_vend = px.bar(df_comissao_vend, y='VALOR', x='VENDEDOR', text='VALOR', title='Comissão de Vendedores')
fig_comissao_vend.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_comissao_vend.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# HISTOGRAMA - PRODUTOS POR SAFRA
df_prods.rename(columns={'safra': 'SAFRA'}, inplace=True)
fig_prods_safra = px.line(df_prods, x='SAFRA', y=df_prods.columns, title='Venda de Produtos')

# Localização dos Clientes
fig_map_clientes = px.scatter_mapbox(df_map_clientes, lat="lat", lon="lon", hover_name="Cidade", hover_data=["Estado","Populacao","Cliente"],
                        color_discrete_sequence=["fuchsia"], zoom=5, height=500)
fig_map_clientes.update_layout(mapbox_style="open-street-map")
fig_map_clientes.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_map_clientes.update_layout(title="Localização dos Clientes")

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
        dcc.Graph(figure=fig_comissao_vend),
        html.Br(),
        dcc.Graph(figure=fig_prods_safra),
        html.Br(),
        dcc.Graph(figure=fig_map_clientes),
        html.Br(),
        dcc.Dropdown(
            id='dd_mapa_clientes',
            options=[
                {'label': 'Itiquira', 'value': 'Itiquira'}
            ],
            value=['Itiquira'],
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


# Filtro de Clientes
@app.callback(
    Output(component_id='fig_mapa_clientes', component_property='figure'),
    [Input(component_id='dd_mapa_clientes', component_property='value')]
)
def graf_mapa_clientes(dd_mapa_clientes):
    df_mapa_clientes = df_map_clientes.where('Cidade' == 'Itiquira')
    fig_mapa_clientes = px.scatter_mapbox(df_mapa_clientes, lat="lat", lon="lon", hover_name="Cidade",
                                         hover_data=["Estado", "Populacao", "Cliente"],
                                         color_discrete_sequence=["fuchsia"], zoom=5, height=500)
    # fig_mapa_clientes.update_layout(mapbox_style="open-street-map")
    # fig_mapa_clientes.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig_mapa_clientes.update_layout(title="Localização dos Clientes")
    return fig_mapa_clientes


app.run_server(debug=True, use_reloader=True)

