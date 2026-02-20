# Guia N°1: Estática y Ruido
---
## Descripción 
En este repositorio se presenta el informe y los resultados de la Práctica de Laboratorio #1 de Estática y Ruido. Se trabajó con diferentes señales biomédicas, analizando su adquisición, comportamiento y presencia de ruido, así como su procesamiento y las conclusiones obtenidas del estudio experimental.

## Procedimiento
Durante el presente archivo, se calcularán parámetros estadísticos de señales biomédicas reales con el fin de proporcionar una descripción de esta y establecer posibles relaciones entre los valores estadísticos obtenidos y el proceso fisiológico. Esto debido a que las señales fisiológicas contienen información relevante, como amplitud y
frecuencia e información que la contamina, denominada ruido.
Es así que tomaremos una señal de physionet [<sup>[1]</sup>](#ref-schumann), del que importaremos la señal en python y a su vez se graficará utilizando el compilador spider, en el que se analizara mediante el cálculo de la media, desviación estándar, coeficiente de variación, asimetría y curtosis.
Estos cálculos se realizarán de dos formas: 
1. Programando las fórmulas matematicas desde cero
2. Utilizando funciones predefinidas de Spider.

Posteriormente, se genera una señal sintética similar usando un generador de señales biológicas, capturandolos mediante hardware NI-DAQ comparando sus estadísticos con los de la señal original.
Finalmente, se investigó la relación señal-ruido (SNR) contaminando la señal con ruidos de tipo gaussiano, impulso y artefacto para medir su impacto.

### ¿De qué se trata el estudio?
El objetivo principal del estudio es proporcionar una base de datos de señales biológicas de alta resolución para describir y cuantificar el efecto del envejecimiento saludable en la regulación cardiovascular autonómica.

La investigación parte de la premisa de que el control autonómico del ritmo cardíaco y la presión arterial disminuye progresivamente con la edad. Al documentar estos cambios en personas sanas, los investigadores buscan establecer una referencia que permita distinguir el envejecimiento normal de condiciones patológicas (como la demencia o enfermedades cardiovasculares) y desarrollar marcadores de "edad biológica" cardiovascular mediante aprendizaje automático (machine learning).

### ¿Cómo fueron capturados los datos?
Los datos se obtuvieron siguiendo un protocolo clínico estandarizado:
- Registraron datos de 1,121 voluntarios sanos.
- Las grabaciones se realizaron simultáneamente en estado de reposo.

Señales capturadas:
- (ECG), para monitorear la actividad eléctrica del corazón.
- Presión arterial continua no invasiva, para poder observar la dinámica de la presión latido a latido.
- Son señales de alta resolución que permiten analizar la variabilidad de la frecuencia cardíaca (HRV), la dinámica de las ondas de pulso y el acoplamiento cardiovascular.

### ¿Quién los tomó?
Los datos fueron capturados y publicados por investigadores del Laboratorio de Neurociencia Autonómica, Imagen y Cognición (LANIC), perteneciente al Departamento de Medicina Psicosomática y Psicoterapia del Hospital Universitario de Jena, en Alemania.
Los autores principales responsables del conjunto de datos son:
- Andy Schumann y Karl-Jürgen Bär

El estudio contó con el apoyo de la Fundación Alemana de Investigación (DFG) y el Centro Interdisciplinario de Investigación Clínica de Jena.

## PARTE A
La señal tomada de physionet corresponde a la número 0743.dat y 0743.hea (señales que se utilizaron durante todo el desarrollo de la guía).
### Programando desde cero:
Al ser importada la señal se utilizaron los siguientes parámetros usando Spider como compilador de phython, gracias a su terminal:

<img width="902" height="819" alt="Captura de pantalla 2026-02-19 190453" src="https://github.com/user-attachments/assets/e1c42f82-17e3-4042-9911-a50232cfceb0" />

<p><i>Estadísticos descriptivos para la señal 0743</i></p>
Esto con el fin de obtener dos tipos de gráficas una referente al ECG (Electrocardiograma) y la segunda respecto a NIBP (Non-Invasive Blood Pressure).

El programa cargó una grabación de 934 segundos (15 minutos), pero para este ejercicio se creo una ventana de 10 segundos.
- El ECG mide la actividad eléctrica del corazón en milivoltios ($mV$).
- El NIBP mide la presión de la sangre en milímetros de mercurio ($mmHg$).

El ECG tiene valores muy pequeños, lo que es normal debido a que la señal sube y baja constantemente por lo cual se empleó:
1. Asimetría (4.10): Al ser un valor positivo alto, indica que hay picos muy marcados hacia arriba (las ondas R del latido).
2. Curtosis (18.98): Este valor tan alto confirma que la señal tiene formas muy puntiagudas (el latido es un disparo eléctrico súbito).

Por su parte los estadísticos de NIBP son más grandes y fáciles de interpretar en un contexto médico:
1. Media (75.64 $mmHg$): Es la presión promedio durante esos 10 segundos.
2. Desviación Estándar (19.97 $mmHg$): Indica cuánto varía la presión. Una variación de casi 20 unidades sugiere que la señal captura el cambio entre la presión máxima (sístole) y mínima (diástole).
3. Curtosis (-0.25): Al ser un valor negativo y cercano a cero, significa que la presión es más plana comparada con los picos del corazón.

<img width="1946" height="889" alt="grafica1_senales_cero" src="https://github.com/user-attachments/assets/62c655e2-df82-49b4-af87-7cc4943be424" />
<p><i>Gráfica ECG y NIBP</i></p>
Finalmente se obtuvo el histograma con el fin de ver cómo se distribuyen los valores de las señales biomédicas que acabas de procesar.
<img width="1935" height="742" alt="grafica2_histogramas_cero" src="https://github.com/user-attachments/assets/94a8b94d-c054-4c20-8a61-06dea50cf94b" />
<p><i>Histogramas</i></p>

A su vez este es el diagrama de flujo el cual representa el paso a paso de la programación usada: 
<img width="1344" height="963" alt="Diagrama de Flujo_ - visual selection (1)" src="https://github.com/user-attachments/assets/e7a742b2-1db2-4f4a-9c75-e651ffc63bdf" /> <p><i>Diagrama de proceso</i></p>

## PARTE B
Se generó una señal fisiológica del mismo tipo de la usada en la parte A utilizando el generador de señales biológicas y se capturó con la NI-DAQ (en el que se dejó el archivo para la captura).

Esta primera imagén es la representación directa de los voltajes que capturó la tarjeta DAQ.

<img width="737" height="889" alt="grafica_boxplot_capturado_20260219_112925" src="https://github.com/user-attachments/assets/b9f9edda-353a-4c7f-aef6-fbb95c9bc56c" />

<i>Gráfica boxplot de la señal capturada por la NI-DAQ</i></p>
<img width="1337" height="744" alt="grafica_histograma_capturado_20260219_112925" src="https://github.com/user-attachments/assets/7fa454ae-6eb8-497a-9ef7-8ccff02d86b6" />
<i>Histograma 2</i></p>
<img width="1937" height="744" alt="grafica_senal_capturada_20260219_112925" src="https://github.com/user-attachments/assets/39c7f13a-8a3d-4262-9d7d-78e2f9916af7" />
<i>Gráfica señal capturada por la NI-DAQ</i></p>

El archivo txt. suministrado en archivos, contiene una lista de números decimales (flotantes). Cada número representa la amplitud de la señal en un instante de tiempo específico, es decir, el voltaje ($V$) que la tarjeta NI-DAQ midió en su entrada analógica.
Asímismo valores como 0.00315, 0.00283, etc, lo que nos indica que la señal capturada tiene un nivel de ruido o una amplitud muy baja en ese fragmento, cercana a 0V.


### Referencias

* <a name="ref-schumann"></a> **Schumann, A., et al.** (Julio de 2021). *Envejecimiento autonómico:
 un conjunto de datos para cuantificar los cambios de la función autonómica cardiovascular durante el envejecimiento saludable*. PhysioNet. [https://doi.org/10.13026/2hsy-t491](https://doi.org/10.13026/2hsy-t491)












