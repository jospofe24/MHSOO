import serial, time, csv, datetime

#Defino variable de conexión al Arduino
ser = serial.Serial('/dev/ttyACM0')
print(' ')
print ('\nIniciando conexion...')
print(' ')
ser.flushInput() #limpio conexión para evitar sobre escritura de datos y evitar errores

#Muestro detalles de la conexión serial al arduino
print ('Estado del puerto: %s ' % (ser.isOpen()))
print(' ')
print ('Nombre del dispositivo conectado: %s ' % (ser.name))
print(' ')

'''Creo el archivo para guardar los datos en CSV como medicion_hum_temp.csv
    y creo una fila con los nombres de las variables a guardar.
    Esto tiene que hacerse primero para guardar la fila con los nombres de lo
    contrario escribiría cada vez sobre los datos obtenidos.'''
new_arch = str(input("¿Desea sobreescribir el archivo con los datos? S/N: "))
print(' ')
if new_arch == 'S':
    with open('medicion_hum_temp.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Ubicacion","Fecha", "Hora", "Humedad", "Temperatura"])
        cont = 1
elif new_arch == 'N':
    pass

t_med = input("Ingrese el tiempo a medir en minutos: ")
#Tiempo de medición. 60 * X, siendo X el tiempo en minutos
t_end = time.time() + 60 * float(t_med)
print(' ')
lugar = str(input("Ingrese el nombre del lugar en donde va a realizar la medición: "))
print(' ')
start_time = time.time()
#Imprimo en pantalla los datos medidos
print("Insertando los datos...")
print(' ')
print('Humedad','Temperatura')
'''Loop para medir la cantidad de tiempo definida anteriormente (t_end)
La señal enviada por el Arduino es un string definido como 'humedad,temperatura' y
hay que separarlo (data = data_long.split()). Una vez separado, defino cada nueva variable
(hum=data.split(",")[0] y temp=data.split(",")[1])'''
while time.time() < t_end:
    data_long = ser.readline()
    data_long = data_long.decode("utf-8")
    data = data_long.split()
    data = str(data).strip('[]')
    hum=data.split(",")[0]
    temp=data.split(",")[1]
    print(hum,'%',temp,'C°')
    print(' ')
    '''Aquí se escriben los datos al archivo csv con fecha y hora
    El archivo csv se abre como 'a' (append) para no sobreescribir
    el que se creo antes'''
    with open("medicion_hum_temp.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        now = datetime.datetime.now()
        writer.writerow([lugar,now.strftime("%Y-%m-%d"),now.strftime("%H:%M:%S"),hum,temp])
        elapsed_time = time.time() - start_time

print('Finalizada la captación de datos.')
print(' ')
print('Tiempo de medición:',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
