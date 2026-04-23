# SISTEMA DE GESTÃO DE LOJISTAS

Aplicação web interativa para gerenciar dados de lojistas (proprietários de lojas) com CRUD completo usando **Streamlit** e **Pandas**.

## 📋 Requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install streamlit==1.28.1 pandas==2.1.3
```

## ▶️ Como executar

```bash
streamlit run cadastro.lojista.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

## 📊 Funcionalidades

### 🏠 Início
- Dashboard com estatísticas gerais
- Atalhos rápidos para as principais operações

### 📊 Listar
- Visualiza todos os lojistas em forma de tabela
- Opção para baixar dados em CSV

### ➕ Criar
- Formulário para adicionar novo lojista
- Validação automática de dados
- Prevenção de CNPJ duplicado

### 👁️ Visualizar
- Ver detalhes completos de um lojista selecionado
- Informações: nome, loja, CNPJ, email, telefone, endereço, data de cadastro

### ✏️ Editar
- Atualizar dados de um lojista existente
- Preserva data de criação original
- Validação de CNPJ duplicado

### 🗑️ Deletar
- Remover lojista com confirmação
- Mostra detalhes antes de deletar

### 🔍 Buscar
- Buscar por nome, loja ou CNPJ
- Resultados em tempo real

## 💾 Armazenamento

Os dados são armazenados em um arquivo CSV (`lojistas.csv`) na mesma pasta do projeto.

Campos armazenados:
- `id` - Identificador único (UUID)
- `nome` - Nome completo do proprietário
- `cnpj` - CNPJ da loja
- `endereco` - Endereço da loja
- `nome_loja` - Nome da loja
- `email` - Email de contato
- `telefone` - Telefone de contato
- `data_criacao` - Data/hora de criação

## 🔧 Validações

- **Nome**: Obrigatório, não vazio
- **CNPJ**: Obrigatório, não pode ser duplicado
- **Endereço**: Obrigatório, não vazio
- **Nome da Loja**: Obrigatório, não vazio
- **Email**: Obrigatório, deve conter @
- **Telefone**: Obrigatório, não vazio

## 📱 Interface

- Menu lateral para navegação rápida
- Formulários com validação integrada
- Tabelas interativas com dados dos lojistas
- Mensagens de sucesso/erro amigáveis
- Download de dados em CSV
- Design responsivo (funciona em desktop, tablet e mobile)

## 📝 Exemplo de Uso

1. Abra a aplicação: `streamlit run cadastro.lojista.py`
2. Clique em "➕ Criar" para adicionar um novo lojista
3. Preencha os dados:
   - Nome: João Silva
   - CNPJ: 12.345.678/0001-90
   - Loja: Silva Importados
   - Email: joao@silva.com
   - Telefone: (11) 98765-4321
   - Endereço: Rua das Flores, 123, São Paulo

4. Clique em "💾 Salvar"
5. Veja os dados em "📊 Listar"
6. Busque por "Silva" em "🔍 Buscar"

## 🐛 Solução de Problemas

### Erro: "streamlit: command not found"
Instale novamente: `pip install streamlit`

### Erro: "No module named 'pandas'"
Instale pandas: `pip install pandas`

### Arquivo não carrega
Verifique se está na pasta correta e se tem permissão de leitura/escrita

## 📄 Estrutura do Projeto

```
projeto/
├── cadastro.lojista.py    # Aplicação principal
├── requirements.txt        # Dependências
├── lojistas.csv           # Arquivo de dados (criado automaticamente)
└── README.md              # Este arquivo
```

## 👨‍💻 Autor

Educacional - 2026

## 📝 Licença

Aberto para uso educacional
