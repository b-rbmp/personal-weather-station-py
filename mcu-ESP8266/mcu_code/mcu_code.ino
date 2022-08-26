#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h> // Biblioteca: https://arduinojson.org/
#include <MQ135.h> // Biblioteca: https://github.com/GeorgK/MQ135.git
#include <DHT12.h> // Biblioteca: https://github.com/xreef/DHT12_sensor_library
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

String apiKey = "SECRET_API_KEY"; // Entre a API Key registrada no Web App
const char *ssid = "SECRET_SSID"; // Entre com o SSID da rede WiFi
const char *password = "SECRET_PASSWORD"; // Entre com a senha do WiFi
const char *server = "localhost:8000"; // Entre com o servidor back-end

Adafruit_BMP280 bmp; // I2C
DHT12 dht12;
WiFiClient client;

void sensor_data() {
  MQ135 sensor_gas = MQ135(A0);
  float air_quality = sensor_gas.getPPM();
  float humidity = dht12.readHumidity();
  float temperature = dht12.readTemperature(); // Mais preciso que o bmp 
  float pressure = bmp.readPressure();

  if (WiFi.status() == WL_CONNECTED) { // Ve se o ESP8266 está conectado
    DynamicJsonDocument doc(256); // <- 2256 bytes in the heap
    doc["api_key"] = apiKey;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["pressure"] = pressure;
    doc["air_quality"] = air_quality;
    // Serialize JSON document
    String json;
    serializeJson(doc, json);
    
    HTTPClient http;
  
    // Send request
    http.begin(client, server);
    http.addHeader("Content-Type", "application/json");
    http.POST(json);
    
    // Read response
    Serial.print(http.getString());
    
    // Disconnect
    http.end();
  } else {
 
    Serial.println("Erro na conexão WiFi");
 
  }
}
void setup() {
  Serial.begin(9600);
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");
  
  // Envia o IP local do ESP8266
  Serial.println(WiFi.localIP());  

  bmp.begin(BMP280_ADDRESS);

  sensor_data();
  ESP.deepSleep(60e7); // Deep sleep por 10 minutos. Limite é 71 minutos. Após o tempo, é gerado um sinal de reset e o setup() é executado novamente
}

void loop() {
}
