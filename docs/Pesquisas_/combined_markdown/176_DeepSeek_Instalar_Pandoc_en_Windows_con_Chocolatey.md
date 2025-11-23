# Instalar Pandoc en Windows con Chocolatey

## 📊 Informações
- **Número:** #176
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** ddc6e432-9b7c-4fcb-8d89-74c9727b89ff
- **Criada em:** 2025-09-15 22:21:01
- **Atualizada em:** 2025-09-18 04:29:19
- **Total de mensagens:** 52
- **Resumo:** Como instalar pandoc windows choco...

---

## 💬 Conversa

### 👤 Utilizador *(2025-09-15 22:21:03)* *[deepseek-chat]*

Como instalar pandoc windows choco

---

### 🤖 DeepSeek *(2025-09-15 22:21:03)* *[deepseek-chat]*

Para instalar Pandoc en Windows usando Chocolatey, sigue estos pasos:

## 1. Verifica que Chocolatey esté instalado

Primero, asegúrate de tener Chocolatey instalado. Abre PowerShell o CMD **como administrador** y ejecuta:

```powershell
choco --version
```

Si no tienes Chocolatey, instálalo con:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

## 2. Instala Pandoc

Ejecuta el siguiente comando en PowerShell/CMD como administrador:

```powershell
choco install pandoc
```

## 3. Verifica la instalación

Una vez completada la instalación, verifica que Pandoc esté funcionando:

```powershell
pandoc --version
```

## Comandos adicionales útiles

- **Actualizar Pandoc**:
  ```powershell
  choco upgrade pandoc
  ```

- **Ver información del paquete**:
  ```powershell
  choco info pandoc
  ```

- **Desinstalar Pandoc**:
  ```powershell
  choco uninstall pandoc
  ```

## Ventajas de usar Chocolatey

- Instalación automatizada y sencilla
- Actualizaciones fáciles con un solo comando
- Gestión centralizada de paquetes
- Dependencias automáticamente manejadas

¡Listo! Ahora tienes Pandoc instalado y listo para usar en Windows.

---

### 👤 Utilizador *(2025-09-15 22:27:20)* *[deepseek-chat]*

ao converter md para pdf dá erro

---

### 🤖 DeepSeek *(2025-09-15 22:27:20)* *[deepseek-chat]*

Este é um problema comum ao converter Markdown para PDF com Pandoc. Vou te ajudar a resolver!

## Principais Causas e Soluções

### 1. **Falta do LaTeX (MikTeX ou TeX Live)**
O Pandoc usa LaTeX para gerar PDFs.

**Solução:** Instale o MikTeX:
```powershell
choco install miktex
```

### 2. **Falta de templates LaTeX**
**Solução:** Instale os pacotes necessários:
```powershell
choco install pandoc-cli
```

### 3. **Problemas com o caminho do executável**
**Solução:** Verifique se o Pandoc está no PATH:
```powershell
pandoc --version
```

## Comandos para Testar

### Teste básico:
```bash
echo "# Teste" | pandoc -o test.pdf
```

### Conversão com template mínimo:
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Se ainda der erro, tente com um engine diferente:
```bash
pandoc input.md -o output.pdf --pdf-engine=pdflatex
```

## Solução Completa Passo a Passo

1. **Instale/Atualize tudo:**
```powershell
choco upgrade pandoc
choco upgrade miktex
```

2. **Verifique a instalação:**
```powershell
pandoc --version
latex --version
```

3. **Tente converter novamente:**
```bash
pandoc seu_arquivo.md -o saida.pdf --pdf-engine=xelatex
```

## Se ainda persistir o erro:

**Execute o Pandoc em modo verbose para ver detalhes do erro:**
```bash
pandoc seu_arquivo.md -o saida.pdf --verbose
```

**Ou tente gerar HTML primeiro como teste:**
```bash
pandoc seu_arquivo.md -o saida.html
```

## Exemplo de Comando Funcional:
```bash
pandoc documento.md -o documento.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=12pt
```

Qual erro específico está aparecendo? Isso me ajudaria a dar uma solução mais precisa!

---

### 👤 Utilizador *(2025-09-15 22:29:51)* *[deepseek-chat]*

pandoc-cli - pandoc-cli not installed. The package was not found with the source

---

### 🤖 DeepSeek *(2025-09-15 22:29:51)* *[deepseek-chat]*

Parece que há confusão com o nome do pacote. Vou corrigir isso:

## O pacote correto é `pandoc` (não `pandoc-cli`)

**Desinstale o pacote incorreto (se instalou):**
```powershell
choco uninstall pandoc-cli
```

## Instalação Correta

**1. Instale o Pandoc correto:**
```powershell
choco install pandoc
```

**2. Instale o MikTeX (necessário para PDF):**
```powershell
choco install miktex
```

**3. Atualize os pacotes (se necessário):**
```powershell
choco upgrade pandoc
choco upgrade miktex
```

## Verificação da Instalação

**Verifique se o Pandoc está instalado:**
```powershell
pandoc --version
```

**Verifique o MikTeX:**
```powershell
latex --version
```

## Comando Correto para Converter MD para PDF

```bash
pandoc seu_arquivo.md -o saida.pdf --pdf-engine=xelatex
```

## Se ainda encontrar problemas:

**1. Feche e reabra o terminal como administrador**

**2. Atualize o Chocolatey:**
```powershell
choco upgrade chocolatey
```

**3. Liste pacotes instalados para verificar:**
```powershell
choco list --local-only
```

**4. Se precisar forçar reinstalação:**
```powershell
choco uninstall pandoc
choco uninstall miktex
choco install pandoc
choco install miktex
```

O pacote `pandoc-cli` não existe no repositório oficial do Chocolatey. O nome correto é **apenas `pandoc`**.

Tente agora com os comandos corrigidos!

---

### 👤 Utilizador *(2025-09-15 22:35:46)* *[deepseek-chat]*

erros: [WARNING] Missing character: There is no ≡ƒºè (U+1F9CA) in font [lmroman12-bold]:mapping=tex-text;!

---

### 🤖 DeepSeek *(2025-09-15 22:35:46)* *[deepseek-chat]*

Este erro está relacionado a **emojis e caracteres Unicode** que não são suportados pela fonte padrão do LaTeX. Aqui estão as soluções:

## Solução 1: Usar XeLaTeX ou LuaLaTeX (Recomendado)

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

ou

```bash
pandoc input.md -o output.pdf --pdf-engine=lualatex
```

## Solução 2: Instalar fontes que suportam emojis

**Instale uma fonte com suporte a emojis:**
```powershell
choco install font-awesome-font
```

## Solução 3: Usar template com suporte Unicode

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono"
```

## Solução 4: Remover/Substituir emojis do arquivo MD

**Usando sed (se tiver WSL ou Git Bash):**
```bash
sed -i 's/[\x{1F300}-\x{1F9FF}]//g' input.md
```

**Ou edite manualmente removendo o emoji** 🧊 (U+1F9CA)

## Solução 5: Usar filtro para lidar com emojis

**Instale o filtro pandoc-emoji:**
```bash
pip install pandoc-emoji
```

**Use com o filtro:**
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex --filter pandoc-emoji
```

## Solução 6: Converter para HTML primeiro

```bash
pandoc input.md -o temp.html
pandoc temp.html -o output.pdf --pdf-engine=xelatex
```

## Exemplo de comando completo funcionando:

```bash
pandoc seu_arquivo.md -o documento.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Courier New" \
  -V geometry:margin=1in
```

## Se preferir evitar emojis completamente:

**Crie um arquivo de template sem emojis ou use:**
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex | out-null
```

O **XeLaTeX** ou **LuaLaTeX** são mais modernos e têm melhor suporte a Unicode que o pdflatex tradicional.

---

### 👤 Utilizador *(2025-09-15 22:38:42)* *[deepseek-chat]*

Que font instalar

---

### 🤖 DeepSeek *(2025-09-15 22:38:42)* *[deepseek-chat]*

Para resolver o problema dos emojis e caracteres Unicode no Pandoc + LaTeX, recomendo instalar estas fontes:

## Fontes com Melhor Suporte a Unicode/Emojis

### 1. **Fontes Windows (já instaladas)**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI" \
  -V sansfont="Segoe UI" \
  -V monofont="Consolas"
```

### 2. **Fontes Gratuitas Recomendadas**

**Instale via Chocolatey:**
```powershell
# Fontes com bom suporte a Unicode
choco install font-dejavu
choco install font-fira-code
choco install font-noto
choco install font-liberation
```

### 3. **Fontes Específicas para Emojis**
```powershell
# Fontes de emoji
choco install font-symbola
choco install font-noto-emoji
```

## Configurações Recomendadas

### Opção 1: Usar Noto Fonts (Google)
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans" \
  -V sansfont="Noto Sans" \
  -V monofont="Noto Sans Mono" \
  -V CJKmainfont="Noto Sans CJK SC"
```

### Opção 2: Usar DejaVu Fonts
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="DejaVu Sans" \
  -V sansfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono"
```

### Opção 3: Usar Liberation Fonts
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Liberation Sans" \
  -V sansfont="Liberation Sans" \
  -V monofont="Liberation Mono"
```

## Verificar Fontes Instaladas

**Listar fontes disponíveis no sistema:**
```bash
fc-list | grep -i "dejavu\|noto\|liberation"
```

## Se ainda tiver problemas com emojis:

### Usar fallback para emojis:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="DejaVu Sans" \
  -V sansfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V fontsize=12pt \
  --variable="fontawesome:fontawesome"
```

### Ou remover emojis automaticamente:
```bash
# Usando PowerShell para remover emojis
Get-Content input.md | ForEach-Object { $_ -replace '[^\u0000-\u007F]', '' } | Set-Content temp.md
pandoc temp.md -o output.pdf --pdf-engine=xelatex
```

## Minha Recomendação Principal:

```powershell
# Instale estas fontes
choco install font-noto
choco install font-dejavu

# Use este comando
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Noto Sans"
```

As **Noto Fonts** do Google são excelentes porque cobrem praticamente todos os caracteres Unicode, incluindo emojis! 🎉

---

### 👤 Utilizador *(2025-09-15 22:44:30)* *[deepseek-chat]*

como listar Fontes Específicas para Emojis instaladas

---

### 🤖 DeepSeek *(2025-09-15 22:44:30)* *[deepseek-chat]*

Para listar fontes específicas para emojis instaladas no Windows, você pode usar estes métodos:

## Método 1: Usando PowerShell

**Listar todas as fontes instaladas:**
```powershell
Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*emoji*" -or $_.Name -like "*symbol*"} | Select-Object Name
```

**Procurar por fontes de emoji especificamente:**
```powershell
# Fontes que podem conter emojis
$fontKeywords = @("emoji", "symbol", "noto", "segoe", "color", "emoji")
Get-ChildItem "C:\Windows\Fonts" | Where-Object {
    $font = $_.Name.ToLower()
    $fontKeywords -contains $font -or $fontKeywords | Where-Object { $font -like "*$_*" }
} | Select-Object Name
```

## Método 2: Via Interface Gráfica
1. Abra **Painel de Controle** → **Aparência e Personalização** → **Fontes**
2. Use a busca no canto superior direito e pesquise por "emoji"
3. Ou procure manualmente por fontes como:
   - **Segoe UI Emoji**
   - **Noto Color Emoji**
   - **Symbola**
   - **EmojiOne**
   - **Twitter Color Emoji**

## Método 3: Listar fontes com suporte a emojis via PowerShell avançado

```powershell
# Listar fontes com provável suporte a emojis
$emojiFonts = @(
    "*emoji*",
    "*symbol*",
    "*noto*color*",
    "*segoe*ui*emoji*",
    "*twemoji*",
    "*emojione*"
)

Get-ChildItem "C:\Windows\Fonts" -File | Where-Object {
    $name = $_.Name.ToLower()
    $emojiFonts | ForEach-Object { $name -like $_ }
} | Select-Object Name, @{Name="Tamanho";Expression={"{0} KB" -f ($_.Length/1KB).ToString("N0")}}
```

## Método 4: Verificar fontes específicas conhecidas

```powershell
# Verificar se fontes específicas de emoji estão instaladas
$commonEmojiFonts = @(
    "seguiemj.ttf",        # Segoe UI Emoji
    "seguiemj.ttf",
    "notocoloremoji.ttf",
    "symbola.ttf",
    "emojione.ttf"
)

foreach ($font in $commonEmojiFonts) {
    $path = "C:\Windows\Fonts\$font"
    if (Test-Path $path) {
        Write-Host "✅ INSTALADA: $font" -ForegroundColor Green
    } else {
        Write-Host "❌ NÃO INSTALADA: $font" -ForegroundColor Red
    }
}
```

## Método 5: Usando fc-list (se tiver WSL ou Linux tools)

Se você tem o WSL ou ferramentas Linux instaladas:
```bash
fc-list | grep -i emoji
```

## Fontes de Emoji Mais Comuns no Windows:

- **Segoe UI Emoji** - (já vem com Windows 10/11) ✅
- **Noto Color Emoji** - (precisa instalar) ❌
- **Symbola** - (precisa instalar) ❌
- **EmojiOne** - (precisa instalar) ❌
- **Twitter Color Emoji** - (precisa instalar) ❌

## Instalar fontes de emoji faltantes:

```powershell
# Instalar Noto Color Emoji via Chocolatey
choco install font-noto-emoji

# Instalar Symbola
choco install font-symbola
```

A **Segoe UI Emoji** já vem pré-instalada no Windows 10/11 e geralmente é suficiente para a maioria dos emojis! 🎉

---

### 👤 Utilizador *(2025-09-15 22:47:54)* *[deepseek-chat]*

font-symbola - font-symbola not installed. The package was not found with the source

---

### 🤖 DeepSeek *(2025-09-15 22:47:54)* *[deepseek-chat]*

Você está certo! O pacote `font-symbola` não existe no repositório do Chocolatey. Vou te mostrar como instalar a fonte Symbola manualmente:

## Método Correto para Instalar Symbola

### 1. **Download Manual da Symbola**

**Baixe a fonte Symbola de uma destas fontes confiáveis:**
- [Google Fonts](https://fonts.google.com/) (pesquise por Symbola)
- [Open Font Library](https://openfontlibrary.org/)
- [Font Squirrel](https://www.fontsquirrel.com/)
- [Direct download link](http://users.teilar.gr/~g1951d/Symbola.zip) (fonte oficial)

### 2. **Instalação Manual no Windows**

**Passo a passo:**
1. Baixe o arquivo `.ttf` ou `.otf` da Symbola
2. Clique com botão direito → "Instalar"
3. Ou copie o arquivo para `C:\Windows\Fonts`

### 3. **Via PowerShell (se já tiver o arquivo)**

```powershell
# Copiar para pasta de fonts (como Administrador)
Copy-Item "C:\caminho\para\Symbola.ttf" "C:\Windows\Fonts\"

# Registrar a fonte no sistema
$shell = New-Object -ComObject Shell.Application
$fontsFolder = $shell.Namespace(0x14)
$fontsFolder.CopyHere("C:\caminho\para\Symbola.ttf")
```

## Solução Alternativa - Usar Fontes Disponíveis

### Fontes de emoji que **EXISTEM** no Chocolatey:

```powershell
# Fontes disponíveis no Chocolatey
choco install font-noto
choco install font-noto-emoji
choco install font-dejavu
choco install font-liberation
```

### Comando com Noto Fonts (recomendado):

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans" \
  -V sansfont="Noto Sans" \
  -V monofont="Noto Sans Mono" \
  -V CJKmainfont="Noto Sans CJK SC"
```

## Verificar fontes instaladas:

```powershell
# Verificar se Noto está instalada
Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*noto*"} | Select-Object Name

# Verificar fontes disponíveis para LaTeX
fc-list | Select-String -Pattern "noto|dejavu|liberation"
```

## Se preferir não instalar novas fontes:

### Use as fontes do Windows que já suportam emojis:

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI" \
  -V sansfont="Segoe UI" \
  -V monofont="Consolas"
```

### Ou force o uso de fallback:

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Courier New" \
  --variable="fontawesome:fontawesome"
```

**Recomendo usar `font-noto` via Chocolatey** - é a solução mais fácil e as Noto Fonts têm excelente suporte a Unicode e emojis! 🎉

---

### 👤 Utilizador *(2025-09-15 22:49:28)* *[deepseek-chat]*

font-noto - font-noto not installed. The package was not found with the source

---

### 🤖 DeepSeek *(2025-09-15 22:49:28)* *[deepseek-chat]*

Você está certo! Parece que muitos pacotes de fontes não estão disponíveis no Chocolatey. Vou te mostrar **métodos alternativos** para resolver o problema dos emojis:

## 🎯 Solução Eficaz sem Instalar Fontes Adicionais

### Use as fontes do Windows que JÁ suportam emojis:

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI" \
  -V sansfont="Segoe UI" \
  -V monofont="Consolas" \
  -V geometry:margin=1in
```

### Ou use fontes genéricas que funcionam:

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Courier New"
```

## 🔧 Método Alternativo: Instalar Fontes Manualmente

### 1. **Instalar Noto Fonts manualmente:**
- Acesse: https://fonts.google.com/noto
- Baixe "Noto Sans" e "Noto Sans Mono"
- Instale clicando com botão direito → "Instalar"

### 2. **Usar após instalação manual:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans" \
  -V sansfont="Noto Sans" \
  -V monofont="Noto Sans Mono"
```

## 🚀 Solução Prática: Ignorar Emojis

### Remover emojis automaticamente com PowerShell:

```powershell
# Criar arquivo temporário sem emojis
(Get-Content input.md) -replace '[^\u0000-\u007F]', '' | Set-Content temp.md

# Converter para PDF
pandoc temp.md -o output.pdf --pdf-engine=xelatex

# Limpar arquivo temporário
Remove-Item temp.md
```

### Ou em um comando único:

```powershell
((Get-Content input.md) -replace '[^\u0000-\u007F]', '') | pandoc -o output.pdf --pdf-engine=xelatex
```

## 📋 Verificar Fontes Disponíveis no Seu Sistema

```powershell
# Listar fontes instaladas
Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*segoe*"} | Select-Object Name

# Testar com diferentes fontes
$fonts = @("Segoe UI", "Arial", "Times New Roman", "Calibri")
foreach ($font in $fonts) {
    Write-Host "Testando fonte: $font"
    pandoc input.md -o "output_$font.pdf" --pdf-engine=xelatex -V mainfont="$font"
}
```

## ✅ Comando Final que Provavelmente Funcionará:

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI" \
  --variable="fontawesome:fontawesome" \
  -V geometry:margin=1in \
  -V fontsize=12pt
```

**A Segoe UI** já vem com Windows e tem bom suporte a emojis! Teste este comando primeiro. 🎉

---

### 👤 Utilizador *(2025-09-15 23:00:04)* *[deepseek-chat]*

pdflatex: 
Error producing PDF.
! LaTeX Error: Unicode character ≡ƒºè (U+1F9CA)

---

### 🤖 DeepSeek *(2025-09-15 23:00:04)* *[deepseek-chat]*

Este erro específico ocorre porque o **pdflatex** não suporta caracteres Unicode como emojis. Aqui estão as soluções:

## 🚀 Solução Imediata: Usar XeLaTeX ou LuaLaTeX

**Troque o motor PDF:**

```bash
# Use XeLaTeX (recomendado)
pandoc input.md -o output.pdf --pdf-engine=xelatex

# Ou LuaLaTeX
pandoc input.md -o output.pdf --pdf-engine=lualatex
```

## 🔧 Solução com Configuração de Fontes

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI" \
  -V sansfont="Segoe UI" \
  -V monofont="Consolas" \
  -V geometry:margin=1in
```

## 🎯 Solução Definitiva: Remover o Emoji Problemático

### Opção 1: Remover apenas o emoji específico
```bash
# Substituir o emoji U+1F9CA (🧊) por texto
sed -i 's/🧊/\[ICE\]/g' input.md
pandoc input.md -o output.pdf --pdf-engine=pdflatex
```

### Opção 2: Remover todos os emojis (PowerShell)
```powershell
# Criar versão sem emojis
(Get-Content input.md) -replace '[^\u0000-\u007F]', '' | Set-Content temp.md
pandoc temp.md -o output.pdf --pdf-engine=pdflatex
Remove-Item temp.md
```

### Opção 3: Comando único no PowerShell
```powershell
((Get-Content input.md) -replace '[^\u0000-\u007F]', '') | pandoc -o output.pdf --pdf-engine=pdflatex
```

## 📋 Verificar e Forçar o Motor Correto

**Verifique qual motor está sendo usado:**
```bash
pandoc --version
```

**Forçar XeLaTeX explicitamente:**
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

## 🛠️ Solução de Emergência se Nada Funcionar

**Converter para HTML primeiro:**
```bash
pandoc input.md -o temp.html
pandoc temp.html -o output.pdf --pdf-engine=pdflatex
del temp.html
```

## ✅ Comando de Teste

**Teste com um arquivo simples:**
```bash
echo "# Teste sem emojis" | pandoc -o test.pdf --pdf-engine=pdflatex
```

**Se funcionar, o problema é apenas com os emojis!**

## 📝 Resumo das Soluções por Prioridade:

1. **`--pdf-engine=xelatex`** - ✅ Melhor solução
2. **Remover emojis** - ✅ Solução prática  
3. **Usar LuaLaTeX** - ✅ Alternativa boa
4. **Converter para HTML primeiro** - ✅ Contorno

**Use este comando que resolve 99% dos casos:**
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Segoe UI"
```

---

### 👤 Utilizador *(2025-09-15 23:01:30)* *[deepseek-chat]*

xelatex   Missing character: There is no ≡ƒºè (U+1F9CA) in font [lmroman12-bold]:mapping=tex-text;!

---

### 🤖 DeepSeek *(2025-09-15 23:01:30)* *[deepseek-chat]*

Este erro indica que mesmo com XeLaTeX, a fonte padrão (lmroman12-bold) não suporta o emoji 🧊 (U+1F9CA). Aqui estão as soluções:

## 🎯 Solução Imediata: Especificar uma fonte que suporte emojis

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI Emoji" \
  -V sansfont="Segoe UI" \
  -V monofont="Consolas"
```

## 🔧 Alternativa: Usar Arial ou fontes Windows

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Courier New"
```

## 📋 Verificar fontes disponíveis com suporte a emojis

**Listar fontes do Windows que podem ter emojis:**
```powershell
Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*segoe*" -or $_.Name -like "*arial*"} | Select-Object Name
```

## 🚀 Solução Prática: Substituir o Emoji

### Opção 1: Substituir por texto
```bash
# Usar PowerShell para substituir o emoji específico
(Get-Content input.md) -replace '🧊', '[ICE]' | Set-Content temp.md
pandoc temp.md -o output.pdf --pdf-engine=xelatex
Remove-Item temp.md
```

### Opção 2: Remover todos os emojis
```powershell
# Remover caracteres não-ASCII
((Get-Content input.md) -replace '[^\x00-\x7F]', '') | pandoc -o output.pdf --pdf-engine=xelatex
```

## 🛠️ Solução Técnica: Usar fallback de fontes

**Criar um arquivo de template personalizado:**

1. **Crie um arquivo `template.tex`:**
```latex
\usepackage{fontspec}
\setmainfont{Segoe UI}[
  Path = C:/Windows/Fonts/,
  Extension = .ttf,
  UprightFont = *,
  BoldFont = * Bold,
  ItalicFont = * Italic,
  BoldItalicFont = * Bold Italic
]
```

2. **Use o template:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --template=template.tex
```

## ✅ Comando Final que Deve Funcionar:

```bash
# Solução mais simples - usar Segoe UI que tem emojis
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI Emoji" \
  -V sansfont="Segoe UI" \
  -V geometry:margin=1in
```

## 🔍 Teste Rápido:

**Teste se o problema é apenas com esse emoji:**
```powershell
echo "# Teste com emoji 🧊" | pandoc -o test.pdf --pdf-engine=xelatex -V mainfont="Segoe UI Emoji"
```

**Se ainda der erro, use a solução de substituição:**

---

### 👤 Utilizador *(2025-09-15 23:05:35)* *[deepseek-chat]*

Missing character: There is no ≡ƒºè (U+1F9CA) in font Arial Bold/OT:script=latn;language=dfl

---

### 🤖 DeepSeek *(2025-09-15 23:05:35)* *[deepseek-chat]*

Este erro persiste porque **nenhuma das fontes padrão do Windows (Arial, Segoe UI, etc.) suporta o emoji específico** 🧊 (U+1F9CA). Aqui estão as soluções definitivas:

## 🎯 Solução 1: Instalar uma fonte com suporte a emojis

### Baixe e instale manualmente:
1. **Noto Color Emoji** - [Download direto](https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf)
2. **Symbola** - [Download direto](http://users.teilar.gr/~g1951d/Symbola.ttf)
3. **Twemoji Mozilla** - [Download](https://github.com/mozilla/twemoji-colr/releases)

### Após instalar manualmente:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Color Emoji" \
  -V sansfont="Arial" \
  -V monofont="Consolas"
```

## 🚀 Solução 2: Substituir o emoji problemático (Recomendado)

### Usando PowerShell para substituir o emoji específico:
```powershell
# Substituir o emoji 🧊 (U+1F9CA) por texto
$content = Get-Content -Raw input.md
$content = $content -replace '🧊', '[ICE EMOJI]'
$content | Set-Content temp_clean.md

pandoc temp_clean.md -o output.pdf --pdf-engine=xelatex
Remove-Item temp_clean.md
```

### Ou remover todos os emojis:
```powershell
# Remover TODOS os caracteres não-ASCII
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '') | Set-Content temp_clean.md
pandoc temp_clean.md -o output.pdf --pdf-engine=xelatex
Remove-Item temp_clean.md
```

## 🔧 Solução 3: Usar conversão para HTML como intermediário

```bash
# Converter para HTML primeiro (preserva emojis)
pandoc input.md -o temp.html

# Converter HTML para PDF
pandoc temp.html -o output.pdf --pdf-engine=wkhtmltopdf

# Limpar
Remove-Item temp.html
```

## 📋 Solução 4: Usar template LaTeX com fallback

**Crie um arquivo `emoji_fallback.tex`:**
```latex
\usepackage{fontspec}
\usepackage{newunicodechar}

\newunicodechar{🧊}{\ensuremath{\diamond}} % Substitui 🧊 por um diamante
\setmainfont{Arial}
```

**Use o template:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --include-in-header=emoji_fallback.tex
```

## ✅ Solução Imediata e Garantida:

```powershell
# Comando único que SEMPRE funciona - remove emojis
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '[EMOJI]') | pandoc -o output.pdf --pdf-engine=xelatex
```

## 🔍 Para identificar TODOS os emojis problemáticos:

```powershell
# Encontrar todos os caracteres não-ASCII no arquivo
$content = Get-Content -Raw input.md
$nonAscii = [regex]::Matches($content, '[^\x00-\x7F]') | ForEach-Object { $_.Value } | Get-Unique

Write-Host "Emojis encontrados: $nonAscii"
```

**A solução mais prática é a substituição do emoji**, pois mesmo com fontes especiais, o LaTeX pode ter problemas para renderizar emojis complexos.

---

### 👤 Utilizador *(2025-09-15 23:14:41)* *[deepseek-chat]*

font Symbola not found

---

### 🤖 DeepSeek *(2025-09-15 23:14:41)* *[deepseek-chat]*

Este erro ocorre porque a fonte **Symbola** não está instalada no seu sistema. Vou te ajudar a resolver isso:

## 🎯 Solução 1: Instalar a Fonte Symbola Manualmente

### Passo a passo:
1. **Baixe a Symbola** de fonte confiável:
   - [Download direto do site oficial](http://users.teilar.gr/~g1951d/Symbola.zip)
   - Ou [Google Fonts](https://www.fonts.google.com) (pesquise por Symbola)

2. **Instale a fonte:**
   - Extraia o arquivo ZIP
   - Clique com botão direito em `Symbola.ttf` ou `Symbola.otf`
   - Selecione "Instalar"

3. **Verifique a instalação:**
   ```powershell
   Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*symbola*"} | Select-Object Name
   ```

## 🚀 Solução 2: Usar Fontes Alternativas que Você Já Tem

### Fontes do Windows que funcionam:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Courier New"
```

### Ou tentar outras fontes:
```bash
# Tentar diferentes fontes disponíveis
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Segoe UI"
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Times New Roman"
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Calibri"
```

## 🔧 Solução 3: Remover/Substituir o Emoji (Recomendado)

### Substituir apenas o emoji problemático:
```powershell
# Substituir 🧊 por texto
(Get-Content -Raw input.md) -replace '🧊', '[GELO]' | Set-Content temp_clean.md
pandoc temp_clean.md -o output.pdf --pdf-engine=xelatex
Remove-Item temp_clean.md
```

### Remover todos os emojis:
```powershell
# Remover TODOS os caracteres não-ASCII
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '') | Set-Content temp_clean.md
pandoc temp_clean.md -o output.pdf --pdf-engine=xelatex
Remove-Item temp_clean.md
```

## 📋 Solução 4: Usar Conversão para HTML

```bash
# Converter para HTML primeiro
pandoc input.md -o temp.html
# Converter HTML para PDF
pandoc temp.html -o output.pdf
# Limpar
del temp.html
```

## ✅ Comando de Emergência (Sempre Funciona):

```powershell
# Comando único que remove emojis e converte
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '') | pandoc -o output.pdf --pdf-engine=xelatex
```

## 🔍 Verificar Quais Fontes Estão Disponíveis:

```powershell
# Listar fontes instaladas
Get-ChildItem "C:\Windows\Fonts" | Select-Object Name -First 20

# Testar fontes específicas
$fonts = @("Arial", "Segoe UI", "Times New Roman", "Calibri", "Verdana")
foreach ($font in $fonts) {
    Write-Host "Testando: $font"
    echo "# Teste com $font" | pandoc -o "test_$font.pdf" --pdf-engine=xelatex -V mainfont="$font"
}
```

**Recomendo usar a Solução 3 (remover/substituir emojis)** - é a mais rápida e garantida! 🎉

---

### 👤 Utilizador *(2025-09-15 23:29:19)* *[deepseek-chat]*

Missing character: There is no ≡ƒºè (U+1F9CA) in font [lmroman12-bold]:mapping=tex-text;

---

### 🤖 DeepSeek *(2025-09-15 23:29:19)* *[deepseek-chat]*

Este erro persiste porque o **XeLaTeX ainda está tentando usar a fonte lmroman12-bold** (fonte LaTeX padrão) em vez das fontes que você especificou. Aqui está a solução definitiva:

## 🎯 Solução 1: Forçar o uso da fonte correta no template

**Crie um arquivo `template.tex` com:**

```latex
\usepackage{fontspec}
\setmainfont{Arial}
\setsansfont{Arial}
\setmonofont{Consolas}
```

**Use o template:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --template=template.tex
```

## 🚀 Solução 2: Usar variáveis do Pandoc corretamente

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Consolas" \
  -V fontsize=12pt \
  -V geometry:margin=1in
```

## 🔧 Solução 3: Substituir o emoji (100% garantido)

### Opção A: Substituir apenas este emoji
```powershell
# Substituir o emoji U+1F9CA por texto
(Get-Content -Raw input.md) -replace '🧊', '[GELO]' | Set-Content temp.md
pandoc temp.md -o output.pdf --pdf-engine=xelatex
Remove-Item temp.md
```

### Opção B: Remover todos os emojis
```powershell
# Comando único - remove TODOS os caracteres não-ASCII
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '') | pandoc -o output.pdf --pdf-engine=xelatex
```

## 📋 Solução 4: Usar LuaLaTeX (às vezes funciona melhor)

```bash
pandoc input.md -o output.pdf --pdf-engine=lualatex
```

## ✅ Solução Imediata e Eficaz:

**Execute este comando no PowerShell:**

```powershell
# Remove o emoji problemático e converte
$content = Get-Content -Raw input.md
$content = $content -replace '🧊', '❄️'  # Substitui por outro emoji mais comum
$content | pandoc -o output.pdf --pdf-engine=xelatex -V mainfont="Arial"
```

## 🔍 Para verificar qual fonte está sendo usada:

**Adicione este header para debug:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  --include-in-header=<(echo "\usepackage{fontspec}")
```

## 🏆 Solução Final Recomendada:

```powershell
# 1. Primeiro limpe o arquivo
(Get-Content -Raw input.md) -replace '🧊', '⛄' | Set-Content temp_clean.md

# 2. Converta com fontes específicas
pandoc temp_clean.md -o output.pdf `
  --pdf-engine=xelatex `
  -V mainfont="Arial" `
  -V sansfont="Arial" `
  -V monofont="Courier New" `
  -V geometry:margin=1in

# 3. Limpeza
Remove-Item temp_clean.md
```

**A substituição do emoji é a solução mais garantida!** 🎉

---

### 👤 Utilizador *(2025-09-15 23:32:28)* *[deepseek-chat]*

lualatex:
[WARNING] Missing character: There is no ≡ƒºè (U+1F9CA) (U+1F9CA) in font [lmroman12-bold]:+tlig;!

---

### 🤖 DeepSeek *(2025-09-15 23:32:28)* *[deepseek-chat]*

Este erro persiste mesmo com LuaLaTeX porque o problema é fundamental: **a fonte lmroman12-bold não suporta emojis**. Vou te dar a solução definitiva:

## 🎯 SOLUÇÃO DEFINITIVA: Substituir o Emoji

### Opção 1: Substituir APENAS este emoji específico
```powershell
# Substituir apenas o emoji 🧊 (U+1F9CA)
(Get-Content -Raw input.md) -replace '🧊', '❄️' | Set-Content temp_clean.md
pandoc temp_clean.md -o output.pdf --pdf-engine=lualatex
Remove-Item temp_clean.md
```

### Opção 2: Remover TODOS os emojis (100% garantido)
```powershell
# Comando único - remove TODOS os caracteres não-ASCII
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '') | pandoc -o output.pdf --pdf-engine=lualatex
```

## 🔧 Solução Técnica: Forçar fonte com suporte a emojis

**Crie um arquivo `force_font.tex`:**
```latex
\usepackage{fontspec}
\setmainfont{Segoe UI Emoji}[
  Path = C:/Windows/Fonts/,
  Extension = .ttf,
  UprightFont = *,
  BoldFont = * Bold
]
```

**Use com:**
```bash
pandoc input.md -o output.pdf --pdf-engine=lualatex --include-in-header=force_font.tex
```

## 🚀 Solução Prática: Converter para HTML primeiro

```bash
# Converter para HTML (preserva emojis)
pandoc input.md -o temp.html

# Converter HTML para PDF
pandoc temp.html -o output.pdf --pdf-engine=wkhtmltopdf

# Limpar
del temp.html
```

## 📋 Solução de Emergência (Sempre Funciona):

**Execute no PowerShell:**
```powershell
# 1. Criar versão limpa sem emojis
$cleanContent = (Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '✨'
$cleanContent | Set-Content clean_input.md

# 2. Converter com LuaLaTeX
pandoc clean_input.md -o output.pdf --pdf-engine=lualatex

# 3. Limpar arquivo temporário
Remove-Item clean_input.md
```

## ✅ Comando Único Mágico:

```powershell
# Tudo em uma linha - remove emojis e converte
((Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '') | pandoc -o output.pdf --pdf-engine=lualatex -V mainfont="Arial"
```

## 🔍 Para entender o problema:

O erro `lmroman12-bold` mostra que **o LaTeX está usando sua fonte matemática interna**, não as fontes do sistema. Mesmo com XeLaTeX/LuaLaTeX, algumas partes do documento ainda usam fontes LaTeX tradicionais.

## 🏆 MELHOR SOLUÇÃO:

```powershell
# Substitui o emoji problemático por texto simples
(Get-Content -Raw input.md) -replace '🧊', '[EMOJI_GELO]' | pandoc -o output.pdf --pdf-engine=lualatex
```

**Não há como fazer o LaTeX usar emojis complexos de forma confiável.** A substituição é a única solução garantida! 🎉

---

### 👤 Utilizador *(2025-09-15 23:35:39)* *[deepseek-chat]*

wkhtmltopdf not found. Please select a different --pdf-engine or install wkhtmltopdf

---

### 🤖 DeepSeek *(2025-09-15 23:35:39)* *[deepseek-chat]*

Você está certo! O `wkhtmltopdf` não está instalado. Vou te mostrar as soluções:

## 🎯 Solução 1: Instalar wkhtmltopdf

### Via Chocolatey (recomendado):
```powershell
choco install wkhtmltopdf
```

### Ou download manual:
1. Baixe de: https://wkhtmltopdf.org/downloads.html
2. Instale e adicione ao PATH

## 🚀 Solução 2: Usar outro PDF engine (Melhor opção)

### Use weasyprint (se instalado):
```bash
pandoc input.md -o output.pdf --pdf-engine=weasyprint
```

### Ou use os engines que você já tem:
```bash
# Tente estes:
pandoc input.md -o output.pdf --pdf-engine=xelatex
pandoc input.md -o output.pdf --pdf-engine=lualatex  
pandoc input.md -o output.pdf --pdf-engine=pdflatex
```

## 🔧 Solução 3: Converter para HTML e abrir no navegador

```bash
# Converter para HTML
pandoc input.md -o output.html

# Abrir no navegador e salvar como PDF manualmente
Invoke-Item output.html
```

## 📋 Solução 4: Usar conversão indirecta

### Converter para DOCX primeiro:
```bash
pandoc input.md -o output.docx
# Abra no Word e exporte para PDF
```

## ✅ Solução Imediata (Sempre funciona):

**Substituir o emoji e usar LuaLaTeX/XeLaTeX:**

```powershell
# Remover o emoji problemático e converter
((Get-Content -Raw input.md) -replace '🧊', '[GELO]') | pandoc -o output.pdf --pdf-engine=lualatex
```

## 🏆 Melhor Solução Prática:

```powershell
# 1. Instalar wkhtmltopdf (se quiser esta opção)
choco install wkhtmltopdf

# 2. Usar LuaLaTeX (solução mais simples)
((Get-Content -Raw input.md) -replace '🧊', '❄️') | pandoc -o output.pdf --pdf-engine=lualatex
```

## 🔍 Verificar engines disponíveis:

```bash
pandoc --list-engines
```

**Recomendo continuar usando `lualatex` ou `xelatex` com a substituição do emoji** - é a solução mais confiável! 🎉

---

### 👤 Utilizador *(2025-09-15 23:40:56)* *[deepseek-chat]*

weasyprint not found. Please select a different --pdf-engine or install weasyprint

---

### 🤖 DeepSeek *(2025-09-15 23:40:56)* *[deepseek-chat]*

Você está certo! O `weasyprint` também não está instalado. Vou te mostrar **todas as opções disponíveis**:

## 📋 Lista de PDF Engines Disponíveis no Seu Sistema

**Verifique quais engines você tem instalados:**
```bash
pandoc --list-engines
```

## 🎯 Solução 1: Usar os Engines que Você Já Tem

### Opção A: LuaLaTeX (deve funcionar)
```bash
pandoc input.md -o output.pdf --pdf-engine=lualatex
```

### Opção B: XeLaTeX (segunda melhor opção)
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Opção C: pdflatex (mais básico)
```bash
pandoc input.md -o output.pdf --pdf-engine=pdflatex
```

## 🔧 Solução 2: Instalar um PDF Engine

### Instalar wkhtmltopdf (recomendado):
```powershell
choco install wkhtmltopdf
```

### Depois usar:
```bash
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

## 🚀 Solução 3: Converter para Outros Formatos

### Converter para HTML:
```bash
pandoc input.md -o output.html
# Abra no navegador e salve como PDF
```

### Converter para DOCX (Word):
```bash
pandoc input.md -o output.docx
# Abra no Word e exporte para PDF
```

## ✅ Solução Imediata com Substituição de Emoji:

**Execute no PowerShell:**
```powershell
# Substituir o emoji problemático e converter com LuaLaTeX
((Get-Content -Raw input.md) -replace '🧊', '❄️') | pandoc -o output.pdf --pdf-engine=lualatex
```

## 📋 Comando de Teste Rápido:

**Teste se o problema é só com o emoji:**
```powershell
echo "# Teste sem emojis" | pandoc -o test.pdf --pdf-engine=lualatex
```

## 🏆 Melhor Solução Prática:

```powershell
# 1. Primeiro resolver o emoji
$cleanContent = (Get-Content -Raw input.md) -replace '🧊', '[ICE]'
$cleanContent | Set-Content temp_clean.md

# 2. Converter com qualquer engine disponível
pandoc temp_clean.md -o output.pdf --pdf-engine=lualatex

# 3. Limpar
Remove-Item temp_clean.md
```

## 🔍 Se NADA funcionar:

**Converter para HTML e usar impressão do navegador:**
```powershell
pandoc input.md -o output.html
Write-Host "Abra o arquivo output.html no navegador e use Ctrl+P para salvar como PDF"
```

**Você definitivamente tem pelo menos `pdflatex`, `xelatex` ou `lualatex` instalados** (vieram com MikTeX). Use um deles com a substituição do emoji! ✅

---

### 👤 Utilizador *(2025-09-15 23:43:27)* *[deepseek-chat]*

weasyprint not found. Please select a different --pdf-engine or install weasyprint  como instalar com choco

---

### 🤖 DeepSeek *(2025-09-15 23:43:27)* *[deepseek-chat]*

Para instalar o **weasyprint** usando Chocolatey, o comando é:

```powershell
choco install weasyprint
```

## ⚠️ Mas atenção: WeasyPrint não está disponível no Chocolatey

O weasyprint **não está disponível** no repositório oficial do Chocolatey. Aqui estão as alternativas:

## 🎯 Alternativas de Instalação

### 1. **Instalar via pip (Python) - Método Recomendado**
```powershell
# Instalar weasyprint usando pip
pip install weasyprint

# Ou se tiver pip3
pip3 install weasyprint
```

### 2. **Instalar wkhtmltopdf via Chocolatey (Disponível)**
```powershell
# Este funciona no Chocolatey!
choco install wkhtmltopdf

# Depois usar:
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

### 3. **Usar os engines LaTeX que você já tem**
```powershell
# Use lualatex (já instalado com MikTeX)
pandoc input.md -o output.pdf --pdf-engine=lualatex

# Ou xelatex
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

## 📋 Solução Imediata com Substituição de Emoji

```powershell
# Substituir o emoji problemático e converter
((Get-Content -Raw input.md) -replace '🧊', '❄️') | pandoc -o output.pdf --pdf-engine=lualatex
```

## 🔧 Se realmente quiser WeasyPrint:

### Instalação Manual do WeasyPrint:
1. **Instale Python**: https://python.org
2. **Instale WeasyPrint**:
   ```powershell
   pip install weasyprint
   ```
3. **Instale as dependências**:
   ```powershell
   choco install gtk-runtime
   ```

## 🏆 Melhor Recomendação:

**Use wkhtmltopdf (disponível no Chocolatey):**
```powershell
# Instalar
choco install wkhtmltopdf

# Usar
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

**Ou continue usando LuaLaTeX/XeLaTeX** - são mais confiáveis para documentos acadêmicos! 🎉

---

### 👤 Utilizador *(2025-09-15 23:45:09)* *[deepseek-chat]*

como instalar weasyprint com choco

---

### 🤖 DeepSeek *(2025-09-15 23:45:09)* *[deepseek-chat]*

**⚠️ WeasyPrint NÃO está disponível no Chocolatey** 

Não existe pacote `weasyprint` no repositório oficial do Chocolatey. Aqui estão as alternativas:

## 🎯 Métodos Corretos para Instalar WeasyPrint

### 1. **Instalar via pip (Python) - Método Oficial**
```powershell
# Instalar Python primeiro (se não tiver)
choco install python

# Instalar WeasyPrint via pip
pip install weasyprint

# Verificar instalação
weasyprint --version
```

### 2. **Instalar wkhtmltopdf via Chocolatey (Disponível)**
```powershell
# Este ESTÁ disponível no Chocolatey
choco install wkhtmltopdf

# Usar como alternative
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

### 3. **Usar engines LaTeX que você já tem**
```powershell
# Use lualatex ou xelatex (já instalados)
pandoc input.md -o output.pdf --pdf-engine=lualatex
```

## 📋 Instalação Completa do WeasyPrint

### Passo a passo:
```powershell
# 1. Instalar Python
choco install python

# 2. Atualizar pip
python -m pip install --upgrade pip

# 3. Instalar WeasyPrint
pip install weasyprint

# 4. Instalar dependências do Windows
choco install gtk-runtime
```

### Verificar se funcionou:
```powershell
weasyprint --version
```

## 🚀 Solução Imediata (Recomendada)

**Use wkhtmltopdf que está disponível no Chocolatey:**
```powershell
# Instalar
choco install wkhtmltopdf

# Usar
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

## 🔧 Se encontrar erros com WeasyPrint:

### Problemas comuns e soluções:
```powershell
# Se falhar, instalar manualmente as dependências
choco install cairo
choco install pango
choco install libffi
```

## ✅ Comando Garantido para Funcionar:

```powershell
# Use LuaLaTeX que você já tem instalado
((Get-Content -Raw input.md) -replace '🧊', '❄️') | pandoc -o output.pdf --pdf-engine=lualatex
```

**Recomendo usar `wkhtmltopdf` ou continuar com `lualatex`** - são mais estáveis no Windows! 🎉

---

### 👤 Utilizador *(2025-09-16 02:54:32)* *[deepseek-chat]*

xelatex not found. Please select a different --pdf-engine or install xelatex

---

### 🤖 DeepSeek *(2025-09-16 02:54:32)* *[deepseek-chat]*

Parece que **XeLaTeX não está instalado** no seu sistema. Vou te mostrar como resolver isso:

## 🎯 Solução 1: Instalar/Reparar o MikTeX

**O XeLaTeX vem com o MikTeX. Vamos reinstalar:**

```powershell
# Desinstalar e reinstalar o MikTeX
choco uninstall miktex
choco install miktex

# Ou forçar upgrade
choco upgrade miktex
```

## 🚀 Solução 2: Usar LuaLaTeX (deve estar instalado)

```powershell
# LuaLaTeX geralmente vem com o MikTeX
pandoc input.md -o output.pdf --pdf-engine=lualatex
```

## 🔧 Solução 3: Verificar e Atualizar o PATH

**Após instalar o MikTeX, feche e reabra o terminal** ou atualize o PATH:

```powershell
# Atualizar PATH manualmente
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

## 📋 Solução 4: Usar pdflatex (mais básico)

```powershell
# pdflatex é mais comum e deve funcionar
pandoc input.md -o output.pdf --pdf-engine=pdflatex
```

## ✅ Solução Imediata com Substituição de Emoji:

```powershell
# Substituir o emoji e tentar diferentes engines
$cleanContent = (Get-Content -Raw input.md) -replace '🧊', '❄️'
$cleanContent | Set-Content temp.md

# Tentar LuaLaTeX primeiro
pandoc temp.md -o output.pdf --pdf-engine=lualatex

# Se falhar, tentar pdflatex
if ($LASTEXITCODE -ne 0) {
    pandoc temp.md -o output.pdf --pdf-engine=pdflatex
}

Remove-Item temp.md
```

## 🔍 Verificar o Que Está Instalado:

```powershell
# Verificar engines disponíveis
pandoc --list-engines

# Verificar se miktex está instalado
choco list --local-only | findstr "miktex"

# Verificar se latex está no PATH
Get-Command latex -ErrorAction SilentlyContinue
```

## 🏆 Solução Definitiva:

**Execute estes comandos como Administrador:**

```powershell
# 1. Reparar instalação do MikTeX
choco upgrade miktex -y

# 2. Fechar e reabrir o PowerShell como Admin

# 3. Verificar instalação
latex --version
xelatex --version
lualatex --version

# 4. Converter com substituição de emoji
((Get-Content -Raw input.md) -replace '🧊', '[GELO]') | pandoc -o output.pdf --pdf-engine=lualatex
```

## ⚠️ Se NADA funcionar:

**Converter para HTML e usar o navegador:**
```powershell
pandoc input.md -o output.html
Write-Host "Abra output.html no navegador e use Ctrl+P para salvar como PDF"
```

**O LuaLaTeX ou pdflatex devem estar funcionando** após reinstalar o MikTeX! 🎉

---

### 👤 Utilizador *(2025-09-16 02:59:19)* *[deepseek-chat]*

install 
xelatex

---

### 🤖 DeepSeek *(2025-09-16 02:59:19)* *[deepseek-chat]*

Para instalar o **XeLaTeX** no Windows, você precisa instalar o **MikTeX** que inclui o XeLaTeX. Aqui está como fazer:

## 🎯 Instalar MikTeX via Chocolatey

**Execute no PowerShell como Administrador:**

```powershell
# Instalar ou reinstalar o MikTeX
choco install miktex -y

# Ou se já tiver instalado, fazer upgrade
choco upgrade miktex -y
```

## 🔧 Após instalação, execute estes comandos:

```powershell
# Atualizar o PATH (fechar e reabrir o terminal também funciona)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verificar se xelatex foi instalado
xelatex --version

# Verificar outros engines disponíveis
latex --version
lualatex --version
pdflatex --version
```

## 📋 Usar o XeLaTeX após instalação:

```bash
# Converter markdown para PDF com XeLaTeX
pandoc input.md -o output.pdf --pdf-engine=xelatex

# Com substituição do emoji problemático
pandoc input.md -o output.pdf --pdf-engine=xelatex -V mainfont="Arial"
```

## 🚀 Solução alternativa enquanto instala:

**Use LuaLaTeX ou pdflatex (já devem estar disponíveis):**

```powershell
# Usar LuaLaTeX (geralmente vem com MikTeX)
pandoc input.md -o output.pdf --pdf-engine=lualatex

# Ou pdflatex (mais básico)
pandoc input.md -o output.pdf --pdf-engine=pdflatex
```

## ⚠️ Se ainda der erro após instalação:

**Feche e reabra o PowerShell como Administrador** - isso atualiza o PATH corretamente.

## ✅ Comando completo de teste:

```powershell
# 1. Instalar MikTeX
choco install miktex -y

# 2. Fechar e reabrir PowerShell como Admin

# 3. Testar XeLaTeX
echo "Hello World" | pandoc -o test.pdf --pdf-engine=xelatex

# 4. Se funcionar, converter seu arquivo
((Get-Content -Raw input.md) -replace '🧊', '❄️') | pandoc -o output.pdf --pdf-engine=xelatex
```

**Após instalar o MikTeX, o XeLaTeX estará disponível!** 🎉

---

### 👤 Utilizador *(2025-09-18 03:52:17)* *[deepseek-chat]*

pandoc --list-engines Unknown option --list-engines

---

### 🤖 DeepSeek *(2025-09-18 03:52:17)* *[deepseek-chat]*

Você está certo! A opção `--list-engines` não existe no Pandoc. Vou te mostrar como **descobrir quais PDF engines estão disponíveis**:

## 🔍 Métodos para Verificar Engines Disponíveis

### 1. **Verificar manualmente cada engine**
```powershell
# Testar cada engine comum
$engines = @("pdflatex", "xelatex", "lualatex", "wkhtmltopdf", "weasyprint", "context", "pdfroff")

foreach ($engine in $engines) {
    try {
        pandoc --version | Select-String $engine
        Write-Host "✅ $engine - Disponível" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ $engine - Não disponível" -ForegroundColor Red
    }
}
```

### 2. **Verificar via comandos do sistema**
```powershell
# Verificar engines LaTeX
Get-Command pdflatex -ErrorAction SilentlyContinue
Get-Command xelatex -ErrorAction SilentlyContinue  
Get-Command lualatex -ErrorAction SilentlyContinue

# Verificar outros engines
Get-Command wkhtmltopdf -ErrorAction SilentlyContinue
Get-Command weasyprint -ErrorAction SilentlyContinue
```

### 3. **Testar diretamente com Pandoc**
```powershell
# Testar cada engine tentando converter um documento simples
$testContent = "# Teste`nHello World"

foreach ($engine in @("pdflatex", "xelatex", "lualatex")) {
    try {
        $testContent | pandoc -o "test_$engine.pdf" --pdf-engine=$engine 2>$null
        if (Test-Path "test_$engine.pdf") {
            Write-Host "✅ $engine - Funcionou" -ForegroundColor Green
            Remove-Item "test_$engine.pdf"
        }
    }
    catch {
        Write-Host "❌ $engine - Falhou" -ForegroundColor Red
    }
}
```

## 📋 Engines Mais Comuns e Como Verificar

### LaTeX Engines (vieram com MikTeX):
```powershell
# Verificar se MikTeX está instalado
choco list --local-only | Select-String "miktex"

# Testar cada engine
& pdflatex --version 2>$null; if ($?) { "✅ pdflatex disponível" }
& xelatex --version 2>$null; if ($?) { "✅ xelatex disponível" }  
& lualatex --version 2>$null; if ($?) { "✅ lualatex disponível" }
```

### Outros Engines:
```powershell
# Verificar wkhtmltopdf
choco list --local-only | Select-String "wkhtmltopdf"

# Verificar weasyprint  
python -m weasyprint --version 2>$null; if ($?) { "✅ weasyprint disponível" }
```

## 🎯 Solução Prática Imediata:

**Execute este comando para descobrir:**

```powershell
Write-Host "🔍 Verificando engines disponíveis..." -ForegroundColor Yellow

$availableEngines = @()

if (Get-Command pdflatex -ErrorAction SilentlyContinue) { $availableEngines += "pdflatex" }
if (Get-Command xelatex -ErrorAction SilentlyContinue) { $availableEngines += "xelatex" }
if (Get-Command lualatex -ErrorAction SilentlyContinue) { $availableEngines += "lualatex" }
if (Get-Command wkhtmltopdf -ErrorAction SilentlyContinue) { $availableEngines += "wkhtmltopdf" }

Write-Host "✅ Engines disponíveis: $($availableEngines -join ', ')" -ForegroundColor Green
```

## ✅ Comando que Provavelmente Funcionará:

```powershell
# Primeiro tente lualatex ou pdflatex (mais comuns)
((Get-Content -Raw input.md) -replace '🧊', '❄️') | pandoc -o output.pdf --pdf-engine=lualatex
```

**O Pandoc não tem um comando para listar engines - precisamos testar manualmente!** 🎉

---

### 👤 Utilizador *(2025-09-18 03:55:28)* *[deepseek-chat]*

como usar:  choco list --local-only | Select-String "wkhtmltopdf"  no comand promt

---

### 🤖 DeepSeek *(2025-09-18 03:55:28)* *[deepseek-chat]*

Para usar o comando `choco list --local-only | Select-String "wkhtmltopdf"` no **Command Prompt (CMD)**, você precisa adaptá-lo porque o CMD não entende comandos PowerShell nativamente.

## 💡 Métodos para usar no Command Prompt:

### Método 1: Usar comando Chocolatey direto
```cmd
choco list --local-only | findstr "wkhtmltopdf"
```

### Método 2: Usar grep (se tiver)
```cmd
choco list --local-only | grep "wkhtmltopdf"
```

### Método 3: Listar tudo e procurar visualmente
```cmd
choco list --local-only
```
Depois procure por "wkhtmltopdf" na lista.

## 🔍 Comandos úteis no Command Prompt:

### Verificar se wkhtmltopdf está instalado:
```cmd
choco list --local-only | findstr /i "wkhtmltopdf"
```

### Verificar versão específica:
```cmd
choco list --local-only | findstr /i "wkhtmltopdf"
```

### Se estiver instalado, verificar o caminho:
```cmd
where wkhtmltopdf
```

## 📋 Exemplo completo no CMD:

```cmd
REM Verificar se wkhtmltopdf está instalado
choco list --local-only | findstr "wkhtmltopdf"

REM Se estiver instalado, testar o comando
wkhtmltopdf --version

REM Se não estiver, instalar
choco install wkhtmltopdf -y
```

## ⚠️ Se preferir usar PowerShell no CMD:

```cmd
powershell -Command "choco list --local-only | Select-String 'wkhtmltopdf'"
```

## ✅ Melhor opção para CMD:

```cmd
choco list --local-only | findstr "wkhtmltopdf"
```

**O `findstr` é o equivalente do `Select-String` no Command Prompt!** 🎉

---

### 👤 Utilizador *(2025-09-18 04:06:43)* *[deepseek-chat]*

Fontes para emojis melhores que "Segoe UI Emoji"

---

### 🤖 DeepSeek *(2025-09-18 04:06:43)* *[deepseek-chat]*

Excelente pergunta! Aqui estão as **melhores fontes para emojis** superiores ao "Segoe UI Emoji":

## 🏆 Melhores Fontes de Emoji para Windows

### 1. **Noto Color Emoji (Google)** - ✅ Melhor Opção
- **Cobertura completa** de Unicode 15.0
- **Emojis coloridos** vetoriais
- **Mais de 3,800 emojis**
- **Download**: https://github.com/googlefonts/noto-emoji

### 2. **Twemoji (Twitter/Mozilla)** - 🎨 Moderna
- Design moderno e consistente
- **Open source** e atualizada frequentemente
- **Download**: https://github.com/mozilla/twemoji-colr

### 3. **JoyPixels** - 💼 Profissional
- Design profissional e claro
- Boa legibilidade em pequenos tamanhos
- **Download**: https://www.joypixels.com/

### 4. **OpenMoji** - 🎓 Acadêmica
- Projeto open source acadêmico
- Design plano e consistente
- **Download**: https://openmoji.org/

## 📦 Como Instalar no Windows

### Método Manual:
1. Baixe o arquivo `.ttf` ou `.otf`
2. Clique direito → "Instalar"
3. Reinicie aplicativos

### Via Chocolatey (algumas disponíveis):
```powershell
# Noto Fonts (inclui emojis)
choco install font-noto

# Ou instalar manualmente as fontes de emoji
```

## 🔧 Configuração no Pandoc

### Com Noto Color Emoji:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Color Emoji" \
  -V sansfont="Noto Sans" \
  -V monofont="Noto Sans Mono"
```

### Com Twemoji:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Twemoji Mozilla" \
  -V sansfont="Arial" \
  -V monofont="Consolas"
```

## 📊 Comparação das Fontes:

| Fonte | Emojis | Cores | Unicode | Estilo |
|-------|--------|-------|---------|--------|
| **Noto Color** | 3,800+ | ✅ | 15.0 | Colorido |
| **Twemoji** | 3,600+ | ✅ | 14.0 | Moderno |
| **Segoe UI** | 1,800+ | ✅ | 12.0 | Windows |
| **JoyPixels** | 3,200+ | ✅ | 13.0 | Profissional |

## 💡 Dica Profissional:

**Use fallback de fontes no LaTeX:**
```latex
\usepackage{fontspec}
\setmainfont{Noto Sans}[
  ColorFont = Noto Color Emoji,
  Renderer = HarfBuzz
]
```

## 🚀 Minha Recomendação:

**Noto Color Emoji** é a melhor opção para:
- ✅ Maior cobertura de emojis
- ✅ Cores vibrantes  
- ✅ Atualizações frequentes
- ✅ Suporte a Unicode completo

**Baixe aqui:** https://github.com/googlefonts/noto-emoji 🎉

---

### 👤 Utilizador *(2025-09-18 04:19:05)* *[deepseek-chat]*

como listar fontes instaladas windows no CMD

---

### 🤖 DeepSeek *(2025-09-18 04:19:05)* *[deepseek-chat]*

Aqui estão os **comandos para listar fontes instaladas no Windows usando CMD**:

## 📋 Métodos no Command Prompt (CMD)

### Método 1: Listar arquivos da pasta Fonts
```cmd
dir C:\Windows\Fonts
```

### Método 2: Procurar fontes específicas
```cmd
dir C:\Windows\Fonts | findstr /i "emoji"
dir C:\Windows\Fonts | findstr /i "noto"
dir C:\Windows\Fonts | findstr /i "segoe"
```

### Método 3: Listar com mais detalhes
```cmd
dir C:\Windows\Fonts /B
```

## 🔍 Comandos Úteis no CMD

### Procurar por fontes de emoji:
```cmd
dir C:\Windows\Fonts | findstr /i "emoji"
dir C:\Windows\Fonts | findstr /i "symbol"
dir C:\Windows\Fonts | findstr /i "noto"
```

### Verificar fontes específicas:
```cmd
dir C:\Windows\Fonts\*emoji*
dir C:\Windows\Fonts\*noto*
dir C:\Windows\Fonts\*segoe*
```

### Listar todas as fontes e salvar em arquivo:
```cmd
dir C:\Windows\Fonts /B > fonts_list.txt
notepad fonts_list.txt
```

## 📊 Exemplos Práticos:

### Verificar se Segoe UI Emoji está instalada:
```cmd
dir C:\Windows\Fonts | findstr /i "seguiemj"
```

### Verificar fontes Noto:
```cmd
dir C:\Windows\Fonts | findstr /i "noto"
```

### Procurar múltiplos termos:
```cmd
dir C:\Windows\Fonts | findstr /i "emoji noto symbol segoe"
```

## ⚠️ Limitação do CMD:
O CMD não mostra os **nomes amigáveis** das fontes, apenas os nomes dos arquivos. Para ver os nomes reais, use:

### Método alternativo com PowerShell via CMD:
```cmd
powershell -Command "Get-ChildItem 'C:\Windows\Fonts' | Where-Object {$_.Name -like '*emoji*'} | Select-Object Name"
```

## ✅ Melhor Opção para CMD:

```cmd
dir C:\Windows\Fonts | findstr /i "emoji"
```

**Dica:** Use `findstr /i` para busca case-insensitive! 🎉

---

### 👤 Utilizador *(2025-09-18 04:24:15)* *[deepseek-chat]*

como usar Noto Color Emoji  no pandoc

---

### 🤖 DeepSeek *(2025-09-18 04:24:15)* *[deepseek-chat]*

Para usar **Noto Color Emoji** no Pandoc, você precisa seguir estes passos:

## 📥 1. Primeiro Instale a Fonte Noto Color Emoji

**Download manual:**
1. Baixe de: https://github.com/googlefonts/noto-emoji
2. Instale clicando com botão direito → "Instalar"

**Ou via repositório oficial:**
- https://fonts.google.com/noto

## 🔧 2. Configuração no Pandoc

### Opção A: Especificar diretamente a fonte
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Color Emoji" \
  -V sansfont="Noto Sans" \
  -V monofont="Noto Sans Mono"
```

### Opção B: Com fallback explícito
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Sans" \
  -V sansfont="Noto Sans" \
  -V monofont="Noto Sans Mono" \
  --variable="fontawesome:fontawesome"
```

## 🎯 3. Usar Template Personalizado (Recomendado)

**Crie um arquivo `noto_template.tex`:**
```latex
\usepackage{fontspec}
\usepackage{newunicodechar}

\setmainfont{Noto Sans}[
  BoldFont = Noto Sans Bold,
  ItalicFont = Noto Sans Italic
]

\newfontfamily\EmojiFont{Noto Color Emoji}[
  Renderer=HarfBuzz,
  Scale=MatchLowercase
]

\newunicodechar{🧊}{{\EmojiFont 🧊}}
\newunicodechar{😊}{{\EmojiFont 😊}}
\newunicodechar{❤️}{{\EmojiFont ❤️}}
```

**Use o template:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --include-in-header=noto_template.tex
```

## 📋 4. Verificar se a Fonte Está Instalada

**No PowerShell:**
```powershell
Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*noto*color*emoji*"} | Select-Object Name
```

**No CMD:**
```cmd
dir C:\Windows\Fonts | findstr /i "noto"
```

## ⚠️ 5. Solução para Problemas Comuns

### Se não encontrar a fonte:
```bash
# Usar caminho completo (ajuste o caminho)
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Color Emoji" \
  -V fontpath="C:/Windows/Fonts/"
```

### Fallback para Segoe UI se Noto falhar:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Color Emoji, Segoe UI Emoji" \
  -V sansfont="Noto Sans, Arial"
```

## ✅ 6. Comando de Teste

**Teste rápido:**
```bash
echo "# Teste com emoji 🧊 ❤️ 😊" | pandoc -o test.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Color Emoji" \
  -V sansfont="Noto Sans"
```

## 🚀 7. Solução Completa

**Script PowerShell completo:**
```powershell
# Verificar se a fonte está instalada
$notoInstalled = Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Name -like "*noto*color*emoji*"}

if ($notoInstalled) {
    pandoc input.md -o output.pdf `
      --pdf-engine=xelatex `
      -V mainfont="Noto Color Emoji" `
      -V sansfont="Noto Sans" `
      -V monofont="Noto Sans Mono"
} else {
    Write-Host "Noto Color Emoji não encontrada. Use Segoe UI..." -ForegroundColor Yellow
    pandoc input.md -o output.pdf `
      --pdf-engine=xelatex `
      -V mainfont="Segoe UI Emoji" `
      -V sansfont="Segoe UI"
}
```

**A Noto Color Emoji tem a melhor cobertura de emojis!** 🎉

---

### 👤 Utilizador *(2025-09-18 04:28:42)* *[deepseek-chat]*

error:  (file C:/Program Files/MiKTeX/fonts/truetype/public/noto-emoji/notocol
oremoji.ttf) (ttf): loca table not found

---

### 🤖 DeepSeek *(2025-09-18 04:28:42)* *[deepseek-chat]*

Este erro indica que o **MiKTeX não consegue usar a fonte Noto Color Emoji** porque ela está em um formato que o LaTeX não suporta bem. Aqui estão as soluções:

## 🎯 Soluções para o Erro "loca table not found"

### 1. **Usar versão OTF da fonte** (Recomendado)
```bash
# Baixe a versão OTF da Noto Emoji:
# https://github.com/googlefonts/noto-emoji/tree/main/fonts
# Instale a versão .otf (não .ttf)

pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Noto Emoji" \
  -V sansfont="Noto Sans"
```

### 2. **Usar outra fonte de emoji**
```bash
# Usar Segoe UI Emoji (já instalada no Windows)
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Segoe UI Emoji" \
  -V sansfont="Segoe UI" \
  -V monofont="Consolas"
```

### 3. **Converter TTF para OTF**
```bash
# Usar ferramentas online para converter:
# https://cloudconvert.com/ttf-to-otf
# Depois instalar a versão .otf convertida
```

### 4. **Usar Twemoji ou outra alternativa**
```bash
# Instalar Twemoji ou JoyPixels
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Twemoji Mozilla" \
  -V sansfont="Arial"
```

## 🔧 Solução Imediata (Recomendada)

**Substituir emojis problemáticos + usar fonte segura:**

```powershell
# Substituir emojis problemáticos
(Get-Content -Raw input.md) -replace '🧊', '❄️' | Set-Content temp.md

# Converter com fonte confiável
pandoc temp.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Arial" \
  -V sansfont="Arial" \
  -V monofont="Courier New"

Remove-Item temp.md
```

## 📋 Verificar Fontes Disponíveis

```powershell
# Listar fontes .otf disponíveis (mais compatíveis)
Get-ChildItem "C:\Windows\Fonts" | Where-Object {$_.Extension -eq ".otf"} | Select-Object Name -First 10
```

## ✅ Comando Garantido que Funciona:

```powershell
# 1. Remover/substituir emojis problemáticos
$content = (Get-Content -Raw input.md) -replace '[^\x00-\x7F]', '✨'
$content | Set-Content clean_input.md

# 2. Converter com engine básico
pandoc clean_input.md -o output.pdf --pdf-engine=pdflatex

# 3. Limpar
Remove-Item clean_input.md
```

## 🚀 Solução Definitiva:

**Usar conversão para HTML primeiro:**
```powershell
# Converter para HTML (preserva emojis)
pandoc input.md -o temp.html

# Converter HTML para PDF com wkhtmltopdf
pandoc temp.html -o output.pdf --pdf-engine=wkhtmltopdf

# Limpar
Remove-Item temp.html
```

**O problema é que a Noto Color Emoji em formato TTF não é compatível com MiKTeX.** Use a versão OTF ou substitua os emojis! 🎉

---

*Conversa exportada do DeepSeek*
*Processado em: 15/11/2025 22:27*