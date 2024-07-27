import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([

                html.Div([
              
                     html.Div("gg"),
                     html.Footer(["Plan Maestro – Estudios y diseños para la regularización \nde las subestaciones y redes de media tensión en el campus de la \nsede Bogotá de la Universidad Nacional de Colombia"],
                       className="Footer-cont-inicio")],style={"display":"block"}),
    ]

    , className="ContainerInicio")