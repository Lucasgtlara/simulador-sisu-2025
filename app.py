import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Simulador Sisu 2025", page_icon="🎓", layout="wide")

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
    .ad-container {
        margin-top: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- NOVA FUNÇÃO DE ANÚNCIOS (AFILIADOS) ---
def exibir_anuncio(tipo, altura=None):
    """
    Exibe banners de Afiliado (Imagens clicáveis).
    Você deve trocar os LINKS e as IMAGENS pelos seus reais da Amazon/Shopee.
    """
    
    # --- DADOS DOS BANNERS (Configure aqui seus links de afiliado) ---
    # Notebook (Para o Topo)
    img_notebook = "https://m.media-amazon.com/images/I/713GzsYLBbL._AC_SX522_.jpg" 
    link_notebook = "https://amzn.to/3NSFItN" # <--- TROQUE AQUI
    
    # Kindle/Livros (Para a Lateral)
    img_kindle = "https://m.media-amazon.com/images/I/81Z2YCqqy-L._AC_SX679_.jpg"
    link_kindle = "https://amzn.to/3NqnjEI" # <--- TROQUE AQUI

    # Link Shopee (Para o Rodapé)
    link_shopee = "https://shopee.com.br/SEU_LINK_SHOPEE" # <--- TROQUE AQUI

    if tipo == 'topo':
        # Banner Horizontal (Ex: Promoção de Notebooks)
        # Usamos HTML/CSS para criar um banner responsivo e clicável
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
        # Texto simples com link (Menos intrusivo para o fim da página)
        html_code = f"""
        <div style="background-color:#fff3cd; padding: 15px; text-align: center; border-radius: 8px; border: 1px solid #ffeeba; font-family: sans-serif;">
            🎓 <b>Vai morar sozinho?</b> <br>
            <a href="{link_shopee}" target="_blank" style="color: #d35400; font-weight: bold; text-decoration: underline;">
                Veja nossa lista de itens essenciais de casa na Shopee!
            </a>
        </div>
        """
        altura = 80

    # Renderiza o componente HTML
    components.html(html_code, height=altura)

# --- 1. CARREGAMENTO DE DADOS (Robusto) ---
@st.cache_data
def carregar_dados():
    try:
        # Lê o CSV ignorando linhas ruins e usando UTF-8
        df = pd.read_csv("grades.csv", sep=";", header=None, on_bad_lines='skip', encoding='utf-8')
        
        indices_fixos = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        nomes_fixos = [
            "Codigo", "Curso", "Grau", "Turno", "Campus", "Cidade", "UF", "Universidade", "Sigla",
            "P_Redacao", "P_Matematica", "P_Linguagens", "P_Humanas", "P_Natureza"
        ]
        
        lista_dfs = []
        # Varredura das cotas no arquivo wide
        for i in range(21, df.shape[1], 5):
            if i + 2 < df.shape[1]:
                temp = df.iloc[:, indices_fixos + [i, i+2]].copy()
                temp.columns = nomes_fixos + ["Cota", "Nota_Corte"]
                temp = temp.dropna(subset=["Nota_Corte"])
                lista_dfs.append(temp)
        
        if lista_dfs:
            final = pd.concat(lista_dfs, ignore_index=True)
            # Converte colunas numéricas
            cols_num = ["P_Redacao", "P_Matematica", "P_Linguagens", "P_Humanas", "P_Natureza", "Nota_Corte"]
            for col in cols_num:
                final[col] = pd.to_numeric(final[col], errors='coerce')
            return final
        return None

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

df_sisu = carregar_dados()

# --- 2. BARRA LATERAL (Inputs e Anúncio Vertical) ---
with st.sidebar:
    st.header("📝 Suas Notas")
    n_red = st.number_input("Redação", 0, 1000, 760, step=10)
    n_mat = st.number_input("Matemática", 0, 1000, 740, step=10)
    n_lin = st.number_input("Linguagens", 0, 1000, 680, step=10)
    n_hum = st.number_input("Humanas", 0, 1000, 700, step=10)
    n_nat = st.number_input("Natureza", 0, 1000, 690, step=10)
    
    st.divider()
    
    # ANÚNCIO LATERAL (KINDLE/LIVROS)
    exibir_anuncio('lateral')

# --- 3. TELA PRINCIPAL ---
st.title("🎓 Simulador Sisu 2025")

# ANÚNCIO TOPO (NOTEBOOKS)
exibir_anuncio('topo')

if df_sisu is None:
    st.warning("⚠️ Base de dados não encontrada.")
    st.stop()

# --- FILTROS ---
with st.container(border=True):
    st.subheader("🔍 Filtros de Busca")
    busca_nome = st.text_input("Nome do Curso (ex: Direito, Medicina):")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        cotas = sorted(list(df_sisu['Cota'].unique()))
        idx = next((i for i, c in enumerate(cotas) if "Ampla" in str(c)), 0)
        cota_user = st.selectbox("Cota:", cotas, index=idx)
    with c2:
        ufs = ["Todos"] + sorted(list(df_sisu['UF'].unique()))
        uf_user = st.selectbox("Estado (UF):", ufs)
    with c3:
        unis = ["Todas"] + sorted(list(df_sisu['Sigla'].unique()))
        uni_user = st.selectbox("Universidade:", unis)

# ALERTA SOBRE A UNB (Específico para DF)
if uf_user == "DF" or (busca_nome and "unb" in busca_nome.lower()):
    st.warning("⚠️ **Aviso:** A UnB usa edital próprio ('Acesso Enem UnB') e não aparece nesta lista do Sisu. No DF, mostramos IFB e UnDF.")

# --- BOTÃO DE CÁLCULO ---
if st.button("Calcular Chances 🚀", type="primary", use_container_width=True):
    
    # Filtragem
    res = df_sisu[df_sisu['Cota'] == cota_user].copy()
    if uf_user != "Todos": res = res[res['UF'] == uf_user]
    if uni_user != "Todas": res = res[res['Sigla'] == uni_user]
    if busca_nome: res = res[res['Curso'].str.contains(busca_nome, case=False, na=False)]
    
    # Cálculo da Média Ponderada
    pesos = res['P_Redacao'] + res['P_Matematica'] + res['P_Linguagens'] + res['P_Humanas'] + res['P_Natureza']
    pesos = pesos.replace(0, 1)
    res['Sua_Media'] = ((n_red * res['P_Redacao']) + (n_mat * res['P_Matematica']) + (n_lin * res['P_Linguagens']) + (n_hum * res['P_Humanas']) + (n_nat * res['P_Natureza'])) / pesos
    
    # Aprovação e Diferença
    res['Aprovado'] = res['Sua_Media'] >= res['Nota_Corte']
    res['Diferenca'] = res['Sua_Media'] - res['Nota_Corte']
    res = res.sort_values(by=['Aprovado', 'Diferenca'], ascending=False)
    
    st.divider()
    
    if res.empty:
        st.info("Nenhum curso encontrado com esses filtros.")
    else:
        # --- RESULTADOS FREEMIUM ---
        st.success(f"Encontramos **{len(res)}** opções disponíveis!")
        
        # Mostra apenas o Top 3 (Isca)
        st.subheader("📋 Top 3 Resultados (Demonstração Grátis)")
        
        for i, row in res.head(3).iterrows():
            icon = "✅" if row['Aprovado'] else "❌"
            cor = "green" if row['Aprovado'] else "red"
            st.markdown(f"**{icon} {row['Curso']}** - {row['Sigla']} ({row['UF']})")
            st.write(f"Sua Média: **{row['Sua_Media']:.2f}** | Corte: {row['Nota_Corte']:.2f}")
            st.markdown("---")
            
        # --- ÁREA PREMIUM (BLOQUEADA) ---
        with st.container():
            st.markdown(f"""
            <div class="premium-box">
                <div class="premium-title">🔐 Desbloqueie o Resultado Completo</div>
                <p>Você encontrou <b>{len(res)} opções</b> de curso!</p>
                <p>Libere agora a <b>Lista Completa</b>, o <b>Gráfico Comparativo</b> e receba nosso <b>Guia Exclusivo de Matrícula</b> (Documentos e Prazos).</p>
                <p style="font-size:18px;">Valor simbólico: <b>R$ 6,90</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            c_pay1, c_pay2, c_pay3 = st.columns([1, 2, 1])
            with c_pay2:
                # SEU LINK REAL DO MERCADO PAGO
                st.link_button("⭐ QUERO MINHA APROVAÇÃO", "https://mpago.li/21eyi3e", use_container_width=True)
                st.caption("Pagamento seguro via Mercado Pago 🔒 - Acesso Imediato")
        
        st.divider()
        
        # ANÚNCIO RODAPÉ (SHOPEE)
        exibir_anuncio('rodape')

