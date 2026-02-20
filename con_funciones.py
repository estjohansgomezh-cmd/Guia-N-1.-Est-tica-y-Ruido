# =============================================================================
# PRÁCTICA DE LABORATORIO – ANÁLISIS ESTADÍSTICO DE SEÑALES
# Universidad Militar Nueva Granada | Procesamiento Digital de Señales
#
# PARTE A – Estadísticos con FUNCIONES PREDEFINIDAS (NumPy + SciPy)
#
# INSTRUCCIONES PARA CORRER EN SPYDER:
#   1. Pon este archivo, 0743.dat y 0743.hea en la MISMA carpeta
#   2. En Spyder cambia el "Working directory" a esa carpeta
#   3. Presiona F5 para correr
# =============================================================================

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# =============================================================================
# PASO 1 – LEER LA SEÑAL
# =============================================================================
FS        = 1000    # frecuencia de muestreo: 1000 muestras por segundo
N_TOTAL   = 933820

GAIN_ECG  = 19288.4144;  BASE_ECG  = -22050
GAIN_NIBP = 594.1943;    BASE_NIBP = -53203

raw  = np.fromfile("0743.dat", dtype=np.int16).reshape(-1, 2).astype(np.float64)
ecg_completo  = (raw[:, 0] - BASE_ECG)  / GAIN_ECG
nibp_completo = (raw[:, 1] - BASE_NIBP) / GAIN_NIBP

print(f"Señal completa cargada: {N_TOTAL} muestras = {N_TOTAL/FS:.0f} segundos")


# =============================================================================
# PASO 2 – RECORTAR A 10 SEGUNDOS
# =============================================================================
# Si quieres cambiar la ventana, solo cambia este número:
SEGUNDOS  = 10
N_VENTANA = SEGUNDOS * FS    # 10 × 1000 = 10000 muestras

ecg  = ecg_completo[:N_VENTANA]
nibp = nibp_completo[:N_VENTANA]
t    = np.arange(N_VENTANA) / FS   # vector de tiempo en segundos

print(f"Ventana de análisis   : {N_VENTANA} muestras = {SEGUNDOS} segundos")


# =============================================================================
# PASO 3 – ESTADÍSTICOS CON FUNCIONES PREDEFINIDAS
# =============================================================================
# NumPy y SciPy tienen funciones optimizadas que hacen lo mismo que
# los bucles for del otro archivo, pero mucho más rápido.

# ── ECG ──────────────────────────────────────────────────────────────────────
mu_ecg  = np.mean(ecg)           # Media aritmética
s_ecg   = np.std(ecg,  ddof=1)   # Desviación estándar muestral
                                  # ddof=1 → usa N-1 (igual que desde cero)
v_ecg   = np.var(ecg,  ddof=1)   # Varianza muestral
cv_ecg  = (s_ecg / abs(mu_ecg)) * 100   # Coef. variación (no hay función
                                          # predefinida, se calcula así)
g1_ecg  = stats.skew(ecg)        # Asimetría – scipy.stats
g2_ecg  = stats.kurtosis(ecg)    # Curtosis exceso Fisher – scipy.stats
                                  # (normal → 0, igual que en el otro archivo)

# ── NIBP ─────────────────────────────────────────────────────────────────────
mu_nibp  = np.mean(nibp)
s_nibp   = np.std(nibp,  ddof=1)
v_nibp   = np.var(nibp,  ddof=1)
cv_nibp  = (s_nibp / abs(mu_nibp)) * 100
g1_nibp  = stats.skew(nibp)
g2_nibp  = stats.kurtosis(nibp)


# =============================================================================
# PASO 4 – MOSTRAR RESULTADOS
# =============================================================================
print("\n" + "="*58)
print(f"  ESTADÍSTICOS – NUMPY / SCIPY  |  Ventana: {SEGUNDOS} s")
print("="*58)

print(f"\n  ECG (mV) — {N_VENTANA} muestras")
print(f"    np.mean()        Media          : {mu_ecg:>12.6f} mV")
print(f"    np.std(ddof=1)   Desv. estándar : {s_ecg:>12.6f} mV")
print(f"    np.var(ddof=1)   Varianza       : {v_ecg:>12.6f} mV²")
print(f"    (s/|μ|)×100      Coef. variación: {cv_ecg:>12.4f} %")
print(f"    stats.skew()     Asimetría      : {g1_ecg:>12.6f}")
print(f"    stats.kurtosis() Curtosis       : {g2_ecg:>12.6f}")

print(f"\n  NIBP (mmHg) — {N_VENTANA} muestras")
print(f"    np.mean()        Media          : {mu_nibp:>12.4f} mmHg")
print(f"    np.std(ddof=1)   Desv. estándar : {s_nibp:>12.4f} mmHg")
print(f"    np.var(ddof=1)   Varianza       : {v_nibp:>12.4f} mmHg²")
print(f"    (s/|μ|)×100      Coef. variación: {cv_nibp:>12.4f} %")
print(f"    stats.skew()     Asimetría      : {g1_nibp:>12.6f}")
print(f"    stats.kurtosis() Curtosis       : {g2_nibp:>12.6f}")

# stats.describe() da todo de un solo golpe (bonus)
print("\n  stats.describe() ECG :")
d = stats.describe(ecg)
print(f"    N={d.nobs}  min={d.minmax[0]:.4f}  max={d.minmax[1]:.4f}")
print(f"    media={d.mean:.6f}  varianza={d.variance:.6f}")
print(f"    asimetría={d.skewness:.6f}  curtosis={d.kurtosis:.6f}")


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
plt.savefig("grafica1_senales_numpy.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 2: histogramas con np.histogram ──────────────────────────────────
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(13, 5))
fig2.suptitle(f"Histogramas – np.histogram  |  Ventana {SEGUNDOS} s",
              fontsize=13, fontweight='bold')

# np.histogram devuelve conteos y bordes; hacemos density=True para
# obtener densidad de probabilidad (área total = 1), igual que el método manual
for ax, señal, mu, s, g1, g2, color, unidad, nombre in [
    (ax3, ecg,  mu_ecg,  s_ecg,  g1_ecg,  g2_ecg,  '#EF5350', 'mV',   'ECG'),
    (ax4, nibp, mu_nibp, s_nibp, g1_nibp, g2_nibp, '#42A5F5', 'mmHg', 'NIBP'),
]:
    conteos, bordes = np.histogram(señal, bins=60, density=True)
    centros = (bordes[:-1] + bordes[1:]) / 2
    ancho   = bordes[1] - bordes[0]

    ax.bar(centros, conteos, width=ancho*0.9, color=color,
           alpha=0.85, label='Datos')

    # Curva normal teórica superpuesta para comparar la forma
    x_ref = np.linspace(señal.min(), señal.max(), 500)
    ax.plot(x_ref, stats.norm.pdf(x_ref, mu, s), 'k-', lw=2,
            label='Normal teórica')
    ax.axvline(mu, color='navy', ls='--', lw=1.5,
               label=f'Media = {mu:.3f}')

    ax.set_xlabel(f"Amplitud ({unidad})", fontsize=11)
    ax.set_ylabel("Densidad de probabilidad", fontsize=11)
    ax.set_title(f"{nombre}  |  Asim.={g1:.3f}  Kurt.={g2:.3f}", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("grafica2_histogramas_numpy.png", dpi=150, bbox_inches='tight')
plt.show()

# ── Gráfica 3: boxplots ──────────────────────────────────────────────────────
fig3, (ax5, ax6) = plt.subplots(1, 2, figsize=(9, 5))
fig3.suptitle(f"Box-plots  |  Ventana {SEGUNDOS} s", fontsize=13,
              fontweight='bold')

ax5.boxplot(ecg,  patch_artist=True,
            boxprops=dict(facecolor='#FFCDD2'),
            medianprops=dict(color='red', lw=2),
            whiskerprops=dict(lw=1.2),
            flierprops=dict(marker='.', markersize=2, alpha=0.3))
ax5.set_title("ECG", fontsize=11)
ax5.set_ylabel("Amplitud (mV)", fontsize=11)
ax5.grid(True, alpha=0.3, axis='y')

ax6.boxplot(nibp, patch_artist=True,
            boxprops=dict(facecolor='#BBDEFB'),
            medianprops=dict(color='blue', lw=2),
            whiskerprops=dict(lw=1.2),
            flierprops=dict(marker='.', markersize=2, alpha=0.3))
ax6.set_title("NIBP", fontsize=11)
ax6.set_ylabel("Amplitud (mmHg)", fontsize=11)
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig("grafica3_boxplots.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n✓ Listo. Revisa las gráficas en el panel de Spyder (o como archivos .png)")