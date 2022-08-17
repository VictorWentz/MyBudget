from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
# from globals import *
from app import app

card_icon = {
    'color': 'white',
    'textAlign': 'center',
    'fontSize': 30,
    'margin': 'auto'
}

graph_margin = dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
    # Primeira Linha
    dbc.Row([
        # Coluna Saldo Total
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo'),
                    html.H5('R$ 5000', id='p-saldo-dashboard', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card([
                    html.Div(className='fa fa-university', style=card_icon),
                ], color='warning', style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'})
            ])

        ], width=4),
        # Coluna Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Receita'),
                    html.H5('R$ 10000', id='p-receita-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card([
                    html.Div(className='fa fa-smile-o', style=card_icon),
                ], color='success', style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'})
            ])

        ], width=4),
        # Coluna Despesa
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Despesa'),
                    html.H5('R$ 5000', id='p-despesa-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card([
                    html.Div(className='fa fa-meh-o', style=card_icon),
                ], color='danger', style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'})
            ])

        ], width=4)
    ], style={'margin': '10px'}),
    
    # Segunda Linha
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Filtar Lançamentos', className='card-title'),
                html.Label('Categorias das Receitas'),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-receita',
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type='session',
                        multi=True
                    ),
                ),
                html.Label('Categorias das Despesas', style={'margin-top': '10px'}),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-despesa',
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type='session',
                        multi=True
                    ),
                ),
                html.Legend('Período da Análise', style={'margin-top': '10px'}),
                dcc.DatePickerRange(
                    month_format='Do MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime(2022,4,1).date(),
                    end_date=datetime.today() + timedelta(days=31),
                    updatemode='singledate',
                    id='date-picker-config',
                    style={'z-index': '100'}
                )

            ], style={'height': '100%', 'padding': '20px'})

        ],width=4),

        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph-line-dash', style={'height': '100%', 'padding':'10px'})
            ])
        ], width=8),
    
    ], style={'margin': '10px'}),

    # Terceira Linha
    dbc.Row([
        dbc.Col([dbc.Card(dcc.Graph(id='graph-time-dash', style={'padding':'10px'}))], width=6),
        dbc.Col([dbc.Card(dcc.Graph(id='graph-pie-dash-receita', style={'padding':'10px'}))], width=3),
        dbc.Col([dbc.Card(dcc.Graph(id='graph-pie-dash-despesa', style={'padding':'10px'}))], width=3),
    ])

])



# =========  Callbacks  =========== #
# RECEITA
@app.callback(
    [
        Output('dropdown-receita', 'options'),
        Output('dropdown-receita', 'value'),
        Output('p-receita-dashboards', 'children')
    ],
    Input('store-receitas', 'data')
)
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return ([{'label': x, 'value': x} for x in val], val, f'R$ {valor}')

# DESPESA
@app.callback(
    [
        Output('dropdown-despesa', 'options'),
        Output('dropdown-despesa', 'value'),
        Output('p-despesa-dashboards', 'children')
    ],
    Input('store-despesas', 'data')
)
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return ([{'label': x, 'value': x} for x in val], val, f'R$ {valor}')


# SALDO
@app.callback(
    Output('p-saldo-dashboard', 'children'),
    [
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data')
    ]
)
def saldo_total(despesas, receitas):
    df_despesa = pd.DataFrame(despesas)
    df_receita = pd.DataFrame(receitas)

    valor = df_receita['Valor'].sum() - df_despesa['Valor'].sum()

    return f'R$ {valor}'


# PRIMEIRA FIGURA
@app.callback(
    Output('graph-line-dash', 'figure'),
    [
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data'),
        Input('dropdown-despesa', 'value'),
        Input('dropdown-receita', 'value'),

    ]
)
def update_graph_line(data_despesa, data_receitas, cat_despesa, cat_receita):
    
    df_despesas = pd.DataFrame(data_despesa).set_index('Data')[['Valor']]
    df_receitas = pd.DataFrame(data_receitas).set_index('Data')[['Valor']]

    df_ds = df_despesas.groupby('Data').sum().rename(columns={'Valor': 'Despesas'})
    df_rc = df_receitas.groupby('Data').sum().rename(columns={'Valor': 'Receitas'})

    df_acum = df_ds.join(df_rc, how='outer').fillna(0)
    df_acum['Acumulo'] = df_acum['Receitas'] - df_acum['Despesas']
    df_acum['Acumulo'] = df_acum['Acumulo'].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Fluxo de Caixa', x = df_acum.index,
    y = df_acum['Acumulo'], mode='lines'))

    fig.update_layout(margin=graph_margin, height=400)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig
    
    