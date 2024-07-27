import dash
from dash import html, callback, Output, Input, dcc
import subprocess
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from Pages.managerDocument import docEvaluacionRiesgo



# Registro de la página
dash.register_page(__name__, order=1)

archivoNivelriesgo = pd.read_excel("Datos\\Evaluacion de riesgo\\GDB-SE MT.xlsx", sheet_name="SE-Info-Levamntamiento" , index_col="ID" )
df_lvl = pd.DataFrame(archivoNivelriesgo)



slash = ["Arco eléctrico",
          "Ausencia de electricidad",
          "Contacto Directo",
          "Contacto indirecto",
          "Cortocircuito",
          "Electricidad estática",
          "Equipo defectuoso",
          "Rayos",
          "Sobrecarga",
          "Tensión de Contacto",
          "Tensión de Paso"]

# Layout de la página
layout = html.Div([
    
    html.Div([
        
        dcc.Graph(id="stampa", style={"margin-top":"20px"} ),
        
          ],style={"background-color":"white","border-radius":"20px","width":"50%","height":"50%"}),
    html.Div([

        html.Div(id="miremos",className="miremos"),

        html.Div([

            dcc.Dropdown(
                id='riesgo-subestacion-dropdown',
                options=docEvaluacionRiesgo("Rayos").index,
                value=236,
                placeholder="Selecciona una subestación",
                clearable=False,
                style={"margin-top":"15px",
                       "border-radius":"15px",
                       "width":"150px"} ),

            dcc.Dropdown(
                options=slash,
                value="Arco eléctrico",
                clearable=False,
                style={ "border-radius":"15px",
                        "width":"150px"}, 
                id="Radio")
                
                ],style={"display":"inline-flex"}),

        html.Div([
                html.Div(id="bot-abrir-valRies", style={"background-color":"aqua",    
                                                        "margin-left":"10px",
                                                        "margin-bottom":"15px",
                                                        "font-weight":"800",
                                                        "border-radius":"10px",
                                                        "cursor":"pointer",
                                                        "padding":"10px"}),
                html.Div(id="estado-riesgo"),
                html.Div(id="condicion-Div",style={"margin-top":"15px"}),
                html.Div(id="infor-riesgo",className="infor-riesgos-Div" )
         ])

        ],style={"background-color":"transparent","margin-left":"15px"}),

    

], className='Container-Evaluacion', style={"display":"inline-flex"})

@callback(
        Output("stampa","figure"),
        Output("estado-riesgo","children"),
        Output("infor-riesgo","children"),
        Output("condicion-Div","children"),
        Input("riesgo-subestacion-dropdown","value"),
        Input("Radio","value")     
)
def graficar(Id,riesgo):

    if riesgo != None:
        doc = docEvaluacionRiesgo(riesgo)
        grafica = doc[doc.columns[[i for i in range(1,7)]]]
        fig = px.bar(x=grafica.loc[Id].index, y=grafica.loc[Id].values , title=riesgo)
        lvl= df_lvl.loc[Id].get("Valoración del riesgo de SE (1 - 125)")
        children=["Seleccione Para Empezar"]
        
        if df_lvl.loc[Id].get("Condición Física")=="Buena":
            children_calidad =[html.Div(f"Condición Física: Buena ", style={"background-color":"#5ee67ec7",
                                                                                                "border-radius":"15px",
                                                                                                "padding":"10px",
                                                                                                "margin-left":"10px",
                                                                                                "width":"80%",
                                                                                                "font-weight":"800"
                                                                                                })]
        elif df_lvl.loc[Id].get("Condición Física")=="Aceptable":
            children_calidad =[html.Div(f"Condición Física: Aceptable ", style={"background-color":"yellow",
                                                                                                "border-radius":"15px",
                                                                                                "padding":"10px",
                                                                                                "margin-left":"10px",
                                                                                                "width":"80%",
                                                                                                "font-weight":"800"
                                                                                                })]
        else:
            children_calidad =[html.Div(f"Condición Física: Deteriorada", style={"background-color":"orange",
                                                                                                "border-radius":"15px",
                                                                                                "padding":"10px",
                                                                                                "margin-left":"10px",
                                                                                                "width":"80%",
                                                                                                "font-weight":"800"
                                                                                                })]
            
                
        children_infor_riesgos = [
            html.H4(f"{columna} : {df_lvl.loc[Id].get(columna)} ")  for columna in df_lvl.columns
        ]
        if type(lvl) == int:
            if lvl >=89 :
                children = [html.Div(f"Valoración \nRiesgo de SE (1 - 125): {lvl}", style={"background-color":"#a82929ce",
                                                                                                "border-radius":"15px",
                                                                                                "padding":"10px",
                                                                                                "margin-left":"10px",
                                                                                                "width":"80%",
                                                                                                "font-weight":"800"})]
            elif lvl >= 56:
                children = [html.Div(f"Valoración \nRiesgo de SE (1 - 125): {lvl}", style={"background-color":"yellow",
                                                                                                "border-radius":"15px",
                                                                                                "padding":"10px",
                                                                                                "margin-left":"10px",
                                                                                                "width":"80%",
                                                                                                "font-weight":"800"})]
            else:
                children = [html.Div(f"Valoración \nRiesgo de SE (1 - 125): {lvl}", style={"background-color":"#5ee67ec7",
                                                                                                "border-radius":"15px",
                                                                                               "padding":"10px",
                                                                                                "margin-left":"10px",
                                                                                                "width":"80%",
                                                                                                "font-weight":"800"})]
        else:
            children=["Provicional Obra"]

        return  fig, children, children_infor_riesgos, children_calidad
    else:
        grafica = docEvaluacionRiesgo("Arco eléctrico")
        return  px.bar(x=grafica.loc[Id].index, y=grafica.loc[Id].values ), "jojo", children_infor_riesgos, children_calidad

# Callback para abrir el archivo Excel
@callback(
    Output("miremos", "children"),
    Input("miremos", "n_clicks")
)
def openExcel(clikeo):
    if clikeo is None:
        return "Archivo Riesgos sin Abrir"
    else:
        # Puedes incluir el código para abrir el archivo Excel aquí si es necesario
        subprocess.run(["start", "EXCEL.EXE", "Datos\\Evaluacion de riesgo\\PMSEREUN-EJ-02-01-HDA-9.xlsx"], shell=True)

        return f"Archivo de Riesgos Abierto {clikeo}"

@callback(
    Output("bot-abrir-valRies","children"),
    Input("bot-abrir-valRies","n_clicks")
)

def openExcelValRies(clickers):
    if clickers is None:
        return "Archivo Valoracion sin Abrir"
    else:
        # Puedes incluir el código para abrir el archivo Excel aquí si es necesario
        subprocess.run(["start", "EXCEL.EXE", "Datos\\Evaluacion de riesgo\\GDB-SE MT.xlsx"], shell=True)

        return f"Archivo de Riesgos Abierto {clickers}"