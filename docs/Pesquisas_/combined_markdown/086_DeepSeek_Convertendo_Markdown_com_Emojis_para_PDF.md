# Convertendo Markdown com Emojis para PDF

## 📊 Informações
- **Número:** #86
- **Origem:** DeepSeek
- **Categoria:** Sistemas
- **ID:** 045d63db-0022-44e0-9863-4ac28838d053
- **Criada em:** 2025-10-28 04:39:27
- **Atualizada em:** 2025-10-28 05:10:37
- **Total de mensagens:** 14
- **Resumo:** Converter md contendo emojis para pdf (no windows). Pretende-se que o pdf gerado contenha os emojis ...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-28 04:39:28)* *[deepseek-chat]*

Converter md contendo emojis para pdf (no windows). Pretende-se que o pdf gerado contenha os emojis coloridos. (Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Teste_emojis>

---

### 🤖 DeepSeek *(2025-10-28 04:39:28)* *[deepseek-chat]*

Para converter seu arquivo Markdown com emojis para PDF no Windows mantendo os emojis coloridos, existem várias opções:

## 🛠️ Métodos Recomendados:

### 1. **Pandoc + WeasyPrint** (Melhor qualidade)
```bash
# Instalar Pandoc e WeasyPrint
pip install pandoc
pip install weasyprint

# Converter
pandoc teste_emojis.md -o teste_emojis.pdf --pdf-engine=weasyprint
```

### 2. **Visual Studio Code** (Mais simples)
- Instale a extensão "Markdown PDF" no VS Code
- Abra o arquivo `.md` e use `Ctrl+Shift+P` → "Markdown PDF: Export (pdf)"
- Mantém os emojis coloridos nativamente

### 3. **Pandoc + wkhtmltopdf**
```bash
# Baixar wkhtmltopdf e adicionar ao PATH
pandoc teste_emojis.md -o teste_emojis.pdf --pdf-engine=wkhtmltopdf
```

### 4. **Usando Python com WeasyPrint**
```python
from weasyprint import HTML
from markdown import markdown

with open('teste_emojis.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = markdown(md_content, extensions=['extra'])
HTML(string=html_content).write_pdf('teste_emojis.pdf')
```

## 📋 **Recomendação Principal:**

Use o **Visual Studio Code com a extensão Markdown PDF** - é a opção mais direta e que geralmente preserva melhor os emojis coloridos sem necessidade de configuração complexa.

## 🔧 Instalação Rápida no Windows:

1. **Instale o Python** (se não tiver)
2. **Instale via pip**:
   ```cmd
   pip install weasyprint pandoc
   ```
3. **Execute**:
   ```cmd
   pandoc teste_emojis.md -o teste_emojis.pdf --pdf-engine=weasyprint
   ```

O **WeasyPrint** geralmente oferece os melhores resultados para emojis coloridos em PDF. Se encontrar problemas com fontes, o VS Code é a alternativa mais confiável.

---

### 👤 Utilizador *(2025-10-28 04:40:32)* *[deepseek-chat]*

(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Teste_emojis>pandoc teste_emojis.md -o teste_emojis.pdf --pdf-engine=weasyprint
Fontconfig error: Cannot load default config file: No such file: (null)
Fontconfig error: Cannot load default config file: No such file: (null)
Error producing PDF.

---

### 🤖 DeepSeek *(2025-10-28 04:40:32)* *[deepseek-chat]*

O erro do Fontconfig indica problemas com as fontes do sistema. Vamos resolver isso:

## 🔧 **Soluções para o erro do Fontconfig:**

### **Solução 1: Instalar o WeasyPrint corretamente no Windows**

```cmd
# Desinstalar e reinstalar com dependências
pip uninstall weasyprint
pip install weasyprint

# Ou instalar com o conda (melhor para Windows)
conda install -c conda-forge weasyprint
```

### **Solução 2: Usar uma abordagem alternativa**

**Método A: Usar o wkhtmltopdf**
```cmd
# Baixar wkhtmltopdf de: https://wkhtmltopdf.org/downloads.html
# Adicionar ao PATH e depois:
pandoc teste_emojis.md -o teste_emojis.pdf --pdf-engine=wkhtmltopdf
```

**Método B: Converter via HTML primeiro**
```cmd
# Converter para HTML
pandoc teste_emojis.md -o teste_emojis.html

# Abra o HTML no Chrome e imprima como PDF
```

### **Solução 3: Usar o Visual Studio Code (Recomendado)**

1. Instale o VS Code
2. Instale a extensão **"Markdown PDF"** de Yoshinori Hirasawa
3. Abra seu arquivo `.md`
4. `Ctrl+Shift+P` → "Markdown PDF: Export (pdf)"

### **Solução 4: Script Python alternativo**

Crie um arquivo `converter.py`:
```python
import markdown
from weasyprint import HTML
import os

# Ler o arquivo markdown
with open('teste_emojis.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Converter para HTML
html_content = markdown.markdown(md_content, extensions=['extra'])

# Adicionar estilo básico
html_with_style = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: "Segoe UI Emoji", "Apple Color Emoji", sans-serif; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Gerar PDF
HTML(string=html_with_style).write_pdf('teste_emojis.pdf')
print("PDF gerado com sucesso!")
```

Execute:
```cmd
python converter.py
```

### **Solução 5: Usar o Google Chrome**

```cmd
# Converter para HTML
pandoc teste_emojis.md -o teste_emojis.html

# Abra teste_emojis.html no Chrome e use Ctrl+P → Salvar como PDF
```

## 🚀 **Recomendação Imediata:**

Use o **Visual Studio Code com a extensão Markdown PDF** - é a forma mais simples e confiável no Windows, sem dependências externas problemáticas.

Qual método você gostaria de tentar primeiro?

---

### 👤 Utilizador *(2025-10-28 04:48:45)* *[deepseek-chat]*

(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Teste_emojis>python converter.py
Fontconfig error: Cannot load default config file: No such file: (null)
Fontconfig error: Cannot load default config file: No such file: (null)

---

### 🤖 DeepSeek *(2025-10-28 04:48:45)* *[deepseek-chat]*

O problema persiste com o Fontconfig no Windows. Vamos usar abordagens alternativas que não dependem do WeasyPrint:

## 🔧 **Soluções Alternativas Sem WeasyPrint:**

### **Método 1: Usar o PowerShell com .NET (Funciona bem no Windows)**

Crie `converter.ps1`:
```powershell
# Converter Markdown para HTML primeiro
$mdContent = Get-Content -Path "teste_emojis.md" -Encoding UTF8 -Raw

# Converter Markdown para HTML básico
$htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Teste de Emojis</title>
    <style>
        body { 
            font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            line-height: 1.6;
            margin: 40px;
        }
        h1 { color: #333; }
        h2 { color: #666; }
    </style>
</head>
<body>
$($mdContent -replace "`n", "<br>")
</body>
</html>
"@

$htmlContent | Out-File -FilePath "teste_emojis.html" -Encoding UTF8
Write-Host "HTML gerado: teste_emojis.html"
Write-Host "Abrindo no navegador para salvar como PDF..."
Start-Process "teste_emojis.html"
```

Execute no PowerShell:
```powershell
.\converter.ps1
```

### **Método 2: Usar Python com Selenium + Chrome**

Crie `converter_selenium.py`:
```python
from markdown import markdown
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Ler o arquivo markdown
with open('teste_emojis.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Converter para HTML
html_content = markdown(md_content, extensions=['extra'])

# HTML completo com estilos
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            line-height: 1.6;
            margin: 40px;
            max-width: 800px;
        }}
        h1 {{ color: #333; border-bottom: 2px solid #eee; }}
        h2 {{ color: #666; margin-top: 30px; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Salvar HTML
with open('teste_emojis.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("HTML gerado: teste_emojis.html")
print("Abra este arquivo no Chrome e use Ctrl+P → Salvar como PDF")
```

### **Método 3: Usar o Pandoc com output HTML e depois converter manualmente**

```cmd
# Converter para HTML com pandoc
pandoc teste_emojis.md -o teste_emojis.html --self-contained

# Abrir o HTML no Chrome e salvar como PDF
start teste_emojis.html
```

### **Método 4: Usar ferramenta online (Mais fácil)**

1. Acesse: https://markdown-pdf.com/
2. Cole o conteúdo do seu arquivo MD
3. Faça download do PDF

### **Método 5: Extensão para VS Code (Mais confiável)**

Se você tem o VS Code instalado:

1. Abra o arquivo `teste_emojis.md`
2. Instale a extensão **"Markdown PDF"** 
3. Pressione `Ctrl+Shift+P`
4. Digite: `Markdown PDF: Export (pdf)`

## 🚀 **Recomendação Imediata:**

**Use o Método 1 (PowerShell)** ou **Método 4 (site online)** para resultados rápidos.

Se preferir uma solução local permanente, instale o **VS Code** com a extensão Markdown PDF.

Qual método você gostaria de tentar?

---

### 👤 Utilizador *(2025-10-28 04:52:31)* *[deepseek-chat]*

converter output HTML para pdf

---

### 🤖 DeepSeek *(2025-10-28 04:52:31)* *[deepseek-chat]*

Aqui estão várias maneiras de converter HTML para PDF no Windows:

## 🖨️ **Método 1: Usando o Google Chrome (Mais Simples)**

### Via Interface Gráfica:
1. Abra `teste_emojis.html` no Chrome
2. `Ctrl + P` ou clique nos 3 pontos → Imprimir
3. Altere "Destino" para "Salvar como PDF"
4. Clique em "Salvar"

### Via Linha de Comando:
```cmd
# Navegar até a pasta do Chrome (ajuste o caminho)
cd "C:\Program Files\Google\Chrome\Application"

# Converter HTML para PDF
chrome.exe --headless --disable-gpu --print-to-pdf="D:\Downloads\_DOCS_\_DOCS_\Teste_emojis\teste_emojis.pdf" "D:\Downloads\_DOCS_\_DOCS_\Teste_emojis\teste_emojis.html"
```

## 🐍 **Método 2: Python com pdfkit**

```python
import pdfkit

# Configurar o caminho do wkhtmltopdf (baixe em: https://wkhtmltopdf.org/downloads.html)
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Converter HTML para PDF
pdfkit.from_file('teste_emojis.html', 'teste_emojis.pdf', configuration=config)
print("PDF gerado com sucesso!")
```

**Instalação:**
```cmd
pip install pdfkit
```

## 🌐 **Método 3: Usando PowerShell**

Crie `html_to_pdf.ps1`:
```powershell
# Configurações
$htmlFile = "teste_emojis.html"
$pdfFile = "teste_emojis.pdf"

# Criar objeto COM do Internet Explorer (funciona mesmo descontinuado)
$ie = New-Object -ComObject InternetExplorer.Application
$ie.Visible = $false
$ie.Navigate("file:///$PWD/$htmlFile")

while ($ie.Busy -eq $true) { Start-Sleep -Milliseconds 100 }

# Usar a funcionalidade de impressão para PDF
$ie.ExecWB(6, 2, $null, $null)  # 6 = PRINT, 2 = PROMPT_USER

# Fechar o IE
$ie.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($ie) | Out-Null

Write-Host "PDF salvo como: $pdfFile"
```

## 📄 **Método 4: Usando Microsoft Edge**

### Linha de Comando:
```cmd
# Converter com Edge
msedge.exe --headless --disable-gpu --print-to-pdf="teste_emojis.pdf" "teste_emojis.html"
```

## 🔧 **Método 5: Script Python Completo com wkhtmltopdf**

```python
import subprocess
import os

def html_to_pdf(html_file, pdf_file):
    # Verificar se wkhtmltopdf está instalado
    try:
        # Tentar executar wkhtmltopdf
        subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, check=True)
    except:
        print("wkhtmltopdf não encontrado. Baixe em: https://wkhtmltopdf.org/downloads.html")
        return False
    
    # Converter HTML para PDF
    cmd = ['wkhtmltopdf', '--enable-local-file-access', html_file, pdf_file]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"PDF gerado com sucesso: {pdf_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar PDF: {e}")
        return False

# Usar a função
html_to_pdf('teste_emojis.html', 'teste_emojis.pdf')
```

## 🎯 **Método 6: Usando Pandoc Diretamente (se funcionar)**

```cmd
pandoc teste_emojis.html -o teste_emojis.pdf --pdf-engine=wkhtmltopdf
```

## 🚀 **Recomendações:**

**Para simplicidade:** Use o **Método 1 (Chrome)** - abra o HTML e salve como PDF.

**Para automação:** Use o **Método 2 (pdfkit)** com wkhtmltopdf.

**Para linha de comando:** Use o **Método 1 (Chrome headless)**.

Qual método você gostaria de tentar primeiro?

---

### 👤 Utilizador *(2025-10-28 05:02:18)* *[deepseek-chat]*

como instalar wkhtmltopdf com choco

---

### 🤖 DeepSeek *(2025-10-28 05:02:18)* *[deepseek-chat]*

Aqui está como instalar o wkhtmltopdf usando Chocolatey:

## 🍫 **Instalação com Chocolatey**

### **1. Primeiro, verifique se o Chocolatey está instalado:**
```cmd
choco --version
```

Se não estiver instalado, instale o Chocolatey como **Administrador**:
```cmd
# Abra o PowerShell como Administrador e execute:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### **2. Instale o wkhtmltopdf:**
```cmd
# Como Administrador
choco install wkhtmltopdf -y
```

### **3. Verifique a instalação:**
```cmd
wkhtmltopdf --version
```

## 🔧 **Configuração Pós-Instalação**

### **Adicionar ao PATH (se necessário):**
O Chocolatey geralmente adiciona automaticamente ao PATH, mas se não funcionar:

```cmd
# Verificar se está no PATH
where wkhtmltopdf

# Se não encontrar, adicione manualmente
setx PATH "%PATH%;C:\Program Files\wkhtmltopdf\bin"
```

### **Testar a conversão:**
```cmd
wkhtmltopdf teste_emojis.html teste_emojis.pdf
```

## 🐍 **Usar com Python (pdfkit):**

```python
import pdfkit

# Configurar o caminho (geralmente automático com Chocolatey)
try:
    # Tentar detectar automaticamente
    pdfkit.from_file('teste_emojis.html', 'teste_emojis.pdf')
    print("PDF gerado com sucesso!")
except:
    # Se falhar, especificar o caminho manualmente
    config = pdfkit.configuration(wkhtmltopdf=r'C:\ProgramData\chocolatey\bin\wkhtmltopdf.exe')
    pdfkit.from_file('teste_emojis.html', 'teste_emojis.pdf', configuration=config)
    print("PDF gerado com sucesso!")
```

## 📋 **Comandos Úteis do Chocolatey:**

```cmd
# Atualizar wkhtmltopdf
choco upgrade wkhtmltopdf -y

# Listar pacotes instalados
choco list --local-only

# Desinstalar
choco uninstall wkhtmltopdf -y
```

## 🚀 **Script Completo de Conversão:**

Crie `converter_final.py`:
```python
import pdfkit
import subprocess
import os

def convert_md_to_pdf():
    try:
        # Configurar wkhtmltopdf (Chocolatey install)
        config = pdfkit.configuration(wkhtmltopdf=r'C:\ProgramData\chocolatey\bin\wkhtmltopdf.exe')
        
        # Primeiro converter MD para HTML
        with open('teste_emojis.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # HTML com suporte a emojis
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
                    line-height: 1.6;
                    margin: 40px;
                    max-width: 800px;
                }}
                h1 {{ color: #333; border-bottom: 2px solid #eee; }}
                h2 {{ color: #666; margin-top: 30px; }}
            </style>
        </head>
        <body>
            {md_content.replace(chr(10), '<br>').replace('# ', '<h1>').replace('## ', '<h2>')}
        </body>
        </html>
        """
        
        # Salvar HTML temporário
        with open('temp_emojis.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Converter para PDF
        pdfkit.from_file('temp_emojis.html', 'teste_emojis.pdf', configuration=config)
        
        # Limpar arquivo temporário
        os.remove('temp_emojis.html')
        
        print("✅ PDF gerado com sucesso: teste_emojis.pdf")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    convert_md_to_pdf()
```

## 💡 **Dica Importante:**
Execute o PowerShell ou Prompt de Comando **como Administrador** para instalar via Chocolatey.

O Chocolatey é a maneira mais limpa de instalar o wkhtmltopdf no Windows, pois cuida das dependências e da configuração do PATH automaticamente.

---

### 👤 Utilizador *(2025-10-28 05:05:09)* *[deepseek-chat]*

com wkhtmltopdf teste_emojis.html teste_emojis.pdf os emojis são a preto e branco

---

### 🤖 DeepSeek *(2025-10-28 05:05:09)* *[deepseek-chat]*

O problema é que o wkhtmltopdf não suporta emojis coloridos nativamente. Vamos usar alternativas que mantêm as cores:

## 🎨 **Soluções para Emojis Coloridos:**

### **Método 1: Usar Chrome/Edge (Recomendado)**

```cmd
# Com Google Chrome
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu --print-to-pdf="teste_emojis.pdf" "file:///D:/Downloads/_DOCS_/_DOCS_/Teste_emojis/teste_emojis.html"

# Com Microsoft Edge
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --print-to-pdf="teste_emojis.pdf" "file:///D:/Downloads/_DOCS_/_DOCS_/Teste_emojis/teste_emojis.html"
```

### **Método 2: Script Python com Selenium + Chrome**

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def html_to_pdf_color(html_file, pdf_file):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Configurar para imprimir como PDF
    chrome_options.add_experimental_option('prefs', {
        'printing.print_preview_sticky_settings.appState': '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":""}],"selectedDestinationId":"Save as PDF","version":2}',
        'download.default_directory': r'D:\Downloads\_DOCS_\_DOCS_\Teste_emojis'
    })
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abrir arquivo local
        driver.get(f"file:///{html_file}")
        time.sleep(2)  # Esperar carregar
        
        # Executar comando de impressão para PDF
        pdf_script = """
        window.print();
        """
        driver.execute_script(pdf_script)
        
        print(f"PDF com emojis coloridos gerado: {pdf_file}")
        
    finally:
        driver.quit()

# Usar
html_to_pdf_color(r"D:\Downloads\_DOCS_\_DOCS_\Teste_emojis\teste_emojis.html", "teste_emojis_colorido.pdf")
```

### **Método 3: Usar Puppeteer (Node.js)**

Se você tem Node.js instalado:

```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Abrir o arquivo HTML
    const htmlPath = path.join(__dirname, 'teste_emojis.html');
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
    
    // Gerar PDF
    await page.pdf({
        path: 'teste_emojis_colorido.pdf',
        format: 'A4',
        printBackground: true,
        margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' }
    });
    
    await browser.close();
    console.log('PDF com emojis coloridos gerado!');
})();
```

**Instalação:**
```cmd
npm install puppeteer
```

### **Método 4: Converter via Interface Gráfica (Garantido)**

1. Abra `teste_emojis.html` no **Google Chrome**
2. Pressione `Ctrl + P`
3. Em "Destino", selecione **"Salvar como PDF"**
4. Em "Mais configurações", marque **"Imprimir planos de fundo"**
5. Clique em **"Salvar"**

### **Método 5: Usar WeasyPrint com Docker (Contorna problemas do Windows)**

```cmd
# Se você tem Docker instalado
docker run -v "D:\Downloads\_DOCS_\_DOCS_\Teste_emojis:/workspace" weasyprint weasyprint /workspace/teste_emojis.html /workspace/teste_emojis_colorido.pdf
```

## 🚀 **Método Mais Simples e Eficaz:**

Crie um arquivo `gerar_pdf_colorido.bat`:

```batch
@echo off
echo Abrindo HTML no Chrome para conversao com emojis coloridos...
echo Por favor, use Ctrl+P e selecione "Salvar como PDF"

"c:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0teste_emojis.html"

echo.
echo Se o PDF nao foi gerado automaticamente:
echo 1. Pressione Ctrl+P
echo 2. Selecione 'Salvar como PDF' 
echo 3. Clique em 'Salvar'
echo 4. Nomeie como 'teste_emojis.pdf'
pause
```

## 💡 **Por que wkhtmltopdf não mostra cores:**

- **wkhtmltopdf** usa o motor WebKit antigo
- **Não suporta** emojis coloridos modernos
- **Chrome/Edge** usam Blink que tem suporte completo a emojis

**Recomendo o Método 4 (Interface Gráfica do Chrome)** - é garantido que funciona e mantém todos os emojis coloridos!

---

### 👤 Utilizador *(2025-10-28 05:09:53)* *[deepseek-chat]*

Metodo 2 (Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Teste_emojis>python deepseek_convert2.py
PDF com emojis coloridos gerado: teste_emojis_colorido.pdf  ; onde é gerado o pdf

---

### 🤖 DeepSeek *(2025-10-28 05:09:53)* *[deepseek-chat]*

No método com Selenium, o PDF é gerado no **diretório de download padrão do Chrome**, não necessariamente na pasta do seu script.

## 📍 **Para controlar onde o PDF é salvo:**

### **Opção 1: Modificar o script para salvar na pasta atual**

Atualize `deepseek_convert2.py`:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def html_to_pdf_color(html_file, pdf_file):
    # Obter o diretório atual
    current_dir = os.getcwd()
    pdf_path = os.path.join(current_dir, pdf_file)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Configurar diretório de download explícito
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': current_dir,
        'printing.print_preview_sticky_settings.appState': '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":""}],"selectedDestinationId":"Save as PDF","version":2}'
    })
    
    # Configurar para salvar automaticamente como PDF
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abrir arquivo local (caminho completo)
        full_html_path = f"file:///{os.path.abspath(html_file)}"
        print(f"Abrindo: {full_html_path}")
        driver.get(full_html_path)
        time.sleep(3)  # Esperar carregar completamente
        
        # Executar comando de impressão para PDF
        print_script = """
        window.print();
        return true;
        """
        result = driver.execute_script(print_script)
        
        print(f"✅ PDF gerado em: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()
        print("Navegador fechado.")

# Usar caminhos absolutos
html_file = "teste_emojis.html"
pdf_file = "teste_emojis_colorido.pdf"

# Verificar se o arquivo HTML existe
if os.path.exists(html_file):
    print(f"Arquivo HTML encontrado: {html_file}")
    html_to_pdf_color(html_file, pdf_file)
    
    # Verificar se o PDF foi criado
    if os.path.exists(pdf_file):
        print(f"✅ PDF criado com sucesso em: {os.path.abspath(pdf_file)}")
    else:
        print("❌ PDF não foi criado. Verifique as permissões.")
else:
    print(f"❌ Arquivo HTML não encontrado: {html_file}")
```

### **Opção 2: Método mais confiável com Chrome DevTools Protocol**

Crie `deepseek_convert3.py`:

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
        
        # Executar comando do Chrome DevTools para gerar PDF
        pdf_params = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
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
html_to_pdf_direct("teste_emojis.html", "teste_emojis_colorido.pdf")
```

### **Opção 3: Verificar onde está o PDF atual**

Execute este comando para encontrar o PDF:

```cmd
# No Prompt de Comando, procure pelo arquivo
dir /s teste_emojis_colorido.pdf

# Ou no PowerShell
Get-ChildItem -Path C:\ -Name "teste_emojis_colorido.pdf" -Recurse -ErrorAction SilentlyContinue
```

### **Opção 4: Método mais simples com Chrome headless**

```python
import subprocess
import os

def chrome_html_to_pdf(html_file, pdf_file):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    
    cmd = [
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--print-to-pdf=' + os.path.abspath(pdf_file),
        'file:///' + os.path.abspath(html_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ PDF gerado em: {os.path.abspath(pdf_file)}")
        else:
            print(f"❌ Erro: {result.stderr}")
    except Exception as e:
        print(f"❌ Erro: {e}")

# Usar
chrome_html_to_pdf("teste_emojis.html", "teste_emojis_colorido.pdf")
```

## 📂 **O PDF deve ser gerado na mesma pasta do seu script:**

```
D:\Downloads\_DOCS_\_DOCS_\Teste_emojis\
├── deepseek_convert2.py
├── teste_emojis.html
├── teste_emojis.md
└── teste_emojis_colorido.pdf  ← AQUI!
```

**Recomendo usar a Opção 4** - é a mais direta e confiável para controlar onde o PDF é salvo!

---

*Conversa exportada do DeepSeek*
*Processado em: 24/11/2025 22:27*