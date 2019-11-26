 // Incluimos librerias
#include <LiquidCrystal.h> //Display
#include <DHT.h> //Sensor humedad, temperatura
 
// Definimos el pin digital donde se conecta el sensor
#define DHTPIN 6
// Defino el tipo de sensor
#define DHTTYPE DHT11

//Asigno pines para el display LCD
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
 
// Inicializamos el sensor DHT11
DHT dht(DHTPIN, DHTTYPE);
 
void setup() {
  // Inicializamos comunicación serie
  Serial.begin(9600);

 // Indicamos medidas de LCD
 lcd.begin(16,2);
 // Comenzamos el sensor DHT
 dht.begin();
 
}
 
void loop() {
    // Defino tiempo entre cada medición en milisegundos
  delay(30000);
 
  // Leemos la humedad relativa
  float h = dht.readHumidity();
  // Leemos la temperatura en grados centígrados
  float t = dht.readTemperature();
 
  // Envio datos a puerto serie
  Serial.print(h);
  Serial.print(","); //añado coma para separar los datos y poder escribirlos al CSV
  Serial.println(t);

  
  // Envio a LCD
  lcd.setCursor(0, 0);
  lcd.print("Temp.: ");
  lcd.print(t);
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Humedad: ");
  lcd.print(h);
  lcd.print("%");
 
}
