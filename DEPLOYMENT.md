# 🚀 Deployment Guide

Este guia explica como fazer o deploy da biblioteca `dockepy` para o PyPI usando GitHub Actions.

## 📋 Pré-requisitos

### 1. Token do PyPI
1. Acesse [PyPI](https://pypi.org) e faça login
2. Vá para **Account Settings** → **API tokens**
3. Crie um novo token com escopo **Entire account (all projects)**
4. Copie o token

### 2. Configurar Secret no GitHub
1. Vá para o repositório no GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. Nome: `PYPI_API_TOKEN`
5. Valor: Cole o token do PyPI

## 🎯 Como Fazer Deploy

### Opção 1: GitHub Actions (Recomendado)

1. **Acesse o repositório no GitHub**
2. Vá para a aba **Actions**
3. Selecione **Deploy to PyPI** no menu lateral
4. Clique em **Run workflow**
5. Configure os parâmetros:
   - **Version type**: Escolha o tipo de bump
     - `patch`: 0.1.0 → 0.1.1 (correções)
     - `minor`: 0.1.0 → 0.2.0 (novas funcionalidades)
     - `major`: 0.1.0 → 1.0.0 (mudanças que quebram compatibilidade)
   - **Skip tests**: Deixe `false` (recomendado)
6. Clique em **Run workflow**

### Opção 2: Teste Local

```bash
# Testar o processo de deploy localmente
./deploy-locally.sh patch

# Ou para versões maiores
./deploy-locally.sh minor
./deploy-locally.sh major
```

## 🔄 O que o Deploy Faz

### 1. Validação
- ✅ Executa todos os testes
- ✅ Roda linting (Black, Flake8, MyPy)
- ✅ Verifica se o código está limpo

### 2. Versionamento
- 📊 Lê a versão atual do `pyproject.toml`
- 🔢 Calcula a nova versão baseada no tipo escolhido
- 📝 Atualiza o `pyproject.toml` com a nova versão

### 3. Build
- 🔨 Constrói o pacote usando `python -m build`
- ✅ Verifica o pacote com `twine check`

### 4. Git Operations
- 📝 Cria commit com a nova versão
- 🏷️ Cria tag `v{versão}` (ex: `v0.1.1`)
- 📤 Faz push do commit e da tag

### 5. PyPI Upload
- 📦 Faz upload para o PyPI usando `twine`
- 🎉 Cria release no GitHub automaticamente

## 📦 Instalação da Nova Versão

Após o deploy, os usuários podem instalar a nova versão:

```bash
# Instalar a versão mais recente
pip install dockepy

# Ou instalar uma versão específica
pip install dockepy==0.1.1

# Atualizar para a versão mais recente
pip install --upgrade dockepy
```

## 🛡️ Segurança

- ✅ Token do PyPI é armazenado como secret
- ✅ Deploy só funciona com código que passa nos testes
- ✅ Versionamento automático previne erros manuais
- ✅ Build e verificação antes do upload

## 🚨 Troubleshooting

### Erro: "Token inválido"
- Verifique se o secret `PYPI_API_TOKEN` está configurado
- Confirme se o token do PyPI está ativo

### Erro: "Versão já existe"
- A versão já foi publicada no PyPI
- Escolha um tipo de bump diferente ou incremente manualmente

### Erro: "Testes falharam"
- Corrija os problemas nos testes
- Execute `./run-ci-locally.sh` para testar localmente

### Erro: "Linting falhou"
- Execute `black .` para formatar o código
- Corrija erros do Flake8 e MyPy

## 📚 Comandos Úteis

```bash
# Testar CI localmente
./run-ci-locally.sh

# Testar deploy localmente
./deploy-locally.sh patch

# Verificar versão atual
python -c "import toml; print(toml.load('pyproject.toml')['project']['version'])"

# Verificar pacote local
twine check dist/*

# Instalar versão local para teste
pip install dist/dockepy-*.whl
```

## 🎉 Resultado

Após o deploy bem-sucedido:
- 📦 Pacote disponível no PyPI
- 🏷️ Tag criada no GitHub
- 📋 Release criada automaticamente
- 🔗 Link direto para instalação: `pip install dockepy`