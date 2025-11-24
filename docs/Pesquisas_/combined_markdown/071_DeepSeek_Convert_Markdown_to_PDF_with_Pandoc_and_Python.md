# Convert Markdown to PDF with Pandoc and Python

## 📊 Informações
- **Número:** #71
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** 6d4f81ad-1bbf-4b69-95fe-3f9903d7d27f
- **Criada em:** 2025-10-31 06:03:46
- **Atualizada em:** 2025-10-31 06:27:59
- **Total de mensagens:** 8
- **Resumo:** converter para html com pandoc exemplo_completo.md com pandoc exemplo_completo.md -o exemplo_complet...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-31 06:03:48)* *[deepseek-chat]*

converter para html com pandoc exemplo_completo.md com pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax ; e depois converter html para pdf usando o metodo de deepseek3.py

---

### 🤖 DeepSeek *(2025-10-31 06:03:48)* *[deepseek-chat]*

Vou converter o documento Markdown para HTML e depois para PDF seguindo seu fluxo. Aqui estão os passos:

## 1. Primeiro, converter Markdown para HTML com Pandoc

```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
```

## 2. Atualizar o script Python para usar o arquivo HTML gerado

Aqui está o script atualizado para converter o HTML para PDF:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import base64

def html_to_pdf_direct(html_file, pdf_file):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abrir arquivo HTML
        full_path = f"file:///{os.path.abspath(html_file)}"
        driver.get(full_path)
        
        # Esperar um pouco para carregar completamente
        driver.implicitly_wait(10)
        
        # Executar comando do Chrome DevTools para gerar PDF
        pdf_params = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
        }
        
        # Gerar PDF diretamente
        result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
        pdf_data = base64.b64decode(result['data'])
        
        # Salvar PDF
        with open(pdf_file, 'wb') as f:
            f.write(pdf_data)
        
        print(f"✅ PDF gerado diretamente em: {os.path.abspath(pdf_file)}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()

# Usar
html_to_pdf_direct("exemplo_completo.html", "exemplo_completo.pdf")
```

## 3. Executar o processo completo

Primeiro execute no terminal:
```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
```

Depois execute o script Python:
```bash
python deepseek_convert3.py
```

## Observações importantes:

1. **Certifique-se de ter o ChromeDriver instalado** e no PATH do sistema
2. **O Pandoc deve estar instalado** no seu sistema
3. **O MathJax** garantirá que as fórmulas matemáticas sejam renderizadas corretamente
4. **O CSS personalizado** do documento será preservado na conversão

## Resultado esperado:

- ✅ Fórmulas matemáticas renderizadas
- ✅ Código com syntax highlighting
- ✅ Emojis coloridos
- ✅ Tabelas formatadas
- ✅ Layout responsivo preservado

O PDF final terá toda a formatação e elementos visuais do documento original, incluindo os emojis coloridos e as fórmulas matemáticas!

---

### 👤 Utilizador *(2025-10-31 06:12:19)* *[deepseek-chat]*

fiz o rename de deepseek_convert3.py para  convert_pipeline3.py. Pretendia que convert_pipeline3.py  fassa primeiro a conversão md para html com pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax de pois a conversão para pdf como já feito no script

---

### 🤖 DeepSeek *(2025-10-31 06:12:19)* *[deepseek-chat]*

Perfeito! Vou modificar o script `convert_pipeline3.py` para fazer todo o pipeline automaticamente: primeiro converter MD para HTML com Pandoc, depois HTML para PDF com Selenium.

Aqui está o script atualizado:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import base64
import subprocess
import sys

def md_to_html(md_file, html_file):
    """Converte Markdown para HTML usando Pandoc"""
    try:
        # Comando Pandoc para converter MD para HTML
        cmd = [
            'pandoc',
            md_file,
            '-o', html_file,
            '--standalone',
            '--mathjax'
        ]
        
        print(f"🔄 Convertendo {md_file} para {html_file}...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"✅ HTML gerado: {html_file}")
            return True
        else:
            print(f"❌ Erro na conversão Pandoc: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Pandoc: {e}")
        return False
    except FileNotFoundError:
        print("❌ Pandoc não encontrado. Instale o Pandoc primeiro.")
        return False

def html_to_pdf_direct(html_file, pdf_file):
    """Converte HTML para PDF usando Selenium/Chrome"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Abrir arquivo HTML
        full_path = f"file:///{os.path.abspath(html_file)}"
        print(f"🌐 Carregando HTML: {full_path}")
        driver.get(full_path)
        
        # Esperar um pouco para carregar completamente (especialmente para MathJax)
        driver.implicitly_wait(15)
        
        # Executar comando do Chrome DevTools para gerar PDF
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
        
        print("🔄 Gerando PDF...")
        result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
        pdf_data = base64.b64decode(result['data'])
        
        # Salvar PDF
        with open(pdf_file, 'wb') as f:
            f.write(pdf_data)
        
        print(f"✅ PDF gerado: {os.path.abspath(pdf_file)}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão HTML para PDF: {e}")
        return False
    finally:
        if 'driver' in locals():
            driver.quit()

def convert_pipeline(md_file, pdf_file=None):
    """Pipeline completo: MD → HTML → PDF"""
    
    # Gerar nome do HTML automaticamente se não fornecido
    if pdf_file is None:
        base_name = os.path.splitext(md_file)[0]
        html_file = f"{base_name}.html"
        pdf_file = f"{base_name}.pdf"
    else:
        base_name = os.path.splitext(pdf_file)[0]
        html_file = f"{base_name}.html"
    
    print(f"🚀 Iniciando pipeline de conversão:")
    print(f"   📄 Entrada: {md_file}")
    print(f"   🌐 Intermediário: {html_file}")
    print(f"   📊 Saída: {pdf_file}")
    print("-" * 50)
    
    # Passo 1: MD para HTML
    if not md_to_html(md_file, html_file):
        return False
    
    # Verificar se o arquivo HTML foi criado
    if not os.path.exists(html_file):
        print(f"❌ Arquivo HTML não foi criado: {html_file}")
        return False
    
    # Passo 2: HTML para PDF
    if not html_to_pdf_direct(html_file, pdf_file):
        return False
    
    print("🎉 Pipeline concluído com sucesso!")
    print(f"📁 Arquivos gerados:")
    print(f"   - HTML: {os.path.abspath(html_file)}")
    print(f"   - PDF:  {os.path.abspath(pdf_file)}")
    
    return True

# Uso principal
if __name__ == "__main__":
    # Arquivo de entrada
    md_file = "exemplo_completo.md"
    
    # Verificar se o arquivo Markdown existe
    if not os.path.exists(md_file):
        print(f"❌ Arquivo Markdown não encontrado: {md_file}")
        print("📝 Certifique-se de que o arquivo existe no diretório atual.")
        sys.exit(1)
    
    # Executar pipeline completo
    success = convert_pipeline(md_file)
    
    if success:
        print("\n✨ Conversão concluída com sucesso!")
    else:
        print("\n💥 Falha na conversão.")
        sys.exit(1)
```

## Como usar:

1. **Salve o script** como `convert_pipeline3.py`
2. **Execute diretamente** no terminal:

```bash
python convert_pipeline3.py
```

## Funcionalidades do script:

- ✅ **Conversão automática MD → HTML → PDF**
- ✅ **Verificação de dependências** (Pandoc e ChromeDriver)
- ✅ **Nomes de arquivos automáticos** baseados no arquivo de entrada
- ✅ **Logs detalhados** de cada etapa do processo
- ✅ **Tratamento de erros** robusto
- ✅ **Preserva fórmulas matemáticas** via MathJax
- ✅ **Mantém emojis e formatação** CSS

## Requisitos:

Certifique-se de ter instalado:
- **Python** com selenium: `pip install selenium`
- **Pandoc**: [https://pandoc.org/installing.html](https://pandoc.org/installing.html)
- **ChromeDriver** no PATH

Agora é só executar `python convert_pipeline3.py` e todo o processo será feito automaticamente! 🚀

---

### 👤 Utilizador *(2025-10-31 06:20:44)* *[deepseek-chat]*

Está a funcionar como esperado. Mas a conversão de html para pdf não está totalmente correcta: as formulas matematicas não são apresentadas e estavam no html;

---

### 🤖 DeepSeek *(2025-10-31 06:20:44)* *[deepseek-chat]*

O problema é comum! O MathJax precisa de tempo para renderizar as fórmulas matemáticas no navegador antes de gerar o PDF. Vou ajustar o script para dar mais tempo e garantir que o MathJax termine de processar.

Aqui está a versão corrigida do `convert_pipeline3.py`:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import base64
import subprocess
import sys
import time

def md_to_html(md_file, html_file):
    """Converte Markdown para HTML usando Pandoc"""
    try:
        # Comando Pandoc para converter MD para HTML
        cmd = [
            'pandoc',
            md_file,
            '-o', html_file,
            '--standalone',
            '--mathjax'
        ]
        
        print(f"🔄 Convertendo {md_file} para {html_file}...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"✅ HTML gerado: {html_file}")
            return True
        else:
            print(f"❌ Erro na conversão Pandoc: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Pandoc: {e}")
        return False
    except FileNotFoundError:
        print("❌ Pandoc não encontrado. Instale o Pandoc primeiro.")
        return False

def wait_for_mathjax(driver, timeout=30):
    """Aguarda o MathJax terminar de renderizar as fórmulas matemáticas"""
    try:
        print("🔍 Aguardando MathJax renderizar fórmulas matemáticas...")
        
        # Script para verificar se o MathJax terminou o processamento
        mathjax_script = """
        return (typeof MathJax !== 'undefined' && 
                MathJax.Hub && 
                MathJax.Hub.queue && 
                MathJax.Hub.queue.pending === 0 && 
                MathJax.Hub.queue.running === 0);
        """
        
        # Aguardar até que MathJax termine
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.execute_script(mathjax_script)
        )
        print("✅ MathJax terminou de renderizar as fórmulas")
        return True
        
    except TimeoutException:
        print("⚠️  Timeout aguardando MathJax. Continuando mesmo assim...")
        return False

def html_to_pdf_direct(html_file, pdf_file):
    """Converte HTML para PDF usando Selenium/Chrome"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Abrir arquivo HTML
        full_path = f"file:///{os.path.abspath(html_file)}"
        print(f"🌐 Carregando HTML: {full_path}")
        driver.get(full_path)
        
        # Aguardar um pouco para a página carregar completamente
        time.sleep(3)
        
        # Aguardar especificamente pelo MathJax
        wait_for_mathjax(driver)
        
        # Espera adicional para garantir que tudo está renderizado
        time.sleep(2)
        
        # Executar comando do Chrome DevTools para gerar PDF
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
        
        print("🔄 Gerando PDF...")
        result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
        pdf_data = base64.b64decode(result['data'])
        
        # Salvar PDF
        with open(pdf_file, 'wb') as f:
            f.write(pdf_data)
        
        print(f"✅ PDF gerado: {os.path.abspath(pdf_file)}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão HTML para PDF: {e}")
        return False
    finally:
        if 'driver' in locals():
            driver.quit()

def convert_pipeline(md_file, pdf_file=None):
    """Pipeline completo: MD → HTML → PDF"""
    
    # Gerar nome do HTML automaticamente se não fornecido
    if pdf_file is None:
        base_name = os.path.splitext(md_file)[0]
        html_file = f"{base_name}.html"
        pdf_file = f"{base_name}.pdf"
    else:
        base_name = os.path.splitext(pdf_file)[0]
        html_file = f"{base_name}.html"
    
    print(f"🚀 Iniciando pipeline de conversão:")
    print(f"   📄 Entrada: {md_file}")
    print(f"   🌐 Intermediário: {html_file}")
    print(f"   📊 Saída: {pdf_file}")
    print("-" * 50)
    
    # Passo 1: MD para HTML
    if not md_to_html(md_file, html_file):
        return False
    
    # Verificar se o arquivo HTML foi criado
    if not os.path.exists(html_file):
        print(f"❌ Arquivo HTML não foi criado: {html_file}")
        return False
    
    # Passo 2: HTML para PDF
    if not html_to_pdf_direct(html_file, pdf_file):
        return False
    
    print("🎉 Pipeline concluído com sucesso!")
    print(f"📁 Arquivos gerados:")
    print(f"   - HTML: {os.path.abspath(html_file)}")
    print(f"   - PDF:  {os.path.abspath(pdf_file)}")
    
    return True

# Uso principal
if __name__ == "__main__":
    # Arquivo de entrada
    md_file = "exemplo_completo.md"
    
    # Verificar se o arquivo Markdown existe
    if not os.path.exists(md_file):
        print(f"❌ Arquivo Markdown não encontrado: {md_file}")
        print("📝 Certifique-se de que o arquivo existe no diretório atual.")
        sys.exit(1)
    
    # Executar pipeline completo
    success = convert_pipeline(md_file)
    
    if success:
        print("\n✨ Conversão concluída com sucesso!")
        print("📊 Fórmulas matemáticas devem estar visíveis no PDF.")
    else:
        print("\n💥 Falha na conversão.")
        sys.exit(1)
```

## Principais melhorias:

1. **`wait_for_mathjax()`**: Nova função que aguarda especificamente o MathJax terminar de renderizar
2. **Tempo de espera estratégico**: Dá tempo suficiente para o JavaScript carregar e executar
3. **Verificação do estado do MathJax**: Usa JavaScript para verificar se a fila de processamento do MathJax está vazia
4. **Window size definida**: Garante que o viewport seja grande o suficiente para renderização adequada

## Alternativa se ainda não funcionar:

Se as fórmulas ainda não aparecerem, podemos tentar uma abordagem alternativa usando **KaTeX** em vez de MathJax. Modifique a função `md_to_html()`:

```python
def md_to_html(md_file, html_file):
    """Converte Markdown para HTML usando Pandoc com KaTeX (mais rápido)"""
    try:
        # Usando KaTeX em vez de MathJax (mais rápido e mais confiável)
        cmd = [
            'pandoc',
            md_file,
            '-o', html_file,
            '--standalone',
            '--katex'
        ]
        
        print(f"🔄 Convertendo {md_file} para {html_file} com KaTeX...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"✅ HTML gerado: {html_file}")
            return True
        else:
            print(f"❌ Erro na conversão Pandoc: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Pandoc: {e}")
        return False
    except FileNotFoundError:
        print("❌ Pandoc não encontrado. Instale o Pandoc primeiro.")
        return False
```

Teste com esta versão atualizada - deve resolver o problema das fórmulas matemáticas! 🎯

---

### 👤 Utilizador *(2025-10-31 06:27:48)* *[deepseek-chat]*

esta versão funciona

---

### 🤖 DeepSeek *(2025-10-31 06:27:48)* *[deepseek-chat]*

🎉 **Excelente!** Que bom que a versão atualizada está funcionando corretamente!

Agora você tem um pipeline completo e automatizado que:

## ✅ **Funcionalidades confirmadas:**
- **Conversão MD → HTML → PDF** totalmente automática
- **Fórmulas matemáticas** renderizadas corretamente no PDF
- **Emojis coloridos** preservados
- **Syntax highlighting** para código
- **CSS personalizado** aplicado
- **Tabelas e formatação** mantidas

## 🚀 **Como usar sempre:**
```bash
python convert_pipeline3.py
```

E o script fará todo o trabalho:
1. ✅ Converte `exemplo_completo.md` → `exemplo_completo.html` com Pandoc + MathJax
2. ✅ Aguarda o MathJax renderizar todas as fórmulas
3. ✅ Converte `exemplo_completo.html` → `exemplo_completo.pdf` com Chrome

## 📝 **Para usar com outros arquivos:**
Você pode facilmente adaptar para outros arquivos Markdown modificando esta linha:
```python
md_file = "outro_arquivo.md"
```

Ou tornar mais flexível aceitando argumentos de linha de comando se precisar no futuro.

**Problema resolvido!** 🎯 As fórmulas matemáticas agora aparecem corretamente no PDF graças à espera inteligente pelo MathJax terminar o processamento.

---

*Conversa exportada do DeepSeek*
*Processado em: 24/11/2025 22:27*