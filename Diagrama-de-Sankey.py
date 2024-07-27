import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1('Diagramas de Sankey'),
    html.Div('DATAFRAME'),
], className='Container-Sankey')