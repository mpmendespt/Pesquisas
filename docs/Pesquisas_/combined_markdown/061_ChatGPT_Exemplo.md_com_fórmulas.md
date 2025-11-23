# Exemplo.md com fórmulas

## 📊 Informações
- **Número:** #61
- **Origem:** ChatGPT
- **Categoria:** Outros
- **ID:** 6903d31d-8ec8-8329-83e4-a53a4959a45e
- **Criada em:** 2025-10-30 21:05:34
- **Atualizada em:** 2025-11-01 20:40:13
- **Total de mensagens:** 24
- **Resumo:** exemplo.md com exemplos de formulas matematicas lingagens de progamação...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-30 21:05:32)* *[ChatGPT]*

exemplo.md com exemplos de formulas matematicas lingagens de progamação

---

### 🤖 ChatGPT *(2025-10-30 21:05:34)* *[ChatGPT]*

O arquivo `exemplo.md` que você enviou já contém uma boa estrutura Markdown com código, texto formatado e até CSS embutido【4†exemplo.md】.  

Aqui está uma **versão ampliada** dele com **exemplos de fórmulas matemáticas** e **mais linguagens de programação**, mantendo o mesmo estilo:

---

```markdown
---
title: Meu Documento de Teste
author: Manuel
date: \today
lang: pt-BR
css: |
  body {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  h1, h2, h3 {
    color: #2E7D32; /* Verde escuro */
  }
  pre, code {
    background-color: #f6f8fa;
    padding: 10px;
    border-radius: 5px;
  }
---

# Introdução

Olá! Este é um **documento em negrito** e *itálico*. Vamos testar recursos.

## Lista e Código

- Item 1: Pandoc é incrível.
- Item 2: Veja o código abaixo.

I created `.env` file at the root.
Backticks inside backticks? `` `No problem.` ``

```json
{
  "learning": "Markdown",
  "showing": "block code snippet"
}
```

```js
const x = "Block code snippet in JS";
console.log(x);
```

```python
def hello():
    print("Olá, mundo!")
    return True
```

```bash
# Exemplo de comando no terminal
echo "Olá, Linux!"
```

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Olá, C++!" << endl;
    return 0;
}
```

## Fórmulas Matemáticas

Aqui estão alguns exemplos de fórmulas usando **LaTeX no Markdown** (funciona com Pandoc, Typora, Obsidian, etc.):

Inline: A famosa fórmula de Einstein \( E = mc^2 \).

Bloco matemático:

$$
\int_0^{2\pi} \sin(x) \, dx = 0
$$

Equação quadrática:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

Soma e produto:

$$
\sum_{i=1}^n i = \frac{n(n+1)}{2}
$$

$$
\prod_{k=1}^n k = n!
$$

## Tabela

| Linguagem | Extensão | Paradigma |
|------------|-----------|------------|
| Python     | `.py`     | Multiparadigma |
| JavaScript | `.js`     | Funcional / OO |
| C++        | `.cpp`    | Imperativo / OO |

## Links

Veja o [Cheatsheet][markdown-cheatsheet] e a [Documentação][docs].

[markdown-cheatsheet]: https://www.markdownguide.org/cheat-sheet/
[docs]: https://pandoc.org/MANUAL.html

---

```

---

Deseja que eu gere um **PDF** a partir desse Markdown (com as fórmulas renderizadas corretamente)?  
Posso configurar para isso em estilo acadêmico, simples ou moderno.

---

### 👤 Utilizador *(2025-10-30 21:07:12)* *[ChatGPT]*

pretendo um file md completo

---

### 🤖 ChatGPT *(2025-10-30 21:07:13)* *[ChatGPT]*

Perfeito 👍  
Aqui está um **arquivo Markdown completo (`exemplo_completo.md`)**, bem estruturado, com:

- Cabeçalho YAML (título, autor, data, CSS embutido)  
- Texto formatado (negrito, itálico, listas)  
- Blocos de código em várias linguagens (Python, JS, C++, Bash, HTML)  
- Fórmulas matemáticas com LaTeX  
- Tabela e links  
- Imagem de exemplo  

---

```markdown
---
title: Documento Completo de Exemplo
author: Manuel
date: \today
lang: pt-BR
css: |
  body {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
    line-height: 1.6;
  }
  h1, h2, h3 {
    color: #1565C0; /* Azul */
  }
  pre, code {
    background-color: #f6f8fa;
    padding: 10px;
    border-radius: 5px;
  }
---

# 🧭 Introdução

Olá! Este é um **documento Markdown completo** com exemplos de **fórmulas matemáticas**, **códigos em várias linguagens** e **formatos úteis**.  
O Markdown é simples, poderoso e compatível com conversores como **Pandoc**, **Typora** e **Obsidian**.

---

## 🗒️ Texto Formatado

- **Negrito**
- *Itálico*
- ***Negrito e itálico***
- ~~Texto riscado~~

> "Markdown é uma linguagem de marcação leve que permite escrever com clareza e exportar para HTML, PDF e outros formatos."

---

## 🧩 Listas

### Lista Ordenada
1. Primeiro item  
2. Segundo item  
3. Terceiro item

### Lista Não Ordenada
- Item A
- Item B
  - Subitem B1
  - Subitem B2

---

## 💻 Exemplos de Código

### JSON
```json
{
  "nome": "Manuel",
  "aprendendo": "Markdown",
  "linguagens": ["Python", "JavaScript", "C++"]
}
```

### JavaScript
```js
const saudacao = nome => `Olá, ${nome}!`;
console.log(saudacao("Mundo"));
```

### Python
```python
def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)

print(f"5! = {fatorial(5)}")
```

### C++
```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Olá, C++!" << endl;
    return 0;
}
```

### Bash
```bash
#!/bin/bash
echo "Rodando script no terminal..."
```

### HTML
```html
<!DOCTYPE html>
<html>
  <body>
    <h1>Exemplo em HTML</h1>
    <p>Markdown pode conter blocos HTML.</p>
  </body>
</html>
```

---

## 🧮 Fórmulas Matemáticas

Inline: a famosa equação \( E = mc^2 \)

Bloco de equação:

$$
\int_0^{2\pi} \sin(x)\,dx = 0
$$

Equação quadrática:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

Soma e produto:

$$
\sum_{i=1}^n i = \frac{n(n+1)}{2}
$$

$$
\prod_{k=1}^n k = n!
$$

Matriz:

$$
A = 
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
$$

---

## 📊 Tabela de Linguagens

| Linguagem   | Extensão | Paradigma          | Popularidade |
|--------------|-----------|--------------------|---------------|
| Python       | `.py`     | Multiparadigma     | ⭐⭐⭐⭐⭐ |
| JavaScript   | `.js`     | Funcional / OO     | ⭐⭐⭐⭐ |
| C++          | `.cpp`    | Imperativo / OO    | ⭐⭐⭐ |
| Bash         | `.sh`     | Script / Automação | ⭐⭐ |

---

## 🖼️ Imagens

![Imagem de teste](teste.jpg)

Ou imagem da web:  
![Logo Markdown](https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg)

---

## 🔗 Links Úteis

- [Guia Completo de Markdown](https://www.markdownguide.org/basic-syntax/)
- [Documentação do Pandoc](https://pandoc.org/MANUAL.html)
- [Editor Typora](https://typora.io/)
- [Repositório GitHub](https://github.com/)

---

## 🧱 Comentários e Observações

<!-- Este é um comentário que não será exibido na renderização final -->

> “Markdown é onde a simplicidade encontra a elegância.”

---

## ✅ Conclusão

Você agora tem um **modelo completo de arquivo Markdown** — perfeito para testes, relatórios, anotações técnicas ou geração de PDF com Pandoc.

Para converter em PDF:
```bash
pandoc exemplo_completo.md -o exemplo_completo.pdf --pdf-engine=xelatex
```

---

```

---

Deseja que eu gere esse conteúdo como um arquivo `.md` para download (`exemplo_completo.md`)?

---

### 👤 Utilizador *(2025-10-30 21:08:21)* *[ChatGPT]*

sim

---

### 🤖 ChatGPT *(2025-10-30 21:08:42)* *[ChatGPT]*

✅ Aqui está o seu arquivo Markdown completo, pronto para download:

[📄 Baixar exemplo_completo.md](sandbox:/mnt/data/exemplo_completo.md)

---

### 👤 Utilizador *(2025-10-30 21:10:13)* *[ChatGPT]*

para já pretendo converter para html

---

### 🤖 ChatGPT *(2025-10-30 21:10:17)* *[ChatGPT]*

✅ Conversão concluída!  
Aqui está o arquivo HTML gerado a partir do seu Markdown:

[🌐 Baixar exemplo_completo.html](sandbox:/mnt/data/exemplo_completo.html)

---

### 👤 Utilizador *(2025-10-30 21:10:44)* *[ChatGPT]*

pretendo converter para html com pandoc

---

### 🤖 ChatGPT *(2025-10-30 21:10:45)* *[ChatGPT]*

Perfeito — você quer usar o **Pandoc** diretamente no seu computador, certo?  
Aqui está o **comando exato** para converter o arquivo `exemplo_completo.md` em um arquivo HTML formatado, com suporte a CSS e fórmulas matemáticas via MathJax:

---

### 🧩 Comando básico
```bash
pandoc exemplo_completo.md -o exemplo_completo.html
```

---

### 💅 Com estilo (usando o CSS embutido do próprio Markdown)
O seu arquivo `.md` já contém um bloco CSS no cabeçalho YAML, então este comando já respeitará o estilo automaticamente:
```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone
```

---

### 🧮 Com suporte a fórmulas matemáticas (MathJax)
Se quiser renderizar as equações LaTeX corretamente no HTML:
```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
```

---

### 🌐 Versão com título, autor e metadados
```bash
pandoc exemplo_completo.md -o exemplo_completo.html \
  --standalone \
  --metadata title="Documento Completo de Exemplo" \
  --mathjax \
  --toc \
  --css estilo.css
```

> 💡 Se quiser personalizar mais o visual, você pode salvar o CSS do seu cabeçalho YAML num arquivo separado (`estilo.css`) e aplicar com `--css estilo.css`.

---

Deseja que eu gere também um **exemplo de arquivo HTML renderizado** (com MathJax e o CSS embutido) para você visualizar diretamente?

---

### 👤 Utilizador *(2025-10-30 21:13:14)* *[ChatGPT]*

(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Teste_github-pandoc_css>pandoc exemplo_completo.md -o exemplo_completo.html
[WARNING] Could not convert TeX math
  x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
  , rendering as TeX
[WARNING] Could not convert TeX math
  \sum_{i=1}^n i = \frac{n(n+1)}{2}
  , rendering as TeX
[WARNING] Could not convert TeX math
  \prod_{k=1}^n k = n!
  , rendering as TeX
[WARNING] Could not convert TeX math
  A =
  \begin{bmatrix}
  1 & 2 & 3 \\
  4 & 5 & 6
  \end{bmatrix}
  , rendering as TeX

---

### 🤖 ChatGPT *(2025-10-30 21:13:16)* *[ChatGPT]*

Perfeito — o **Pandoc** está te avisando que ele **não conseguiu converter as fórmulas LaTeX para HTML nativamente**, então as deixou apenas como texto TeX.  

👉 Isso acontece porque o comando que você usou **não incluiu um mecanismo para renderizar matemática**, como **MathJax** ou **KaTeX**.

---

### ✅ 💡 Solução: use o parâmetro `--mathjax`
Execute o comando assim:

```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
```

🔹 O `--mathjax` adiciona automaticamente o script do **MathJax** no HTML, permitindo que as equações sejam renderizadas corretamente no navegador.  
🔹 Você não precisa instalar nada extra — o Pandoc usa o MathJax hospedado online por padrão.

---

### 💻 Alternativa: usar o KaTeX (renderização mais rápida)
Se preferir usar **KaTeX**, que é leve e offline:

```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --katex
```

> O KaTeX vem embutido em algumas versões do Pandoc. Caso não apareça formatado, adicione o link manualmente depois no `<head>` do HTML.

---

### 🎨 Dica extra (opcional)
Se quiser gerar um HTML completo com sumário, metadados e CSS bonito:
```bash
pandoc exemplo_completo.md -o exemplo_completo.html \
  --standalone \
  --mathjax \
  --toc \
  --metadata title="Documento Completo de Exemplo"
```

---

Deseja que eu te mostre **como embutir o MathJax manualmente** no HTML gerado (para funcionar até sem internet)?

---

### 👤 Utilizador *(2025-10-30 21:21:43)* *[ChatGPT]*

converter para html com pandoc exemplo_completo.md

---

### 🤖 ChatGPT *(2025-10-30 21:21:50)* *[ChatGPT]*

✅ Conversão realizada com sucesso!  
Aqui está o arquivo HTML gerado a partir do seu `exemplo_completo.md`, com **MathJax** e **sumário automático** incluídos:

[🌐 Baixar exemplo_completo.html](sandbox:/mnt/data/exemplo_completo.html)

---

### 👤 Utilizador *(2025-10-30 21:28:11)* *[ChatGPT]*

pretendo agora apos pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
 fazer uma conversão do html para pdf, usando o metodo do deepseek_convert3.py

---

### 🤖 ChatGPT *(2025-10-30 21:28:15)* *[ChatGPT]*

Perfeito 👌  
O seu script `deepseek_convert3.py` usa o **Selenium + Chrome headless** para converter um arquivo HTML em PDF diretamente, sem precisar do Pandoc.

Ele define a função:
```python
html_to_pdf_direct(html_file, pdf_file)
```
e já faz um exemplo no final com:
```python
html_to_pdf_direct("teste_emojis.html", "teste_emojis_colorido3.pdf")
```

---

### ✅ Como adaptar para o seu arquivo

Você já gerou o `exemplo_completo.html` com o comando Pandoc:
```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
```

Agora, basta modificar o final do seu script para converter **esse HTML para PDF**:

```python
# Substituir a linha final do script por:
html_to_pdf_direct("exemplo_completo.html", "exemplo_completo.pdf")
```

---

### 💡 Passos completos:

1. Certifique-se de ter o **Google Chrome** e o **ChromeDriver** instalados (versões compatíveis).  
   - Teste no terminal:
     ```bash
     chromedriver --version
     ```

2. No mesmo diretório onde estão:
   - `deepseek_convert3.py`
   - `exemplo_completo.html`

   execute:
   ```bash
   python deepseek_convert3.py
   ```

3. Se tudo correr bem, será criado um arquivo:
   ```
   exemplo_completo.pdf
   ```
   com todo o conteúdo renderizado (incluindo MathJax e CSS).

---

Quer que eu edite automaticamente o seu `deepseek_convert3.py` para apontar para `exemplo_completo.html` → `exemplo_completo.pdf` e te devolver a versão pronta?

---

### 👤 Utilizador *(2025-10-30 21:30:09)* *[ChatGPT]*

o que eu pretendo é usar pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax para converter para html e depois html_to_pdf_direct(html_file, pdf_file)

---

### 🤖 ChatGPT *(2025-10-30 21:30:09)* *[ChatGPT]*

Perfeito ✅ — o que você quer é um **fluxo em duas etapas automáticas**:  

1. **Usar o Pandoc** para converter o Markdown → HTML  
2. **Usar a função `html_to_pdf_direct()`** (do seu `deepseek_convert3.py`) para converter o HTML → PDF  

Vamos montar isso passo a passo 👇  

---

## 🧩 1️⃣ Converter Markdown para HTML com Pandoc
Comando no terminal:
```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
```

Isso gera o arquivo `exemplo_completo.html` (com o MathJax para fórmulas renderizadas corretamente no navegador).

---

## 🧩 2️⃣ Converter HTML para PDF com o método do `deepseek_convert3.py`
Agora que o HTML foi gerado, você pode criar (ou editar) um script Python para automatizar a conversão:

### 🔧 Novo script: `convert_pipeline.py`
```python
import os
from deepseek_convert3 import html_to_pdf_direct

# Caminhos dos arquivos
html_file = "exemplo_completo.html"
pdf_file = "exemplo_completo.pdf"

# Verificar se o HTML existe
if not os.path.exists(html_file):
    print("❌ Arquivo HTML não encontrado. Execute primeiro o comando Pandoc:")
    print("pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax")
else:
    print("✅ Convertendo HTML para PDF...")
    html_to_pdf_direct(html_file, pdf_file)
```

---

## 🧮 3️⃣ Fluxo completo

Você só precisa rodar **duas linhas no terminal**:

```bash
pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax
python convert_pipeline.py
```

---

### 💡 Dica adicional
Se quiser automatizar tudo (Markdown → HTML → PDF) em **um único script Python**, aqui vai a versão completa:

```python
import os
import subprocess
from deepseek_convert3 import html_to_pdf_direct

md_file = "exemplo_completo.md"
html_file = "exemplo_completo.html"
pdf_file = "exemplo_completo.pdf"

# 1. Converter Markdown → HTML com Pandoc
print("🪄 Convertendo Markdown para HTML com Pandoc...")
subprocess.run([
    "pandoc", md_file,
    "-o", html_file,
    "--standalone",
    "--mathjax"
], check=True)

# 2. Converter HTML → PDF com Chrome Headless
print("🧭 Convertendo HTML para PDF com Selenium + Chrome...")
html_to_pdf_direct(html_file, pdf_file)

print(f"✅ Conversão completa: {pdf_file}")
```

---

Quer que eu gere e te envie esse script Python pronto (`convert_pipeline.py`) para download?

---

### 👤 Utilizador *(2025-10-30 21:37:12)* *[ChatGPT]*

sim com o nome convert_pipeline3.py

---

### 👤 Utilizador *(2025-10-31 11:12:35)* *[ChatGPT]*

sim com o nome convert_pipeline3.py

---

### 🤖 ChatGPT *(2025-10-30 21:37:16)* *[ChatGPT]*

Parece que não consigo executar análises de dados avançadas neste momento, portanto não consegui gerar o arquivo automaticamente.  

Mas você pode criar o script **facilmente** copiando o conteúdo abaixo e salvando como `convert_pipeline3.py` no mesmo diretório onde estão os arquivos `exemplo_completo.md` e `deepseek_convert3.py`:

```python
import os
import subprocess
from deepseek_convert3 import html_to_pdf_direct

md_file = "exemplo_completo.md"
html_file = "exemplo_completo.html"
pdf_file = "exemplo_completo.pdf"

# 1. Converter Markdown → HTML com Pandoc
print("🪄 Convertendo Markdown para HTML com Pandoc...")
subprocess.run([
    "pandoc", md_file,
    "-o", html_file,
    "--standalone",
    "--mathjax"
], check=True)

# 2. Converter HTML → PDF com Chrome Headless
print("🧭 Convertendo HTML para PDF com Selenium + Chrome...")
html_to_pdf_direct(html_file, pdf_file)

print(f"✅ Conversão completa: {pdf_file}")
```

---

Depois de salvar, execute o pipeline completo com:
```bash
python convert_pipeline3.py
```

💡 Isso fará automaticamente:
1. `pandoc exemplo_completo.md -o exemplo_completo.html --standalone --mathjax`
2. E depois chamará `html_to_pdf_direct()` para gerar `exemplo_completo.pdf`.

---

### 🤖 ChatGPT *(2025-10-31 11:12:37)* *[ChatGPT]*

It seems like I can’t do more advanced data analysis right now. Please try again later.  

Mas posso te mostrar o conteúdo completo do arquivo aqui — basta copiar e salvar localmente como **`convert_pipeline3.py`** no mesmo diretório onde estão os outros arquivos (`exemplo_completo.md` e `deepseek_convert3.py`):

```python
import os
import subprocess
from deepseek_convert3 import html_to_pdf_direct

md_file = "exemplo_completo.md"
html_file = "exemplo_completo.html"
pdf_file = "exemplo_completo.pdf"

# 1. Converter Markdown → HTML com Pandoc
print("🪄 Convertendo Markdown para HTML com Pandoc...")
subprocess.run([
    "pandoc", md_file,
    "-o", html_file,
    "--standalone",
    "--mathjax"
], check=True)

# 2. Converter HTML → PDF com Chrome Headless
print("🧭 Convertendo HTML para PDF com Selenium + Chrome...")
html_to_pdf_direct(html_file, pdf_file)

print(f"✅ Conversão completa: {pdf_file}")
```

---

### 💡 Como usar:

1. Coloque esse arquivo (`convert_pipeline3.py`) na mesma pasta dos outros arquivos.  
2. No terminal, execute:
   ```bash
   python convert_pipeline3.py
   ```
3. Ele vai:
   - Usar o **Pandoc** para gerar o `exemplo_completo.html`
   - Depois chamar o **Chrome headless (via Selenium)** para criar `exemplo_completo.pdf`  

Quer que eu te adicione também suporte opcional a modo paisagem (`landscape=True`) ou margens personalizadas no PDF?

---

### 🤖 ChatGPT *(2025-10-31 11:13:31)* *[ChatGPT]*

Parece que não consigo fazer análises de dados avançadas agora, então não consegui criar o arquivo `convert_pipeline3.py` automaticamente neste momento.  

Mas você pode criar o arquivo facilmente no seu computador — basta abrir um editor de texto (como VS Code, Notepad++ ou até o Bloco de Notas) e colar o seguinte conteúdo dentro de um novo arquivo chamado **`convert_pipeline3.py`**:

```python
import os
import subprocess
from deepseek_convert3 import html_to_pdf_direct

md_file = "exemplo_completo.md"
html_file = "exemplo_completo.html"
pdf_file = "exemplo_completo.pdf"

# 1. Converter Markdown → HTML com Pandoc
print("🪄 Convertendo Markdown para HTML com Pandoc...")
subprocess.run([
    "pandoc", md_file,
    "-o", html_file,
    "--standalone",
    "--mathjax"
], check=True)

# 2. Converter HTML → PDF com Chrome Headless
print("🧭 Convertendo HTML para PDF com Selenium + Chrome...")
html_to_pdf_direct(html_file, pdf_file)

print(f"✅ Conversão completa: {pdf_file}")
```

Depois salve esse arquivo **no mesmo diretório** onde estão:
- `exemplo_completo.md`
- `deepseek_convert3.py`

E execute o comando no terminal:
```bash
python convert_pipeline3.py
```

👉 Isso fará automaticamente:
1. A conversão do `.md` → `.html` via **Pandoc**
2. A conversão do `.html` → `.pdf` via **Selenium + Chrome**

---

### 🤖 ChatGPT *(2025-10-31 11:14:03)* *[ChatGPT]*

Parece que não consigo executar a ferramenta de criação de arquivos Python neste momento. 😕  

Mas você pode facilmente criar o arquivo **`convert_pipeline3.py`** manualmente.  
Basta copiar o código abaixo e colá-lo num editor de texto (como VS Code, Notepad++, ou mesmo o Bloco de Notas) e salvar com esse nome no mesmo diretório onde estão `exemplo_completo.md` e `deepseek_convert3.py`:

---

```python
import os
import subprocess
from deepseek_convert3 import html_to_pdf_direct

md_file = "exemplo_completo.md"
html_file = "exemplo_completo.html"
pdf_file = "exemplo_completo.pdf"

# 1️⃣ Converter Markdown → HTML com Pandoc
print("🪄 Convertendo Markdown para HTML com Pandoc...")
subprocess.run([
    "pandoc", md_file,
    "-o", html_file,
    "--standalone",
    "--mathjax"
], check=True)

# 2️⃣ Converter HTML → PDF com Chrome Headless (Selenium)
print("🧭 Convertendo HTML para PDF com Selenium + Chrome...")
html_to_pdf_direct(html_file, pdf_file)

print(f"✅ Conversão completa: {pdf_file}")
```

---

### 💡 Como usar:
1. Coloque este arquivo no mesmo diretório dos outros dois (`exemplo_completo.md` e `deepseek_convert3.py`);
2. Abra o terminal e execute:
   ```bash
   python convert_pipeline3.py
   ```
3. Ele vai:
   - gerar `exemplo_completo.html` com Pandoc,  
   - e depois converter automaticamente para `exemplo_completo.pdf` via Selenium + Chrome.

Quer que eu te mostre como configurar o **ChromeDriver** corretamente para esse script funcionar sem erros?

---

*Conversa exportada do ChatGPT*
*Processado em: 23/11/2025 23:05*