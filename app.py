import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="Simulador Sisu 2025", page_icon="🎓", layout="wide")

# --- VERIFICAÇÃO DE ACESSO (LINK SECRETO) ---
# Se o link tiver "?acesso=premium", a variável vira True
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
    .vip-header {
        background-color: #198754;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .vip-card {
        background-color: #f8f9fa;
        border-left: 5px solid #198754;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE ANÚNCIOS (Mantida) ---
def exibir_anuncio(tipo):
    # (Seus códigos de afiliado Amazon/Shopee aqui - mantive simplificado para focar na lógica VIP)
    if tipo == 'topo':
        return # Pode reativar depois
    # ... (Resto da lógica de anúncios se mantém igual)

# --- CARREGAMENTO DE DADOS ---
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
            for col in cols_num:
                final[col] = pd.to_numeric(final[col], errors='coerce')
            return final
    except Exception:
        return None
    return None

df_sisu = carregar_dados()

# --- BARRA LATERAL ---
with st.sidebar:
    if acesso_vip:
        st.success("💎 ACESSO VIP ATIVO")
    st.header("📝 Suas Notas")
    n_red = st.number_input("Redação", 0, 1000, 760, step=10)
    n_mat = st.number_input("Matemática", 0, 1000, 740, step=10)
    n_lin = st.number_input("Linguagens", 0, 1000, 680, step=10)
    n_hum = st.number_input("Humanas", 0, 1000, 700, step=10)
    n_nat = st.number_input("Natureza", 0, 1000, 690, step=10)

# --- TELA PRINCIPAL ---

# 1. CABEÇALHO DIFERENCIADO
if acesso_vip:
    st.markdown("""
    <div class="vip-header">
        <h1>🎓 Área do Aprovado (Premium)</h1>
        <p>Aqui está sua estratégia completa e a lista total de cursos!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title("🎓 Simulador Sisu 2025")

if df_sisu is None:
    st.warning("⚠️ Base de dados não encontrada.")
    st.stop()

# 2. FILTROS (Escondidos num expander se for VIP para limpar a tela)
if acesso_vip:
    with st.expander("⚙️ Alterar Filtros de Busca", expanded=False):
        filtros_container = st.container()
else:
    filtros_container = st.container(border=True)

with filtros_container:
    if not acesso_vip: st.subheader("🔍 Filtros")
    busca_nome = st.text_input("Nome do Curso:")
    c1, c2, c3 = st.columns(3)
    with c1:
        cotas = sorted(list(df_sisu['Cota'].unique()))
        idx = next((i for i, c in enumerate(cotas) if "Ampla" in str(c)), 0)
        cota_user = st.selectbox("Cota:", cotas, index=idx)
    with c2:
        ufs = ["Todos"] + sorted(list(df_sisu['UF'].unique()))
        uf_user = st.selectbox("Estado:", ufs)
    with c3:
        unis = ["Todas"] + sorted(list(df_sisu['Sigla'].unique()))
        uni_user = st.selectbox("Universidade:", unis)

# --- BOTÃO CALCULAR ---
botao_texto = "Atualizar Lista VIP 🔄" if acesso_vip else "Calcular Chances 🚀"
if st.button(botao_texto, type="primary", use_container_width=True):
    
    # Lógica de Cálculo
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
        st.success(f"Encontramos **{len(res)}** opções!")

        # --- MODO VIP: MOSTRA TUDO + MANUAL ---
        if acesso_vip:
            tab1, tab2 = st.tabs(["📄 GUIA DA MATRÍCULA (PDF)", "📋 LISTA COMPLETA DE CURSOS"])
            
            with tab1:
                col_dload, col_share = st.columns(2)
                
                # BOTÃO DOWNLOAD PDF
                with col_dload:
                    try:
                        with open("manual_sisu.pdf", "rb") as pdf_file:
                            st.download_button(
                                label="📥 Baixar PDF do Guia",
                                data=pdf_file,
                                file_name="Manual_Aprovacao_Sisu_2025.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    except:
                        st.error("Erro: Arquivo PDF não encontrado no servidor.")

                # BOTÃO COMPARTILHAR WHATSAPP
                with col_share:
                    texto_zap = urllib.parse.quote(f"Ei! Usei o Simulador Sisu e passei em {len(res)} cursos! Olha esse app: https://seusite.tech")
                    st.link_button("💚 Compartilhar no WhatsApp", f"https://wa.me/?text={texto_zap}", use_container_width=True)

                st.markdown("---")
                
                # CONTEÚDO DO GUIA NA TELA (Texto do PDF)
                st.subheader("📖 Manual da Aprovação e Matrícula")
                
                with st.expander("📂 1. Checklist de Documentos (Obrigatório)", expanded=True):
                    st.markdown("""
                    **Comece a separar isso hoje[cite: 15]:**
                    * [ ] **RG e CPF:** Original e Cópia[cite: 16].
                    * [ ] **Certificado de Conclusão do Ensino Médio:** Diploma oficial[cite: 17].
                    * [ ] **Histórico Escolar Completo:** Notas do 1º ao 3º ano[cite: 18].
                    * [ ] **Comprovante de Residência:** Máx. 90 dias[cite: 19].
                    * [ ] **Foto 3x4 Recente**[cite: 20].
                    * [ ] **Quitação Eleitoral:** App e-Título[cite: 21].
                    * [ ] **Reservista:** Para homens > 18 anos[cite: 22].
                    """)
                
                with st.expander("⚠️ 2. Regras Especiais de Cotas"):
                    st.warning("Se você passou por cotas, atenção redobrada! [cite: 23]")
                    st.markdown("""
                    **Escola Pública:** Declaração de que cursou **integralmente** em escola pública (bolsista de particular não conta) [cite: 25-27].
                    
                    **Cota de Renda:**
                    * **CadÚnico:** Se tiver, facilita 90%[cite: 29].
                    * **Sem CadÚnico:** Extratos bancários e holerites de **todos** da casa [cite: 30-31].
                    """)
                
                with st.expander("🔥 3. O Segredo da Lista de Espera"):
                    st.markdown("""
                    **O "Pulo do Gato"[cite: 35]:**
                    Não basta clicar no botão do site do Sisu![cite: 38].
                    
                    1. Manifeste interesse no site do Sisu.
                    2. **Confirmação Dupla:** Entre no site da **PRÓPRIA UNIVERSIDADE** e confirme interesse lá também[cite: 42].
                    
                    *Muitas faculdades (UFRJ, UnB, etc.) eliminam quem não faz esse segundo cadastro [cite: 43-44].*
                    """)
            
            with tab2:
                # LISTA COMPLETA (Sem bloqueio)
                st.dataframe(
                    res[['Curso', 'Universidade', 'Sigla', 'UF', 'Turno', 'Sua_Media', 'Nota_Corte', 'Diferenca']],
                    hide_index=True,
                    use_container_width=True
                )

        # --- MODO GRÁTIS: MOSTRA SÓ 3 E BLOQUEIA ---
        else:
            st.subheader("📋 Top 3 Resultados (Demonstração)")
            for i, row in res.head(3).iterrows():
                icon = "✅" if row['Aprovado'] else "❌"
                st.write(f"{icon} **{row['Curso']}** - {row['Sigla']} ({row['Sua_Media']:.2f})")
            
            st.markdown("---")
            
            # BLOQUEIO DE VENDA
            with st.container():
                st.markdown(f"""
                <div class="premium-box">
                    <div class="premium-title">🔐 Desbloqueie a Lista Completa</div>
                    <p>Encontramos <b>{len(res)} opções</b> para você!</p>
                    <p>Libere a lista total, o download do <b>Manual de Matrícula</b> e as dicas de Lista de Espera.</p>
                    <p><b>Apenas R$ 5,00</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                email = st.text_input("📧 Seu e-mail:", placeholder="Para receber o acesso VIP")
                if email:
                    st.link_button("⭐ LIBERAR TUDO AGORA", "https://mpago.li/21eyi3e", use_container_width=True)
                else:
                    st.caption("Digite seu e-mail para habilitar a compra.")
