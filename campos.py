import dash_bootstrap_components as dbc
import dash_html_components as html 
import pandas as pd

def deptos(depto = True, pais = '', departamento = ''):
    divipola = pd.read_csv('Datos/Divipola.csv')
    if depto:
        return (divipola.loc[divipola['Pais'] == pais, 'Departamento'].sort_values()).unique()
    else:
        return (divipola.loc[(divipola['Pais'] == pais) & (divipola['Departamento'] == departamento), 'Municipio'].sort_values()).unique()

def campo_label(id_, label = '', plh = '', tipo = '', ayuda = '', valor = '',
                xl = 4, lg = 4, md = 4, sm = 5, xs = 5,
                stl = {'padding-top': '5px', 'padding-left': '10px'}):
    if tipo == 'text' or tipo == 'number':
        text_input = dbc.Col([
            dbc.FormGroup([
                dbc.Label(id = id_+'_label', children = label),
                dbc.Input(id = id_, placeholder = plh, type = tipo,
                          debounce = True, value = valor),
                dbc.FormText(id = id_ + '_ayuda', children = ayuda)
            ])], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = stl)
        return text_input

    if tipo == 'text_ok' or tipo == 'number_ok':
        text_input = dbc.Col([
            dbc.FormGroup([
                dbc.Label(label),
                dbc.Input(id = id_, placeholder = plh, type = tipo,
                          debounce = True, value = valor),
                #dbc.FormText(ayuda)
            ])], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = stl)
        return text_input
    
    if tipo == 'seleccion':
        input = dbc.Col([
            dbc.FormGroup([
                dbc.Label(id = id_ + '_label', children = label),
                dbc.Select(id = id_, options = valor),
                dbc.FormText(id = id_ + '_ayuda', children = ayuda)
            ])
        ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
        style = stl)
        return input


def campo_text(id_ = '', plh = '', tipo = '', valor = '', style_ = {},
               xl = 4, lg = 2, md = 4, sm = 5, xs = 5, fontsize = '12px',
               stl = {'padding-top': '5px', 'padding-left': '10px'}):
    if tipo == 'text' or tipo == 'number':
        input = dbc.Col([
            dbc.Input(id = id_, type = tipo, placeholder = plh,
                      debounce = True, style = style_, value = valor)],
                xl = xl, lg = lg, md = md, sm = sm, xs = xs,
                style = stl)
        return input

    if tipo == 'readonly':
        output = dbc.Col([
                 html.P(valor, style = {'fontSize': fontsize,
                                        'text-align': 'center',
                                        #'border-style': 'solid',
                                        'border-radius': '3px',
                                        'border-color': 'silver',
                                        'border-width': '0.5px',
                                        'height': '35px',
                                        'padding-top': '8px'})
                                        ],
                 xl = xl, lg = lg, md = md, sm = sm, xs = xs,
                 style = stl)
        return output

    if tipo == 'read':
        output = dbc.Col([
                 html.P(valor, style = {'fontSize': fontsize,
                                        'text-align': 'center',
                                        'border-style': 'solid',
                                        'border-radius': '3px',
                                        'border-color': 'silver',
                                        'border-width': '0.5px',
                                        'height': '35px',
                                        'padding-top': '8px'})
                                        ],
                 xl = xl, lg = lg, md = md, sm = sm, xs = xs,
                 style = stl)
        return output