import os
from turtle import back
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd






# ========= Layout ========= #
layout = dbc.Col([
    # HEAD
    html.H1('MyBudget', className='text-primary'),
    html.P('By: Victor Wentz', className='text-info'),
    html.Hr(),
    # PERFIL
    dbc.Button(id='button-avatar', 
        children=[html.Img(src='/assets/img_hom.png', id = 'avatar-change', alt='Avatar', className='perfil_avatar')],
        style={'background-color': 'transparent', 'border-color': 'transparent'}) ,

    # BOTÕES RECEITA E DESPESA
    dbc.Row([
        dbc.Col([
            dbc.Button(id='button-receita', color='success',
            children=['+ Receitas'])
        ],width=6),

        dbc.Col([dbc.Button(id='button-despesa', color='danger',
            children=['- Despesa'])],width=6),
    ]),
    # NAVEGAÇÃO
    html.Hr(),
    dbc.Nav([
        dbc.NavLink('Dashboard', href='/dashboards', active='exact'),
        dbc.NavLink('Extratos', href='/extratos', active='exact'),
    ], vertical=True, pills=True, id='nav-button', style={'margin-botton': '50px'}),

    # Modal Receita
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Receitas')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição:'),
                    dbc.Input(placeholder='Ex.: dividendos, herença ...', id='txt-receita')
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor:'),
                    dbc.Input(placeholder='R$100.00', id='valor-receita')
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(id='date-receita',
                    min_date_allowed=date(2020,1,1),
                    max_date_allowed=date(2030,12,31),
                    date=datetime.today(),
                    style={'width': '100%'}),    
                ], width=4),
                dbc.Col([
                    dbc.Label('Extras'),
                    dbc.Checklist(id = 'switches-input-receita',
                    options=[], value=[], switch=True)
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da Receita'),
                    dbc.Select(id='select-receita', options=[], value=[])
                ], width=4)
                
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Adicionar Categoria', style={'color': 'green'}),
                                dbc.Input(type='text', placeholder='Nova Categoria...', id='input-add-category', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success', id='add-category-receita', style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(id='category-div-add-receita', style={})
                            ], width=6),
                            dbc.Col([
                                html.Legend('Excluir Categoria', style={'color': 'red'}),
                                dbc.Checklist(id='checklist-selected-receita',
                                options=[], value=[], label_checked_style={'color': 'red'}, input_checked_style={'background': 'blue', 'borderColor': 'orange'}),
                                dbc.Button('Remover', color='warning', id='remove-category-receita', style={'margin-top': '20px'})
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion-receita'),
                html.Div(id='id-teste-receita', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar Receita', id='salvar-receita', color='success'),
                    dbc.Popover(dbc.PopoverBody('Receita Salva'), target='salvar-receita', placement='left', trigger='click'),
                ])
            ], style={'margin-top': '25px'})
        ]),
    ], id = 'modal-nova-receita', size='lg', is_open=False, centered=True, backdrop=True, style={'background-color': 'rgba(17,140,79,0.05)'}),

     # Modal Despesa
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Receitas')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição:'),
                    dbc.Input(placeholder='Ex.: gasolina, shop...', id='txt-despesa')
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor:'),
                    dbc.Input(placeholder='R$100.00', id='valor-despesa')
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(id='date-despesa',
                    min_date_allowed=date(2020,1,1),
                    max_date_allowed=date(2030,12,31),
                    date=datetime.today(),
                    style={'width': '100%'}),    
                ], width=4),
                dbc.Col([
                    dbc.Label('Extras'),
                    dbc.Checklist(id = 'switches-input-despesa',
                    options=[], value=[], switch=True)
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da despesa'),
                    dbc.Select(id='select-despesa', options=[], value=[])
                ], width=4)
                
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Adicionar Categoria', style={'color': 'green'}),
                                dbc.Input(type='text', placeholder='Nova Categoria...', id='input-add-despesa', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success', id='add-category-despesa', style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(id='category-div-add-despesa', style={})
                            ], width=6),
                            dbc.Col([
                                html.Legend('Excluir Categoria', style={'color': 'red'}),
                                dbc.Checklist(id='checklist-selected-despesa',
                                options=[], value=[], label_checked_style={'color': 'red'}, input_checked_style={'background': 'blue', 'borderColor': 'orange'}),
                                dbc.Button('Remover', color='warning', id='remove-category-despesa', style={'margin-top': '20px'})
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion-despesa'),
                html.Div(id='id-teste-despesa', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar despesa', id='salvar-despesa', color='success'),
                    dbc.Popover(dbc.PopoverBody('despesa Salva'), target='salvar-despesa', placement='left', trigger='click'),
                ])
            ], style={'margin-top': '25px'})
        ]),
    ], id = 'modal-nova-despesa', size='lg', is_open=False, centered=True, backdrop=True, style={'background-color': 'rgba(17,140,79,0.05)'}),

    # LOGOUT
    dbc.Button(id='logout-button', color='warning',
    children=['Logout'], style={'margin-top': '450px'})

 ], id='sidebar-complete')





# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output('modal-nova-receita', 'is_open'),
    Input('button-receita', 'n_clicks'),
    State('modal-nova-receita', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Pop-up Despesa
@app.callback(
    Output('modal-nova-despesa', 'is_open'),
    Input('button-despesa', 'n_clicks'),
    State('modal-nova-despesa', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open