import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

# Configuração da Página
st.set_page_config(page_title="Investigador Histórico", page_icon="📅")

def traduzir(texto):
    try:
        return GoogleTranslator(source='en', target='pt').translate(texto)
    except:
        return texto

# Estilo CSS para melhorar o visual
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1A73E8; color: white; border-radius: 10px; }
    .main { background-color: #F0F2F5; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 Investigador Histórico Pro")
st.write("Descubra o dia da semana e fatos científicos de qualquer data.")

# Entrada de dados
data_input = st.text_input("Digite a data (DD/MM/AAAA)", placeholder="Ex: 20/07/1969")

if st.button("Analisar"):
    try:
        data_obj = datetime.strptime(data_input, "%d/%m/%Y")
        hoje = datetime.now()
        dias_pt = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        dia_semana = dias_pt[data_obj.weekday()]
        
        st.subheader(f"📅 Dia da semana: {dia_semana}")
        
        if data_obj > hoje:
            st.info(f"🔮 Esta data ainda vai acontecer! Em {data_input}, estaremos em uma {dia_semana.lower()}.")
        else:
            with st.spinner('Buscando na Wikipedia...'):
                dia, mes = str(data_obj.day).zfill(2), str(data_obj.month).zfill(2)
                url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{mes}/{dia}"
                res = requests.get(url, headers={'User-Agent': 'MeuApp/1.0'})
                
                if res.status_code == 200:
                    dados = res.json()
                    eventos = dados.get('selected', []) + dados.get('events', [])
                    
                    # Seção: No dia exato
                    st.markdown("### 📍 O que aconteceu exatamente neste dia:")
                    achou_ano = False
                    for e in eventos:
                        if str(e['year']) == str(data_obj.year):
                            st.success(traduzir(e['text']))
                            achou_ano = True
                    if not achou_ano: st.write("Nenhum registro específico deste ano exato.")

                    # Seção: Ciência
                    st.markdown("### 🔬 Destaques Científicos (Mesmo dia, outros anos):")
                    termos = ['moon', 'space', 'science', 'nasa', 'physics', 'orbit', 'discovery', 'tech']
                    count = 0
                    for e in eventos:
                        if any(t in e['text'].lower() for t in termos) and str(e['year']) != str(data_obj.year):
                            st.write(f"**{e['year']}**: {traduzir(e['text'])}")
                            count += 1
                            if count >= 5: break
                else:
                    st.error("Não foi possível conectar com a Wikipedia.")
    except:
        st.error("Por favor, use o formato DD/MM/AAAA (ex: 06/11/1982)")

# Botão de download do relatório (Opcional no Streamlit)
if data_input:
    st.download_button("Baixar Resultado em TXT", f"Relatório de {data_input}", file_name="historico.txt")
