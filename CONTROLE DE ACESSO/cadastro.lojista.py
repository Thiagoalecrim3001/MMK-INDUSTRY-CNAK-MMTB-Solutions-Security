"""
SISTEMA DE GESTÃO DE LOJISTAS - STREAMLIT + PANDAS
Aplicação web interativa com Streamlit e Pandas
Execute: streamlit run cadastro.lojista.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import os
import re


# ============================================================================
# CONFIGURAÇÃO
# ============================================================================
st.set_page_config(
    page_title="Gestão de Lojistas",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Arquivo CSV
ARQUIVO_CSV = 'lojistas.csv'


# ============================================================================
# CLASSE LOJISTA
# ============================================================================
class Lojista:
    """Representa um lojista com validação"""
    
    def __init__(self, nome, cnpj, endereco, nome_loja, email, telefone, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.nome_loja = nome_loja
        self.email = email
        self.telefone = telefone
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'nome_loja': self.nome_loja,
            'email': self.email,
            'telefone': self.telefone,
            'data_criacao': self.data_criacao
        }
    
    def validar(self):
        """Valida dados do lojista"""
        if not self.nome or len(self.nome.strip()) == 0:
            return False, "Nome é obrigatório"
        if not self.cnpj or len(self.cnpj.strip()) == 0:
            return False, "CNPJ é obrigatório"
        if not self.endereco or len(self.endereco.strip()) == 0:
            return False, "Endereço é obrigatório"
        if not self.nome_loja or len(self.nome_loja.strip()) == 0:
            return False, "Nome da Loja é obrigatório"
        if not self.email or len(self.email.strip()) == 0:
            return False, "Email é obrigatório"
        if '@' not in self.email:
            return False, "Email inválido"
        if not self.telefone or len(self.telefone.strip()) == 0:
            return False, "Telefone é obrigatório"
        return True, "OK"


# ============================================================================
# FUNÇÕES DE ARMAZENAMENTO (PANDAS + CSV)
# ============================================================================
def carregar_dataframe():
    """Carrega dados do CSV em DataFrame"""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV)
    else:
        return pd.DataFrame(columns=[
            'id', 'nome', 'cnpj', 'endereco', 'nome_loja', 'email', 'telefone', 'data_criacao'
        ])


def salvar_dataframe(df):
    """Salva DataFrame em CSV"""
    df.to_csv(ARQUIVO_CSV, index=False, encoding='utf-8')


def criar_lojista(nome, cnpj, endereco, nome_loja, email, telefone):
    """Cria novo lojista"""
    lojista = Lojista(nome, cnpj, endereco, nome_loja, email, telefone)
    valido, mensagem = lojista.validar()
    
    if not valido:
        return False, mensagem
    
    df = carregar_dataframe()
    
    # Verifica se CNPJ já existe
    if not df.empty and (df['cnpj'].str.lower() == cnpj.lower()).any():
        return False, "CNPJ já cadastrado!"
    
    novo_row = pd.DataFrame([lojista.to_dict()])
    df = pd.concat([df, novo_row], ignore_index=True)
    salvar_dataframe(df)
    
    return True, "Lojista criado com sucesso!"


def obter_todos_lojistas():
    """Retorna todos os lojistas"""
    df = carregar_dataframe()
    return df if not df.empty else None


def obter_lojista_por_id(id_lojista):
    """Obtém lojista pelo ID"""
    df = carregar_dataframe()
    if df.empty:
        return None
    resultado = df[df['id'] == id_lojista]
    return resultado.iloc[0] if not resultado.empty else None


def atualizar_lojista(id_lojista, nome, cnpj, endereco, nome_loja, email, telefone):
    """Atualiza um lojista"""
    lojista = Lojista(nome, cnpj, endereco, nome_loja, email, telefone, id_lojista)
    valido, mensagem = lojista.validar()
    
    if not valido:
        return False, mensagem
    
    df = carregar_dataframe()
    
    if (df['id'] == id_lojista).sum() == 0:
        return False, "Lojista não encontrado!"
    
    # Verifica se CNPJ já existe em outro lojista
    cnpj_existente = df[(df['cnpj'].str.lower() == cnpj.lower()) & (df['id'] != id_lojista)]
    if not cnpj_existente.empty:
        return False, "CNPJ já cadastrado para outro lojista!"
    
    # Preserva data de criação
    data_criacao = df[df['id'] == id_lojista]['data_criacao'].values[0]
    
    df.loc[df['id'] == id_lojista, 'nome'] = nome
    df.loc[df['id'] == id_lojista, 'cnpj'] = cnpj
    df.loc[df['id'] == id_lojista, 'endereco'] = endereco
    df.loc[df['id'] == id_lojista, 'nome_loja'] = nome_loja
    df.loc[df['id'] == id_lojista, 'email'] = email
    df.loc[df['id'] == id_lojista, 'telefone'] = telefone
    df.loc[df['id'] == id_lojista, 'data_criacao'] = data_criacao
    
    salvar_dataframe(df)
    return True, "Lojista atualizado com sucesso!"


def deletar_lojista(id_lojista):
    """Deleta um lojista"""
    df = carregar_dataframe()
    
    if (df['id'] == id_lojista).sum() == 0:
        return False, "Lojista não encontrado!"
    
    df = df[df['id'] != id_lojista]
    salvar_dataframe(df)
    
    return True, "Lojista deletado com sucesso!"


def buscar_lojistas(termo):
    """Busca lojistas por nome, loja ou CNPJ"""
    df = carregar_dataframe()
    if df.empty:
        return None
    
    termo_lower = termo.lower()
    mascara = (
        df['nome'].str.lower().str.contains(termo_lower, na=False) |
        df['nome_loja'].str.lower().str.contains(termo_lower, na=False) |
        df['cnpj'].str.lower().str.contains(termo_lower, na=False)
    )
    resultado = df[mascara]
    
    return resultado if not resultado.empty else None


# ============================================================================
# INTERFACE STREAMLIT
# ============================================================================
def main():
    # Sidebar com navegação
    with st.sidebar:
        st.header("📋 Menu")
        opcao = st.radio(
            "Selecione uma operação:",
            ["🏠 Início", "📊 Listar", "➕ Criar", "👁️ Visualizar", "✏️ Editar", "🗑️ Deletar", "🔍 Buscar"]
        )
    
    # Página inicial
    if opcao == "🏠 Início":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        df = obter_todos_lojistas()
        total = len(df) if df is not None else 0
        
        with col1:
            st.metric("Total de Lojistas", total)
        
        with col2:
            st.info("📦 Sistema de Gestão de Lojistas")
        
        with col3:
            st.success("✅ Pronto para usar")
        
        st.markdown("---")
        st.subheader("📌 Atalhos Rápidos")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Novo Lojista", use_container_width=True):
                st.session_state.page = "Criar"
                st.rerun()
        
        with col2:
            if st.button("📊 Ver Lista", use_container_width=True):
                st.session_state.page = "Listar"
                st.rerun()
        
        with col3:
            if st.button("🔍 Buscar", use_container_width=True):
                st.session_state.page = "Buscar"
                st.rerun()
    
    # Listar lojistas
    elif opcao == "📊 Listar":
        st.subheader("📊 Lista de Lojistas")
        
        df = obter_todos_lojistas()
        
        if df is None or df.empty:
            st.warning("⚠️ Nenhum lojista cadastrado")
        else:
            st.info(f"Total: {len(df)} lojista(s)")
            
            # Tabela com formatação
            df_display = df.copy()
            df_display = df_display[['nome', 'nome_loja', 'cnpj', 'email', 'telefone', 'data_criacao']]
            
            st.dataframe(df_display, use_container_width=True)
            
            # Download CSV
            csv = df.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=f"lojistas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Criar lojista
    elif opcao == "➕ Criar":
        st.subheader("➕ Criar Novo Lojista")
        
        with st.form("form_criar"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo:", key="novo_nome")
                cnpj = st.text_input("CNPJ:", key="novo_cnpj")
                email = st.text_input("Email:", key="novo_email")
            
            with col2:
                nome_loja = st.text_input("Nome da Loja:", key="novo_nome_loja")
                telefone = st.text_input("Telefone:", key="novo_telefone")
                endereco = st.text_area("Endereço:", key="novo_endereco", height=100)
            
            submitted = st.form_submit_button("💾 Salvar", use_container_width=True)
            
            if submitted:
                sucesso, mensagem = criar_lojista(nome, cnpj, endereco, nome_loja, email, telefone)
                if sucesso:
                    st.success(f"✅ {mensagem}")
                    st.balloons()
                else:
                    st.error(f"❌ {mensagem}")
    
    # Visualizar lojista
    elif opcao == "👁️ Visualizar":
        st.subheader("👁️ Visualizar Lojista")
        
        df = obter_todos_lojistas()
        
        if df is None or df.empty:
            st.warning("⚠️ Nenhum lojista cadastrado")
        else:
            lojista_nome = st.selectbox(
                "Selecione um lojista:",
                options=df['nome'].tolist(),
                format_func=lambda x: f"{x}"
            )
            
            if lojista_nome:
                lojista_dados = df[df['nome'] == lojista_nome].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Nome:**", lojista_dados['nome'])
                    st.write("**CNPJ:**", lojista_dados['cnpj'])
                    st.write("**Email:**", lojista_dados['email'])
                    st.write("**Telefone:**", lojista_dados['telefone'])
                
                with col2:
                    st.write("**Loja:**", lojista_dados['nome_loja'])
                    st.write("**Endereço:**", lojista_dados['endereco'])
                    st.write("**Data de Cadastro:**", lojista_dados['data_criacao'])
                    st.write("**ID:**", lojista_dados['id'][:8] + "...")
    
    # Editar lojista
    elif opcao == "✏️ Editar":
        st.subheader("✏️ Editar Lojista")
        
        df = obter_todos_lojistas()
        
        if df is None or df.empty:
            st.warning("⚠️ Nenhum lojista cadastrado")
        else:
            lojista_nome = st.selectbox(
                "Selecione um lojista para editar:",
                options=df['nome'].tolist(),
                format_func=lambda x: f"{x}",
                key="select_editar"
            )
            
            if lojista_nome:
                lojista = df[df['nome'] == lojista_nome].iloc[0]
                
                with st.form("form_editar"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nome = st.text_input("Nome Completo:", value=lojista['nome'])
                        cnpj = st.text_input("CNPJ:", value=lojista['cnpj'])
                        email = st.text_input("Email:", value=lojista['email'])
                    
                    with col2:
                        nome_loja = st.text_input("Nome da Loja:", value=lojista['nome_loja'])
                        telefone = st.text_input("Telefone:", value=lojista['telefone'])
                        endereco = st.text_area("Endereço:", value=lojista['endereco'], height=100)
                    
                    st.info(f"Data de Cadastro: {lojista['data_criacao']}")
                    
                    submitted = st.form_submit_button("💾 Atualizar", use_container_width=True)
                    
                    if submitted:
                        sucesso, mensagem = atualizar_lojista(
                            lojista['id'], nome, cnpj, endereco, nome_loja, email, telefone
                        )
                        if sucesso:
                            st.success(f"✅ {mensagem}")
                            st.rerun()
                        else:
                            st.error(f"❌ {mensagem}")
    
    # Deletar lojista
    elif opcao == "🗑️ Deletar":
        st.subheader("🗑️ Deletar Lojista")
        
        df = obter_todos_lojistas()
        
        if df is None or df.empty:
            st.warning("⚠️ Nenhum lojista cadastrado")
        else:
            lojista_nome = st.selectbox(
                "Selecione um lojista para deletar:",
                options=df['nome'].tolist(),
                format_func=lambda x: f"{x}",
                key="select_deletar"
            )
            
            if lojista_nome:
                lojista = df[df['nome'] == lojista_nome].iloc[0]
                
                st.warning(f"⚠️ Você está prestes a deletar: **{lojista['nome_loja']}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Nome:**", lojista['nome'])
                    st.write("**CNPJ:**", lojista['cnpj'])
                    st.write("**Email:**", lojista['email'])
                
                with col2:
                    st.write("**Loja:**", lojista['nome_loja'])
                    st.write("**Telefone:**", lojista['telefone'])
                    st.write("**Endereço:**", lojista['endereco'])
                
                if st.button("🗑️ Confirmar Exclusão", use_container_width=True, type="secondary"):
                    sucesso, mensagem = deletar_lojista(lojista['id'])
                    if sucesso:
                        st.success(f"✅ {mensagem}")
                        st.rerun()
                    else:
                        st.error(f"❌ {mensagem}")
    
    # Buscar lojista
    elif opcao == "🔍 Buscar":
        st.subheader("🔍 Buscar Lojista")
        
        termo_busca = st.text_input("Digite o nome, loja ou CNPJ para buscar:", placeholder="Ex: João, Loja Silva, 12.345.678...")
        
        if termo_busca:
            df_resultados = buscar_lojistas(termo_busca)
            
            if df_resultados is None:
                st.warning(f"⚠️ Nenhum lojista encontrado com '{termo_busca}'")
            else:
                st.success(f"✅ {len(df_resultados)} resultado(s) encontrado(s)")
                
                df_display = df_resultados[['nome', 'nome_loja', 'cnpj', 'email', 'telefone', 'data_criacao']]
                st.dataframe(df_display, use_container_width=True)
        else:
            st.info("💡 Digite algo para buscar")


if __name__ == "__main__":
    main()
