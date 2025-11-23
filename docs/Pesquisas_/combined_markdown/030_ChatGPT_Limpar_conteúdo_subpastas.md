# Limpar conteúdo subpastas

## 📊 Informações
- **Número:** #30
- **Origem:** ChatGPT
- **Categoria:** Programação
- **ID:** 690bda29-0084-8321-a14f-4da8bafacf4b
- **Criada em:** 2025-11-05 23:13:45
- **Atualizada em:** 2025-11-05 23:44:25
- **Total de mensagens:** 8
- **Resumo:** Apagar conteudo de subpastas criadas por comb_fragments_system3_html_export.py; Esse script deve cha...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-05 23:13:42)* *[ChatGPT]*

Apagar conteudo de subpastas criadas por comb_fragments_system3_html_export.py; Esse script deve chamar-se Cleanfiles.py (Apagar nessas pastas html md csv json)

---

### 👤 Utilizador *(2025-11-05 23:17:44)* *[ChatGPT]*

Apagar conteudo de subpastas criadas por comb_fragments_system3_html_export.py; Esse script deve chamar-se Cleanfiles.py (Apagar nessas pastas html md csv json e pdf)

---

### 🤖 ChatGPT *(2025-11-05 23:13:47)* *[ChatGPT]*

Perfeito 👍  
Com base no script `comb_fragments_system3_html_export.py`, as subpastas criadas automaticamente são:

- `combined_markdown/`  
- `combined_csv/`  
- `combined_json/`  
- `combined_html/`  
- `combined_pdfs/`

Você pediu um novo script chamado **`Cleanfiles.py`** que apague **somente o conteúdo** dessas subpastas (sem removê-las), excluindo os arquivos com extensões `.html`, `.md`, `.csv`, `.json`.

Aqui está o código completo do **Cleanfiles.py**:

```python
# Cleanfiles.py
import os
from pathlib import Path
import logging

def limpar_subpastas():
    # Subpastas criadas pelo comb_fragments_system3_html_export.py
    pastas = [
        "combined_markdown",
        "combined_csv",
        "combined_json",
        "combined_html",
        "combined_pdfs"
    ]
    
    # Extensões que serão apagadas
    extensoes_alvo = {".html", ".md", ".csv", ".json"}
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    for pasta in pastas:
        caminho = Path(pasta)
        if not caminho.exists():
            logging.warning(f"⚠️ Pasta não encontrada: {caminho}")
            continue
        
        arquivos_removidos = 0
        
        for arquivo in caminho.glob("**/*"):
            if arquivo.is_file() and arquivo.suffix.lower() in extensoes_alvo:
                try:
                    arquivo.unlink()
                    logging.info(f"🗑️ Removido: {arquivo}")
                    arquivos_removidos += 1
                except Exception as e:
                    logging.error(f"❌ Erro ao apagar {arquivo}: {e}")
        
        if arquivos_removidos == 0:
            logging.info(f"📂 Nenhum arquivo alvo encontrado em: {caminho}")
        else:
            logging.info(f"✅ Total apagado em {caminho}: {arquivos_removidos} arquivo(s)")

if __name__ == "__main__":
    limpar_subpastas()
```

### 🧩 Como usar
1. Coloque este arquivo `Cleanfiles.py` **na mesma pasta** onde está o `comb_fragments_system3_html_export.py`.
2. Execute no terminal:
   ```bash
   python Cleanfiles.py
   ```
3. Ele vai apagar **apenas** arquivos `.html`, `.md`, `.csv` e `.json` dentro das pastas citadas.

Deseja que o script também ofereça uma opção tipo `--dry-run` (para mostrar o que seria apagado sem realmente apagar)?

---

### 🤖 ChatGPT *(2025-11-05 23:17:47)* *[ChatGPT]*

Perfeito 👍  
Com base no conteúdo do seu script **`comb_fragments_system3_html_export.py`**, você quer criar um novo script chamado **`Cleanfiles.py`** que apague arquivos de certos tipos dentro das subpastas criadas por ele — ou seja, dentro de:

- `combined_markdown/`  
- `combined_csv/`  
- `combined_json/`  
- `combined_pdfs/`  
- `combined_html/`

E você quer apagar os arquivos **`.html`, `.md`, `.csv`, `.json`, `.pdf`**.

Aqui está o código completo e seguro para o **`Cleanfiles.py`**:

```python
#!/usr/bin/env python3
# Cleanfiles.py
"""
Apaga arquivos gerados pelo comb_fragments_system3_html_export.py
Remove arquivos .html, .md, .csv, .json e .pdf das subpastas correspondentes.
"""

import os
from pathlib import Path
import logging

def limpar_pastas():
    # Diretórios criados pelo comb_fragments_system3_html_export.py
    pastas = [
        "combined_markdown",
        "combined_csv",
        "combined_json",
        "combined_pdfs",
        "combined_html"
    ]
    
    # Extensões a serem removidas
    extensoes = (".html", ".md", ".csv", ".json", ".pdf")
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Cleanfiles")
    
    total_apagados = 0
    for pasta in pastas:
        dir_path = Path(pasta)
        if not dir_path.exists():
            logger.warning(f"Pasta não encontrada: {dir_path}")
            continue
        
        logger.info(f"🧹 Limpando pasta: {dir_path}")
        count = 0
        
        for root, _, files in os.walk(dir_path):
            for nome in files:
                if nome.lower().endswith(extensoes):
                    caminho = Path(root) / nome
                    try:
                        caminho.unlink()
                        logger.info(f"   🗑️  Apagado: {caminho}")
                        count += 1
                    except Exception as e:
                        logger.error(f"   ⚠️  Erro ao apagar {caminho}: {e}")
        
        total_apagados += count
        if count == 0:
            logger.info(f"   (Nenhum arquivo encontrado para apagar em {dir_path})")
        else:
            logger.info(f"   ✅ {count} arquivos apagados em {dir_path}")
    
    logger.info(f"\n🧾 Total de arquivos apagados: {total_apagados}")

if __name__ == "__main__":
    limpar_pastas()
```

### ✅ Como usar

1. Coloque o arquivo **`Cleanfiles.py`** na mesma pasta onde está `comb_fragments_system3_html_export.py`.
2. Execute no terminal:

```bash
python Cleanfiles.py
```

3. Ele mostrará no console quais arquivos foram apagados de cada subpasta.

---

Quer que eu adicione uma opção `--dry-run` (modo simulação, apenas mostra o que seria apagado)? Isso pode ajudar a testar antes de realmente apagar.

---

### 👤 Utilizador *(2025-11-05 23:41:41)* *[ChatGPT]*

sim --dry-run

---

### 🤖 ChatGPT *(2025-11-05 23:41:42)* *[ChatGPT]*

Perfeito ✅  
Aqui está a versão **atualizada** do script **`Cleanfiles.py`**, agora com a opção `--dry-run` para simular a limpeza sem apagar nada (útil para verificar o que seria removido antes de executar de fato):

---

```python
#!/usr/bin/env python3
# Cleanfiles.py
"""
Apaga arquivos gerados pelo comb_fragments_system3_html_export.py
Remove arquivos .html, .md, .csv, .json e .pdf das subpastas correspondentes.
Suporta modo --dry-run (simulação sem apagar).
"""

import os
import argparse
from pathlib import Path
import logging

def limpar_pastas(dry_run=False):
    # Diretórios criados pelo comb_fragments_system3_html_export.py
    pastas = [
        "combined_markdown",
        "combined_csv",
        "combined_json",
        "combined_pdfs",
        "combined_html"
    ]
    
    # Extensões a serem removidas
    extensoes = (".html", ".md", ".csv", ".json", ".pdf")
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Cleanfiles")
    
    total_apagados = 0
    for pasta in pastas:
        dir_path = Path(pasta)
        if not dir_path.exists():
            logger.warning(f"Pasta não encontrada: {dir_path}")
            continue
        
        logger.info(f"🧹 Limpando pasta: {dir_path}")
        count = 0
        
        for root, _, files in os.walk(dir_path):
            for nome in files:
                if nome.lower().endswith(extensoes):
                    caminho = Path(root) / nome
                    if dry_run:
                        logger.info(f"   🔍 (Dry-run) Apagaria: {caminho}")
                        count += 1
                    else:
                        try:
                            caminho.unlink()
                            logger.info(f"   🗑️  Apagado: {caminho}")
                            count += 1
                        except Exception as e:
                            logger.error(f"   ⚠️  Erro ao apagar {caminho}: {e}")
        
        total_apagados += count
        if count == 0:
            logger.info(f"   (Nenhum arquivo encontrado em {dir_path})")
        else:
            status = "seriam apagados" if dry_run else "apagados"
            logger.info(f"   ✅ {count} arquivos {status} em {dir_path}")
    
    status_final = "seriam apagados" if dry_run else "apagados"
    logger.info(f"\n🧾 Total de arquivos {status_final}: {total_apagados}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apaga arquivos gerados pelo comb_fragments_system3_html_export.py")
    parser.add_argument("--dry-run", action="store_true", help="Simula a limpeza sem apagar arquivos")
    args = parser.parse_args()

    limpar_pastas(dry_run=args.dry_run)
```

---

### 💡 Como usar:

🔹 **Simular (não apaga nada):**
```bash
python Cleanfiles.py --dry-run
```

🔹 **Apagar de verdade:**
```bash
python Cleanfiles.py
```

---

Deseja que eu adicione também uma opção `--extensoes` para escolher quais tipos apagar (por exemplo, só `.html` e `.pdf`)?

---

### 👤 Utilizador *(2025-11-05 23:43:33)* *[ChatGPT]*

sim --extensoes

---

### 🤖 ChatGPT *(2025-11-05 23:43:33)* *[ChatGPT]*

Excelente 👌  
Aqui está a **versão final e aprimorada** do script **`Cleanfiles.py`**, agora com suporte aos parâmetros:

- `--dry-run` → simula sem apagar.  
- `--extensoes` → permite escolher quais tipos de arquivos apagar (por exemplo, `.html .pdf`).

---

```python
#!/usr/bin/env python3
# Cleanfiles.py
"""
Apaga arquivos gerados pelo comb_fragments_system3_html_export.py.
Remove arquivos com extensões específicas nas subpastas criadas pelo exportador.

Opções:
  --dry-run      → simula a limpeza (não apaga de verdade)
  --extensoes    → define quais extensões apagar (ex: --extensoes .html .pdf)
"""

import os
import argparse
from pathlib import Path
import logging

def limpar_pastas(dry_run=False, extensoes=None):
    """
    Remove arquivos das subpastas criadas por comb_fragments_system3_html_export.py.
    """
    # Pastas padrão do script original
    pastas = [
        "combined_markdown",
        "combined_csv",
        "combined_json",
        "combined_pdfs",
        "combined_html"
    ]
    
    # Extensões padrão, se não forem fornecidas
    if not extensoes:
        extensoes = (".html", ".md", ".csv", ".json", ".pdf")
    else:
        extensoes = tuple(e.lower() for e in extensoes)

    # Configuração do logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Cleanfiles")
    
    total_apagados = 0
    for pasta in pastas:
        dir_path = Path(pasta)
        if not dir_path.exists():
            logger.warning(f"Pasta não encontrada: {dir_path}")
            continue
        
        logger.info(f"🧹 Limpando pasta: {dir_path}")
        count = 0
        
        for root, _, files in os.walk(dir_path):
            for nome in files:
                if nome.lower().endswith(extensoes):
                    caminho = Path(root) / nome
                    if dry_run:
                        logger.info(f"   🔍 (Dry-run) Apagaria: {caminho}")
                        count += 1
                    else:
                        try:
                            caminho.unlink()
                            logger.info(f"   🗑️  Apagado: {caminho}")
                            count += 1
                        except Exception as e:
                            logger.error(f"   ⚠️  Erro ao apagar {caminho}: {e}")
        
        total_apagados += count
        if count == 0:
            logger.info(f"   (Nenhum arquivo encontrado em {dir_path})")
        else:
            status = "seriam apagados" if dry_run else "apagados"
            logger.info(f"   ✅ {count} arquivos {status} em {dir_path}")
    
    status_final = "seriam apagados" if dry_run else "apagados"
    logger.info(f"\n🧾 Total de arquivos {status_final}: {total_apagados}")

def main():
    parser = argparse.ArgumentParser(
        description="Apaga arquivos gerados pelo comb_fragments_system3_html_export.py"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a limpeza sem apagar arquivos"
    )
    parser.add_argument(
        "--extensoes",
        nargs="+",
        help="Define quais extensões apagar (ex: --extensoes .html .pdf)"
    )
    
    args = parser.parse_args()
    
    limpar_pastas(dry_run=args.dry_run, extensoes=args.extensoes)

if __name__ == "__main__":
    main()
```

---

### 💡 Exemplos de uso

🧪 **Simular a limpeza (mostrar o que seria apagado):**
```bash
python Cleanfiles.py --dry-run
```

🧹 **Apagar tudo (html, md, csv, json, pdf):**
```bash
python Cleanfiles.py
```

📄 **Apagar apenas HTML e PDF:**
```bash
python Cleanfiles.py --extensoes .html .pdf
```

🔍 **Simular apenas JSON e CSV:**
```bash
python Cleanfiles.py --dry-run --extensoes .json .csv
```

---

Deseja que eu adicione uma opção `--path` para poder rodar o script em outro diretório (fora da pasta atual)? Isso é útil se quiser limpar uma pasta diferente.

---

*Conversa exportada do ChatGPT*
*Processado em: 23/11/2025 23:05*