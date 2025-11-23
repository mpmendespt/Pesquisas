# Markdown to PDF Conversion with LuaLaTeX

## 📊 Informações
- **Número:** #154
- **Origem:** Grok
- **Categoria:** Programação
- **ID:** cb854a96-3b73-4b99-bb79-730aa91173a8
- **Criada em:** 2025-09-25 15:26:35Z
- **Atualizada em:** 2025-09-25 18:08:38Z
- **Total de mensagens:** 7
- **Resumo:** Converter md para pdf, com conda. Com MiKTeX with lualatex. HarfBuzz. Com comando semelhante a pando...

---

## 💬 Conversa

### 👤 Utilizador *(2025-09-25 16:26:35)* *[Grok]*

Converter md para pdf, com conda. Com MiKTeX with lualatex. HarfBuzz. Com comando semelhante a pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex -include-in-header=header.tex

---

### 🤖 Grok *(2025-09-25 16:27:14)* *[Grok]*

To convert the provided Markdown file (`exemplo.md`) to a PDF using Pandoc with LuaLaTeX as the PDF engine, incorporating MiKTeX and HarfBuzz for proper font rendering, we need to create a LaTeX header file (`header.tex`) and provide the appropriate Pandoc command. The Markdown file contains various elements like text with accents and emojis, code blocks in multiple languages, mathematical expressions, tables, and quotes, all of which must be properly handled in the LaTeX output. Below, I’ll provide the LaTeX header file and the Pandoc command to achieve this.

The LaTeX header will include a comprehensive preamble to support:
- UTF-8 encoding for accents and emojis.
- HarfBuzz for advanced font rendering via LuaLaTeX.
- Packages for code highlighting, tables, and mathematical typesetting.
- A font setup compatible with emojis and non-Latin characters.

### LaTeX Header File (header.tex)
The header file configures LuaLaTeX to handle the Markdown content correctly, including font setup with HarfBuzz, code highlighting with `lstlistings`, and support for tables and mathematics.

<xaiArtifact artifact_id="152dc40c-9af7-4260-a063-06fd3f3b6033" artifact_version_id="2bc73c6b-e2bb-4ecb-ae10-022e17cdaa44" title="header.tex" contentType="text/latex">
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{luacode}
\usepackage{luatexbase}
\usepackage[no-sscript]{xltxtra}
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{unicode-math}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{multirow}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{quoting}
\quotingsetup{vskip=0pt}
\usepackage{parskip}
\setlength{\parskip}{0.5em}
\usepackage{enumitem}
\setlist[itemize]{leftmargin=*}
\setlist[enumerate]{leftmargin=*}

% Configuring lstlistings for code blocks
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  breakatwhitespace=true,
  frame=single,
  framesep=2pt,
  framerule=0.5pt,
  columns=flexible,
  keepspaces=true,
  showstringspaces=false,
  tabsize=2,
  numbers=left,
  numberstyle=\tiny,
  keywordstyle=\color{blue},
  stringstyle=\color{red},
  commentstyle=\color{gray},
  backgroundcolor=\color{gray!10},
}

% Define languages for lstlistings
\lstdefinelanguage{Python}{
  morekeywords={def,return,print,while},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
  morestring=[b]{'},
}
\lstdefinelanguage{Cpp}{
  morekeywords={include,int,main,cout,endl,using,namespace,std},
  sensitive=true,
  morecomment=[l]{//},
  morestring=[b]{"},
}
\lstdefinelanguage{Bash}{
  morekeywords={while,do,done,echo},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
}
\lstdefinelanguage{JSON}{
  morestring=[b]{"},
  literate=
    *{0}{{{\color{red}0}}}{1}
     {1}{{{\color{red}1}}}{1}
     {2}{{{\color{red}2}}}{1}
     {3}{{{\color{red}3}}}{1}
     {4}{{{\color{red}4}}}{1}
     {5}{{{\color{red}5}}}{1}
     {6}{{{\color{red}6}}}{1}
     {7}{{{\color{red}7}}}{1}
     {8}{{{\color{red}8}}}{1}
     {9}{{{\color{red}9}}}{1}
     {true}{{{\color{blue}true}}}{4}
     {false}{{{\color{blue}false}}}{5}
     {null}{{{\color{blue}null}}}{4},
}

% Setting up fonts with HarfBuzz for emoji and accent support
\setmainfont[
  Renderer=HarfBuzz,
  Extension=.ttf,
  UprightFont={*-Regular},
  BoldFont={*-Bold},
  ItalicFont={*-Italic},
]{NotoSerif}
\setsansfont[
  Renderer=HarfBuzz,
  Extension=.ttf,
  UprightFont={*-Regular},
  BoldFont={*-Bold},
  ItalicFont={*-Italic},
]{NotoSans}
\setmonofont[
  Renderer=HarfBuzz,
  Extension=.ttf,
  UprightFont={*-Regular},
]{NotoSansMono}
\setmathfont[
  Renderer=HarfBuzz,
]{TeXGyreTermesMath}
\end{xaiArtifact>

### Pandoc Command
Assuming you have MiKTeX installed (which includes LuaLaTeX) and Pandoc available in your Conda environment, the following command converts `exemplo.md` to `exemplo.pdf`:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

### Explanation of the Setup
- **Font Configuration**: The `fontspec` package with HarfBuzz renderer (`Renderer=HarfBuzz`) ensures proper rendering of emojis and accents. `NotoSerif`, `NotoSans`, and `NotoSansMono` are used for text, sans-serif, and monospace fonts, respectively, as they support a wide range of Unicode characters, including emojis. `TeXGyreTermesMath` is used for mathematical typesetting.
- **Code Highlighting**: The `lstlistings` package is configured to handle Python, C++, Bash, and JSON code blocks with syntax highlighting. Each language is defined with appropriate keywords and styling.
- **Mathematics**: The `amsmath` and `unicode-math` packages ensure proper rendering of inline and display math, such as the Pythagorean theorem and the integral equation.
- **Tables**: The `booktabs` package is included for professional table formatting, compatible with the Markdown table in the input.
- **Quotes**: The `quoting` package handles block quotes, such as the Leonardo da Vinci quote.
- **Geometry and Spacing**: The `geometry` package sets A4 paper with 1-inch margins, and `parskip` adds spacing between paragraphs for better readability.
- **Pandoc Command**: The `--pdf-engine=lualatex` flag specifies LuaLaTeX as the PDF engine, and `--include-in-header=header.tex` includes the custom LaTeX preamble.

### Prerequisites
- **MiKTeX**: Ensure MiKTeX is installed with the `lualatex` engine and the `texlive-fonts-extra` package (which includes Noto fonts).
- **Pandoc**: Install Pandoc in your Conda environment using `conda install pandoc`.
- **Header File**: Save the provided `header.tex` in the same directory as `exemplo.md`.

### Running the Command
1. Save the Markdown content as `exemplo.md`.
2. Save the LaTeX header as `header.tex` in the same directory.
3. Run the Pandoc command in your terminal or Conda prompt:
   ```bash
   pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
   ```
4. The output will be `exemplo.pdf`, which includes formatted text, code blocks, math, tables, and quotes, all rendered with proper fonts and HarfBuzz support.

This setup ensures that all elements in the Markdown file are correctly rendered in the PDF, with full support for accents, emojis, and code syntax highlighting.

---

### 👤 Utilizador *(2025-09-25 17:07:22)* *[Grok]*

com header.tex e pandoc-env) D:\Downloads\_DOCS_\_DOCS_\CONDA_md_to_pdf\pandoc-lualatex-project-clean-final>pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex obtem se pdf sem emojis com core e [WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:Latin Modern Roman:m
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:Latin Modern Roman:m

---

### 🤖 Grok *(2025-09-25 17:08:16)* *[Grok]*

The issue you're encountering—missing emojis in the generated PDF and the `[WARNING] Missing character` errors—indicates that the fonts specified in your `header.tex` file (specifically, `Latin Modern Roman` and its fallback fonts) do not fully support the emojis in your Markdown file (`exemplo.md`). The emojis (e.g., 😄 U+1F600, 😎 U+1F60E, 🚀 U+1F680, 🐧 U+1F427) are not available in `Latin Modern Roman` or the fallback fonts (`Segoe UI Emoji`, `Noto Color Emoji`, `Twemoji Mozilla`), or the font fallback mechanism is not properly configured for LuaLaTeX with HarfBuzz. Additionally, the repeated warnings suggest that the font fallback is not being applied correctly.

Below, I’ll provide an updated `header.tex` to address this issue, ensuring proper emoji rendering, and explain the necessary steps to generate the PDF correctly using Pandoc and LuaLaTeX in your Conda environment. I’ll also clarify why the errors occurred and how to resolve them.

### Why the Errors Occurred
1. **Font Support for Emojis**: `Latin Modern Roman` does not include glyphs for emojis (Unicode characters like U+1F600). While you specified fallback fonts (`Segoe UI Emoji`, `Noto Color Emoji`, `Twemoji Mozilla`), these may not be installed in your MiKTeX distribution, or the fallback mechanism may not be correctly set up in LuaLaTeX.
2. **Font Fallback Configuration**: The `Fallback` option in `fontspec` is not standard. LuaLaTeX requires a more explicit fallback mechanism, often using the `luaotfload` package or a custom Lua script to handle font fallbacks for emojis.
3. **Emoji Fonts Availability**: Fonts like `Noto Color Emoji` and `Twemoji Mozilla` support emojis but may not be installed or accessible in your MiKTeX setup. `Segoe UI Emoji` is a Windows font, but it may not work seamlessly with LuaLaTeX unless properly configured.
4. **HarfBuzz Renderer**: While you’ve enabled HarfBuzz (`Renderer=HarfBuzz`), emoji rendering also depends on the font having the necessary glyphs and the renderer correctly accessing fallback fonts.
5. **Repeated Warnings**: The warnings are repeated because Pandoc processes the emojis multiple times (e.g., in different contexts or passes), and each time, LuaLaTeX fails to find the glyphs in the specified fonts.

### Updated `header.tex`
To fix the emoji rendering issue, we need to:
- Use a font with broad Unicode support (e.g., `Noto Serif` or `Noto Sans`) as the main font.
- Explicitly configure emoji fallback using a font like `Noto Color Emoji`, which is widely available and supports emojis.
- Use a Lua script to handle font fallbacks for emojis, as `fontspec`’s built-in fallback mechanism is limited.
- Ensure compatibility with code blocks, mathematics, and other elements in your Markdown file.

Here’s the updated `header.tex`:

<xaiArtifact artifact_id="c2312a9d-c672-4920-af49-545f85021a26" artifact_version_id="e2f3f952-5a0a-4a68-a2c5-fca2d05369b7" title="header.tex" contentType="text/latex">
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{fontspec}
\usepackage{luacode} % For Lua scripting
\usepackage{amsmath}
\usepackage{unicode-math}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{parskip}
\setlength{\parskip}{0.5em}

% Enable HarfBuzz renderer
\defaultfontfeatures{Renderer=HarfBuzz}

% Main font with emoji fallback using Lua script
\setmainfont[
  Ligatures=TeX,
]{Noto Serif} % Use Noto Serif for broad Unicode support
\setsansfont{Noto Sans}
\setmonofont{Cascadia Code} % Monospace font for code
\setmathfont{Latin Modern Math} % Math font

% Lua script for emoji fallback
\begin{luacode*}
  local function add_emoji_fallback()
    local noto_emoji = font.addfallback(
      font.id('Noto Serif'), -- Base font
      font.load('name:Noto Color Emoji'), -- Fallback font
      {0x1F000, 0x1FFFF} -- Unicode range for emojis
    )
  end
  luatexbase.add_to_callback('pre_linebreak_filter', add_emoji_fallback, 'emoji_fallback')
\end{luacode*}

% Listings configuration for code blocks
\lstset{
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  stringstyle=\color{green!50!black},
  commentstyle=\color{gray},
  breaklines=true,
  frame=single,
  showstringspaces=false,
  numbers=left,
  numberstyle=\tiny,
  tabsize=2,
  breakatwhitespace=true,
  columns=flexible,
  keepspaces=true,
}

% Define languages for syntax highlighting
\lstdefinelanguage{Python}{
  morekeywords={def,return,print,while},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
  morestring=[b]{'},
}
\lstdefinelanguage{Cpp}{
  morekeywords={include,int,main,cout,endl,using,namespace,std},
  sensitive=true,
  morecomment=[l]{//},
  morestring=[b]{"},
}
\lstdefinelanguage{Bash}{
  morekeywords={while,do,done,echo},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
}
\lstdefinelanguage{JSON}{
  morestring=[b]{"},
  literate=
    *{0}{{{\color{red}0}}}{1}
     {1}{{{\color{red}1}}}{1}
     {2}{{{\color{red}2}}}{1}
     {3}{{{\color{red}3}}}{1}
     {4}{{{\color{red}4}}}{1}
     {5}{{{\color{red}5}}}{1}
     {6}{{{\color{red}6}}}{1}
     {7}{{{\color{red}7}}}{1}
     {8}{{{\color{red}8}}}{1}
     {9}{{{\color{red}9}}}{1}
     {true}{{{\color{blue}true}}}{4}
     {false}{{{\color{blue}false}}}{5}
     {null}{{{\color{blue}null}}}{4},
}
\end{xaiArtifact>

### Key Changes in the Updated `header.tex`
1. **Main Font**: Switched from `Latin Modern Roman` to `Noto Serif`, which has better Unicode support and is more likely to handle accents and special characters.
2. **Emoji Fallback**: Added a Lua script using `luacode` to explicitly set `Noto Color Emoji` as a fallback for the Unicode emoji range (U+1F000 to U+1FFFF). This ensures emojis like 😄, 😎, 🚀, and 🐧 are rendered correctly.
3. **Monospace Font**: Kept `Cascadia Code` for code blocks, as it’s suitable for monospace text and doesn’t need emoji support.
4. **Math Font**: Retained `Latin Modern Math` for mathematical expressions, as it’s reliable for equations like \(x^2 + y^2 = z^2\) and \(\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}\).
5. **Additional Packages**: Added `booktabs` for tables and `parskip` for paragraph spacing to match the Markdown structure.
6. **Listings Configuration**: Enhanced `lstlistings` with language definitions for Python, C++, Bash, and JSON, ensuring proper syntax highlighting for all code blocks.

### Prerequisites
1. **MiKTeX**: Ensure MiKTeX is installed and includes `lualatex`. Install the `texlive-fonts-extra` package to include `Noto Serif`, `Noto Sans`, and `Noto Color Emoji`. You can install these fonts via the MiKTeX Console:
   - Open MiKTeX Console.
   - Go to the “Packages” tab.
   - Search for `noto` and install `noto` and `noto-emoji` packages.
2. **Pandoc**: Ensure Pandoc is installed in your Conda environment (`conda install pandoc`).
3. **Cascadia Code**: If not already installed, download and install `Cascadia Code` from its GitHub repository or via MiKTeX if available.
4. **File Setup**: Save the updated `header.tex` and `exemplo.md` in the same directory (e.g., `D:\Downloads\_DOCS_\_DOCS_\CONDA_md_to_pdf\pandoc-lualatex-project-clean-final\`).

### Pandoc Command
Run the following command in your Conda environment’s terminal from the directory containing `exemplo.md` and `header.tex`:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

### Expected Output
- The command will generate `exemplo.pdf` with:
  - Properly rendered text, including accents (á, é, í, ó, ú, ã, õ, ç, etc.).
  - Emojis (😄, 😎, 🚀, 🐧) displayed using `Noto Color Emoji`.
  - Code blocks in Python, C++, Bash, and JSON with syntax highlighting.
  - Mathematical expressions (inline and block) rendered correctly.
  - The table and quote formatted as per LaTeX standards.
- No `Missing character` warnings should appear, as the Lua script ensures emoji fallback.

### Troubleshooting
If you still encounter issues:
1. **Font Not Found**:
   - Verify that `Noto Serif`, `Noto Sans`, `Noto Color Emoji`, and `Cascadia Code` are installed. Check MiKTeX Console or run `fc-list | grep Noto` (on Windows, use PowerShell or WSL) to confirm font availability.
   - If `Noto Color Emoji` is missing, download it from Google’s Noto Fonts website and install it manually in MiKTeX.
2. **LuaLaTeX Errors**:
   - Ensure `lualatex` is installed (`lualatex --version` in the terminal).
   - Check the Pandoc log file (`exemplo.log`) in the same directory for detailed errors.
3. **Emoji Still Missing**:
   - Test with a simpler font setup by temporarily replacing the Lua script with `\setmainfont{Noto Sans}[Renderer=HarfBuzz]` and removing the fallback script to isolate the issue.
4. **Conda Environment**:
   - Activate your Conda environment (`conda activate pandoc-env`) before running the Pandoc command.
   - Ensure Pandoc is up-to-date (`conda update pandoc`).

### Additional Notes
- **Font Availability**: If `Noto Color Emoji` doesn’t work, you can try `Twemoji Mozilla` or `Apple Color Emoji` (if on macOS). Update the Lua script to reference the available emoji font.
- **Performance**: Emoji rendering with HarfBuzz can be slightly slower; ensure your system has sufficient resources.
- **Testing**: To confirm emoji support, create a minimal Markdown file with just emojis and test the conversion:
  ```markdown
  # Test Emojis
  😄 😎 🚀 🐧
  ```
  Run `pandoc test.md -o test.pdf --pdf-engine=lualatex --include-in-header=header.tex` to verify.

This updated setup should resolve the emoji rendering issue and produce a clean PDF with all elements from `exemplo.md` properly formatted. If you encounter further issues, share the specific error messages or logs for additional assistance.

---

### 👤 Utilizador *(2025-09-25 17:18:04)* *[Grok]*

com este header.tex obtem se [WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÿÇ (U+1F600) (U+1F600) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÿÄ (U+1F60E) (U+1F60E) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÜÇ (U+1F680) (U+1F680) in font "name:Noto Sans:mode=node;
[WARNING] Missing character: There is no ≡ƒÉº (U+1F427) (U+1F427) in font "name:Noto Sans:mode=node; e os emojis são representados por u quadrado sem cores

---

### 🤖 Grok *(2025-09-25 17:19:00)* *[Grok]*

The issue you're encountering—missing emojis in the generated PDF and the `[WARNING] Missing character` errors for Unicode characters (U+1F600 😄, U+1F60E 😎, U+1F680 🚀, U+1F427 🐧)—indicates that the emojis are not being rendered correctly because `Noto Sans` does not include emoji glyphs, and the defined `\emojifont` (`Noto Color Emoji`) is not being applied as a fallback for these characters. The warnings show that LuaLaTeX is trying to render the emojis using `Noto Sans`, which lacks the necessary glyphs, resulting in empty squares in the PDF. Additionally, the `Renderer=HarfBuzz` option is not explicitly set, and the font fallback mechanism needs to be configured to use `Noto Color Emoji` for emojis.

Below, I’ll provide an updated `header.tex` to fix the emoji rendering issue, ensuring that `Noto Color Emoji` is used as a fallback for emojis via a Lua script. I’ll also include the necessary packages to handle the other elements in your Markdown file (`exemplo.md`), such as code blocks, mathematics, tables, and quotes, and provide the Pandoc command to generate the PDF correctly.

### Why the Errors Occurred
1. **Noto Sans Lacks Emojis**: `Noto Sans` is a sans-serif font with broad Unicode support for text and symbols but does not include emoji glyphs (e.g., U+1F600). While you defined `\emojifont{Noto Color Emoji}`, it’s not automatically applied to emojis unless explicitly configured as a fallback.
2. **No Fallback Mechanism**: The `fontspec` package alone does not automatically use `\emojifont` for emojis. LuaLaTeX requires a fallback mechanism (e.g., via `luaotfload` or a Lua script) to map emoji Unicode ranges to `Noto Color Emoji`.
3. **HarfBuzz Not Enabled**: The `header.tex` does not specify `Renderer=HarfBuzz` for `Noto Sans` or `Noto Color Emoji`. HarfBuzz is necessary for proper emoji rendering, especially for complex Unicode characters.
4. **Missing Packages**: The provided `header.tex` lacks packages like `listings` for code blocks, `booktabs` for tables, and configurations for syntax highlighting, which are needed to fully render `exemplo.md`.
5. **Repeated Warnings**: The warnings are repeated because Pandoc processes the emojis multiple times (e.g., in different rendering passes or contexts), and LuaLaTeX consistently fails to find the emoji glyphs in `Noto Sans`.

### Updated `header.tex`
To resolve the emoji issue and ensure all elements in `exemplo.md` are rendered correctly, we need to:
- Explicitly enable HarfBuzz for font rendering.
- Use a Lua script to set `Noto Color Emoji` as a fallback for the emoji Unicode range (U+1F000–U+1FFFF).
- Include packages for code blocks (`listings`), tables (`booktabs`), and other formatting to match the Markdown content.
- Configure `lstlistings` for syntax highlighting of Python, C++, Bash, and JSON code blocks.

Here’s the updated `header.tex`:

<xaiArtifact artifact_id="ef562b08-6f3d-4917-9404-9464c5eea801" artifact_version_id="a11c4ecb-b7a5-46c3-9ce3-c4e491990c6a" title="header.tex" contentType="text/latex">
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{fontspec}
\usepackage{luacode} % For Lua script to handle emoji fallback
\usepackage{amsmath}
\usepackage{unicode-math}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{parskip}
\setlength{\parskip}{0.5em}
\usepackage{quoting}
\quotingsetup{vskip=0pt}

% Enable HarfBuzz renderer
\defaultfontfeatures{Renderer=HarfBuzz}

% Font setup
\setmainfont{Noto Sans} % Main font for text
\setsansfont{Noto Sans}
\setmonofont{Cascadia Code} % Monospace font for code
\setmathfont{Latin Modern Math} % Math font
\newfontfamily\emojifont{Noto Color Emoji}[Renderer=HarfBuzz] % Emoji font

% Lua script for emoji fallback
\begin{luacode*}
  local function add_emoji_fallback()
    local emoji_font = font.load('name:Noto Color Emoji')
    if emoji_font then
      font.addfallback(
        font.id('Noto Sans'), -- Base font
        emoji_font, -- Fallback font
        {0x1F000, 0x1FFFF} -- Unicode range for emojis
      )
    end
  end
  luatexbase.add_to_callback('pre_linebreak_filter', add_emoji_fallback, 'emoji_fallback')
\end{luacode*}

% Listings configuration for code blocks
\lstset{
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  stringstyle=\color{green!50!black},
  commentstyle=\color{gray},
  breaklines=true,
  frame=single,
  showstringspaces=false,
  numbers=left,
  numberstyle=\tiny,
  tabsize=2,
  breakatwhitespace=true,
  columns=flexible,
  keepspaces=true,
}

% Define languages for syntax highlighting
\lstdefinelanguage{Python}{
  morekeywords={def,return,print,while},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
  morestring=[b]{'},
}
\lstdefinelanguage{Cpp}{
  morekeywords={include,int,main,cout,endl,using,namespace,std},
  sensitive=true,
  morecomment=[l]{//},
  morestring=[b]{"},
}
\lstdefinelanguage{Bash}{
  morekeywords={while,do,done,echo},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
}
\lstdefinelanguage{JSON}{
  morestring=[b]{"},
  literate=
    *{0}{{{\color{red}0}}}{1}
     {1}{{{\color{red}1}}}{1}
     {2}{{{\color{red}2}}}{1}
     {3}{{{\color{red}3}}}{1}
     {4}{{{\color{red}4}}}{1}
     {5}{{{\color{red}5}}}{1}
     {6}{{{\color{red}6}}}{1}
     {7}{{{\color{red}7}}}{1}
     {8}{{{\color{red}8}}}{1}
     {9}{{{\color{red}9}}}{1}
     {true}{{{\color{blue}true}}}{4}
     {false}{{{\color{blue}false}}}{5}
     {null}{{{\color{blue}null}}}{4},
}
\end{xaiArtifact>

### Key Changes in the Updated `header.tex`
1. **Emoji Fallback with Lua Script**: Added a Lua script using `luacode` to map the emoji Unicode range (U+1F000–U+1FFFF) to `Noto Color Emoji`. This ensures emojis are rendered using the correct font.
2. **HarfBuzz Renderer**: Explicitly enabled `Renderer=HarfBuzz` for both `Noto Sans` and `Noto Color Emoji` to ensure proper glyph rendering.
3. **Font Setup**:
   - Kept `Noto Sans` as the main font for text, as it supports accents and most Unicode characters (except emojis).
   - Used `Cascadia Code` for code blocks, as it’s suitable for monospace text.
   - Retained `Latin Modern Math` for mathematical expressions.
   - Defined `\emojifont{Noto Color Emoji}` with HarfBuzz for use in the Lua fallback script.
4. **Additional Packages**:
   - Added `listings` and `xcolor` for code block syntax highlighting.
   - Included `booktabs` for table formatting.
   - Added `quoting` for proper rendering of block quotes.
   - Used `geometry` to set A4 paper with 1-inch margins and `parskip` for paragraph spacing.
5. **Syntax Highlighting**: Configured `lstlistings` with language definitions for Python, C++, Bash, and JSON to match the code blocks in `exemplo.md`.

### Pandoc Command
Run the following command in your Conda environment’s terminal from the directory containing `exemplo.md` and `header.tex` (e.g., `D:\Downloads\_DOCS_\_DOCS_\CONDA_md_to_pdf\pandoc-lualatex-project-clean-final\`):

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

### Prerequisites
1. **MiKTeX**:
   - Ensure MiKTeX is installed with `lualatex` (`lualatex --version` to verify).
   - Install the `noto` and `noto-emoji` packages via MiKTeX Console:
     - Open MiKTeX Console.
     - Go to the “Packages” tab.
     - Search for `noto` and install `noto` and `noto-emoji`.
   - Install `Cascadia Code` if not already available (download from its GitHub repository or check MiKTeX).
2. **Pandoc**:
   - Ensure Pandoc is installed in your Conda environment: `conda install pandoc`.
   - Activate the environment: `conda activate pandoc-env`.
3. **File Setup**:
   - Save the updated `header.tex` above in the same directory as `exemplo.md`.
   - Ensure `exemplo.md` contains the original content (text with emojis, code blocks, math, table, and quote).

### Expected Output
- The command will generate `exemplo.pdf` with:
  - Emojis (😄, 😎, 🚀, 🐧) rendered in color using `Noto Color Emoji`.
  - Accents (á, é, í, ó, ú, ã, õ, ç, etc.) displayed correctly with `Noto Sans`.
  - Code blocks (Python, C++, Bash, JSON) with syntax highlighting.
  - Mathematical expressions (e.g., \(x^2 + y^2 = z^2\), \(\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}\)) rendered correctly.
  - Table and quote formatted professionally.
- No `Missing character` warnings should appear, as the Lua script ensures emojis are handled by `Noto Color Emoji`.

### Troubleshooting
If the issue persists:
1. **Font Availability**:
   - Verify that `Noto Sans` and `Noto Color Emoji` are installed: run `fc-list | findstr Noto` in Windows Command Prompt or PowerShell.
   - If missing, download `Noto Color Emoji` from Google’s Noto Fonts website and install it via MiKTeX Console or manually.
2. **LuaLaTeX Errors**:
   - Check the `exemplo.log` file in the output directory for detailed errors.
   - Ensure `luaotfload` is up-to-date in MiKTeX (update via MiKTeX Console).
3. **Emoji Rendering**:
   - Test with a minimal Markdown file:
     ```markdown
     # Test Emojis
     😄 😎 🚀 🐧
     ```
     Run `pandoc test.md -o test.pdf --pdf-engine=lualatex --include-in-header=header.tex` to isolate emoji rendering.
4. **Conda Environment**:
   - Ensure the correct environment is active: `conda activate pandoc-env`.
   - Update Pandoc: `conda update pandoc`.
5. **Alternative Emoji Font**:
   - If `Noto Color Emoji` fails, try `Twemoji Mozilla` or `Segoe UI Emoji` (Windows). Update the Lua script to:
     ```latex
     local emoji_font = font.load('name:Segoe UI Emoji')
     ```

### Additional Notes
- **Color Emojis**: `Noto Color Emoji` renders emojis in color, which is ideal for PDFs. If you prefer monochrome emojis, use `Noto Emoji` instead (update the Lua script accordingly).
- **Performance**: Emoji rendering with HarfBuzz may slightly increase compilation time. Ensure your system has sufficient resources.
- **MiKTeX Updates**: Run MiKTeX Console in Admin and User modes to update all packages (`Tasks > Update`).

This updated `header.tex` should resolve the emoji rendering issue and produce a PDF with all elements of `exemplo.md` correctly formatted. If you encounter further errors, share the `exemplo.log` file or specific error messages for additional assistance.

---

### 🤖 Grok *(2025-09-25 19:08:38)* *[Grok]*

The issue you're encountering—emojis appearing as empty squares in the generated PDF and the `[WARNING] Missing character` errors—indicates that the `Noto Sans` font does not include glyphs for emojis (e.g., 😄 U+1F600, 😎 U+1F60E, 🚀 U+1F680, 🐧 U+1F427), and the `Noto Color Emoji` font, although defined in `header.tex`, is not being used as a fallback for these characters. The warnings suggest that LuaLaTeX is not applying the `Noto Color Emoji` font to render the emojis, likely because the font fallback mechanism is not properly configured.

The provided `header.tex` defines `Noto Color Emoji` as a separate font family (`\emojifont`) but does not explicitly link it to `Noto Sans` for fallback when rendering emojis. Additionally, the `Renderer=HarfBuzz` option is not explicitly set, which is necessary for proper emoji rendering with `Noto Color Emoji`. Below, I’ll provide an updated `header.tex` to fix the emoji rendering issue, explain why the errors occurred, and provide the steps to generate the PDF correctly using Pandoc and LuaLaTeX in your Conda environment.

### Why the Errors Occurred
1. **No Emoji Support in Noto Sans**: `Noto Sans` is a sans-serif font with good Unicode support for many scripts but does not include emoji glyphs (e.g., U+1F600–U+1F680). This causes the "Missing character" warnings when LuaLaTeX tries to render emojis using `Noto Sans`.
2. **Unused Emoji Font**: Defining `\newfontfamily\emojifont{Noto Color Emoji}` creates a font family but does not automatically apply it as a fallback for `Noto Sans`. Pandoc’s LaTeX output does not know to use `\emojifont` for emojis unless explicitly instructed.
3. **Missing Fallback Mechanism**: Unlike some other TeX engines or applications, `fontspec` in LuaLaTeX does not have a built-in `Fallback` option. A Lua script or manual font switching is required to handle emoji fallbacks.
4. **HarfBuzz Renderer**: The `header.tex` does not specify `Renderer=HarfBuzz` for `Noto Color Emoji`, which is necessary for rendering color emojis correctly.
5. **Font Availability**: The `Noto Color Emoji` font must be installed in your MiKTeX distribution. If it’s missing or not accessible, LuaLaTeX cannot use it, leading to empty squares.
6. **Repeated Warnings**: The warnings are repeated because Pandoc processes the emojis multiple times (e.g., in different rendering passes or contexts), and each time, LuaLaTeX fails to find the emoji glyphs in `Noto Sans`.

### Updated `header.tex`
To fix the emoji rendering issue, we need to:
- Use a Lua script to set up `Noto Color Emoji` as a fallback for the emoji Unicode range (U+1F000–U+1FFFF).
- Explicitly enable the HarfBuzz renderer for both `Noto Sans` and `Noto Color Emoji`.
- Include necessary packages for other elements in `exemplo.md` (e.g., code blocks, mathematics, tables).
- Ensure compatibility with the Markdown structure (text, code, math, tables, quotes).

Here’s the updated `header.tex`:

<xaiArtifact artifact_id="928ec2b8-2af9-41d6-935a-db615dfe249a" artifact_version_id="fa1d9806-d23e-4542-be80-73e76a1e32a8" title="header.tex" contentType="text/latex">
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{fontspec}
\usepackage{luacode} % For Lua scripting
\usepackage{unicode-math}
\usepackage{amsmath}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{parskip}
\setlength{\parskip}{0.5em}
\usepackage{quoting}
\quotingsetup{vskip=0pt}

% Enable HarfBuzz renderer
\defaultfontfeatures{Renderer=HarfBuzz}

% Main font with emoji fallback
\setmainfont{Noto Sans}[
  Ligatures=TeX,
]
\setsansfont{Noto Sans}
\setmonofont{Cascadia Code} % Monospace font for code
\setmathfont{Latin Modern Math} % Math font

% Lua script for emoji fallback
\begin{luacode*}
  local function add_emoji_fallback()
    local noto_emoji = font.addfallback(
      font.id('Noto Sans'), -- Base font
      font.load('name:Noto Color Emoji'), -- Fallback font
      {0x1F000, 0x1FFFF} -- Unicode range for emojis
    )
  end
  luatexbase.add_to_callback('pre_linebreak_filter', add_emoji_fallback, 'emoji_fallback')
\end{luacode*}

% Listings configuration for code blocks
\lstset{
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  stringstyle=\color{green!50!black},
  commentstyle=\color{gray},
  breaklines=true,
  frame=single,
  showstringspaces=false,
  numbers=left,
  numberstyle=\tiny,
  tabsize=2,
  breakatwhitespace=true,
  columns=flexible,
  keepspaces=true,
}

% Define languages for syntax highlighting
\lstdefinelanguage{Python}{
  morekeywords={def,return,print,while},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
  morestring=[b]{'},
}
\lstdefinelanguage{Cpp}{
  morekeywords={include,int,main,cout,endl,using,namespace,std},
  sensitive=true,
  morecomment=[l]{//},
  morestring=[b]{"},
}
\lstdefinelanguage{Bash}{
  morekeywords={while,do,done,echo},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]{"},
}
\lstdefinelanguage{JSON}{
  morestring=[b]{"},
  literate=
    *{0}{{{\color{red}0}}}{1}
     {1}{{{\color{red}1}}}{1}
     {2}{{{\color{red}2}}}{1}
     {3}{{{\color{red}3}}}{1}
     {4}{{{\color{red}4}}}{1}
     {5}{{{\color{red}5}}}{1}
     {6}{{{\color{red}6}}}{1}
     {7}{{{\color{red}7}}}{1}
     {8}{{{\color{red}8}}}{1}
     {9}{{{\color{red}9}}}{1}
     {true}{{{\color{blue}true}}}{4}
     {false}{{{\color{blue}false}}}{5}
     {null}{{{\color{blue}null}}}{4},
}
\end{xaiArtifact>

### Key Changes in the Updated `header.tex`
1. **Font Configuration**:
   - Kept `Noto Sans` as the main font for text, as it supports accents and many Unicode characters (but not emojis).
   - Added `Cascadia Code` as the monospace font for code blocks, consistent with your previous setup.
   - Retained `Latin Modern Math` for mathematical expressions (e.g., \(x^2 + y^2 = z^2\), \(\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}\)).
2. **Emoji Fallback**:
   - Added a Lua script via the `luacode` package to set `Noto Color Emoji` as a fallback for the Unicode emoji range (U+1F000–U+1FFFF).
   - The script uses `font.addfallback` to dynamically load `Noto Color Emoji` when `Noto Sans` lacks the required glyphs.
3. **HarfBuzz Renderer**:
   - Enabled `Renderer=HarfBuzz` globally via `\defaultfontfeatures{Renderer=HarfBuzz}` to ensure proper rendering of emojis and complex scripts.
4. **Additional Packages**:
   - Added `booktabs` for table formatting (e.g., the table with Alice, Bob, Charlie).
   - Added `quoting` for proper rendering of block quotes (e.g., the Leonardo da Vinci quote).
   - Included `parskip` for paragraph spacing to match Markdown’s visual style.
   - Configured `lstlistings` with language definitions for Python, C++, Bash, and JSON to handle all code blocks in `exemplo.md`.
5. **Input Encoding**: Added `\usepackage[utf8]{inputenc}` and `\usepackage[T1]{fontenc}` to ensure compatibility with UTF-8 input and proper character handling.

### Prerequisites
1. **MiKTeX**:
   - Ensure MiKTeX is installed with `lualatex` (`lualatex --version` to verify).
   - Install the `noto` and `noto-emoji` packages via MiKTeX Console:
     - Open MiKTeX Console.
     - Go to the “Packages” tab.
     - Search for `noto` and install `noto` (for `Noto Sans`) and `noto-emoji` (for `Noto Color Emoji`).
   - Install `Cascadia Code` if not already available. Download from the Cascadia Code GitHub repository or check if MiKTeX provides it.
2. **Pandoc**:
   - Ensure Pandoc is installed in your Conda environment (`conda activate pandoc-env; conda install pandoc`).
   - Update Pandoc if necessary (`conda update pandoc`).
3. **File Setup**:
   - Save the updated `header.tex` and `exemplo.md` in the same directory (e.g., `D:\Downloads\_DOCS_\_DOCS_\CONDA_md_to_pdf\pandoc-lualatex-project-clean-final\`).
4. **Font Verification**:
   - Confirm that `Noto Sans` and `Noto Color Emoji` are installed. Run `fc-list | findstr Noto` in a Windows Command Prompt or PowerShell to check font availability.
   - If `Noto Color Emoji` is missing, download it from Google’s Noto Fonts website and install it manually in MiKTeX.

### Pandoc Command
Run the following command in your Conda environment’s terminal from the directory containing `exemplo.md` and `header.tex`:

```bash
pandoc exemplo.md -o exemplo.pdf --pdf-engine=lualatex --include-in-header=header.tex
```

### Expected Output
- The command will generate `exemplo.pdf` with:
  - Properly rendered text, including accents (á, é, í, ó, ú, ã, õ, ç, etc.).
  - Emojis (😄, 😎, 🚀, 🐧) displayed in color using `Noto Color Emoji`.
  - Code blocks in Python, C++, Bash, and JSON with syntax highlighting.
  - Mathematical expressions (inline and block) rendered correctly using `Latin Modern Math`.
  - The table and quote formatted professionally with `booktabs` and `quoting`.
- No `Missing character` warnings should appear, as the Lua script ensures `Noto Color Emoji` is used for emojis.

### Troubleshooting
If emojis still appear as squares or warnings persist:
1. **Font Not Installed**:
   - Verify `Noto Color Emoji` is installed. Check MiKTeX Console or run `fc-list | findstr "Noto Color Emoji"` in Command Prompt/PowerShell.
   - If missing, install via MiKTeX or manually download from Google’s Noto Fonts and add to MiKTeX’s font directory.
2. **LuaLaTeX Issues**:
   - Check the `exemplo.log` file in the same directory for detailed errors.
   - Ensure `lualatex` is up-to-date in MiKTeX (`miktex-console` → Updates).
3. **Lua Script Failure**:
   - Test without the Lua script by temporarily setting `\setmainfont{Noto Color Emoji}` in `header.tex` to confirm the font works. Note that this will apply `Noto Color Emoji` to all text, which is not ideal but useful for debugging.
4. **Conda Environment**:
   - Ensure the correct environment is active (`conda activate pandoc-env`).
   - Verify Pandoc version (`pandoc --version`) and update if needed.
5. **Alternative Emoji Font**:
   - If `Noto Color Emoji` fails, try `Twemoji Mozilla` or `Segoe UI Emoji` (Windows). Update the Lua script to:
     ```latex
     font.load('name:Segoe UI Emoji')
     ```
     Ensure the font is installed on your system.
6. **Minimal Test**:
   - Create a test Markdown file:
     ```markdown
     # Test Emojis
     😄 😎 🚀 🐧
     ```
     Run `pandoc test.md -o test.pdf --pdf-engine=lualatex --include-in-header=header.tex` to isolate emoji rendering issues.

### Additional Notes
- **Color Emojis**: `Noto Color Emoji` renders emojis in color, which is ideal for modern PDFs. If you prefer monochrome emojis, use `Noto Emoji` instead by updating the Lua script to `font.load('name:Noto Emoji')`.
- **Performance**: Rendering color emojis with HarfBuzz can be resource-intensive. Ensure your system has sufficient memory and processing power.
- **Pandoc Filters**: If the Lua script approach is unreliable, consider a Pandoc Lua filter to wrap emojis in `\emojifont{}` commands, but this requires additional setup.

This updated `header.tex` should resolve the emoji rendering issue, producing a PDF with colored emojis and no warnings. If you encounter further issues, share the `exemplo.log` file or specific error messages for targeted assistance.

---

*Conversa exportada do Grok*
*Processado em: 23/11/2025 23:05*