import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Transformações Geométricas", layout="centered")

# ======================================================
# RELATÓRIO
# ======================================================

st.title("📘 Relatório de Atividade Prática 2")
st.markdown("""
## Transformações Geométricas e Modelo de Câmera

Esta atividade implementa:

- Transformações 2D e 3D
- Translação e rotação
- Transformação perspectiva
- Modelo de câmera

---

### 🎯 Objetivo

Aplicar transformações geométricas e compreender como objetos 3D são projetados em 2D.

---

### 🌍 Aplicação Real

Esses conceitos são usados em:

- Jogos 3D 🎮  
- Computação gráfica (OpenGL, Unity)  
- Realidade virtual 🥽  
- Simulação e engenharia 🛠️  

Toda renderização 3D passa por essas etapas.
""")

# ======================================================
# MATRIZES
# ======================================================

def matrizT2d(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])


def matrizR2d(beta, cx=0, cy=0):
    cos = math.cos(beta)
    sin = math.sin(beta)

    return np.array([
        [cos, -sin, cx - cx*cos + cy*sin],
        [sin, cos, cy - cx*sin - cy*cos],
        [0, 0, 1]
    ])


def matrizT3d(tx, ty, tz):
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]
    ])


def matrizRx3d(beta):
    return np.array([
        [1,0,0,0],
        [0,math.cos(beta),-math.sin(beta),0],
        [0,math.sin(beta),math.cos(beta),0],
        [0,0,0,1]
    ])


def matrizRz3d(beta):
    return np.array([
        [math.cos(beta),-math.sin(beta),0,0],
        [math.sin(beta),math.cos(beta),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])


def matrizP(l):
    return np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,1/l,0]
    ])

# ======================================================
# TRANSFORMAÇÃO 2D
# ======================================================

def affine2d(img, M):
    h, w = img.shape
    result = np.zeros_like(img)

    for y in range(h):
        for x in range(w):
            p = np.array([x, y, 1])
            p2 = M @ p
            x2, y2 = int(p2[0]), int(p2[1])

            if 0 <= x2 < w and 0 <= y2 < h:
                result[y2, x2] = img[y, x]

    return result

# ======================================================
# IMAGEM BASE (RETÂNGULO)
# ======================================================

def imagem_base():
    img = np.zeros((500,500), dtype=np.uint8)

    img[200:300,150:350] = 255
    return img

# ======================================================
# 3D
# ======================================================

def affineN(M, pontos):
    return [M @ p for p in pontos]

# ======================================================
# MENU
# ======================================================

st.sidebar.title("Navegação")
opcao = st.sidebar.radio(
    "Escolha:",
    ["Transformações 2D", "Erro de Rotação", "Modelo de Câmera 3D"]
)

# ======================================================
# 1 - TRANSFORMAÇÕES 2D
# ======================================================

if opcao == "Transformações 2D":

    st.header("📐 Transformações 2D")

    img = imagem_base()

    st.subheader("Imagem Original")
    st.image(img, clamp=True)

    M = matrizT2d(50,80)
    img1 = affine2d(img, M)

    st.subheader("Translação (50,80)")
    st.image(img1, clamp=True)

    M2 = matrizT2d(-250,250)
    img2 = affine2d(img, M2)

    st.subheader("Translação (-250,250)")
    st.image(img2, clamp=True)

    M3 = matrizR2d(math.radians(90), 250, 250)
    img3 = affine2d(img, M3)

    st.subheader("Rotação 90°")
    st.image(img3, clamp=True)


# ======================================================
# 2 - ERRO DE ROTAÇÃO
# ======================================================

elif opcao == "Erro de Rotação":

    st.header("⚠️ Erro de Rotação")

    img = imagem_base()

    # Rotação única
    M = matrizR2d(math.radians(90),250,250)
    img90 = affine2d(img, M)

    # Múltiplas rotações
    img_iter = img.copy()
    for _ in range(9):
        M = matrizR2d(math.radians(10),250,250)
        img_iter = affine2d(img_iter, M)

    st.subheader("Rotação direta 90°")
    st.image(img90, clamp=True)

    st.subheader("9 rotações de 10°")
    st.image(img_iter, clamp=True)

    st.markdown("""
    🔎 Observação:

    O erro ocorre devido à discretização dos pixels.
    Pequenas transformações acumulam erro ao longo do tempo.
    """)


# ======================================================
# 3 - CÂMERA 3D
# ======================================================

elif opcao == "Modelo de Câmera 3D":

    st.header("📷 Modelo de Câmera 3D")

    pontos = [
        np.array([1,1,1,1]),
        np.array([1,1,-1,1]),
        np.array([1,-1,1,1]),
        np.array([1,-1,-1,1]),
        np.array([-1,1,1,1]),
        np.array([-1,1,-1,1]),
        np.array([-1,-1,1,1]),
        np.array([-1,-1,-1,1])
    ]

    # Transformações
    T = matrizT3d(8,-7,5)
    Rx = matrizRx3d(math.radians(60))
    Rz = matrizRz3d(math.radians(45))
    P = matrizP(-1)

    M = P @ Rz @ Rx @ T

    resultado = affineN(M, pontos)

    st.subheader("Pontos projetados (homogêneos)")
    for p in resultado:
        st.write(p)

    st.markdown("""
    ✔ Aplicamos composição de transformações  
    ✔ Simulação de câmera 3D  
    ✔ Projeção perspectiva  

    Esse processo é a base de qualquer engine 3D.
    """)
