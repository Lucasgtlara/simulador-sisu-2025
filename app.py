import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador Sisu 2025", page_icon="🎓", layout="wide")

# --- CSS PARA ESTILO (ANÚNCIOS E ÁREA PREMIUM) ---
st.markdown("""
<style>
    .ad-space {
        background-color: #f8f9fa;
        border: 2px dashed #ccc;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
        border-radius: 8px;
        color: #555;
    }
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
        font-size: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. CARREGAMENTO DOS DADOS ---
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("grades.csv", sep=";", header=None, on_bad_lines='skip', encoding='utf-8')
        
        indices_fixos = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        nomes_fixos = [
            "Codigo", "Curso", "Grau", "Turno", "Campus", "Cidade", "UF", "Universidade", "Sigla",
            "P_Redacao", "P_Matematica", "P_Linguagens", "P_Humanas", "P_Natureza"
        ]
        
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
            for col in cols_num:
                final[col] = pd.to_numeric(final[col], errors='coerce')
            return final
        return None

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

df_sisu = carregar_dados()

# --- 2. BARRA LATERAL (NOTAS + ANÚNCIO) ---
with st.sidebar:
    st.header("📝 Suas Notas")
    n_red = st.number_input("Redação", 0, 1000, 760, step=10)
    n_mat = st.number_input("Matemática", 0, 1000, 740, step=10)
    n_lin = st.number_input("Linguagens", 0, 1000, 680, step=10)
    n_hum = st.number_input("Humanas", 0, 1000, 700, step=10)
    n_nat = st.number_input("Natureza", 0, 1000, 690, step=10)
    
    st.divider()
    
    # ESPAÇO PARA ANÚNCIO LATERAL (Google Ads Vertical)
    st.markdown('<div class="ad-space">📢 <b>Google Ads</b><br>Anúncio Vertical Aqui</div>', unsafe_allow_html=True)

# --- 3. TELA PRINCIPAL ---
st.title("🎓 Simulador Sisu 2025")

# ESPAÇO PARA ANÚNCIO NO TOPO (Google Ads Horizontal)
st.markdown('<div class="ad-space">📢 <b>Publicidade</b><br>Anúncio Horizontal Aqui</div>', unsafe_allow_html=True)

if df_sisu is None:
    st.warning("⚠️ Base de dados não encontrada.")
    st.stop()

# --- FILTROS ---
with st.container(border=True):
    st.subheader("🔍 Filtros")
    busca_nome = st.text_input("Nome do Curso:")
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

# ALERTA UNB
if uf_user == "DF" or (busca_nome and "unb" in busca_nome.lower()):
    st.warning("⚠️ **Aviso:** A UnB usa edital próprio ('Acesso Enem UnB') e não aparece nesta lista. No DF, mostramos IFB e UnDF.")

# --- BOTÃO DE CÁLCULO ---
if st.button("Calcular Chances 🚀", type="primary", use_container_width=True):
    
    # Filtragem e Cálculo
    res = df_sisu[df_sisu['Cota'] == cota_user].copy()
    if uf_user != "Todos": res = res[res['UF'] == uf_user]
    if uni_user != "Todas": res = res[res['Sigla'] == uni_user]
    if busca_nome: res = res[res['Curso'].str.contains(busca_nome, case=False, na=False)]
    
    pesos = res['P_Redacao'] + res['P_Matematica'] + res['P_Linguagens'] + res['P_Humanas'] + res['P_Natureza']
    pesos = pesos.replace(0, 1)
    res['Sua_Media'] = ((n_red * res['P_Redacao']) + (n_mat * res['P_Matematica']) + (n_lin * res['P_Linguagens']) + (n_hum * res['P_Humanas']) + (n_nat * res['P_Natureza'])) / pesos
    res['Aprovado'] = res['Sua_Media'] >= res['Nota_Corte']
    res['Diferenca'] = res['Sua_Media'] - res['Nota_Corte']
    res = res.sort_values(by=['Aprovado', 'Diferenca'], ascending=False)
    
    st.divider()
    
    if res.empty:
        st.info("Nenhum curso encontrado.")
    else:
        # --- RESULTADOS (FREEMIUM) ---
        st.success(f"Encontramos **{len(res)}** opções!")
        
        # MOSTRA SÓ OS TOP 3 DE GRAÇA (Para gerar curiosidade)
        st.subheader("📋 Top 3 Resultados (Demonstração Grátis)")
        for i, row in res.head(3).iterrows():
            icon = "✅" if row['Aprovado'] else "❌"
            st.write(f"{icon} **{row['Curso']}** na {row['Sigla']} ({row['UF']}) - Média: {row['Sua_Media']:.2f}")
            
        st.markdown("---")
        
        # --- ÁREA PREMIUM (BLOQUEIO) ---
        with st.container():
            st.markdown("""
            <div class="premium-box">
                <div class="premium-title">🔐 Desbloqueie o Relatório Completo + Guia de Matrícula</div>
                <p>Você encontrou <b>""" + str(len(res)) + """ opções</b> de curso!</p>
                <p>Para ver a <b>lista completa</b>, o gráfico detalhado e receber nosso <b>Guia Exclusivo "Passo a Passo da Matrícula"</b> (Documentação, Prazos e Lista de Espera), libere o acesso agora.</p>
                <p>Valor simbólico: <b>R$ 9,90</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            c_pay1, c_pay2, c_pay3 = st.columns([1, 2, 1])
            with c_pay2:
                # BOTÃO COM SEU LINK DO MERCADO PAGO
                st.link_button("⭐ LIBERAR ACESSO AGORA", "https://mpago.li/21eyi3e", use_container_width=True)
                st.caption("Pagamento seguro via Mercado Pago 🔒")