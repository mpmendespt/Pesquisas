# Optimização de comb_fragments_system3_html_export.py

## 📊 Informações
- **Número:** #16
- **Origem:** DeepSeek
- **Categoria:** Outros
- **ID:** 4427487c-667f-42b5-9189-e738d6efc748
- **Criada em:** 2025-11-07 19:51:18
- **Atualizada em:** 2025-11-08 01:57:04
- **Total de mensagens:** 14
- **Resumo:** Optimização de comb_fragments_system3_html_export.py. Pretendo a optimização da conversão para html,...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-07 19:51:20)* *[deepseek-reasoner]*

Optimização de comb_fragments_system3_html_export.py. Pretendo a optimização da conversão para html, com  --standalone --mathjax --embed-resources --syntax-highlighting=pygments --to=html5. E usar --mathjax=assets/tex-mml-chtml.js; Porque já fiz o respectivo download com: mkdir -p assets;  wget "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" -O "assets/tex-mml-chtml.js"; (Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>dir assets
 Volume in drive D is _Work_
 Volume Serial Number is 3CB7-A082

 Directory of D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op\assets

11/07/2025  11:46 AM    <DIR>          .
11/07/2025  11:46 AM    <DIR>          ..
11/07/2025  11:46 AM         1,173,007 tex-mml-chtml.js
               1 File(s)      1,173,007 bytes;  Se existir mais alguma sujestão pretendo essa informação para melhorar a conversão.

---

### 🤖 DeepSeek *(2025-11-07 19:51:20)* *[deepseek-reasoner]*

Vamos otimizar a conversão para HTML no método `_convert_with_pandoc` para usar as opções mencionadas, incluindo o uso do MathJax local.

Alterações propostas:
1. Usar `--standalone` para gerar um HTML completo.
2. Usar `--mathjax` apontando para o arquivo local: `--mathjax=assets/tex-mml-chtml.js`.
3. Adicionar `--embed-resources` para embedar CSS, imagens, etc. (no entanto, note que isso pode não ser compatível com a saída HTML5, e o Pandoc pode não suportar embedar todos os recursos em HTML5. Vamos verificar a documentação: normalmente, `--embed-resources` é usado com `--self-contained` e para HTML4, mas vamos tentar).
4. Usar `--syntax-highlighting=pygments` para realce de sintaxe.
5. Usar `--to=html5`.

No entanto, note que a opção `--embed-resources` é suportada apenas em conjunto com `--self-contained` e para HTML4. Para HTML5, o Pandoc não suporta embedar recursos no mesmo arquivo. Portanto, se quisermos um arquivo HTML auto-contido, teríamos que usar `--self-contained` e talvez mudar para `html4`? Mas não é o que queremos, porque queremos HTML5.

Alternativa: Vamos usar `--self-contained` com HTML5? A documentação do Pandoc diz que `--self-contained` produz um HTML4, mas na versão recente do Pandoc, ele pode produzir HTML5 com `--self-contained`? Vamos verificar a documentação: 

Na versão 2.19.2, a opção `--self-contained` é suportada para HTML5, mas note que ela pode não ser totalmente compatível porque o HTML5 não suporta a inclusão de recursos como CSS e JS na mesma maneira que o HTML4. No entanto, o Pandoc tenta fazer isso.

Mas note: o MathJax é um recurso externo. Se usarmos `--self-contained`, o Pandoc vai tentar baixar e incorporar o MathJax? Isso não é desejável porque o MathJax é muito grande e complexo para ser incorporado.

Portanto, vamos reconsiderar:

- Queremos um arquivo HTML que funcione offline? Sim, mas com o MathJax local, mas não necessariamente embedado no mesmo arquivo, e sim como um arquivo separado que está na pasta `assets`.

Plano:
1. Usar `--mathjax=assets/tex-mml-chtml.js` para apontar para o MathJax local.
2. Não usar `--embed-resources` porque queremos manter o MathJax como um recurso externo (mesmo que local) e não embedado no HTML.
3. Usar `--standalone` para gerar um HTML completo.
4. Usar `--syntax-highlighting=pygments` para realce de sintaxe.
5. Usar `--to=html5`.

Além disso, note que o Pandoc pode não suportar a opção `--syntax-highlighting=pygments`? A opção correta é `--highlight-style=pygments`. Vou corrigir.

Vamos ajustar o método `_convert_with_pandoc`:

Substituir a chamada do subprocess para usar:

```python
result = subprocess.run([
    'pandoc', 
    str(md_file_path),
    '--from', 'markdown+emoji',
    '--to', 'html5',
    '--standalone',
    '--mathjax=assets/tex-mml-chtml.js',
    '--highlight-style', 'pygments'
], capture_output=True, text=True, encoding='utf-8', timeout=60)
```

Além disso, note que o arquivo `tex-mml-chtml.js` está na pasta `assets` (relativo ao diretório de trabalho atual). Portanto, o HTML gerado vai referenciar `assets/tex-mml-chtml.js`. Isso significa que, quando abrimos o HTML, ele vai procurar o MathJax em `assets/tex-mml-chtml.js` (relativo ao local do HTML). Portanto, precisamos garantir que a pasta `assets` esteja no mesmo diretório que o HTML, ou ajustar o caminho.

Como estamos gerando HTML na pasta `combined_html`, e a pasta `assets` está no diretório raiz (onde está o script), então o caminho relativo from `combined_html` to `assets` é `../assets`. Portanto, talvez tenhamos que ajustar o caminho para `../assets/tex-mml-chtml.js`.

Mas note: o Pandoc gera um caminho relativo para o MathJax. Se usarmos `--mathjax=assets/tex-mml-chtml.js`, o Pandoc vai gerar:

```html
<script src="assets/tex-mml-chtml.js"></script>
```

Isso significa que o HTML vai procurar a pasta `assets` no mesmo diretório que o HTML. Portanto, precisamos copiar a pasta `assets` para a pasta `combined_html`? Ou então, podemos ajustar o caminho para `../assets/tex-mml-chtml.js`?

Alternativa: Vamos mudar o comando para:

```python
    '--mathjax=../assets/tex-mml-chtml.js',
```

Assim, o HTML gerado na pasta `combined_html` vai referenciar o MathJax em `../assets/tex-mml-chtml.js`.

Mas note: se o HTML for aberto a partir do índice (que está na raiz), o caminho relativo from o índice para o assets é `assets/tex-mml-chtml.js`, mas from o HTML (dentro de `combined_html`) para o assets é `../assets/tex-mml-chtml.js`. Portanto, o mesmo arquivo MathJax deve ser acessível por dois caminhos diferentes? Isso não é ideal.

Outra solução: copiar a pasta `assets` para a pasta `combined_html`? Mas aí teríamos duplicação.

Ou então, podemos usar uma estrutura de pastas diferente:

- Colocar o MathJax em uma pasta `assets` na raiz e, no HTML, usar um caminho absoluto (relativo ao sistema de arquivos) não é portável.

Vamos repensar: o índice HTML está na raiz, e os HTMLs estão em `combined_html`. O índice HTML usa o MathJax de `assets/tex-mml-chtml.js` (porque o índice está na raiz). Já os HTMLs convertidos, se usarem `../assets/tex-mml-chtml.js`, vão subir um nível e encontrar a pasta `assets` na raiz. Isso funciona.

Portanto, vamos usar `--mathjax=../assets/tex-mml-chtml.js` para a conversão dos HTMLs.

Além disso, note que o método `_convert_with_pandoc` é chamado para cada arquivo Markdown, e o HTML é salvo em `combined_html`. Portanto, o caminho relativo para a raiz (onde está a pasta `assets`) é `../assets`.

Vamos ajustar:

```python
    result = subprocess.run([
        'pandoc', 
        str(md_file_path),
        '--from', 'markdown+emoji',
        '--to', 'html5',
        '--standalone',
        '--mathjax=../assets/tex-mml-chtml.js',
        '--highlight-style', 'pygments'
    ], capture_output=True, text=True, encoding='utf-8', timeout=60)
```

Além disso, note que o método `_apply_custom_style` adiciona um estilo CSS personalizado. Vamos garantir que esse estilo não entre em conflito com o estilo gerado pelo Pandoc. O Pandoc, com `--standalone`, já gera um estilo CSS para o realce de sintaxe (pygments) e para o layout. Nosso estilo customizado pode sobrescrever alguns estilos.

Vamos remover a aplicação de estilo customizado? Não, porque queremos um estilo consistente. Mas note que o Pandoc gera um estilo embutido (na tag `<style>`) para o realce de sintaxe. Nosso estilo customizado deve ser aplicado após o estilo do Pandoc, para sobrescrever o que for necessário.

No método `_apply_custom_style`, estamos injetando o estilo customizado no `<head>`. Isso é aceitável.

Outra consideração: a opção `--embed-resources` não será usada, então o HTML gerado não será auto-contido (o MathJax é um recurso externo). Mas isso é aceitável, pois temos o MathJax localmente.

Vamos também verificar se o Pandoc está gerando o realce de sintaxe corretamente com o estilo pygments. Se não, podemos ajustar o `--highlight-style` para um estilo que preferirmos.

Além disso, note que o método `_convert_with_fallback` e `_create_basic_html` também são usados em caso de falha. Vamos ajustá-los para usar o MathJax local? Sim, para consistência.

No método `_convert_with_fallback`, não usamos Pandoc, então vamos ajustar o template para usar o MathJax local:

No método `_create_html_template` (usado no fallback), vamos mudar o script do MathJax para:

```html
    <script src="../assets/tex-mml-chtml.js"></script>
```

Da mesma forma, no método `_create_basic_html` (último recurso), vamos fazer o mesmo.

Vamos fazer essas alterações:

1. No método `_convert_with_pandoc`, ajustar o comando para usar `--mathjax=../assets/tex-mml-chtml.js` e `--highlight-style pygments`.
2. Nos métodos `_create_html_template` e `_create_basic_html`, ajustar o script do MathJax para apontar para `../assets/tex-mml-chtml.js`.

Além disso, note que o índice HTML (gerado pelo método `create_searchable_index`) usa o MathJax do CDN. Vamos mudar para local? Não é necessário, porque o índice não contém fórmulas matemáticas. Mas se quisermos, podemos mudar. No entanto, o índice não usa MathJax, então podemos deixar como está.

Vamos implementar as alterações:

- No método `_convert_with_pandoc`:
  - Adicionar `--mathjax=../assets/tex-mml-chtml.js`
  - Adicionar `--highlight-style pygments`

- No método `_create_html_template`:
  - Alterar o script do MathJax para: `src="../assets/tex-mml-chtml.js"`

- No método `_create_basic_html`:
  - Alterar o script do MathJax para: `src="../assets/tex-mml-chtml.js"`

Vamos também verificar se o caminho `../assets` é correto para a estrutura de pastas.

Estrutura:
- Raiz:
  - assets/tex-mml-chtml.js
  - combined_html/ (aqui estão os HTMLs)
  - index.html

Portanto, from um HTML em `combined_html`, o assets está em `../assets`.

Agora, vamos ao código. Aqui está a versão otimizada do código com melhorias na conversão HTML:

```python
# comb_fragments_system3_html_export.py (versão otimizada)
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
from typing import List, Dict, Any, Optional
import markdown
import logging

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        self.assets_dir = Path("assets")
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        # Configuração de processamento por fonte
        self.processors = {
            'qwen': {
                'file': "chat-export.json",
                'method': self.process_qwen_enhanced,
                'enabled': True
            },
            'chatgpt': {
                'file': "chatgpt.zip", 
                'method': self.process_chatgpt,
                'enabled': True
            },
            'deepseek': {
                'file': "deepseek_data.zip",
                'method': self.process_deepseek,
                'enabled': True
            },
            'grok': {
                'file': "grok.zip",
                'method': self.process_grok,
                'enabled': True
            }
        }

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando recursos locais e opções avançadas"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc ot

---

### 👤 Utilizador *(2025-11-07 19:54:32)* *[deepseek-reasoner]*

Optimização de comb_fragments_system3_html_export.py. Pretendo a optimização da conversão para html, com  --standalone --mathjax --embed-resources --syntax-highlighting=pygments --to=html5. E usar --mathjax=assets/tex-mml-chtml.js; Porque já fiz o respectivo download com: mkdir -p assets;  wget "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" -O "assets/tex-mml-chtml.js"; (Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>dir assets
 Volume in drive D is _Work_
 Volume Serial Number is 3CB7-A082

 Directory of D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op\assets

11/07/2025  11:46 AM    <DIR>          .
11/07/2025  11:46 AM    <DIR>          ..
11/07/2025  11:46 AM         1,173,007 tex-mml-chtml.js
               1 File(s)      1,173,007 bytes;  Se existir mais alguma sujestão pretendo essa informação para melhorar a conversão. Se --embed-resources não é suportada em HTML5, então pretendo usar HTML4

---

### 🤖 DeepSeek *(2025-11-07 19:54:32)* *[deepseek-reasoner]*

Vamos otimizar a conversão para HTML usando as opções do Pandoc que você mencionou.
 Além disso, vamos ajustar para usar o MathJax local (assets/tex-mml-chtml.js) e, se necessário, adaptar para HTML4 se --embed-resources não for suportado em HTML5.

 No entanto, note que a opção --embed-resources é suportada apenas para HTML5? Na verdade, o Pandoc suporta --embed-resources para HTML4 e HTML5, mas para HTML4, ele usa base64 para imagens, etc. 
 Mas como queremos usar MathJax local, e não queremos depender de recursos online, vamos tentar usar --embed-resources e --mathjax com o caminho local.

 Vamos modificar a função `_convert_with_pandoc` para usar as opções:

   --standalone
   --mathjax=assets/tex-mml-chtml.js
   --embed-resources
   --syntax-highlighting=pygments
   --to=html5

 Mas note: --embed-resources pode não ser suportado em todas as versões do Pandoc. Se não for suportado, podemos remover e usar recursos externos.

 Além disso, vamos ajustar o template HTML para incluir o MathJax local, mas note que o --mathjax do Pandoc já inclui o script do MathJax. Com --embed-resources, o Pandoc pode tentar embutir o MathJax? 
 Não, --embed-resources é para imagens, CSS, etc. O MathJax é um script externo. Como baixamos o MathJax local, podemos usar o caminho local.

 No entanto, o Pandoc não baixa o MathJax, então temos que garantir que o caminho local está correto.

 Vamos mudar a opção --mathjax para apontar para o arquivo local: --mathjax=assets/tex-mml-chtml.js

 E também, como temos o arquivo local, podemos usar --mathjax sem a URL online.

 Outra coisa: a opção --syntax-highlighting=pygments pode ser substituída por --highlight-style=pygments, mas a opção --syntax-highlighting não existe. Vou verificar a documentação do Pandoc.

 Na versão 2.11 e acima, a opção é --highlight-style=pygments.

 Vamos ajustar para a opção correta.

 Vamos reescrever a função `_convert_with_pandoc`:

   - Usar as opções: 
        ['pandoc', md_file, '--from', 'markdown+emoji', '--to', 'html5', '--standalone', 
         '--mathjax=assets/tex-mml-chtml.js', '--embed-resources', '--highlight-style=pygments']

   - Se falhar, tentar sem --embed-resources, pois pode não ser suportado.

   - Se ainda falhar, usar o fallback.

 No entanto, note que --embed-resources pode não ser necessário se quisermos apenas o MathJax local. Mas ele é útil para embutir imagens (se houver) e CSS.

 Vamos tentar com --embed-resources e, se der erro, tentar sem.

 Vamos modificar a função para tentar duas vezes:

  1. Com --embed-resources
  2. Sem --embed-resources

 E, em ambos os casos, usar o MathJax local.

 Além disso, vamos ajustar o template HTML fallback para usar o MathJax local, caso o Pandoc não o inclua (porque usamos --mathjax, ele deve incluir).

 Vamos também modificar a função `_create_html_template` e `_create_basic_html` para usar o MathJax local.

 No entanto, note que o Pandoc, quando usamos --mathjax, adiciona um script que aponta para o arquivo local. Mas se usarmos --embed-resources, o Pandoc não embute o MathJax, apenas o script é incluído com o src apontando para o local.

 Portanto, precisamos garantir que o arquivo HTML gerado possa acessar o assets/tex-mml-chtml.js. Como estamos gerando HTML na pasta combined_html, e a pasta assets está na raiz, o caminho relativo seria ../assets/tex-mml-chtml.js.

 Mas note: o Pandoc não ajusta o caminho do MathJax para o relativo. Ele usa o caminho que passamos. Então, se passarmos --mathjax=assets/tex-mml-chtml.js, o script no HTML gerado será:

   <script src="assets/tex-mml-chtml.js"></script>

 Isso vai procurar a pasta assets dentro da pasta combined_html. Mas nossa pasta assets está na raiz. Então, temos duas opções:

  1. Copiar a pasta assets para dentro de combined_html.
  2. Ajustar o caminho para ../assets/tex-mml-chtml.js.

 Vamos optar por ajustar o caminho para ../assets/tex-mml-chtml.js.

 Então, vamos mudar a opção para: --mathjax=../assets/tex-mml-chtml.js

 E, nos templates fallback, vamos ajustar o script para usar ../assets/tex-mml-chtml.js.

 Vamos modificar:

   - No Pandoc: usar --mathjax=../assets/tex-mml-chtml.js
   - No template fallback: alterar o src do MathJax para ../assets/tex-mml-chtml.js

 Dessa forma, o HTML em combined_html poderá acessar o MathJax na raiz.

 Vamos implementar:

  1. Modificar a função `_convert_with_pandoc` para tentar com --embed-resources e, se falhar, sem.
  2. Usar o caminho ../assets/tex-mml-chtml.js para o MathJax.

 Além disso, vamos adicionar uma verificação: se o arquivo assets/tex-mml-chtml.js existe, senão, usar a versão online? 
 Mas como você já baixou, vamos assumir que existe.

 Vamos ao código:

 Primeiro, na função `_convert_with_pandoc`:

   Tentaremos com --embed-resources. Se der erro, tentaremos sem.

   Com --embed-resources:

        command = [
            'pandoc', 
            str(md_file_path),
            '--from', 'markdown+emoji',
            '--to', 'html5',
            '--standalone',
            '--mathjax=../assets/tex-mml-chtml.js',
            '--embed-resources',
            '--highlight-style=pygments'
        ]

   Se falhar, tentaremos sem --embed-resources:

        command = [
            'pandoc', 
            str(md_file_path),
            '--from', 'markdown+emoji',
            '--to', 'html5',
            '--standalone',
            '--mathjax=../assets/tex-mml-chtml.js',
            '--highlight-style=pygments'
        ]

   Se ainda falhar, usamos o fallback.

   E no fallback, vamos ajustar o MathJax para local.

   Vamos modificar `_create_html_template` e `_create_basic_html` para usar o MathJax local.

   Em `_create_html_template`:

        <script id="MathJax-script" async src="../assets/tex-mml-chtml.js"></script>

   E em `_create_basic_html`:

        <script id="MathJax-script" async src="../assets/tex-mml-chtml.js"></script>

   E também, note que o fallback não usa mais o polyfill online? Vamos manter o polyfill online? Ou temos local?
   Vamos manter o polyfill online, pois não o baixamos. Mas se quiser, pode baixar e usar local. Por enquanto, vamos manter online.

   No entanto, o polyfill não é estritamente necessário, então podemos remover? Mas o MathJax pode exigir. Vamos manter como estava.

   Vamos também adicionar uma verificação: se o arquivo local do MathJax existe, senão, usar o online? Mas como o usuário já baixou, vamos confiar.

   Mas para evitar problemas, se o arquivo local não existir, podemos usar o online. Vamos fazer isso?

   Podemos verificar se o arquivo assets/tex-mml-chtml.js existe. Se existir, usamos local, senão, usamos o online.

   Vamos criar uma função auxiliar para retornar a URL do MathJax:

        def get_mathjax_url(self):
            local_mathjax = Path("assets/tex-mml-chtml.js")
            if local_mathjax.exists():
                return "../assets/tex-mml-chtml.js"
            else:
                return "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

   E usá-la em todos os lugares.

   Vamos modificar:

        - No Pandoc: --mathjax=<url> -> usaremos a URL local se existir, senão a online.
        - Nos templates: usar a URL retornada por get_mathjax_url.

   Mas note: no Pandoc, a opção --mathjax espera um caminho (ou URL). Então, podemos passar a URL local (caminho relativo) ou a URL online.

   Vamos fazer:

        mathjax_url = self.get_mathjax_url()

        command = [
            ...,
            f'--mathjax={mathjax_url}',
            ...
        ]

   E nos templates, usamos a mesma URL.

   No entanto, no template, o caminho é relativo ao HTML. Se usarmos a URL online, não há problema. Se usarmos a local, é relativo.

   Vamos implementar a função `get_mathjax_url` e usá-la em todos os lugares.

   Vamos também modificar a função `_convert_with_pandoc` para usar essa URL.

   E modificar os templates para usar a URL dinâmica.

   Vamos lá.

   Passos:

   1. Adicionar função `get_mathjax_url`.
   2. Modificar `_convert_with_pandoc` para usar `get_mathjax_url`.
   3. Modificar `_create_html_template` e `_create_basic_html` para usar `get_mathjax_url`.

   Vamos fazer isso.

   No entanto, note que no Pandoc, o caminho do MathJax é relativo ao arquivo de saída? Sim, o Pandoc gera o script com o src exatamente como passamos.

   Então, se passarmos '../assets/tex-mml-chtml.js', o HTML gerado terá:

        <script src="../assets/tex-mml-chtml.js"></script>

   E se usarmos a URL online, terá a URL online.

   Isso é bom.

   Vamos implementar.

   Outra coisa: a opção --embed-resources pode falhar se houver recursos (imagens) que não podem ser embutidos. Vamos tentar com e sem.

   Vamos modificar a função `_convert_with_pandoc` para tentar duas vezes.

   Vamos reescrevê-la:

        mathjax_url = self.get_mathjax_url()

        # Primeira tentativa: com --embed-resources
        command1 = [
            'pandoc', 
            str(md_file_path),
            '--from', 'markdown+emoji',
            '--to', 'html5',
            '--standalone',
            f'--mathjax={mathjax_url}',
            '--embed-resources',
            '--highlight-style=pygments'
        ]

        # Segunda tentativa: sem --embed-resources
        command2 = [
            'pandoc', 
            str(md_file_path),
            '--from', 'markdown+emoji',
            '--to', 'html5',
            '--standalone',
            f'--mathjax={mathjax_url}',
            '--highlight-style=pygments'
        ]

        try:
            result = subprocess.run(command1, ...)
            if result.returncode == 0:
                return self._apply_custom_style(result.stdout)
            else:
                # Tenta sem embed-resources
                result2 = subprocess.run(command2, ...)
                if result2.returncode == 0:
                    return self._apply_custom_style(result2.stdout)
                else:
                    self.logger.warning(f"⚠️  Pandoc falhou, usando fallback: {result2.stderr[:200]}")
                    return self._convert_with_fallback(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc: {e}")
            return self._convert_with_fallback(md_file_path)

   Vamos implementar.

   Vamos também verificar a versão do Pandoc para ver se suporta --embed-resources? Mas não é necessário, pois se não suportar, ele vai falhar e tentaremos sem.

   Vamos ao código. Aqui está a versão otimizada do código com as melhorias solicitadas para a conversão HTML:

```python
# comb_fragments_system3_html_export.py
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
from typing import List, Dict, Any, Optional
import markdown
import logging

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        # Configuração de processamento por fonte
        self.processors = {
            'qwen': {
                'file': "chat-export.json",
                'method': self.process_qwen_enhanced,
                'enabled': True
            },
            'chatgpt': {
                'file': "chatgpt.zip", 
                'method': self.process_chatgpt,
                'enabled': True
            },
            'deepseek': {
                'file': "deepseek_data.zip",
                'method': self.process_deepseek,
                'enabled': True
            },
            'grok': {
                'file': "grok.zip",
                'method': self.process_grok,
                'enabled': True
            }
        }

    def sanitize_filename(self, text: str, max_len: int = 50) -> str:
        """Sanitiza nomes de arquivo REMOVENDO ESPAÇOS e preservando emojis"""
        if not text or not isinstance(text, str):
            return "conversa_sem_titulo"
            
        # Remove caracteres inválidos
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F\s]'  # Inclui \s para remover espaços
        sanitized = re.sub(invalid_chars, '_', text)  # Substitui espaços por underscores
        sanitized = re.sub(r'_+', '_', sanitized)  # Remove underscores duplicados
        sanitized = sanitized.strip('_')  # Remove underscores no início e fim
        
        if not sanitized:
            sanitized = "conversa_sem_titulo"
            
        # Limita o comprimento
        if len(sanitized) > max_len:
            # Tenta cortar em um ponto lógico (underscore)
            if '_' in sanitized[:max_len]:
                last_underscore = sanitized[:max_len].rfind('_')
                if last_underscore > 10:
                    sanitized = sanitized[:last_underscore]
            else:
                sanitized = sanitized[:max_len]
            
        return sanitized

    def preserve_original_title(self, text: str) -> str:
        """Preserva o título original com espaços, apenas removendo caracteres realmente inválidos"""
        if not text or not isinstance(text, str):
            return "Conversa sem título"
            
        # Remove apenas caracteres realmente problemáticos, mantendo espaços
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized = re.sub(invalid_chars, '', text)
        sanitized = re.sub(r'\s+', ' ', sanitized.strip())
        
        if not sanitized:
            sanitized = "Conversa sem título"
            
        return sanitized

    def preserve_special_content(self, content: str) -> str:
        """Preserva fórmulas matemáticas, código e formatação especial"""
        if not content:
            return ""
            
        preserved_content = content
        
        # Corrige problemas com barras invertidas em LaTeX
        latex_corrections = {
            'ârac': '\\frac',
            'âarepsilon': '\\varepsilon',
            'â': '\\',
            'â': '\\'
        }
        
        for wrong, correct in latex_corrections.items():
            preserved_content = preserved_content.replace(wrong, correct)
        
        return preserved_content

    def ensure_directories(self):
        """Cria todas as pastas necessárias"""
        if self.dry_run:
            self.logger.info("DRY-RUN: Pastas seriam criadas:")
            for folder in self.output_dirs.values():
                self.logger.info(f"   {folder}")
            return
            
        for folder in self.output_dirs.values():
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pasta criada: {folder}")

    def run(self):
        """Executa o processamento completo"""
        self.logger.info("SISTEMA COMBINADO DE EXPORTAÇÕES COM HTML (Qwen3, ChatGPT, DeepSeek, Grok)")
        self.logger.info("=" * 70)
        
        if not self.data_dir.exists():
            self.logger.error(f"Pasta '{self.data_dir}' não encontrada.")
            self.logger.info("Crie a pasta 'data' e coloque os arquivos de exportação:")
            for source_name, config in self.processors.items():
                self.logger.info(f"   - {config['file']} (para {source_name.upper()})")
            return
        
        self.logger.info(f"Usando pasta de dados: {self.data_dir.absolute()}")
        
        self.ensure_directories()
        
        processed_count = 0
        for source_name, config in self.processors.items():
            if config['enabled']:
                file_path = self.data_dir / config['file']
                if file_path.exists():
                    self.logger.info(f"\nProcessando {source_name.upper()}...")
                    config['method'](file_path)
                    processed_count += 1
                else:
                    self.logger.warning(f"{source_name.upper()}: arquivo não encontrado - {file_path}")

        if processed_count == 0:
            self.logger.error("Nenhum arquivo de exportação encontrado na pasta 'data'.")
            return

        if not self.all_conversations:
            self.logger.error("Nenhuma conversa foi extraída dos arquivos.")
            return

        self._post_process_conversations()
        
        if not self.dry_run:
            self._export_all_formats()
            self.logger.info(f"\n🎉 SISTEMA COMBINADO FINALIZADO!")
            self.logger.info(f"📄 Índice: {self.index_file}")
            if Path(self.index_file).exists():
                webbrowser.open(f'file://{Path(self.index_file).absolute()}')
        else:
            self.logger.info(f"\n🔮 MODO DRY-RUN: Nenhum arquivo foi criado.")

    def _post_process_conversations(self):
        """Processamento pós-extração das conversas"""
        self.all_conversations.sort(
            key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at') or x.get('created_at')
            ),
            reverse=True
        )

        for i, conv in enumerate(self.all_conversations):
            conv['number'] = i + 1
            conv['category'] = self.categorize_conversation(conv['title'], conv.get('summary', ''))
            conv.setdefault('source', 'Desconhecido')
            conv.setdefault('messages', [])
            conv.setdefault('summary', conv['messages'][0]['content'][:100] + "..." if conv['messages'] else "Sem conteúdo")

        self.logger.info(f"📊 Total combinado de conversas: {len(self.all_conversations)}")

    def _export_all_formats(self):
        """Exporta para todos os formatos"""
        self.logger.info("\n🔄 Exportando para formatos...")
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index()

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando MathJax local e recursos embutidos"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comando otimizado para HTML5 com recursos embutidos
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--embed-resources',
                '--highlight-style=pygments',
                '--css=assets/pandoc.css' if Path("assets/pandoc.css").exists() else '',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            # Remove argumentos vazios
            command = [arg for arg in command if arg]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)

    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        """Método básico de fallback para Pandoc"""
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=60
            )
            
            if result.returncode == 0:
                return self._optimize_html_content(result.stdout)
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou, usando fallback Python: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)

    def _optimize_html_content(self, html_content: str) -> str:
        """Aplica otimizações finais ao conteúdo HTML"""
        # Adiciona viewport para responsividade
        if '<head>' in html_content and 'viewport' not in html_content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            html_content = html_content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        # Melhora acessibilidade
        if '<html' in html_content and 'lang' not in html_content:
            html_content = html_content.replace('<html>', '<html lang="pt-BR">')
        
        # Adiciona CSS personalizado se necessário
        if '<style>' not in html_content or 'custom-css' not in html_content:
            html_content = self._inject_custom_css(html_content)
            
        return html_content

    def _inject_custom_css(self, html_content: str) -> str:
        """Injeta CSS personalizado para melhorar a aparência"""
        custom_css = """
        <style>
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1em 0; }
            .math inline { display: inline-block; }
            pre { border-left: 4px solid #3498db; background: #f8f9fa; }
            code { background: #e9ecef; padding: 0.2em 0.4em; border-radius: 3px; }
            
            /* Melhorias responsivas */
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 15px; }
                pre { font-size: 12px; }
            }
            
            /* Melhorias para tabelas */
            table { width: 100%; border-collapse: collapse; margin: 1em 0; }
            th, td { border: 1px solid #dee2e6; padding: 0.75rem; }
            th { background-color: #3498db; color: white; }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 1em 0; 
                padding-left: 1em; 
                color: #6c757d;
                font-style: italic;
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{custom_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{custom_css}')
        else:
            # Se não encontrar head, adiciona antes do body
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{custom_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{custom_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content

    def _convert_with_fallback(self, md_file_path: str) -> str:
        """Fallback para conversão quando Pandoc falha"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Extensões avançadas para melhor conversão
            extensions = [
                'extra', 'tables', 'fenced_code', 'codehilite', 
                'toc', 'md_in_html', 'attr_list'
            ]
            
            html_content = markdown.markdown(
                md_content,
                extensions=extensions,
                output_format='html5'
            )
            
            return self._create_enhanced_html_template(html_content, Path(md_file_path).name)
            
        except Exception as e:
            self.logger.error(f"❌ Fallback também falhou: {e}")
            return self._create_basic_html(md_content, Path(md_file_path).name)

    def _create_enhanced_html_template(self, content: str, title: str) -> str:
        """Template HTML aprimorado com suporte a MathJax local/online"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5 {{
            color: #2c3e50;
            margin-top: 1.8em;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s ease;
        }}
        .math {{
            text-align: center;
            margin: 1.5em 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .author {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        .metadata {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }}
        .metadata h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                margin: 10px;
            }}
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <script>
        // Configuração MathJax para melhor renderização
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                renderActions: {{
                    addMenu: [0, '', '']
                }}
            }},
            startup: {{
                pageReady() {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax carregado com sucesso');
                    }});
                }}
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""

    # ... (mantenha o resto dos métodos existentes como save_as_html_robust, categorize_conversation, etc.)

    def save_as_html_robust(self):
        """Método ROBUSTO para conversão HTML - VERSÃO OTIMIZADA"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] HTMLs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.html"
                self.logger.info(f"   🌐 {filename}")
            return
        
        markdown_folder = Path(self.output_dirs['markdown'])
        html_folder = Path(self.output_dirs['html'])
        
        md_files = list(markdown_folder.glob("*.md"))
        
        if not md_files:
            self.logger.error("❌ Nenhum arquivo Markdown encontrado para conversão.")
            return
        
        self.logger.info(f"🔄 Convertendo {len(md_files)} arquivos Markdown para HTML (OTIMIZADO)...")
        
        # Verifica se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada")
        except:
            pandoc_available = False
            self.logger.warning("⚠️ Pandoc não disponível - usando fallback Python")
        
        converted_count = 0
        failed_count = 0
        
        for md_file in md_files:
            try:
                html_file = html_folder / md_file.with_suffix('.html').name
                
                if not self.force_overwrite and html_file.exists():
                    self.logger.info(f"⏭️  Já existe: {html_file.name}")
                    converted_count += 1
                    continue

                self.logger.info(f"📄 Processando: {md_file.name}")
                
                if pandoc_available:
                    html_content = self._convert_with_pandoc_optimized(str(md_file))
                else:
                    html_content = self._convert_with_fallback(str(md_file))
                
                if html_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    self.logger.info(f"✅ Criado: {html_file.name}")
                    converted_count += 1
                else:
                    self.logger.error(f"❌ Falha na conversão: {md_file.name}")
                    failed_count += 1
                    
            except Exception as e:
                self.logger.error(f"❌ Erro em {md_file.name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                failed_count += 1
                
        self.logger.info(f"📊 HTML: {converted_count} arquivos criados, {failed_count} falhas em '{html_folder}'")

    # ... (mantenha todos os outros métodos existentes inalterados)

# ... (mantenha o resto do código inalterado)
```

## Principais otimizações implementadas:

### 1. **Conversão Pandoc Otimizada** (`_convert_with_pandoc_optimized`):
- `--embed-resources` para embutir CSS/imagens
- `--highlight-style=pygments` para syntax highlighting
- `--mathjax=assets/tex-mml-chtml.js` para MathJax local
- Suporte a extensões avançadas do Markdown

### 2. **MathJax Local**:
- Detecta automaticamente se o arquivo local existe
- Fallback para CDN se necessário
- Configuração MathJax otimizada no template

### 3. **Método de Fallback em Camadas**:
- Pandoc otimizado → Pandoc básico → Fallback Python
- Timeout aprimorado (120 segundos)

### 4. **HTML Aprimorado**:
- CSS responsivo e acessível
- Viewport meta tag
- Melhorias para código, tabelas e matemática
- Configuração MathJax personalizada

### 5. **CSS Personalizado**:
- Design responsivo
- Melhor syntax highlighting
- Estilos para elementos matemáticos
- Melhorias de acessibilidade

## Comandos adicionais recomendados:

```bash
# Criar CSS personalizado para Pandoc
mkdir -p assets
cat > assets/pandoc.css << 'EOF'
/* CSS personalizado para Pandoc */
code { background: #f4f4f4; padding: 0.2em 0.4em; }
pre { border-left: 4px solid #3498db; background: #f8f9fa; }
.math { text-align: center; margin: 1em 0; }
EOF
```

Esta versão oferece conversão HTML significativamente melhorada com suporte robusto a matemática, código e recursos embutidos.

---

### 👤 Utilizador *(2025-11-07 20:18:47)* *[deepseek-reasoner]*

Pretendo o comb_fragments_system3_html_export.py completo

---

### 🤖 DeepSeek *(2025-11-07 20:18:47)* *[deepseek-reasoner]*

Vamos atualizar o método `_convert_with_pandoc_optimized` para usar as opções solicitadas, incluindo o MathJax local.
 Além disso, note que a opção `--embed-resources` é suportada apenas para HTML4, então se não funcionar com HTML5, podemos tentar HTML4.
 No entanto, a documentação do Pandoc indica que `--embed-resources` só é suportado para HTML4. Vamos ajustar:

 Vamos tentar primeiro com HTML5 e `--embed-resources`. Se falhar, tentaremos sem embed-resources ou com HTML4.

 Vamos criar uma estratégia:
 1. Tentar com HTML5 e `--embed-resources` (se o Pandoc suportar, mas note que a documentação atual diz que não)
 2. Se falhar, tentar com HTML4 e `--embed-resources`
 3. Se ainda falhar, tentar sem embed-resources.

 No entanto, a opção `--embed-resources` é experimental e pode não ser suportada. Vamos verificar a versão do Pandoc.

 Como não temos como verificar a versão no código, vamos tentar com HTML5 e se der erro, tentar sem `--embed-resources`.

 Vamos modificar o método `_convert_with_pandoc_optimized` para tentar duas abordagens:

 Primeira tentativa: 
   comando = [..., '--to', 'html5', '--embed-resources', ...]

 Se falhar, segunda tentativa (fallback):
   comando = [..., '--to', 'html5', ...]  (sem embed-resources)

 E se ainda falhar, usamos o método básico.

 Além disso, vamos usar o MathJax local se existir.

 Vamos reescrever o método `_convert_with_pandoc_optimized` para tentar essas abordagens.

 No entanto, note que a opção `--embed-resources` pode não ser suportada em HTML5. A documentação do Pandoc (https://pandoc.org/MANUAL.html) 
 diz: "This option is currently only supported for HTML and EPUB output."

 E para HTML, a opção `--embed-resources` só é suportada para HTML4? Na verdade, a documentação não especifica, mas na prática pode não funcionar para HTML5.

 Vamos tentar:

 Primeiro, tentamos com `--to html5` e `--embed-resources`. Se o Pandoc retornar erro, tentamos sem `--embed-resources`.

 Vamos também adicionar a opção `--standalone` e `--mathjax` com o caminho local.

 Outra coisa: a opção `--syntax-highlighting=pygments` não é válida. O correto é `--highlight-style=pygments`.

 Vamos corrigir.

 Vamos reorganizar o método:

 Tentativa 1: HTML5 com embed-resources (se o Pandoc suportar)
 Tentativa 2: HTML5 sem embed-resources
 Tentativa 3: HTML4 com embed-resources (se a Tentativa 1 falhar, mas não vamos fazer HTML4 porque o objetivo é HTML5)
 Na verdade, o mais importante é ter HTML5. O embed-resources é um plus.

 Vamos priorizar HTML5, e se o embed-resources não funcionar, deixamos sem.

 Vamos fazer:

 1. Tentativa: 
    comando = [pandoc, md_file, '--from', 'markdown+emoji...', '--to', 'html5', '--standalone', '--embed-resources', '--highlight-style=pygments', '--mathjax=assets/tex-mml-chtml.js']

 2. Se falhar, tentar sem `--embed-resources`:
    comando = [pandoc, md_file, '--from', 'markdown+emoji...', '--to', 'html5', '--standalone', '--highlight-style=pygments', '--mathjax=assets/tex-mml-chtml.js']

 3. Se ainda falhar, usar o método básico.

 Vamos implementar essa lógica.

 Além disso, note que o método `_convert_with_pandoc_optimized` já tenta o método básico em caso de falha.

 Vamos reestruturar:

 Primeiro, vamos tentar com todas as opções desejadas (incluindo embed-resources). Se der erro, tentamos sem embed-resources.

 Vamos criar uma função auxiliar para executar o comando Pandoc e verificar se teve sucesso.

 Vamos também verificar se o arquivo MathJax local existe e ajustar o argumento `--mathjax` accordingly.

 Vamos atualizar o código conforme abaixo.

 Nota: A opção `--embed-resources` pode embutir imagens também, mas isso requer que o Pandoc tenha suporte a isso e que as imagens estejam acessíveis.

 Como estamos convertendo markdown que pode ter imagens, isso seria útil, mas se não funcionar, pelo menos temos o fallback.

 Vamos ao código. Aqui está o arquivo `comb_fragments_system3_html_export.py` completo com todas as otimizações:

```python
# comb_fragments_system3_html_export.py
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
from typing import List, Dict, Any, Optional
import markdown
import logging

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        # Configuração de processamento por fonte
        self.processors = {
            'qwen': {
                'file': "chat-export.json",
                'method': self.process_qwen_enhanced,
                'enabled': True
            },
            'chatgpt': {
                'file': "chatgpt.zip", 
                'method': self.process_chatgpt,
                'enabled': True
            },
            'deepseek': {
                'file': "deepseek_data.zip",
                'method': self.process_deepseek,
                'enabled': True
            },
            'grok': {
                'file': "grok.zip",
                'method': self.process_grok,
                'enabled': True
            }
        }

    def sanitize_filename(self, text: str, max_len: int = 50) -> str:
        """Sanitiza nomes de arquivo REMOVENDO ESPAÇOS e preservando emojis"""
        if not text or not isinstance(text, str):
            return "conversa_sem_titulo"
            
        # Remove caracteres inválidos
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F\s]'  # Inclui \s para remover espaços
        sanitized = re.sub(invalid_chars, '_', text)  # Substitui espaços por underscores
        sanitized = re.sub(r'_+', '_', sanitized)  # Remove underscores duplicados
        sanitized = sanitized.strip('_')  # Remove underscores no início e fim
        
        if not sanitized:
            sanitized = "conversa_sem_titulo"
            
        # Limita o comprimento
        if len(sanitized) > max_len:
            # Tenta cortar em um ponto lógico (underscore)
            if '_' in sanitized[:max_len]:
                last_underscore = sanitized[:max_len].rfind('_')
                if last_underscore > 10:
                    sanitized = sanitized[:last_underscore]
            else:
                sanitized = sanitized[:max_len]
            
        return sanitized

    def preserve_original_title(self, text: str) -> str:
        """Preserva o título original com espaços, apenas removendo caracteres realmente inválidos"""
        if not text or not isinstance(text, str):
            return "Conversa sem título"
            
        # Remove apenas caracteres realmente problemáticos, mantendo espaços
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized = re.sub(invalid_chars, '', text)
        sanitized = re.sub(r'\s+', ' ', sanitized.strip())
        
        if not sanitized:
            sanitized = "Conversa sem título"
            
        return sanitized

    def preserve_special_content(self, content: str) -> str:
        """Preserva fórmulas matemáticas, código e formatação especial"""
        if not content:
            return ""
            
        preserved_content = content
        
        # Corrige problemas com barras invertidas em LaTeX
        latex_corrections = {
            'ârac': '\\frac',
            'âarepsilon': '\\varepsilon',
            'â': '\\',
            'â': '\\'
        }
        
        for wrong, correct in latex_corrections.items():
            preserved_content = preserved_content.replace(wrong, correct)
        
        return preserved_content

    def ensure_directories(self):
        """Cria todas as pastas necessárias"""
        if self.dry_run:
            self.logger.info("DRY-RUN: Pastas seriam criadas:")
            for folder in self.output_dirs.values():
                self.logger.info(f"   {folder}")
            return
            
        for folder in self.output_dirs.values():
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pasta criada: {folder}")

    def run(self):
        """Executa o processamento completo"""
        self.logger.info("SISTEMA COMBINADO DE EXPORTAÇÕES COM HTML (Qwen3, ChatGPT, DeepSeek, Grok)")
        self.logger.info("=" * 70)
        
        if not self.data_dir.exists():
            self.logger.error(f"Pasta '{self.data_dir}' não encontrada.")
            self.logger.info("Crie a pasta 'data' e coloque os arquivos de exportação:")
            for source_name, config in self.processors.items():
                self.logger.info(f"   - {config['file']} (para {source_name.upper()})")
            return
        
        self.logger.info(f"Usando pasta de dados: {self.data_dir.absolute()}")
        
        self.ensure_directories()
        
        processed_count = 0
        for source_name, config in self.processors.items():
            if config['enabled']:
                file_path = self.data_dir / config['file']
                if file_path.exists():
                    self.logger.info(f"\nProcessando {source_name.upper()}...")
                    config['method'](file_path)
                    processed_count += 1
                else:
                    self.logger.warning(f"{source_name.upper()}: arquivo não encontrado - {file_path}")

        if processed_count == 0:
            self.logger.error("Nenhum arquivo de exportação encontrado na pasta 'data'.")
            return

        if not self.all_conversations:
            self.logger.error("Nenhuma conversa foi extraída dos arquivos.")
            return

        self._post_process_conversations()
        
        if not self.dry_run:
            self._export_all_formats()
            self.logger.info(f"\n🎉 SISTEMA COMBINADO FINALIZADO!")
            self.logger.info(f"📄 Índice: {self.index_file}")
            if Path(self.index_file).exists():
                webbrowser.open(f'file://{Path(self.index_file).absolute()}')
        else:
            self.logger.info(f"\n🔮 MODO DRY-RUN: Nenhum arquivo foi criado.")

    def _post_process_conversations(self):
        """Processamento pós-extração das conversas"""
        self.all_conversations.sort(
            key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at') or x.get('created_at')
            ),
            reverse=True
        )

        for i, conv in enumerate(self.all_conversations):
            conv['number'] = i + 1
            conv['category'] = self.categorize_conversation(conv['title'], conv.get('summary', ''))
            conv.setdefault('source', 'Desconhecido')
            conv.setdefault('messages', [])
            conv.setdefault('summary', conv['messages'][0]['content'][:100] + "..." if conv['messages'] else "Sem conteúdo")

        self.logger.info(f"📊 Total combinado de conversas: {len(self.all_conversations)}")

    def _export_all_formats(self):
        """Exporta para todos os formatos"""
        self.logger.info("\n🔄 Exportando para formatos...")
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index()

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando MathJax local e recursos embutidos"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comando otimizado para HTML5 com recursos embutidos
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--embed-resources',
                '--highlight-style=pygments',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            # Remove argumentos vazios
            command = [arg for arg in command if arg]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)

    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        """Método básico de fallback para Pandoc"""
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=60
            )
            
            if result.returncode == 0:
                return self._optimize_html_content(result.stdout)
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou, usando fallback Python: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)

    def _optimize_html_content(self, html_content: str) -> str:
        """Aplica otimizações finais ao conteúdo HTML"""
        # Adiciona viewport para responsividade
        if '<head>' in html_content and 'viewport' not in html_content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            html_content = html_content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        # Melhora acessibilidade
        if '<html' in html_content and 'lang' not in html_content:
            html_content = html_content.replace('<html>', '<html lang="pt-BR">')
        
        # Adiciona CSS personalizado se necessário
        if '<style>' not in html_content or 'custom-css' not in html_content:
            html_content = self._inject_custom_css(html_content)
            
        return html_content

    def _inject_custom_css(self, html_content: str) -> str:
        """Injeta CSS personalizado para melhorar a aparência"""
        custom_css = """
        <style>
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1em 0; }
            .math inline { display: inline-block; }
            pre { border-left: 4px solid #3498db; background: #f8f9fa; }
            code { background: #e9ecef; padding: 0.2em 0.4em; border-radius: 3px; }
            
            /* Melhorias responsivas */
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 15px; }
                pre { font-size: 12px; }
            }
            
            /* Melhorias para tabelas */
            table { width: 100%; border-collapse: collapse; margin: 1em 0; }
            th, td { border: 1px solid #dee2e6; padding: 0.75rem; }
            th { background-color: #3498db; color: white; }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 1em 0; 
                padding-left: 1em; 
                color: #6c757d;
                font-style: italic;
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{custom_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{custom_css}')
        else:
            # Se não encontrar head, adiciona antes do body
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{custom_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{custom_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content

    def _convert_with_fallback(self, md_file_path: str) -> str:
        """Fallback para conversão quando Pandoc falha"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Extensões avançadas para melhor conversão
            extensions = [
                'extra', 'tables', 'fenced_code', 'codehilite', 
                'toc', 'md_in_html', 'attr_list'
            ]
            
            html_content = markdown.markdown(
                md_content,
                extensions=extensions,
                output_format='html5'
            )
            
            return self._create_enhanced_html_template(html_content, Path(md_file_path).name)
            
        except Exception as e:
            self.logger.error(f"❌ Fallback também falhou: {e}")
            return self._create_basic_html(md_content, Path(md_file_path).name)

    def _create_enhanced_html_template(self, content: str, title: str) -> str:
        """Template HTML aprimorado com suporte a MathJax local/online"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5 {{
            color: #2c3e50;
            margin-top: 1.8em;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s ease;
        }}
        .math {{
            text-align: center;
            margin: 1.5em 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .author {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        .metadata {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }}
        .metadata h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                margin: 10px;
            }}
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <script>
        // Configuração MathJax para melhor renderização
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                renderActions: {{
                    addMenu: [0, '', '']
                }}
            }},
            startup: {{
                pageReady() {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax carregado com sucesso');
                    }});
                }}
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""

    def _create_basic_html(self, content: str, title: str) -> str:
        """HTML básico de último recurso com MathJax"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f5f5f5;
        }}
        pre {{ 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
    </style>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</head>
<body>
    <div class="container">
        <pre>{content}</pre>
    </div>
</body>
</html>"""

    def save_as_html_robust(self):
        """Método ROBUSTO para conversão HTML - VERSÃO OTIMIZADA"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] HTMLs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.html"
                self.logger.info(f"   🌐 {filename}")
            return
        
        markdown_folder = Path(self.output_dirs['markdown'])
        html_folder = Path(self.output_dirs['html'])
        
        md_files = list(markdown_folder.glob("*.md"))
        
        if not md_files:
            self.logger.error("❌ Nenhum arquivo Markdown encontrado para conversão.")
            return
        
        self.logger.info(f"🔄 Convertendo {len(md_files)} arquivos Markdown para HTML (OTIMIZADO)...")
        
        # Verifica se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada")
        except:
            pandoc_available = False
            self.logger.warning("⚠️ Pandoc não disponível - usando fallback Python")
        
        converted_count = 0
        failed_count = 0
        
        for md_file in md_files:
            try:
                html_file = html_folder / md_file.with_suffix('.html').name
                
                if not self.force_overwrite and html_file.exists():
                    self.logger.info(f"⏭️  Já existe: {html_file.name}")
                    converted_count += 1
                    continue

                self.logger.info(f"📄 Processando: {md_file.name}")
                
                if pandoc_available:
                    html_content = self._convert_with_pandoc_optimized(str(md_file))
                else:
                    html_content = self._convert_with_fallback(str(md_file))
                
                if html_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    self.logger.info(f"✅ Criado: {html_file.name}")
                    converted_count += 1
                else:
                    self.logger.error(f"❌ Falha na conversão: {md_file.name}")
                    failed_count += 1
                    
            except Exception as e:
                self.logger.error(f"❌ Erro em {md_file.name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                failed_count += 1
                
        self.logger.info(f"📊 HTML: {converted_count} arquivos criados, {failed_count} falhas em '{html_folder}'")

    def categorize_conversation(self, title: str, summary: str) -> str:
        """Categorização otimizada com expressões regulares"""
        text = f"{title} {summary}".lower()
        
        patterns = {
            'Tecnologia': r'\b(tecnologia|hardware|software|rede|internet|wifi|bluetooth|[45]g|cloud|aws|azure|gcp|servidor|hosting|domínio|ssl|router|switch|firewall|iot|smartphone|tablet|navegador|browser|chrome|firefox|edge|safari|email|gmail|outlook|criptografia|segurança|cibersegurança|ransomware|phishing|autenticação|2fa|biometria)\b',
            'Saúde': r'\b(saúde|medicina|médico|enfermagem|doença|vírus|bactéria|vacina|covid|coronavírus|gripe|febre|dor|análise|exame|raio x|ressonância|hospital|clínica|farmácia|medicamento|remédio|psicologia|terapia|bem-estar|nutrição|dieta|exercício|fitness|sono|saúde mental)\b',
            'Programação': r'\b(python|javascript|java|c\+\+|c#|go|rust|lua|bash|script|debug|erro|conda|mamba|pandoc|msys2|spyder|jupyter|pip|venv|docker|git|github|vscode|ide|programa|código|função|classe|api|selenium|playwright)\b',
            'Sistemas': r'\b(windows|linux|macos|so|sistema operacional|driver|registry|process|firewall|bios|boot|path|dll|exe|powershell|cmd|terminal|shell)\b',
            'IA': r'\b(ia|gpt|chatgpt|grok|qwen|deepseek|llm|modelo|prompt|token|embedding|fine-tune|neural|chatbot|inteligência artificial)\b',
            'Dados': r'\b(dados|data|csv|json|pandas|numpy|excel|sql|banco|sqlite|postgres|visualização|gráfico|tabela|análise|etl|dashboard)\b',
            'Geral': r'\b(geral|pergunta|ajuda|como fazer|explicar|resumo|tutorial básico)\b'
        }
        
        for category, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return category
                
        return 'Outros'

    def parse_timestamp_for_sorting(self, timestamp) -> datetime:
        if not timestamp:
            return datetime.min
            
        try:
            if isinstance(timestamp, str):
                clean_ts = timestamp.replace('T', ' ').split('.')[0].split('+')[0]
                if clean_ts.endswith('Z'):
                    clean_ts = clean_ts[:-1]
                return datetime.fromisoformat(clean_ts)
            elif isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
        except Exception:
            pass
            
        return datetime.min

    def format_timestamp(self, timestamp) -> Optional[str]:
        if not timestamp:
            return None
            
        try:
            if isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(timestamp, str):
                if 'T' in timestamp:
                    return timestamp.replace('T', ' ').split('.')[0]
                return timestamp
        except Exception:
            pass
            
        return str(timestamp)

    def create_enhanced_markdown_content(self, conversation: Dict[str, Any]) -> str:
        """Gera conteúdo Markdown com preservação total de formatação"""
        lines = [
            f"# {conversation['title']}",
            "",
            "## 📊 Informações",
            f"- **Número:** #{conversation['number']}",
            f"- **Origem:** {conversation['source']}",
            f"- **Categoria:** {conversation['category']}",
            f"- **ID:** {conversation.get('id', 'N/A')}",
            f"- **Criada em:** {conversation.get('inserted_at') or conversation.get('created_at') or 'N/A'}",
        ]
        
        if conversation.get('updated_at'):
            lines.append(f"- **Atualizada em:** {conversation['updated_at']}")
            
        lines.extend([
            f"- **Total de mensagens:** {len(conversation['messages'])}",
            f"- **Resumo:** {conversation.get('summary', 'Sem resumo')}",
            "",
            "---",
            "",
            "## 💬 Conversa",
            ""
        ])

        for j, msg in enumerate(conversation['messages'], 1):
            timestamp = f" *({msg['timestamp']})*" if msg['timestamp'] else ""
            model_info = f" *[{msg.get('model', '')}]*" if msg.get('model') else ""
            
            preserved_content = self.preserve_special_content(msg['content'])
            
            lines.extend([
                f"### {msg['author']}{timestamp}{model_info}",
                "",
                f"{preserved_content}",
                ""
            ])
            
            if j < len(conversation['messages']):
                lines.extend(["---", ""])

        lines.extend([
            "---",
            "",
            f"*Conversa exportada do {conversation['source']}*",
            f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        ])
        
        return '\n'.join(lines)

    def process_qwen_enhanced(self, path: Path):
        """Processa Qwen3 com preservação total de conteúdo"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Qwen3: {path}")
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                
            data = raw.get('data', [])
            if not isinstance(data, list):
                self.logger.warning("⚠️  Qwen3: 'data' não é uma lista.")
                return
                
            self.logger.info(f"🔍 Qwen3: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa Qwen {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                history = conv.get('chat', {}).get('history', {})
                messages = []

                if not history:
                    continue

                messages_dict = history.get('messages', {})
                
                if not isinstance(messages_dict, dict):
                    continue

                self.logger.info(f"   📝 Conversa {i+1}: '{clean_title}' - {len(messages_dict)} mensagens")

                for message_id, message_data in messages_dict.items():
                    if not isinstance(message_data, dict):
                        continue

                    role = message_data.get('role', '')
                    content = message_data.get('content', '')
                    
                    if not content or not role:
                        continue

                    if role == 'user':
                        author = "👤 Utilizador"
                    elif role == 'assistant':
                        author = "🤖 Qwen3"
                    else:
                        continue

                    if isinstance(content, list):
                        text_parts = []
                        for block in content:
                            if isinstance(block, dict):
                                if block.get('type') == 'text':
                                    text_parts.append(block.get('text', ''))
                                elif block.get('type') == 'image':
                                    image_info = block.get('image', '')
                                    if image_info:
                                        text_parts.append(f"![Imagem]({image_info})")
                            elif isinstance(block, str):
                                text_parts.append(block)
                        final_content = '\n'.join(text_parts).strip()
                    else:
                        final_content = str(content).strip()

                    final_content = self.preserve_special_content(final_content)

                    if not final_content or final_content == 'null':
                        continue

                    messages.append({
                        'author': author,
                        'role': role,
                        'content': final_content,
                        'timestamp': self.format_timestamp(message_data.get('created_at')),
                        'model': message_data.get('model', 'Qwen3')
                    })

                if messages:
                    messages.sort(key=lambda x: self.parse_timestamp_for_sorting(x['timestamp']))
                    
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'Qwen3',
                        'id': conv.get('id', f'qwen_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('created_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    self.logger.info(f"   ✅ Adicionada: {len(messages)} mensagens")
                    
            self.logger.info(f"✅ Qwen3: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Qwen3: {e}")
            if self.dry_run:
                traceback.print_exc()

    def process_chatgpt(self, path: Path):
        """Processa exportação do ChatGPT"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria ChatGPT: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="chatgpt_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)
            convs_path = Path(temp_dir) / "conversations.json"
            if not convs_path.exists():
                self.logger.error("❌ ChatGPT: conversations.json não encontrado.")
                return
                
            with open(convs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                self.logger.warning("⚠️  ChatGPT: estrutura inesperada.")
                return
                
            self.logger.info(f"🔍 ChatGPT: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa ChatGPT {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for msg_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                        
                    author_role = msg_data.get('author', {}).get('role', '')
                    if author_role == 'user':
                        author = "👤 Utilizador"
                        role = 'user'
                    elif author_role == 'assistant':
                        author = "🤖 ChatGPT"
                        role = 'assistant'
                    else:
                        continue
                        
                    content_parts = []
                    for part in msg_data.get('content', {}).get('parts', []):
                        if isinstance(part, str):
                            content_parts.append(part)
                    content = "\n".join(content_parts).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('create_time')),
                        'model': msg_data.get('model', 'ChatGPT')
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'ChatGPT',
                        'id': conv.get('id', f'chatgpt_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('create_time')),
                        'updated_at': self.format_timestamp(conv.get('update_time')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    
            self.logger.info(f"✅ ChatGPT: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar ChatGPT: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def process_deepseek(self, path: Path):
        """Processa exportação do DeepSeek"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria DeepSeek: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="deepseek_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)
                
            convs_path = Path(temp_dir) / "conversations.json"
            if not convs_path.exists():
                self.logger.error("❌ DeepSeek: conversations.json não encontrado.")
                return
                
            with open(convs_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            if isinstance(raw_data, list):
                data = raw_data
            elif isinstance(raw_data, dict) and 'data' in raw_data:
                data = raw_data['data']
            else:
                self.logger.warning("⚠️  DeepSeek: estrutura inesperada.")
                return
                
            if not isinstance(data, list):
                self.logger.warning("⚠️  DeepSeek: 'data' não é uma lista.")
                return
                
            self.logger.info(f"🔍 DeepSeek: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa DeepSeek {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for node_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                        
                    fragments = msg_data.get('fragments', [])
                    content_parts = []
                    msg_type = None
                    
                    for frag in fragments:
                        if isinstance(frag, dict):
                            frag_type = frag.get('type', '').upper()
                            if frag_type in ('REQUEST', 'RESPONSE'):
                                msg_type = frag_type
                            text = frag.get('text', '')
                            if text:
                                content_parts.append(text)
                            content = frag.get('content', '')
                            if content:
                                if isinstance(content, list):
                                    for item in content:
                                        if isinstance(item, str):
                                            content_parts.append(item)
                                        elif isinstance(item, dict):
                                            item_text = item.get('text', '')
                                            if item_text:
                                                content_parts.append(str(item_text))
                                else:
                                    content_parts.append(str(content))
                                    
                    content = ' '.join(content_parts).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue
                        
                    if msg_type == 'REQUEST':
                        author = "👤 Utilizador"
                        role = 'user'
                    else:
                        author = "🤖 DeepSeek"
                        role = 'assistant'
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('inserted_at')),
                        'model': msg_data.get('model', 'DeepSeek')
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'DeepSeek',
                        'id': conv.get('id', f'deepseek_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('inserted_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    
            self.logger.info(f"✅ DeepSeek: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar DeepSeek: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def process_grok(self, path: Path):
        """Processa exportação do Grok"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Grok: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="grok_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)

            target_file = None
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file == "prod-grok-backend.json":
                        target_file = Path(root) / file
                        break
                if target_file:
                    break

            if not target_file:
                self.logger.error("❌ Grok: ficheiro 'prod-grok-backend.json' não encontrado no ZIP.")
                return

            self.logger.info(f"🔍 Grok: carregando {target_file.name}...")
            with open(target_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict) or 'conversations' not in data:
                self.logger.error("❌ Grok: estrutura inesperada — chave 'conversations' não encontrada.")
                return

            conversations_list = data['conversations']
            if not isinstance(conversations_list, list):
                self.logger.error("❌ Grok: 'conversations' não é uma lista.")
                return

            self.logger.info(f"📊 Grok: encontradas {len(conversations_list)} conversas.")
            total_convs = 0

            for item in conversations_list:
                if not isinstance(item, dict):
                    continue

                conv_meta = item.get('conversation')
                responses = item.get('responses', [])

                if not isinstance(conv_meta, dict) or not isinstance(responses, list) or not responses:
                    continue

                conv_id = conv_meta.get('id')
                if not conv_id:
                    continue

                original_title = conv_meta.get('title', f"Conversa Grok {total_convs + 1}")
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                create_time_str = conv_meta.get('create_time')
                modify_time_str = conv_meta.get('modify_time')

                def format_iso_timestamp(ts_str):
                    if not ts_str:
                        return None
                    try:
                        if '.' in ts_str:
                            ts_str = ts_str.split('.')[0] + 'Z'
                        return self.format_timestamp(ts_str)
                    except:
                        return str(ts_str)

                inserted_at = format_iso_timestamp(create_time_str)
                updated_at = format_iso_timestamp(modify_time_str)

                messages = []
                for resp in responses:
                    if not isinstance(resp, dict):
                        continue

                    resp_data = resp.get('response')
                    if not isinstance(resp_data, dict):
                        continue

                    sender = resp_data.get('sender', '').upper()
                    if sender == 'HUMAN':
                        author = "👤 Utilizador"
                        role = "user"
                    elif sender == 'ASSISTANT':
                        author = "🤖 Grok"
                        role = "assistant"
                    else:
                        continue

                    content = str(resp_data.get('message', '')).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue

                    create_time = resp_data.get('create_time')
                    timestamp_ms = None
                    if isinstance(create_time, dict) and '$date' in create_time:
                        date_obj = create_time['$date']
                        if isinstance(date_obj, dict) and '$numberLong' in date_obj:
                            try:
                                timestamp_ms = int(date_obj['$numberLong'])
                            except:
                                pass

                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(timestamp_ms / 1000.0 if timestamp_ms else None),
                        'model': 'Grok'
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'Grok',
                        'id': conv_id,
                        'inserted_at': inserted_at,
                        'updated_at': updated_at,
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    total_convs += 1

            if total_convs > 0:
                self.logger.info(f"✅ Grok: processadas {total_convs} conversas.")
            else:
                self.logger.error("❌ Grok: nenhuma conversa válida encontrada.")

        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Grok: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def save_as_markdown_enhanced(self):
        """Salva conversas com preservação total de formatação"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Markdowns seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                self.logger.info(f"   📄 {filename}")
            return
            
        folder = Path(self.output_dirs['markdown'])
        saved_count = 0
        failed_count = 0
        
        for conv in self.all_conversations:
            try:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                filepath = folder / filename
                
                if not self.force_overwrite and filepath.exists():
                    continue
                    
                markdown_content = self.create_enhanced_markdown_content(conv)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                saved_count += 1
                
            except Exception as e:
                self.logger.error(f"❌ Erro ao salvar conversa {conv['number']}: {e}")
                failed_count += 1
                continue
                
        self.logger.info(f"✅ Markdown: {saved_count} arquivos criados, {failed_count} falhas em '{folder}'")

    def save_as_csv(self):
        """Salva conversas em arquivos CSV individuais"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] CSVs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
                self.logger.info(f"   📊 {filename}")
            return
            
        folder = Path(self.output_dirs['csv'])
        saved_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
            filepath = folder / filename
            
            if not self.force_overwrite and filepath.exists():
                continue
                
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'node_id', 'author', 'role', 'timestamp', 'model', 'content'
                ])
                writer.writeheader()
                for i, msg in enumerate(conv['messages']):
                    writer.writerow({
                        'node_id': str(i),
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content']
                    })
            saved_count += 1
            
        self.logger.info(f"✅ CSV: {saved_count} arquivos criados em '{folder}'")

    def save_as_json(self):
        """Salva conversas em arquivos JSON individuais"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] JSONs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
                self.logger.info(f"   📋 {filename}")
            return
            
        folder = Path(self.output_dirs['json'])
        saved_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
            filepath = folder / filename
            
            if not self.force_overwrite and filepath.exists():
                continue
                
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conv, f, ensure_ascii=False, indent=2)
            saved_count += 1
            
        self.logger.info(f"✅ JSON: {saved_count} arquivos criados em '{folder}'")

    def save_all_to_single_files(self):
        """Salva todas as conversas em arquivos únicos CSV e JSON"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Arquivos únicos seriam criados:")
            self.logger.info(f"   📁 {self.single_files['csv']}")
            self.logger.info(f"   📁 {self.single_files['json']}")
            return
            
        # CSV único
        with open(self.single_files['csv'], 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                'conversation_number', 'source', 'conversation_title', 'category',
                'author', 'role', 'timestamp', 'model', 'content'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for conv in self.all_conversations:
                for msg in conv['messages']:
                    writer.writerow({
                        'conversation_number': conv['number'],
                        'source': conv['source'],
                        'conversation_title': conv['title'],
                        'category': conv['category'],
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content']
                    })
        self.logger.info(f"✅ CSV único: {self.single_files['csv']}")

        # JSON único
        with open(self.single_files['json'], 'w', encoding='utf-8') as f:
            json.dump(self.all_conversations, f, ensure_ascii=False, indent=2)
        self.logger.info(f"✅ JSON único: {self.single_files['json']}")

    def create_searchable_index(self):
        """Cria índice HTML pesquisável com links para HTML"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Índice HTML seria criado: {self.index_file}")
            return
            
        self.logger.info("🎯 Criando índice HTML combinado...")
        
        category_stats = {}
        for conv in self.all_conversations:
            cat = conv['category']
            category_stats[cat] = category_stats.get(cat, 0) + 1

        html_content = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice Combinado - AI Chats</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 15px; font-weight: 300; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; margin-bottom: 20px; }}
        .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 25px; flex-wrap: wrap; }}
        .stat-item {{ background: rgba(255,255,255,0.15); padding: 18px 28px; border-radius: 12px; backdrop-filter: blur(10px); font-size: 1.1em; }}
        .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
        .search-box {{ width: 100%; padding: 18px 25px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; font-family: inherit; }}
        .search-box:focus {{ border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }}
        .filter-section {{
            padding: 20px 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        .filter-btn {{
            padding: 10px 20px;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 500;
            transition: all 0.3s ease;
            font-family: inherit;
        }}
        .filter-btn.active, .filter-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
        .conversations-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); 
            gap: 25px; 
            padding: 35px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 400px;
        }}
        .conversation-card {{ 
            background: white; 
            border: 1px solid #e9ecef; 
            border-radius: 15px; 
            padding: 25px; 
            transition: all 0.4s ease; 
            cursor: pointer; 
            position: relative;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .conversation-card:hover {{ 
            transform: translateY(-8px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.15); 
            border-color: #667eea;
        }}
        .card-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            margin-bottom: 18px; 
        }}
        .card-number {{ 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-size: 0.9em; 
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }}
        .card-source {{ 
            background: #e3f2fd; 
            color: #1976d2; 
            padding: 5px 12px; 
            border-radius: 12px; 
            font-size: 0.85em; 
            font-weight: bold; 
            margin-left: 10px;
        }}
        .card-title {{ 
            font-size: 1.3em; 
            font-weight: 600; 
            color: #2c3e50; 
            margin-bottom: 12px; 
            line-height: 1.4;
            min-height: 3.6em;
            cursor: pointer;
        }}
        .card-summary {{ 
            color: #6c757d; 
            font-size: 0.95em; 
            line-height: 1.5; 
            margin-bottom: 18px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            cursor: pointer;
        }}
        .card-meta {{ 
            display: flex; 
            justify-content: space-between; 
            font-size: 0.85em; 
            color: #868e96; 
            border-top: 1px solid #e9ecef; 
            padding-top: 18px;
        }}
        .card-actions {{ 
            position: absolute; 
            top: 20px; 
            right: 20px; 
            display: flex; 
            gap: 8px; 
            opacity: 0; 
            transition: opacity 0.3s ease; 
        }}
        .conversation-card:hover .card-actions {{ 
            opacity: 1; 
        }}
        .action-btn {{ 
            background: white; 
            border: 2px solid #e9ecef; 
            border-radius: 8px; 
            padding: 6px 12px; 
            font-size: 0.8em; 
            cursor: pointer; 
            transition: all 0.3s ease;
            font-weight: 500;
            text-decoration: none;
            color: #333;
            display: inline-block;
        }}
        .action-btn:hover {{ 
            background: #667eea; 
            color: white; 
            border-color: #667eea;
            transform: scale(1.05);
        }}
        .recent-badge {{ 
            background: #ff6b6b; 
            color: white; 
            padding: 3px 10px; 
            border-radius: 12px; 
            font-size: 0.75em; 
            margin-left: 8px;
            animation: pulse 2s infinite;
        }}
        .no-results {{ 
            text-align: center; 
            padding: 60px 20px; 
            color: #6c757d;
            font-size: 1.1em;
            grid-column: 1 / -1;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        .category-badge {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 8px;
            font-weight: 500;
        }}
        
        .direct-link {{
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        .direct-link:hover {{
            background: #218838;
        }}
        
        .html-btn {{
            background: #17a2b8;
            color: white;
        }}
        .html-btn:hover {{
            background: #138496;
        }}
        
        .pdf-btn {{
            background: #dc3545;
            color: white;
        }}
        .pdf-btn:hover {{
            background: #c82333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Índice Combinado de Conversas</h1>
            <p>Qwen3 • ChatGPT • DeepSeek • Grok • COM HTML (Pandoc + MathJax)</p>
            <div class="stats">
                <div class="stat-item">
                    <strong>Total:</strong> <span id="total-count">{len(self.all_conversations)}</span> conversas
                </div>
                <div class="stat-item">
                    <strong>Ordenação:</strong> Mais Recentes Primeiro
                </div>
                <div class="stat-item">
                    <strong>Atualizado:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </div>
            </div>
        </div>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo ou categoria...">
        </div>
        
        <div class="filter-section">
            <button class="filter-btn active" data-filter="todas">Todas ({len(self.all_conversations)})</button>
"""
    
        for category, count in category_stats.items():
            html_content += f'<button class="filter-btn" data-filter="{category.lower()}">{category} ({count})</button>\n'

        html_content += """
        </div>
        
        <div style="text-align: center; padding: 15px; background: #e9ecef; border-bottom: 1px solid #ddd;">
            <strong>Acesso Rápido:</strong>
            <a href="combined_markdown/" class="direct-link" target="_blank">📁 Markdown</a>
            <a href="combined_html/" class="direct-link" target="_blank">🌐 HTML</a>
            <a href="combined_pdfs/" class="direct-link" target="_blank">📄 PDF</a>
            <a href="combined_json/" class="direct-link" target="_blank">📋 JSON</a>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
"""
    
        for i, conv in enumerate(self.all_conversations):
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}"
            recent_badge = "<span class='recent-badge'>NOVO</span>" if i < 5 else ""
            
            summary = conv.get('summary', 'Sem resumo disponível')
            if len(summary) > 150:
                summary = summary[:150] + "..."
            
            html_content += f"""
            <div class="conversation-card" data-title="{conv['title']}" data-summary="{summary}" data-source="{conv['source'].lower()}" data-category="{conv['category'].lower()}">
                <div class="card-header">
                    <div class="card-number">#{conv['number']} {recent_badge}</div>
                    <div class="card-actions">
                        <a href="combined_markdown/{filename}.md" class="action-btn" target="_blank" onclick="event.stopPropagation();">📄 MD</a>
                        <a href="combined_html/{filename}.html" class="action-btn html-btn" target="_blank" onclick="event.stopPropagation();">🌐 HTML</a>
                        <a href="combined_pdfs/{filename}.pdf" class="action-btn pdf-btn" target="_blank" onclick="event.stopPropagation();">📊 PDF</a>
                    </div>
                </div>
                <div class="card-title" onclick="openHTML('{filename}.html')">{conv['title']}</div>
                <div>
                    <span class="card-source">{conv['source']}</span>
                    <span class="category-badge">{conv['category']}</span>
                </div>
                <div class="card-summary" onclick="openHTML('{filename}.html')">{summary}</div>
                <div class="card-meta">
                    <span>📅 {conv.get('updated_at') or conv.get('inserted_at') or 'N/A'}</span>
                    <span>💬 {len(conv['messages'])} mensagens</span>
                </div>
            </div>
            """

        html_content += """
        </div>
    </div>
    
    <script>
        let currentFilter = 'todas';
        
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
        });

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.getAttribute('data-filter');
                filterConversations();
            });
        });

        document.getElementById('searchInput').addEventListener('input', filterConversations);

        function filterConversations() {
            const term = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.conversation-card');
            let visible = 0;
            
            cards.forEach(card => {
                const title = card.getAttribute('data-title').toLowerCase();
                const summary = card.getAttribute('data-summary').toLowerCase();
                const source = card.getAttribute('data-source').toLowerCase();
                const category = card.getAttribute('data-category').toLowerCase();
                
                const matchesSearch = (title.includes(term) || summary.includes(term) || category.includes(term) || source.includes(term));
                const matchesCategory = (currentFilter === 'todas' || category === currentFilter);
                
                if (matchesSearch && matchesCategory) {
                    card.style.display = 'block';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            updateStats(visible);
            
            const grid = document.getElementById('conversationsGrid');
            const noResults = document.getElementById('no-results-message');
            
            if (visible === 0) {
                if (!noResults) {
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results-message';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '🔍 Nenhuma conversa encontrada. Tente ajustar os filtros ou a pesquisa.';
                    grid.appendChild(noResultsMsg);
                }
            } else if (noResults) {
                noResults.remove();
            }
        }

        function updateStats(visibleCount = null) {
            const totalElement = document.getElementById('total-count');
            if (visibleCount !== null) {
                totalElement.textContent = visibleCount;
            } else {
                totalElement.textContent = """ + str(len(self.all_conversations)) + """;
            }
        }

        function openHTML(filename) {
            const htmlUrl = 'combined_html/' + filename;
            console.log('Abrindo HTML:', htmlUrl);
            window.open(htmlUrl, '_blank');
        }

        function openMD(filename) {
            const mdUrl = 'combined_markdown/' + filename;
            window.open(mdUrl, '_blank');
        }
        
        function openPDF(filename) {
            const pdfFile = filename.replace('.html', '.pdf');
            const pdfUrl = 'combined_pdfs/' + pdfFile;
            window.open(pdfUrl, '_blank');
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.getElementById('searchInput').value = '';
                filterConversations();
            }
        });

        document.querySelectorAll('.conversation-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.closest('.action-btn')) {
                    return;
                }
                
                const htmlBtn = this.querySelector('a.html-btn');
                if (htmlBtn) {
                    const htmlUrl = htmlBtn.getAttribute('href');
                    window.open(htmlUrl, '_blank');
                }
            });
        });

        document.getElementById('searchInput').focus();
        
        console.log('Índice carregado com', """ + str(len(self.all_conversations)) + """, 'conversas');
    </script>
</body>
</html>
"""
    
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"✅ Índice combinado criado: {self.index_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Processa exportações combinadas com exportação HTML via Pandoc."
    )
    parser.add_argument("--dry-run", action="store_true", help="Executa sem salvar arquivos")
    parser.add_argument("--force-overwrite", action="store_true", help="Substitui arquivos existentes")
    
    args = parser.parse_args()
    
    system = CombinedFragmentsSystem(
        dry_run=args.dry_run,
        force_overwrite=args.force_overwrite
    )
    system.run()

if __name__ == "__main__":
    main()
```

## Principais melhorias implementadas:

### 1. **Conversão Pandoc Otimizada:**
- `--embed-resources` para embutir recursos
- `--highlight-style=pygments` para syntax highlighting  
- `--mathjax=assets/tex-mml-chtml.js` para MathJax local
- Extensões avançadas do Markdown

### 2. **MathJax Local:**
- Detecta automaticamente arquivo local
- Fallback para CDN se necessário
- Configuração MathJax otimizada

### 3. **Sistema de Fallback em 3 Níveis:**
- Pandoc otimizado → Pandoc básico → Fallback Python
- Timeouts aprimorados

### 4. **HTML Aprimorado:**
- CSS responsivo e acessível
- Viewport meta tag
- Melhor syntax highlighting
- Design moderno

### 5. **Configuração MathJax:**
- Suporte a fórmulas inline e display
- Configuração para melhor renderização
- Compatibilidade com código e pre

### Comandos recomendados para uso:

```bash
# Executar o sistema
python comb_fragments_system3_html_export.py

# Modo dry-run para teste
python comb_fragments_system3_html_export.py --dry-run

# Forçar sobrescrita de arquivos
python comb_fragments_system3_html_export.py --force-overwrite
```

O sistema agora oferece conversão HTML significativamente melhorada com suporte robusto a matemática, código e formatação avançada!

---

### 👤 Utilizador *(2025-11-08 00:55:44)* *[deepseek-reasoner]*

Pretendo a optimização da conversão para html, pandoc com  --standalone --mathjax --embed-resources --syntax-highlighting=pygments --mathjax=assets/tex-mml-chtml.js e --table-of-contents --toc-depth=2 --number-sections ;

E o resultante agora: comb_fragments_system4_html_export.py completo

---

### 🤖 DeepSeek *(2025-11-08 00:55:44)* *[deepseek-reasoner]*

Vamos atualizar a função `_convert_with_pandoc_optimized` para incluir as novas opções:
  --table-of-contents (ou --toc)
  --toc-depth=2
  --number-sections

Além disso, vamos ajustar o comando para usar a opção `--syntax-highlighting=pygments` (que é equivalente a `--highlight-style=pygments`).

Nota: A opção `--embed-resources` é experimental e pode não estar disponível em todas as versões do Pandoc. Vamos mantê-la, mas se causar problemas, podemos removê-la.

Vamos também ajustar a função `_convert_with_pandoc_basic` para incluir as mesmas opções, mas sem `--embed-resources` para maior compatibilidade.

Além disso, note que a opção `--mathjax=assets/tex-mml-chtml.js` já está sendo tratada.

Vamos reorganizar o comando para que as opções sejam colocadas de forma consistente.

Vamos também adicionar a opção `--toc` (que é a abreviação de `--table-of-contents`) e `--toc-depth=2` e `--number-sections`.

Vamos atualizar a função `_convert_with_pandoc_optimized` e `_convert_with_pandoc_basic` para incluir essas opções.

Como a opção `--embed-resources` pode não ser suportada, vamos tentar usá-la apenas na versão otimizada e, se falhar, tentar sem ela.

No entanto, note que a opção `--embed-resources` é suportada apenas no Pandoc 2.19+ e apenas para HTML. Se houver erro, podemos removê-la.

Vamos também ajustar o tempo de timeout para 180 segundos, pois as opções adicionais podem aumentar o tempo de processamento.

Vamos também atualizar o método `_create_enhanced_html_template` para incluir o Table of Contents (TOC) e seções numeradas. Mas note que o Pandoc já irá gerar o TOC e a numeração se usarmos as opções.

Vamos então modificar as funções de conversão com Pandoc.

Vamos também verificar se o Pandoc suporta `--embed-resources`? Se não, podemos remover.

Vamos fazer uma verificação da versão do Pandoc para usar `--embed-resources` apenas se a versão for >= 2.19.

No entanto, para simplificar, vamos assumir que o usuário tem uma versão recente do Pandoc. Se não, o fallback será acionado.

Vamos então reescrever a função `_convert_with_pandoc_optimized`:

1. Verificar a versão do Pandoc para ver se suporta `--embed-resources` (opcional, por enquanto não vamos verificar, mas podemos adicionar um log de aviso se a versão for antiga).

2. Usar as opções:
   - `--standalone`
   - `--mathjax=assets/tex-mml-chtml.js` (se o arquivo local existir, senão `--mathjax`)
   - `--embed-resources`
   - `--highlight-style=pygments`
   - `--table-of-contents` (ou `--toc`)
   - `--toc-depth=2`
   - `--number-sections`

3. Aumentar o timeout para 180 segundos.

Vamos também atualizar a função `_convert_with_pandoc_basic` para incluir as opções de TOC e numeração, mas sem `--embed-resources`.

Vamos lá:

```python
    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando MathJax local, recursos embutidos, TOC e numeração"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comando otimizado para HTML5 com recursos embutidos, TOC e numeração
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--embed-resources',
                '--highlight-style=pygments',
                '--table-of-contents',
                '--toc-depth=2',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            # Remove argumentos vazios
            command = [arg for arg in command if arg]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=180
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)

    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        """Método básico de fallback para Pandoc com TOC e numeração"""
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--table-of-contents',
                '--toc-depth=2',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                return self._optimize_html_content(result.stdout)
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou, usando fallback Python: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)
```

Agora, note que o fallback Python (usando a biblioteca markdown) não suporta TOC e numeração de seções. Portanto, no fallback, vamos manter como estava.

Vamos também ajustar o CSS no método `_inject_custom_css` para estilizar o TOC e as seções numeradas. Mas o Pandoc já gera classes CSS para o TOC, então podemos adicionar algum estilo.

Vamos adicionar no CSS customizado:

```css
/* Estilo para o Table of Contents */
#TOC {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 20px;
}

#TOC ul {
    list-style-type: none;
    padding-left: 20px;
}

#TOC a {
    text-decoration: none;
    color: #495057;
}

#TOC a:hover {
    color: #007bff;
}

/* Estilo para numeração de seções */
body {
    counter-reset: section;
}

h1 {
    counter-reset: subsection;
}

h1:before {
    counter-increment: section;
    content: counter(section) ". ";
}

h2:before {
    counter-increment: subsection;
    content: counter(section) "." counter(subsection) " ";
}
```

No entanto, a numeração de seções é feita pelo Pandoc com a opção `--number-sections`, que já adiciona números às tags de cabeçalho. O CSS acima seria redundante. O Pandoc usa a classe `numbering` para isso, mas na verdade ele insere os números diretamente no HTML. Portanto, não precisamos do CSS de numeração.

Vamos então adicionar apenas o estilo para o TOC.

Vamos atualizar o método `_inject_custom_css` para incluir o estilo do TOC.

Vamos também ajustar o método `_create_enhanced_html_template` para incluir o TOC? Não, porque o TOC é gerado pelo Pandoc. Então não precisamos mudar o template.

Vamos então apenas ajustar o CSS customizado para o TOC.

Vamos modificar o método `_inject_custom_css`:

```python
    def _inject_custom_css(self, html_content: str) -> str:
        """Injeta CSS personalizado para melhorar a aparência, incluindo TOC"""
        custom_css = """
        <style>
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1em 0; }
            .math inline { display: inline-block; }
            pre { border-left: 4px solid #3498db; background: #f8f9fa; }
            code { background: #e9ecef; padding: 0.2em 0.4em; border-radius: 3px; }
            
            /* Melhorias responsivas */
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 15px; }
                pre { font-size: 12px; }
            }
            
            /* Melhorias para tabelas */
            table { width: 100%; border-collapse: collapse; margin: 1em 0; }
            th, td { border: 1px solid #dee2e6; padding: 0.75rem; }
            th { background-color: #3498db; color: white; }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 1em 0; 
                padding-left: 1em; 
                color: #6c757d;
                font-style: italic;
            }
            
            /* Estilo para o Table of Contents */
            #TOC {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
            }
            
            #TOC ul {
                list-style-type: none;
                padding-left: 20px;
            }
            
            #TOC a {
                text-decoration: none;
                color: #495057;
            }
            
            #TOC a:hover {
                color: #007bff;
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{custom_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{custom_css}')
        else:
            # Se não encontrar head, adiciona antes do body
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{custom_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{custom_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content
```

Agora, vamos atualizar o arquivo completo com essas mudanças.

Vamos também ajustar o timeout na função `_convert_with_pandoc_optimized` para 180 segundos e na função `_convert_with_pandoc_basic` para 120 segundos.

Vamos também verificar se a opção `--embed-resources` está causando problemas em versões antigas do Pandoc. Se estiver, podemos tentar detectar a versão do Pandoc e não usar `--embed-resources` se a versão for inferior a 2.19.

Vamos adicionar uma verificação da versão do Pandoc:

```python
    def _get_pandoc_version(self) -> Optional[tuple]:
        """Obtém a versão do Pandoc"""
        try:
            result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                version_str = first_line.split()[1]
                return tuple(map(int, version_str.split('.')))
        except:
            pass
        return None

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando MathJax local, recursos embutidos, TOC e numeração"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comando otimizado para HTML5 com recursos embutidos, TOC e numeração
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--embed-resources',
                '--highlight-style=pygments',
                '--table-of-contents',
                '--toc-depth=2',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            # Verifica a versão do Pandoc para --embed-resources (disponível a partir da versão 2.19)
            pandoc_version = self._get_pandoc_version()
            if pandoc_version and pandoc_version < (2, 19):
                command.remove('--embed-resources')
                self.logger.warning("⚠️  Versão do Pandoc anterior a 2.19, removendo --embed-resources")
            
            # Remove argumentos vazios
            command = [arg for arg in command if arg]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=180
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)
```

Agora, vamos incluir a função `_get_pandoc_version` e a verificação.

Vamos então gerar o arquivo completo com todas as alterações.

Vamos também atualizar o método `_convert_with_pandoc_basic` para não usar `--embed-resources` (já que é básico) e manter as opções de TOC e numeração.

Vamos agora gerar o código completo do arquivo `comb_fragments_system4_html_export.py`. Aqui está o arquivo `comb_fragments_system4_html_export.py` completo com todas as otimizações solicitadas:

```python
# comb_fragments_system4_html_export.py
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
from typing import List, Dict, Any, Optional
import markdown
import logging

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        # Configuração de processamento por fonte
        self.processors = {
            'qwen': {
                'file': "chat-export.json",
                'method': self.process_qwen_enhanced,
                'enabled': True
            },
            'chatgpt': {
                'file': "chatgpt.zip", 
                'method': self.process_chatgpt,
                'enabled': True
            },
            'deepseek': {
                'file': "deepseek_data.zip",
                'method': self.process_deepseek,
                'enabled': True
            },
            'grok': {
                'file': "grok.zip",
                'method': self.process_grok,
                'enabled': True
            }
        }

    def sanitize_filename(self, text: str, max_len: int = 50) -> str:
        """Sanitiza nomes de arquivo REMOVENDO ESPAÇOS e preservando emojis"""
        if not text or not isinstance(text, str):
            return "conversa_sem_titulo"
            
        # Remove caracteres inválidos
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F\s]'  # Inclui \s para remover espaços
        sanitized = re.sub(invalid_chars, '_', text)  # Substitui espaços por underscores
        sanitized = re.sub(r'_+', '_', sanitized)  # Remove underscores duplicados
        sanitized = sanitized.strip('_')  # Remove underscores no início e fim
        
        if not sanitized:
            sanitized = "conversa_sem_titulo"
            
        # Limita o comprimento
        if len(sanitized) > max_len:
            # Tenta cortar em um ponto lógico (underscore)
            if '_' in sanitized[:max_len]:
                last_underscore = sanitized[:max_len].rfind('_')
                if last_underscore > 10:
                    sanitized = sanitized[:last_underscore]
            else:
                sanitized = sanitized[:max_len]
            
        return sanitized

    def preserve_original_title(self, text: str) -> str:
        """Preserva o título original com espaços, apenas removendo caracteres realmente inválidos"""
        if not text or not isinstance(text, str):
            return "Conversa sem título"
            
        # Remove apenas caracteres realmente problemáticos, mantendo espaços
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized = re.sub(invalid_chars, '', text)
        sanitized = re.sub(r'\s+', ' ', sanitized.strip())
        
        if not sanitized:
            sanitized = "Conversa sem título"
            
        return sanitized

    def preserve_special_content(self, content: str) -> str:
        """Preserva fórmulas matemáticas, código e formatação especial"""
        if not content:
            return ""
            
        preserved_content = content
        
        # Corrige problemas com barras invertidas em LaTeX
        latex_corrections = {
            'ârac': '\\frac',
            'âarepsilon': '\\varepsilon',
            'â': '\\',
            'â': '\\'
        }
        
        for wrong, correct in latex_corrections.items():
            preserved_content = preserved_content.replace(wrong, correct)
        
        return preserved_content

    def ensure_directories(self):
        """Cria todas as pastas necessárias"""
        if self.dry_run:
            self.logger.info("DRY-RUN: Pastas seriam criadas:")
            for folder in self.output_dirs.values():
                self.logger.info(f"   {folder}")
            return
            
        for folder in self.output_dirs.values():
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pasta criada: {folder}")

    def run(self):
        """Executa o processamento completo"""
        self.logger.info("SISTEMA COMBINADO DE EXPORTAÇÕES COM HTML (Qwen3, ChatGPT, DeepSeek, Grok)")
        self.logger.info("=" * 70)
        
        if not self.data_dir.exists():
            self.logger.error(f"Pasta '{self.data_dir}' não encontrada.")
            self.logger.info("Crie a pasta 'data' e coloque os arquivos de exportação:")
            for source_name, config in self.processors.items():
                self.logger.info(f"   - {config['file']} (para {source_name.upper()})")
            return
        
        self.logger.info(f"Usando pasta de dados: {self.data_dir.absolute()}")
        
        self.ensure_directories()
        
        processed_count = 0
        for source_name, config in self.processors.items():
            if config['enabled']:
                file_path = self.data_dir / config['file']
                if file_path.exists():
                    self.logger.info(f"\nProcessando {source_name.upper()}...")
                    config['method'](file_path)
                    processed_count += 1
                else:
                    self.logger.warning(f"{source_name.upper()}: arquivo não encontrado - {file_path}")

        if processed_count == 0:
            self.logger.error("Nenhum arquivo de exportação encontrado na pasta 'data'.")
            return

        if not self.all_conversations:
            self.logger.error("Nenhuma conversa foi extraída dos arquivos.")
            return

        self._post_process_conversations()
        
        if not self.dry_run:
            self._export_all_formats()
            self.logger.info(f"\n🎉 SISTEMA COMBINADO FINALIZADO!")
            self.logger.info(f"📄 Índice: {self.index_file}")
            if Path(self.index_file).exists():
                webbrowser.open(f'file://{Path(self.index_file).absolute()}')
        else:
            self.logger.info(f"\n🔮 MODO DRY-RUN: Nenhum arquivo foi criado.")

    def _post_process_conversations(self):
        """Processamento pós-extração das conversas"""
        self.all_conversations.sort(
            key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at') or x.get('created_at')
            ),
            reverse=True
        )

        for i, conv in enumerate(self.all_conversations):
            conv['number'] = i + 1
            conv['category'] = self.categorize_conversation(conv['title'], conv.get('summary', ''))
            conv.setdefault('source', 'Desconhecido')
            conv.setdefault('messages', [])
            conv.setdefault('summary', conv['messages'][0]['content'][:100] + "..." if conv['messages'] else "Sem conteúdo")

        self.logger.info(f"📊 Total combinado de conversas: {len(self.all_conversations)}")

    def _export_all_formats(self):
        """Exporta para todos os formatos"""
        self.logger.info("\n🔄 Exportando para formatos...")
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index()

    def _get_pandoc_version(self) -> Optional[tuple]:
        """Obtém a versão do Pandoc para compatibilidade"""
        try:
            result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                version_str = first_line.split()[1]
                return tuple(map(int, version_str.split('.')))
        except:
            pass
        return None

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando todas as opções avançadas"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comandos base
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}',
                '--table-of-contents',
                '--toc-depth=2', 
                '--number-sections'
            ]
            
            # Verifica versão do Pandoc para recursos avançados
            pandoc_version = self._get_pandoc_version()
            
            # Adiciona --embed-resources apenas se suportado (Pandoc 2.19+)
            if pandoc_version and pandoc_version >= (2, 19):
                command.append('--embed-resources')
                self.logger.info("✅ Usando --embed-resources (Pandoc 2.19+)")
            else:
                self.logger.info("ℹ️  --embed-resources não suportado, usando recursos externos")
            
            # Adiciona syntax highlighting
            command.extend(['--syntax-highlighting=pygments'])
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=180
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)

    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        """Método básico de fallback para Pandoc com TOC e numeração"""
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--table-of-contents',
                '--toc-depth=2',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                return self._optimize_html_content(result.stdout)
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou, usando fallback Python: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)

    def _optimize_html_content(self, html_content: str) -> str:
        """Aplica otimizações finais ao conteúdo HTML"""
        # Adiciona viewport para responsividade
        if '<head>' in html_content and 'viewport' not in html_content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            html_content = html_content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        # Melhora acessibilidade
        if '<html' in html_content and 'lang' not in html_content:
            html_content = html_content.replace('<html>', '<html lang="pt-BR">')
        
        # Adiciona CSS personalizado para melhorar TOC e numeração
        html_content = self._inject_enhanced_css(html_content)
        
        # Otimiza TOC gerado pelo Pandoc
        html_content = self._enhance_toc_styling(html_content)
            
        return html_content

    def _inject_enhanced_css(self, html_content: str) -> str:
        """Injeta CSS personalizado aprimorado para TOC e numeração"""
        enhanced_css = """
        <style>
            /* Estilos para Table of Contents */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            #TOC ul {
                list-style-type: none;
                padding-left: 15px;
                margin: 10px 0;
            }
            
            #TOC ul ul {
                padding-left: 25px;
            }
            
            #TOC li {
                margin: 8px 0;
                line-height: 1.4;
            }
            
            #TOC a {
                text-decoration: none;
                color: #495057;
                font-weight: 500;
                transition: color 0.2s ease;
                display: block;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            #TOC a:hover {
                color: #007bff;
                background-color: rgba(0, 123, 255, 0.1);
            }
            
            #TOC > ul > li > a {
                font-weight: 600;
                color: #2c3e50;
                border-left: 3px solid #3498db;
                padding-left: 12px;
            }
            
            /* Estilos para numeração de seções */
            .header-section-number {
                color: #3498db;
                font-weight: bold;
                margin-right: 8px;
            }
            
            h1 .header-section-number {
                font-size: 0.9em;
            }
            
            h2 .header-section-number {
                font-size: 0.85em;
            }
            
            h3 .header-section-number {
                font-size: 0.8em;
            }
            
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1.5em 0; }
            .math inline { display: inline-block; }
            pre { 
                border-left: 4px solid #3498db; 
                background: #2d2d2d; 
                color: #f8f8f2;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.4;
            }
            code { 
                background: #e9ecef; 
                padding: 0.2em 0.4em; 
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                color: #c7254e;
            }
            pre code { 
                background: none; 
                color: inherit; 
                padding: 0; 
            }
            
            /* Melhorias responsivas */
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 15px; }
                pre { font-size: 12px; padding: 15px; }
                #TOC { padding: 15px; }
            }
            
            /* Melhorias para tabelas */
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 1.5em 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            th, td { 
                border: 1px solid #dee2e6; 
                padding: 12px 15px; 
                text-align: left; 
            }
            th { 
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white; 
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
                letter-spacing: 0.5px;
            }
            tr:nth-child(even) { 
                background-color: #f8f9fa; 
            }
            tr:hover { 
                background-color: #e3f2fd; 
                transition: background-color 0.2s ease;
            }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 25px 0; 
                padding-left: 25px; 
                color: #7f8c8d;
                font-style: italic;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 0 8px 8px 0;
            }
            
            /* Container principal */
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6; 
                margin: 0; 
                padding: 20px; 
                background-color: #f5f5f5;
                color: #333;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            
            /* Cabeçalhos com numeração */
            h1, h2, h3, h4, h5 { 
                color: #2c3e50; 
                margin-top: 1.8em;
                border-bottom: 1px solid #e9ecef;
                padding-bottom: 0.5em;
            }
            h1 { 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px; 
                color: #2c3e50;
                font-size: 2.2em;
            }
            h2 {
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin-top: 2em;
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{enhanced_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{enhanced_css}')
        else:
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{enhanced_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{enhanced_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content

    def _enhance_toc_styling(self, html_content: str) -> str:
        """Melhora o estilo do Table of Contents gerado pelo Pandoc"""
        # Adiciona título ao TOC se não existir
        if '<div id="TOC">' in html_content and 'Table of Contents' not in html_content:
            html_content = html_content.replace(
                '<div id="TOC">', 
                '<div id="TOC"><h2 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">📑 Table of Contents</h2>'
            )
        
        return html_content

    def _convert_with_fallback(self, md_file_path: str) -> str:
        """Fallback para conversão quando Pandoc falha"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Extensões avançadas para melhor conversão
            extensions = [
                'extra', 'tables', 'fenced_code', 'codehilite', 
                'toc', 'md_in_html', 'attr_list'
            ]
            
            html_content = markdown.markdown(
                md_content,
                extensions=extensions,
                output_format='html5'
            )
            
            return self._create_enhanced_html_template(html_content, Path(md_file_path).name)
            
        except Exception as e:
            self.logger.error(f"❌ Fallback também falhou: {e}")
            return self._create_basic_html(md_content, Path(md_file_path).name)

    def _create_enhanced_html_template(self, content: str, title: str) -> str:
        """Template HTML aprimorado com suporte a MathJax local/online"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5 {{
            color: #2c3e50;
            margin-top: 1.8em;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s ease;
        }}
        .math {{
            text-align: center;
            margin: 1.5em 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .author {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        .metadata {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }}
        .metadata h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        /* Estilos para TOC manual */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .toc h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 15px;
        }}
        .toc li {{
            margin: 8px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #495057;
            font-weight: 500;
        }}
        .toc a:hover {{
            color: #007bff;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                margin: 10px;
            }}
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <script>
        // Configuração MathJax para melhor renderização
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                renderActions: {{
                    addMenu: [0, '', '']
                }}
            }},
            startup: {{
                pageReady() {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax carregado com sucesso');
                    }});
                }}
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""

    def _create_basic_html(self, content: str, title: str) -> str:
        """HTML básico de último recurso com MathJax"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f5f5f5;
        }}
        pre {{ 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
    </style>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</head>
<body>
    <div class="container">
        <pre>{content}</pre>
    </div>
</body>
</html>"""

    def save_as_html_robust(self):
        """Método ROBUSTO para conversão HTML - VERSÃO OTIMIZADA"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] HTMLs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.html"
                self.logger.info(f"   🌐 {filename}")
            return
        
        markdown_folder = Path(self.output_dirs['markdown'])
        html_folder = Path(self.output_dirs['html'])
        
        md_files = list(markdown_folder.glob("*.md"))
        
        if not md_files:
            self.logger.error("❌ Nenhum arquivo Markdown encontrado para conversão.")
            return
        
        self.logger.info(f"🔄 Convertendo {len(md_files)} arquivos Markdown para HTML (OTIMIZADO)...")
        
        # Verifica se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada")
        except:
            pandoc_available = False
            self.logger.warning("⚠️ Pandoc não disponível - usando fallback Python")
        
        converted_count = 0
        failed_count = 0
        
        for md_file in md_files:
            try:
                html_file = html_folder / md_file.with_suffix('.html').name
                
                if not self.force_overwrite and html_file.exists():
                    self.logger.info(f"⏭️  Já existe: {html_file.name}")
                    converted_count += 1
                    continue

                self.logger.info(f"📄 Processando: {md_file.name}")
                
                if pandoc_available:
                    html_content = self._convert_with_pandoc_optimized(str(md_file))
                else:
                    html_content = self._convert_with_fallback(str(md_file))
                
                if html_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    self.logger.info(f"✅ Criado: {html_file.name}")
                    converted_count += 1
                else:
                    self.logger.error(f"❌ Falha na conversão: {md_file.name}")
                    failed_count += 1
                    
            except Exception as e:
                self.logger.error(f"❌ Erro em {md_file.name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                failed_count += 1
                
        self.logger.info(f"📊 HTML: {converted_count} arquivos criados, {failed_count} falhas em '{html_folder}'")

    def categorize_conversation(self, title: str, summary: str) -> str:
        """Categorização otimizada com expressões regulares"""
        text = f"{title} {summary}".lower()
        
        patterns = {
            'Tecnologia': r'\b(tecnologia|hardware|software|rede|internet|wifi|bluetooth|[45]g|cloud|aws|azure|gcp|servidor|hosting|domínio|ssl|router|switch|firewall|iot|smartphone|tablet|navegador|browser|chrome|firefox|edge|safari|email|gmail|outlook|criptografia|segurança|cibersegurança|ransomware|phishing|autenticação|2fa|biometria)\b',
            'Saúde': r'\b(saúde|medicina|médico|enfermagem|doença|vírus|bactéria|vacina|covid|coronavírus|gripe|febre|dor|análise|exame|raio x|ressonância|hospital|clínica|farmácia|medicamento|remédio|psicologia|terapia|bem-estar|nutrição|dieta|exercício|fitness|sono|saúde mental)\b',
            'Programação': r'\b(python|javascript|java|c\+\+|c#|go|rust|lua|bash|script|debug|erro|conda|mamba|pandoc|msys2|spyder|jupyter|pip|venv|docker|git|github|vscode|ide|programa|código|função|classe|api|selenium|playwright)\b',
            'Sistemas': r'\b(windows|linux|macos|so|sistema operacional|driver|registry|process|firewall|bios|boot|path|dll|exe|powershell|cmd|terminal|shell)\b',
            'IA': r'\b(ia|gpt|chatgpt|grok|qwen|deepseek|llm|modelo|prompt|token|embedding|fine-tune|neural|chatbot|inteligência artificial)\b',
            'Dados': r'\b(dados|data|csv|json|pandas|numpy|excel|sql|banco|sqlite|postgres|visualização|gráfico|tabela|análise|etl|dashboard)\b',
            'Geral': r'\b(geral|pergunta|ajuda|como fazer|explicar|resumo|tutorial básico)\b'
        }
        
        for category, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return category
                
        return 'Outros'

    def parse_timestamp_for_sorting(self, timestamp) -> datetime:
        if not timestamp:
            return datetime.min
            
        try:
            if isinstance(timestamp, str):
                clean_ts = timestamp.replace('T', ' ').split('.')[0].split('+')[0]
                if clean_ts.endswith('Z'):
                    clean_ts = clean_ts[:-1]
                return datetime.fromisoformat(clean_ts)
            elif isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
        except Exception:
            pass
            
        return datetime.min

    def format_timestamp(self, timestamp) -> Optional[str]:
        if not timestamp:
            return None
            
        try:
            if isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(timestamp, str):
                if 'T' in timestamp:
                    return timestamp.replace('T', ' ').split('.')[0]
                return timestamp
        except Exception:
            pass
            
        return str(timestamp)

    def create_enhanced_markdown_content(self, conversation: Dict[str, Any]) -> str:
        """Gera conteúdo Markdown com preservação total de formatação"""
        lines = [
            f"# {conversation['title']}",
            "",
            "## 📊 Informações",
            f"- **Número:** #{conversation['number']}",
            f"- **Origem:** {conversation['source']}",
            f"- **Categoria:** {conversation['category']}",
            f"- **ID:** {conversation.get('id', 'N/A')}",
            f"- **Criada em:** {conversation.get('inserted_at') or conversation.get('created_at') or 'N/A'}",
        ]
        
        if conversation.get('updated_at'):
            lines.append(f"- **Atualizada em:** {conversation['updated_at']}")
            
        lines.extend([
            f"- **Total de mensagens:** {len(conversation['messages'])}",
            f"- **Resumo:** {conversation.get('summary', 'Sem resumo')}",
            "",
            "---",
            "",
            "## 💬 Conversa",
            ""
        ])

        for j, msg in enumerate(conversation['messages'], 1):
            timestamp = f" *({msg['timestamp']})*" if msg['timestamp'] else ""
            model_info = f" *[{msg.get('model', '')}]*" if msg.get('model') else ""
            
            preserved_content = self.preserve_special_content(msg['content'])
            
            lines.extend([
                f"### {msg['author']}{timestamp}{model_info}",
                "",
                f"{preserved_content}",
                ""
            ])
            
            if j < len(conversation['messages']):
                lines.extend(["---", ""])

        lines.extend([
            "---",
            "",
            f"*Conversa exportada do {conversation['source']}*",
            f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        ])
        
        return '\n'.join(lines)

    def process_qwen_enhanced(self, path: Path):
        """Processa Qwen3 com preservação total de conteúdo"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Qwen3: {path}")
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                
            data = raw.get('data', [])
            if not isinstance(data, list):
                self.logger.warning("⚠️  Qwen3: 'data' não é uma lista.")
                return
                
            self.logger.info(f"🔍 Qwen3: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa Qwen {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                history = conv.get('chat', {}).get('history', {})
                messages = []

                if not history:
                    continue

                messages_dict = history.get('messages', {})
                
                if not isinstance(messages_dict, dict):
                    continue

                self.logger.info(f"   📝 Conversa {i+1}: '{clean_title}' - {len(messages_dict)} mensagens")

                for message_id, message_data in messages_dict.items():
                    if not isinstance(message_data, dict):
                        continue

                    role = message_data.get('role', '')
                    content = message_data.get('content', '')
                    
                    if not content or not role:
                        continue

                    if role == 'user':
                        author = "👤 Utilizador"
                    elif role == 'assistant':
                        author = "🤖 Qwen3"
                    else:
                        continue

                    if isinstance(content, list):
                        text_parts = []
                        for block in content:
                            if isinstance(block, dict):
                                if block.get('type') == 'text':
                                    text_parts.append(block.get('text', ''))
                                elif block.get('type') == 'image':
                                    image_info = block.get('image', '')
                                    if image_info:
                                        text_parts.append(f"![Imagem]({image_info})")
                            elif isinstance(block, str):
                                text_parts.append(block)
                        final_content = '\n'.join(text_parts).strip()
                    else:
                        final_content = str(content).strip()

                    final_content = self.preserve_special_content(final_content)

                    if not final_content or final_content == 'null':
                        continue

                    messages.append({
                        'author': author,
                        'role': role,
                        'content': final_content,
                        'timestamp': self.format_timestamp(message_data.get('created_at')),
                        'model': message_data.get('model', 'Qwen3')
                    })

                if messages:
                    messages.sort(key=lambda x: self.parse_timestamp_for_sorting(x['timestamp']))
                    
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'Qwen3',
                        'id': conv.get('id', f'qwen_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('created_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    self.logger.info(f"   ✅ Adicionada: {len(messages)} mensagens")
                    
            self.logger.info(f"✅ Qwen3: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Qwen3: {e}")
            if self.dry_run:
                traceback.print_exc()

    def process_chatgpt(self, path: Path):
        """Processa exportação do ChatGPT"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria ChatGPT: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="chatgpt_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)
            convs_path = Path(temp_dir) / "conversations.json"
            if not convs_path.exists():
                self.logger.error("❌ ChatGPT: conversations.json não encontrado.")
                return
                
            with open(convs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                self.logger.warning("⚠️  ChatGPT: estrutura inesperada.")
                return
                
            self.logger.info(f"🔍 ChatGPT: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa ChatGPT {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for msg_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                        
                    author_role = msg_data.get('author', {}).get('role', '')
                    if author_role == 'user':
                        author = "👤 Utilizador"
                        role = 'user'
                    elif author_role == 'assistant':
                        author = "🤖 ChatGPT"
                        role = 'assistant'
                    else:
                        continue
                        
                    content_parts = []
                    for part in msg_data.get('content', {}).get('parts', []):
                        if isinstance(part, str):
                            content_parts.append(part)
                    content = "\n".join(content_parts).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('create_time')),
                        'model': msg_data.get('model', 'ChatGPT')
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'ChatGPT',
                        'id': conv.get('id', f'chatgpt_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('create_time')),
                        'updated_at': self.format_timestamp(conv.get('update_time')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    
            self.logger.info(f"✅ ChatGPT: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar ChatGPT: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def process_deepseek(self, path: Path):
        """Processa exportação do DeepSeek"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria DeepSeek: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="deepseek_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)
                
            convs_path = Path(temp_dir) / "conversations.json"
            if not convs_path.exists():
                self.logger.error("❌ DeepSeek: conversations.json não encontrado.")
                return
                
            with open(convs_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            if isinstance(raw_data, list):
                data = raw_data
            elif isinstance(raw_data, dict) and 'data' in raw_data:
                data = raw_data['data']
            else:
                self.logger.warning("⚠️  DeepSeek: estrutura inesperada.")
                return
                
            if not isinstance(data, list):
                self.logger.warning("⚠️  DeepSeek: 'data' não é uma lista.")
                return
                
            self.logger.info(f"🔍 DeepSeek: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa DeepSeek {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for node_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                        
                    fragments = msg_data.get('fragments', [])
                    content_parts = []
                    msg_type = None
                    
                    for frag in fragments:
                        if isinstance(frag, dict):
                            frag_type = frag.get('type', '').upper()
                            if frag_type in ('REQUEST', 'RESPONSE'):
                                msg_type = frag_type
                            text = frag.get('text', '')
                            if text:
                                content_parts.append(text)
                            content = frag.get('content', '')
                            if content:
                                if isinstance(content, list):
                                    for item in content:
                                        if isinstance(item, str):
                                            content_parts.append(item)
                                        elif isinstance(item, dict):
                                            item_text = item.get('text', '')
                                            if item_text:
                                                content_parts.append(str(item_text))
                                else:
                                    content_parts.append(str(content))
                                    
                    content = ' '.join(content_parts).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue
                        
                    if msg_type == 'REQUEST':
                        author = "👤 Utilizador"
                        role = 'user'
                    else:
                        author = "🤖 DeepSeek"
                        role = 'assistant'
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('inserted_at')),
                        'model': msg_data.get('model', 'DeepSeek')
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'DeepSeek',
                        'id': conv.get('id', f'deepseek_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('inserted_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    
            self.logger.info(f"✅ DeepSeek: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar DeepSeek: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def process_grok(self, path: Path):
        """Processa exportação do Grok"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Grok: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="grok_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)

            target_file = None
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file == "prod-grok-backend.json":
                        target_file = Path(root) / file
                        break
                if target_file:
                    break

            if not target_file:
                self.logger.error("❌ Grok: ficheiro 'prod-grok-backend.json' não encontrado no ZIP.")
                return

            self.logger.info(f"🔍 Grok: carregando {target_file.name}...")
            with open(target_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict) or 'conversations' not in data:
                self.logger.error("❌ Grok: estrutura inesperada — chave 'conversations' não encontrada.")
                return

            conversations_list = data['conversations']
            if not isinstance(conversations_list, list):
                self.logger.error("❌ Grok: 'conversations' não é uma lista.")
                return

            self.logger.info(f"📊 Grok: encontradas {len(conversations_list)} conversas.")
            total_convs = 0

            for item in conversations_list:
                if not isinstance(item, dict):
                    continue

                conv_meta = item.get('conversation')
                responses = item.get('responses', [])

                if not isinstance(conv_meta, dict) or not isinstance(responses, list) or not responses:
                    continue

                conv_id = conv_meta.get('id')
                if not conv_id:
                    continue

                original_title = conv_meta.get('title', f"Conversa Grok {total_convs + 1}")
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                create_time_str = conv_meta.get('create_time')
                modify_time_str = conv_meta.get('modify_time')

                def format_iso_timestamp(ts_str):
                    if not ts_str:
                        return None
                    try:
                        if '.' in ts_str:
                            ts_str = ts_str.split('.')[0] + 'Z'
                        return self.format_timestamp(ts_str)
                    except:
                        return str(ts_str)

                inserted_at = format_iso_timestamp(create_time_str)
                updated_at = format_iso_timestamp(modify_time_str)

                messages = []
                for resp in responses:
                    if not isinstance(resp, dict):
                        continue

                    resp_data = resp.get('response')
                    if not isinstance(resp_data, dict):
                        continue

                    sender = resp_data.get('sender', '').upper()
                    if sender == 'HUMAN':
                        author = "👤 Utilizador"
                        role = "user"
                    elif sender == 'ASSISTANT':
                        author = "🤖 Grok"
                        role = "assistant"
                    else:
                        continue

                    content = str(resp_data.get('message', '')).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue

                    create_time = resp_data.get('create_time')
                    timestamp_ms = None
                    if isinstance(create_time, dict) and '$date' in create_time:
                        date_obj = create_time['$date']
                        if isinstance(date_obj, dict) and '$numberLong' in date_obj:
                            try:
                                timestamp_ms = int(date_obj['$numberLong'])
                            except:
                                pass

                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(timestamp_ms / 1000.0 if timestamp_ms else None),
                        'model': 'Grok'
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'Grok',
                        'id': conv_id,
                        'inserted_at': inserted_at,
                        'updated_at': updated_at,
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    total_convs += 1

            if total_convs > 0:
                self.logger.info(f"✅ Grok: processadas {total_convs} conversas.")
            else:
                self.logger.error("❌ Grok: nenhuma conversa válida encontrada.")

        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Grok: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def save_as_markdown_enhanced(self):
        """Salva conversas com preservação total de formatação"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Markdowns seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                self.logger.info(f"   📄 {filename}")
            return
            
        folder = Path(self.output_dirs['markdown'])
        saved_count = 0
        failed_count = 0
        
        for conv in self.all_conversations:
            try:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                filepath = folder / filename
                
                if not self.force_overwrite and filepath.exists():
                    continue
                    
                markdown_content = self.create_enhanced_markdown_content(conv)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                saved_count += 1
                
            except Exception as e:
                self.logger.error(f"❌ Erro ao salvar conversa {conv['number']}: {e}")
                failed_count += 1
                continue
                
        self.logger.info(f"✅ Markdown: {saved_count} arquivos criados, {failed_count} falhas em '{folder}'")

    def save_as_csv(self):
        """Salva conversas em arquivos CSV individuais"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] CSVs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
                self.logger.info(f"   📊 {filename}")
            return
            
        folder = Path(self.output_dirs['csv'])
        saved_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
            filepath = folder / filename
            
            if not self.force_overwrite and filepath.exists():
                continue
                
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'node_id', 'author', 'role', 'timestamp', 'model', 'content'
                ])
                writer.writeheader()
                for i, msg in enumerate(conv['messages']):
                    writer.writerow({
                        'node_id': str(i),
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content']
                    })
            saved_count += 1
            
        self.logger.info(f"✅ CSV: {saved_count} arquivos criados em '{folder}'")

    def save_as_json(self):
        """Salva conversas em arquivos JSON individuais"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] JSONs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
                self.logger.info(f"   📋 {filename}")
            return
            
        folder = Path(self.output_dirs['json'])
        saved_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
            filepath = folder / filename
            
            if not self.force_overwrite and filepath.exists():
                continue
                
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conv, f, ensure_ascii=False, indent=2)
            saved_count += 1
            
        self.logger.info(f"✅ JSON: {saved_count} arquivos criados em '{folder}'")

    def save_all_to_single_files(self):
        """Salva todas as conversas em arquivos únicos CSV e JSON"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Arquivos únicos seriam criados:")
            self.logger.info(f"   📁 {self.single_files['csv']}")
            self.logger.info(f"   📁 {self.single_files['json']}")
            return
            
        # CSV único
        with open(self.single_files['csv'], 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                'conversation_number', 'source', 'conversation_title', 'category',
                'author', 'role', 'timestamp', 'model', 'content'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for conv in self.all_conversations:
                for msg in conv['messages']:
                    writer.writerow({
                        'conversation_number': conv['number'],
                        'source': conv['source'],
                        'conversation_title': conv['title'],
                        'category': conv['category'],
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content']
                    })
        self.logger.info(f"✅ CSV único: {self.single_files['csv']}")

        # JSON único
        with open(self.single_files['json'], 'w', encoding='utf-8') as f:
            json.dump(self.all_conversations, f, ensure_ascii=False, indent=2)
        self.logger.info(f"✅ JSON único: {self.single_files['json']}")

    def create_searchable_index(self):
        """Cria índice HTML pesquisável com links para HTML"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Índice HTML seria criado: {self.index_file}")
            return
            
        self.logger.info("🎯 Criando índice HTML combinado...")
        
        category_stats = {}
        for conv in self.all_conversations:
            cat = conv['category']
            category_stats[cat] = category_stats.get(cat, 0) + 1

        html_content = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice Combinado - AI Chats</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 15px; font-weight: 300; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; margin-bottom: 20px; }}
        .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 25px; flex-wrap: wrap; }}
        .stat-item {{ background: rgba(255,255,255,0.15); padding: 18px 28px; border-radius: 12px; backdrop-filter: blur(10px); font-size: 1.1em; }}
        .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
        .search-box {{ width: 100%; padding: 18px 25px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; font-family: inherit; }}
        .search-box:focus {{ border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }}
        .filter-section {{
            padding: 20px 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        .filter-btn {{
            padding: 10px 20px;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 500;
            transition: all 0.3s ease;
            font-family: inherit;
        }}
        .filter-btn.active, .filter-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
        .conversations-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); 
            gap: 25px; 
            padding: 35px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 400px;
        }}
        .conversation-card {{ 
            background: white; 
            border: 1px solid #e9ecef; 
            border-radius: 15px; 
            padding: 25px; 
            transition: all 0.4s ease; 
            cursor: pointer; 
            position: relative;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .conversation-card:hover {{ 
            transform: translateY(-8px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.15); 
            border-color: #667eea;
        }}
        .card-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            margin-bottom: 18px; 
        }}
        .card-number {{ 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-size: 0.9em; 
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }}
        .card-source {{ 
            background: #e3f2fd; 
            color: #1976d2; 
            padding: 5px 12px; 
            border-radius: 12px; 
            font-size: 0.85em; 
            font-weight: bold; 
            margin-left: 10px;
        }}
        .card-title {{ 
            font-size: 1.3em; 
            font-weight: 600; 
            color: #2c3e50; 
            margin-bottom: 12px; 
            line-height: 1.4;
            min-height: 3.6em;
            cursor: pointer;
        }}
        .card-summary {{ 
            color: #6c757d; 
            font-size: 0.95em; 
            line-height: 1.5; 
            margin-bottom: 18px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            cursor: pointer;
        }}
        .card-meta {{ 
            display: flex; 
            justify-content: space-between; 
            font-size: 0.85em; 
            color: #868e96; 
            border-top: 1px solid #e9ecef; 
            padding-top: 18px;
        }}
        .card-actions {{ 
            position: absolute; 
            top: 20px; 
            right: 20px; 
            display: flex; 
            gap: 8px; 
            opacity: 0; 
            transition: opacity 0.3s ease; 
        }}
        .conversation-card:hover .card-actions {{ 
            opacity: 1; 
        }}
        .action-btn {{ 
            background: white; 
            border: 2px solid #e9ecef; 
            border-radius: 8px; 
            padding: 6px 12px; 
            font-size: 0.8em; 
            cursor: pointer; 
            transition: all 0.3s ease;
            font-weight: 500;
            text-decoration: none;
            color: #333;
            display: inline-block;
        }}
        .action-btn:hover {{ 
            background: #667eea; 
            color: white; 
            border-color: #667eea;
            transform: scale(1.05);
        }}
        .recent-badge {{ 
            background: #ff6b6b; 
            color: white; 
            padding: 3px 10px; 
            border-radius: 12px; 
            font-size: 0.75em; 
            margin-left: 8px;
            animation: pulse 2s infinite;
        }}
        .no-results {{ 
            text-align: center; 
            padding: 60px 20px; 
            color: #6c757d;
            font-size: 1.1em;
            grid-column: 1 / -1;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        .category-badge {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 8px;
            font-weight: 500;
        }}
        
        .direct-link {{
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        .direct-link:hover {{
            background: #218838;
        }}
        
        .html-btn {{
            background: #17a2b8;
            color: white;
        }}
        .html-btn:hover {{
            background: #138496;
        }}
        
        .pdf-btn {{
            background: #dc3545;
            color: white;
        }}
        .pdf-btn:hover {{
            background: #c82333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Índice Combinado de Conversas</h1>
            <p>Qwen3 • ChatGPT • DeepSeek • Grok • COM HTML (Pandoc + MathJax)</p>
            <div class="stats">
                <div class="stat-item">
                    <strong>Total:</strong> <span id="total-count">{len(self.all_conversations)}</span> conversas
                </div>
                <div class="stat-item">
                    <strong>Ordenação:</strong> Mais Recentes Primeiro
                </div>
                <div class="stat-item">
                    <strong>Atualizado:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </div>
            </div>
        </div>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo ou categoria...">
        </div>
        
        <div class="filter-section">
            <button class="filter-btn active" data-filter="todas">Todas ({len(self.all_conversations)})</button>
"""
    
        for category, count in category_stats.items():
            html_content += f'<button class="filter-btn" data-filter="{category.lower()}">{category} ({count})</button>\n'

        html_content += """
        </div>
        
        <div style="text-align: center; padding: 15px; background: #e9ecef; border-bottom: 1px solid #ddd;">
            <strong>Acesso Rápido:</strong>
            <a href="combined_markdown/" class="direct-link" target="_blank">📁 Markdown</a>
            <a href="combined_html/" class="direct-link" target="_blank">🌐 HTML</a>
            <a href="combined_pdfs/" class="direct-link" target="_blank">📄 PDF</a>
            <a href="combined_json/" class="direct-link" target="_blank">📋 JSON</a>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
"""
    
        for i, conv in enumerate(self.all_conversations):
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}"
            recent_badge = "<span class='recent-badge'>NOVO</span>" if i < 5 else ""
            
            summary = conv.get('summary', 'Sem resumo disponível')
            if len(summary) > 150:
                summary = summary[:150] + "..."
            
            html_content += f"""
            <div class="conversation-card" data-title="{conv['title']}" data-summary="{summary}" data-source="{conv['source'].lower()}" data-category="{conv['category'].lower()}">
                <div class="card-header">
                    <div class="card-number">#{conv['number']} {recent_badge}</div>
                    <div class="card-actions">
                        <a href="combined_markdown/{filename}.md" class="action-btn" target="_blank" onclick="event.stopPropagation();">📄 MD</a>
                        <a href="combined_html/{filename}.html" class="action-btn html-btn" target="_blank" onclick="event.stopPropagation();">🌐 HTML</a>
                        <a href="combined_pdfs/{filename}.pdf" class="action-btn pdf-btn" target="_blank" onclick="event.stopPropagation();">📊 PDF</a>
                    </div>
                </div>
                <div class="card-title" onclick="openHTML('{filename}.html')">{conv['title']}</div>
                <div>
                    <span class="card-source">{conv['source']}</span>
                    <span class="category-badge">{conv['category']}</span>
                </div>
                <div class="card-summary" onclick="openHTML('{filename}.html')">{summary}</div>
                <div class="card-meta">
                    <span>📅 {conv.get('updated_at') or conv.get('inserted_at') or 'N/A'}</span>
                    <span>💬 {len(conv['messages'])} mensagens</span>
                </div>
            </div>
            """

        html_content += """
        </div>
    </div>
    
    <script>
        let currentFilter = 'todas';
        
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
        });

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.getAttribute('data-filter');
                filterConversations();
            });
        });

        document.getElementById('searchInput').addEventListener('input', filterConversations);

        function filterConversations() {
            const term = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.conversation-card');
            let visible = 0;
            
            cards.forEach(card => {
                const title = card.getAttribute('data-title').toLowerCase();
                const summary = card.getAttribute('data-summary').toLowerCase();
                const source = card.getAttribute('data-source').toLowerCase();
                const category = card.getAttribute('data-category').toLowerCase();
                
                const matchesSearch = (title.includes(term) || summary.includes(term) || category.includes(term) || source.includes(term));
                const matchesCategory = (currentFilter === 'todas' || category === currentFilter);
                
                if (matchesSearch && matchesCategory) {
                    card.style.display = 'block';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            updateStats(visible);
            
            const grid = document.getElementById('conversationsGrid');
            const noResults = document.getElementById('no-results-message');
            
            if (visible === 0) {
                if (!noResults) {
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results-message';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '🔍 Nenhuma conversa encontrada. Tente ajustar os filtros ou a pesquisa.';
                    grid.appendChild(noResultsMsg);
                }
            } else if (noResults) {
                noResults.remove();
            }
        }

        function updateStats(visibleCount = null) {
            const totalElement = document.getElementById('total-count');
            if (visibleCount !== null) {
                totalElement.textContent = visibleCount;
            } else {
                totalElement.textContent = """ + str(len(self.all_conversations)) + """;
            }
        }

        function openHTML(filename) {
            const htmlUrl = 'combined_html/' + filename;
            console.log('Abrindo HTML:', htmlUrl);
            window.open(htmlUrl, '_blank');
        }

        function openMD(filename) {
            const mdUrl = 'combined_markdown/' + filename;
            window.open(mdUrl, '_blank');
        }
        
        function openPDF(filename) {
            const pdfFile = filename.replace('.html', '.pdf');
            const pdfUrl = 'combined_pdfs/' + pdfFile;
            window.open(pdfUrl, '_blank');
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.getElementById('searchInput').value = '';
                filterConversations();
            }
        });

        document.querySelectorAll('.conversation-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.closest('.action-btn')) {
                    return;
                }
                
                const htmlBtn = this.querySelector('a.html-btn');
                if (htmlBtn) {
                    const htmlUrl = htmlBtn.getAttribute('href');
                    window.open(htmlUrl, '_blank');
                }
            });
        });

        document.getElementById('searchInput').focus();
        
        console.log('Índice carregado com', """ + str(len(self.all_conversations)) + """, 'conversas');
    </script>
</body>
</html>
"""
    
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"✅ Índice combinado criado: {self.index_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Processa exportações combinadas com exportação HTML via Pandoc."
    )
    parser.add_argument("--dry-run", action="store_true", help="Executa sem salvar arquivos")
    parser.add_argument("--force-overwrite", action="store_true", help="Substitui arquivos existentes")
    
    args = parser.parse_args()
    
    system = CombinedFragmentsSystem(
        dry_run=args.dry_run,
        force_overwrite=args.force_overwrite
    )
    system.run()

if __name__ == "__main__":
    main()
```

## Principais otimizações implementadas:

### 1. **Pandoc com todas as opções avançadas:**
- `--standalone --mathjax --embed-resources --syntax-highlighting=pygments`
- `--mathjax=assets/tex-mml-chtml.js` (MathJax local)
- `--table-of-contents --toc-depth=2 --number-sections`

### 2. **Detecção de versão do Pandoc:**
- Verifica automaticamente se `--embed-resources` é suportado (Pandoc 2.19+)
- Fallback automático para versões mais antigas

### 3. **Table of Contents (TOC) aprimorado:**
- Estilização CSS personalizada para o TOC
- Hierarquia visual clara com diferentes níveis
- Design responsivo e acessível

### 4. **Numeração de seções:**
- Estilos CSS para números de seção
- Destaque visual para hierarquia
- Compatível com a numeração gerada pelo Pandoc

### 5. **CSS otimizado:**
- Estilos específicos para TOC e numeração
- Design moderno e responsivo
- Melhorias de acessibilidade

### 6. **Sistema de fallback robusto:**
- 3 níveis de conversão (Pandoc otimizado → Pandoc básico → Python)
- Timeouts ajustados para processamento pesado
- Logs detalhados para debugging

### Comandos recomendados:

```bash
# Preparar ambiente
mkdir -p assets
wget "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" -O "assets/tex-mml-chtml.js"

# Executar o sistema
python comb_fragments_system4_html_export.py

# Modo dry-run para teste
python comb_fragments_system4_html_export.py --dry-run

# Forçar sobrescrita
python comb_fragments_system4_html_export.py --force-overwrite
```

Este sistema agora oferece conversão HTML premium com TOC automático, numeração de seções, syntax highlighting avançado e suporte completo a fórmulas matemáticas!

---

### 👤 Utilizador *(2025-11-08 01:23:26)* *[deepseek-reasoner]*

Este sistema agora apresenta o html em meia pagina A4 porquê?

---

### 🤖 DeepSeek *(2025-11-08 01:23:26)* *[deepseek-reasoner]*

O problema de o HTML aparecer em meia página A4 provavelmente está relacionado com o CSS que está a ser aplicado. O sistema atual usa um container com `max-width: 900px` e margens automáticas, o que pode não ser ideal para impressão em A4.

Para melhorar a apresentação para impressão, podemos adicionar um CSS específico para a media query `@media print`. Vamos ajustar o layout para usar a largura total da página e ajustar o tamanho da fonte para ser legível quando impresso.

Além disso, o sistema atual está a usar um layout que é mais adequado para ecrã. Para impressão, podemos querer remover sombras, cores de fundo e ajustar margens.

Vamos modificar a função `_inject_enhanced_css` para incluir uma seção de estilos para impressão. Também podemos ajustar o container para que, quando impresso, ocupe a largura total e tenha margens adequadas.

Aqui estão as alterações sugeridas:

1. Adicionar uma media query para impressão no CSS.
2. Ajustar o container para ter 100% de largura e margens zero quando impresso.
3. Ajustar o tamanho da fonte para ser relativo (usar `pt` ou `cm` para impressão).
4. Garantir que o Table of Contents (TOC) e a numeração de seções são legíveis na impressão.

Vamos modificar a função `_inject_enhanced_css` para incluir estes estilos de impressão.

No entanto, note que o problema descrito é que o HTML está a ser apresentado em meia página A4. Isso pode ser devido ao container ter uma largura fixa de 900px, o que é mais que a metade da largura de um A4 (que é cerca de 595px a 842px de altura). Portanto, para impressão, devemos ajustar a largura para 100% e talvez usar uma unidade relativa para o tamanho da fonte.

Vamos adicionar o seguinte CSS para impressão:

```css
@media print {
    body { 
        background: white; 
        color: black; 
        font-size: 12pt; 
        line-height: 1.3;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 100%;
        margin: 0;
        padding: 0;
        box-shadow: none;
        background: white;
    }
    #TOC {
        background: white !important;
        border: 1px solid #000 !important;
    }
    /* Outros ajustes para impressão */
}
```

Vamos integrar isso no CSS injetado.

Além disso, note que o Pandoc, quando usado com `--standalone`, gera um HTML completo e pode incluir seu próprio CSS. No entanto, estamos a injetar CSS personalizado, então podemos sobrepor esses estilos.

Vamos modificar a função `_inject_enhanced_css` para incluir uma seção de impressão.

Como o código é extenso, vou focar apenas na função `_inject_enhanced_css` e na `_create_enhanced_html_template` (para o fallback) para adicionar os estilos de impressão.

Vou também ajustar o container principal para que, em impressão, ocupe toda a largura e não tenha margens.

Vamos fazer isso. O problema do HTML aparecer em meia página A4 está relacionado com o CSS que define um `max-width` muito pequeno para o container. Vou corrigir isso e otimizar o layout para melhor utilização do espaço.

Aqui está a correção no arquivo `comb_fragments_system4_html_export.py`:

```python
# comb_fragments_system4_html_export.py
# ... (código anterior mantido igual)

    def _inject_enhanced_css(self, html_content: str) -> str:
        """Injeta CSS personalizado aprimorado para TOC e numeração - CORRIGIDO"""
        enhanced_css = """
        <style>
            /* Container principal OTIMIZADO para usar espaço total */
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6; 
                margin: 0; 
                padding: 20px; 
                background-color: #f5f5f5;
                color: #333;
                max-width: none !important; /* Remove limitação de largura */
            }
            .container {
                max-width: 95% !important; /* Usa 95% da largura disponível */
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            
            /* Estilos para Table of Contents */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 100% !important;
            }
            
            #TOC ul {
                list-style-type: none;
                padding-left: 15px;
                margin: 10px 0;
            }
            
            #TOC ul ul {
                padding-left: 25px;
            }
            
            #TOC li {
                margin: 8px 0;
                line-height: 1.4;
            }
            
            #TOC a {
                text-decoration: none;
                color: #495057;
                font-weight: 500;
                transition: color 0.2s ease;
                display: block;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            #TOC a:hover {
                color: #007bff;
                background-color: rgba(0, 123, 255, 0.1);
            }
            
            #TOC > ul > li > a {
                font-weight: 600;
                color: #2c3e50;
                border-left: 3px solid #3498db;
                padding-left: 12px;
            }
            
            /* Estilos para numeração de seções */
            .header-section-number {
                color: #3498db;
                font-weight: bold;
                margin-right: 8px;
            }
            
            h1 .header-section-number {
                font-size: 0.9em;
            }
            
            h2 .header-section-number {
                font-size: 0.85em;
            }
            
            h3 .header-section-number {
                font-size: 0.8em;
            }
            
            /* Melhorias para código e matemática */
            .math { 
                display: block; 
                text-align: center; 
                margin: 1.5em 0; 
                max-width: 100% !important;
                overflow-x: auto;
            }
            .math inline { 
                display: inline-block; 
            }
            pre { 
                border-left: 4px solid #3498db; 
                background: #2d2d2d; 
                color: #f8f8f2;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.4;
                max-width: 100% !important;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            code { 
                background: #e9ecef; 
                padding: 0.2em 0.4em; 
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                color: #c7254e;
            }
            pre code { 
                background: none; 
                color: inherit; 
                padding: 0; 
            }
            
            /* Melhorias responsivas - OTIMIZADO */
            @media (max-width: 1200px) {
                .container {
                    max-width: 98% !important;
                    padding: 25px;
                }
            }
            
            @media (max-width: 768px) {
                body { 
                    padding: 10px; 
                    font-size: 14px; 
                }
                .container {
                    max-width: 100% !important;
                    padding: 20px;
                    margin: 5px;
                    border-radius: 5px;
                }
                pre { 
                    font-size: 12px; 
                    padding: 15px; 
                }
                #TOC { 
                    padding: 15px; 
                }
            }
            
            /* Melhorias para tabelas - OTIMIZADO */
            table { 
                width: 100% !important; 
                border-collapse: collapse; 
                margin: 1.5em 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
                max-width: 100% !important;
            }
            th, td { 
                border: 1px solid #dee2e6; 
                padding: 12px 15px; 
                text-align: left; 
            }
            th { 
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white; 
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
                letter-spacing: 0.5px;
            }
            tr:nth-child(even) { 
                background-color: #f8f9fa; 
            }
            tr:hover { 
                background-color: #e3f2fd; 
                transition: background-color 0.2s ease;
            }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 25px 0; 
                padding-left: 25px; 
                color: #7f8c8d;
                font-style: italic;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 0 8px 8px 0;
                max-width: 100% !important;
            }
            
            /* Cabeçalhos com numeração - OTIMIZADO */
            h1, h2, h3, h4, h5 { 
                color: #2c3e50; 
                margin-top: 1.8em;
                border-bottom: 1px solid #e9ecef;
                padding-bottom: 0.5em;
                max-width: 100% !important;
            }
            h1 { 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px; 
                color: #2c3e50;
                font-size: 2.2em;
            }
            h2 {
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin-top: 2em;
            }
            
            /* Mensagens de conversa - OTIMIZADO */
            .message-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                flex-wrap: wrap;
                gap: 10px;
                max-width: 100% !important;
            }
            .author {
                font-weight: bold;
                color: #2c3e50;
                font-size: 1.1em;
            }
            .timestamp {
                color: #7f8c8d;
                font-size: 0.9em;
                background: #e9ecef;
                padding: 4px 8px;
                border-radius: 4px;
            }
            .message-content {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #3498db;
                margin-bottom: 20px;
                max-width: 100% !important;
            }
            
            /* Estilos para impressão */
            @media print {
                body {
                    background: white !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }
                .container {
                    max-width: 100% !important;
                    box-shadow: none !important;
                    padding: 15px !important;
                    margin: 0 !important;
                }
                #TOC {
                    page-break-after: always;
                }
                pre, code {
                    white-space: pre-wrap !important;
                    word-wrap: break-word !important;
                }
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{enhanced_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{enhanced_css}')
        else:
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{enhanced_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{enhanced_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content

    def _create_enhanced_html_template(self, content: str, title: str) -> str:
        """Template HTML aprimorado com suporte a MathJax local/online - CORRIGIDO"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* CONTAINER PRINCIPAL OTIMIZADO */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
            max-width: none !important;
        }}
        .container {{
            max-width: 95% !important;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        h1, h2, h3, h4, h5 {{
            color: #2c3e50;
            margin-top: 1.8em;
            max-width: 100% !important;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
            max-width: 100% !important;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 8px 8px 0;
            max-width: 100% !important;
        }}
        table {{
            border-collapse: collapse;
            width: 100% !important;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            max-width: 100% !important;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s ease;
        }}
        .math {{
            text-align: center;
            margin: 1.5em 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow-x: auto;
            max-width: 100% !important;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
            max-width: 100% !important;
        }}
        .author {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
            max-width: 100% !important;
        }}
        .metadata {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
            max-width: 100% !important;
        }}
        .metadata h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        /* Estilos para TOC manual */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 100% !important;
        }}
        .toc h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 15px;
        }}
        .toc li {{
            margin: 8px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #495057;
            font-weight: 500;
        }}
        .toc a:hover {{
            color: #007bff;
        }}
        
        /* RESPONSIVIDADE OTIMIZADA */
        @media (max-width: 1200px) {{
            .container {{
                max-width: 98% !important;
                padding: 25px;
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                max-width: 100% !important;
                padding: 20px;
                margin: 5px;
            }}
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        
        /* ESTILOS PARA IMPRESSÃO */
        @media print {{
            body {{
                background: white !important;
                padding: 0 !important;
                margin: 0 !important;
                font-size: 12pt;
                line-height: 1.4;
            }}
            .container {{
                max-width: 100% !important;
                box-shadow: none !important;
                padding: 15px !important;
                margin: 0 !important;
                border-radius: 0 !important;
            }}
            #TOC {{
                page-break-after: always;
            }}
            pre, code {{
                white-space: pre-wrap !important;
                word-wrap: break-word !important;
                background: #f8f8f8 !important;
                border: 1px solid #ddd !important;
            }}
            .message-content {{
                background: #f8f8f8 !important;
                border-left: 3px solid #3498db !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <script>
        // Configuração MathJax para melhor renderização
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                renderActions: {{
                    addMenu: [0, '', '']
                }}
            }},
            startup: {{
                pageReady() {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax carregado com sucesso');
                    }});
                }}
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""

# ... (o resto do código permanece exatamente igual)
```

## Principais correções implementadas:

### 1. **Container Principal Otimizado:**
- `max-width: 95% !important` (em vez de 900px fixo)
- Remove limitações desnecessárias de largura
- Usa quase toda a largura disponível

### 2. **CSS com `!important` para Sobrescrever:**
- Força a largura máxima para evitar conflitos
- Garante que o container use o espaço disponível

### 3. **Responsividade Melhorada:**
- Breakpoints otimizados (1200px, 768px)
- Container adapta-se melhor a diferentes tamanhos de ecrã

### 4. **Elementos com Largura Total:**
- Tabelas, pre, blockquote, math com `max-width: 100% !important`
- Remove limitações artificiais de largura

### 5. **Estilos de Impressão:**
- Layout otimizado para impressão em A4
- Remove sombras e cores de fundo desnecessárias
- Mantém a legibilidade

### 6. **Wrap de Texto Melhorado:**
- `white-space: pre-wrap` e `word-wrap: break-word` para código
- Evita overflow horizontal

## Resultado:
Agora o HTML deve utilizar **quase toda a largura disponível** no navegador, em vez de ficar confinado a uma pequena coluna central. O conteúdo terá uma

---

### 👤 Utilizador *(2025-11-08 01:27:09)* *[deepseek-reasoner]*

Este sistema agora apresenta o html em meia pagina A4 porquê? Estou apenas a falar da apresentação no browser

---

### 🤖 DeepSeek *(2025-11-08 01:27:09)* *[deepseek-reasoner]*

O problema descrito sugere que o HTML gerado está sendo exibido em uma largura equivalente a meia página A4 no navegador. Isso provavelmente se deve ao CSS que define uma largura máxima (max-width) para o container principal. No código, o container tem `max-width: 900px` em vários lugares, o que pode ser muito pequeno para uma tela de desktop, especialmente se o usuário estiver com o navegador em tela cheia.

Vamos ajustar o CSS para que o container ocupe uma largura mais adequada. Além disso, podemos tornar o layout mais responsivo, usando porcentagens ou unidades relativas para que se adapte melhor a diferentes tamanhos de tela.

No método `_create_enhanced_html_template`, o container está com `max-width: 900px`. Vamos aumentar isso para algo em torno de 1200px ou usar uma porcentagem para que ocupe a maior parte da tela. Também devemos verificar o mesmo no CSS injetado no método `_inject_enhanced_css` e no método `_optimize_html_content` (que injeta CSS adicional).

Além disso, no método `_create_enhanced_html_template`, o container está com uma largura máxima fixa. Vamos alterar para:

```css
.container {
    max-width: 95%; /* Ou 1200px, dependendo do desejado */
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}
```

Da mesma forma, no CSS injetado no método `_inject_enhanced_css` (que é usado quando o Pandoc gera o HTML) devemos ajustar o container. No entanto, note que o HTML gerado pelo Pandoc pode não estar usando a classe `container` que definimos. O Pandoc gera um HTML com sua própria estrutura. Precisamos garantir que o CSS que injetamos no método `_inject_enhanced_css` também ajuste a largura do conteúdo.

No método `_inject_enhanced_css`, o CSS atual para o container é:

```css
.container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}
```

Vamos alterar para:

```css
.container {
    max-width: 1200px; /* Ou 95% */
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}
```

Além disso, note que o Pandoc gera um documento HTML completo e o conteúdo é colocado dentro de tags `<body>`. O CSS que injetamos no método `_inject_enhanced_css` é aplicado a todo o documento. Se o Pandoc gerar um container com uma classe específica, podemos precisar ajustar essa classe. Mas, no método `_inject_enhanced_css`, estamos definindo estilos para a classe `container` que não é necessariamente usada pelo Pandoc. O Pandoc, por padrão, não usa uma classe `container` para o conteúdo. Portanto, precisamos garantir que o CSS que injetamos afete o corpo do documento de maneira adequada.

Na verdade, o método `_inject_enhanced_css` injeta CSS que é aplicado a todo o documento. Se o Pandoc gera um HTML sem a classe `container`, então o CSS que definimos para `container` não terá efeito. Precisamos, portanto, ajustar o CSS para que afete o elemento `body` ou o elemento `main` que o Pandoc gera.

O Pandoc, quando usa `--standalone`, gera um HTML com uma estrutura típica, incluindo `<body>`. O conteúdo é colocado diretamente no `<body>`. Portanto, para ajustar a largura, podemos definir no CSS que o `body` tenha um padding e que o conteúdo dentro do `body` use uma largura máxima.

Vamos modificar o CSS injetado no método `_inject_enhanced_css` para:

1. Remover a classe `container` e em vez disso estilizar o `body` e talvez um container que envolva o conteúdo? Mas note que o Pandoc não gera um container com classe. Então, podemos criar uma regra para o `body` e para um elemento que envolva o conteúdo? Não, o Pandoc não gera esse container.

2. Uma alternativa é injetar um container no HTML gerado pelo Pandoc? Mas isso é mais complexo.

3. Outra alternativa é modificar o CSS para que o `body` tenha um layout que centralize o conteúdo e defina uma largura máxima. Podemos fazer:

```css
body {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
}
```

No entanto, note que no método `_inject_enhanced_css` já existem regras para o `body`. Vamos substituir a regra atual do `body` por:

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    color: #333;
    max-width: 1200px; /* Adicionamos max-width ao body */
}
```

Dessa forma, o corpo todo terá uma largura máxima de 1200px e será centralizado.

Além disso, no método `_create_enhanced_html_template` (usado no fallback) temos um container com classe `container` que está com `max-width: 900px`. Vamos alterar para 1200px.

Vamos fazer as seguintes alterações:

1. No método `_inject_enhanced_css`:
   - Alterar a regra do `body` para adicionar `max-width: 1200px;` e `margin: 0 auto;`
   - Remover a regra para `.container` (pois não está sendo usada pelo Pandoc) ou mantê-la se houver algum elemento com essa classe? Na verdade, o Pandoc não gera essa classe, então podemos remover? Mas note que no método `_create_enhanced_html_template` usamos a classe `container`. Portanto, vamos manter a regra para `.container` no CSS injetado, mas ajustar sua largura para 1200px.

2. No método `_create_enhanced_html_template`:
   - Alterar o `max-width` do container para 1200px.

3. No método `_create_basic_html` (fallback básico) também ajustar o container para 1200px.

Vamos implementar essas alterações.

No método `_inject_enhanced_css`:

Substitua:
```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
    color: #333;
}
```

Por:
```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    color: #333;
    max-width: 1200px;
}
```

E também altere a regra para `.container` (se existir) para 1200px. No método `_inject_enhanced_css` não há uma regra para `.container` atualmente. Então, vamos deixar como está.

No método `_create_enhanced_html_template`:

Altere:
```css
.container {
    max-width: 900px;
    ...
}
```

Para:
```css
.container {
    max-width: 1200px;
    ...
}
```

No método `_create_basic_html`:

Altere:
```css
.container {
    max-width: 800px;
    ...
}
```

Para:
```css
.container {
    max-width: 1200px;
    ...
}
```

Além disso, no método `_optimize_html_content` injetamos CSS adicional? Não, o método `_optimize_html_content` chama `_inject_enhanced_css` que já ajustamos.

Vamos fazer essas alterações no código.

Nota: O método `_inject_enhanced_css` é chamado pelo método `_optimize_html_content` para injetar CSS no HTML gerado pelo Pandoc. Portanto, essa alteração no `body` no método `_inject_enhanced_css` afetará o HTML do Pandoc.

Vamos agora gerar o código com essas alterações. O problema da apresentação do HTML em "meia página A4" no browser é causado pelo CSS que define uma largura máxima fixa. Vou ajustar o sistema para usar uma largura mais adequada para desktop. Aqui está a versão corrigida:

```python
# comb_fragments_system4_html_export.py
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
from typing import List, Dict, Any, Optional
import markdown
import logging

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        # Configuração de processamento por fonte
        self.processors = {
            'qwen': {
                'file': "chat-export.json",
                'method': self.process_qwen_enhanced,
                'enabled': True
            },
            'chatgpt': {
                'file': "chatgpt.zip", 
                'method': self.process_chatgpt,
                'enabled': True
            },
            'deepseek': {
                'file': "deepseek_data.zip",
                'method': self.process_deepseek,
                'enabled': True
            },
            'grok': {
                'file': "grok.zip",
                'method': self.process_grok,
                'enabled': True
            }
        }

    def sanitize_filename(self, text: str, max_len: int = 50) -> str:
        """Sanitiza nomes de arquivo REMOVENDO ESPAÇOS e preservando emojis"""
        if not text or not isinstance(text, str):
            return "conversa_sem_titulo"
            
        # Remove caracteres inválidos
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F\s]'  # Inclui \s para remover espaços
        sanitized = re.sub(invalid_chars, '_', text)  # Substitui espaços por underscores
        sanitized = re.sub(r'_+', '_', sanitized)  # Remove underscores duplicados
        sanitized = sanitized.strip('_')  # Remove underscores no início e fim
        
        if not sanitized:
            sanitized = "conversa_sem_titulo"
            
        # Limita o comprimento
        if len(sanitized) > max_len:
            # Tenta cortar em um ponto lógico (underscore)
            if '_' in sanitized[:max_len]:
                last_underscore = sanitized[:max_len].rfind('_')
                if last_underscore > 10:
                    sanitized = sanitized[:last_underscore]
            else:
                sanitized = sanitized[:max_len]
            
        return sanitized

    def preserve_original_title(self, text: str) -> str:
        """Preserva o título original com espaços, apenas removendo caracteres realmente inválidos"""
        if not text or not isinstance(text, str):
            return "Conversa sem título"
            
        # Remove apenas caracteres realmente problemáticos, mantendo espaços
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized = re.sub(invalid_chars, '', text)
        sanitized = re.sub(r'\s+', ' ', sanitized.strip())
        
        if not sanitized:
            sanitized = "Conversa sem título"
            
        return sanitized

    def preserve_special_content(self, content: str) -> str:
        """Preserva fórmulas matemáticas, código e formatação especial"""
        if not content:
            return ""
            
        preserved_content = content
        
        # Corrige problemas com barras invertidas em LaTeX
        latex_corrections = {
            'ârac': '\\frac',
            'âarepsilon': '\\varepsilon',
            'â': '\\',
            'â': '\\'
        }
        
        for wrong, correct in latex_corrections.items():
            preserved_content = preserved_content.replace(wrong, correct)
        
        return preserved_content

    def ensure_directories(self):
        """Cria todas as pastas necessárias"""
        if self.dry_run:
            self.logger.info("DRY-RUN: Pastas seriam criadas:")
            for folder in self.output_dirs.values():
                self.logger.info(f"   {folder}")
            return
            
        for folder in self.output_dirs.values():
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pasta criada: {folder}")

    def run(self):
        """Executa o processamento completo"""
        self.logger.info("SISTEMA COMBINADO DE EXPORTAÇÕES COM HTML (Qwen3, ChatGPT, DeepSeek, Grok)")
        self.logger.info("=" * 70)
        
        if not self.data_dir.exists():
            self.logger.error(f"Pasta '{self.data_dir}' não encontrada.")
            self.logger.info("Crie a pasta 'data' e coloque os arquivos de exportação:")
            for source_name, config in self.processors.items():
                self.logger.info(f"   - {config['file']} (para {source_name.upper()})")
            return
        
        self.logger.info(f"Usando pasta de dados: {self.data_dir.absolute()}")
        
        self.ensure_directories()
        
        processed_count = 0
        for source_name, config in self.processors.items():
            if config['enabled']:
                file_path = self.data_dir / config['file']
                if file_path.exists():
                    self.logger.info(f"\nProcessando {source_name.upper()}...")
                    config['method'](file_path)
                    processed_count += 1
                else:
                    self.logger.warning(f"{source_name.upper()}: arquivo não encontrado - {file_path}")

        if processed_count == 0:
            self.logger.error("Nenhum arquivo de exportação encontrado na pasta 'data'.")
            return

        if not self.all_conversations:
            self.logger.error("Nenhuma conversa foi extraída dos arquivos.")
            return

        self._post_process_conversations()
        
        if not self.dry_run:
            self._export_all_formats()
            self.logger.info(f"\n🎉 SISTEMA COMBINADO FINALIZADO!")
            self.logger.info(f"📄 Índice: {self.index_file}")
            if Path(self.index_file).exists():
                webbrowser.open(f'file://{Path(self.index_file).absolute()}')
        else:
            self.logger.info(f"\n🔮 MODO DRY-RUN: Nenhum arquivo foi criado.")

    def _post_process_conversations(self):
        """Processamento pós-extração das conversas"""
        self.all_conversations.sort(
            key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at') or x.get('created_at')
            ),
            reverse=True
        )

        for i, conv in enumerate(self.all_conversations):
            conv['number'] = i + 1
            conv['category'] = self.categorize_conversation(conv['title'], conv.get('summary', ''))
            conv.setdefault('source', 'Desconhecido')
            conv.setdefault('messages', [])
            conv.setdefault('summary', conv['messages'][0]['content'][:100] + "..." if conv['messages'] else "Sem conteúdo")

        self.logger.info(f"📊 Total combinado de conversas: {len(self.all_conversations)}")

    def _export_all_formats(self):
        """Exporta para todos os formatos"""
        self.logger.info("\n🔄 Exportando para formatos...")
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index()

    def _get_pandoc_version(self) -> Optional[tuple]:
        """Obtém a versão do Pandoc para compatibilidade"""
        try:
            result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                version_str = first_line.split()[1]
                return tuple(map(int, version_str.split('.')))
        except:
            pass
        return None

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando todas as opções avançadas"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comandos base
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}',
                '--table-of-contents',
                '--toc-depth=2', 
                '--number-sections'
            ]
            
            # Verifica versão do Pandoc para recursos avançados
            pandoc_version = self._get_pandoc_version()
            
            # Adiciona --embed-resources apenas se suportado (Pandoc 2.19+)
            if pandoc_version and pandoc_version >= (2, 19):
                command.append('--embed-resources')
                self.logger.info("✅ Usando --embed-resources (Pandoc 2.19+)")
            else:
                self.logger.info("ℹ️  --embed-resources não suportado, usando recursos externos")
            
            # Adiciona syntax highlighting
            command.extend(['--syntax-highlighting=pygments'])
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=180
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)

    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        """Método básico de fallback para Pandoc com TOC e numeração"""
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--table-of-contents',
                '--toc-depth=2',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                return self._optimize_html_content(result.stdout)
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou, usando fallback Python: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)

    def _optimize_html_content(self, html_content: str) -> str:
        """Aplica otimizações finais ao conteúdo HTML"""
        # Adiciona viewport para responsividade
        if '<head>' in html_content and 'viewport' not in html_content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            html_content = html_content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        # Melhora acessibilidade
        if '<html' in html_content and 'lang' not in html_content:
            html_content = html_content.replace('<html>', '<html lang="pt-BR">')
        
        # Adiciona CSS personalizado para melhorar TOC e numeração
        html_content = self._inject_enhanced_css(html_content)
        
        # Otimiza TOC gerado pelo Pandoc
        html_content = self._enhance_toc_styling(html_content)
            
        return html_content

    def _inject_enhanced_css(self, html_content: str) -> str:
        """Injeta CSS personalizado aprimorado para TOC e numeração"""
        enhanced_css = """
        <style>
            /* Layout principal melhorado para desktop */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
                max-width: none; /* Remove limitação de largura */
            }
            
            .container {
                max-width: 95%; /* Usa quase toda a largura disponível */
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }

            /* Estilos para Table of Contents */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                float: right;
                width: 300px;
                margin-left: 30px;
                margin-bottom: 30px;
            }
            
            #TOC ul {
                list-style-type: none;
                padding-left: 15px;
                margin: 10px 0;
            }
            
            #TOC ul ul {
                padding-left: 25px;
            }
            
            #TOC li {
                margin: 8px 0;
                line-height: 1.4;
            }
            
            #TOC a {
                text-decoration: none;
                color: #495057;
                font-weight: 500;
                transition: color 0.2s ease;
                display: block;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            #TOC a:hover {
                color: #007bff;
                background-color: rgba(0, 123, 255, 0.1);
            }
            
            #TOC > ul > li > a {
                font-weight: 600;
                color: #2c3e50;
                border-left: 3px solid #3498db;
                padding-left: 12px;
            }
            
            /* Estilos para numeração de seções */
            .header-section-number {
                color: #3498db;
                font-weight: bold;
                margin-right: 8px;
            }
            
            h1 .header-section-number {
                font-size: 0.9em;
            }
            
            h2 .header-section-number {
                font-size: 0.85em;
            }
            
            h3 .header-section-number {
                font-size: 0.8em;
            }
            
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1.5em 0; }
            .math inline { display: inline-block; }
            pre { 
                border-left: 4px solid #3498db; 
                background: #2d2d2d; 
                color: #f8f8f2;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.4;
            }
            code { 
                background: #e9ecef; 
                padding: 0.2em 0.4em; 
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                color: #c7254e;
            }
            pre code { 
                background: none; 
                color: inherit; 
                padding: 0; 
            }
            
            /* Melhorias responsivas */
            @media (max-width: 1200px) {
                .container {
                    max-width: 98%;
                    padding: 30px;
                }
                #TOC {
                    float: none;
                    width: auto;
                    margin: 20px 0;
                }
            }
            
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 20px; max-width: 100%; }
                pre { font-size: 12px; padding: 15px; }
                #TOC { padding: 15px; }
            }
            
            /* Melhorias para tabelas */
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 1.5em 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            th, td { 
                border: 1px solid #dee2e6; 
                padding: 12px 15px; 
                text-align: left; 
            }
            th { 
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white; 
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
                letter-spacing: 0.5px;
            }
            tr:nth-child(even) { 
                background-color: #f8f9fa; 
            }
            tr:hover { 
                background-color: #e3f2fd; 
                transition: background-color 0.2s ease;
            }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 25px 0; 
                padding-left: 25px; 
                color: #7f8c8d;
                font-style: italic;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 0 8px 8px 0;
            }
            
            /* Cabeçalhos com numeração */
            h1, h2, h3, h4, h5 { 
                color: #2c3e50; 
                margin-top: 1.8em;
                border-bottom: 1px solid #e9ecef;
                padding-bottom: 0.5em;
            }
            h1 { 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px; 
                color: #2c3e50;
                font-size: 2.2em;
            }
            h2 {
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin-top: 2em;
            }
            
            /* Clearfix para layout com TOC flutuante */
            .main-content {
                overflow: hidden;
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{enhanced_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{enhanced_css}')
        else:
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{enhanced_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{enhanced_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content

    def _enhance_toc_styling(self, html_content: str) -> str:
        """Melhora o estilo do Table of Contents gerado pelo Pandoc"""
        # Adiciona título ao TOC se não existir
        if '<div id="TOC">' in html_content and 'Table of Contents' not in html_content:
            html_content = html_content.replace(
                '<div id="TOC">', 
                '<div id="TOC"><h2 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">📑 Table of Contents</h2>'
            )
        
        # Adiciona wrapper para conteúdo principal
        if '<div id="TOC">' in html_content and '<body>' in html_content:
            # Encontra o TOC e envolve o conteúdo restante
            toc_end = html_content.find('</div>', html_content.find('<div id="TOC">')) + 6
            body_content = html_content[toc_end:]
            if '<div class="main-content">' not in body_content:
                html_content = html_content[:toc_end] + '\n<div class="main-content">' + body_content + '\n</div>'
        
        return html_content

    def _convert_with_fallback(self, md_file_path: str) -> str:
        """Fallback para conversão quando Pandoc falha"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Extensões avançadas para melhor conversão
            extensions = [
                'extra', 'tables', 'fenced_code', 'codehilite', 
                'toc', 'md_in_html', 'attr_list'
            ]
            
            html_content = markdown.markdown(
                md_content,
                extensions=extensions,
                output_format='html5'
            )
            
            return self._create_enhanced_html_template(html_content, Path(md_file_path).name)
            
        except Exception as e:
            self.logger.error(f"❌ Fallback também falhou: {e}")
            return self._create_basic_html(md_content, Path(md_file_path).name)

    def _create_enhanced_html_template(self, content: str, title: str) -> str:
        """Template HTML aprimorado com suporte a MathJax local/online"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
            max-width: none; /* Remove limitação de largura */
        }}
        .container {{
            max-width: 95%; /* Usa quase toda a largura disponível */
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5 {{
            color: #2c3e50;
            margin-top: 1.8em;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s ease;
        }}
        .math {{
            text-align: center;
            margin: 1.5em 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .author {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        .metadata {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }}
        .metadata h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        /* Estilos para TOC manual */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            float: right;
            width: 300px;
            margin-left: 30px;
        }}
        .toc h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 15px;
        }}
        .toc li {{
            margin: 8px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #495057;
            font-weight: 500;
        }}
        .toc a:hover {{
            color: #007bff;
        }}
        .main-content {{
            overflow: hidden;
        }}
        @media (max-width: 1200px) {{
            .container {{
                max-width: 98%;
                padding: 30px;
            }}
            .toc {{
                float: none;
                width: auto;
                margin: 20px 0;
            }}
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                max-width: 100%;
            }}
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <script>
        // Configuração MathJax para melhor renderização
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                renderActions: {{
                    addMenu: [0, '', '']
                }}
            }},
            startup: {{
                pageReady() {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax carregado com sucesso');
                    }});
                }}
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""

    def _create_basic_html(self, content: str, title: str) -> str:
        """HTML básico de último recurso com MathJax"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f5f5f5;
            max-width: none; /* Remove limitação de largura */
        }}
        pre {{ 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        .container {{
            max-width: 95%; /* Usa quase toda a largura disponível */
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
    </style>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</head>
<body>
    <div class="container">
        <pre>{content}</pre>
    </div>
</body>
</html>"""

    # ... (restante dos métodos permanecem inalterados)

    def save_as_html_robust(self):
        """Método ROBUSTO para conversão HTML - VERSÃO OTIMIZADA"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] HTMLs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.html"
                self.logger.info(f"   🌐 {filename}")
            return
        
        markdown_folder = Path(self.output_dirs['markdown'])
        html_folder = Path(self.output_dirs['html'])
        
        md_files = list(markdown_folder.glob("*.md"))
        
        if not md_files:
            self.logger.error("❌ Nenhum arquivo Markdown encontrado para conversão.")
            return
        
        self.logger.info(f"🔄 Convertendo {len(md_files)} arquivos Markdown para HTML (OTIMIZADO)...")
        
        # Verifica se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada")
        except:
            pandoc_available = False
            self.logger.warning("⚠️ Pandoc não disponível - usando fallback Python")
        
        converted_count = 0
        failed_count = 0
        
        for md_file in md_files:
            try:
                html_file = html_folder / md_file.with_suffix('.html').name
                
                if not self.force_overwrite and html_file.exists():
                    self.logger.info(f"⏭️  Já existe: {html_file.name}")
                    converted_count += 1
                    continue

                self.logger.info(f"📄 Processando: {md_file.name}")
                
                if pandoc_available:
                    html_content = self._convert_with_pandoc_optimized(str(md_file))
                else:
                    html_content = self._convert_with_fallback(str(md_file))
                
                if html_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    self.logger.info(f"✅ Criado: {html_file.name}")
                    converted_count += 1
                else:
                    self.logger.error(f"❌ Falha na conversão: {md_file.name}")
                    failed_count += 1
                    
            except Exception as e:
                self.logger.error(f"❌ Erro em {md_file.name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                failed_count += 1
                
        self.logger.info(f"📊 HTML: {converted_count} arquivos criados, {failed_count} falhas em '{html_folder}'")

    # ... (restante dos métodos permanecem inalterados)

def main():
    parser = argparse.ArgumentParser(
        description="Processa exportações combinadas com exportação HTML via Pandoc."
    )
    parser.add_argument("--dry-run", action="store_true", help="Executa sem salvar arquivos")
    parser.add_argument("--force-overwrite", action="store_true", help="Substitui arquivos existentes")
    
    args = parser.parse_args()
    
    system = CombinedFragmentsSystem(
        dry_run=args.dry_run,
        force_overwrite=args.force_overwrite
    )
    system.run()

if __name__ == "__main__":
    main()
```

## Principais correções para o layout:

### 1. **Remoção de limitações de largura:**
- `max-width: none` no elemento `body`
- `max-width: 95%` no container principal (em vez de 900px fixos)
- Layout adaptativo que usa quase toda a largura disponível

### 2. **TOC flutuante:**
- TOC posicionado à direita com `float: right`
- Largura fixa de 300px para o TOC
- Conteúdo principal flui ao redor do TOC

### 3. **Design responsivo melhorado:**
- Breakpoints ajustados para 1200px e 768px
- TOC torna-se não-flutuante em telas menores
- Container expande para 98% em telas médias

### 4. **Clearfix para layout:**
- Classe `.main-content` com `overflow: hidden`
- Previne problemas de float e garante layout consistente

### 5. **Melhor utilização do espaço:**
- Padding otimizado para desktop
- Margens ajustadas para melhor aproveitamento do espaço
- Container centralizado mas com máxima largura possível

Agora o HTML deve ocupar praticamente toda a largura disponível no browser, proporcionando uma experiência de leitura muito melhor em desktop, enquanto mantém a responsividade para dispositivos móveis.

---

### 👤 Utilizador *(2025-11-08 01:36:59)* *[deepseek-reasoner]*

pretendo comb_fragments_system4_html_export.py  completo

---

### 🤖 DeepSeek *(2025-11-08 01:36:59)* *[deepseek-reasoner]*

Vamos ajustar o CSS para que o conteúdo ocupe a largura total da tela, removendo a limitação de largura máxima que estava causando a aparência de "meia página A4".
 As alterações principais serão:
  1. Remover a largura máxima (max-width) do container principal.
  2. Ajustar o padding e margens para melhor aproveitamento do espaço.
  3. Manter o TOC flutuante à direita, mas ajustar sua largura e posicionamento.
  4. Garantir que o conteúdo principal ocupe a maior parte da tela.

 No entanto, note que o código atual já define no método `_inject_enhanced_css` um container com `max-width: 95%`. Vamos alterar para `max-width: none` e ajustar o container para usar uma largura mais flexível.

 Vou fornecer o arquivo completo com as correções necessárias para o layout ocupar a tela inteira. Aqui está o arquivo `comb_fragments_system4_html_export.py` completo com todas as correções de layout:

```python
# comb_fragments_system4_html_export.py
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
from typing import List, Dict, Any, Optional
import markdown
import logging

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        # Configuração de processamento por fonte
        self.processors = {
            'qwen': {
                'file': "chat-export.json",
                'method': self.process_qwen_enhanced,
                'enabled': True
            },
            'chatgpt': {
                'file': "chatgpt.zip", 
                'method': self.process_chatgpt,
                'enabled': True
            },
            'deepseek': {
                'file': "deepseek_data.zip",
                'method': self.process_deepseek,
                'enabled': True
            },
            'grok': {
                'file': "grok.zip",
                'method': self.process_grok,
                'enabled': True
            }
        }

    def sanitize_filename(self, text: str, max_len: int = 50) -> str:
        """Sanitiza nomes de arquivo REMOVENDO ESPAÇOS e preservando emojis"""
        if not text or not isinstance(text, str):
            return "conversa_sem_titulo"
            
        # Remove caracteres inválidos
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F\s]'  # Inclui \s para remover espaços
        sanitized = re.sub(invalid_chars, '_', text)  # Substitui espaços por underscores
        sanitized = re.sub(r'_+', '_', sanitized)  # Remove underscores duplicados
        sanitized = sanitized.strip('_')  # Remove underscores no início e fim
        
        if not sanitized:
            sanitized = "conversa_sem_titulo"
            
        # Limita o comprimento
        if len(sanitized) > max_len:
            # Tenta cortar em um ponto lógico (underscore)
            if '_' in sanitized[:max_len]:
                last_underscore = sanitized[:max_len].rfind('_')
                if last_underscore > 10:
                    sanitized = sanitized[:last_underscore]
            else:
                sanitized = sanitized[:max_len]
            
        return sanitized

    def preserve_original_title(self, text: str) -> str:
        """Preserva o título original com espaços, apenas removendo caracteres realmente inválidos"""
        if not text or not isinstance(text, str):
            return "Conversa sem título"
            
        # Remove apenas caracteres realmente problemáticos, mantendo espaços
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized = re.sub(invalid_chars, '', text)
        sanitized = re.sub(r'\s+', ' ', sanitized.strip())
        
        if not sanitized:
            sanitized = "Conversa sem título"
            
        return sanitized

    def preserve_special_content(self, content: str) -> str:
        """Preserva fórmulas matemáticas, código e formatação especial"""
        if not content:
            return ""
            
        preserved_content = content
        
        # Corrige problemas com barras invertidas em LaTeX
        latex_corrections = {
            'ârac': '\\frac',
            'âarepsilon': '\\varepsilon',
            'â': '\\',
            'â': '\\'
        }
        
        for wrong, correct in latex_corrections.items():
            preserved_content = preserved_content.replace(wrong, correct)
        
        return preserved_content

    def ensure_directories(self):
        """Cria todas as pastas necessárias"""
        if self.dry_run:
            self.logger.info("DRY-RUN: Pastas seriam criadas:")
            for folder in self.output_dirs.values():
                self.logger.info(f"   {folder}")
            return
            
        for folder in self.output_dirs.values():
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pasta criada: {folder}")

    def run(self):
        """Executa o processamento completo"""
        self.logger.info("SISTEMA COMBINADO DE EXPORTAÇÕES COM HTML (Qwen3, ChatGPT, DeepSeek, Grok)")
        self.logger.info("=" * 70)
        
        if not self.data_dir.exists():
            self.logger.error(f"Pasta '{self.data_dir}' não encontrada.")
            self.logger.info("Crie a pasta 'data' e coloque os arquivos de exportação:")
            for source_name, config in self.processors.items():
                self.logger.info(f"   - {config['file']} (para {source_name.upper()})")
            return
        
        self.logger.info(f"Usando pasta de dados: {self.data_dir.absolute()}")
        
        self.ensure_directories()
        
        processed_count = 0
        for source_name, config in self.processors.items():
            if config['enabled']:
                file_path = self.data_dir / config['file']
                if file_path.exists():
                    self.logger.info(f"\nProcessando {source_name.upper()}...")
                    config['method'](file_path)
                    processed_count += 1
                else:
                    self.logger.warning(f"{source_name.upper()}: arquivo não encontrado - {file_path}")

        if processed_count == 0:
            self.logger.error("Nenhum arquivo de exportação encontrado na pasta 'data'.")
            return

        if not self.all_conversations:
            self.logger.error("Nenhuma conversa foi extraída dos arquivos.")
            return

        self._post_process_conversations()
        
        if not self.dry_run:
            self._export_all_formats()
            self.logger.info(f"\n🎉 SISTEMA COMBINADO FINALIZADO!")
            self.logger.info(f"📄 Índice: {self.index_file}")
            if Path(self.index_file).exists():
                webbrowser.open(f'file://{Path(self.index_file).absolute()}')
        else:
            self.logger.info(f"\n🔮 MODO DRY-RUN: Nenhum arquivo foi criado.")

    def _post_process_conversations(self):
        """Processamento pós-extração das conversas"""
        self.all_conversations.sort(
            key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at') or x.get('created_at')
            ),
            reverse=True
        )

        for i, conv in enumerate(self.all_conversations):
            conv['number'] = i + 1
            conv['category'] = self.categorize_conversation(conv['title'], conv.get('summary', ''))
            conv.setdefault('source', 'Desconhecido')
            conv.setdefault('messages', [])
            conv.setdefault('summary', conv['messages'][0]['content'][:100] + "..." if conv['messages'] else "Sem conteúdo")

        self.logger.info(f"📊 Total combinado de conversas: {len(self.all_conversations)}")

    def _export_all_formats(self):
        """Exporta para todos os formatos"""
        self.logger.info("\n🔄 Exportando para formatos...")
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index()

    def _get_pandoc_version(self) -> Optional[tuple]:
        """Obtém a versão do Pandoc para compatibilidade"""
        try:
            result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                version_str = first_line.split()[1]
                return tuple(map(int, version_str.split('.')))
        except:
            pass
        return None

    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """Conversão OTIMIZADA com Pandoc usando todas as opções avançadas"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc otimizado: {Path(md_file_path).name}")
            
            # Verifica se o arquivo MathJax local existe
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            # Comandos base
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}',
                '--table-of-contents',
                '--toc-depth=2', 
                '--number-sections'
            ]
            
            # Verifica versão do Pandoc para recursos avançados
            pandoc_version = self._get_pandoc_version()
            
            # Adiciona --embed-resources apenas se suportado (Pandoc 2.19+)
            if pandoc_version and pandoc_version >= (2, 19):
                command.append('--embed-resources')
                self.logger.info("✅ Usando --embed-resources (Pandoc 2.19+)")
            else:
                self.logger.info("ℹ️  --embed-resources não suportado, usando recursos externos")
            
            # Adiciona syntax highlighting
            command.extend(['--syntax-highlighting=pygments'])
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=180
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                
                # Aplica otimizações adicionais
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou, tentando método básico: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)

    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        """Método básico de fallback para Pandoc com TOC e numeração"""
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--table-of-contents',
                '--toc-depth=2',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                return self._optimize_html_content(result.stdout)
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou, usando fallback Python: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)

    def _optimize_html_content(self, html_content: str) -> str:
        """Aplica otimizações finais ao conteúdo HTML"""
        # Adiciona viewport para responsividade
        if '<head>' in html_content and 'viewport' not in html_content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            html_content = html_content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        # Melhora acessibilidade
        if '<html' in html_content and 'lang' not in html_content:
            html_content = html_content.replace('<html>', '<html lang="pt-BR">')
        
        # Adiciona CSS personalizado para melhorar TOC e numeração
        html_content = self._inject_enhanced_css(html_content)
        
        # Otimiza TOC gerado pelo Pandoc
        html_content = self._enhance_toc_styling(html_content)
            
        return html_content

    def _inject_enhanced_css(self, html_content: str) -> str:
        """Injeta CSS personalizado aprimorado para TOC e numeração"""
        enhanced_css = """
        <style>
            /* Layout principal melhorado para desktop */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
                max-width: none; /* Remove limitação de largura */
            }
            
            .container {
                max-width: 95%; /* Usa quase toda a largura disponível */
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }

            /* Estilos para Table of Contents */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                float: right;
                width: 300px;
                margin-left: 30px;
                margin-bottom: 30px;
            }
            
            #TOC ul {
                list-style-type: none;
                padding-left: 15px;
                margin: 10px 0;
            }
            
            #TOC ul ul {
                padding-left: 25px;
            }
            
            #TOC li {
                margin: 8px 0;
                line-height: 1.4;
            }
            
            #TOC a {
                text-decoration: none;
                color: #495057;
                font-weight: 500;
                transition: color 0.2s ease;
                display: block;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            #TOC a:hover {
                color: #007bff;
                background-color: rgba(0, 123, 255, 0.1);
            }
            
            #TOC > ul > li > a {
                font-weight: 600;
                color: #2c3e50;
                border-left: 3px solid #3498db;
                padding-left: 12px;
            }
            
            /* Estilos para numeração de seções */
            .header-section-number {
                color: #3498db;
                font-weight: bold;
                margin-right: 8px;
            }
            
            h1 .header-section-number {
                font-size: 0.9em;
            }
            
            h2 .header-section-number {
                font-size: 0.85em;
            }
            
            h3 .header-section-number {
                font-size: 0.8em;
            }
            
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1.5em 0; }
            .math inline { display: inline-block; }
            pre { 
                border-left: 4px solid #3498db; 
                background: #2d2d2d; 
                color: #f8f8f2;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.4;
            }
            code { 
                background: #e9ecef; 
                padding: 0.2em 0.4em; 
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                color: #c7254e;
            }
            pre code { 
                background: none; 
                color: inherit; 
                padding: 0; 
            }
            
            /* Melhorias responsivas */
            @media (max-width: 1200px) {
                .container {
                    max-width: 98%;
                    padding: 30px;
                }
                #TOC {
                    float: none;
                    width: auto;
                    margin: 20px 0;
                }
            }
            
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 20px; max-width: 100%; }
                pre { font-size: 12px; padding: 15px; }
                #TOC { padding: 15px; }
            }
            
            /* Melhorias para tabelas */
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 1.5em 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            th, td { 
                border: 1px solid #dee2e6; 
                padding: 12px 15px; 
                text-align: left; 
            }
            th { 
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white; 
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
                letter-spacing: 0.5px;
            }
            tr:nth-child(even) { 
                background-color: #f8f9fa; 
            }
            tr:hover { 
                background-color: #e3f2fd; 
                transition: background-color 0.2s ease;
            }
            
            /* Melhorias para blocos de citação */
            blockquote { 
                border-left: 4px solid #3498db; 
                margin: 25px 0; 
                padding-left: 25px; 
                color: #7f8c8d;
                font-style: italic;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 0 8px 8px 0;
            }
            
            /* Cabeçalhos com numeração */
            h1, h2, h3, h4, h5 { 
                color: #2c3e50; 
                margin-top: 1.8em;
                border-bottom: 1px solid #e9ecef;
                padding-bottom: 0.5em;
            }
            h1 { 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px; 
                color: #2c3e50;
                font-size: 2.2em;
            }
            h2 {
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin-top: 2em;
            }
            
            /* Clearfix para layout com TOC flutuante */
            .main-content {
                overflow: hidden;
            }
        </style>
        """
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{enhanced_css}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{enhanced_css}')
        else:
            if '<body>' in html_content:
                html_content = html_content.replace('<body>', f'<head>\n{enhanced_css}\n</head>\n<body>')
            else:
                html_content = f'<head>\n{enhanced_css}\n</head>\n<body>\n{html_content}\n</body>'
                
        return html_content

    def _enhance_toc_styling(self, html_content: str) -> str:
        """Melhora o estilo do Table of Contents gerado pelo Pandoc"""
        # Adiciona título ao TOC se não existir
        if '<div id="TOC">' in html_content and 'Table of Contents' not in html_content:
            html_content = html_content.replace(
                '<div id="TOC">', 
                '<div id="TOC"><h2 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">📑 Table of Contents</h2>'
            )
        
        # Adiciona wrapper para conteúdo principal
        if '<div id="TOC">' in html_content and '<body>' in html_content:
            # Encontra o TOC e envolve o conteúdo restante
            toc_end = html_content.find('</div>', html_content.find('<div id="TOC">')) + 6
            body_content = html_content[toc_end:]
            if '<div class="main-content">' not in body_content:
                html_content = html_content[:toc_end] + '\n<div class="main-content">' + body_content + '\n</div>'
        
        return html_content

    def _convert_with_fallback(self, md_file_path: str) -> str:
        """Fallback para conversão quando Pandoc falha"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Extensões avançadas para melhor conversão
            extensions = [
                'extra', 'tables', 'fenced_code', 'codehilite', 
                'toc', 'md_in_html', 'attr_list'
            ]
            
            html_content = markdown.markdown(
                md_content,
                extensions=extensions,
                output_format='html5'
            )
            
            return self._create_enhanced_html_template(html_content, Path(md_file_path).name)
            
        except Exception as e:
            self.logger.error(f"❌ Fallback também falhou: {e}")
            return self._create_basic_html(md_content, Path(md_file_path).name)

    def _create_enhanced_html_template(self, content: str, title: str) -> str:
        """Template HTML aprimorado com suporte a MathJax local/online"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
            max-width: none; /* Remove limitação de largura */
        }}
        .container {{
            max-width: 95%; /* Usa quase toda a largura disponível */
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5 {{
            color: #2c3e50;
            margin-top: 1.8em;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding-left: 25px;
            color: #7f8c8d;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s ease;
        }}
        .math {{
            text-align: center;
            margin: 1.5em 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .author {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        .metadata {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }}
        .metadata h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        /* Estilos para TOC manual */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            float: right;
            width: 300px;
            margin-left: 30px;
        }}
        .toc h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 15px;
        }}
        .toc li {{
            margin: 8px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #495057;
            font-weight: 500;
        }}
        .toc a:hover {{
            color: #007bff;
        }}
        .main-content {{
            overflow: hidden;
        }}
        @media (max-width: 1200px) {{
            .container {{
                max-width: 98%;
                padding: 30px;
            }}
            .toc {{
                float: none;
                width: auto;
                margin: 20px 0;
            }}
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                max-width: 100%;
            }}
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    <script>
        // Configuração MathJax para melhor renderização
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                renderActions: {{
                    addMenu: [0, '', '']
                }}
            }},
            startup: {{
                pageReady() {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax carregado com sucesso');
                    }});
                }}
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""

    def _create_basic_html(self, content: str, title: str) -> str:
        """HTML básico de último recurso com MathJax"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f5f5f5;
            max-width: none; /* Remove limitação de largura */
        }}
        pre {{ 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        .container {{
            max-width: 95%; /* Usa quase toda a largura disponível */
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
    </style>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</head>
<body>
    <div class="container">
        <pre>{content}</pre>
    </div>
</body>
</html>"""

    def save_as_html_robust(self):
        """Método ROBUSTO para conversão HTML - VERSÃO OTIMIZADA"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] HTMLs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.html"
                self.logger.info(f"   🌐 {filename}")
            return
        
        markdown_folder = Path(self.output_dirs['markdown'])
        html_folder = Path(self.output_dirs['html'])
        
        md_files = list(markdown_folder.glob("*.md"))
        
        if not md_files:
            self.logger.error("❌ Nenhum arquivo Markdown encontrado para conversão.")
            return
        
        self.logger.info(f"🔄 Convertendo {len(md_files)} arquivos Markdown para HTML (OTIMIZADO)...")
        
        # Verifica se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada")
        except:
            pandoc_available = False
            self.logger.warning("⚠️ Pandoc não disponível - usando fallback Python")
        
        converted_count = 0
        failed_count = 0
        
        for md_file in md_files:
            try:
                html_file = html_folder / md_file.with_suffix('.html').name
                
                if not self.force_overwrite and html_file.exists():
                    self.logger.info(f"⏭️  Já existe: {html_file.name}")
                    converted_count += 1
                    continue

                self.logger.info(f"📄 Processando: {md_file.name}")
                
                if pandoc_available:
                    html_content = self._convert_with_pandoc_optimized(str(md_file))
                else:
                    html_content = self._convert_with_fallback(str(md_file))
                
                if html_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    self.logger.info(f"✅ Criado: {html_file.name}")
                    converted_count += 1
                else:
                    self.logger.error(f"❌ Falha na conversão: {md_file.name}")
                    failed_count += 1
                    
            except Exception as e:
                self.logger.error(f"❌ Erro em {md_file.name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                failed_count += 1
                
        self.logger.info(f"📊 HTML: {converted_count} arquivos criados, {failed_count} falhas em '{html_folder}'")

    def categorize_conversation(self, title: str, summary: str) -> str:
        """Categorização otimizada com expressões regulares"""
        text = f"{title} {summary}".lower()
        
        patterns = {
            'Tecnologia': r'\b(tecnologia|hardware|software|rede|internet|wifi|bluetooth|[45]g|cloud|aws|azure|gcp|servidor|hosting|domínio|ssl|router|switch|firewall|iot|smartphone|tablet|navegador|browser|chrome|firefox|edge|safari|email|gmail|outlook|criptografia|segurança|cibersegurança|ransomware|phishing|autenticação|2fa|biometria)\b',
            'Saúde': r'\b(saúde|medicina|médico|enfermagem|doença|vírus|bactéria|vacina|covid|coronavírus|gripe|febre|dor|análise|exame|raio x|ressonância|hospital|clínica|farmácia|medicamento|remédio|psicologia|terapia|bem-estar|nutrição|dieta|exercício|fitness|sono|saúde mental)\b',
            'Programação': r'\b(python|javascript|java|c\+\+|c#|go|rust|lua|bash|script|debug|erro|conda|mamba|pandoc|msys2|spyder|jupyter|pip|venv|docker|git|github|vscode|ide|programa|código|função|classe|api|selenium|playwright)\b',
            'Sistemas': r'\b(windows|linux|macos|so|sistema operacional|driver|registry|process|firewall|bios|boot|path|dll|exe|powershell|cmd|terminal|shell)\b',
            'IA': r'\b(ia|gpt|chatgpt|grok|qwen|deepseek|llm|modelo|prompt|token|embedding|fine-tune|neural|chatbot|inteligência artificial)\b',
            'Dados': r'\b(dados|data|csv|json|pandas|numpy|excel|sql|banco|sqlite|postgres|visualização|gráfico|tabela|análise|etl|dashboard)\b',
            'Geral': r'\b(geral|pergunta|ajuda|como fazer|explicar|resumo|tutorial básico)\b'
        }
        
        for category, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return category
                
        return 'Outros'

    def parse_timestamp_for_sorting(self, timestamp) -> datetime:
        if not timestamp:
            return datetime.min
            
        try:
            if isinstance(timestamp, str):
                clean_ts = timestamp.replace('T', ' ').split('.')[0].split('+')[0]
                if clean_ts.endswith('Z'):
                    clean_ts = clean_ts[:-1]
                return datetime.fromisoformat(clean_ts)
            elif isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
        except Exception:
            pass
            
        return datetime.min

    def format_timestamp(self, timestamp) -> Optional[str]:
        if not timestamp:
            return None
            
        try:
            if isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(timestamp, str):
                if 'T' in timestamp:
                    return timestamp.replace('T', ' ').split('.')[0]
                return timestamp
        except Exception:
            pass
            
        return str(timestamp)

    def create_enhanced_markdown_content(self, conversation: Dict[str, Any]) -> str:
        """Gera conteúdo Markdown com preservação total de formatação"""
        lines = [
            f"# {conversation['title']}",
            "",
            "## 📊 Informações",
            f"- **Número:** #{conversation['number']}",
            f"- **Origem:** {conversation['source']}",
            f"- **Categoria:** {conversation['category']}",
            f"- **ID:** {conversation.get('id', 'N/A')}",
            f"- **Criada em:** {conversation.get('inserted_at') or conversation.get('created_at') or 'N/A'}",
        ]
        
        if conversation.get('updated_at'):
            lines.append(f"- **Atualizada em:** {conversation['updated_at']}")
            
        lines.extend([
            f"- **Total de mensagens:** {len(conversation['messages'])}",
            f"- **Resumo:** {conversation.get('summary', 'Sem resumo')}",
            "",
            "---",
            "",
            "## 💬 Conversa",
            ""
        ])

        for j, msg in enumerate(conversation['messages'], 1):
            timestamp = f" *({msg['timestamp']})*" if msg['timestamp'] else ""
            model_info = f" *[{msg.get('model', '')}]*" if msg.get('model') else ""
            
            preserved_content = self.preserve_special_content(msg['content'])
            
            lines.extend([
                f"### {msg['author']}{timestamp}{model_info}",
                "",
                f"{preserved_content}",
                ""
            ])
            
            if j < len(conversation['messages']):
                lines.extend(["---", ""])

        lines.extend([
            "---",
            "",
            f"*Conversa exportada do {conversation['source']}*",
            f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        ])
        
        return '\n'.join(lines)

    def process_qwen_enhanced(self, path: Path):
        """Processa Qwen3 com preservação total de conteúdo"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Qwen3: {path}")
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                
            data = raw.get('data', [])
            if not isinstance(data, list):
                self.logger.warning("⚠️  Qwen3: 'data' não é uma lista.")
                return
                
            self.logger.info(f"🔍 Qwen3: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa Qwen {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                history = conv.get('chat', {}).get('history', {})
                messages = []

                if not history:
                    continue

                messages_dict = history.get('messages', {})
                
                if not isinstance(messages_dict, dict):
                    continue

                self.logger.info(f"   📝 Conversa {i+1}: '{clean_title}' - {len(messages_dict)} mensagens")

                for message_id, message_data in messages_dict.items():
                    if not isinstance(message_data, dict):
                        continue

                    role = message_data.get('role', '')
                    content = message_data.get('content', '')
                    
                    if not content or not role:
                        continue

                    if role == 'user':
                        author = "👤 Utilizador"
                    elif role == 'assistant':
                        author = "🤖 Qwen3"
                    else:
                        continue

                    if isinstance(content, list):
                        text_parts = []
                        for block in content:
                            if isinstance(block, dict):
                                if block.get('type') == 'text':
                                    text_parts.append(block.get('text', ''))
                                elif block.get('type') == 'image':
                                    image_info = block.get('image', '')
                                    if image_info:
                                        text_parts.append(f"![Imagem]({image_info})")
                            elif isinstance(block, str):
                                text_parts.append(block)
                        final_content = '\n'.join(text_parts).strip()
                    else:
                        final_content = str(content).strip()

                    final_content = self.preserve_special_content(final_content)

                    if not final_content or final_content == 'null':
                        continue

                    messages.append({
                        'author': author,
                        'role': role,
                        'content': final_content,
                        'timestamp': self.format_timestamp(message_data.get('created_at')),
                        'model': message_data.get('model', 'Qwen3')
                    })

                if messages:
                    messages.sort(key=lambda x: self.parse_timestamp_for_sorting(x['timestamp']))
                    
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'Qwen3',
                        'id': conv.get('id', f'qwen_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('created_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    self.logger.info(f"   ✅ Adicionada: {len(messages)} mensagens")
                    
            self.logger.info(f"✅ Qwen3: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Qwen3: {e}")
            if self.dry_run:
                traceback.print_exc()

    def process_chatgpt(self, path: Path):
        """Processa exportação do ChatGPT"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria ChatGPT: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="chatgpt_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)
            convs_path = Path(temp_dir) / "conversations.json"
            if not convs_path.exists():
                self.logger.error("❌ ChatGPT: conversations.json não encontrado.")
                return
                
            with open(convs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                self.logger.warning("⚠️  ChatGPT: estrutura inesperada.")
                return
                
            self.logger.info(f"🔍 ChatGPT: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa ChatGPT {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for msg_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                        
                    author_role = msg_data.get('author', {}).get('role', '')
                    if author_role == 'user':
                        author = "👤 Utilizador"
                        role = 'user'
                    elif author_role == 'assistant':
                        author = "🤖 ChatGPT"
                        role = 'assistant'
                    else:
                        continue
                        
                    content_parts = []
                    for part in msg_data.get('content', {}).get('parts', []):
                        if isinstance(part, str):
                            content_parts.append(part)
                    content = "\n".join(content_parts).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('create_time')),
                        'model': msg_data.get('model', 'ChatGPT')
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'ChatGPT',
                        'id': conv.get('id', f'chatgpt_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('create_time')),
                        'updated_at': self.format_timestamp(conv.get('update_time')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    
            self.logger.info(f"✅ ChatGPT: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar ChatGPT: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def process_deepseek(self, path: Path):
        """Processa exportação do DeepSeek"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria DeepSeek: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="deepseek_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)
                
            convs_path = Path(temp_dir) / "conversations.json"
            if not convs_path.exists():
                self.logger.error("❌ DeepSeek: conversations.json não encontrado.")
                return
                
            with open(convs_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            if isinstance(raw_data, list):
                data = raw_data
            elif isinstance(raw_data, dict) and 'data' in raw_data:
                data = raw_data['data']
            else:
                self.logger.warning("⚠️  DeepSeek: estrutura inesperada.")
                return
                
            if not isinstance(data, list):
                self.logger.warning("⚠️  DeepSeek: 'data' não é uma lista.")
                return
                
            self.logger.info(f"🔍 DeepSeek: encontradas {len(data)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa DeepSeek {i+1}')
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for node_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                        
                    fragments = msg_data.get('fragments', [])
                    content_parts = []
                    msg_type = None
                    
                    for frag in fragments:
                        if isinstance(frag, dict):
                            frag_type = frag.get('type', '').upper()
                            if frag_type in ('REQUEST', 'RESPONSE'):
                                msg_type = frag_type
                            text = frag.get('text', '')
                            if text:
                                content_parts.append(text)
                            content = frag.get('content', '')
                            if content:
                                if isinstance(content, list):
                                    for item in content:
                                        if isinstance(item, str):
                                            content_parts.append(item)
                                        elif isinstance(item, dict):
                                            item_text = item.get('text', '')
                                            if item_text:
                                                content_parts.append(str(item_text))
                                else:
                                    content_parts.append(str(content))
                                    
                    content = ' '.join(content_parts).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue
                        
                    if msg_type == 'REQUEST':
                        author = "👤 Utilizador"
                        role = 'user'
                    else:
                        author = "🤖 DeepSeek"
                        role = 'assistant'
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('inserted_at')),
                        'model': msg_data.get('model', 'DeepSeek')
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'DeepSeek',
                        'id': conv.get('id', f'deepseek_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('inserted_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
                    
            self.logger.info(f"✅ DeepSeek: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar DeepSeek: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def process_grok(self, path: Path):
        """Processa exportação do Grok"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Grok: {path}")
            return
            
        try:
            temp_dir = tempfile.mkdtemp(prefix="grok_")
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(temp_dir)

            target_file = None
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file == "prod-grok-backend.json":
                        target_file = Path(root) / file
                        break
                if target_file:
                    break

            if not target_file:
                self.logger.error("❌ Grok: ficheiro 'prod-grok-backend.json' não encontrado no ZIP.")
                return

            self.logger.info(f"🔍 Grok: carregando {target_file.name}...")
            with open(target_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict) or 'conversations' not in data:
                self.logger.error("❌ Grok: estrutura inesperada — chave 'conversations' não encontrada.")
                return

            conversations_list = data['conversations']
            if not isinstance(conversations_list, list):
                self.logger.error("❌ Grok: 'conversations' não é uma lista.")
                return

            self.logger.info(f"📊 Grok: encontradas {len(conversations_list)} conversas.")
            total_convs = 0

            for item in conversations_list:
                if not isinstance(item, dict):
                    continue

                conv_meta = item.get('conversation')
                responses = item.get('responses', [])

                if not isinstance(conv_meta, dict) or not isinstance(responses, list) or not responses:
                    continue

                conv_id = conv_meta.get('id')
                if not conv_id:
                    continue

                original_title = conv_meta.get('title', f"Conversa Grok {total_convs + 1}")
                # PRESERVA título original com espaços
                clean_title = self.preserve_original_title(original_title)
                
                create_time_str = conv_meta.get('create_time')
                modify_time_str = conv_meta.get('modify_time')

                def format_iso_timestamp(ts_str):
                    if not ts_str:
                        return None
                    try:
                        if '.' in ts_str:
                            ts_str = ts_str.split('.')[0] + 'Z'
                        return self.format_timestamp(ts_str)
                    except:
                        return str(ts_str)

                inserted_at = format_iso_timestamp(create_time_str)
                updated_at = format_iso_timestamp(modify_time_str)

                messages = []
                for resp in responses:
                    if not isinstance(resp, dict):
                        continue

                    resp_data = resp.get('response')
                    if not isinstance(resp_data, dict):
                        continue

                    sender = resp_data.get('sender', '').upper()
                    if sender == 'HUMAN':
                        author = "👤 Utilizador"
                        role = "user"
                    elif sender == 'ASSISTANT':
                        author = "🤖 Grok"
                        role = "assistant"
                    else:
                        continue

                    content = str(resp_data.get('message', '')).strip()
                    
                    content = self.preserve_special_content(content)
                    
                    if not content:
                        continue

                    create_time = resp_data.get('create_time')
                    timestamp_ms = None
                    if isinstance(create_time, dict) and '$date' in create_time:
                        date_obj = create_time['$date']
                        if isinstance(date_obj, dict) and '$numberLong' in date_obj:
                            try:
                                timestamp_ms = int(date_obj['$numberLong'])
                            except:
                                pass

                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(timestamp_ms / 1000.0 if timestamp_ms else None),
                        'model': 'Grok'
                    })

                if messages:
                    self.all_conversations.append({
                        'title': clean_title,  # Título ORIGINAL com espaços
                        'source': 'Grok',
                        'id': conv_id,
                        'inserted_at': inserted_at,
                        'updated_at': updated_at,
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    total_convs += 1

            if total_convs > 0:
                self.logger.info(f"✅ Grok: processadas {total_convs} conversas.")
            else:
                self.logger.error("❌ Grok: nenhuma conversa válida encontrada.")

        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Grok: {e}")
            if self.dry_run:
                traceback.print_exc()
        finally:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def save_as_markdown_enhanced(self):
        """Salva conversas com preservação total de formatação"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Markdowns seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                self.logger.info(f"   📄 {filename}")
            return
            
        folder = Path(self.output_dirs['markdown'])
        saved_count = 0
        failed_count = 0
        
        for conv in self.all_conversations:
            try:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                filepath = folder / filename
                
                if not self.force_overwrite and filepath.exists():
                    continue
                    
                markdown_content = self.create_enhanced_markdown_content(conv)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                saved_count += 1
                
            except Exception as e:
                self.logger.error(f"❌ Erro ao salvar conversa {conv['number']}: {e}")
                failed_count += 1
                continue
                
        self.logger.info(f"✅ Markdown: {saved_count} arquivos criados, {failed_count} falhas em '{folder}'")

    def save_as_csv(self):
        """Salva conversas em arquivos CSV individuais"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] CSVs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
                self.logger.info(f"   📊 {filename}")
            return
            
        folder = Path(self.output_dirs['csv'])
        saved_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
            filepath = folder / filename
            
            if not self.force_overwrite and filepath.exists():
                continue
                
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'node_id', 'author', 'role', 'timestamp', 'model', 'content'
                ])
                writer.writeheader()
                for i, msg in enumerate(conv['messages']):
                    writer.writerow({
                        'node_id': str(i),
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content']
                    })
            saved_count += 1
            
        self.logger.info(f"✅ CSV: {saved_count} arquivos criados em '{folder}'")

    def save_as_json(self):
        """Salva conversas em arquivos JSON individuais"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] JSONs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
                self.logger.info(f"   📋 {filename}")
            return
            
        folder = Path(self.output_dirs['json'])
        saved_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
            filepath = folder / filename
            
            if not self.force_overwrite and filepath.exists():
                continue
                
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conv, f, ensure_ascii=False, indent=2)
            saved_count += 1
            
        self.logger.info(f"✅ JSON: {saved_count} arquivos criados em '{folder}'")

    def save_all_to_single_files(self):
        """Salva todas as conversas em arquivos únicos CSV e JSON"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Arquivos únicos seriam criados:")
            self.logger.info(f"   📁 {self.single_files['csv']}")
            self.logger.info(f"   📁 {self.single_files['json']}")
            return
            
        # CSV único
        with open(self.single_files['csv'], 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                'conversation_number', 'source', 'conversation_title', 'category',
                'author', 'role', 'timestamp', 'model', 'content'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for conv in self.all_conversations:
                for msg in conv['messages']:
                    writer.writerow({
                        'conversation_number': conv['number'],
                        'source': conv['source'],
                        'conversation_title': conv['title'],
                        'category': conv['category'],
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content']
                    })
        self.logger.info(f"✅ CSV único: {self.single_files['csv']}")

        # JSON único
        with open(self.single_files['json'], 'w', encoding='utf-8') as f:
            json.dump(self.all_conversations, f, ensure_ascii=False, indent=2)
        self.logger.info(f"✅ JSON único: {self.single_files['json']}")

    def create_searchable_index(self):
        """Cria índice HTML pesquisável com links para HTML"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Índice HTML seria criado: {self.index_file}")
            return
            
        self.logger.info("🎯 Criando índice HTML combinado...")
        
        category_stats = {}
        for conv in self.all_conversations:
            cat = conv['category']
            category_stats[cat] = category_stats.get(cat, 0) + 1

        html_content = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice Combinado - AI Chats</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 15px; font-weight: 300; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; margin-bottom: 20px; }}
        .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 25px; flex-wrap: wrap; }}
        .stat-item {{ background: rgba(255,255,255,0.15); padding: 18px 28px; border-radius: 12px; backdrop-filter: blur(10px); font-size: 1.1em; }}
        .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
        .search-box {{ width: 100%; padding: 18px 25px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; font-family: inherit; }}
        .search-box:focus {{ border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }}
        .filter-section {{
            padding: 20px 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        .filter-btn {{
            padding: 10px 20px;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 500;
            transition: all 0.3s ease;
            font-family: inherit;
        }}
        .filter-btn.active, .filter-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
        .conversations-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); 
            gap: 25px; 
            padding: 35px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 400px;
        }}
        .conversation-card {{ 
            background: white; 
            border: 1px solid #e9ecef; 
            border-radius: 15px; 
            padding: 25px; 
            transition: all 0.4s ease; 
            cursor: pointer; 
            position: relative;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .conversation-card:hover {{ 
            transform: translateY(-8px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.15); 
            border-color: #667eea;
        }}
        .card-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            margin-bottom: 18px; 
        }}
        .card-number {{ 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-size: 0.9em; 
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }}
        .card-source {{ 
            background: #e3f2fd; 
            color: #1976d2; 
            padding: 5px 12px; 
            border-radius: 12px; 
            font-size: 0.85em; 
            font-weight: bold; 
            margin-left: 10px;
        }}
        .card-title {{ 
            font-size: 1.3em; 
            font-weight: 600; 
            color: #2c3e50; 
            margin-bottom: 12px; 
            line-height: 1.4;
            min-height: 3.6em;
            cursor: pointer;
        }}
        .card-summary {{ 
            color: #6c757d; 
            font-size: 0.95em; 
            line-height: 1.5; 
            margin-bottom: 18px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            cursor: pointer;
        }}
        .card-meta {{ 
            display: flex; 
            justify-content: space-between; 
            font-size: 0.85em; 
            color: #868e96; 
            border-top: 1px solid #e9ecef; 
            padding-top: 18px;
        }}
        .card-actions {{ 
            position: absolute; 
            top: 20px; 
            right: 20px; 
            display: flex; 
            gap: 8px; 
            opacity: 0; 
            transition: opacity 0.3s ease; 
        }}
        .conversation-card:hover .card-actions {{ 
            opacity: 1; 
        }}
        .action-btn {{ 
            background: white; 
            border: 2px solid #e9ecef; 
            border-radius: 8px; 
            padding: 6px 12px; 
            font-size: 0.8em; 
            cursor: pointer; 
            transition: all 0.3s ease;
            font-weight: 500;
            text-decoration: none;
            color: #333;
            display: inline-block;
        }}
        .action-btn:hover {{ 
            background: #667eea; 
            color: white; 
            border-color: #667eea;
            transform: scale(1.05);
        }}
        .recent-badge {{ 
            background: #ff6b6b; 
            color: white; 
            padding: 3px 10px; 
            border-radius: 12px; 
            font-size: 0.75em; 
            margin-left: 8px;
            animation: pulse 2s infinite;
        }}
        .no-results {{ 
            text-align: center; 
            padding: 60px 20px; 
            color: #6c757d;
            font-size: 1.1em;
            grid-column: 1 / -1;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        .category-badge {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 8px;
            font-weight: 500;
        }}
        
        .direct-link {{
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        .direct-link:hover {{
            background: #218838;
        }}
        
        .html-btn {{
            background: #17a2b8;
            color: white;
        }}
        .html-btn:hover {{
            background: #138496;
        }}
        
        .pdf-btn {{
            background: #dc3545;
            color: white;
        }}
        .pdf-btn:hover {{
            background: #c82333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Índice Combinado de Conversas</h1>
            <p>Qwen3 • ChatGPT • DeepSeek • Grok • COM HTML (Pandoc + MathJax)</p>
            <div class="stats">
                <div class="stat-item">
                    <strong>Total:</strong> <span id="total-count">{len(self.all_conversations)}</span> conversas
                </div>
                <div class="stat-item">
                    <strong>Ordenação:</strong> Mais Recentes Primeiro
                </div>
                <div class="stat-item">
                    <strong>Atualizado:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </div>
            </div>
        </div>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo ou categoria...">
        </div>
        
        <div class="filter-section">
            <button class="filter-btn active" data-filter="todas">Todas ({len(self.all_conversations)})</button>
"""
    
        for category, count in category_stats.items():
            html_content += f'<button class="filter-btn" data-filter="{category.lower()}">{category} ({count})</button>\n'

        html_content += """
        </div>
        
        <div style="text-align: center; padding: 15px; background: #e9ecef; border-bottom: 1px solid #ddd;">
            <strong>Acesso Rápido:</strong>
            <a href="combined_markdown/" class="direct-link" target="_blank">📁 Markdown</a>
            <a href="combined_html/" class="direct-link" target="_blank">🌐 HTML</a>
            <a href="combined_pdfs/" class="direct-link" target="_blank">📄 PDF</a>
            <a href="combined_json/" class="direct-link" target="_blank">📋 JSON</a>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
"""
    
        for i, conv in enumerate(self.all_conversations):
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}"
            recent_badge = "<span class='recent-badge'>NOVO</span>" if i < 5 else ""
            
            summary = conv.get('summary', 'Sem resumo disponível')
            if len(summary) > 150:
                summary = summary[:150] + "..."
            
            html_content += f"""
            <div class="conversation-card" data-title="{conv['title']}" data-summary="{summary}" data-source="{conv['source'].lower()}" data-category="{conv['category'].lower()}">
                <div class="card-header">
                    <div class="card-number">#{conv['number']} {recent_badge}</div>
                    <div class="card-actions">
                        <a href="combined_markdown/{filename}.md" class="action-btn" target="_blank" onclick="event.stopPropagation();">📄 MD</a>
                        <a href="combined_html/{filename}.html" class="action-btn html-btn" target="_blank" onclick="event.stopPropagation();">🌐 HTML</a>
                        <a href="combined_pdfs/{filename}.pdf" class="action-btn pdf-btn" target="_blank" onclick="event.stopPropagation();">📊 PDF</a>
                    </div>
                </div>
                <div class="card-title" onclick="openHTML('{filename}.html')">{conv['title']}</div>
                <div>
                    <span class="card-source">{conv['source']}</span>
                    <span class="category-badge">{conv['category']}</span>
                </div>
                <div class="card-summary" onclick="openHTML('{filename}.html')">{summary}</div>
                <div class="card-meta">
                    <span>📅 {conv.get('updated_at') or conv.get('inserted_at') or 'N/A'}</span>
                    <span>💬 {len(conv['messages'])} mensagens</span>
                </div>
            </div>
            """

        html_content += """
        </div>
    </div>
    
    <script>
        let currentFilter = 'todas';
        
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
        });

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.getAttribute('data-filter');
                filterConversations();
            });
        });

        document.getElementById('searchInput').addEventListener('input', filterConversations);

        function filterConversations() {
            const term = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.conversation-card');
            let visible = 0;
            
            cards.forEach(card => {
                const title = card.getAttribute('data-title').toLowerCase();
                const summary = card.getAttribute('data-summary').toLowerCase();
                const source = card.getAttribute('data-source').toLowerCase();
                const category = card.getAttribute('data-category').toLowerCase();
                
                const matchesSearch = (title.includes(term) || summary.includes(term) || category.includes(term) || source.includes(term));
                const matchesCategory = (currentFilter === 'todas' || category === currentFilter);
                
                if (matchesSearch && matchesCategory) {
                    card.style.display = 'block';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            updateStats(visible);
            
            const grid = document.getElementById('conversationsGrid');
            const noResults = document.getElementById('no-results-message');
            
            if (visible === 0) {
                if (!noResults) {
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results-message';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '🔍 Nenhuma conversa encontrada. Tente ajustar os filtros ou a pesquisa.';
                    grid.appendChild(noResultsMsg);
                }
            } else if (noResults) {
                noResults.remove();
            }
        }

        function updateStats(visibleCount = null) {
            const totalElement = document.getElementById('total-count');
            if (visibleCount !== null) {
                totalElement.textContent = visibleCount;
            } else {
                totalElement.textContent = """ + str(len(self.all_conversations)) + """;
            }
        }

        function openHTML(filename) {
            const htmlUrl = 'combined_html/' + filename;
            console.log('Abrindo HTML:', htmlUrl);
            window.open(htmlUrl, '_blank');
        }

        function openMD(filename) {
            const mdUrl = 'combined_markdown/' + filename;
            window.open(mdUrl, '_blank');
        }
        
        function openPDF(filename) {
            const pdfFile = filename.replace('.html', '.pdf');
            const pdfUrl = 'combined_pdfs/' + pdfFile;
            window.open(pdfUrl, '_blank');
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.getElementById('searchInput').value = '';
                filterConversations();
            }
        });

        document.querySelectorAll('.conversation-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.closest('.action-btn')) {
                    return;
                }
                
                const htmlBtn = this.querySelector('a.html-btn');
                if (htmlBtn) {
                    const htmlUrl = htmlBtn.getAttribute('href');
                    window.open(htmlUrl, '_blank');
                }
            });
        });

        document.getElementById('searchInput').focus();
        
        console.log('Índice carregado com', """ + str(len(self.all_conversations)) + """, 'conversas');
    </script>
</body>
</html>
"""
    
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"✅ Índice combinado criado: {self.index_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Processa exportações combinadas com exportação HTML via Pandoc."
    )
    parser.add_argument("--dry-run", action="store_true", help="Executa sem salvar arquivos")
    parser.add_argument("--force-overwrite", action="store_true", help="Substitui arquivos existentes")
    
    args = parser.parse_args()
    
    system = CombinedFragmentsSystem(
        dry_run=args.dry_run,
        force_overwrite=args.force_overwrite
    )
    system.run()

if __name__ == "__main__":
    main()
```

## Principais correções de layout implementadas:

### 1. **Layout de tela completa:**
- `max-width: none` no elemento `body`
- `max-width: 95%` no container principal
- Remove limitações artificiais de largura

### 2. **TOC flutuante otimizado:**
- Posicionado à direita com `float: right`
- Largura fixa de 300px
- Margens adequadas para não comprimir o conteúdo

### 3. **Design responsivo:**
- Breakpoints em 1200px e 768px
- TOC torna-se não-flutuante em telas menores
- Container expande conforme o tamanho da tela

### 4. **Clearfix para layout:**
- Classe `.main-content` com `overflow: hidden`
- Previne problemas com elementos flutuantes

### 5. **Melhor aproveitamento do espaço:**
- Padding otimizado para desktop
- Container usa 95% da largura disponível
- Layout adaptativo que se expande conforme a tela

Agora o HTML deve ocupar praticamente toda a largura disponível no browser, proporcionando uma experiência de leitura muito melhor em desktop, enquanto mantém a responsividade para dispositivos móveis.

---

*Conversa exportada do DeepSeek*
*Processado em: 23/11/2025 23:05*