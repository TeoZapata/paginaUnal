import dash
from dash import html, callback, Output, Input, dash_table, dcc
import subprocess
import pandas as pd

dash.register_page(__name__,order=3)

def cargarArchivo(ruta):
    data = pd.read_csv(ruta)
    return data

    
archivo = cargarArchivo(".\\Datos\\LaboratorioFormateos\\datosLevantamiento.csv")

layout = html.Div([
    html.Button("Abrir Archivo", id="tablas-abrir-archivo"),
    html.Button("Cargar", id="cargar"),
    html.Div([
        html.Div(id="ok"),
        html.Div([
           f"{archivo.columns}"
        ])

    ], style={"background-color": "white", 
                            "padding":"15px",
                            "margin-top":"15px",
                            "height": "150px",
                            "border-radius": "10px"}, id="tablas-informacion"),

    html.Div([
        html.Div("Contenido"),
        html.Div([
                dash_table.DataTable(data=archivo.to_dict("records") ,page_size=4, style_table={"overflowX":"auto"})
            ])
    ], className="tablas-DataFrame", style={"background-color": "white", 
                            "padding":"15px",
                            "height": "200px",
                            "border-radius": "10px",
                            "margin-top":"15px"}),

], className='Container-Tablas')



@callback(
    Output("ok","children"),
    Input("tablas-abrir-archivo", "n_clicks")
)
def acciona(n_clicks):
    if n_clicks:
        subprocess.run(["start", "EXCEL.EXE", "Datos\\Levantamiento\\datosLevantamiento.xlsx"], shell=True)
        return "ok"