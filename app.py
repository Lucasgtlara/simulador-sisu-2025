import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador Sisu 2025", page_icon="🎓", layout="wide")

# --- 0. VERIFICAÇÃO DE ACESSO (LINK SECRETO) ---
query_params = st.query_params
acesso_vip = False
if "acesso" in query_params and query_params["acesso"] == "premium":
    acesso_vip = True

# --- CSS PERSONALIZADO ---
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
    .success-box {
        padding: 15px; 
        background-color: #d4edda; 
        color: #155724; 
        border-radius: 5px; 
        margin-bottom: 10px;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        padding: 15px; 
        background-color: #fff3cd; 
        color: #856404; 
        border-radius: 5px; 
        margin-bottom: 10px;
        border-left: 5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE ANÚNCIOS ---
def exibir_anuncio(tipo, altura=None):
    # SEUS LINKS DE AFILIADO
    img_notebook = "https://m.media-amazon.com/images/I/713GzsYLBbL._AC_SX522_.jpg" 
    link_notebook = "https://amzn.to/3NSFItN"
    
    img_kindle = "https://m.media-amazon.com/images/I/81Z2YCqqy-L._AC_SX679_.jpg"
    link_kindle = "https://amzn.to/3NqnjEI"

    link_shopee = "https://shopee.com.br/SEU_LINK_SHOPEE" 

    if tipo == 'topo':
        html_code = f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <a href="{link_notebook}" target="_blank" style="text-decoration: none; width: 100%;">
                <div style="width: 100%; height: 100px; background: linear-gradient(90deg, #232f3e 0%, #37475a 100%); border-radius: 8px; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; color: white; font-family: sans-serif; box-sizing: border-box;">
                    <div style="flex: 1;">
                        <span style="color: #ff9900; font-weight: bold; font-size: 14px;">OFERTA ESTUDANTE</span><br>
                        <span style="font-size: 18px; font-weight: bold;">Notebooks para a Faculdade</span><br>
                        <span style="font-size: 12px;">Parcele em até 10x sem juros</span>
                    </div>
                    <div style="background: #ff9900; color: black; padding: 8px 15px; border-radius: 4px; font-weight: bold; font-size: 14px;">Ver Ofertas ></div>
                </div>
            </a>
            <div style="font-size: 10px; color: #aaa; margin-top: 4px;">Publicidade - Amazon</div>
        </div>
        """
        altura = 120 
        
    elif tipo == 'lateral':
        html_code = f"""
        <div style="text-align: center; background: #fff; padding: 15px; border: 1px solid #eee; border-radius: 8px; font-family: sans-serif;">
            <p style="font-weight: bold; color: #333; margin-bottom: 10px; font-size: 14px;">Material de Estudo</p>
            <a href="{link_kindle}" target="_blank" style="text-decoration: none;">
                <img src="{img_kindle}" style="width: 100%; max-width: 120px; height: auto; margin-bottom: 10px;">
                <div style="font-size: 13px; color: #555; margin-bottom: 10px;">Leve seus livros PDF para qualquer lugar.</div>
                <button style="background: #ff9900; color: #111; border: none; padding: 8px 15px; border-radius: 20px; font-weight: bold; cursor: pointer; width: 100%;">Ver na Amazon</button>
            </a>
        </div>
        """
        altura = 320
        
    elif tipo == 'rodape':
        html_code = f"""
        <div style="background-color:#fff3cd; padding: 15px; text-align: center; border-radius: 8px; border: 1px solid #ffeeba; font-family: sans-serif;">
            🎓 <b>Vai morar sozinho?</b> <br>
            <a href="{link_shopee}" target="_blank" style="color: #d35400; font-weight: bold; text-decoration: underline;">Veja nossa lista de itens essenciais de casa na Shopee!</a>
        </div>
        """
        altura = 80

    components.html(html_code, height=altura)

# --- 1. CARREGAMENTO DE DADOS ---
@st.cache_data
def carregar_dados():
    try:
        # Lê o CSV
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
            for col in cols_num:
                final[col] = pd.to_numeric(final[col], errors='coerce')
            return final
        return None

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

df_sisu = carregar_dados()

# --- 2. BARRA LATERAL ---
with st.sidebar:
    if acesso_vip:
        st.success("💎 ACESSO VIP LIBERADO")
    st.header("📝 Suas Notas")
    n_red = st.number_input("Redação", 0, 1000, 760, step=10)
    n_mat = st.number_input("Matemática", 0, 1000, 740, step=10)
    n_lin = st.number_input("Linguagens", 0, 1000, 680, step=10)
    n_hum = st.number_input("Humanas", 0, 1000, 700, step=10)
    n_nat = st.number_input("Natureza", 0, 1000, 690, step=10)
    
    st.divider()
    exibir_anuncio('lateral')

# --- 3. TELA PRINCIPAL ---
if acesso_vip:
    st.markdown("""<div class="vip-header"><h1>🎓 Área do Aprovado (Premium)</h1><p>Bem-vindo! Aqui está o acesso completo aos dados e ao Guia.</p></div>""", unsafe_allow_html=True)
else:
    st.title("🎓 Simulador Sisu 2025")
    exibir_anuncio('topo')

if df_sisu is None:
    st.warning("⚠️ Base de dados não encontrada. Verifique se 'grades.csv' está no GitHub.")
    st.stop()

# Filtros
if acesso_vip:
    filtros_container = st.expander("⚙️ Alterar Filtros de Busca", expanded=False)
else:
    filtros_container = st.container(border=True)

with filtros_container:
    if not acesso_vip: st.subheader("🔍 Filtros de Busca")
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

if uf_user == "DF" or (busca_nome and "unb" in busca_nome.lower()):
    st.warning("⚠️ **Aviso:** A UnB usa edital próprio e não aparece nesta lista. No DF, mostramos IFB e UnDF.")

# Botão Calcular
txt_botao = "Atualizar Lista VIP 🔄" if acesso_vip else "Calcular Chances 🚀"
if st.button(txt_botao, type="primary", use_container_width=True):
    
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
        st.info("Nenhum curso encontrado com esses filtros.")
    else:
        if acesso_vip:
            # === ÁREA VIP COMPLETA ===
            st.success(f"Encontramos **{len(res)}** opções disponíveis para você!")
            
            tab1, tab2 = st.tabs(["📄 GUIA DA MATRÍCULA (PDF)", "📊 MEUS RESULTADOS COMPLETOS"])
            
            with tab1:
                # [ABA 1: DOWNLOAD DO GUIA]
                col_dload, col_share = st.columns(2)
                with col_dload:
                    try:
                        with open("manual_sisu.pdf", "rb") as pdf_file:
                            st.download_button("📥 Baixar PDF do Guia", data=pdf_file, file_name="Manual_Sisu.pdf", mime="application/pdf", use_container_width=True)
                    except:
                        st.error("⚠️ Arquivo 'manual_sisu.pdf' não encontrado no GitHub.")
                with col_share:
                    texto_zap = urllib.parse.quote(f"Passei em {len(res)} cursos! Veja suas chances: https://seusite.tech")
                    st.link_button("💚 Compartilhar no WhatsApp", f"https://wa.me/?text={texto_zap}", use_container_width=True)
                
                st.markdown("---")
                st.subheader("📖 Checklist Rápido (Resumo)")
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #198754;">
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li>✅ <b>RG e CPF</b> (Original e Cópia)</li>
                        <li>✅ <b>Histórico Escolar</b> Completo</li>
                        <li>✅ <b>Comprovante de Residência</b> (Atualizado)</li>
                        <li>✅ <b>Foto 3x4</b> Recente</li>
                    </ul>
                    <small><i>*Baixe o PDF acima para ver a lista completa de cotas!</i></small>
                </div>
                """, unsafe_allow_html=True)

            with tab2:
                # [ABA 2: RESULTADOS DIVIDIDOS]
                
                # Filtrar Aprovados
                aprovados = res[res['Aprovado'] == True]
                nao_aprovados = res[res['Aprovado'] == False]
                
                # --- PARTE 1: ONDE PASSOU ---
                if not aprovados.empty:
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>🏆 PARABÉNS! VOCÊ PASSA EM {len(aprovados)} CURSOS!</h3>
                        <p>Nesta lista abaixo, sua nota é <b>MAIOR</b> que a nota de corte.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(aprovados[['Curso', 'Universidade', 'Sigla', 'UF', 'Turno', 'Sua_Media', 'Nota_Corte', 'Diferenca']], hide_index=True, use_container_width=True)
                else:
                    st.warning("Com essas notas, você não passaria direto na chamada regular nestes cursos. Veja a Lista de Espera abaixo.")
                
                st.divider()
                
                # --- PARTE 2: LISTA DE ESPERA ---
                if not nao_aprovados.empty:
                    st.markdown(f"""
                    <div class="warning-box">
                        <h3>⚠️ LISTA DE ESPERA ({len(nao_aprovados)} opções)</h3>
                        <p>Nesta lista, sua nota ficou abaixo do corte. Veja a coluna 'Diferença' para saber o quão perto você está.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(nao_aprovados[['Curso', 'Universidade', 'Sigla', 'UF', 'Turno', 'Sua_Media', 'Nota_Corte', 'Diferenca']], hide_index=True, use_container_width=True)

        else:
            # === ÁREA GRÁTIS (SÓ MOSTRA 3) ===
            st.success(f"Encontramos **{len(res)}** opções disponíveis!")
            st.subheader("📋 Top 3 Resultados (Demonstração Grátis)")
            
            for i, row in res.head(3).iterrows():
                icon = "✅" if row['Aprovado'] else "❌"
                st.markdown(f"**{icon} {row['Curso']}** - {row['Sigla']} ({row['UF']})")
                st.write(f"Sua Média: **{row['Sua_Media']:.2f}** | Corte: {row['Nota_Corte']:.2f}")
                st.markdown("---")
            
            with st.container():
                st.markdown("""<div class="premium-box"><div class="premium-title">🔐 Desbloqueie o Resultado Completo</div><p>Libere a Lista Total e o Guia de Matrícula.</p><p style="font-size:18px;">Valor: <b>R$ 5,00</b></p></div>""", unsafe_allow_html=True)
                c_pay1, c_pay2, c_pay3 = st.columns([1, 2, 1])
                with c_pay2:
                    st.link_button("⭐ QUERO MINHA APROVAÇÃO", "https://mpago.li/21eyi3e", use_container_width=True)
            
            st.divider()
            exibir_anuncio('rodape')
