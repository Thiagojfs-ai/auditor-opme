import streamlit as st
import pandas as pd
import pdfplumber
import re
from datetime import datetime
from rapidfuzz import process, fuzz

st.set_page_config(layout="wide")
st.title("🩺 Auditor Inteligente de OPME")

def limpar_nome(nome):
    nome = str(nome).upper()
    nome = nome.replace("PARAFUSOS", "PARAFUSO")
    nome = nome.replace("RCL", "")
    return nome.strip()

def aplicar_depara(nome, depara):
    nome_limpo = limpar_nome(nome)
    return depara.get(nome_limpo, nome_limpo)

def extrair_dados(pdf):
    texto = ""
    with pdfplumber.open(pdf) as pdf_file:
        for page in pdf_file.pages:
            texto += page.extract_text() + "\n"

    dados = {}

    dados["nome"] = re.search(r"Nome (.+)", texto)
    dados["nome"] = dados["nome"].group(1) if dados["nome"] else ""

    dados["tuss"] = re.search(r"Cód\. TUSS: (\d+)", texto)
    dados["tuss"] = int(dados["tuss"].group(1)) if dados["tuss"] else None

    dados["crm"] = re.search(r"CRM (\d+)", texto)
    dados["crm"] = int(dados["crm"].group(1)) if dados["crm"] else None

    opmes = re.findall(r"([A-Z\s\(\)]+) RCL (\d+)", texto)
    dados["opme"] = [{"nome": o[0].strip(), "qtd": int(o[1])} for o in opmes]

    return dados

st.header("📄 Upload PDF")

pdf = st.file_uploader("Envie o PDF", type=["pdf"])

if pdf:
    dados = extrair_dados(pdf)

    st.subheader("📋 Dados extraídos")
    st.json(dados)

    st.success("App funcionando 🎉")
