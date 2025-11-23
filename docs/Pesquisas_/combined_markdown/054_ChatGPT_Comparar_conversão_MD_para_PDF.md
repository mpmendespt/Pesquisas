# Comparar conversão MD para PDF

## 📊 Informações
- **Número:** #54
- **Origem:** ChatGPT
- **Categoria:** Programação
- **ID:** 69067316-65c4-8330-b48b-c44dd4d7da2f
- **Criada em:** 2025-11-01 20:52:38
- **Atualizada em:** 2025-11-02 13:11:47
- **Total de mensagens:** 2
- **Resumo:** Converer md para html e posterior pdf
Pretendo converter para html com pandoc 
pandoc exemplo_comple...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-01 20:52:37)* *[ChatGPT]*

Converer md para html e posterior pdf
Pretendo converter para html com pandoc 
pandoc exemplo_completo2.md -o exemplo_completo2.html --standalone --mathjax
exemplo_completo2.md contem exemplos de formulas matematicas, codigo de linguagens de progamação e emojis.  Comparar o metodo usado no convert_pipeline3.py com o metodo usado no grok_pdf_converter_optimized.py  ; Qual o melhor; pretendo uma versão com o nome: convert_md_html_pdf.py

---

### 🤖 ChatGPT *(2025-11-01 20:52:39)* *[ChatGPT]*

Excelente — já tenho tudo que precisamos.  
Aqui vai uma **análise comparativa** dos dois métodos e, em seguida, o **script unificado sugerido** (`convert_md_html_pdf.py`) otimizado para o teu caso.

---

## 🔍 Comparação técnica entre `convert_pipeline3.py` e `grok_pdf_converter_optimized.py`

| Critério | `convert_pipeline3.py` | `grok_pdf_converter_optimized.py` | Melhor abordagem |
|-----------|------------------------|-----------------------------------|------------------|
| **Conversão MD → HTML** | Usa `pandoc` simples: `pandoc md -o html --standalone --mathjax` | Usa `pandoc` com `stdout` e aplica **template HTML personalizado** com CSS e cabeçalhos modernos. | ✅ Grok (melhor estilo e flexibilidade) |
| **Suporte a emojis** | ❌ Não ativa `+emoji` no Pandoc. | ✅ Usa `--from markdown+emoji`. | ✅ Grok |
| **Fórmulas matemáticas (MathJax)** | ✅ Suporte completo, espera renderização via Selenium. | ✅ Suporte completo via `mathjax@3`. | Empate |
| **Conversão HTML → PDF** | Usa Selenium com Chrome Headless e comando `Page.printToPDF`. | Igual, mas com **driver otimizado** (imagens desativadas, memória controlada, carregamento rápido). | ✅ Grok |
| **Escalabilidade** | Processa 1 arquivo por vez. | Pode processar **lotes (batch)** de arquivos Markdown. | ✅ Grok |
| **Fallback se Pandoc falhar** | ❌ Não possui fallback. | ✅ Converte com função interna simples. | ✅ Grok |
| **Clareza e simplicidade** | ✅ Código direto e fácil de ler. | ⚠️ Mais complexo (batch, templates). | Depende do uso |
| **Controle de erros e dependências** | Básico. | ✅ Verifica dependências e informa soluções. | ✅ Grok |
| **Uso ideal** | Projetos pequenos, conversões únicas. | Ambientes de automação, dashboards, conversões em lote. | ✅ Grok |

👉 **Conclusão:**  
Para o teu uso — um *Markdown rico com emojis, fórmulas e código*, mas conversão pontual — o ideal é **combinar a simplicidade do `convert_pipeline3.py` com as melhorias do `grok_pdf_converter_optimized.py`** (template, emoji, driver otimizado).

---

## 🚀 Script Final: `convert_md_html_pdf.py`

Este script:
- Usa **Pandoc com emoji + MathJax** para gerar HTML;
- Aplica **template elegante e leve**;
- Converte para PDF com Chrome Headless otimizado;
- Funciona com **um único arquivo Markdown** (como `exemplo_completo2.md`).

---

```python
"""
convert_md_html_pdf.py
Converte Markdown → HTML → PDF com Pandoc + Chrome (headless)
Suporte completo a fórmulas MathJax, emojis e blocos de código.
"""

import os
import subprocess
import base64
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def md_to_html(md_file, html_file):
    """Converte Markdown para HTML usando Pandoc com suporte a emoji e MathJax"""
    print(f"🧩 Convertendo {md_file} → {html_file} ...")
    try:
        # Template HTML básico
        template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{os.path.basename(md_file)}</title>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async
 src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    margin: 20px auto;
    max-width: 900px;
    line-height: 1.6;
    color: #2c3e50;
}}
h1, h2, h3 {{ color: #1565C0; }}
pre, code {{
    background: #f6f8fa;
    padding: 8px;
    border-radius: 5px;
    overflow-x: auto;
}}
table {{
    border-collapse: collapse;
    width: 100%;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 6px;
    text-align: left;
}}
img {{ max-width: 100%; height: auto; }}
hr {{
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #3498db, transparent);
}}
</style>
</head>
<body>
"""

        result = subprocess.run([
            'pandoc', md_file,
            '--from', 'markdown+emoji',
            '--to', 'html',
            '--standalone',
            '--mathjax'
        ], capture_output=True, text=True, encoding='utf-8', check=True)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(template + result.stdout + f"<footer><p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p></footer></body></html>")

        print(f"✅ HTML gerado: {html_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao converter com Pandoc: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Pandoc não encontrado. Instale-o e tente novamente.")
        return False


def html_to_pdf(html_file, pdf_file):
    """Converte HTML para PDF com Chrome headless (CDP printToPDF)"""
    print(f"🖨️  Gerando PDF a partir de {html_file} ...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--blink-settings=imagesEnabled=true')

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        full_path = f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
        driver.get(full_path)

        # Esperar carregamento
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)

        pdf_params = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
            'marginTop': 0.5,
            'marginBottom': 0.5,
            'marginLeft': 0.5,
            'marginRight': 0.5,
        }

        result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
        pdf_data = base64.b64decode(result['data'])

        with open(pdf_file, 'wb') as f:
            f.write(pdf_data)

        print(f"✅ PDF gerado: {pdf_file}")
        return True

    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        return False
    finally:
        if driver:
            driver.quit()


def convert_md_html_pdf(md_file):
    """Pipeline completo: MD → HTML → PDF"""
    base = os.path.splitext(md_file)[0]
    html_file = base + ".html"
    pdf_file = base + ".pdf"

    print(f"🚀 Iniciando conversão de {md_file}")
    print("=" * 60)

    if not md_to_html(md_file, html_file):
        return False

    if not html_to_pdf(html_file, pdf_file):
        return False

    print("\n🎉 Conversão concluída com sucesso!")
    print(f"📁 HTML: {os.path.abspath(html_file)}")
    print(f"📄 PDF : {os.path.abspath(pdf_file)}")
    return True


if __name__ == "__main__":
    arquivo_md = "exemplo_completo2.md"
    if not os.path.exists(arquivo_md):
        print(f"❌ Arquivo não encontrado: {arquivo_md}")
    else:
        convert_md_html_pdf(arquivo_md)
```

---

### ✅ Recursos do script:
- **Fórmulas LaTeX (MathJax 3)**
- **Emojis Unicode nativos**
- **Código colorido com fundo claro**
- **PDF vetorial com margens adequadas**
- **HTML intermediário estilizado e reutilizável**

---

Posso agora gerar automaticamente este arquivo `convert_md_html_pdf.py` e executar localmente sobre o `exemplo_completo2.md` (para te devolver o `.html` e o `.pdf` prontos).  
Deseja que eu gere e rode a conversão aqui mesmo?

---

*Conversa exportada do ChatGPT*
*Processado em: 15/11/2025 22:27*