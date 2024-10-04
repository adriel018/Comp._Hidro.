import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.special import ellipj

st.title("Exercício Prático Sobre Teorias de Onda")
st.markdown("Elaborado por <span style='color: red;'>Adriel Lucas F. de Oliveira</span>", unsafe_allow_html=True)

h = st.sidebar.number_input('Profundidade (m)', value=5.0, step=1.0, help='Valor da profundidade proposto no exercício')
Hs = st.sidebar.number_input('Altura Significativa da Onda (m)', value=3.0, step=1.0, help='Valor da altura significativa proposto no exercício')
T = st.sidebar.number_input('Período da Onda (s)', value=7.0, step=1.0, help='Valor do período proposto no exercício')
g = 9.81

def comprimento_onda(T, g):
    omega = 2 * np.pi / T
    k = omega**2 / g
    return 2 * np.pi / k

if st.sidebar.button('Calcular'):
    lambda_onda = comprimento_onda(T, g)
    N_Ursell = (Hs * lambda_onda**2) / h**3
    st.write(f'Número de Ursell: {N_Ursell:.2f}')

    if N_Ursell < 10:
        st.markdown("A Teoria <span style='color: red;'>de Stokes</span> é a mais adequada.", unsafe_allow_html=True)
    elif N_Ursell > 26:
        st.markdown("A Teoria <span style='color: red;'>Cnoidal</span> é a mais adequada.", unsafe_allow_html=True)
    else:
        st.markdown("Ambas as teorias (<span style='color: red;'>Stokes</span> e <span style='color: red;'>Cnoidal</span>) são adequadas para representar a onda.", unsafe_allow_html=True)

    x = np.linspace(0, 100, 1000)
    t = 20

    def elevacao_linear(x, t, Hs, lambda_onda):
        k = 2 * np.pi / lambda_onda
        omega = 2 * np.pi / T
        return (Hs / 2) * np.cos(k * x - omega * t)

    def elevacao_stokes(x, t, Hs, lambda_onda, h):
        k = 2 * np.pi / lambda_onda
        omega = 2 * np.pi / T
        # zeta_1 = (Hs / 2) * np.cos(k * x - omega * t)
        zeta_2 = (((np.pi * (Hs ** 2) * np.cosh(k * h)) / (8 * lambda_onda * (np.sinh(k * h) ** 3)))
                  * (2 + np.cosh(2 * k * h)) * np.cos(2 * (k * x - omega * t)))
        return zeta_2

    def elevacao_cnoidal(x, t, Hs, lambda_onda, m=0.2):
        k = 2 * np.pi / lambda_onda
        omega = 2 * np.pi / T
        u = k * x - omega * t
        sn, cn, dn, ph = ellipj(u, m)
        return Hs * sn

    elev_linear = elevacao_linear(x, t, Hs, lambda_onda)
    elev_stokes = elevacao_stokes(x, t, Hs, lambda_onda, h)
    elev_cnoidal = elevacao_cnoidal(x, t, Hs, lambda_onda)

    plt.figure(figsize=(10, 6))
    plt.plot(x, elev_linear, label='Teoria Linear', linestyle='--', color = 'black')
    plt.plot(x, elev_stokes, label='Teoria Stokes (2ª ordem)', linestyle='--', color = 'blue')
    plt.plot(x, elev_cnoidal, label='Teoria Cnoidal', linestyle='-', color = 'red')

    plt.title('Comparação das Elevações da Onda pelas Três Teorias')
    plt.xlabel('Posição (m)')
    plt.ylabel('Elevação da Onda (m)')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)
    plt.clf()
