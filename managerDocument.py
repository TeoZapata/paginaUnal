import pandas as pd



archivo = pd.read_excel("Datos\\Evaluacion de riesgo\\PMSEREUN-EJ-02-01-HDA-9.xlsx", sheet_name="Formato columnas", header=20, index_col=2)


df = pd.DataFrame(archivo)
df.drop(df.columns[[0,1]], axis=1, inplace=True)

def docEvaluacionRiesgo(riesgo:str)->pd.DataFrame:
  
    """"Arco eléctrico":(0,7)],
                "Ausencia de electricidad":range(7,14)],
                "Contacto Directo":range(14,21)],
                "Contacto indirecto":range(21,28)],
                "Cortocircuito":range(28,35)],
                "Electricidad estática":range(35,42)],
                "Equipo defectuoso":range(42,49)],
                "Rayos":range(49,56)],
                "Sobrecarga":range(56,63)],
                "Tensión de Contacto":range(63,70)],
                "Tensión de Paso":range(70,77)]}   """
    

    
    Riesgos = {"Arco eléctrico":pd.Index([i for i in range(0,7)]),
                "Ausencia de electricidad":pd.Index([i for i in range(7,14)]),
                "Contacto Directo":pd.Index([i for i in range(14,21)]),
                "Contacto indirecto":pd.Index([i for i in range(21,28)]),
                "Cortocircuito":pd.Index([i for i in range(28,35)]),
                "Electricidad estática":pd.Index([i for i in range(35,42)]),
                "Equipo defectuoso":pd.Index([i for i in range(42,49)]),
                "Rayos":pd.Index([i for i in range(49,56)]),
                "Sobrecarga":pd.Index([i for i in range(56,63)]),
                "Tensión de Contacto":pd.Index([i for i in range(63,70)]),
                "Tensión de Paso":pd.Index([i for i in range(70,77)])}        
   

    return df[df.columns[Riesgos.get(riesgo)]]





