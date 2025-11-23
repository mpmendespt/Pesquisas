# Usar Noto Emoji Pandoc

## 📊 Informações
- **Número:** #178
- **Origem:** ChatGPT
- **Categoria:** Programação
- **ID:** 68cb2065-e8e8-832b-acfc-6989aa36667a
- **Criada em:** 2025-09-17 21:56:13
- **Atualizada em:** 2025-09-17 22:20:16
- **Total de mensagens:** 20
- **Resumo:** Noto Color Emoji como usar esta fonte no pandoc windows...

---

## 💬 Conversa

### 👤 Utilizador *(2025-09-17 21:56:13)* *[ChatGPT]*

Noto Color Emoji como usar esta fonte no pandoc windows

---

### 🤖 ChatGPT *(2025-09-17 21:56:13)* *[ChatGPT]*

No **Windows**, usar a fonte **Noto Color Emoji** com o **Pandoc** pode ser um pouco complicado porque:

1. O Windows não renderiza **emoji coloridos** via fontes OpenType-SVG/OT-COLR v1 no PDF de forma nativa.  
2. O **Pandoc**, quando gera **PDF**, normalmente usa o LaTeX (via `xelatex` ou `lualatex`) ou então o **wkhtmltopdf**/WeasyPrint (HTML → PDF).  
3. O suporte a emoji colorido depende do mecanismo de saída que você escolher.

Aqui vai um guia prático:

---

### 1. Instalar a fonte
- Baixe a fonte [Noto Color Emoji](https://github.com/googlefonts/noto-emoji).  
- Clique com o botão direito no arquivo `.ttf` ou `.otf` → **Instalar**.

---

### 2. Usar com Pandoc → PDF via XeLaTeX
Você precisa do **xelatex** ou **lualatex** (vem com TeX Live ou MikTeX).

Exemplo de comando Pandoc:

```powershell
pandoc input.md -o output.pdf --pdf-engine=xelatex ^
  -V mainfont="Times New Roman" ^
  -V monofont="Consolas" ^
  -V CJKmainfont="Noto Color Emoji"
```

No LaTeX template, você pode forçar o uso da fonte para emoji:

```latex
\newfontfamily\emoji{Noto Color Emoji}
```

E no Markdown usar algo como:

```markdown
Aqui vai um emoji: {\emoji 😀}
```

⚠️ Problema: O **Noto Color Emoji** não renderiza em **cores** no LaTeX/XeLaTeX — só em escala de cinza (ou blocos). Isso é limitação do motor de PDF.

---

### 3. Usar com Pandoc → PDF via HTML (wkhtmltopdf ou weasyprint)
Esse caminho preserva o **color emoji**.

Exemplo:

```powershell
pandoc input.md -o output.pdf --pdf-engine=weasyprint
```

E no CSS adicione:

```css
body {
  font-family: "Noto Color Emoji", "Segoe UI Emoji", sans-serif;
}
```

Crie um arquivo `custom.css` e passe no Pandoc:

```powershell
pandoc input.md -o output.pdf --css=custom.css --pdf-engine=weasyprint
```

👉 Esse é o método que realmente mantém **emoji coloridos** no PDF.

---

### 4. Alternativa rápida
Se quiser apenas gerar **HTML com emoji colorido** e depois imprimir em PDF (via navegador):

```powershell
pandoc input.md -o output.html --css=custom.css
```

Depois abra no **Chrome/Edge** → **Imprimir → Salvar como PDF**.

---

📌 Resumindo:  
- `xelatex` / `lualatex` = suporta a fonte, mas **não renderiza cor**.  
- `weasyprint` ou `wkhtmltopdf` (HTML → PDF) = mantém os **emoji coloridos**.  
- Para melhor resultado, use `--pdf-engine=weasyprint` + CSS com `"Noto Color Emoji"`.

---

Quer que eu prepare um **exemplo mínimo completo** (um `.md` + `.css`) que você só roda no Windows com Pandoc para sair com emoji colorido no PDF?

---

### 👤 Utilizador *(2025-09-17 21:57:50)* *[ChatGPT]*

error:  (file C:/Program Files/MiKTeX/fonts/truetype/public/noto-emoji/notocol
oremoji.ttf) (ttf): loca table not found

---

### 🤖 ChatGPT *(2025-09-17 21:57:50)* *[ChatGPT]*

Ótimo, você me mostrou o erro real do **MiKTeX/XeLaTeX**:

```
(file C:/Program Files/MiKTeX/fonts/truetype/public/noto-emoji/notocoloremoji.ttf) (ttf): loca table not found
```

---

### 🔎 O que significa
O **XeLaTeX/LuaLaTeX** não consegue usar a **Noto Color Emoji** porque:
- Essa fonte é um **COLR/CPAL ou OpenType-SVG font** (multi-camada/colorida).  
- O motor de PDF do TeX não entende esse tipo de fonte → por isso aparece `loca table not found`.  
- Isso **não é bug do MiKTeX**, é limitação do LaTeX + FreeType.

---

### ✅ Como resolver / alternativas

#### 1. Usar um motor baseado em **HTML** (WeasyPrint ou wkhtmltopdf)
Esse é o jeito mais fácil de **ter emoji colorido**:

```powershell
pandoc input.md -o output.pdf --pdf-engine=weasyprint --css=custom.css
```

`custom.css`:
```css
body {
  font-family: "Noto Color Emoji", "Segoe UI Emoji", sans-serif;
}
```

> WeasyPrint usa Cairo/FreeType e consegue lidar com a `Noto Color Emoji`.

---

#### 2. Usar **Segoe UI Emoji** (nativa do Windows)
Se você insiste no caminho `xelatex`/`lualatex`, pode usar a fonte **Segoe UI Emoji**, que o Windows já suporta (embora também não seja colorida no PDF, mas pelo menos não dá erro):

```powershell
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Segoe UI Emoji"
```

---

#### 3. Gerar PDF via navegador (garantia de cor)
1. `pandoc input.md -o output.html --css=custom.css`
2. Abra no **Edge/Chrome**
3. `Ctrl+P → Salvar como PDF`

---

#### 4. Conversão mista
Se você precisa usar LaTeX mas quer emoji, pode:
- Usar pacotes como [`emoji`](https://ctan.org/pkg/emoji) do LaTeX, que convertem emoji em **imagens PNG** inseridas no PDF.
- Ou usar scripts que substituem `😀` por `\includegraphics{emoji_u1f600.png}` (complicado, mas funciona).

---

📌 **Conclusão:**
- **Noto Color Emoji** não funciona no MiKTeX/XeLaTeX → erro inevitável.  
- Para emoji colorido em PDF no Windows → use `weasyprint` ou exporte via navegador.  
- Se aceitar emoji preto e branco → use `Segoe UI Emoji` no XeLaTeX.  

---

Quer que eu monte um **exemplo funcional** de `input.md` + `custom.css` + comando `pandoc` que gera um PDF com **emoji colorido** via `weasyprint` no Windows?

---

### 👤 Utilizador *(2025-09-17 21:58:39)* *[ChatGPT]*

posso usar:  pandoc guia-congelamento.md -o out35.pdf  --pdf-engine=lualatex -V mainfont="Noto Color Emoji"

---

### 🤖 ChatGPT *(2025-09-17 21:58:39)* *[ChatGPT]*

Você até **pode rodar** esse comando:

```powershell
pandoc guia-congelamento.md -o out35.pdf --pdf-engine=lualatex -V mainfont="Noto Color Emoji"
```

mas dois pontos importantes:

---

### 🔴 O que vai acontecer
- O **LuaLaTeX** (assim como o XeLaTeX) **não entende a fonte Noto Color Emoji**, porque ela é **COLR/CPAL ou OpenType-SVG**.  
- Resultado:
  - Muitas vezes dá o mesmo erro (`loca table not found`)  
  - Ou o PDF sai com **caixinhas quadradas**/símbolos em vez de emoji.  
  - Mesmo que “funcione”, os emoji vão sair **preto e branco**, nunca coloridos.  

---

### ✅ Alternativas
Se você precisa **emoji colorido no PDF**:

1. **HTML → PDF via WeasyPrint (recomendado)**
   ```powershell
   pandoc guia-congelamento.md -o out35.pdf --pdf-engine=weasyprint --css=custom.css
   ```
   `custom.css`:
   ```css
   body {
     font-family: "Noto Color Emoji", "Segoe UI Emoji", sans-serif;
   }
   ```

   → Esse fluxo mantém os emoji em **cores**.

2. **Usar Segoe UI Emoji no LuaLaTeX**
   ```powershell
   pandoc guia-congelamento.md -o out35.pdf --pdf-engine=lualatex -V mainfont="Segoe UI Emoji"
   ```
   → Funciona, mas só em **preto e branco**.

3. **Via navegador**
   ```powershell
   pandoc guia-congelamento.md -o out35.html --css=custom.css
   ```
   Depois abrir no **Chrome/Edge** → Imprimir → Salvar como PDF.  
   → Mantém os emoji coloridos.

---

👉 Ou seja: **o comando que você sugeriu vai rodar, mas nunca te dará emoji colorido no PDF**.  
Se a sua prioridade é **emoji colorido**, você precisa trocar o motor (`weasyprint` ou navegador).  

---

Quer que eu te mostre um exemplo **mínimo pronto para copiar e colar** (`.md` + `.css`) que já sai com emoji colorido no PDF usando `weasyprint` no Windows?

---

### 👤 Utilizador *(2025-09-17 21:59:43)* *[ChatGPT]*

então como usar: mainfont="Noto Color Emoji"

---

### 🤖 ChatGPT *(2025-09-17 21:59:43)* *[ChatGPT]*

Boa pergunta 👍  

No **Pandoc + LaTeX (XeLaTeX / LuaLaTeX)**, a opção  

```bash
-V mainfont="Noto Color Emoji"
```  

significa: *“defina a fonte principal do documento para Noto Color Emoji”*.  

---

### 🔎 Mas o problema
- O motor do LaTeX (XeLaTeX/LuaLaTeX) **não consegue usar fontes coloridas** como `Noto Color Emoji` (formato COLR/CPAL ou SVG-in-OT).  
- Por isso, você recebe erro (`loca table not found`) ou, quando não dá erro, os emoji aparecem **em preto e branco** ou como **caixas**.  

Ou seja: **não dá para usar `mainfont="Noto Color Emoji"` com LaTeX para ter emoji colorido.**  

---

### ✅ O que dá para fazer

#### 1. Se você só quer testar a sintaxe
Esse comando é válido (mas não terá cor):

```powershell
pandoc guia.md -o out.pdf --pdf-engine=lualatex -V mainfont="Segoe UI Emoji"
```

(`Segoe UI Emoji` é mais estável no Windows; mas também só mostra emoji em preto e branco no PDF).

---

#### 2. Se realmente precisa de **emoji colorido**
Use um motor baseado em **HTML/CSS**, não LaTeX:

```powershell
pandoc guia.md -o out.pdf --pdf-engine=weasyprint --css=emoji.css
```

Arquivo `emoji.css`:

```css
body {
  font-family: "Noto Color Emoji", "Segoe UI Emoji", sans-serif;
}
```

Esse sim vai usar `Noto Color Emoji` de verdade, mantendo cor.  

---

#### 3. Alternativa via navegador
```powershell
pandoc guia.md -o out.html --css=emoji.css
```
Depois abra no **Chrome/Edge** → Imprimir → PDF.  
Funciona igual, e preserva cor.

---

📌 **Resumo**:  
- `mainfont="Noto Color Emoji"` funciona *só como instrução de fonte* em LaTeX, mas o motor **não sabe renderizar fontes coloridas** → sem cor ou erro.  
- Para **emoji colorido**, você precisa mudar para `weasyprint` (ou navegador).  

---

Quer que eu te monte um exemplo **mínimo completo** (um `.md` com emoji + `.css`) para você rodar no Windows com Pandoc e sair direto com emoji colorido no PDF?

---

### 👤 Utilizador *(2025-09-17 22:00:34)* *[ChatGPT]*

e não é possivel usar outra pdf-engine

---

### 🤖 ChatGPT *(2025-09-17 22:00:34)* *[ChatGPT]*

Boa! 👍  
Depende do que você entende por *“outra pdf-engine”*.  

O **Pandoc** aceita alguns motores de PDF diferentes, mas cada grupo tem limitações:

---

### 1. **Engines LaTeX** (xelatex, lualatex, pdflatex)
- **pdflatex** → não suporta Unicode/emoji de jeito nenhum.  
- **xelatex / lualatex** → até aceitam Unicode + troca de fonte (`mainfont`), mas **não renderizam emoji colorido**.  
  - Se você indicar `mainfont="Noto Color Emoji"`, ou dá erro (`loca table not found`) ou sai em **preto e branco**.  
👉 Não existe motor LaTeX que renderize emoji colorido no PDF.

---

### 2. **Engines baseados em HTML/CSS** (WeasyPrint, wkhtmltopdf, prince)
Esses usam navegador ou motor de renderização web:  
- **weasyprint** (Python, fácil de instalar via `pip install weasyprint`)  
- **wkhtmltopdf** (baseado no WebKit, às vezes com falhas em fontes coloridas)  
- **PrinceXML** (pago, mas excelente suporte a fontes).  

Com eles você consegue usar:

```powershell
pandoc guia.md -o guia.pdf --pdf-engine=weasyprint --css=emoji.css
```

👉 Aqui o `emoji.css` pode forçar `font-family: "Noto Color Emoji"` e os emoji saem **coloridos de verdade**.

---

### 3. **Truques híbridos**
- Gerar **HTML** com Pandoc (`-o guia.html`) → abrir no **Chrome/Edge** → "Imprimir em PDF".  
  - Também preserva cor.  
- Usar pacotes LaTeX como [`emoji`](https://ctan.org/pkg/emoji) que convertem emoji em **imagens PNG** inseridas no PDF (funciona, mas dá trabalho).

---

✅ **Conclusão:**  
Não existe “pdf-engine milagrosa” dentro do mundo LaTeX que faça o `Noto Color Emoji` funcionar em cor.  
Se você quer PDF com emoji colorido, precisa usar **engine baseada em HTML/CSS** (`weasyprint`, `wkhtmltopdf`, ou navegador).  

---

Quer que eu te mostre como instalar o **WeasyPrint no Windows** e configurar o Pandoc para usá-lo direto?

---

### 👤 Utilizador *(2025-09-17 22:07:11)* *[ChatGPT]*

qual é a melhor font para usar emojis coloridos e qual pdf-engine usar

---

### 🤖 ChatGPT *(2025-09-17 22:07:10)* *[ChatGPT]*

Excelente pergunta 👌  

### 🎨 Melhor fonte para emojis coloridos
No Windows e no ecossistema Pandoc, as fontes mais estáveis são:

- **Segoe UI Emoji** → já vem com o Windows.  
  - Mostra emoji colorido em navegadores e apps modernos.  
  - Em LaTeX (`xelatex`/`lualatex`) fica **preto e branco**, mas pelo menos não quebra.  

- **Noto Color Emoji** (do Google) → padrão Android/Linux.  
  - Muito completa, mas **não funciona em LaTeX engines** (erro ou quadrados).  
  - Funciona bem em engines baseadas em HTML/CSS.

👉 Para **PDF com emoji colorido**, tanto `Segoe UI Emoji` quanto `Noto Color Emoji` funcionam — desde que você use um motor baseado em **HTML/CSS**.

---

### ⚙️ Melhor PDF engine
- **LaTeX engines (xelatex, lualatex, pdflatex)**  
  - Confiáveis para textos científicos e fórmulas.  
  - ❌ Nenhuma delas renderiza emoji colorido.  

- **HTML-based engines** (✅ recomendadas para emoji colorido):  
  1. **WeasyPrint** (recomendado — software livre, fácil de instalar com `pip install weasyprint`)  
     ```powershell
     pandoc guia.md -o guia.pdf --pdf-engine=weasyprint --css=emoji.css
     ```
  2. **wkhtmltopdf** (baseado no WebKit, mas às vezes falha em CSS moderno).  
  3. **PrinceXML** (pago, mas altíssima qualidade tipográfica).  
  4. **Chrome/Edge “imprimir em PDF”** (alternativa manual, mas funciona muito bem).

---

### 📌 Resumindo
- **Fonte recomendada**:  
  - `Segoe UI Emoji` (Windows nativa)  
  - ou `Noto Color Emoji` (se você instalou e preferir o estilo Android).  

- **PDF-engine recomendada**:  
  - **WeasyPrint** (para emoji colorido).  
  - Use `xelatex`/`lualatex` **apenas se não precisar de cor nos emoji**.  

---

Quer que eu prepare um exemplo **mínimo** (`.md` + `.css`) que você pode rodar no Windows com `pandoc + weasyprint` e já sai um PDF com emoji colorido?

---

### 👤 Utilizador *(2025-09-17 22:09:28)* *[ChatGPT]*

Exemplos HTML-based engines

---

### 🤖 ChatGPT *(2025-09-17 22:09:28)* *[ChatGPT]*

Perfeito 👌 Vamos organizar exemplos práticos usando **Pandoc com engines baseadas em HTML/CSS** — que são as únicas que preservam **emoji colorido** no PDF.  

---

## 🟢 1. WeasyPrint (recomendado, open source)
### Instalação
```powershell
pip install weasyprint
```

### Uso com Pandoc
Arquivo `guia.md`:
```markdown
# Guia com Emoji

Este é um teste 😀 🍕 🚀
```

Arquivo `emoji.css`:
```css
body {
  font-family: "Noto Color Emoji", "Segoe UI Emoji", sans-serif;
  font-size: 14pt;
}
```

Comando:
```powershell
pandoc guia.md -o guia.pdf --pdf-engine=weasyprint --css=emoji.css
```

✅ Emojis saem **coloridos** no PDF.

---

## 🟢 2. wkhtmltopdf (baseado em WebKit)
### Instalação
Baixar de: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)  
(Precisa adicionar ao PATH).

### Uso com Pandoc
```powershell
pandoc guia.md -o guia.pdf --pdf-engine=wkhtmltopdf --css=emoji.css
```

⚠️ Limitações:
- Suporte parcial a CSS moderno.
- Emojis funcionam, mas alguns estilos podem quebrar.

---

## 🟢 3. PrinceXML (pago, mas profissional)
### Instalação
[https://www.princexml.com/download/](https://www.princexml.com/download/)  
(licença comercial, mas tem versão gratuita de teste com marca d’água).

### Uso com Pandoc
```powershell
pandoc guia.md -o guia.pdf --pdf-engine=prince --css=emoji.css
```

✅ Qualidade tipográfica de nível editorial.  
💰 Mas exige licença para uso sério.

---

## 🟢 4. Chrome / Edge (atalho manual)
Gerar HTML:
```powershell
pandoc guia.md -o guia.html --css=emoji.css
```

Abrir `guia.html` no navegador → **Ctrl+P → Salvar como PDF**.  

✅ Suporte completo a emoji colorido.  
❌ Processo manual (a não ser que use Puppeteer/Playwright para automatizar).

---

### 📌 Resumo
- Melhor engine livre → **WeasyPrint**.  
- Simples de instalar, funciona no Windows, suporta emoji colorido com `Noto Color Emoji` ou `Segoe UI Emoji`.  
- Para profissional/editorial → **PrinceXML**.  
- Atalho rápido → **Chrome/Edge salvar como PDF**.  

---

Quer que eu prepare um **pacotinho de exemplo pronto** (um `.md` e um `.css`) que você só roda com Pandoc + WeasyPrint no Windows e já sai um PDF com emojis coloridos?

---

### 👤 Utilizador *(2025-09-17 22:11:46)* *[ChatGPT]*

sim (pacotinho de exemplo pronto (um .md e um .css))  WeasyPrint

---

### 🤖 ChatGPT *(2025-09-17 22:11:47)* *[ChatGPT]*

Perfeito 🚀 Vou te montar um **exemplo mínimo** para rodar no **Windows** com **Pandoc + WeasyPrint** e sair direto com PDF cheio de emoji colorido.  

---

## 📄 1. Arquivo Markdown (`guia.md`)
Salve como `guia.md`:

```markdown
# Guia com Emoji 😎

Este é um teste de PDF com **emoji colorido**.

- Comida: 🍕 🍔 🍩
- Transportes: 🚗 🚲 🚀
- Natureza: 🌳 🌻 🌞

Misturando texto e emoji:  
Eu adoro programar com Pandoc 🤓🔥
```

---

## 🎨 2. Arquivo CSS (`emoji.css`)
Salve como `emoji.css`:

```css
body {
  font-family: "Noto Color Emoji", "Segoe UI Emoji", sans-serif;
  font-size: 14pt;
  line-height: 1.6;
  margin: 2cm;
}

h1 {
  color: #2c3e50;
  font-size: 24pt;
  text-align: center;
  margin-bottom: 20px;
}

ul {
  list-style-type: "👉 ";
}
```

Esse CSS força o uso da **Noto Color Emoji** (se instalada) ou **Segoe UI Emoji** (já vem no Windows).

---

## ⚙️ 3. Comando Pandoc + WeasyPrint
Depois de instalar o WeasyPrint (`pip install weasyprint`), rode no PowerShell:

```powershell
pandoc guia.md -o guia.pdf --pdf-engine=weasyprint --css=emoji.css
```

---

## ✅ Resultado
- O `guia.pdf` vai ter **emoji colorido**, renderizado com a fonte definida.  
- Funciona no Windows, Linux e macOS.  

---

👉 Quer que eu te ensine também a deixar esse comando ainda mais fácil (por exemplo, criando um script `.bat` no Windows para converter Markdown → PDF com um clique)?

---

### 👤 Utilizador *(2025-09-17 22:18:50)* *[ChatGPT]*

weasyprint dá erros

---

### 🤖 ChatGPT *(2025-09-17 22:18:49)* *[ChatGPT]*

Entendi 👍 — no Windows o **WeasyPrint** às vezes dá dor de cabeça porque depende de bibliotecas nativas do **Cairo, Pango e GDK-PixBuf**.  
Se você rodou `pip install weasyprint` e ao gerar PDF aparecem erros, geralmente é por **dependências faltando**.

---

## 🔎 Erros mais comuns do WeasyPrint no Windows
1. `ImportError: cannot import name 'cairo'`  
   → Cairo não instalado.

2. `OSError: no library called "cairo"` ou `"pango"`  
   → faltam DLLs de renderização.

3. PDF sai em branco ou não abre  
   → versão quebrada de uma dependência.

---

## ✅ Como corrigir (Windows)

### 1. Usar o pacote pronto (recomendado)
A equipe do WeasyPrint mantém builds portáteis no **Gohlke wheels** (não precisa compilar nada).  
- Acesse: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#weasyprint](https://www.lfd.uci.edu/~gohlke/pythonlibs/#weasyprint)  
- Baixe o `.whl` compatível com sua versão do Python (ex: `weasyprint-60.2-cp310-cp310-win_amd64.whl` para Python 3.10 64-bit).  
- Instale:  
  ```powershell
  pip install caminho\do\arquivo.whl
  ```

Isso já inclui as dependências.

---

### 2. Alternativa: instalar dependências manualmente
Se você quiser continuar com `pip install weasyprint`:
1. Instale bibliotecas gráficas via Chocolatey:
   ```powershell
   choco install gtk3
   ```
   ou use [MSYS2](https://www.msys2.org/) e rode:
   ```bash
   pacman -S mingw-w64-x86_64-gtk3
   ```
2. Garanta que `cairo.dll`, `pango.dll` e `gdk-pixbuf-2.0.dll` estejam no PATH do Windows.

---

### 3. Usar **Chrome/Edge** como PDF-engine (mais simples)
Se o objetivo principal é **emoji colorido** e o WeasyPrint está difícil de configurar, dá para usar o navegador:

```powershell
pandoc guia.md -o guia.html --css=emoji.css
```

Depois abra `guia.html` → **Ctrl+P → Salvar como PDF**.  
👉 Sai com emoji colorido sem depender do Cairo/Pango.

(Se quiser automatizar, dá pra usar **Puppeteer** ou **Playwright**).

---

📌 **Resumo**:
- O WeasyPrint funciona, mas no Windows é chato instalar.  
- Alternativa fácil e estável: gerar **HTML** e converter para PDF com o navegador.  
- Se quiser insistir no WeasyPrint → recomendo instalar via **wheel do Gohlke**, que já vem pronto.  

---

Quer que eu monte um **passo a passo só com Chrome/Edge** (sem WeasyPrint), mas automatizado, para que o Pandoc já saia direto em PDF com emoji colorido?

---

### 👤 Utilizador *(2025-09-17 22:20:07)* *[ChatGPT]*

easyPrint could not import some external libraries

---

### 🤖 ChatGPT *(2025-09-17 22:20:07)* *[ChatGPT]*

Perfeito — essa mensagem **“WeasyPrint could not import some external libraries”** é clássica no **Windows** 🪟.  
Ela aparece porque o WeasyPrint depende de **Cairo, Pango e GDK-PixBuf**, mas no Windows essas libs não vêm junto.

---

## 🔎 Causas comuns
- Instalou com `pip install weasyprint` mas **faltam DLLs**.  
- PATH do Windows não contém as libs gráficas.  
- Usando Python “puro” sem GTK/Pango.

---

## ✅ Soluções possíveis

### 1. Instalar versão pronta (recomendado no Windows)
Baixe o `.whl` compilado que já inclui tudo:  
👉 [Gohlke wheels – weasyprint](https://www.lfd.uci.edu/~gohlke/pythonlibs/#weasyprint)

Exemplo (para Python 3.10, 64-bit):
```powershell
pip install weasyprint-60.2-cp310-cp310-win_amd64.whl
```

Isso instala junto **cairo + pango**, sem dor de cabeça.

---

### 2. Instalar dependências via MSYS2 (opção avançada)
Se quiser usar o pacote oficial do PyPI:
1. Instale [MSYS2](https://www.msys2.org/).  
2. No terminal MSYS2:
   ```bash
   pacman -S mingw-w64-x86_64-cairo mingw-w64-x86_64-pango mingw-w64-x86_64-gdk-pixbuf2
   ```
3. Adicione os diretórios de binários (`C:\msys64\mingw64\bin`) ao PATH do Windows.

---

### 3. Evitar WeasyPrint no Windows
Se o problema é **só usar emoji colorido**, há caminhos bem mais fáceis:
- **Chrome/Edge**:  
  ```powershell
  pandoc guia.md -o guia.html --css=emoji.css
  ```
  Depois abra no navegador → **Ctrl+P → Salvar PDF** (emoji colorido garantido).
- **wkhtmltopdf**: funciona no Windows sem dependências complicadas, embora o suporte a CSS moderno seja menor:
  ```powershell
  pandoc guia.md -o guia.pdf --pdf-engine=wkhtmltopdf --css=emoji.css
  ```

---

## 📌 Resumindo
- Esse erro significa: *WeasyPrint não achou Cairo/Pango*.  
- Melhor solução no Windows: instalar o `.whl` pronto do Gohlke.  
- Alternativa prática: usar `wkhtmltopdf` ou navegador para PDF com emoji colorido.  

---

👉 Quer que eu te monte um **tutorial de instalação “sem dor” do wkhtmltopdf no Windows**, para você usar direto como `--pdf-engine=wkhtmltopdf` no Pandoc?

---

*Conversa exportada do ChatGPT*
*Processado em: 23/11/2025 14:36*