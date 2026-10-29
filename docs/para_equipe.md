# Guia de Configuração e Manutenção do Repositório

Este documento orienta a configuração padronizada do ambiente de desenvolvimento em Python para todos os integrantes da equipe no Windows pelo terminal powershell.

## 1. Ambiente Virtual (.venv)

# Criar Ambiente Virtual <powershell>
> python -m venv .venv
**OBS: deve ser executado na pasta raíz 'C:\Users\...\previsao-demanda-ru-ufpb'**

# Liberar a Execução de Scripts Locais (se necessário) <powershell>
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ativar Ambiente Virtual <powershell>
> .venv\Scripts\Activate.ps1
**OBS: deve aparecer "(.venv)" ao inicio da ultima linha no terminal**


## 2. Gerenciamento, Atualização e Instalação de Bibliotecas (PIP)

# Verificar Pacotes Instalados (opcional) <powershell>
> pip list

# Cria e Atualiza 'requirements.txt' (ocasional) <powershell>
> pip freeze > requirements.txt
**OBS: deve ser executado apenas após a instalação de um novo pacote, pois atualizar o 'requirements.txt'**

# Instalar Pacotes (ocasional) <powershell>
> pip install <pacote> 
> # Exemplo: pip install pandas==2.2.2
**OBS: apenas após a instalação de um novo pacote**

# Atualizar Pacotes (opcional)
> pip install --upgrade <pacote>

# Desinstalar Pacotes (EVITAR)
> pip uninstall <pacote>

# Instalar Dependências do Projeto a partir do arquivo compartilhado (OBRIGATÓRIO)
> pip install -r requirements.txt
**OBS: sem isso voce nao consegue executar nada pois nao teria nenhum pacote instalado**