# Anaconda Prompt inicia em CWINDOWSsystem32

## 📊 Informações
- **Número:** #111
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** a2b46b23-7a85-4d1f-8ccf-e442c223cf68
- **Criada em:** 2025-10-21 02:53:32
- **Atualizada em:** 2025-10-21 03:17:55
- **Total de mensagens:** 16
- **Resumo:** Anaconda prompt inicia com: C:\WINDOWS\system32>mamba activate C:\Anaconda3

(base) C:\WINDOWS\syste...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-21 02:53:34)* *[deepseek-chat]*

Anaconda prompt inicia com: C:\WINDOWS\system32>mamba activate C:\Anaconda3

(base) C:\WINDOWS\system32> ;  porquê?

---

### 🤖 DeepSeek *(2025-10-21 02:53:34)* *[deepseek-chat]*

O problema que você está descrevendo é comum e tem algumas causas possíveis:

## **Por que o Anaconda Prompt inicia em `C:\WINDOWS\system32`?**

### **Causas principais:**

1. **Configuração padrão do atalho**: O atalho do Anaconda Prompt pode estar configurado para iniciar no diretório do sistema
2. **Instalação recente**: Após uma nova instalação ou atualização
3. **Permissões**: O prompt está sendo executado com privilégios administrativos

### **Soluções:**

## **1. Corrigir via Propriedades do Atalho**
- Clique com o botão direito no atalho do **Anaconda Prompt**
- Selecione **Propriedades**
- Na aba **Atalho**, verifique o campo **Iniciar em**
- Altere para: `%USERPROFILE%` ou `C:\`
- Clique em **OK**

## **2. Criar um novo atalho personalizado**
```cmd
%windir%\System32\cmd.exe "/K" C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
```

## **3. Verificar variáveis de ambiente**
- Pressione `Win + R`, digite `sysdm.cpl`
- Clique em **Variáveis de Ambiente**
- Verifique se `C:\Anaconda3` e `C:\Anaconda3\Scripts` estão no **PATH**

## **4. Solução rápida dentro do prompt**
Uma vez aberto, você pode simplesmente navegar para seu diretório preferido:
```cmd
cd %USERPROFILE%
# ou
cd C:\seus\projetos
```

## **Observação importante:**
O fato de mostrar `(base)` indica que o ambiente **conda base está ativado corretamente**, então a funcionalidade principal do Anaconda está funcionando. A questão é apenas o diretório inicial.

A solução mais simples é geralmente a **opção 1** (alterar as propriedades do atalho).

---

### 👤 Utilizador *(2025-10-21 02:55:17)* *[deepseek-chat]*

a questão tem a ver com: mamba activate C:\Anaconda3

---

### 🤖 DeepSeek *(2025-10-21 02:55:17)* *[deepseek-chat]*

Excelente observação! Você identificou o cerne do problema. Vamos analisar isso:

## **Análise do comando `mamba activate C:\Anaconda3`**

### **O que está acontecendo:**

1. **Ativação explícita do caminho completo**: O comando está especificando o caminho completo `C:\Anaconda3` em vez de usar a ativação normal do ambiente base

2. **Possíveis causas**:
   - **Configuração incorreta** no atalho ou script de inicialização
   - **Problema na instalação** do Mamba/Conda
   - **Variáveis de ambiente** configuradas incorretamente

### **Como deveria ser:**
Normalmente, o Anaconda Prompt deveria executar apenas:
```cmd
conda activate base
# ou
mamba activate base
```

### **Soluções:**

## **1. Corrigir o script de inicialização do Anaconda Prompt**
- Navegue até: `C:\Anaconda3\Scripts\`
- Encontre o arquivo `activate.bat` ou `anaconda-prompt-init.bat`
- Verifique se há uma linha com `mamba activate C:\Anaconda3` e substitua por `mamba activate base`

## **2. Verificar o atalho do Anaconda Prompt**
- **Botão direito** → **Propriedades**
- No campo **Destino**, deveria estar algo como:
```
%windir%\System32\cmd.exe "/K" C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
```

## **3. Verificar a instalação do Mamba**
```cmd
mamba info --base
```
Isso deve retornar `C:\Anaconda3` - se não retornar, há problema na configuração.

## **4. Solução alternativa - Reinstalar o Mamba**
```cmd
conda install mamba -n base -c conda-forge
# ou
conda update --all
```

## **5. Verificar variáveis de ambiente**
- `CONDA_EXE` deveria apontar para `C:\Anaconda3\Scripts\conda.exe`
- `CONDA_PREFIX` deveria ser `C:\Anaconda3`

### **Teste rápido:**
Abra um **CMD normal** (não Anaconda Prompt) e execute:
```cmd
C:\Anaconda3\Scripts\activate.bat
```
Isso deve ativar o ambiente base corretamente.

O problema está provavelmente na forma como o Mamba foi instalado ou configurado para inicializar com caminho absoluto em vez do ambiente padrão.

---

### 👤 Utilizador *(2025-10-21 02:57:17)* *[deepseek-chat]*

a questão tem a ver com: mamba activate C:\Anaconda3; e não com (base), porque é isso que se pretende

---

### 🤖 DeepSeek *(2025-10-21 02:57:17)* *[deepseek-chat]*

Entendo! O problema é que o comando `mamba activate C:\Anaconda3` está sendo executado automaticamente ao iniciar, em vez de simplesmente ativar o ambiente base padrão.

## **Causas possíveis:**

### **1. Script de inicialização modificado**
Verifique o script de inicialização do Anaconda Prompt:
- Localize: `C:\Anaconda3\Scripts\activate.bat`
- Ou: `C:\Anaconda3\condabin\conda.bat`

### **2. Variável de ambiente CONDA_AUTO_ACTIVATE_BASE**
```cmd
echo %CONDA_AUTO_ACTIVATE_BASE%
```
Se estiver definida como `false`, pode estar forçando ativação manual.

### **3. Configuração do conda**
```cmd
conda config --show
```
Verifique as configurações relacionadas à auto-ativação.

## **Soluções:**

### **Solução 1: Verificar e corrigir o atalho**
- **Propriedades do atalho** → Campo "Destino" deve ser:
```cmd
%windir%\System32\cmd.exe "/K" C:\Anaconda3\Scripts\activate.bat
```
**NÃO** deve incluir `mamba activate C:\Anaconda3`

### **Solução 2: Reconfigurar auto-ativação**
```cmd
conda config --set auto_activate_base true
```

### **Solução 3: Verificar scripts de inicialização**
- Verifique `C:\Anaconda3\Scripts\activate.bat`
- Deve conter apenas a lógica padrão de ativação

### **Solução 4: Reinstalar/Reparar Anaconda**
Se as soluções acima não funcionarem, considere reparar a instalação.

O comportamento normal deve ser apenas `(base)` sem o comando `mamba activate` explícito aparecer.

---

### 👤 Utilizador *(2025-10-21 03:04:10)* *[deepseek-chat]*

eu tenho auto_activate_base: true; o atalho é: %WINDIR%\System32\cmd.exe "/K" C:\Anaconda3\Scripts\activate.bat C:\Anaconda3; activate.bat contem: @REM Copyright (C) 2021 QuantStack
@REM SPDX-License-Identifier: BSD-3-Clause

@CALL "%~dp0..\condabin\mamba_hook.bat"
mamba activate %*

---

### 🤖 DeepSeek *(2025-10-21 03:04:10)* *[deepseek-chat]*

Agora identifiquei o problema! O script `activate.bat` está configurado para usar **mamba** em vez do conda padrão.

## **Análise do problema:**

O seu `activate.bat` contém:
```batch
@CALL "%~dp0..\condabin\mamba_hook.bat"
mamba activate %*
```

Isso força o uso do `mamba activate C:\Anaconda3` em vez da ativação silenciosa do ambiente base.

## **Soluções:**

### **Opção 1: Modificar o activate.bat (Recomendado)**
Altere o conteúdo do `C:\Anaconda3\Scripts\activate.bat` para:
```batch
@CALL "%~dp0..\condabin\conda.bat"
@CALL "%~dp0..\condabin\mamba_hook.bat"
conda activate %*
```

### **Opção 2: Usar o conda.bat diretamente no atalho**
Mude o atalho para:
```
%WINDIR%\System32\cmd.exe "/K" C:\Anaconda3\condabin\conda.bat
```

### **Opção 3: Criar um activate.bat personalizado**
Crie um novo arquivo `activate.bat` com:
```batch
@CALL "%~dp0..\condabin\conda.bat"
@CALL conda activate base
```

## **Explicação:**
- O `mamba_hook.bat` é necessário para manter a compatibilidade com mamba
- Mas o comando de ativação deve ser `conda activate` para o comportamento padrão
- O `%*` passa argumentos, mas sem argumentos ele deve ativar o ambiente base silenciosamente

A **Opção 1** é a mais limpa pois mantém a funcionalidade do mamba enquanto corrige o comportamento de inicialização.

---

### 👤 Utilizador *(2025-10-21 03:08:27)* *[deepseek-chat]*

Com a Opção 1; agora dá: usage: conda-script.py [-h] [-v] [--no-plugins] [-V] COMMAND ...

conda is a tool for managing and deploying applications, environments and packages.

options:
  -h, --help            Show this help message and exit.
  -v, --verbose         Can be used multiple times. Once for detailed output, twice for INFO logging, thrice for DEBUG
                        logging, four times for TRACE logging.
  --no-plugins          Disable all plugins that are not built into conda.
  -V, --version         Show the conda version number and exit.

commands:
  The following built-in and plugins subcommands are available.

  COMMAND
    activate            Activate a conda environment.
    build               Build conda packages from a conda recipe.
    clean               Remove unused packages and caches.
    commands            List all available conda subcommands (including those from plugins). Generally only used by
                        tab-completion.
    compare             Compare packages between conda environments.
    config              Modify configuration values in .condarc.
    content-trust       Signing and verification tools for Conda
    convert             Convert pure Python packages to other platforms (a.k.a., subdirs).
    create              Create a new conda environment from a list of specified packages.
    deactivate          Deactivate the current active conda environment.
    debug               Debug the build or test phases of conda recipes.
    develop             Install a Python package in 'development mode'. Similar to `pip install --editable`.
    doctor              Display a health report for your environment.
    env                 Create and manage conda environments.
    export              Export a given environment
    index               Update package index metadata files.
    info                Display information about current conda install.
    init                Initialize conda for shell interaction.
    inspect             Tools for inspecting conda packages.
    install             Install a list of packages into a specified conda environment.
    list                List installed packages in a conda environment.
    metapackage         Specialty tool for generating conda metapackage.
    notices             Retrieve latest channel notifications.
    pack                See `conda pack --help`.
    package             Create low-level conda packages. (EXPERIMENTAL)
    remove (uninstall)  Remove a list of packages from a specified conda environment.
    rename              Rename an existing environment.
    render              Expand a conda recipe into a platform-specific recipe.
    repo                See `conda repo --help`.
    repoquery           Advanced search for repodata.
    run                 Run an executable in a conda environment.
    search              Search for packages and display associated information using the MatchSpec format.
    server              See `conda server --help`.
    skeleton            Generate boilerplate conda recipes.
    token               Set repository access token and configure default_channels
    tos                 A subcommand for viewing, accepting, rejecting, and otherwise interacting with a channel's
                        Terms of Service (ToS). This plugin periodically checks for updated Terms of Service for the
                        active/selected channels. Channels with a Terms of Service will need to be accepted or
                        rejected prior to use. Conda will only allow package installation from channels without a
                        Terms of Service or with an accepted Terms of Service. Attempting to use a channel with a
                        rejected Terms of Service will result in an error.
    update (upgrade)    Update conda packages to the latest compatible version.

C:\WINDOWS\system32>conda activate C:\Anaconda3

---

### 🤖 DeepSeek *(2025-10-21 03:08:27)* *[deepseek-chat]*

O problema é que o `conda activate` está sendo chamado sem argumentos, então ele mostra a ajuda e não ativa o ambiente. Vamos corrigir:

## **Solução para o activate.bat:**

Modifique o `C:\Anaconda3\Scripts\activate.bat` para:

```batch
@CALL "%~dp0..\condabin\conda.bat"
@CALL "%~dp0..\condabin\mamba_hook.bat"
@IF "%*"=="" (
    conda activate base
) ELSE (
    conda activate %*
)
```

## **Alternativa mais simples:**

Ou use esta versão mais direta:

```batch
@CALL "%~dp0..\condabin\conda.bat"
@CALL "%~dp0..\condabin\mamba_hook.bat"
conda activate base
```

## **Explicação:**

- **`@IF "%*"==""`** verifica se não há argumentos passados
- **`conda activate base`** ativa explicitamente o ambiente base quando não há argumentos
- Isso evita que o comando `conda activate` sem argumentos mostre a mensagem de ajuda

## **Se ainda não funcionar, teste esta abordagem:**

Altere o atalho diretamente para:
```
%WINDIR%\System32\cmd.exe "/K" C:\Anaconda3\condabin\conda.bat activate base
```

A chave é garantir que `conda activate base` seja executado explicitamente quando não há parâmetros.

---

### 👤 Utilizador *(2025-10-21 03:12:25)* *[deepseek-chat]*

Com: Solução para o activate.bat:  temos: usage: conda-script.py [-h] [-v] [--no-plugins] [-V] COMMAND ...

conda is a tool for managing and deploying applications, environments and packages.

options:
  -h, --help            Show this help message and exit.
  -v, --verbose         Can be used multiple times. Once for detailed output, twice for INFO logging, thrice for DEBUG
                        logging, four times for TRACE logging.
  --no-plugins          Disable all plugins that are not built into conda.
  -V, --version         Show the conda version number and exit.

commands:
  The following built-in and plugins subcommands are available.

  COMMAND
    activate            Activate a conda environment.
    build               Build conda packages from a conda recipe.
    clean               Remove unused packages and caches.
    commands            List all available conda subcommands (including those from plugins). Generally only used by
                        tab-completion.
    compare             Compare packages between conda environments.
    config              Modify configuration values in .condarc.
    content-trust       Signing and verification tools for Conda
    convert             Convert pure Python packages to other platforms (a.k.a., subdirs).
    create              Create a new conda environment from a list of specified packages.
    deactivate          Deactivate the current active conda environment.
    debug               Debug the build or test phases of conda recipes.
    develop             Install a Python package in 'development mode'. Similar to `pip install --editable`.
    doctor              Display a health report for your environment.
    env                 Create and manage conda environments.
    export              Export a given environment
    index               Update package index metadata files.
    info                Display information about current conda install.
    init                Initialize conda for shell interaction.
    inspect             Tools for inspecting conda packages.
    install             Install a list of packages into a specified conda environment.
    list                List installed packages in a conda environment.
    metapackage         Specialty tool for generating conda metapackage.
    notices             Retrieve latest channel notifications.
    pack                See `conda pack --help`.
    package             Create low-level conda packages. (EXPERIMENTAL)
    remove (uninstall)  Remove a list of packages from a specified conda environment.
    rename              Rename an existing environment.
    render              Expand a conda recipe into a platform-specific recipe.
    repo                See `conda repo --help`.
    repoquery           Advanced search for repodata.
    run                 Run an executable in a conda environment.
    search              Search for packages and display associated information using the MatchSpec format.
    server              See `conda server --help`.
    skeleton            Generate boilerplate conda recipes.
    token               Set repository access token and configure default_channels
    tos                 A subcommand for viewing, accepting, rejecting, and otherwise interacting with a channel's
                        Terms of Service (ToS). This plugin periodically checks for updated Terms of Service for the
                        active/selected channels. Channels with a Terms of Service will need to be accepted or
                        rejected prior to use. Conda will only allow package installation from channels without a
                        Terms of Service or with an accepted Terms of Service. Attempting to use a channel with a
                        rejected Terms of Service will result in an error.
    update (upgrade)    Update conda packages to the latest compatible version.

(base) C:\WINDOWS\system32>

---

### 🤖 DeepSeek *(2025-10-21 03:12:25)* *[deepseek-chat]*

O problema é que o `conda.bat` não está sendo executado corretamente. Vamos tentar uma abordagem diferente:

## **Solução 1: Modificar o activate.bat para usar call corretamente**

Altere `C:\Anaconda3\Scripts\activate.bat` para:

```batch
@echo off
call "%~dp0..\condabin\conda.bat" activate base
```

## **Solução 2: Usar abordagem mais direta**

Ou tente esta versão:

```batch
@echo off
set "ROOT_PREFIX=C:\Anaconda3"
call "%ROOT_PREFIX%\condabin\conda.bat" activate base
```

## **Solução 3: Verificar se conda.bat existe**

Verifique se este arquivo existe:
`C:\Anaconda3\condabin\conda.bat`

Se não existir, procure por:
`C:\Anaconda3\Scripts\conda.bat`

E use o caminho correto.

## **Solução 4: Abordagem alternativa - usar o conda diretamente**

```batch
@echo off
C:\Anaconda3\python.exe -m conda activate base
```

## **Solução 5: Restaurar o activate.bat original**

Se nada funcionar, tente restaurar o conteúdo original do `activate.bat`:

```batch
@echo off
set "ROOT_PREFIX=%~dp0.."
set "CONDA_EXE=%ROOT_PREFIX%\condabin\conda.bat"
call "%CONDA_EXE%" activate base
```

**Teste primeiro a Solução 1**, pois é a mais simples. O problema parece ser que o `conda.bat` não está sendo chamado corretamente para inicializar o shell do conda antes do comando `activate`.

---

### 👤 Utilizador *(2025-10-21 03:15:31)* *[deepseek-chat]*

fico com: Solução 1: Modificar o activate.bat para usar call corretamente: o resultado é: (base) C:\WINDOWS\system32>

---

### 🤖 DeepSeek *(2025-10-21 03:15:31)* *[deepseek-chat]*

Perfeito! Agora está funcionando corretamente. 

## **Status: ✅ Resolvido**

O comportamento atual:
- `(base) C:\WINDOWS\system32>` 

é **exatamente o esperado** para o Anaconda Prompt. Isso significa que:

### **O que foi corrigido:**
- ✅ O ambiente base é ativado automaticamente (mostrado pelo `(base)`)
- ✅ Não aparece mais o comando `mamba activate C:\Anaconda3` 
- ✅ O conda/mamba está funcionando normalmente
- ✅ A ativação é silenciosa e apropriada

### **Comportamento normal:**
- `(base)` indica que o ambiente conda base está ativo
- `C:\WINDOWS\system32` é o diretório padrão do prompt (isso é normal)
- Você pode navegar para qualquer diretório com `cd`

### **Para testar se está tudo funcionando:**
```cmd
conda --version
conda list
mamba --version
```

O problema inicial de mostrar o comando `mamba activate` explicitamente foi completamente resolvido. O prompt agora funciona como deveria! 🎉

---

### 👤 Utilizador *(2025-10-21 03:17:46)* *[deepseek-chat]*

(base) D:\Downloads\_DOCS_\_DOCS_\CONDA_Reparar>conda --version
conda 25.9.1

(base) D:\Downloads\_DOCS_\_DOCS_\CONDA_Reparar>conda list
# packages in environment at C:\Anaconda3:
#
# Name                           Version              Build               Channel
_anaconda_depends                2025.06              py313_mkl_2
aiobotocore                      2.19.0               py313haa95532_0
aiohappyeyeballs                 2.4.4                py313haa95532_0
aiohttp                          3.11.10              py313h827c3e9_0
aioitertools                     0.7.1                pyhd3eb1b0_0
aiosignal                        1.2.0                pyhd3eb1b0_0
alabaster                        0.7.16               py313haa95532_0
altair                           5.5.0                pyhd8ed1ab_1
anaconda-anon-usage              0.7.1                py313hfc23b7f_100
anaconda-auth                    0.10.0               pyhd8ed1ab_0
anaconda-catalogs                0.2.0                py313haa95532_2
anaconda-cli-base                0.5.2                py313haa95532_0
anaconda-client                  1.13.0               py313haa95532_1
anaconda-navigator               2.6.6                py313haa95532_2
anaconda-project                 0.11.1               py313haa95532_1
anaconda_powershell_prompt       1.1.0                haa95532_1
anaconda_prompt                  1.1.0                haa95532_1
annotated-types                  0.6.0                py313haa95532_0
anyio                            4.7.0                py313haa95532_0
appdirs                          1.4.4                pypi_0
archspec                         0.2.3                pyhd3eb1b0_0
argon2-cffi                      21.3.0               pyhd3eb1b0_0
argon2-cffi-bindings             21.2.0               py313h827c3e9_1
arrow                            1.3.0                py313haa95532_0
arrow-cpp                        19.0.0               h33d5241_2
astroid                          3.3.8                py313haa95532_0
astropy                          7.0.0                py313h827c3e9_0
astropy-iers-data                0.2025.1.13.0.34.51  py313haa95532_0
asttokens                        3.0.0                pyhd8ed1ab_1
async-lru                        2.0.4                py313haa95532_0
asyncssh                         2.17.0               py313haa95532_0
atomicwrites                     1.4.0                py_0
attrs                            24.3.0               py313haa95532_0
automat                          24.8.1               py313haa95532_0
autopep8                         2.0.4                pyhd3eb1b0_0
aws-c-auth                       0.6.19               h2bbff1b_0
aws-c-cal                        0.5.20               h2bbff1b_0
aws-c-common                     0.8.5                h2bbff1b_0
aws-c-compression                0.2.16               h2bbff1b_0
aws-c-event-stream               0.2.15               hd77b12b_0
aws-c-http                       0.6.25               h2bbff1b_0
aws-c-io                         0.13.10              h2bbff1b_0
aws-c-mqtt                       0.7.13               h2bbff1b_0
aws-c-s3                         0.1.51               h2bbff1b_0
aws-c-sdkutils                   0.1.6                h2bbff1b_0
aws-checksums                    0.1.13               h2bbff1b_0
aws-crt-cpp                      0.18.16              hd77b12b_0
aws-sdk-cpp                      1.11.212             h6a15179_0
babel                            2.16.0               py313haa95532_0
bcrypt                           4.3.0                py313h636fa0f_0
beautifulsoup4                   4.12.3               py313haa95532_0
binaryornot                      0.4.4                pyhd8ed1ab_2
black                            24.10.0              py313haa95532_0
blas                             1.0                  mkl
bleach                           6.2.0                pyh29332c3_4
blinker                          1.9.0                py313haa95532_0
blosc                            1.21.6               hfd34d9b_1
bokeh                            3.6.2                py313haa95532_0
boltons                          24.1.0               py313haa95532_0
boost-cpp                        1.82.0               h59b6b97_2
botocore                         1.36.3               py313haa95532_0
bottleneck                       1.4.2                py313h2cb717b_0
brotli-python                    1.0.9                py313h5da7b33_9
bzip2                            1.0.8                h0ad9c76_8
c-ares                           1.19.1               h2bbff1b_0
c-blosc2                         2.17.1               h0eb4811_0
ca-certificates                  2025.10.5            h4c7d964_0
cachetools                       5.5.1                py313haa95532_0
cattrs                           25.2.0               pyhd8ed1ab_0
certifi                          2025.10.5            py313haa95532_0
cffi                             1.17.1               py313h827c3e9_1
chardet                          4.0.0                py313haa95532_1003
charset-normalizer               3.3.2                pyhd3eb1b0_0
click                            8.1.8                py313haa95532_0
cloudpickle                      3.0.0                py313haa95532_0
colorama                         0.4.6                pyhd8ed1ab_1
colorcet                         3.1.0                pyhd8ed1ab_1
comm                             0.2.1                py313haa95532_0
conda                            25.9.1               py313hfa70ccb_0
conda-anaconda-telemetry         0.1.2                py313haa95532_1
conda-anaconda-tos               0.2.0                py313haa95532_0
conda-build                      25.5.0               pypi_0
conda-content-trust              0.2.0                py313haa95532_1
conda-index                      0.6.1                py313haa95532_0
conda-libmamba-solver            25.4.0               pyhd3eb1b0_0
conda-pack                       0.7.1                py313haa95532_0
conda-package-handling           2.4.0                pyh7900ff3_2
conda-package-streaming          0.11.0               py313haa95532_0
conda-repo-cli                   1.0.165              py313haa95532_0
conda-token                      0.7.0                hd3eb1b0_0
constantly                       23.10.4              py313haa95532_0
contourpy                        1.3.1                py313h214f63a_0
cookiecutter                     1.7.3                pyhd3eb1b0_0
cpp-expected                     1.3.1                h477610d_0
cryptography                     44.0.1               py313hbd6ee87_0
cssselect                        1.2.0                py313haa95532_0
curl                             8.15.0               hf943856_0
cycler                           0.11.0               pyhd3eb1b0_0
cytoolz                          1.0.1                py313h827c3e9_0
dask                             2025.2.0             py313haa95532_0
dask-core                        2025.2.0             py313haa95532_0
dask-expr                        2.0.0                py313haa95532_0
datashader                       0.18.0               py313haa95532_0
debugpy                          1.8.11               py313h5da7b33_0
decorator                        5.1.1                pyhd3eb1b0_0
defusedxml                       0.7.1                pyhd3eb1b0_0
deprecated                       1.2.13               py313haa95532_0
diff-match-patch                 20200713             pyhd3eb1b0_0
dill                             0.3.8                py313haa95532_0
distributed                      2025.2.0             py313haa95532_0
distro                           1.9.0                pyhd8ed1ab_1
docstring-to-markdown            0.11                 py313haa95532_0
docutils                         0.21.2               pyhd8ed1ab_1
et_xmlfile                       1.1.0                py313haa95532_1
evalidate                        2.0.3                py313haa95532_0
exceptiongroup                   1.3.0                pyhd8ed1ab_0
executing                        0.8.3                pyhd3eb1b0_0
expat                            2.7.1                h8ddb27b_0
filelock                         3.17.0               py313haa95532_0
flake8                           7.1.1                py313haa95532_0
flask                            3.1.0                py313haa95532_0
fmt                              11.2.0               h1d4551f_0
fonttools                        4.55.3               py313h827c3e9_0
freeglut                         3.4.0                h8a1e904_1
freetype                         2.14.1               h57928b3_0
frozendict                       2.4.2                py313haa95532_0
frozenlist                       1.5.0                py313h827c3e9_0
fsspec                           2025.3.2             py313h4442805_0
fzf                              0.66.0               hb13f615_0
gflags                           2.2.2                hd77b12b_1
gitdb                            4.0.7                pyhd3eb1b0_0
gitpython                        3.1.43               py313haa95532_0
glog                             0.5.0                hd77b12b_1
gmp                              6.3.0                h537511b_0
gmpy2                            2.2.1                py313h827c3e9_0
greenlet                         3.1.1                py313h5da7b33_0
h11                              0.16.0               py313haa95532_0
h5py                             3.12.1               py313h535c9fb_1
hdf5                             1.14.5               ha36df97_2
heapdict                         1.0.1                pyhd3eb1b0_0
holoviews                        1.20.2               py313haa95532_0
httpcore                         1.0.9                py313haa95532_0
httpx                            0.28.1               pyhd8ed1ab_0
hvplot                           0.11.3               py313haa95532_0
hyperlink                        21.0.0               pyh29332c3_1
icc_rt                           2022.1.0             h6049295_2
icu                              73.1                 h6c2663c_0
idna                             3.7                  py313haa95532_0
imageio                          2.37.0               py313haa95532_0
imagesize                        1.4.1                py313haa95532_0
imbalanced-learn                 0.13.0               py313haa95532_0
importlib-metadata               8.5.0                py313haa95532_0
incremental                      24.7.2               pyhd8ed1ab_1
inflection                       0.5.1                py313haa95532_1
iniconfig                        1.1.1                pyhd3eb1b0_0
intake                           2.0.7                py313haa95532_0
intel-openmp                     2023.1.0             h59b6b97_46320
intervaltree                     3.1.0                pyhd8ed1ab_1
ipykernel                        6.29.5               py313haa95532_1
ipython                          8.30.0               py313haa95532_0
ipython_pygments_lexers          1.1.1                pyhd8ed1ab_0
ipywidgets                       8.1.5                py313haa95532_0
isort                            6.0.1                py313haa95532_0
itemadapter                      0.3.0                pyhd3eb1b0_0
itemloaders                      1.3.2                pyhd8ed1ab_1
itsdangerous                     2.2.0                pyhd8ed1ab_1
jaraco.classes                   3.2.1                pyhd3eb1b0_0
jaraco.context                   6.0.0                py313haa95532_0
jaraco.functools                 4.1.0                py313haa95532_0
jedi                             0.19.2               pyhd8ed1ab_1
jellyfish                        1.1.3                py313h8ecf97c_0
jinja2                           3.1.6                py313haa95532_0
jinja2-time                      0.2.0                pyhd3eb1b0_3
jmespath                         1.0.1                pyhd8ed1ab_1
joblib                           1.4.2                py313haa95532_0
jpeg                             9e                   h827c3e9_3
json5                            0.9.25               py313haa95532_0
jsonpatch                        1.33                 py313haa95532_1
jsonpointer                      2.1                  pyhd3eb1b0_0
jsonschema                       4.23.0               py313haa95532_0
jsonschema-specifications        2023.7.1             py313haa95532_0
jupyter                          1.1.1                pyhd8ed1ab_1
jupyter-lsp                      2.2.5                py313haa95532_0
jupyter_client                   8.6.3                pyhd8ed1ab_1
jupyter_console                  6.6.3                py313haa95532_1
jupyter_core                     5.7.2                py313haa95532_0
jupyter_events                   0.12.0               py313haa95532_0
jupyter_server                   2.15.0               py313haa95532_0
jupyter_server_terminals         0.5.3                pyhd8ed1ab_1
jupyterlab                       4.4.9                pyhd8ed1ab_0
jupyterlab-variableinspector     3.2.4                py313haa95532_0
jupyterlab_pygments              0.3.0                pyhd8ed1ab_2
jupyterlab_server                2.27.3               pyhd8ed1ab_1
jupyterlab_widgets               3.0.13               py313haa95532_0
keyring                          25.6.0               py313haa95532_0
kiwisolver                       1.4.8                py313h5da7b33_0
krb5                             1.20.1               h5b6d351_0
lazy_loader                      0.4                  py313haa95532_0
lcms2                            2.16                 h62be587_1
lerc                             4.0.0                h6470a55_1
libabseil                        20250127.0           cxx17_h52369b4_0
libarchive                       3.8.1                h815d515_0
libboost                         1.82.0               h3399ecb_2
libbrotlicommon                  1.0.9                h827c3e9_9
libbrotlidec                     1.0.9                h827c3e9_9
libbrotlienc                     1.0.9                h827c3e9_9
libclang                         14.0.6               default_h77d9078_1
libclang13                       14.0.6               default_h77d9078_1
libcurl                          8.15.0               h2300eb9_0
libdeflate                       1.22                 h5bf469e_0
libevent                         2.1.12               h56d1f94_1
libexpat                         2.7.1                hac47afa_0
libffi                           3.4.4                hd77b12b_1
libfreetype                      2.14.1               h57928b3_0
libfreetype6                     2.14.1               hdbac1cb_0
libgrpc                          1.71.0               hf4237ab_0
libiconv                         1.16                 h2bbff1b_3
libkrb5                          1.21.3               h885b0b7_4
liblief                          0.16.4               h585ebfc_0
libmamba                         2.3.2                hd264f3a_2
libmambapy                       2.3.2                py313ha758d27_2
libmpdec                         4.0.0                h827c3e9_0
libpng                           1.6.50               h7351971_1
libpq                            17.4                 h4a159e6_2
libprotobuf                      5.29.3               he9d8c4a_0
libre2-11                        2024.07.02           h5da7b33_0
libsodium                        1.0.18               h62dcd97_0
libsolv                          0.7.35               h8883371_0
libspatialindex                  1.9.3                h6c2663c_0
libsqlite                        3.50.4               hf5d6505_0
libssh2                          1.11.1               h9aa295b_0
libthrift                        0.15.0               h532d1ae_1
libtiff                          4.7.0                h404307b_0
libwebp-base                     1.3.2                h3d04722_1
libxml2                          2.13.8               h866ff63_0
libxslt                          1.1.41               h0739af5_0
libzlib                          1.3.1                h2466b09_2
linkify-it-py                    2.0.0                py313haa95532_0
llvmlite                         0.44.0               py313hc403fe3_2
locket                           1.0.0                py313haa95532_0
lsprotocol                       2025.0.0             pyhe01879c_0
lxml                             6.0.0                py313he881f1c_0
lz4                              4.3.2                py313h827c3e9_1
lz4-c                            1.9.4                h2bbff1b_1
lzo                              2.10                 h6a83c73_1002
m2-msys2-runtime                 2.5.0.17080.65c939c  3
m2-patch                         2.7.5                2
mamba                            2.3.2                h6021b6d_2
markdown                         3.8                  py313haa95532_0
markdown-it-py                   2.2.0                py313haa95532_1
markupsafe                       3.0.2                py313h827c3e9_0
matplotlib                       3.10.0               py313haa95532_1
matplotlib-base                  3.10.0               py313h7aa5d4e_1
matplotlib-inline                0.1.6                py313haa95532_0
mbedtls                          3.5.1                h5da7b33_1
mccabe                           0.7.0                pyhd8ed1ab_1
mdit-py-plugins                  0.3.0                py313haa95532_0
mdurl                            0.1.0                py313haa95532_0
menuinst                         2.2.0                py313h5da7b33_1
mistune                          3.1.2                py313haa95532_0
mkl                              2023.1.0             h6b88ed4_46358
mkl-service                      2.4.0                py313h827c3e9_2
mkl_fft                          1.3.11               py313h827c3e9_0
mkl_random                       1.2.8                py313hce38976_0
more-itertools                   10.3.0               py313haa95532_0
mpc                              1.3.1                h827c3e9_0
mpfr                             4.2.1                h56c3642_0
mpmath                           1.3.0                pyhd8ed1ab_1
msgpack-python                   1.0.3                py313h214f63a_0
msys2-conda-epoch                20160418             1
multidict                        6.1.0                py313h827c3e9_0
multipledispatch                 0.6.0                pyhd8ed1ab_1
mypy                             1.14.1               py313h827c3e9_0
mypy_extensions                  1.0.0                py313haa95532_0
narwhals                         1.31.0               py313haa95532_1
navigator-updater                0.5.1                py313haa95532_0
nbclient                         0.10.2               py313haa95532_0
nbconvert                        7.16.6               hc388f54_1
nbconvert-core                   7.16.6               pyhcf101f3_1
nbconvert-pandoc                 7.16.6               h7d6f222_1
nbformat                         5.10.4               pyhd8ed1ab_1
nest-asyncio                     1.6.0                pyhd8ed1ab_1
networkx                         3.4.2                py313haa95532_0
nlohmann_json                    3.11.2               h6c2663c_0
nlohmann_json-abi                3.12.0               h0f90c79_1
nltk                             3.9.1                py313hea850e4_0
notebook                         7.4.7                pyhd8ed1ab_0
notebook-shim                    0.2.4                pyhd8ed1ab_1
numba                            0.61.0               py313h5da7b33_1
numexpr                          2.10.1               py313h4cd664f_0
numpy                            2.1.3                py313he6dc315_0
numpy-base                       2.1.3                py313h6011491_0
numpydoc                         1.7.0                py313haa95532_0
openjpeg                         2.5.2                h9b5d1b5_1
openpyxl                         3.1.5                py313hc624790_2
openssl                          3.5.4                h725018a_0
orc                              2.1.1                hd1c1d5c_0
overrides                        7.4.0                py313haa95532_0
packaging                        24.2                 py313haa95532_0
pandas                           2.2.3                py313h5da7b33_0
pandoc                           2.12                 haa95532_3
pandocfilters                    1.5.0                pyhd3eb1b0_0
panel                            1.7.0                py313haa95532_0
param                            2.2.0                py313haa95532_0
parsel                           1.8.1                py313haa95532_0
parso                            0.8.4                py313haa95532_0
partd                            1.4.2                py313haa95532_0
pathspec                         0.10.3               py313haa95532_0
patsy                            1.0.1                pyhd8ed1ab_1
pcre2                            10.46                h3402e2f_0
pexpect                          4.8.0                pyhd3eb1b0_3
pickleshare                      0.7.5                pyhd8ed1ab_1004
pillow                           11.1.0               py313hea0d53e_1
pip                              25.1                 pyhc872135_2
pkce                             1.0.3                pyhd8ed1ab_1
pkginfo                          1.12.0               py313haa95532_0
platformdirs                     4.3.7                py313haa95532_0
plotly                           5.24.1               py313h4442805_1
pluggy                           1.5.0                py313haa95532_0
ply                              3.11                 pyhd8ed1ab_3
poyo                             0.5.0                pyhd3eb1b0_0
prometheus_client                0.21.1               py313haa95532_0
prompt-toolkit                   3.0.43               py313haa95532_0
prompt_toolkit                   3.0.43               hd3eb1b0_0
propcache                        0.3.1                py313h827c3e9_0
protego                          0.4.0                py313haa95532_0
protobuf                         5.29.3               py313h5da7b33_0
psutil                           5.9.0                py313h827c3e9_1
ptyprocess                       0.7.0                pyhd3eb1b0_2
pure_eval                        0.2.2                pyhd3eb1b0_0
py-cpuinfo                       9.0.0                pyhd8ed1ab_1
py-lief                          0.16.4               py313h585ebfc_0
pyarrow                          19.0.0               py313h5da7b33_1
pyasn1                           0.4.8                pyhd3eb1b0_0
pyasn1-modules                   0.2.8                py_0
pybind11-abi                     4                    hd8ed1ab_3
pycodestyle                      2.12.1               pyhd8ed1ab_1
pycosat                          0.6.6                py313h5ea7bf4_3
pycparser                        2.21                 pyhd3eb1b0_0
pyct                             0.5.0                py313haa95532_0
pycurl                           7.45.6               py313h51539b2_0
pydantic                         2.10.3               py313haa95532_0
pydantic-core                    2.27.1               py313h636fa0f_0
pydantic-settings                2.6.1                py313haa95532_0
pydispatcher                     2.0.5                py313haa95532_3
pydocstyle                       6.3.0                pyhd8ed1ab_1
pyerfa                           2.0.1.5              py310h1f63838_2
pyflakes                         3.2.0                pyhd8ed1ab_1
pygithub                         2.4.0                py313haa95532_0
pygments                         2.19.1               py313haa95532_0
pyjwt                            2.10.1               py313haa95532_0
pylint                           3.3.5                py313haa95532_0
pylint-venv                      3.0.3                py313haa95532_0
pyls-spyder                      0.4.0                pypi_0
pynacl                           1.5.0                py313h7edc060_1
pyodbc                           5.2.0                py313hfe59770_1
pyopenssl                        25.0.0               py313hb6ff9d5_0
pyparsing                        3.2.0                py313haa95532_0
pyqt                             5.15.10              py313h5da7b33_1
pyqt5-sip                        12.13.0              py313h827c3e9_1
pyqtwebengine                    5.15.10              py313h5da7b33_1
pysocks                          1.7.1                pyh09c184e_7
pytables                         3.10.2               py313h98afe49_9
pytest                           8.3.4                py313haa95532_0
python                           3.13.0               hf5aa216_101_cp313
python-dateutil                  2.9.0post0           py313haa95532_2
python-dotenv                    1.1.0                py313haa95532_0
python-fastjsonschema            2.20.0               py313haa95532_0
python-json-logger               3.2.1                py313haa95532_0
python-libarchive-c              5.1                  pyhd3eb1b0_0
python-lmdb                      1.6.2                py313h5da7b33_0
python-lsp-black                 2.0.0                py313haa95532_1
python-lsp-jsonrpc               1.1.2                pyhff2d567_1
python-lsp-ruff                  2.3.0                pyhcf101f3_0
python-lsp-server                1.13.1               pyh332efcf_0
python-lsp-server-base           1.13.1               pyhd8ed1ab_0
python-slugify                   5.0.2                pyhd3eb1b0_0
python-tzdata                    2025.2               pyhd3eb1b0_0
python_abi                       3.13                 8_cp313
pytoolconfig                     1.2.6                py313haa95532_0
pytz                             2024.1               py313haa95532_0
pyuca                            1.2                  pyhd8ed1ab_2
pyviz_comms                      3.0.2                py313haa95532_0
pywavelets                       1.8.0                py313h827c3e9_0
pywin32                          308                  py313h5da7b33_0
pywin32-ctypes                   0.2.2                py313haa95532_0
pywinpty                         2.0.15               py313h5813708_1
pyyaml                           6.0.2                py313h827c3e9_0
pyzmq                            26.2.0               py313h5da7b33_0
qdarkstyle                       3.2.3                pyhd8ed1ab_1
qstylizer                        0.2.2                py313haa95532_0
qt-main                          5.15.2               h19c9488_12
qt-webengine                     5.15.9               h5bd16bc_7
qtawesome                        1.4.0                pypi_0
qtconsole                        5.7.0                pyhd8ed1ab_0
qtconsole-base                   5.7.0                pyha770c72_0
qtpy                             2.4.1                py313haa95532_0
queuelib                         1.6.2                py313haa95532_0
re2                              2024.07.02           h214f63a_0
readchar                         4.0.5                py313haa95532_0
referencing                      0.30.2               py313haa95532_0
regex                            2024.11.6            py313h827c3e9_0
reproc                           14.2.4               hd77b12b_2
reproc-cpp                       14.2.4               hd77b12b_2
requests                         2.32.3               py313haa95532_1
requests-file                    2.1.0                py313haa95532_0
requests-toolbelt                1.0.0                pyhd8ed1ab_1
rfc3339-validator                0.1.4                pyhd8ed1ab_1
rfc3986-validator                0.1.1                py313haa95532_0
rich                             13.9.4               py313haa95532_0
ripgrep                          15.0.0               h77a83cd_0
roman-numerals-py                3.1.0                py313haa95532_0
rope                             1.13.0               py313haa95532_0
rpds-py                          0.22.3               py313h636fa0f_0
rtree                            1.0.1                py313h2eaa2aa_0
ruamel.yaml                      0.18.10              py313h827c3e9_0
ruamel.yaml.clib                 0.2.12               py313h827c3e9_0
ruamel_yaml                      0.17.21              py313h827c3e9_0
ruff                             0.14.1               h3e3edff_0
s3fs                             2025.3.2             py313haa95532_0
scikit-image                     0.25.0               py313h5da7b33_0
scikit-learn                     1.6.1                py313h585ebfc_0
scipy                            1.15.3               py313hde77213_0
scrapy                           2.12.0               py313haa95532_1
seaborn                          0.13.2               py313haa95532_3
semver                           3.0.2                py313haa95532_1
send2trash                       1.8.2                py313haa95532_1
service_identity                 24.2.0               hd8ed1ab_1
setuptools                       72.1.0               py313haa95532_0
shellingham                      1.5.0                py313haa95532_0
simdjson                         4.0.7                h49e36cd_0
sip                              6.7.12               py313h5da7b33_1
six                              1.17.0               pyhe01879c_1
sklearn-compat                   0.1.3                py313haa95532_0
smmap                            4.0.0                pyhd3eb1b0_0
snappy                           1.2.1                hcdb6601_0
sniffio                          1.3.0                py313haa95532_0
snowballstemmer                  2.2.0                pyhd3eb1b0_0
sortedcontainers                 2.4.0                pyhd8ed1ab_1
soupsieve                        2.5                  py313haa95532_0
spdlog                           1.16.0               h7d890cf_1
sphinx                           8.2.3                py313h827c3e9_0
sphinxcontrib-applehelp          2.0.0                pyhd3eb1b0_1
sphinxcontrib-devhelp            2.0.0                pyhd8ed1ab_1
sphinxcontrib-htmlhelp           2.1.0                pyhd8ed1ab_1
sphinxcontrib-jsmath             1.0.1                pyhd8ed1ab_1
sphinxcontrib-qthelp             2.0.0                pyhd3eb1b0_1
sphinxcontrib-serializinghtml    2.0.0                pyhd3eb1b0_0
spyder                           6.1.0                hd8ed1ab_0
spyder-base                      6.1.0                py313hfa70ccb_0
spyder-kernels                   3.1.1                win_pyh7428d3b_0
sqlalchemy                       2.0.39               py313h54f65d0_0
sqlite                           3.45.3               h2bbff1b_0
stack_data                       0.2.0                pyhd3eb1b0_0
statsmodels                      0.14.4               py313h827c3e9_0
streamlit                        1.45.1               py313haa95532_1
superqt                          0.7.3                py313h4442805_0
sympy                            1.13.3               py313haa95532_1
tabulate                         0.9.0                pyhd8ed1ab_2
tbb                              2021.8.0             h59b6b97_0
tblib                            3.1.0                py313haa95532_0
tenacity                         9.0.0                py313haa95532_0
terminado                        0.17.1               py313haa95532_0
text-unidecode                   1.3                  pyhd8ed1ab_2
textdistance                     4.6.3                pyhd8ed1ab_1
threadpoolctl                    3.5.0                py313h4442805_0
three-merge                      0.1.1                pyhd8ed1ab_1
tifffile                         2025.2.18            py313haa95532_0
tinycss2                         1.4.0                py313haa95532_0
tk                               8.6.13               h2c6b04d_2
tldextract                       5.1.2                py313haa95532_0
toml                             0.10.2               pyhd8ed1ab_1
tomli                            2.0.1                py313haa95532_1
tomlkit                          0.13.2               py313haa95532_0
toolz                            1.0.0                py313haa95532_0
tornado                          6.5.1                py313h827c3e9_0
tqdm                             4.67.1               pyhd8ed1ab_1
traitlets                        5.14.3               pyhd8ed1ab_1
truststore                       0.10.0               py313haa95532_0
twisted                          24.11.0              py313haa95532_0
twisted-iocpsupport              1.0.2                py313h827c3e9_1
typer                            0.9.0                py313haa95532_0
typing-extensions                4.12.2               py313haa95532_0
typing_extensions                4.12.2               py313haa95532_0
tzdata                           2025b                h04d1e81_0
uc-micro-py                      1.0.1                py313haa95532_0
ucrt                             10.0.22621.0         haa95532_0
ujson                            5.10.0               py313h5da7b33_1
unidecode                        1.3.8                py313haa95532_0
urllib3                          2.3.0                py313haa95532_0
utf8proc                         2.6.1                h2bbff1b_1
vc                               14.42                haa95532_5
vc14_runtime                     14.44.35208          h818238b_32
vs2015_runtime                   14.44.35208          h38c0c73_32
w3lib                            2.1.2                py313haa95532_0
watchdog                         4.0.2                py313haa95532_0
wcwidth                          0.2.5                pyhd3eb1b0_0
webencodings                     0.5.1                pyhd8ed1ab_3
websocket-client                 1.8.0                py313haa95532_0
werkzeug                         3.1.3                pyhd8ed1ab_1
whatthepatch                     1.0.2                py313haa95532_0
wheel                            0.45.1               pyhd8ed1ab_1
widgetsnbextension               4.0.13               py313haa95532_0
win_inet_pton                    1.1.0                pyh7428d3b_8
winpty                           0.4.3                4
wrapt                            1.17.0               py313h827c3e9_0
xarray                           2025.4.0             py313haa95532_0
xlwings                          0.32.1               py313haa95532_1
xyzservices                      2022.9.0             py313haa95532_1
xz                               5.6.4                h4754444_1
yaml                             0.2.5                h6a83c73_3
yaml-cpp                         0.8.0                hd77b12b_1
yapf                             0.40.2               py313haa95532_0
yarl                             1.18.0               py313h827c3e9_0
zeromq                           4.3.5                h5bddc39_9
zict                             3.0.0                pyhd8ed1ab_1
zipp                             3.21.0               py313haa95532_0
zlib                             1.3.1                h2466b09_2
zlib-ng                          2.0.7                h2bbff1b_0
zope                             1.0                  py313haa95532_1
zope.interface                   7.1.1                py313h827c3e9_0
zstandard                        0.25.0               py313h5fd188c_0
zstd                             1.5.7                hbeecb71_2

(base) D:\Downloads\_DOCS_\_DOCS_\CONDA_Reparar>mamba --version
2.3.2

(base) D:\Downloads\_DOCS_\_DOCS_\CONDA_Reparar>

---

### 🤖 DeepSeek *(2025-10-21 03:17:46)* *[deepseek-chat]*

Excelente! 🎉 

## **Status: ✅ Problema completamente resolvido!**

### **Resultados dos testes:**
- ✅ **Conda**: Versão 25.9.1 funcionando perfeitamente
- ✅ **Mamba**: Versão 2.3.2 funcionando perfeitamente  
- ✅ **Ambiente base**: Ativado corretamente sem mostrar `mamba activate C:\Anaconda3`
- ✅ **Pacotes**: Todos listados normalmente
- ✅ **Navegação**: Funcionando entre diretórios

### **Resumo da solução:**
O problema foi resolvido modificando o `activate.bat` para:
```batch
@echo off
call "%~dp0..\condabin\conda.bat" activate base
```

### **Comportamento atual correto:**
- `(base)` aparece silenciosamente indicando ambiente ativo
- Nenhum comando `mamba activate` explícito é mostrado
- Todas as funcionalidades do conda/mamba estão operacionais

O Anaconda Prompt agora está funcionando **exatamente como deveria**! O problema inicial de mostrar o comando de ativação explicitamente foi completamente eliminado. 

**Missão cumprida!** 🚀

---

*Conversa exportada do DeepSeek*
*Processado em: 24/11/2025 22:27*