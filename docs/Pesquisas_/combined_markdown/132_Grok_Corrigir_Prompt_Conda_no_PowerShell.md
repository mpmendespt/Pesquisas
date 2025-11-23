# Corrigir Prompt Conda no PowerShell

## 📊 Informações
- **Número:** #132
- **Origem:** Grok
- **Categoria:** Programação
- **ID:** 6333cc1a-f74c-46cd-974b-752d0be70a45
- **Criada em:** 2025-10-01 18:49:49Z
- **Atualizada em:** 2025-10-01 18:50:07Z
- **Total de mensagens:** 2
- **Resumo:** O Windows PowerShell aparece com o prompt (base), o que parece que pertence ao conda. Como corrigir ...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-01 19:49:49)* *[Grok]*

O Windows PowerShell aparece com o prompt (base), o que parece que pertence ao conda. Como corrigir e voltar ao original Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.
Try the new cross-platform PowerShell https://aka.ms/pscore6
Loading personal and system profiles took 1283ms.
(base) PS C:\WINDOWS\system32>

---

### 🤖 Grok *(2025-10-01 19:50:07)* *[Grok]*

O prompt `(base)` no Windows PowerShell indica que o ambiente padrão do Conda está ativado. Isso acontece porque o Conda modifica o PowerShell para carregar automaticamente o ambiente base ao iniciar. Para voltar ao PowerShell original, sem o prompt `(base)` e sem o Conda ativado automaticamente, siga estas etapas:

### Passo 1: Desativar o ambiente base temporariamente
1. No PowerShell, digite o seguinte comando para desativar o ambiente base atual:
   ```
   conda deactivate
   ```
   Isso removerá o `(base)` do prompt para a sessão atual.

### Passo 2: Impedir que o Conda carregue o ambiente base automaticamente
Para evitar que o Conda ative o ambiente base toda vez que você abrir o PowerShell:
1. Abra o PowerShell.
2. Digite o seguinte comando para configurar o Conda para não ativar o ambiente base automaticamente:
   ```
   conda config --set auto_activate_base false
   ```
3. Feche e reabra o PowerShell. O prompt `(base)` não deve mais aparecer.

### Passo 3: Verificar e corrigir o perfil do PowerShell (opcional)
O Conda pode ter modificado o script de perfil do PowerShell, que é executado toda vez que o PowerShell é iniciado. Para verificar e corrigir:
1. Verifique se existe um arquivo de perfil do PowerShell:
   ```
   Test-Path $PROFILE
   ```
   Isso retorna `True` se o arquivo de perfil existe, ou `False` se não existe.

2. Se o arquivo de perfil existe, abra-o para edição:
   ```
   notepad $PROFILE
   ```
3. Procure por linhas relacionadas ao Conda, como:
   ```
   # >>> conda initialize >>>
   ...
   # <<< conda initialize <<<
   ```
   Essas linhas inicializam o Conda. Para desativar, você pode:
   - **Comentar as linhas**: Adicione `#` no início de cada linha dentro do bloco do Conda.
   - **Remover as linhas**: Delete todo o bloco relacionado ao Conda, mas tenha cuidado para não remover outras configurações importantes.

4. Salve o arquivo e reinicie o PowerShell.

### Passo 4: Reverter completamente a inicialização do Conda (opcional)
Se você deseja remover completamente a integração do Conda com o PowerShell:
1. Execute o comando para desativar a inicialização do Conda:
   ```
   conda init --reverse powershell
   ```
   Isso remove as modificações feitas pelo Conda no perfil do PowerShell.

2. Verifique novamente o arquivo de perfil (como no Passo 3) e confirme que as linhas do Conda foram removidas.

### Passo 5: Testar
Feche o PowerShell e abra novamente. O prompt deve voltar ao padrão do Windows PowerShell, sem o `(base)` e sem mensagens relacionadas ao Conda.

### Observações
- Se você ainda precisar usar o Conda, pode ativá-lo manualmente com:
  ```
  conda activate base
  ```
  ou ativar outro ambiente específico com:
  ```
  conda activate nome_do_ambiente
  ```
- Se você desinstalar o Conda, certifique-se de remover manualmente quaisquer linhas remanescentes no arquivo de perfil do PowerShell.

Se o problema persistir, me avise para investigar mais a fundo!

---

*Conversa exportada do Grok*
*Processado em: 15/11/2025 22:27*