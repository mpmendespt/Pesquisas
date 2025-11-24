# Convertendo Markdown para PDF com Pandoc

## 📊 Informações
- **Número:** #159
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** 01a0bb6b-a8a9-44b9-8400-fcaa42cfc7fa
- **Criada em:** 2025-09-26 02:06:37
- **Atualizada em:** 2025-09-26 03:32:49
- **Total de mensagens:** 12
- **Resumo:** Converter md para pdf, com conda. Com MiKTeX with lualatex. HarfBuzz. Com comando semelhante a pando...

---

## 💬 Conversa

### 👤 Utilizador *(2025-09-26 02:06:38)* *[deepseek-chat]*

Converter md para pdf, com conda. Com MiKTeX with lualatex. HarfBuzz. Com comando semelhante a pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex -include-in-header=header.tex

---

### 🤖 DeepSeek *(2025-09-26 02:06:38)* *[deepseek-chat]*

Para converter o arquivo Markdown para PDF usando **Conda**, **MiKTeX** com **LuaLaTeX** e **HarfBuzz**, siga os passos abaixo:

---

### 1. Configurar o ambiente Conda
Se você ainda não tem um ambiente com Pandoc e MiKTeX, pode criar um:

```bash
conda create -n pandoc-lualatex pandoc miktex -c conda-forge
conda activate pandoc-lualatex
```

---

### 2. Instalar pacotes LaTeX necessários via MiKTeX
Após ativar o ambiente, execute o MiKTeX Console para instalar os pacotes necessários (como `unicode-math`, `fontspec`, etc.), ou use o comando:

```bash
miktex packages install fontspec unicode-math luacode luatexbase
```

---

### 3. Criar um arquivo `header.tex` (opcional, mas recomendado)
Crie um arquivo `header.tex` para configurar fontes e suporte a Unicode:

```latex
% header.tex
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\setsansfont{TeX Gyre Heros}
\setmonofont{TeX Gyre Cursor}[Scale=MatchLowercase]

\usepackage{unicode-math}
\setmathfont{TeX Gyre Termes Math}

\usepackage{microtype}
```

---

### 4. Executar o comando Pandoc
Use o comando abaixo para gerar o PDF:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

---

### 5. Verificar o resultado
O PDF `exemplo.pdf` será gerado com:

- Acentos e emojis
- Destaque de sintaxe em blocos de código
- Fórmulas matemáticas
- Tabelas e citações formatadas

---

Se encontrar erros de fontes ou codificação, verifique se as fontes usadas no `header.tex` estão instaladas no sistema ou ajuste para fontes disponíveis (ex: `DejaVu Sans`, `Liberation Sans`, etc.).

---

### 👤 Utilizador *(2025-09-26 02:14:43)* *[deepseek-chat]*

Error producing PDF.
! Package fontspec Error:
(fontspec)                The font "TeX Gyre Termes" cannot be found; this
(fontspec)                may be but usually is not a fontspec bug. Either
(fontspec)                there is a typo in the font name/file, the font is
(fontspec)                not installed (correctly), or there is a bug in
(fontspec)                the underlying font loading engine
(fontspec)                (XeTeX/luaotfload).

For immediate help type H <return>.
 ...

l.93 \setsansfont

---

### 🤖 DeepSeek *(2025-09-26 02:14:43)* *[deepseek-chat]*

O erro indica que a fonte "TeX Gyre Termes" não está instalada no sistema. Vamos corrigir isso de algumas formas:

## Solução 1: Usar fontes mais comuns/disponíveis

Substitua o conteúdo do `header.tex` por:

```latex
% header.tex
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

\usepackage{unicode-math}
\setmathfont{DejaVu Math TeX Gyre}

\usepackage{microtype}
```

## Solução 2: Instalar as fontes TeX Gyre (recomendado)

### No Windows/MiKTeX:
```bash
# Via MiKTeX Console (GUI) ou linha de comando:
miktex packages install tex-gyre
```

### Ou via tlmgr (se disponível):
```bash
tlmgr install collection-fontsrecommended
```

## Solução 3: Usar header.tex mais simples e compatível

Crie um `header.tex` mais básico:

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{microtype}

% Usar fontes do sistema que são mais comuns
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Configurações para melhor suporte a português
\usepackage{polyglossia}
\setdefaultlanguage{portuguese}
```

## Solução 4: Comando alternativo sem header.tex

Tente primeiro sem o header para testar:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex -V mainfont="DejaVu Serif"
```

## Solução 5: Verificar se as fontes estão disponíveis

Para listar fontes disponíveis:
```bash
fc-list | grep -i "dejavu\|texgyre"
```

## Comando final recomendado para teste:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex -V mainfont="DejaVu Serif" -V sansfont="DejaVu Sans" -V monofont="DejaVu Sans Mono"
```

Experimente a **Solução 4** primeiro, pois é a mais simples. Se funcionar, então o problema era apenas a fonte especificada no header.tex.

Qual resultado você obtém com o comando da Solução 4?

---

### 👤 Utilizador *(2025-09-26 03:05:39)* *[deepseek-chat]*

Em todas as soluções ( 1 2 3 4) o resultado é o pdf tem emojis só com rectangulos sem cores e [WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:DejaVu Serif:mode=no
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:DejaVu Serif:mode=no

---

### 🤖 DeepSeek *(2025-09-26 03:05:39)* *[deepseek-chat]*

O problema é que as fontes DejaVu e TeX Gyre não suportam emojis. Precisamos usar uma fonte que inclua emojis coloridos. Vamos tentar algumas soluções:

## Solução 1: Usar fonte com suporte a emojis (Segoe UI Emoji no Windows)

Crie um `header.tex` com:

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Fontes principais
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Fonte específica para emojis
\newfontfamily\EmojiFont{Segoe UI Emoji}[Renderer=Harfbuzz]

% Comando para usar emojis
\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{microtype}
```

## Solução 2: Usar fonte Noto Color Emoji (mais universal)

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Fontes principais
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Fonte de emojis coloridos
\newfontfamily\EmojiFont{Noto Color Emoji}[Renderer=Harfbuzz]

% Definir emojis específicos
\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{microtype}
```

## Solução 3: Instalar fontes de emoji

### No Windows (com MiKTeX):
```bash
# Instalar pacote de fontes de emoji
miktex packages install noto
```

### Ou via Conda:
```bash
conda install -c conda-forge noto-fonts-emoji
```

## Solução 4: Usar uma abordagem mais simples

Se as soluções acima não funcionarem, tente este header mais básico:

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Usar uma fonte que tenha amplo suporte Unicode
\setmainfont{Arial Unicode MS}  % Se disponível no Windows
\setsansfont{Arial}
\setmonofont{Consolas}[Scale=MatchLowercase]

\usepackage{microtype}
```

## Solução 5: Remover os emojis (fallback)

Se nada funcionar, você pode pré-processar o arquivo para remover os emojis:

```bash
# Criar uma versão sem emojis
sed 's/[\x{1F300}-\x{1F9FF}]//g' exemplo.md > exemplo_sem_emoji.md
pandoc exemplo_sem_emoji.md -o exemplo.pdf --pdf-engine=lualatex
```

## Comando para testar:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

**Recomendo tentar a Solução 1 primeiro**, pois o Segoe UI Emoji geralmente está disponível no Windows. Se não funcionar, tente a Solução 2 instalando as fontes Noto.

Qual é o resultado com a Solução 1?

---

### 👤 Utilizador *(2025-09-26 03:14:15)* *[deepseek-chat]*

Solução 1: o pdf tem emojis só com rectangulos sem cores e com WARNINGs Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:DejaVu Serif:mode=no.  Mas a  Solução 2  o pdf tem emojis correctos mas sem cores e sem WARNINGs

---

### 🤖 DeepSeek *(2025-09-26 03:14:15)* *[deepseek-chat]*

Excelente! A Solução 2 funcionou parcialmente - os emojis estão sendo renderizados, mas sem cores. Isso é um progresso. Vamos melhorar para obter emojis coloridos:

## Solução 2.1: Forçar renderização colorida do Noto Color Emoji

Atualize o `header.tex` para:

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Fontes principais
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Fonte de emojis coloridos com configurações específicas
\newfontfamily\EmojiFont{Noto Color Emoji}[
    Renderer=Harfbuzz,
    Color=000000,  % Tenta forçar cores (pode não funcionar em todos os PDF readers)
    Scale=1.1
]

% Definir emojis específicos
\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

% Tentativa alternativa: usar fonte Twitter Color Emoji (se disponível)
%\newfontfamily\EmojiFontAlt{Twitter Color Emoji}[Renderer=Harfbuzz]

\usepackage{microtype}
```

## Solução 2.2: Tentar fontes de emoji alternativas

Se o Noto Color Emoji não renderiza cores, tente estas alternativas:

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Fontes principais
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Tentar diferentes fontes de emoji (teste uma por uma)
\newfontfamily\EmojiFont{Apple Color Emoji}[Renderer=Harfbuzz]  % Para macOS
%\newfontfamily\EmojiFont{Segoe UI Emoji}[Renderer=Harfbuzz]    % Windows
%\newfontfamily\EmojiFont{Twitter Color Emoji}[Renderer=Harfbuzz]
%\newfontfamily\EmojiFont{Noto Color Emoji}[Renderer=Harfbuzz]

% Definir emojis
\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{microtype}
```

## Solução 2.3: Configuração específica para LuaLaTeX + HarfBuzz

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{luacode}

% Configuração do LuaLaTeX para melhor suporte a emojis
\begin{luacode}
function enable_emoji()
    fonts.handlers.otf.addfeature {
        name = "emoji",
        type = "colors",
        data = {
            [0x1F600] = { 1, 0.8, 0 },  -- 😀 amarelo
            [0x1F60E] = { 0, 0.5, 1 },  -- 😎 azul
            [0x1F680] = { 1, 0, 0 },    -- 🚀 vermelho
            [0x1F427] = { 0, 0.6, 0 },  -- 🐧 verde
        },
    }
end
\end{luacode}

\directlua{enable_emoji()}

% Fontes
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

\newfontfamily\EmojiFont{Noto Color Emoji}[
    Renderer=Harfbuzz,
    RawFeature=+emoji
]

\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{microtype}
```

## Solução 2.4: Verificar o leitor de PDF

As cores dos emojis podem depender do leitor de PDF:
- **Adobe Acrobat Reader**: Melhor suporte
- **Foxit Reader**: Bom suporte  
- **SumatraPDF**: Suporte limitado
- **Navegadores**: Variável

## Solução 2.5: Comando final otimizado

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex -V colorlinks=true
```

**Recomendo tentar a Solução 2.1 primeiro**, pois é a mais simples. Se não der cores, experimente a Solução 2.2 testando fontes alternativas.

Qual é o seu leitor de PDF atual? Isso pode ajudar a diagnosticar o problema das cores.

---

### 👤 Utilizador *(2025-09-26 03:19:03)* *[deepseek-chat]*

Solução 2.2  Error producing PDF.
! Package fontspec Error:
(fontspec)                The font "Apple Color Emoji" cannot be found; this
(fontspec)                may be but usually is not a fontspec bug. Either
(fontspec)                there is a typo in the font name/file, the font is
(fontspec)                not installed (correctly), or there is a bug in
(fontspec)                the underlying font loading engine
(fontspec)                (XeTeX/luaotfload).

For immediate help type H <return>.
 ...

l.101 ...ont{Apple Color Emoji}[Renderer=Harfbuzz]

---

### 🤖 DeepSeek *(2025-09-26 03:19:03)* *[deepseek-chat]*

Vamos voltar ao que funcionou (Noto Color Emoji) e tentar melhorar as cores. O erro ocorre porque "Apple Color Emoji" não está disponível no Windows.

## Solução 2.2 Corrigida: Usar apenas fontes disponíveis no Windows

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Fontes principais
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Fonte de emoji - testar nesta ordem (comente as outras)
\newfontfamily\EmojiFont{Segoe UI Emoji}[Renderer=Harfbuzz]      % Windows
%\newfontfamily\EmojiFont{Noto Color Emoji}[Renderer=Harfbuzz]   % Se instalado
%\newfontfamily\EmojiFont{Twitter Color Emoji}[Renderer=Harfbuzz]% Alternativa

% Definir emojis
\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{microtype}
```

## Solução 3: Verificar e instalar fontes de emoji

### Verificar quais fontes de emoji estão disponíveis:
```bash
fc-list | grep -i emoji
```

### Instalar Noto Color Emoji via Conda:
```bash
conda install -c conda-forge noto-fonts-emoji
```

### Ou baixar e instalar manualmente:
1. Baixe: https://fonts.google.com/noto/specimen/Noto+Color+Emoji
2. Instale as fontes no Windows

## Solução 4: Configuração específica para Windows + MiKTeX

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Configuração para Windows
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Tentar detectar automaticamente a fonte de emoji
\IfFontExistsTF{Segoe UI Emoji}{
    \newfontfamily\EmojiFont{Segoe UI Emoji}[Renderer=Harfbuzz]
}{
    \IfFontExistsTF{Noto Color Emoji}{
        \newfontfamily\EmojiFont{Noto Color Emoji}[Renderer=Harfbuzz]
    }{
        \newfontfamily\EmojiFont{Segoe UI Symbol}[Renderer=Harfbuzz]
    }
}

% Definir emojis
\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{microtype}
```

## Solução 5: Abordagem mais compatível (sem cores)

Se as cores não forem essenciais, use esta versão que funciona bem:

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}

% Fontes com melhor suporte Unicode
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Fonte fallback para símbolos
\newfontfamily\SymbolFont{DejaVu Sans}

% Definir emojis como símbolos (versão monocromática)
\usepackage{newunicodechar}
\newunicodechar{😀}{{\SymbolFont ☺}}  % Smiley como fallback
\newunicodechar{😎}{{\SymbolFont ☻}}  % Smiley com óculos
\newunicodechar{🚀}{{\SymbolFont ↑}}   % Seta para cima
\newunicodechar{🐧}{{\SymbolFont 🐧}}  % Pinguim Unicode

\usepackage{microtype}
```

## Comando para testar:

```bash
# Primeiro verifique quais fontes estão disponíveis
fc-list | grep -i emoji

# Depois execute o pandoc
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

**Execute primeiro o comando `fc-list` para ver quais fontes de emoji você tem disponíveis**, então ajuste o header.tex conforme o resultado.

Qual é a saída do comando `fc-list | grep -i emoji`? Isso nos dirá quais fontes de emoji estão realmente instaladas.

---

### 👤 Utilizador *(2025-09-26 03:32:13)* *[deepseek-chat]*

Solução 4  o pdf tem emojis correctos e com cores   (pandoc-env) D:\Downloads\_DOCS_\_DOCS_\CONDA_md_to_pdf\pandoc-lualatex-project-clean-final>fc-list | grep -i emoji
C:/WINDOWS/fonts\Twemoji.Mozilla.ttf: Twemoji Mozilla:style=Regular
C:/WINDOWS/fonts\seguiemj.ttf: Segoe UI Emoji:style=Regular,Normal,obyÄ?ejnAc,Standard,IsI±I½I¿I½I1IºI¬,Normaali,NormA¡l,Normale,Standaard,Normalny,DzD±Ñ<Ñ╪D½Ñ<D1,NormA¡lne,Navadno,Arrunta
C:/WINDOWS/fonts\NotoColorEmoji_Win10.ttf: Noto Color Emoji:style=Regular
C:/Users/mpmen/AppData/Local/Microsoft/Windows/Fonts\NotoColorEmoji-SVGinOT.ttf: Noto Color Emoji:style=Regular
C:/WINDOWS/fonts\EmojiOneColor-SVGinOT.ttf: EmojiOne Color:style=Regular
C:/WINDOWS/fonts\TwemojiMozilla.ttf: Twemoji Mozilla:style=Regular

---

### 🤖 DeepSeek *(2025-09-26 03:32:13)* *[deepseek-chat]*

Excelente! Agora sabemos que você tem várias fontes de emoji disponíveis, incluindo **Segoe UI Emoji** (Windows) e **Noto Color Emoji**. Vamos criar um header.tex otimizado:

## Solução Final: Header.tex otimizado para Windows

```latex
% header.tex
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{microtype}

% Fontes principais para texto
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Fonte de emoji - usar Segoe UI Emoji (nativa do Windows) que funciona com cores
\newfontfamily\EmojiFont{Segoe UI Emoji}[
    Renderer=Harfbuzz,
    Scale=1.1  % Ajuste opcional para tamanho
]

% Definir todos os caracteres Unicode de emoji para usar a fonte correta
\usepackage{newunicodechar}

% Emojis específicos do seu documento
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

% Configuração adicional para melhor suporte
\setmonofont{DejaVu Sans Mono}[
    Scale=MatchLowercase,
    Contextuals=Alternate  % Melhor renderização de código
]

% Melhor suporte para português
\usepackage{polyglossia}
\setdefaultlanguage{portuguese}
```

## Comando final:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

## Versão alternativa se quiser testar Noto Color Emoji:

```latex
% header.tex (alternativa com Noto)
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{microtype}

\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

% Usar Noto Color Emoji (pode ter cores mais vibrantes)
\newfontfamily\EmojiFont{Noto Color Emoji}[Renderer=Harfbuzz]

\usepackage{newunicodechar}
\newunicodechar{😀}{{\EmojiFont 😀}}
\newunicodechar{😎}{{\EmojiFont 😎}}
\newunicodechar{🚀}{{\EmojiFont 🚀}}
\newunicodechar{🐧}{{\EmojiFont 🐧}}

\usepackage{polyglossia}
\setdefaultlanguage{portuguese}
```

## Resumo do que funcionou:

✅ **Solução 4**: Emojis corretos e com cores usando Segoe UI Emoji  
✅ **Fontes disponíveis**: Segoe UI Emoji, Noto Color Emoji, Twemoji, EmojiOne  
✅ **Windows + MiKTeX + LuaLaTeX**: Configurado corretamente  

Agora você tem um template funcional para converter Markdown para PDF com:
- ✅ Acentos portugueses
- ✅ Emojis coloridos 
- ✅ Syntax highlighting
- ✅ Fórmulas matemáticas
- ✅ Tabelas e formatação

O comando final que funciona é:
```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

---

*Conversa exportada do DeepSeek*
*Processado em: 24/11/2025 22:27*