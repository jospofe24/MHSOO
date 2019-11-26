import pandas as pd, matplotlib.pylab as plt

## Cargo el archivo CSV
df = pd.read_csv (r'/home/pi/Arduino/temps_sens_josue/medicion_hum_temp.csv')

''' Los datos de las columnas Humedad y Temperatura tienen una comilla que hay que quitar
para poder graficar después'''

cols_to_check = ['Humedad', 'Temperatura']
df[cols_to_check] = df[cols_to_check].replace({"'":""}, regex=True)

''' Las columnas de Humedad y Temperatura hay que convertiralas a float
para poder graficar los valores ya que están como string '''

df = df.astype({"Temperatura": float, "Humedad": float})

## Hay que unir los datos de fecha y hora, ya que pandas lee los dos valores en una sola columna
df['Fecha y Hora'] = df['Fecha'] +" "+ df['Hora']

## Remuevo las columnas de Fecha y Hora
df = df.drop(columns=["Fecha","Hora"], axis=1)

## Convierto a formato de fecha y hora para que pandas lo interprete así
df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"])

''' Le digo al pandas que mi Index, o columna para buscar datos va a
 ser Ubicacion '''
df.set_index("Ubicacion", inplace=True)
reset = 1
while reset == 1:
    print(' ')
    print('Lugares: 1. Cocina 2. Cuarto Lavado 3. Terraza 4. Sala T.V 5. Dormitorio')
    print(' ')
    lugar_int = int(input('Ingrese el número del lugar que desea graficar: '))
    print(' ')
    if lugar_int == 1:
        lugar = str('Cocina')
    elif lugar_int == 2:
        lugar = str('Cuarto_Lavado')
    elif lugar_int == 3:
        lugar = str('Terraza')
    elif lugar_int == 4:
        lugar = str('Sala_TV')
    elif lugar_int == 5:
        lugar = str('Dormitorio')
    print('Variables: 1. Humedad 2. Temperatura')
    print(' ')
    var_int = int(input('Ingrese el número de la variable que desea graficar: '))
    if var_int == 1:
        var = str('Humedad')
    elif var_int == 2:
        var = str('Temperatura')
    print(' ')
    print('Formato de fecha: AAAA-MM-DD')
    print(' ')
    start_date = str(input('A partir de que fecha desea graficar: '))
    print(' ')
    end_date = str(input('Hasta que fecha desea graficar: '))
    print(' ')
    print('Formato de hora: HH:MM:SS')
    print(' ')
    start_time = str(input('A partir de que hora desea graficar: '))
    print(' ')
    end_time = str(input('Hasta que hora desea graficar: '))
    fecha_inicio = start_date + " " + start_time
    fecha_final = end_date + " " + end_time
    ''' Creo un nuevo set para el lugar seleccionado con solo los datos de fecha hora y variable y
    grafico '''
    df_graph = df.loc[lugar,['Fecha y Hora', var]]
    
    ## Añado solo los datos entre las fechas establecidas
    df_graph = df_graph[(df_graph['Fecha y Hora'] > fecha_inicio) & (df_graph['Fecha y Hora'] <= fecha_final)]

    ## Chequeo el frame para que no esté vacío
    if df_graph['Fecha y Hora'].empty:
        print(' ')
        print('No hay datos en las fechas establecidas')
        print(' ')
        print('Reingrese un rango de fechas con datos')
        reset = 1
    ## Si tiene datos, grafico
    else:
        reset = 0
        df_graph['Fecha y Hora'] = df_graph['Fecha y Hora'].dt.time
        df_graph.plot(x='Fecha y Hora',y=var)
        plt.suptitle(lugar, fontsize=15)
        plt.title("Desde el {} hasta el {}.".format(start_date,end_date), fontsize=10)
        plt.xlabel('Hora')
        plt.ylabel(var)
        plt.show()
