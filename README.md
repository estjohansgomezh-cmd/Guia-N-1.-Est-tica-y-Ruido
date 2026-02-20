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
### Funciones predefinidas de python:
<img width="654" height="1234" alt="DIAGRAMA DE FLUJO - visual selection" src="https://github.com/user-attachments/assets/bcaaecbd-67cf-44b7-8e61-a2c57c271a59" />

<i>Diagrama de proceso 2</i></p>
<img width="619" height="292" alt="Cuadro comparativo - visual selection" src="https://github.com/user-attachments/assets/8b75fcc9-933a-4c7c-81c4-614c6d98f7f5" />

## CON FUNCIONES
En esta sección se realizó el análisis estadístico de la señal biomédica 0743 obtenida de PhysioNet, empleando funciones predefinidas de las librerías NumPy y SciPy, lo que permite optimizar el procesamiento y reducir significativamente la complejidad del código respecto a la implementación “desde cero”.

La señal completa contiene 933.820 muestras, equivalentes a 934 segundos de registro. Para efectos del análisis, se trabajó con una ventana de 10 segundos (10.000 muestras), considerando una frecuencia de muestreo de 1000 Hz.

###Procesamiento de la señal

Inicialmente, el archivo 0743.dat fue leído mediante np.fromfile(), convirtiendo los valores digitales a unidades físicas:
ECG → milivoltios (mV)
NIBP → milímetros de mercurio (mmHg)
Posteriormente, se recortó la señal a una ventana de 10 segundos y se construyó el vector de tiempo:

<img width="71" height="53" alt="image" src="https://github.com/user-attachments/assets/df110cda-acfe-4a90-be9c-e455a839c18b" />​
lo que permitió representar correctamente las señales en el dominio temporal.

###Cálculo de estadísticos descriptivos

Para el cálculo de los parámetros estadísticos se utilizaron funciones optimizadas:
-Media → np.mean()
-Desviación estándar muestral → np.std(ddof=1)
-Varianza muestral → np.var(ddof=1)
-Asimetría → stats.skew()
-Curtosis (exceso de Fisher) → stats.kurtosis()
-Coeficiente de variación → calculado como (𝑠/∣𝜇∣)×100
El uso de ddof=1 garantiza que la desviación estándar y la varianza sean muestrales, equivalentes al método manual desarrollado en la parte anterior.

📉 3. Señales en el dominio del tiempo

📌 AQUÍ INSERTAS LA IMAGEN 1
(Señales ECG y NIBP vs tiempo – grafica1_senales_numpy.png)

En la gráfica anterior se observa el comportamiento temporal de ambas señales durante los 10 segundos analizados.

ECG

La señal presenta picos pronunciados correspondientes a los complejos QRS del ciclo cardíaco.
La media es cercana a cero, lo cual es característico de señales eléctricas cardíacas centradas alrededor de un valor promedio.
Las líneas μ ± σ permiten visualizar la dispersión de los datos alrededor del promedio.

NIBP

La señal de presión arterial muestra una variación periódica asociada a cada latido cardíaco.
Se evidencia una mayor amplitud y un comportamiento más suave en comparación con el ECG.
La media representa la presión promedio en el intervalo analizado.

📊 4. Histogramas y distribución de probabilidad

📌 AQUÍ INSERTAS LA IMAGEN 2
(Histogramas – grafica2_histogramas_numpy.png)

Los histogramas permiten analizar la distribución estadística de las amplitudes.

ECG

Presenta asimetría positiva elevada.

La curtosis es alta, lo que indica presencia de valores extremos frecuentes.

La señal no sigue una distribución normal debido a los picos pronunciados del complejo QRS.

NIBP

La asimetría es cercana a cero.

La curtosis es cercana a cero, indicando una forma más parecida a la distribución normal.

La presión arterial presenta una distribución más equilibrada que el ECG.

La curva normal teórica superpuesta permite comparar visualmente el grado de ajuste respecto a una distribución gaussiana.

📦 5. Boxplots y análisis de dispersión

📌 AQUÍ INSERTAS LA IMAGEN 3
(Boxplots – grafica3_boxplots.png)

Los diagramas de caja permiten observar:

Mediana

Cuartiles

Rango intercuartílico

Valores atípicos

ECG

Se observan numerosos valores atípicos correspondientes a los picos del latido cardíaco, lo cual explica su elevada curtosis.

NIBP

Presenta una dispersión más amplia en valores absolutos, pero con menor cantidad de outliers extremos en comparación con el ECG.

🔁 Comparación con el método “desde cero”

En comparación con la implementación manual utilizando bucles for, el uso de funciones predefinidas:

Reduce significativamente la cantidad de código.

Mejora la velocidad de ejecución.

Disminuye la probabilidad de errores.

Facilita la interpretación y validación de resultados.

Utiliza algoritmos optimizados matemáticamente.

Ambos métodos producen resultados equivalentes; sin embargo, el uso de librerías especializadas representa una metodología más profesional y adecuada para aplicaciones reales en procesamiento digital de señales biomédicas.

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

Por ultimo comparando los resultados de la parte A con esta parte B podemos denotar un resultado clave y es la inestabilidad, esto ya que a diferencia de la Parte A, aquí la señal no es "perfecta". Hay pequeñas variaciones (picos) causadas por el hardware y el entorno.


## PARTE C
Se utilizó esta vez la misma señal pero del punto B 
Pero antes definamos ¿qué es la relación señal ruido (SNR)?
Es la proporción entre la potencia de la señal que queremos medir y la potencia del ruido que la corrompe. Se mide en decibelios (dB).
<img width="378" height="124" alt="Captura de pantalla 2026-02-19 215439" src="https://github.com/user-attachments/assets/b6505d7c-61d3-4994-99c8-46da61285fff" />

a. Ruido Gaussiano:
Es el ruido más común en electrónica. Se llama así porque su amplitud sigue una distribución de campana de Gauss.
- Añade un "chisporroteo" constante y uniforme a toda la señal. La línea de la gráfica se vuelve más gruesa.
- Medición del SNR: Como el ruido está en todas las frecuencias por igual, el SNR baja de forma constante. Es predecible y se puede reducir con filtros promedio.

b. Ruido de Impulso:
Son picos repentinos de gran amplitud y muy corta duración.
- Son líneas verticales disparadas hacia arriba o hacia abajo en puntos aleatorios de la gráfica, pero el resto de la señal se mantiene limpia.
- Medición del SNR: El SNR cae drásticamente solo en los instantes del pulso. Para medirlo correctamente, se suele usar la potencia promedio del ruido en toda la ventana de tiempo.

c. Ruido tipo Artefacto:
Este ruido no es aleatorio, sino que tiene una causa específica (como el movimiento de un sensor, la interferencia de 60Hz de un enchufe o un parpadeo en un ECG).
- Crea deformaciones sistemáticas. Puede parecer una "joroba" en la señal o una ondulación lenta que no pertenece al dato original.
- Medición del SNR: Es el más difícil de medir porque a veces se confunde con la señal misma. El SNR se calcula identificando la frecuencia del artefacto y comparando su energía contra la de la señal pura.

<img width="877" height="940" alt="Captura de pantalla 2026-02-19 220203" src="https://github.com/user-attachments/assets/b6c8b631-69ea-4028-a31c-dfa009497138" />
<p><i>Estadísticos descriptivos para la señal 0743</i></p>
<img width="2085" height="1479" alt="parteC_comparacion_senales_20260219_150616" src="https://github.com/user-attachments/assets/a35de72e-23f1-4aa9-8455-c7a62917506e" />
<p><i>Gráficas de las señales contaminadas</i></p>
<img width="1184" height="734" alt="parteC_comparacion_snr_20260219_150616" src="https://github.com/user-attachments/assets/d642ce51-2ce5-48c1-bb2e-8fdd7a8d29a5" />
<p><i>SNR según tipo de ruido</i></p>
<img width="2084" height="595" alt="parteC_histogramas_ruido_20260219_150616" src="https://github.com/user-attachments/assets/b6c11a81-0881-4910-9deb-b5194edaff76" />
<p><i>Histogramas de los tres tipos de ruidos</i></p>
<img width="2085" height="1479" alt="parteC_zoom_detalle_20260219_150616" src="https://github.com/user-attachments/assets/bafb2532-6ea9-42de-9458-64bd0b78a500" />
<p><i>Zoom</i></p>
<img width="603" height="1748" alt="DIAGRAMA DE FLUJO - visual selection (2)" src="https://github.com/user-attachments/assets/fafd3e3b-cab0-4c23-bae2-14e9a11d2822" />

Para cerrar esta parte se dejaron otros dos archivos txt, uno que representa la captura de datos y otro que representa los resultados del SNR.

## Conclusión:
Para concluir, la eficiencia de un sistema de procesamiento de señales se mide por su capacidad de mantener un SNR alto. La experimentación confirmó que la digitalización exitosa de una variable física depende directamente de la minimización de ruidos externos y de una frecuencia de muestreo adecuada, garantizando que el archivo final sea una representación fiel del fenómeno estudiado y no un producto del ruido electromagnético.

## Referencia:

* <a name="ref-schumann"></a> **Schumann, A., et al.** (Julio de 2021). *Envejecimiento autonómico:
 un conjunto de datos para cuantificar los cambios de la función autonómica cardiovascular durante el envejecimiento saludable*. PhysioNet. [https://doi.org/10.13026/2hsy-t491](https://doi.org/10.13026/2hsy-t491)













