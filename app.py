import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse # Necessário para o botão do WhatsApp

# Configuração da Página
st.set_page_config(page_title="Simulador Sisu 2025", page_icon="🎓", layout="wide")

# --- 0. VERIFICAÇÃO DE ACESSO (LINK SECRETO) ---
# Se o link tiver "?acesso=premium", a variável vira True e desbloqueia tudo
query_params = st.query_params
acesso_vip = False
if "acesso" in query_params and query_params["acesso"] == "premium":
    acesso_vip = True

# --- CSS PERSONALIZADO (Estilo do Premium e Anúncios) ---
st.markdown("""
<style>
    .premium-box {
        background-color: #d1e7dd;
        border: 2px solid #198754;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .premium-title {
        color: #198754;
        font-weight: bold;
        font-size: 22px;
        margin-bottom: 10px;
    }
    .vip-header {
        background-color: #198754;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .ad-container {
        margin-top: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- NOVA FUNÇÃO DE ANÚNCIOS (SEUS LINKS MANTIDOS) ---
def exibir_anuncio(tipo, altura=None):
    """
    Exibe banners de Afiliado (Imagens clicáveis).
    """
    
    # --- DADOS DOS BANNERS (SEUS LINKS ORIGINAIS) ---
    # Notebook (Para o Topo)
    img_notebook = "https://m.media-amazon.com/images/I/713GzsYLBbL._AC_SX522_.jpg" 
    link_notebook = "https://amzn.to/3NSFItN"
    
    # Kindle/Livros (Para a Lateral)
    img_kindle = "https://m.media-amazon.com/images/I/81Z2YCqqy-L._AC_SX679_.jpg"
    link_kindle = "https://amzn.to/3NqnjEI"

    # Link Shopee (Para o Rodapé)
    link_shopee = "https://shopee.com.br/SEU_LINK_SHOPEE" # <--- Se tiver link, troque aqui

    if tipo == 'topo':
        # Banner Horizontal (Ex: Promoção de Notebooks)
        html_code = f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <a href="{link_notebook}" target="_blank" style="text-decoration: none; width: 100%;">
                <div style="
                    width: 100%; 
                    height: 100px; 
                    background: linear-gradient(90deg, #232f3e 0%, #37475a 100%); 
                    border-radius: 8px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: space-between; 
                    padding: 0 20px; 
                    color: white; 
                    font-family: sans-serif;
                    box-sizing: border-box;">
                    
                    <div style="flex: 1;">
                        <span style="color: #ff9900; font-weight: bold; font-size: 14px;">OFERTA ESTUDANTE</span><br>
                        <span style="font-size: 18px; font-weight: bold;">Notebooks para a Faculdade</span><br>
                        <span style="font-size: 12px;">Parcele em até 10x sem juros</span>
                    </div>
                    
                    <div style="background: #ff9900; color: black; padding: 8px 15px; border-radius: 4px; font-weight: bold; font-size: 14px;">
                        Ver Ofertas >
                    </div>
                </div>
            </a>
            <div style="font-size: 10px; color: #aaa; margin-top: 4px;">Publicidade - Amazon</div>
        </div>
        """
        altura = 120 
        
    elif tipo == 'lateral':
        # Banner Vertical (Ex: Kindle)
        html_code = f"""
        <div style="text-align: center; background: #fff; padding: 15px; border: 1px solid #eee; border-radius: 8px; font-family: sans-serif;">
            <p style="font-weight: bold; color: #333; margin-bottom: 10px; font-size: 14px;">Material de Estudo</p>
            <a href="{link_kindle}" target="_blank" style="text-decoration: none;">
                <img src="{img_kindle}" style="width: 100%; max-width: 120px; height: auto; margin-bottom: 10px;">
                <div style="font-size: 13px; color: #555; margin-bottom: 10px;">Leve seus livros PDF para qualquer lugar.</div>
                <button style="background: #ff9900; color: #111; border: none; padding: 8px 15px; border-radius: 20px; font-weight: bold; cursor: pointer; width: 100%;">
                    Ver na Amazon
                </button>
            </a>
        </div>
        """
        altura = 320
        
    elif tipo == 'rodape':
        # Texto simples com link
        html_code = f"""
        <div style="background-color:#fff3cd; padding: 15px; text-align: center; border-radius: 8px; border: 1px solid #ffeeba; font-family: sans-serif;">
            🎓 <b>Vai morar sozinho?</b> <br>
            <a href="{link_shopee}" target="_blank" style="color: #d35400; font-weight: bold; text-decoration: underline;">
                Veja nossa lista de itens essenciais de casa na Shopee!
            </a>
        </div>
        """
        altura = 80

    components.html(html_code, height=altura)

# --- 1. CARREGAMENTO DE DADOS ---
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("grades.csv", sep=";", header=None, on_bad_lines='skip', encoding='utf-8')
        indices_fixos = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        nomes_fixos = ["Codigo", "Curso", "Grau", "Turno", "Campus", "Cidade", "UF", "Universidade", "Sigla", "P_Redacao", "P_Matematica", "P_Linguagens", "P_Humanas", "P_Natureza"]
        lista_dfs = []
        for i in range(21, df.shape[1], 5):
            if i + 2 < df.shape[1]:
                temp = df.iloc[:, indices_fixos + [i, i+2]].copy()
                temp.columns = nomes_fixos + ["Cota", "Nota_Corte"]
                temp = temp.dropna(subset=["Nota_Corte"])
                lista_dfs.append(temp)
        if lista_dfs:
            final = pd.concat(lista_dfs, ignore_index=True)
            cols_num = ["P_Redacao", "P_Matematica", "P_Linguagens", "P_Humanas", "P_Natureza", "Nota_Corte"]
