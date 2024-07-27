
import json
import dash
from dash import html, callback, Input, Output, State, dcc
import dash_leaflet as dl
from dash.dependencies import ALL
dash.register_page(__name__, order=2)
import pandas as pd
import numpy as np
import subprocess






# Leer archivo GeoJSON
with open('subeLevanta1.geojson') as f:
    archivo = json.load(f)

subestaciones = []
coordenadas = []

for feature in archivo["features"]:
    subestaciones.append(feature["properties"])
    coordenadas.append(feature["geometry"]["coordinates"])
 
coordenadas_df = pd.Series(coordenadas)
subestaciones_df = pd.DataFrame(subestaciones)
subestaciones_df["coordenadas"]=coordenadas_df
subestaciones_df.set_index(["name"], inplace=True)


# ------------------------------------------------------

AGlevantamiento = pd.read_excel("Datos\\LaboratorioFormateos\\ArchivoGeneral.xlsx", index_col=1)
pd_AGlevantamiento = pd.DataFrame(AGlevantamiento)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}




#-------------------------------------------------------


def mostrarCaract(value):
    return [
        dl.Popup([
            
            html.Div([
                html.P("Información de levantamiento"),
                html.P(f" ID : {subestaciones_df.loc[value].get("Subestacion")}"),
                html.P(f" Cumple Norma Codensa : {subestaciones_df.loc[value].get("Cumple Norma Codensa")}"),
                html.P(f" Calibre : {subestaciones_df.loc[value].get("Calibre")}")
            ])
        
        ], position= [subestaciones_df.loc[value].get("coordenadas")[1],subestaciones_df.loc[value].get("coordenadas")[0]] , autoPan=True, )

    ]


custom_icon = lambda x : dict(
    iconUrl='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.6.0/images/marker-icon.png',
    iconSize=[25, 41], iconAnchor=[12, 41],
    shadowUrl='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.6.0/images/marker-shadow.png',
    shadowSize=[41, 41],
    className=f'icon-ubi-Riesgo-{x}'  # Aquí puedes añadir una clase CSS personalizada
)

# Añadir el marcador con el icono personalizado


layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        #dl.GeoJSON(data=archivo, children=[dl.Popup(id="Popper")], id="puntos"),
        html.Div(id = "pinpun"),
        


        html.Div(id="puntero"),
    ], center=[4.6368843894906355, -74.08367526976248], zoom=16,className="mapa-container"),

    #---- Ventana Caracteristicas
    html.Div(children=[

        html.H1("Datos de Diseño y levantamiento", style={"textAlign": "center"}),

        html.Div([

            html.Div(id="boton-archivoGeneral",style={"cursor":"pointer",
                                                      "align-content":"center",
                                                      "border-radius":"10px",
                                                      "margin":"10px",
                                                      "padding":"5px",
                                                      "background-color":"aqua",
                                                      "width":"100px",
                                                      "height":"50px"}),



            dcc.Dropdown(
            id='subestacion-dropdown',
            value="236",
            options=[{'label': subestacion["name"], 'value': subestacion["name"]} for subestacion in subestaciones],
            placeholder="Selecciona una subestación",
            style={"margin":"10px"},
            clearable=False
            ),

            dcc.RadioItems(["Ver Puntos","Quitar Puntos"], id="opcion-ver-puntos", value="Ver Puntos",style={"margin":"10px"}),


        ],style={"display":"flex","margin-right":"10px"}),

        html.Div([

                dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[

                    dcc.Tab(label='Levantamiento', value='levantamiento-value', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Diseño', value='diseño-value', style=tab_style, selected_style=tab_selected_style),
                
                ], style=tabs_styles),

                html.Div(id='tabs-content-inline')
        ])



    ],id="caracteristicas", className="conte-caract"),
    #-----------------------------------------------------------------------------
], className='Container-Demanda', id="idcontent")


@callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'),
              Input("subestacion-dropdown","value"), prevent_initial_call=True
              
              )
def render_content(tab, ID):

    if tab == 'levantamiento-value':
        return html.Div([
            html.P(f"{pd_AGlevantamiento.columns[i]}:{pd_AGlevantamiento.loc[ID].get(i)}") for i in range(1,9) 
        ], style={"margin-left":"10px"})
    elif tab == 'diseño-value':
        return html.Div([
            html.H3('-----Contruccion----------')
        ])





@callback(
        
        Output("boton-archivoGeneral", "children"),
        Input("boton-archivoGeneral","n_clicks")

)

def openArGen(n_clicks):
    if n_clicks:
        subprocess.run(["start", "EXCEL.EXE", "Datos\\LaboratorioFormateos\\ArchivoGeneral.xlsx"], shell=True)
        return "Archivo Abierto"
    else:
        return "Archivo Sin Abrir"

@callback(
        Output("pinpun","children"),
        Input("opcion-ver-puntos","value")
)


def pintarPuntos(value):


    if value == "Ver Puntos":

        children =[]
        pd_AGlevantamiento.fillna(0, inplace=True)


        children_info = []
        for subestacion in pd_AGlevantamiento.index:
                
                subestacionInfo = pd_AGlevantamiento.loc[subestacion]

                color="NA"
                if( type(subestacionInfo.get("Valoración del riesgo de SE (1 - 125)")) != str ):

                    if int(subestacionInfo.get("Valoración del riesgo de SE (1 - 125)")) >=89:
                        color="Alto"
                    elif int(subestacionInfo.get("Valoración del riesgo de SE (1 - 125)")) >=56:
                        color="Medio"
                    elif int(subestacionInfo.get("Valoración del riesgo de SE (1 - 125)")) >=1:
                        color="Bajo"

                

                children.append( 
                    dl.Marker(
                    position=[subestacionInfo.get("Lat"),
                              subestacionInfo.get("Lon")],
                    icon= custom_icon(color), 
                    children=[dl.Tooltip(subestacion),
                              dl.Popup([
                                  
                                       html.P(f"Valoración Riesgo:  {subestacionInfo.get("Valoración del riesgo de SE (1 - 125)")}"),
                                       html.P(f"Subestación de entrada:  {subestacionInfo.get("Subestación de entrada")}\""),
                                       html.P(f"Subestación de salida:  {subestacionInfo.get("Subestación de salida")}"),
                                       html.P(f"Condición Física:  {subestacionInfo.get("Condición Física")}")
                                              
                                              ])
                                       
                               ],
                    id="marker-point" )
                    )
        return  children         
    
    


        
    
   
#----.---- CallBack para Mostrar Caracteristicas selecionadas


    

#-----------CallBack para Mostrar el PopUp
@callback(
        Output("puntero","children"),
        Input("subestacion-dropdown","value"),
)

def selec(value):
    if value != None:  
        lon, lat = subestaciones_df.loc[value].get("coordenadas")
        return mostrarCaract(value) 
    else:
        return [""]
#
#@callback(
#    Output('Popper', 'children'),
#    Input('puntos', 'clickData')
#
#)
#def display_feature_info(feature):
#
#    if feature is not None:
#        props = feature['properties']
#        coord = feature['geometry']
#        info = [html.H4("Información de la Subestación")]
#        print(coord)
#        for key, value in props.items():
#            info.append(html.P(f"{key}: {value}"))
#        return info
#    return html.P("Haz clic en una subestación para ver su información.")
#
#
