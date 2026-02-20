# -*- coding: utf-8 -*-
"""
=============================================================================
PRÁCTICA DE LABORATORIO – ANÁLISIS ESTADÍSTICO DE SEÑALES
Universidad Militar Nueva Granada
Asignatura: Procesamiento Digital de Señales

PARTE B – Captura de señal con DAQ + Análisis estadístico

Este script:
  1. Captura una señal del generador de señales biológicas usando la DAQ
  2. La guarda en formato .txt para poder usarla después
  3. Calcula los mismos estadísticos de la Parte A
  4. Genera gráficas e histogramas
  5. Compara con los resultados de la Parte A (señal de PhysioNet)

REQUISITOS:
  pip install nidaqmx
  python -m nidaqmx installdriver

Created on Thu Aug 21 08:36:05 2025
Modified for lab practice
@author: Carolina Corredor (base) + Lab Group (modifications)
=============================================================================
"""

import nidaqmx
from nidaqmx.constants import AcquisitionType
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from datetime import datetime

# =============================================================================
# PASO 1 – CONFIGURACIÓN DE LA CAPTURA
# =============================================================================
# IMPORTANTE: Ajusta estos parámetros según tu hardware y el tipo de señal
# que estés capturando del generador de señales biológicas

FS        = 1000        # Frecuencia de muestreo [Hz]
                        # Para ECG usa 1000 Hz, para otras señales ajusta según Nyquist
DURACION  = 10          # Duración de la captura [segundos]
                        # Usa 10 s para que sea comparable con la Parte A

DISPOSITIVO = 'Dev4/ai0'  # ← CAMBIA ESTO según tu DAQ
                          # Para ver el nombre correcto:
                          # 1. Abre NI MAX (Measurement & Automation Explorer)
                          # 2. Ve a "Devices and Interfaces"
                          # 3. Busca tu DAQ y anota el nombre (ej: Dev1, cDAQ1, etc)
                          # 4. Los canales son ai0, ai1, ai2... para entradas analógicas

# Rango de voltaje esperado (ajustar según tu señal)
V_MIN = -5             # Voltaje mínimo [V]
V_MAX =  5             # Voltaje máximo [V]

total_muestras = int(FS * DURACION)
print("="*60)
print("  CAPTURA DE SEÑAL FISIOLÓGICA CON DAQ")
print("="*60)
print(f"  Dispositivo      : {DISPOSITIVO}")
print(f"  Frecuencia       : {FS} Hz")
print(f"  Duración         : {DURACION} s")
print(f"  Total muestras   : {total_muestras}")
print(f"  Rango            : {V_MIN} a {V_MAX} V")
print("\nIniciando captura...")


# =============================================================================
# PASO 2 – CAPTURA CON LA DAQ
# =============================================================================
try:
    with nidaqmx.Task() as task:
        # Configurar canal con rango de voltaje
        task.ai_channels.add_ai_voltage_chan(
            DISPOSITIVO,
            min_val=V_MIN,
            max_val=V_MAX
        )
        
        # Configurar reloj de muestreo
        task.timing.cfg_samp_clk_timing(
            FS,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=total_muestras
        )
        
        # Capturar todas las muestras
        senal = task.read(number_of_samples_per_channel=total_muestras)
    
    print("✓ Captura completada exitosamente")
    
except Exception as e:
    print(f"\n✗ ERROR en la captura: {e}")
    print("\nPosibles soluciones:")
    print("  1. Verifica que la DAQ esté conectada")
    print("  2. Revisa el nombre del dispositivo en NI MAX")
    print("  3. Comprueba que el canal existe (ai0, ai1, etc.)")
    print("  4. Asegúrate de tener los drivers instalados")
    raise


# =============================================================================
# PASO 3 – GUARDAR LA SEÑAL EN ARCHIVO .TXT
# =============================================================================
# Crear nombre de archivo con timestamp para no sobrescribir capturas anteriores
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo_txt = f"senal_capturada_{timestamp}.txt"

# Guardar con formato de 2 columnas: tiempo [s] | amplitud [V]
t = np.arange(len(senal)) / FS
datos_guardar = np.column_stack((t, senal))

np.savetxt(
    archivo_txt,
    datos_guardar,
    fmt='%.6f',           # 6 decimales de precisión
    delimiter='\t',       # separado por tabulación
    header=f'Captura DAQ - {timestamp}\nFs={FS} Hz, Duracion={DURACION} s, Dispositivo={DISPOSITIVO}\nTiempo[s]\tAmplitud[V]',
    comments='# '
)

print(f"✓ Señal guardada en: {archivo_txt}")


# =============================================================================
# PASO 4 – CONVERTIR A NUMPY ARRAY Y VERIFICAR
# =============================================================================
senal = np.array(senal)  # asegurar que sea numpy array

print(f"\n  Muestras capturadas : {len(senal)}")
print(f"  Valor mínimo        : {senal.min():.4f} V")
print(f"  Valor máximo        : {senal.max():.4f} V")


# =============================================================================
# PASO 5 – ESTADÍSTICOS CON FUNCIONES PREDEFINIDAS
# =============================================================================
# Usamos NumPy/SciPy directamente (ya hiciste "desde cero" en la Parte A)

mu  = np.mean(senal)
s   = np.std(senal,  ddof=1)
v   = np.var(senal,  ddof=1)
cv  = (s / abs(mu)) * 100 if mu != 0 else np.inf
g1  = stats.skew(senal)
g2  = stats.kurtosis(senal)

print("\n" + "="*60)
print(f"  ESTADÍSTICOS – SEÑAL CAPTURADA ({DURACION} s)")
print("="*60)
print(f"  Media            : {mu:>12.6f} V")
print(f"  Desv. estándar   : {s:>12.6f} V")
print(f"  Varianza         : {v:>12.6f} V²")
print(f"  Coef. variación  : {cv:>12.4f} %")
print(f"  Asimetría        : {g1:>12.6f}")
print(f"  Curtosis         : {g2:>12.6f}")


# =============================================================================
# PASO 6 – GRÁFICAS
# =============================================================================

# ── Gráfica 1: Señal en el tiempo ───────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(13, 5))
fig1.suptitle(f"Señal capturada con DAQ  |  {DISPOSITIVO}  |  Fs={FS} Hz",
              fontsize=13, fontweight='bold')

ax1.plot(t, senal, color='#C62828', lw=0.8, label='Señal capturada')
ax1.axhline(mu,      color='black',   ls='--', lw=1.4,
            label=f'Media = {mu:.5f} V')
ax1.axhline(mu + s,  color='#2E7D32', ls=':',  lw=1.2,
            label=f'μ+σ = {mu+s:.4f}')
ax1.axhline(mu - s,  color='#2E7D32', ls=':',  lw=1.2,
            label=f'μ-σ = {mu-s:.4f}')
ax1.set_xlabel("Tiempo (s)", fontsize=11)
ax1.set_ylabel("Amplitud (V)", fontsize=11)
ax1.set_xlim(0, DURACION)
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"grafica_senal_capturada_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 2: Histograma + curva normal ────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(9, 5))
fig2.suptitle("Histograma - Señal capturada", fontsize=13, fontweight='bold')

conteos, bordes = np.histogram(senal, bins=60, density=True)
centros = (bordes[:-1] + bordes[1:]) / 2
ancho   = bordes[1] - bordes[0]

ax2.bar(centros, conteos, width=ancho*0.9, color='#EF5350',
        alpha=0.85, label='Datos capturados')

# Curva normal teórica
x_ref = np.linspace(senal.min(), senal.max(), 500)
ax2.plot(x_ref, stats.norm.pdf(x_ref, mu, s), 'k-', lw=2,
         label='Normal teórica')
ax2.axvline(mu, color='navy', ls='--', lw=1.5,
            label=f'Media = {mu:.3f}')

ax2.set_xlabel("Amplitud (V)", fontsize=11)
ax2.set_ylabel("Densidad de probabilidad", fontsize=11)
ax2.set_title(f"Asimetría={g1:.3f}  |  Curtosis={g2:.3f}", fontsize=10)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"grafica_histograma_capturado_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 3: Boxplot ───────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(5, 6))
fig3.suptitle("Box-plot – Señal capturada", fontsize=13, fontweight='bold')

ax3.boxplot(senal, patch_artist=True,
            boxprops=dict(facecolor='#FFCDD2'),
            medianprops=dict(color='red', lw=2),
            whiskerprops=dict(lw=1.2),
            flierprops=dict(marker='.', markersize=3, alpha=0.4))
ax3.set_ylabel("Amplitud (V)", fontsize=11)
ax3.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f"grafica_boxplot_capturado_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n✓ Todas las gráficas generadas y guardadas")


# =============================================================================
# PASO 7 – COMPARACIÓN CON PARTE A (OPCIONAL)
# =============================================================================
print("\n" + "="*60)
print("  COMPARACIÓN CON PARTE A")
print("="*60)
print("\nAhora compara estos estadísticos con los de la señal 0743")
print("de PhysioNet que usaste en la Parte A.")
print("\nPreguntas para el análisis:")
print("  • ¿Los valores son similares o muy diferentes?")
print("  • ¿Por qué crees que hay diferencias?")
print("    (señal sintética vs real, tipo de señal, duración, etc.)")
print("  • ¿La asimetría y curtosis indican distribuciones parecidas?")
print("="*60)