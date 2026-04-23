import streamlit as st
import pandas as pd
import os
 
# Configuração inicial da página web
st.set_page_config(page_title="CNAK Vision - Sistema Unificado", layout="wide")
 
# ---------------------------------------------------------
# 1. GERENCIAMENTO DE ESTADO (Para navegar no mesmo arquivo)
# ---------------------------------------------------------
# Verifica se já existe uma 'página' salva na memória. Se não, inicia no 'cadastro'
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'cadastro'
 
# Funções que trocam o valor da página na memória
def mudar_para_cadastro():
    st.session_state.pagina_atual = 'cadastro'
 
def mudar_para_consulta():
    st.session_state.pagina_atual = 'consulta'
 
def mudar_para_sair():
    st.session_state.pagina_atual = 'sair'
 
nome_arquivo_csv = 'dados_usuarios.csv'
 
# ---------------------------------------------------------
# 2. TELA DE CADASTRO (Inclusão)
# ---------------------------------------------------------
if st.session_state.pagina_atual == 'cadastro':
    st.title("🏢 CNAK Vision - Módulo de Cadastro")
    st.write("Preencha os dados abaixo para registrar um novo usuário.")
 
    # Campos de entrada
    nome = st.text_input("Nome Completo:")
    email = st.text_input("E-mail:")
    cpf = st.text_input("CPF:")
 
    st.write("---")
    # Organiza os botões lado a lado
    col1, col2, col3 = st.columns(3)
 
    with col1:
        if st.button("💾 Salvar Cadastro", use_container_width=True):
            if nome and email and cpf:
                # Cria a nova linha e grava no arquivo CSV
                novo_dado = pd.DataFrame({'Nome': [nome], 'Email': [email], 'CPF': [cpf]})
                arquivo_existe = os.path.isfile(nome_arquivo_csv)
                novo_dado.to_csv(nome_arquivo_csv, mode='a', header=not arquivo_existe, index=False)
               
                st.success(f"Usuário '{nome}' cadastrado com sucesso!")
            else:
                st.warning("⚠️ Por favor, preencha todos os campos antes de salvar.")
 
    with col2:
        # O parâmetro 'on_click' chama a função para mudar a tela instantaneamente
        st.button("🔍 Ir para Consulta", on_click=mudar_para_consulta, use_container_width=True)
 
    with col3:
        st.button("🚪 Sair", on_click=mudar_para_sair, use_container_width=True)
 
 
# ---------------------------------------------------------
# 3. TELA DE CONSULTA E BUSCA (Filtros)
# ---------------------------------------------------------
elif st.session_state.pagina_atual == 'consulta':
    st.title("🏢 CNAK Vision - Módulo de Consulta")
 
    # Só tenta ler se o arquivo já existir
    if os.path.isfile(nome_arquivo_csv):
        df_usuarios = pd.read_csv(nome_arquivo_csv)
 
        st.subheader("🔍 Filtrar Usuário")
        termo_pesquisa = st.text_input("Digite o Nome ou CPF do lojista/visitante:")
       
        st.write("---")
        c1, c2, c3, c4 = st.columns(4)
 
        with c1:
            if st.button("🔍 Buscar", use_container_width=True):
                if termo_pesquisa:
                    # Aplica a filtragem buscando no Nome OU no CPF
                    tabela_filtrada = df_usuarios[
                        df_usuarios['Nome'].astype(str).str.contains(termo_pesquisa, case=False, na=False) |
                        df_usuarios['CPF'].astype(str).str.contains(termo_pesquisa, case=False, na=False)
                    ]
                    st.success("Resultado da Busca:")
                    st.dataframe(tabela_filtrada, use_container_width=True)
                else:
                    st.warning("⚠️ Digite um nome ou CPF antes de clicar em Buscar.")
 
        with c2:
            if st.button("🔄 Mostrar Todos", use_container_width=True):
                st.info(f"Mostrando todos os {df_usuarios.shape} registros cadastrados:")
                st.dataframe(df_usuarios, use_container_width=True)
 
        with c3:
            # Botão que devolve o usuário para a tela de cadastro
            st.button("➕ Cadastrar Novo", on_click=mudar_para_cadastro, use_container_width=True)
 
        with c4:
            st.button("🚪 Sair", on_click=mudar_para_sair, use_container_width=True)
 
    # Novo código para exclusão
    st.write("---")
    st.subheader("🗑️ Excluir Usuário")
    termo_exclusao = st.text_input("Digite o CPF do usuário a excluir:")
    if st.button("🗑️ Excluir"):
        if termo_exclusao:
            mask = df_usuarios['CPF'].astype(str).str.contains(termo_exclusao, case=False, na=False)
            if mask.any():
                df_usuarios = df_usuarios[~mask]
                df_usuarios.to_csv(nome_arquivo_csv, index=False)
                st.success(f"Usuário com CPF '{termo_exclusao}' excluído com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Nenhum usuário encontrado com esse CPF.")
        else:
            st.warning("⚠️ Digite um CPF antes de excluir.")
 
    else:
        st.warning("⚠️ Nenhum dado encontrado. O arquivo CSV ainda não foi criado.")
        st.button("➕ Voltar para Cadastro", on_click=mudar_para_cadastro)
 
 
# ---------------------------------------------------------
# 4. TELA DE SAÍDA (Encerramento)
# ---------------------------------------------------------
elif st.session_state.pagina_atual == 'sair':
    st.title("🚪 Sistema Encerrado")
    st.info("As atividades de segurança foram interrompidas. Você pode fechar esta aba.")
   
    if st.button("🔄 Reiniciar Sistema"):
        mudar_para_cadastro()
        # st.rerun() força a página a recarregar imediatamente
        st.rerun()