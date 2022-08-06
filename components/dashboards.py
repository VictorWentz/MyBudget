from turtle import width
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
                    html.H5('R$ 10000', id='p-receita-dashboard', style={})
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
                    html.H5('R$ 5000', id='p-despesa-dashboard', style={})
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
                        id='dropdown-despesas',
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

            ], style={'margin': '10px', 'height': '100%', 'padding': '20px'})

        ],width=4),

        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph-line-dash', style={'height': '100%', 'padding':'10px'})
            ])
        ], width=8),
    
    ], style={'margin': '10px'}),

    # Terceira Linha
    dbc.Row([
        dbc.Col([dcc.Graph(id='graph-time-dash', style={'padding':'10px'})], width=6),
        dbc.Col([dcc.Graph(id='graph-pie-dash-receita', style={'padding':'10px'})], width=3),
        dbc.Col([dcc.Graph(id='graph-pie-dash-despesa', style={'padding':'10px'})], width=3),
    ])

])



# =========  Callbacks  =========== #
