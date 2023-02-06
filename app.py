import base64
import os
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from campos import campo_label, campo_text, deptos
from update_gspread import actualizar_valor
from datetime import datetime
from logo import logo_encoded

from Datos.db import add_row_db


enviar = False


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width = device-width, initial-scale = 1.0, maximun-scale = 1.2, minimun-scale = 0.5'}]
                )
app.title = 'Calculadora de alimento'
server = app.server
port = int(os.environ.get("PORT", 5000))

app.layout = html.Div([
    dbc.Container([
        dcc.ConfirmDialog(
            id='confirm',
            message='¿Enviar Información Ingresada?'),
        html.Br(),
        dbc.Row([
            html.Center([
            dbc.Col(
                [
                    html.Img(src='data:image/png;base64,{}'.format(logo_encoded.decode()),
                             style={'max-width': '90%', 'height': 'auto'})

                ], xl=12, lg=12, md=12, sm=12, xs=12,
            )]),
            html.Center([
            dbc.Col([
                html.H4('Calculadora comparativa costo por nutriente')],
                xl=12, lg=12, md=12, sm=12, xs=12,
                #width = {'size': 8, 'offset': 0, 'order': 2},
                style={'padding-left': '8px', 'padding-top': '20px'}
            ),])
        ], justify='center', no_gutters=True),
        html.Hr(),

        dbc.Row([
            campo_label(id_='nombre', label='Nombre:', plh='Cliente',
                        tipo='text', ayuda='Ingrese el nombre y apellido del cliente'),

            campo_label(id_='contacto', label='Contacto:', plh='Telefono',
                        tipo='number', ayuda='Ingrese el contacto del cliente')
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_label(id_ = 'pais', label = 'Pais', tipo = 'seleccion',
                        ayuda = '-', valor = [{'label':i, 'value':i} for i in ['Colombia', 'Panamá', 'Ecuador']]),
            dbc.Col([], xl = 4, lg = 4, md = 4, sm = 5, xs = 5, 
                    style = {'padding-top': '5px', 'padding-left': '10px'})
        ], no_gutters = True, justify = 'center'),

        dbc.Row([
            campo_label(id_='departamento', label='Departamento:',
                        tipo='seleccion', valor = [{'label': '-', 'value': '-'}],
                        ayuda='Departamento del cliente'),

            campo_label(id_='municipio', label='Municipio:',
                        tipo='seleccion', valor=[{'label': '-', 'value': '-'}],
                        ayuda='Municipio del cliente')
        ], no_gutters=True, justify='center'),


        html.Br(),
        dbc.Row([
            campo_text(valor='Información', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor='Alimento 1', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor='Alimento 2', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_text(valor='Nombre', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='alm_1', plh='Alimento 1', tipo='text',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='alm_2', plh='Alimento 2', tipo='text',
                       xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),
        dbc.Row([
            campo_text(valor='Precio por Kg', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='precio_1', plh='$', tipo='number',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='precio_2', plh='$', tipo='number',
                       xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_text(valor='Materia Seca (%)', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='mat_sec_alm_1', plh='%', tipo='number',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='mat_sec_alm_2', plh='%', tipo='number',
                       xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_text(valor='Proteina (%)', tipo='readonly', fontsize='16px',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='proteina_alm_1', plh='%', tipo='number',
                       xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(id_='proteina_alm_2', plh='%', tipo='number',
                       xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            dbc.Col([
                dbc.Button('Calcular', color='success',
                           id='enviar', block=True),
            ],
                xl=3, lg=4, md=4, sm=5, xs=5,
                style={'padding-top': '8px'}),
            html.Br()
        ], no_gutters=True, justify='center'),

        html.Br(),

        # dbc.Row([
        #     dbc.Col([
        #         dbc.Spinner(
        #             dbc.Alert(id='salida_info', duration=3000, is_open=False, color = 'warning')),
        #     ], xl=4, lg=6, md=6, sm=10, xs=10,
        #         style={'padding-top': '10px'})
        # ]),


        html.Div(id='screen', children=[]),

        dbc.Row([
            dbc.Col([
                dbc.Spinner(
                    dbc.Alert(id='salida', duration=4000, is_open=False)),
            ], xl=4, lg=6, md=6, sm=10, xs=10,
                style={'padding-top': '10px'})
        ], no_gutters=True)
    ])
])


@app.callback([Output('confirm', 'displayed')],
              [Input('enviar', 'n_clicks')])
def display_confirm(value):
    if value:
        enviar = True
        return [True]
    else:
        enviar = False
        return [False]

# callback etiquetas Pais
@app.callback([Output('departamento_label', 'children'),
               Output('municipio_label', 'children')],
               Input('pais', 'value'))
def labels(pais):
    if pais is None:
        raise dash.exceptions.PreventUpdate()
    if pais == 'Colombia':
        return ['Departamento:', 'Municipio:']
    if pais == 'Panamá':
        return ['Provincia:', 'Distrito:']
    if pais == 'Ecuador':
        return ['Provincia:', 'Canton:']

# placeholder Pais
@app.callback([Output('precio_1', 'placeholder'),
               Output('precio_2', 'placeholder')],
               Input('pais', 'value'))
def placeholder(pais):
    if pais is None:
        raise dash.exceptions.PreventUpdate()
    if pais == 'Colombia':
        return ['$ COP', '$ COP']
    else:
        return ['$ USD', '$ USD']
# callback Departamento
@app.callback(Output('departamento', 'options'),
              Input('pais', 'value'))
def depto(pais):
    if pais is None:
        raise dash.exceptions.PreventUpdate()
    return [{'label': i, 'value': i} for i in deptos(pais = pais)]

# callback seleccion Municipio
@app.callback(Output('municipio', 'options'),
              Input('departamento', 'value'),
              State('pais', 'value'))
def munic(value, pais):
    if pais is None or value is None or value == '-':
        raise dash.exceptions.PreventUpdate()
    return [{'label': i, 'value': i} for i in deptos(depto=False, departamento=str(value), pais = pais)]


@app.callback(Output('nombre_ayuda', 'children'),
              Input('nombre', 'value'))
def nombre(value):
    if value is None or value == '' or len(value.split()) < 2:
        return 'Ingrese el nombre y apellido del cliente'
    else:
        return ''


@app.callback(Output('contacto_ayuda', 'children'),
              Input('contacto', 'value'))
def contacto(value):
    if value == None or value == '' or len(str(value)) < 7:
        return 'Ingrese el contacto del cliente'
    else:
        return ''


@app.callback(Output('departamento_ayuda', 'children'),
              [Input('pais', 'value'),
               Input('departamento', 'value')])
def depto(pais, value):
    if value == None or value == '-':
        if pais == 'Colombia' or pais is None:
            return 'Departamento del cliente'
        else:
            return 'Provincia del cliente'
    else:
        return ''


@app.callback(Output('municipio_ayuda', 'children'),
              [Input('pais', 'value'),
               Input('municipio', 'value')])
def muni(pais, value):
    if value == None or value == '-':
        if pais == 'Colombia' or pais is None:
            return 'Municipio del cliente'
        if pais == 'Panamá':
            return 'Distrito del cliente'
        if pais == 'Ecuador':
            return 'Canton del cliente'
    else:
        return ''


# ids = ['nombre', 'contacto', 'departamento', 'municipio', 'alm_1', 'alm_2', 'precio_1',
#        'precio_2', 'mat_sec_alm_1', 'mat_sec_alm_2', 'proteina_alm_1', 'proteina_alm_2']

ids = ['nombre', 'contacto', 'pais', 'departamento', 'municipio', 'alm_1', 'alm_2', 'precio_1',
       'precio_2', 'mat_sec_alm_1', 'mat_sec_alm_2', 'proteina_alm_1', 'proteina_alm_2']


@app.callback([Output('screen', 'children'),
               Output('salida', 'children'),
               Output('salida', 'is_open'),
               Output('salida', 'color')],
              Input('confirm', 'submit_n_clicks'),
              [State(i, 'value') for i in ids])
def load(n, nombre, contacto, pais, depto, munic, alm_1, alm_2, precio_1, precio_2,
         mat_sec_1, mat_sec_2, prot_1, prot_2):
    if n is None:
        raise dash.exceptions.PreventUpdate()
    # print(f'{nombre}, {contacto}, {depto}, {munic}, {alm_1}, {alm_2}, {precio_1}, {precio_2}, {mat_sec_1}, {mat_sec_2}, {prot_1}, {prot_2}')

    if nombre is None or nombre == '' or len(nombre.split()) < 2:
        return ['', 'Nombre no valido', True, 'danger']
    if contacto is None or contacto == '' or len(str(contacto)) < 7:
        return ['', 'Contacto no valido', True, 'danger']
    if pais is None:
        return ['', 'Pais no valido', True, 'danger']
    if depto is None:
        return ['', 'Departamento no valido', True, 'danger']
    if munic is None:
        return ['', 'Municipio no valido', True, 'danger']
    if alm_1 is None or alm_1 == '':
        return ['', 'Nombre alimento 1 no valido', True, 'danger']
    if alm_2 is None or alm_2 == '':
        return ['', 'Nombre alimento 2 no valido', True, 'danger']
    if isinstance(precio_1, str) or precio_1 is None or precio_1 < 0:
        return ['', 'Precio alimento 1 no valido', True, 'danger']
    if isinstance(precio_2, str) or precio_2 is None or precio_2 < 0:
        return ['', 'Precio alimento 2 no valido', True, 'danger']
    if isinstance(mat_sec_1, str) or mat_sec_1 is None or mat_sec_1 < 0 or mat_sec_1 > 100:
        return ['', '% materia seca alimento 1 no valida', True, 'danger']
    if isinstance(mat_sec_2, str) or mat_sec_2 is None or mat_sec_2 < 0 or mat_sec_2 > 100:
        return ['', '% materia seca alimento 2 no valida', True, 'danger']
    if isinstance(prot_1, str) or prot_1 is None or prot_1 < 0 or prot_1 > 100:
        return ['', '% proteina alimento 1 no valida', True, 'danger']
    if isinstance(prot_2, str) or prot_2 is None or prot_2 < 0 or prot_2 > 100:
        return ['', '% proteina alimento 2 no valida', True, 'danger']
    valor_kg_mt_sec_1 = round(precio_1/(mat_sec_1/100))
    valor_kg_prot_1 = round(valor_kg_mt_sec_1/(prot_1/100))
    valor_kg_mt_sec_2 = round(precio_2/(mat_sec_2/100))
    valor_kg_prot_2 = round(valor_kg_mt_sec_2/(prot_2/100))
    dif_costo_mat_sec = round(
        100*((valor_kg_mt_sec_2/valor_kg_mt_sec_1) - 1), 2)
    dif_costo_prot = round(100*((valor_kg_prot_2/valor_kg_prot_1) - 1), 2)
    db = {
        'Fecha': datetime.now().date().strftime('%Y/%m/%d'),
        'Nombre': nombre,
        'Contacto': contacto,
        'Pais': pais,
        'Departamento': depto,
        'Municipio': munic,
        'Alimento 1': alm_1,
        'Precio (kg) 1': precio_1,
        'Materia seca % 1': mat_sec_1,
        'Proteina % 1': prot_1,
        'Valor kg materia seca 1': valor_kg_mt_sec_1,
        'Valor kg proteina 1': valor_kg_prot_1,
        'Alimento 2': alm_2,
        'Precio (kg) 2': precio_2,
        'Materia seca % 2': mat_sec_2,
        'Proteina seca % 2': prot_2,
        'Valor kg materia seca 2': valor_kg_mt_sec_2,
        'Valor kg proteina 2': valor_kg_prot_2,
        'Diferencia costo materia seca %': dif_costo_mat_sec,
        'Diferencia costo proteina %': dif_costo_prot,
    }
    
    for i,j in db.items():
        db[i] = str(j)

    campo = html.Div(children=[
        dbc.Row([
            campo_text(valor='Comparación económico-nutricional', tipo='readonly',
                       fontsize='16px', xl=10, lg=10, md=10, sm=10, xs=10)
        ], style={'padding-top': '5px'}, justify='center'),

        dbc.Row([
            campo_text(valor='Valor kg materia seca', tipo='readonly',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor=f'${valor_kg_mt_sec_1}', tipo='read',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor=f'${valor_kg_mt_sec_2}', tipo='read',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_text(valor='Valor kg proteina', tipo='readonly',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor=f'$ {valor_kg_prot_1}', tipo='read',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor=f'$ {valor_kg_prot_2}', tipo='read',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_text(valor='Diferencia costo materia seca', tipo='readonly',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor=f'% {dif_costo_mat_sec}', tipo='read',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center'),

        dbc.Row([
            campo_text(valor='Diferencia costo proteina', tipo='readonly',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4),
            campo_text(valor=f'% {dif_costo_prot}', tipo='read',
                       fontsize='16px', xl=3, lg=3, md=4, sm=4, xs=4)
        ], no_gutters=True, justify='center')
    ])
    try:
        add_row_db(tabla = 'comparacion_economico_nutricional', data = db)
        #actualizar_valor('Calculadora-Alimentos', db)
        return [[campo], 'Información enviada con éxito', True, 'success']
    except Exeption as E:
        print(E)
        return ['', 'Información no enviada', True, 'danger']

    return ['', 'Error no documentado', True, 'danger']


if __name__ == '__main__':
    app.server.run(debug=True,
                   host='0.0.0.0',
                   port=port)
