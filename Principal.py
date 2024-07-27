import dash
from dash import html, dcc, callback, Output, Input, State
import re

app = dash.Dash(__name__, use_pages=True)



app.layout = html.Div([

    #-----------Logo boton-----
    html.Button(html.Img(src='assets/logo.png',
                         style={'width': '100%', 'height': '100%', 'background-color': 'white',
                                'border-radius': '50px'}),
                id='toggle-button', className='toggle-button', style={'margin': '10px'}),
    #-------------------------

    #-----------SlideBar para las opciones de pagina---------------
    html.Div([
    
        dcc.Link(f"{re.sub(r'[-|1]', " ", page['name'])}",
                     href=page["relative_path"],
                     className="letra-contenedor") for inx ,page in enumerate(dash.page_registry.values())
    ], className='sidebar', id='sidebar'),
    #------------------------------------


    #---------Contenedor de las paginas
    html.Div([
        dash.page_container
    ], className='content-pages', id="id_content"),
    #----------------------------------

], className='content-main', id="container-principal")


# Callback para mostrar/ocultar la barra lateral
@app.callback(
    Output('sidebar', 'style'),
    Input('toggle-button', 'n_clicks'),
    State('sidebar', 'style')
)
def toggle_sidebar(n_clicks, style):
    if n_clicks and style:
        return {'display': 'none'} if style.get('display') != 'none' else {'display': 'block'}
    return style or {'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=True)
