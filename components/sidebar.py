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

from dados.data_creation import *






# ========= Layout ========= #
layout = dbc.Card([
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
                    dbc.Label("Opções Extras"),
                    dbc.Checklist(
                        options=[{'label': 'Foi recebida', 'value': 1},
                                {'label': 'Receita Recorrente', 'value': 2}],
                        value=[1],
                        id="switches-input-receita",
                        switch=True),
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da Receita'),
                    dbc.Select(id='select-receita',
                     options=[{'label': i , 'value': i} for i in cat_receita],
                    value=cat_receita[0
                    ])
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
                                options=[{'label': i, 'value':i} for i in cat_receita],
                                value=[],
                                label_checked_style={'color': 'red'}, 
                                input_checked_style={'background': 'blue', 'borderColor': 'orange'}),
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
                    dbc.Label("Opções Extras"),
                    dbc.Checklist(
                        options=[{'label': 'Foi recebida', 'value': 1},
                                {'label': 'Receita Recorrente', 'value': 2}],
                        value=[1],
                        id="switches-input-despesa",
                        switch=True)
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da despesa'),
                    dbc.Select(id='select-despesa',
                     options=[{'label': i, 'value': i} for i in cat_despesa], 
                     value=cat_despesa[0])
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
                                options=[{'label': i, 'value':i} for i in cat_despesa], 
                                value=[], 
                                label_checked_style={'color': 'red'}, 
                                input_checked_style={'background': 'blue', 'borderColor': 'orange'}),
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


# RECEITAS
@app.callback(
    Output('store-receitas', 'data'),
    Input('salvar-receita', 'n_clicks'),
    [
        State("txt-receita", "value"),
        State("valor-receita", "value"),
        State("date-receita", "date"),
        State("switches-input-receita", "value"),
        State("select-receita", "value"),
        State('store-receitas', 'data')

    ]
)
def save_form_recipe(n_clicks, description, value, date, switches, category, dict_recipe):

    df_receitas = pd.DataFrame(dict_recipe)

    # Faz o callback não ser executado na primeira vez que roda
    if n_clicks and not (value == '' or value is None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        cat = category[0] if type(category) == list else category
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        # Adiciona item
        df_receitas.loc[df_receitas.shape[0]] = [value, recebido, fixo, date, cat, description]
        df_receitas.to_csv('df_receitas.csv')

    data_return = df_receitas.to_dict()

    return data_return


# DESPESAS
@app.callback(
    Output('store-despesas', 'data'),
    Input('salvar-despesa', 'n_clicks'),
    [
        State("txt-despesa", "value"),
        State("valor-despesa", "value"),
        State("date-despesa", "date"),
        State("switches-input-despesa", "value"),
        State("select-despesa", "value"),
        State('store-despesas', 'data')

    ]
)
def save_form_despesa(n_clicks, description, value, date, switches, category, dict_despesa):

    df_despesa = pd.DataFrame(dict_despesa)

    # Faz o callback não ser executado na primeira vez que roda
    if n_clicks and not (value == '' or value is None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        cat = category[0] if type(category) == list else category
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        # Adiciona item
        df_despesa.loc[df_despesa.shape[0]] = [value, recebido, fixo, date, cat, description]
        df_despesa.to_csv('df_despesas.csv')

    data_return = df_despesa.to_dict()

    return data_return


# Add/Remove categoria despesa
@app.callback(
    [Output("category-div-add-despesa", "children"),
    Output("category-div-add-despesa", "style"),
    Output("select-despesa", "options"),
    Output('checklist-selected-despesa', 'options'),
    Output('checklist-selected-despesa', 'value'),
    Output('store-cat-despesas', 'data')],
    [Input("add-category-despesa", "n_clicks"),
    Input("remove-category-despesa", 'n_clicks')],
    [State("input-add-despesa", "value"),
    State('checklist-selected-despesa', 'value'),
    State('store-cat-despesas', 'data')]
)
def add_category(n, n2, txt, check_delete, data):
    cat_despesa = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {'color': 'red'}

        else:
            cat_despesa = cat_despesa + [txt] if txt not in cat_despesa else cat_despesa
            txt1 = f'A categoria {txt} foi adicionada com sucesso!'
            style1 = {'color': 'green'}
    
    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]  
    
    opt_despesa = [{"label": i, "value": i} for i in cat_despesa]
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    data_return = df_cat_despesa.to_dict()

    return [txt1, style1, opt_despesa, opt_despesa, [], data_return]


# Add/Remove categoria receita
@app.callback(
    [Output("category-div-add-receita", "children"),
    Output("category-div-add-receita", "style"),
    Output("select-receita", "options"),
    Output('checklist-selected-receita', 'options'),
    Output('checklist-selected-receita', 'value'),
    Output('store-cat-receitas', 'data')],
    [Input("add-category-receita", "n_clicks"),
    Input("remove-category-receita", 'n_clicks')],
    [State("input-add-category", "value"),
    State('checklist-selected-receita', 'value'),
    State('store-cat-receitas', 'data')]
)
def add_category(n, n2, txt, check_delete, data):
    cat_receita = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {'color': 'red'}

    if n and not(txt == "" or txt == None):
        cat_receita = cat_receita + [txt] if txt not in cat_receita else cat_receita
        txt1 = f'A categoria {txt} foi adicionada com sucesso!'
        style1 = {'color': 'green'}
    
    if n2:
        if check_delete == []:
            pass
        else:
            cat_receita = [i for i in cat_receita if i not in check_delete]  
    
    opt_receita = [{"label": i, "value": i} for i in cat_receita]
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receita.to_csv("df_cat_receita.csv")
    data_return = df_cat_receita.to_dict()

    return [txt1, style1, opt_receita, opt_receita, [], data_return]