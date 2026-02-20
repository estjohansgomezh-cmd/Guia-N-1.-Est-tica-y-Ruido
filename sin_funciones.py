# =============================================================================
# PRÁCTICA DE LABORATORIO – ANÁLISIS ESTADÍSTICO DE SEÑALES
# Universidad Militar Nueva Granada | Procesamiento Digital de Señales
#
# PARTE A – Estadísticos calculados DESDE CERO
#
# INSTRUCCIONES PARA CORRER EN SPYDER:
#   1. Pon este archivo, 0743.dat y 0743.hea en la MISMA carpeta
#   2. En Spyder cambia el "Working directory" a esa carpeta
#   3. Presiona F5 para correr
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# PASO 1 – LEER LA SEÑAL
# =============================================================================
# El archivo .dat tiene los dos canales (ECG y NIBP) mezclados y guardados
# como números enteros de 16 bits. numpy los lee con fromfile().
# reshape(-1, 2) los separa en 2 columnas: columna 0 = ECG, columna 1 = NIBP
# astype(float64) los convierte a decimales para poder hacer las operaciones

FS        = 1000    # frecuencia de muestreo: 1000 muestras por segundo
N_TOTAL   = 933820  # total de muestras en el archivo

# Parámetros de conversión (del archivo .hea):
# valor_físico = (valor_digital - baseline) / gain
GAIN_ECG  = 19288.4144;  BASE_ECG  = -22050   # resultado en mV
GAIN_NIBP = 594.1943;    BASE_NIBP = -53203   # resultado en mmHg

raw  = np.fromfile("0743.dat", dtype=np.int16).reshape(-1, 2).astype(np.float64)
ecg_completo  = (raw[:, 0] - BASE_ECG)  / GAIN_ECG
nibp_completo = (raw[:, 1] - BASE_NIBP) / GAIN_NIBP

print(f"Señal completa cargada: {N_TOTAL} muestras = {N_TOTAL/FS:.0f} segundos")


# =============================================================================
# PASO 2 – RECORTAR A 10 SEGUNDOS
# =============================================================================
# La señal tiene ~933 segundos, pero para graficar y analizar usamos solo
# los primeros 10 segundos.
#
# 10 segundos × 1000 muestras/segundo = 10000 muestras
#
# En Python, ecg[:10000] significa: "dame desde la muestra 0 hasta la 9999"
# Es como decirle a Excel: muéstrame solo las primeras 10000 filas

SEGUNDOS  = 10               # ← aquí puedes cambiar cuántos segundos quieres
N_VENTANA = SEGUNDOS * FS    # = 10000 muestras

ecg  = ecg_completo[:N_VENTANA]    # recorte de 10 s del ECG
nibp = nibp_completo[:N_VENTANA]   # recorte de 10 s del NIBP
t    = np.arange(N_VENTANA) / FS   # vector de tiempo: 0, 0.001, 0.002 ... 9.999

print(f"Ventana de análisis   : {N_VENTANA} muestras = {SEGUNDOS} segundos")
print(f"ECG  →  min={ecg.min():.3f} mV    max={ecg.max():.3f} mV")
print(f"NIBP →  min={nibp.min():.1f} mmHg  max={nibp.max():.1f} mmHg")


# =============================================================================
# PASO 3 – FUNCIONES ESTADÍSTICAS DESDE CERO
# =============================================================================
# Cada función recibe la señal como lista y calcula el estadístico
# usando solo operaciones básicas: suma, resta, multiplicación, división

def media(x):
    """
    MEDIA – valor promedio de la señal.
    Fórmula: μ = (1/N) · Σ xᵢ
    
    ¿Para qué sirve?
    Indica el 'nivel' central de la señal. En el ECG debería ser
    cercano a 0 porque la señal oscila alrededor de la línea base.
    En NIBP refleja la presión arterial media del paciente.
    """
    N    = len(x)
    suma = 0.0
    for xi in x:
        suma += xi          # suma todos los valores uno por uno
    return suma / N         # divide entre el total de muestras


def varianza(x):
    """
    VARIANZA – qué tan dispersos están los valores respecto a la media.
    Fórmula: s² = [1/(N-1)] · Σ (xᵢ - μ)²
    
    Usamos N-1 en vez de N (corrección de Bessel) para que el estimador
    sea insesgado cuando trabajamos con una muestra y no con toda la señal.
    
    ¿Para qué sirve?
    Una varianza alta significa que la señal tiene mucha amplitud
    (o mucho ruido). Una varianza baja indica señal más plana.
    """
    N  = len(x)
    mu = media(x)
    suma_cuad = 0.0
    for xi in x:
        suma_cuad += (xi - mu) ** 2   # (diferencia con la media) al cuadrado
    return suma_cuad / (N - 1)


def desv_estandar(x):
    """
    DESVIACIÓN ESTÁNDAR – raíz cuadrada de la varianza.
    Fórmula: s = √s²
    
    ¿Para qué sirve?
    Igual que la varianza pero en las mismas unidades que la señal
    (mV para ECG, mmHg para NIBP). Es más fácil de interpretar.
    """
    return varianza(x) ** 0.5


def coef_variacion(x):
    """
    COEFICIENTE DE VARIACIÓN – dispersión relativa en porcentaje.
    Fórmula: CV = (s / |μ|) × 100  [%]
    
    ¿Para qué sirve?
    Permite comparar la dispersión entre señales con distintas
    unidades o magnitudes. Un CV alto indica mucha variabilidad
    relativa respecto al valor promedio.
    """
    return (desv_estandar(x) / abs(media(x))) * 100.0


def asimetria(x):
    """
    ASIMETRÍA (Skewness) – inclinación de la distribución.
    Fórmula: g₁ = (1/N) · Σ [(xᵢ - μ)/s]³
    
    ¿Para qué sirve?
      g₁ > 0 → la cola se extiende hacia la derecha (picos positivos)
      g₁ < 0 → la cola se extiende hacia la izquierda
      g₁ ≈ 0 → distribución simétrica (como una campana)
    
    En el ECG se espera g₁ > 0 por los picos R que son muy positivos.
    """
    N  = len(x)
    mu = media(x)
    s  = desv_estandar(x)
    suma = 0.0
    for xi in x:
        suma += ((xi - mu) / s) ** 3
    return suma / N


def curtosis(x):
    """
    CURTOSIS – qué tan pronunciado es el pico de la distribución.
    Fórmula: g₂ = (1/N) · Σ [(xᵢ - μ)/s]⁴  - 3
    
    Se resta 3 para que una señal con distribución normal perfecta
    dé curtosis = 0 (convención de Fisher, la más usada en ingeniería).
    
    ¿Para qué sirve?
      g₂ > 0 → leptocúrtica: pico muy alto, valores extremos frecuentes
      g₂ < 0 → platicúrtica: distribución más plana que la normal
      g₂ = 0 → igual que la distribución normal
    
    El ECG tiene curtosis muy alta por los picos R estrechos y agudos.
    """
    N  = len(x)
    mu = media(x)
    s  = desv_estandar(x)
    suma = 0.0
    for xi in x:
        suma += ((xi - mu) / s) ** 4
    return (suma / N) - 3


def histograma_manual(x, n_bins=60):
    """
    HISTOGRAMA – distribución de frecuencias de los valores.
    Divide el rango de valores en 'cajitas' (bins) y cuenta cuántos
    valores caen en cada una.
    
    Devuelve:
      centros   → valor central de cada bin
      frec_rel  → fracción de muestras en cada bin (suma = 1)
    """
    x_min  = min(x)
    x_max  = max(x)
    ancho  = (x_max - x_min) / n_bins
    conteos = [0] * n_bins

    for xi in x:
        idx = int((xi - x_min) / ancho)
        if idx == n_bins:       # el valor máximo cae justo en el borde
            idx = n_bins - 1
        conteos[idx] += 1

    N        = len(x)
    centros  = [x_min + (i + 0.5) * ancho for i in range(n_bins)]
    frec_rel = [c / N for c in conteos]
    return centros, frec_rel


# =============================================================================
# PASO 4 – CALCULAR LOS ESTADÍSTICOS
# =============================================================================
# Convertimos los arrays de numpy a listas de Python para usar
# las funciones de arriba (que trabajan con bucles for)

ecg_lista  = ecg.tolist()
nibp_lista = nibp.tolist()

# ECG
mu_ecg  = media(ecg_lista)
s_ecg   = desv_estandar(ecg_lista)
v_ecg   = varianza(ecg_lista)
cv_ecg  = coef_variacion(ecg_lista)
g1_ecg  = asimetria(ecg_lista)
g2_ecg  = curtosis(ecg_lista)

# NIBP
mu_nibp  = media(nibp_lista)
s_nibp   = desv_estandar(nibp_lista)
v_nibp   = varianza(nibp_lista)
cv_nibp  = coef_variacion(nibp_lista)
g1_nibp  = asimetria(nibp_lista)
g2_nibp  = curtosis(nibp_lista)

# Imprimir resultados
print("\n" + "="*58)
print(f"  ESTADÍSTICOS – DESDE CERO  |  Ventana: {SEGUNDOS} s")
print("="*58)

print(f"\n  ECG (mV) — {N_VENTANA} muestras")
print(f"    Media            : {mu_ecg:>12.6f} mV")
print(f"    Desv. estándar   : {s_ecg:>12.6f} mV")
print(f"    Varianza         : {v_ecg:>12.6f} mV²")
print(f"    Coef. variación  : {cv_ecg:>12.4f} %")
print(f"    Asimetría        : {g1_ecg:>12.6f}")
print(f"    Curtosis         : {g2_ecg:>12.6f}")

print(f"\n  NIBP (mmHg) — {N_VENTANA} muestras")
print(f"    Media            : {mu_nibp:>12.4f} mmHg")
print(f"    Desv. estándar   : {s_nibp:>12.4f} mmHg")
print(f"    Varianza         : {v_nibp:>12.4f} mmHg²")
print(f"    Coef. variación  : {cv_nibp:>12.4f} %")
print(f"    Asimetría        : {g1_nibp:>12.6f}")
print(f"    Curtosis         : {g2_nibp:>12.6f}")


# =============================================================================
# PASO 5 – GRÁFICAS
# =============================================================================

# ── Gráfica 1: señales en el tiempo ─────────────────────────────────────────
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6), sharex=True)
fig1.suptitle(f"Señal 0743 – PhysioNet  |  Ventana de {SEGUNDOS} s  (Fs={FS} Hz)",
              fontsize=13, fontweight='bold')

ax1.plot(t, ecg, color='#C62828', lw=0.8, label='ECG')
ax1.axhline(mu_ecg,          color='black',   ls='--', lw=1.4,
            label=f'Media = {mu_ecg:.5f} mV')
ax1.axhline(mu_ecg + s_ecg,  color='#2E7D32', ls=':',  lw=1.2,
            label=f'μ+σ = {mu_ecg+s_ecg:.4f}')
ax1.axhline(mu_ecg - s_ecg,  color='#2E7D32', ls=':',  lw=1.2,
            label=f'μ-σ = {mu_ecg-s_ecg:.4f}')
ax1.set_ylabel("ECG (mV)", fontsize=11)
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.3)

ax2.plot(t, nibp, color='#1565C0', lw=0.8, label='NIBP')
ax2.axhline(mu_nibp,           color='black',   ls='--', lw=1.4,
            label=f'Media = {mu_nibp:.2f} mmHg')
ax2.axhline(mu_nibp + s_nibp,  color='#2E7D32', ls=':',  lw=1.2,
            label=f'μ+σ = {mu_nibp+s_nibp:.2f}')
ax2.axhline(mu_nibp - s_nibp,  color='#2E7D32', ls=':',  lw=1.2,
            label=f'μ-σ = {mu_nibp-s_nibp:.2f}')
ax2.set_xlabel("Tiempo (s)", fontsize=11)
ax2.set_ylabel("NIBP (mmHg)", fontsize=11)
ax2.legend(fontsize=8, loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("grafica1_senales_cero.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 2: histogramas desde cero ───────────────────────────────────────
c_ecg,  f_ecg  = histograma_manual(ecg_lista,  n_bins=60)
c_nibp, f_nibp = histograma_manual(nibp_lista, n_bins=60)

w_ecg  = c_ecg[1]  - c_ecg[0]
w_nibp = c_nibp[1] - c_nibp[0]

fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(13, 5))
fig2.suptitle(f"Histogramas – Desde cero  |  Ventana {SEGUNDOS} s",
              fontsize=13, fontweight='bold')

ax3.bar(c_ecg, f_ecg, width=w_ecg*0.9, color='#EF5350', alpha=0.85)
ax3.axvline(mu_ecg, color='black', lw=2, ls='--',
            label=f'Media = {mu_ecg:.5f}')
ax3.set_xlabel("Amplitud (mV)", fontsize=11)
ax3.set_ylabel("Frecuencia relativa", fontsize=11)
ax3.set_title(f"ECG  |  Asimetría={g1_ecg:.3f}  Curtosis={g2_ecg:.3f}",
              fontsize=10)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)

ax4.bar(c_nibp, f_nibp, width=w_nibp*0.9, color='#42A5F5', alpha=0.85)
ax4.axvline(mu_nibp, color='black', lw=2, ls='--',
            label=f'Media = {mu_nibp:.2f}')
ax4.set_xlabel("Amplitud (mmHg)", fontsize=11)
ax4.set_ylabel("Frecuencia relativa", fontsize=11)
ax4.set_title(f"NIBP  |  Asimetría={g1_nibp:.3f}  Curtosis={g2_nibp:.3f}",
              fontsize=10)
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("grafica2_histogramas_cero.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n✓ Listo. Revisa las gráficas en el panel de Spyder (o como archivos .png)")