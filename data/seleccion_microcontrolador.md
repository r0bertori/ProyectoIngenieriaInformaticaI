# Selección del microcontrolador y mapa de pines

**Proyecto:** El Bar de Moe (ZONEXIS)
**Responsable:** Diego Enríquez Carrera
**Sprint:** 1
**Fecha:** 01/11/2026
**Estado:** Cerrado

## 1. Qué tiene que hacer la placa

La placa se encargará de recopilar las lecturas de los sensores físicos de la maqueta y enviar los datos a nuestra aplicación de escritorio para procesarlos. Como es un prototipo, usaremos módulos de bajo coste para simular los sistemas reales del bar.

| ID | Sensor | Tipo de señal que da |
|---|---|---|
| S01 | Aforo (2 sensores IR FC-51, entrada y salida) | Digital |
| S02 | Humo (módulo MQ-2) | Analógica |
| S03 | CO2 / calidad del aire (módulo MQ-135) | Analógica |
| S04 | Ruido (micrófono KY-038) | Analógica |
| S05 | Estado de la terraza (pulsador/final de carrera) | Digital |
| S06 | Nivel de contenedor (ultrasonidos HC-SR04) | Digital (2 pines) |
| S07 | Consumo eléctrico (módulo INA219) | I2C (SDA, SCL) |
| S08 | Venta de alcohol (pulsador) | Digital |
| S09 | Máquina de tabaco y tragaperras (pulsador) | Digital |
| S10 | Temperatura y humedad (DHT11) | Digital |
| S11 | Botón de emergencia | Digital |

## 2. Comparativa

Hemos comparado el ESP32 con el clásico Arduino Uno para ver cuál nos conviene más de cara a conectarlo con la Raspberry Pi y el backend en Python.

| Característica | ESP32 | Arduino Uno |
|---|---|---|
| Tensión de trabajo de los pines | 3,3 V | 5 V |
| Pines digitales disponibles | ~26 usables | 14 |
| Entradas analógicas | 15 (8 usables con el WiFi encendido) | 6 |
| Conexión inalámbrica (WiFi) | Sí, integrada en la propia placa | No, requiere escudo/módulo aparte |
| Comunicación con el PC/Raspberry | WiFi (MQTT/HTTP), Bluetooth, o cable USB | Solo por cable USB |
| Precio aproximado | 5 - 7 € | ~20 € (original) / 5 - 7 € (clon) |
| Experiencia previa del equipo | Intermedia | Alta |

## 3. Decisión

**Placa elegida:** ESP32 (versión NodeMCU o equivalente de 38 pines).

**Motivo:** Nos decantamos por el ESP32 porque lleva el WiFi integrado de fábrica y su coste es equivalente al de un clon de Arduino. Esto nos permite mandar los datos a la Raspberry Pi de forma inalámbrica, simplificando la maqueta. Además, cuenta con más pines y memoria, lo cual es necesario para gestionar los 11 sensores del proyecto sin recurrir a multiplexores externos.

## 4. Mapa de pines

**Nota técnica:** El ESP32 trabaja a 3.3V. Algunos sensores como los de gas (MQ-2, MQ-135) o el sensor de distancia (HC-SR04) se alimentan a 5V y devuelven señales de 5V. Para proteger la placa, implementaremos divisores de tensión (resistencias) en los pines de recepción de esos sensores para reducir la señal a 3.3V. Las señales analógicas se han agrupado en los pines del ADC1 (32 al 35), ya que el ADC2 se desactiva al usar el WiFi.

| Sensor | Pin de la placa | Tipo de señal | Alimentación | Notas |
|---|---|---|---|---|
| S01 Aforo (entrada) | GPIO 13 | Digital | 3,3 V | Módulo IR FC-51. |
| S01 Aforo (salida) | GPIO 14 | Digital | 3,3 V | Módulo IR FC-51. |
| S02 Humo (MQ-2) | GPIO 34 (ADC1) | Analógica | 5 V | Requiere divisor de tensión en el pin de datos. |
| S03 CO2 (MQ-135) | GPIO 35 (ADC1) | Analógica | 5 V | Requiere divisor de tensión en el pin de datos. |
| S04 Ruido (KY-038) | GPIO 32 (ADC1) | Analógica | 3,3 V | |
| S05 Terraza | GPIO 15 | Digital | 3,3 V | Pulsador simple. |
| S06 Contenedor (Trig)| GPIO 2 | Digital | 3,3 V | Señal de salida del ESP32. |
| S06 Contenedor (Echo)| GPIO 5 | Digital | 5 V | Señal de retorno. Requiere divisor de tensión. |
| S07 Consumo (INA219)| GPIO 21 (SDA), 22 (SCL) | I2C | 3,3 V | |
| S08 Alcohol | GPIO 18 | Digital | 3,3 V | Pulsador. |
| S09 Máquinas | GPIO 19 | Digital | 3,3 V | Pulsador. |
| S10 Temp/Humedad | GPIO 25 | Digital | 3,3 V | Módulo DHT11. |
| S11 Emergencia | GPIO 26 | Digital | 3,3 V | Pulsador. |

Total de pines usados: 14 de los ~26 disponibles.

## 5. Fase de la maqueta

- ¿Caben todos los sensores en una sola placa? Sí.
- Material que habrá que comprar: ESP32, módulos MQ-2 y MQ-135, HC-SR04, INA219, KY-038 y DHT11. También resistencias variadas y una protoboard para cablear los divisores de tensión.
- Riesgos detectados: Trabajar con voltajes mixtos (3.3V y 5V). Es crítico revisar el circuito de los sensores a 5V (MQ y ultrasonidos) antes de conectarlos a los pines del ESP32 para evitar dañar el microcontrolador.

## 6. Referencias

- Hoja de especificaciones de Espressif (ESP32): https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf
- Guía de pines seguros del ESP32: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/