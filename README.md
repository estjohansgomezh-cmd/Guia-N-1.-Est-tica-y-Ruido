# Guia N°1: Estática y Ruido

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

### Referencias

* <a name="ref-schumann"></a> **Schumann, A., et al.** (Julio de 2021). *Envejecimiento autonómico: un conjunto de datos para cuantificar los cambios de la función autonómica cardiovascular durante el envejecimiento saludable*. PhysioNet. [https://doi.org/10.13026/2hsy-t491](https://doi.org/10.13026/2hsy-t491)







