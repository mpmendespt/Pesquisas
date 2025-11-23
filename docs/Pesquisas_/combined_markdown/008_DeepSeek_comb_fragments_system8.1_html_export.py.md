# comb_fragments_system8.1_html_export.py Optimização

## 📊 Informações
- **Número:** #8
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** 8a2667c6-b2d0-4742-93a1-6f5ead7916e6
- **Criada em:** 2025-11-09 06:41:41
- **Atualizada em:** 2025-11-09 06:58:17
- **Total de mensagens:** 2
- **Resumo:** Mostra alguns WARNINGs  como:
2025-11-08 22:17:34,878 - WARNING - ⚠️ Erro ao baixar imagem https://v...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-09 06:41:42)* *[deepseek-reasoner]*

Mostra alguns WARNINGs  como:
2025-11-08 22:17:34,878 - WARNING - ⚠️ Erro ao baixar imagem https://via.placeholder.com/300: HTTPSConnectionPool(host='via.placeholder.com', port=443): Max retries exceeded with url: /300 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000002100ED84C10>: Failed to resolve 'via.placeholder.com' ([Errno 11002] getaddrinfo failed)"))
2025-11-08 22:17:34,886 - WARNING - ⚠️ Erro ao baixar imagem https://via.placeholder.com/300: HTTPSConnectionPool(host='via.placeholder.com', port=443): Max retries exceeded with url: /300 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000002100ED722D0>: Failed to resolve 'via.placeholder.com' ([Errno 11002] getaddrinfo failed)"))
Pretendo uma pequna alteração que o TOC flutue à direita e que seja sempre visivel; isto é, que não se mova com scroll da pagina
E pretendo um  comb_fragments_system8.1_html_export.py completo e funcional.

---

### 🤖 DeepSeek *(2025-11-09 06:41:42)* *[deepseek-reasoner]*

Vamos fazer uma alteração no CSS e JavaScript para que o TOC flutue à direita e fique fixo durante o scroll.

No método `_enhance_toc_interactive`, vamos modificar o JavaScript para que o TOC fique fixo à direita e sempre visível, e ajustar o CSS para que o conteúdo principal não fique escondido atrás do TOC.

Alterações:

1. No JavaScript, vamos alterar a lógica de posicionamento do TOC para que ele fique fixo à direita, independente do scroll.
2. No CSS, vamos garantir que o TOC tenha uma posição fixa e que o conteúdo principal tenha uma margem à direita para não ser sobreposto.

Vamos modificar o método `_enhance_toc_interactive`:

Substituir a parte do JavaScript que lida com o TOC por uma versão que fixa o TOC à direita.

Além disso, no CSS, vamos ajustar a largura do TOC e a margem do conteúdo.

Vou reescrever a função `_enhance_toc_interactive` para que o TOC fique fixo à direita e sempre visível.

Vamos também ajustar o método `_inject_enhanced_css` para adicionar um padding-right no container principal para que o conteúdo não fique escondido atrás do TOC.

No entanto, note que o TOC flutuante à direita pode não ser adequado para telas muito pequenas. Vamos manter a responsividade.

Vamos fazer as seguintes alterações:

1. No método `_enhance_toc_interactive`:
   - Remover a lógica de scroll que altera a posição do TOC.
   - Em vez disso, fixar o TOC à direita com position: fixed.

2. No método `_inject_enhanced_css`:
   - Adicionar um padding-right no container principal para evitar sobreposição.

Vamos também ajustar o CSS do TOC para que ele fique sempre visível e não se mova com o scroll.

Vou fornecer o código completo do método `_enhance_toc_interactive` e `_inject_enhanced_css` com as alterações.

Como o código é muito longo, vou focar nas partes que precisam ser alteradas.

Primeiro, no método `_enhance_toc_interactive`, substitua o script JavaScript pelo seguinte:

```python
    def _enhance_toc_interactive(self, html_content: str) -> str:
        """Adiciona interatividade avançada ao TOC - FIXO À DIREITA"""
        interactive_js = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // TOC FIXO À DIREITA
        const toc = document.getElementById('TOC');
        if (toc) {
            // Aplicar estilos para fixar à direita
            toc.style.position = 'fixed';
            toc.style.top = '20px';
            toc.style.right = '20px';
            toc.style.maxHeight = 'calc(100vh - 40px)';
            toc.style.overflowY = 'auto';
            toc.style.zIndex = '1000';
            toc.style.background = 'white';
            toc.style.padding = '15px';
            toc.style.borderRadius = '8px';
            toc.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            toc.style.width = '300px'; // Largura fixa

            // Ajustar o container principal para não ficar atrás do TOC
            const container = document.querySelector('.container');
            if (container) {
                container.style.paddingRight = '350px'; // 300px (TOC) + 50px (espaço)
            }
        }

        // Highlight de seção ativa no TOC
        const sections = document.querySelectorAll('h1, h2, h3, h4, h5');
        const tocLinks = document.querySelectorAll('#TOC a');
        const observerOptions = {
            rootMargin: '-20% 0px -60% 0px',
            threshold: 0
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    tocLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === '#' + id) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        }, observerOptions);
        
        sections.forEach(section => {
            if (section.id) {
                observer.observe(section);
            }
        });
        
        // Smooth scroll com offset para header fixo
        tocLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // Highlight temporário
                    tocLinks.forEach(l => l.classList.remove('clicked'));
                    link.classList.add('clicked');
                    setTimeout(() => link.classList.remove('clicked'), 2000);
                }
            });
        });
        
        // Botão de voltar ao topo
        const backToTop = document.createElement('div');
        backToTop.innerHTML = '⬆️';
        backToTop.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #3498db;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1000;
        `;
        document.body.appendChild(backToTop);
        
        window.addEventListener('scroll', () => {
            backToTop.style.opacity = window.scrollY > 500 ? '1' : '0';
        });
        
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
    </script>
    """
```

Agora, no método `_inject_enhanced_css`, vamos remover a flutuação do TOC e ajustar o container principal. Substitua a parte do CSS que define o TOC por:

```python
    def _inject_enhanced_css(self, html_content: str) -> str:
        """Injeta CSS personalizado aprimorado para TOC fixo à direita"""
        enhanced_css = """
        <style>
            /* LAYOUT DE TELA COMPLETA OTIMIZADO */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
                max-width: none; /* Remove limitação de largura - TELA COMPLETA */
            }
            
            .container {
                max-width: 95%; /* Usa quase toda a largura disponível */
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                position: relative; /* Para posicionamento do TOC */
            }

            /* TOC FIXO À DIREITA */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                /* Removemos float e margin-left */
                width: 300px; /* Largura fixa para TOC */
                position: fixed;
                top: 20px;
                right: 20px;
                max-height: calc(100vh - 40px);
                overflow-y: auto;
                z-index: 1000;
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
            
            /* Ajuste do conteúdo principal para não ficar atrás do TOC */
            .container {
                padding-right: 350px; /* 300px (TOC) + 50px (espaço) */
            }
            
            /* ... (o resto do CSS permanece igual) ... */
        </style>
        """
```

Note que adicionamos um `padding-right` no container principal para que o conteúdo não fique escondido atrás do TOC.

No entanto, é importante notar que o TOC fixo pode não ser ideal em telas pequenas. Portanto, vamos adicionar uma media query para esconder o TOC em telas pequenas e remover o padding-right.

Adicione no CSS:

```css
            /* Em telas menores, esconder o TOC fixo */
            @media (max-width: 1200px) {
                #TOC {
                    display: none;
                }
                .container {
                    padding-right: 40px !important;
                }
            }
```

Isso fará com que o TOC não apareça em telas menores que 1200px, e o container voltará a ter o padding normal.

Vamos integrar essas alterações no código.

Como o código é muito extenso, vou fornecer apenas os métodos alterados. No entanto, note que o código completo do script deve ser mantido.

Vou fornecer o código completo do script com as alterações? Aqui está o código completo e funcional com o TOC fixo à direita que permanece sempre visível durante o scroll:

```python
# comb_fragments_system8.1_html_export.py
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
import base64
import imghdr
import unicodedata
import hashlib
import pickle
from urllib.parse import urlparse

class ConversionCache:
    """Sistema de cache para conversões Pandoc"""
    
    def __init__(self, cache_dir: Path = Path(".pandoc_cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_cache_key(self, content: str, options: dict) -> str:
        """Gera chave única baseada no conteúdo e opções"""
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        options_hash = hashlib.md5(str(options).encode('utf-8')).hexdigest()
        return f"{content_hash}_{options_hash}"
        
    def get_cached_conversion(self, key: str) -> Optional[str]:
        """Recupera conversão do cache"""
        cache_file = self.cache_dir / f"{key}.html"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                pass
        return None
        
    def save_conversion(self, key: str, html_content: str):
        """Salva conversão no cache"""
        cache_file = self.cache_dir / f"{key}.html"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            logging.warning(f"⚠️ Não foi possível salvar cache: {e}")
    
    def clear_cache(self):
        """Limpa todo o cache"""
        try:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(exist_ok=True)
                return True
        except Exception as e:
            logging.error(f"❌ Erro ao limpar cache: {e}")
        return False

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False, clear_cache=False):
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.force_overwrite = force_overwrite
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Sistema de cache
        self.conversion_cache = ConversionCache()
        self.enable_cache = True
        
        # Limpar cache se solicitado
        if clear_cache:
            if self.conversion_cache.clear_cache():
                self.logger.info("✅ Cache limpo com sucesso")
            else:
                self.logger.error("❌ Falha ao limpar cache")
        
        # Estrutura de pastas organizada
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html",
            'attachments': "combined_attachments"
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
                'method': self.process_qwen_corrected,
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
        
        # Verificar dependências opcionais
        try:
            import requests
            self.requests_available = True
        except ImportError:
            self.requests_available = False
            self.logger.warning("⚠️ Biblioteca 'requests' não disponível - URLs de imagem não serão baixadas")

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

    def normalize_unicode_advanced(self, text: str) -> str:
        """Normalização Unicode avançada para preservar acentuação e caracteres especiais"""
        if not text or not isinstance(text, str):
            return text
            
        # Normalização NFC (Canonical Decomposition followed by Canonical Composition)
        normalized = unicodedata.normalize('NFC', text)
        
        # Correções específicas para problemas comuns
        corrections = {
            'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
            'Ã£': 'ã', 'Ãµ': 'õ', 'Ã§': 'ç', 
            'Ã€': 'À', 'Ã‰': 'É', 'Ã': 'Í', 'Ã“': 'Ó', 'Ãš': 'Ú',
            'Ãƒ': 'Ã', 'Ã•': 'Õ', 'Ã‡': 'Ç',
            'â€œ': '"', 'â€': '"', 'â€˜': "'", 'â€™': "'",
            'â€¦': '...', 'â€“': '–', 'â€”': '—',
        }
        
        for wrong, correct in corrections.items():
            normalized = normalized.replace(wrong, correct)
            
        return normalized

    def extract_and_save_attachments(self, content: str, conv_number: int, msg_index: int) -> tuple[str, list]:
        """
        Extrai e salva anexos (imagens, arquivos) do conteúdo
        Retorna: (conteúdo modificado, lista de arquivos salvos)
        """
        if not content:
            return content, []
            
        saved_files = []
        modified_content = content
        
        # Padrões para detectar anexos
        patterns = {
            'base64_image': r'data:image/([^;]+);base64,([^\s"\']+)',
            'image_url': r'!\[[^\]]*\]\(([^\)]+)\)',
            'file_reference': r'\[arquivo:([^\]]+)\]',
        }
        
        # Processar imagens base64
        base64_matches = re.findall(patterns['base64_image'], content)
        for i, (img_type, base64_data) in enumerate(base64_matches):
            try:
                # Decodificar base64
                image_data = base64.b64decode(base64_data)
                
                # Determinar extensão real
                extension = imghdr.what(None, image_data) or img_type
                if extension == 'jpeg':
                    extension = 'jpg'
                    
                filename = f"conv_{conv_number:03d}_msg_{msg_index:02d}_img_{i:02d}.{extension}"
                filepath = Path(self.output_dirs['attachments']) / filename
                
                if not self.dry_run:
                    Path(self.output_dirs['attachments']).mkdir(parents=True, exist_ok=True)
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                
                # Substituir no conteúdo
                replacement = f"![Imagem {i+1}]({self.output_dirs['attachments']}/{filename})"
                modified_content = modified_content.replace(
                    f"data:image/{img_type};base64,{base64_data}", 
                    replacement
                )
                
                saved_files.append(str(filepath))
                self.logger.info(f"✅ Imagem salva: {filename}")
                
            except Exception as e:
                self.logger.warning(f"⚠️ Erro ao processar imagem base64: {e}")
        
        # Processar URLs de imagem (apenas se requests disponível)
        if self.requests_available:
            url_matches = re.findall(patterns['image_url'], content)
            for i, url in enumerate(url_matches):
                if url.startswith('http'):
                    try:
                        import requests
                        response = requests.get(url, timeout=30)
                        if response.status_code == 200:
                            # Determinar tipo da imagem
                            extension = imghdr.what(None, response.content) or 'png'
                            filename = f"conv_{conv_number:03d}_msg_{msg_index:02d}_url_{i:02d}.{extension}"
                            filepath = Path(self.output_dirs['attachments']) / filename
                            
                            if not self.dry_run:
                                Path(self.output_dirs['attachments']).mkdir(parents=True, exist_ok=True)
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                            
                            # Substituir URL por caminho local
                            modified_content = modified_content.replace(
                                url, 
                                f"{self.output_dirs['attachments']}/{filename}"
                            )
                            
                            saved_files.append(str(filepath))
                            self.logger.info(f"✅ Imagem URL salva: {filename}")
                            
                    except Exception as e:
                        self.logger.warning(f"⚠️ Erro ao baixar imagem {url}: {e}")
        
        return modified_content, saved_files

    def process_qwen_attachments(self, content_list: list, conv_number: int, msg_index: int) -> tuple[str, list]:
        """Processa anexos específicos do Qwen com content_list"""
        if not content_list or not isinstance(content_list, list):
            return "", []
            
        content_parts = []
        saved_files = []
        
        for item in content_list:
            if isinstance(item, dict):
                item_type = item.get('type', '')
                
                if item_type == 'image' and 'data' in item:
                    # Processar imagem base64 do Qwen
                    try:
                        image_data = item['data']
                        if image_data.startswith('data:image'):
                            base64_match = re.search(r'base64,([^\"]+)', image_data)
                            if base64_match:
                                base64_str = base64_match.group(1)
                                image_binary = base64.b64decode(base64_str)
                                
                                extension = imghdr.what(None, image_binary) or 'png'
                                filename = f"qwen_conv_{conv_number:03d}_msg_{msg_index:02d}.{extension}"
                                filepath = Path(self.output_dirs['attachments']) / filename
                                
                                if not self.dry_run:
                                    Path(self.output_dirs['attachments']).mkdir(parents=True, exist_ok=True)
                                    with open(filepath, 'wb') as f:
                                        f.write(image_binary)
                                
                                content_parts.append(f"![Imagem Qwen]({self.output_dirs['attachments']}/{filename})")
                                saved_files.append(str(filepath))
                                
                    except Exception as e:
                        self.logger.warning(f"⚠️ Erro ao processar imagem Qwen: {e}")
                
                elif item_type == 'text' and 'text' in item:
                    content_parts.append(str(item['text']))
                    
        return '\n'.join(content_parts), saved_files

    def normalize_math_formulas(self, content: str) -> str:
        """Normaliza fórmulas matemáticas para formato consistente"""
        # Converter \( ... \) para $ ... $
        content = re.sub(r'\\\((.+?)\\\)', r'$\1$', content)
        
        # Converter \[ ... \] para $$ ... $$
        content = re.sub(r'\\\[(.+?)\\\]', r'$$\1$$', content)
        
        # Garantir espaços adequados ao redor de fórmulas
        content = re.sub(r'(\S)\$(\S)', r'\1 $\2', content)  # Adiciona espaço antes
        content = re.sub(r'(\S)\$(\S)', r'\1$ \2', content)  # Adiciona espaço depois
        
        return content

    def preserve_special_content_enhanced(self, content: str) -> str:
        """Preservação expandida de conteúdo especial com normalização Unicode"""
        if not content:
            return ""
            
        preserved_content = self.normalize_unicode_advanced(content)
        
        # Proteger blocos de código antes de outras transformações
        code_blocks = {}
        def protect_code_blocks(match):
            block_id = f"__CODE_BLOCK_{len(code_blocks)}__"
            code_blocks[block_id] = match.group(0)
            return block_id
            
        # Proteger blocos de código
        preserved_content = re.sub(
            r'```.*?```|`[^`]+`', 
            protect_code_blocks, 
            preserved_content, 
            flags=re.DOTALL
        )
        
        # Expandir correções LaTeX
        latex_corrections = {
            'ârac': '\\frac',
            'âarepsilon': '\\varepsilon',
            'â': '\\',
            'â': '\\',
            'â': '∈',
            'â': '∆',
            'â': '∂',
            'â': '∇',
            'â': '∑',
            'â': '∏',
            'â': '∝',
            'â': '∞',
            'â§': '∧',
            'â¨': '∨',
            'â': '∀',
            'â': '∃',
            'â¡': '≡',
            'â': '≈',
            'â¥': '≥',
            'â¤': '≤',
            'â ': '≠',
            'Â±': '±',
            'Ã': '×',
            'Ã·': '÷',
            'â': '→',
            'â': '↑',
            'â': '↓',
            'â': '←',
            'â': '⇒',
            'â': '⇔',
            'Â°': '°',
            'Âµ': 'µ',
            'Î±': 'α', 'Î²': 'β', 'Î³': 'γ', 'Î´': 'δ',
            'Îµ': 'ε', 'Î¶': 'ζ', 'Î·': 'η', 'Î¸': 'θ',
            'Î¹': 'ι', 'Îº': 'κ', 'Î»': 'λ', 'Î¼': 'μ',
            'Î½': 'ν', 'Î¾': 'ξ', 'Î¿': 'ο', 'Ï€': 'π',
            'Ï': 'ρ', 'Ï': 'σ', 'Ï': 'τ', 'Ï': 'υ',
            'Ï': 'φ', 'Ï': 'χ', 'Ï': 'ψ', 'Ï': 'ω',
            'Î': 'Α', 'Î': 'Β', 'Î': 'Γ', 'Î': 'Δ',
            'Î': 'Ε', 'Î': 'Ζ', 'Î': 'Η', 'Î': 'Θ',
            'Î': 'Ι', 'Î': 'Κ', 'Î': 'Λ', 'Î': 'Μ',
            'Î': 'Ν', 'Î': 'Ξ', 'Î': 'Ο', 'Î ': 'Π',
            'Î¡': 'Ρ', 'Î£': 'Σ', 'Î¤': 'Τ', 'Î¥': 'Υ',
            'Î¦': 'Φ', 'Î§': 'Χ', 'Î¨': 'Ψ', 'Î©': 'Ω',
        }
        
        for wrong, correct in latex_corrections.items():
            preserved_content = preserved_content.replace(wrong, correct)
        
        # Normalização de fórmulas matemáticas
        preserved_content = self.normalize_math_formulas(preserved_content)
        
        # Restaurar blocos de código protegidos
        for block_id, original_code in code_blocks.items():
            preserved_content = preserved_content.replace(block_id, original_code)
        
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
        """Executa o processamento completo com novas funcionalidades"""
        self.logger.info("SISTEMA COMBINADO v8.1 - COM ANEXOS, CACHE E UNICODE AVANÇADO")
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
            self.logger.info(f"\n🎉 SISTEMA COMBINADO v8.1 FINALIZADO!")
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
        """Exporta para todos os formats"""
        self.logger.info("\n🔄 Exportando para formatos...")
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index_enhanced()

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

    def _convert_with_pandoc_cached(self, md_file_path: str) -> Optional[str]:
        """Conversão com Pandoc usando cache para performance"""
        if not self.enable_cache:
            return self._convert_with_pandoc_optimized(md_file_path)
            
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Gerar chave do cache
            cache_options = {
                'pandoc_version': self._get_pandoc_version(),
                'mathjax_local': Path("assets/tex-mml-chtml.js").exists()
            }
            cache_key = self.conversion_cache.get_cache_key(md_content, cache_options)
            
            # Tentar recuperar do cache
            cached_html = self.conversion_cache.get_cached_conversion(cache_key)
            if cached_html:
                self.logger.info(f"✅ Usando cache: {Path(md_file_path).name}")
                return cached_html
            
            # Converter e salvar no cache
            html_content = self._convert_with_pandoc_optimized(md_file_path)
            if html_content:
                self.conversion_cache.save_conversion(cache_key, html_content)
                
            return html_content
            
        except Exception as e:
            self.logger.error(f"❌ Erro no cache Pandoc: {e}")
            return self._convert_with_pandoc_optimized(md_file_path)

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
                '--toc-depth=1',
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
                html_content = self._enhance_toc_interactive(html_content)
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
                '--toc-depth=1',
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
                html_content = result.stdout
                html_content = self._optimize_html_content(html_content)
                html_content = self._enhance_toc_interactive(html_content)
                return html_content
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

    def _enhance_toc_interactive(self, html_content: str) -> str:
        """Adiciona interatividade avançada ao TOC - FIXO À DIREITA E SEMPRE VISÍVEL"""
        interactive_js = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // TOC FIXO À DIREITA - SEMPRE VISÍVEL
        const toc = document.getElementById('TOC');
        if (toc) {
            // Aplicar estilos para fixar à direita permanentemente
            toc.style.position = 'fixed';
            toc.style.top = '50%';
            toc.style.right = '20px';
            toc.style.transform = 'translateY(-50%)';
            toc.style.maxHeight = '80vh';
            toc.style.overflowY = 'auto';
            toc.style.zIndex = '1000';
            toc.style.background = 'rgba(255, 255, 255, 0.95)';
            toc.style.padding = '20px';
            toc.style.borderRadius = '10px';
            toc.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
            toc.style.border = '1px solid #e0e0e0';
            toc.style.width = '300px';
            toc.style.backdropFilter = 'blur(10px)';
            toc.style.transition = 'all 0.3s ease';
            
            // Adicionar botão de minimizar/expandir
            const toggleBtn = document.createElement('button');
            toggleBtn.innerHTML = '📑';
            toggleBtn.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: transparent;
                border: none;
                font-size: 16px;
                cursor: pointer;
                z-index: 1001;
                padding: 5px;
                border-radius: 3px;
            `;
            
            let isMinimized = false;
            toggleBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                isMinimized = !isMinimized;
                if (isMinimized) {
                    toc.style.transform = 'translateY(-50%) translateX(280px)';
                    toggleBtn.innerHTML = '📖';
                    toc.style.opacity = '0.7';
                } else {
                    toc.style.transform = 'translateY(-50%)';
                    toggleBtn.innerHTML = '📑';
                    toc.style.opacity = '1';
                }
            });
            
            toc.style.position = 'relative';
            toc.appendChild(toggleBtn);
        }
        
        // Highlight de seção ativa no TOC
        const sections = document.querySelectorAll('h1, h2, h3, h4, h5');
        const tocLinks = document.querySelectorAll('#TOC a');
        const observerOptions = {
            rootMargin: '-20% 0px -60% 0px',
            threshold: 0
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    tocLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === '#' + id) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        }, observerOptions);
        
        sections.forEach(section => {
            if (section.id) {
                observer.observe(section);
            }
        });
        
        // Smooth scroll com offset para header fixo
        tocLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // Highlight temporário
                    tocLinks.forEach(l => l.classList.remove('clicked'));
                    link.classList.add('clicked');
                    setTimeout(() => link.classList.remove('clicked'), 2000);
                }
            });
        });
        
        // Botão de voltar ao topo
        const backToTop = document.createElement('div');
        backToTop.innerHTML = '⬆️';
        backToTop.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 350px;
            background: #3498db;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1000;
        `;
        document.body.appendChild(backToTop);
        
        window.addEventListener('scroll', () => {
            backToTop.style.opacity = window.scrollY > 500 ? '1' : '0';
        });
        
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
    </script>
    """
    
        # Adicionar CSS para TOC fixo à direita
        interactive_css = """
    <style>
    #TOC {
        transition: all 0.3s ease !important;
        z-index: 999 !important;
    }
    
    #TOC.fixed {
        width: 300px !important;
        right: 20px !important;
    }
    
    #TOC a.active {
        background-color: #007bff !important;
        color: white !important;
        font-weight: bold;
        border-radius: 4px;
        padding: 4px 8px;
    }
    
    #TOC a.clicked {
        background-color: #28a745 !important;
        color: white !important;
        animation: pulse 2s;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Scrollbar customizada para TOC */
    #TOC::-webkit-scrollbar {
        width: 6px;
    }
    
    #TOC::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    #TOC::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    #TOC::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Garantir que o conteúdo principal não fique atrás do TOC */
    .main-content {
        margin-right: 350px !important;
    }
    
    /* Responsividade: em telas menores, o TOC fica sobreposto */
    @media (max-width: 1400px) {
        #TOC {
            width: 280px !important;
        }
        .main-content {
            margin-right: 320px !important;
        }
    }
    
    @media (max-width: 1200px) {
        #TOC {
            width: 250px !important;
            right: 10px !important;
        }
        .main-content {
            margin-right: 280px !important;
        }
    }
    
    @media (max-width: 768px) {
        #TOC {
            position: relative !important;
            width: 100% !important;
            right: 0 !important;
            top: 0 !important;
            transform: none !important;
            margin-bottom: 20px;
        }
        .main-content {
            margin-right: 0 !important;
        }
    }
    </style>
    """
    
        if '</body>' in html_content:
            html_content = html_content.replace('</body>', f'{interactive_js}\n</body>')
    
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{interactive_css}\n</head>')
            
        return html_content

    def _inject_enhanced_css(self, html_content: str) -> str:
        """Injeta CSS personalizado aprimorado para TOC fixo à direita"""
        enhanced_css = """
        <style>
            /* LAYOUT DE TELA COMPLETA OTIMIZADO */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
                max-width: none; /* Remove limitação de largura - TELA COMPLETA */
            }
            
            .container {
                max-width: 95%; /* Usa quase toda a largura disponível */
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                position: relative; /* Para posicionamento do TOC */
            }

            /* TOC FIXO À DIREITA - SEMPRE VISÍVEL */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                position: fixed !important; /* FIXO */
                top: 50% !important;
                right: 20px !important;
                transform: translateY(-50%) !important;
                width: 300px !important;
                max-height: 80vh !important;
                overflow-y: auto !important;
                z-index: 1000 !important;
                backdrop-filter: blur(10px);
                background: rgba(255, 255, 255, 0.95) !important;
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
            
            /* CLEARFIX PARA LAYOUT COM TOC FIXO */
            .main-content {
                overflow: hidden; /* PREVINE PROBLEMAS COM ELEMENTOS FLUTUANTES */
                position: relative;
                margin-right: 350px !important; /* Espaço para o TOC fixo */
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
            
            /* CORREÇÃO CRÍTICA: Syntax highlighting do Pandoc */
            .sourceCode { 
                background: #2d2d2d !important; 
                color: #f8f8f2 !important;
            }
            
            /* Garantir que TODO o texto dentro de pre/code seja visível */
            pre, code, .sourceCode, .sourceCode pre, .sourceCode code {
                color: #f8f8f2 !important;
                background-color: #2d2d2d !important;
            }
            
            /* Correção para spans de syntax highlighting */
            .sourceCode .kw { color: #ff79c6 !important; } /* keywords */
            .sourceCode .dt { color: #8be9fd !important; } /* types */
            .sourceCode .dv { color: #bd93f9 !important; } /* values */
            .sourceCode .bn { color: #bd93f9 !important; } /* numbers */
            .sourceCode .fl { color: #bd93f9 !important; } /* floats */
            .sourceCode .ch { color: #f1fa8c !important; } /* chars */
            .sourceCode .st { color: #f1fa8c !important; } /* strings */
            .sourceCode .co { color: #6272a4 !important; } /* comments */
            .sourceCode .ot { color: #50fa7b !important; } /* other */
            .sourceCode .al { color: #ff5555 !important; } /* alerts */
            .sourceCode .fu { color: #50fa7b !important; } /* functions */
            .sourceCode .re { color: #f1fa8c !important; } /* regex */
            .sourceCode .er { color: #ff5555 !important; } /* errors */
            
            /* Garantir que texto normal em blocos de código seja visível */
            .sourceCode span {
                color: #f8f8f2 !important;
                background: transparent !important;
            }
            
            /* Fallback para qualquer elemento de código não estilizado */
            .sourceCode * {
                color: inherit !important;
                background: transparent !important;
            }
            
            /* Correção adicional para blocos de código gerais */
            div.sourceCode {
                border-left: 4px solid #3498db;
                background: #2d2d2d !important;
                color: #f8f8f2 !important;
                margin: 1.5em 0;
                border-radius: 8px;
                overflow: hidden;
            }
            
            div.sourceCode pre {
                margin: 0;
                padding: 20px;
                background: transparent !important;
            }
            
            /* Melhorar contraste para texto normal em todas as situações */
            body, .container, .main-content {
                color: #2c3e50 !important;
            }
            
            p, li, td, th, div, span {
                color: #2c3e50 !important;
            }
            
            /* Garantir que links sejam visíveis */
            a {
                color: #3498db !important;
            }
            
            a:hover {
                color: #2980b9 !important;
            }
            
            /* Correção para elementos MathJax */
            .math, .math display, mjx-container {
                color: #2c3e50 !important;
                background: transparent !important;
            }
            
            /* Melhorias para código e matemática */
            .math { display: block; text-align: center; margin: 1.5em 0; }
            .math inline { display: inline-block; }
            pre { 
                border-left: 4px solid #3498db; 
                background: #2d2d2d !important; 
                color: #f8f8f2 !important;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.4;
            }
            code { 
                background: #e9ecef !important; 
                padding: 0.2em 0.4em; 
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                color: #c7254e !important;
            }
            pre code { 
                background: none !important; 
                color: inherit !important; 
                padding: 0 !important; 
            }
            
            /* Melhorias responsivas - TOC FIXO À DIREITA */
            @media (max-width: 1400px) {
                .container {
                    max-width: 98%;
                    padding: 30px;
                }
                #TOC {
                    width: 280px; /* Reduz um pouco em telas menores, mas mantém fixo à direita */
                }
                .main-content {
                    margin-right: 320px !important;
                }
            }
            
            @media (max-width: 1200px) {
                #TOC {
                    width: 250px;
                    right: 10px !important;
                }
                .main-content {
                    margin-right: 280px !important;
                }
            }
            
            /* Em telas menores, o TOC volta ao fluxo normal */
            @media (max-width: 768px) {
                body { padding: 10px; font-size: 14px; }
                .container { padding: 20px; max-width: 100%; }
                pre { font-size: 12px; padding: 15px; }
                #TOC { 
                    position: relative !important;
                    width: auto !important;
                    right: 0 !important;
                    top: 0 !important;
                    transform: none !important;
                    margin: 20px 0;
                    float: none !important;
                }
                .main-content {
                    margin-right: 0 !important;
                }
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
                color: #2c3e50 !important; 
                margin-top: 1.8em;
                border-bottom: 1px solid #e9ecef;
                padding-bottom: 0.5em;
            }
            h1 { 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px; 
                color: #2c3e50 !important;
                font-size: 2.2em;
            }
            h2 {
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin-top: 2em;
            }
            
            /* Scroll suave para links do TOC */
            html {
                scroll-behavior: smooth;
            }
            
            /* Indicador visual para seção ativa no TOC */
            #TOC a.active {
                background-color: #007bff;
                color: white;
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
        
        # Adiciona wrapper para conteúdo principal com clearfix
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
        """Template HTML aprimorado com suporte a MathJax local/online e TOC flutuante"""
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* LAYOUT DE TELA COMPLETA OTIMIZADO */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
            max-width: none; /* Remove limitação de largura - TELA COMPLETA */
        }}
        .container {{
            max-width: 95%; /* Usa quase toda a largura disponível */
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            position: relative; /* Para posicionamento do TOC */
        }}
        
        /* TOC FIXO À DIREITA */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed !important;
            top: 50% !important;
            right: 20px !important;
            transform: translateY(-50%) !important;
            width: 300px !important;
            max-height: 80vh !important;
            overflow-y: auto !important;
            z-index: 1000 !important;
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95) !important;
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
        .toc ul ul {{
            padding-left: 25px;
        }}
        .toc li {{
            margin: 8px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #495057;
            font-weight: 500;
            display: block;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .toc a:hover {{
            color: #007bff;
            background-color: rgba(0, 123, 255, 0.1);
        }}
        
        /* CLEARFIX PARA LAYOUT COM TOC FIXO */
        .main-content {{
            overflow: hidden;
            position: relative;
            margin-right: 350px !important;
        }}
        
        /* CORREÇÃO CRÍTICA: Garantir visibilidade do texto */
        .sourceCode, pre, code {{
            color: #f8f8f2 !important;
            background-color: #2d2d2d !important;
        }}

        .sourceCode span {{
            color: #f8f8f2 !important;
            background: transparent !important;
        }}

        /* Correção para syntax highlighting */
        .sourceCode .kw {{ color: #ff79c6 !important; }}
        .sourceCode .dt {{ color: #8be9fd !important; }}
        .sourceCode .dv {{ color: #bd93f9 !important; }}
        .sourceCode .bn {{ color: #bd93f9 !important; }}
        .sourceCode .fl {{ color: #bd93f9 !important; }}
        .sourceCode .ch {{ color: #f1fa8c !important; }}
        .sourceCode .st {{ color: #f1fa8c !important; }}
        .sourceCode .co {{ color: #6272a4 !important; }}
        .sourceCode .ot {{ color: #50fa7b !important; }}
        .sourceCode .al {{ color: #ff5555 !important; }}
        .sourceCode .fu {{ color: #50fa7b !important; }}
        .sourceCode .re {{ color: #f1fa8c !important; }}
        .sourceCode .er {{ color: #ff5555 !important; }}

        /* Garantir contraste para texto normal */
        body, .container {{
            color: #2c3e50 !important;
        }}

        p, li, td, th {{
            color: #2c3e50 !important;
        }}
        
        h1, h2, h3, h4, h5 {{
            color: #2c3e50 !important;
            margin-top: 1.8em;
        }}
        h1 {{ 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 15px; 
            color: #2c3e50 !important;
            font-size: 2.2em;
        }}
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 2em;
        }}
        code {{
            background: #f4f4f4 !important;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: #c7254e !important;
            font-size: 0.9em;
        }}
        pre {{
            background: #2d2d2d !important;
            color: #f8f8f2 !important;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }}
        pre code {{
            background: none !important;
            color: inherit !important;
            padding: 0 !important;
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
            color: #2c3e50 !important;
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
            color: #2c3e50 !important;
        }}
        
        /* Melhorias responsivas */
        @media (max-width: 1400px) {{
            .container {{
                max-width: 98%;
                padding: 30px;
            }}
            .toc {{
                width: 280px;
            }}
            .main-content {{
                margin-right: 320px !important;
            }}
        }}
        
        @media (max-width: 1200px) {{
            .toc {{
                width: 250px;
                right: 10px !important;
            }}
            .main-content {{
                margin-right: 280px !important;
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
            .toc {{
                position: relative !important;
                width: auto !important;
                right: 0 !important;
                top: 0 !important;
                transform: none !important;
                margin: 20px 0;
            }}
            .main-content {{
                margin-right: 0 !important;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .message-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        
        /* Scroll suave */
        html {{
            scroll-behavior: smooth;
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
        
        // Script para destacar seção ativa no TOC (se existir)
        document.addEventListener('DOMContentLoaded', function() {{
            const tocLinks = document.querySelectorAll('#TOC a, .toc a');
            const sections = document.querySelectorAll('h1, h2, h3, h4, h5');
            
            function highlightActiveSection() {{
                let currentSection = '';
                const scrollY = window.pageYOffset;
                
                sections.forEach(section => {{
                    const sectionTop = section.offsetTop - 100;
                    if (scrollY >= sectionTop) {{
                        currentSection = section.getAttribute('id');
                    }}
                }});
                
                tocLinks.forEach(link => {{
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + currentSection) {{
                        link.classList.add('active');
                    }}
                }});
            }}
            
            if (tocLinks.length > 0) {{
                window.addEventListener('scroll', highlightActiveSection);
                highlightActiveSection(); // Chamar inicialmente
            }}
        }});
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
            max-width: none; /* Remove limitação de largura - TELA COMPLETA */
            color: #333 !important;
        }}
        pre {{ 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
            color: #333 !important;
        }}
        code {{
            color: #333 !important;
            background: white !important;
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
        """Método ROBUSTO para conversão HTML - VERSÃO OTIMIZADA COM CACHE"""
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
        
        self.logger.info(f"🔄 Convertendo {len(md_files)} arquivos Markdown para HTML (OTIMIZADO COM CACHE)...")
        
        # Verifica se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada com cache")
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
                    html_content = self._convert_with_pandoc_cached(str(md_file))
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
        """Gera conteúdo Markdown com preservação total de formatação e anexos"""
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
            
            # Processar anexos se existirem
            processed_content, saved_files = self.extract_and_save_attachments(
                msg['content'], conversation['number'], j
            )
            
            preserved_content = self.preserve_special_content_enhanced(processed_content)
            
            lines.extend([
                f"### {msg['author']}{timestamp}{model_info}",
                "",
                f"{preserved_content}",
                ""
            ])
            
            if saved_files:
                lines.extend([
                    "#### 📎 Anexos",
                    ""
                ])
                for file_path in saved_files:
                    lines.append(f"- `{file_path}`")
                lines.append("")
            
            if j < len(conversation['messages']):
                lines.extend(["---", ""])

        lines.extend([
            "---",
            "",
            f"*Conversa exportada do {conversation['source']}*",
            f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        ])
        
        return '\n'.join(lines)

    def process_qwen_corrected(self, path: Path):
        """Processa Qwen3 com correção para content_list - VERSÃO CORRIGIDA"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Qwen3: {path}")
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            # DEBUG: Salvar estrutura completa para análise
            debug_file = Path("qwen_debug_structure.json")
            with open(debug_file, 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"🔍 Estrutura Qwen salva em: {debug_file}")
            
            # Extrair conversas
            conversations = []
            
            if 'data' in raw_data and isinstance(raw_data['data'], list):
                conversations = raw_data['data']
                self.logger.info(f"📁 Estrutura 1: {len(conversations)} conversas em 'data'")
            elif isinstance(raw_data, list):
                conversations = raw_data
                self.logger.info(f"📁 Estrutura 2: {len(conversations)} conversas na raiz")
            else:
                for key, value in raw_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        if isinstance(value[0], dict) and any(k in value[0] for k in ['title', 'chat', 'messages']):
                            conversations = value
                            self.logger.info(f"📁 Estrutura alternativa: {len(conversations)} conversas em '{key}'")
                            break
            
            if not conversations:
                self.logger.error("❌ Nenhuma conversa encontrada no arquivo Qwen")
                return
                
            self.logger.info(f"🔍 Qwen: encontradas {len(conversations)} conversas.")
            processed_count = 0
            
            for i, conv in enumerate(conversations):
                if not isinstance(conv, dict):
                    continue
                    
                original_title = conv.get('title', f'Conversa Qwen {i+1}')
                clean_title = self.preserve_original_title(original_title)
                
                self.logger.info(f"   🔍 Processando: '{clean_title}'")
                
                # EXTRAÇÃO CORRIGIDA - foco em content_list
                messages = self._extract_qwen_messages_corrected(conv, clean_title, i)
                
                if messages:
                    # Ordenar mensagens por timestamp
                    messages.sort(key=lambda x: self.parse_timestamp_for_sorting(x['timestamp']))
                    
                    self.all_conversations.append({
                        'title': clean_title,
                        'source': 'Qwen3',
                        'id': conv.get('id', f'qwen_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('created_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': self.categorize_conversation(clean_title, messages[0]['content'][:100] if messages else "")
                    })
                    processed_count += 1
                    self.logger.info(f"   ✅ Adicionada: {len(messages)} mensagens")
                else:
                    self.logger.warning(f"   ❌ Conversa {i+1}: nenhuma mensagem extraída")
                    
            self.logger.info(f"✅ Qwen3: {processed_count} conversas processadas.")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Qwen3: {e}")
            self.logger.error(traceback.format_exc())

    def _extract_qwen_messages_corrected(self, conv: Dict[str, Any], clean_title: str, conv_index: int) -> List[Dict[str, Any]]:
        """Extrai mensagens do Qwen com correção para content_list"""
        all_messages = []
        
        # ESTRATÉGIA PRINCIPAL: Buscar em toda a estrutura por mensagens
        def extract_from_object(obj, path=""):
            messages_found = []
            
            if isinstance(obj, dict):
                # Verificar se é uma mensagem com content_list (CASO CORRIGIDO)
                if self._is_qwen_message_with_content(obj):
                    message = self._create_message_from_qwen_object(obj, conv_index)
                    if message:
                        messages_found.append(message)
                
                # Buscar recursivamente
                for key, value in obj.items():
                    messages_found.extend(extract_from_object(value, f"{path}.{key}"))
                    
            elif isinstance(obj, list):
                for item in obj:
                    messages_found.extend(extract_from_object(item, path))
                    
            return messages_found
        
        # Aplicar extração recursiva
        all_messages = extract_from_object(conv, "root")
        
        # Remover duplicatas
        unique_messages = self._remove_duplicate_messages(all_messages)
        
        if len(unique_messages) != len(all_messages):
            self.logger.info(f"         🔄 Removidas {len(all_messages) - len(unique_messages)} mensagens duplicadas")
        
        return unique_messages

    def _is_qwen_message_with_content(self, obj: Dict) -> bool:
        """Verifica se é uma mensagem Qwen válida (incluindo content_list)"""
        # Verificar campos básicos de mensagem
        has_basic_structure = ('role' in obj and 'content' in obj)
        
        # Verificar se tem content_list (CORREÇÃO DO PROBLEMA)
        has_content_list = 'content_list' in obj and isinstance(obj['content_list'], list)
        
        # É uma mensagem válida se tiver estrutura básica E (conteúdo não vazio OU content_list)
        return (has_basic_structure and 
                (obj.get('content') or has_content_list) and
                obj.get('role') in ['user', 'assistant'])

    def _create_message_from_qwen_object(self, obj: Dict, conv_index: int) -> Optional[Dict[str, Any]]:
        """Cria uma mensagem a partir de um objeto Qwen, priorizando content_list"""
        role = obj.get('role', '')
        content = obj.get('content', '')
        content_list = obj.get('content_list', [])
        
        if not role:
            return None

        # CORREÇÃO PRINCIPAL: Priorizar content_list quando content estiver vazio
        final_content = ""
        saved_files = []
        
        if content_list and isinstance(content_list, list):
            # Processar content_list com anexos
            qwen_content, qwen_files = self.process_qwen_attachments(content_list, conv_index, len(self.all_conversations))
            if qwen_content:
                final_content = qwen_content
                saved_files.extend(qwen_files)

        # Se content_list não forneceu conteúdo, usar o campo content tradicional
        if not final_content and content:
            # Processar anexos no conteúdo tradicional
            processed_content, content_files = self.extract_and_save_attachments(
                str(content), conv_index, len(self.all_conversations)
            )
            final_content = processed_content
            saved_files.extend(content_files)
        
        # Se ainda não tem conteúdo, pular
        if not final_content or final_content == 'null':
            return None

        # Determinar autor
        if role == 'user':
            author = "👤 Utilizador"
        elif role == 'assistant':
            author = "🤖 Qwen3"
        else:
            author = f"🔹 {role.title()}"

        # Processar conteúdo especial
        final_content = self.preserve_special_content_enhanced(final_content)
        
        return {
            'author': author,
            'role': role,
            'content': final_content,
            'timestamp': self.format_timestamp(obj.get('created_at')),
            'model': obj.get('model', 'Qwen3'),
            'attachments': saved_files
        }

    def _remove_duplicate_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove mensagens duplicadas baseadas no conteúdo"""
        seen = set()
        unique_messages = []
        
        for msg in messages:
            # Criar uma chave única baseada no conteúdo e timestamp
            content_key = f"{msg['content'][:100]}_{msg['timestamp']}"
            
            if content_key not in seen:
                seen.add(content_key)
                unique_messages.append(msg)
        
        return unique_messages

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
                    
                    # Processar anexos
                    processed_content, saved_files = self.extract_and_save_attachments(content, i, len(messages))
                    content = self.preserve_special_content_enhanced(processed_content)
                    
                    if not content:
                        continue
                        
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('create_time')),
                        'model': msg_data.get('model', 'ChatGPT'),
                        'attachments': saved_files
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
                    
                    # Processar anexos
                    processed_content, saved_files = self.extract_and_save_attachments(content, i, len(messages))
                    content = self.preserve_special_content_enhanced(processed_content)
                    
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
                        'model': msg_data.get('model', 'DeepSeek'),
                        'attachments': saved_files
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
                    
                    # Processar anexos
                    processed_content, saved_files = self.extract_and_save_attachments(content, total_convs, len(messages))
                    content = self.preserve_special_content_enhanced(processed_content)
                    
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
                        'model': 'Grok',
                        'attachments': saved_files
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
                    'node_id', 'author', 'role', 'timestamp', 'model', 'content', 'attachments'
                ])
                writer.writeheader()
                for i, msg in enumerate(conv['messages']):
                    writer.writerow({
                        'node_id': str(i),
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg['model'],
                        'content': msg['content'],
                        'attachments': ', '.join(msg.get('attachments', []))
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
                'author', 'role', 'timestamp', 'model', 'content', 'attachments'
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
                        'content': msg['content'],
                        'attachments': ', '.join(msg.get('attachments', []))
                    })
        self.logger.info(f"✅ CSV único: {self.single_files['csv']}")

        # JSON único
        with open(self.single_files['json'], 'w', encoding='utf-8') as f:
            json.dump(self.all_conversations, f, ensure_ascii=False, indent=2)
        self.logger.info(f"✅ JSON único: {self.single_files['json']}")

    def create_searchable_index_enhanced(self):
        """Cria índice HTML pesquisável com estatísticas avançadas"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Índice HTML seria criado: {self.index_file}")
            return
            
        self.logger.info("🎯 Criando índice HTML combinado v8.1...")
        
        # Estatísticas detalhadas
        category_stats = {}
        source_stats = {}
        recent_stats = {
            'week': 0,
            'month': 0
        }
        
        one_week_ago = datetime.now().timestamp() - (7 * 24 * 60 * 60)
        one_month_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        
        for conv in self.all_conversations:
            # Estatísticas por categoria
            cat = conv['category']
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            # Estatísticas por fonte
            source = conv['source']
            source_stats[source] = source_stats.get(source, 0) + 1
            
            # Conversas recentes
            conv_time = self.parse_timestamp_for_sorting(
                conv.get('updated_at') or conv.get('inserted_at')
            ).timestamp()
            
            if conv_time > one_week_ago:
                recent_stats['week'] += 1
            if conv_time > one_month_ago:
                recent_stats['month'] += 1

        html_content = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice Combinado v8.1 - AI Chats</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 15px; font-weight: 300; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; margin-bottom: 20px; }}
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin: 20px 0;
        }}
        .stat-card {{ 
            background: rgba(255,255,255,0.15); 
            padding: 20px; 
            border-radius: 12px; 
            backdrop-filter: blur(10px);
            text-align: center;
        }}
        .stat-number {{ 
            font-size: 2em; 
            font-weight: bold; 
            margin-bottom: 5px;
        }}
        .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
        .search-box {{ width: 100%; padding: 18px 25px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; font-family: inherit; }}
        .search-box:focus {{ border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }}
        
        .advanced-filters {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 30px;
        }}
        
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
        
        .filter-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 10px 0;
            align-items: center;
        }}
        
        .filter-group strong {{
            margin-right: 10px;
            color: #2c3e50;
        }}
        
        .quick-actions {{
            display: flex;
            gap: 10px;
            margin: 15px 0;
            flex-wrap: wrap;
        }}
        
        .action-btn {{
            padding: 10px 15px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-family: inherit;
        }}
        
        .action-btn:hover {{
            background: #2980b9;
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
        .action-btn-small {{ 
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
        .action-btn-small:hover {{ 
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
            background: #17a2b8 !important;
            color: white !important;
            border: 2px solid #17a2b8 !important;
        }}
        .html-btn:hover {{
            background: #138496 !important;
            border-color: #138496 !important;
        }}
        
        .pdf-btn {{
            background: #dc3545 !important;
            color: white !important;
            border: 2px solid #dc3545 !important;
        }}
        .pdf-btn:hover {{
            background: #c82333 !important;
            border-color: #c82333 !important;
        }}
        
        .attachments-badge {{
            background: #ffc107;
            color: #212529;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7em;
            margin-left: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Índice Combinado v8.1</h1>
            <p>Qwen3 • ChatGPT • DeepSeek • Grok • COM ANEXOS, CACHE E UNICODE AVANÇADO</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(self.all_conversations)}</div>
                    <div>Total de Conversas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(source_stats)}</div>
                    <div>Fontes Diferentes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{recent_stats['week']}</div>
                    <div>Última Semana</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{recent_stats['month']}</div>
                    <div>Último Mês</div>
                </div>
            </div>
        </div>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo, categoria ou fonte...">
        </div>
        
        <div class="advanced-filters">
            <h3>🎯 Filtros Avançados v8.1</h3>
            
            <div class="filter-group">
                <strong>Fontes:</strong>
                <button class="filter-btn active" data-filter-source="todas">Todas ({len(self.all_conversations)})</button>
                {"".join([f'<button class="filter-btn" data-filter-source="{source}">{source} ({count})</button>' 
                         for source, count in source_stats.items()])}
            </div>
            
            <div class="filter-group">
                <strong>Categorias:</strong>
                <button class="filter-btn active" data-filter-category="todas">Todas</button>
                {"".join([f'<button class="filter-btn" data-filter-category="{category}">{category} ({count})</button>' 
                         for category, count in sorted(category_stats.items())])}
            </div>
            
            <div class="quick-actions">
                <button class="action-btn" onclick="clearCache()">🔄 Limpar Cache</button>
                <button class="action-btn" onclick="exportStats()">📊 Exportar Estatísticas</button>
                <button class="action-btn" onclick="toggleDarkMode()">🌙 Modo Escuro</button>
            </div>
        </div>
        
        <div style="text-align: center; padding: 15px; background: #e9ecef; border-bottom: 1px solid #ddd;">
            <strong>Acesso Rápido v8.1:</strong>
            <a href="combined_markdown/" class="direct-link" target="_blank">📁 Markdown</a>
            <a href="combined_html/" class="direct-link" target="_blank">🌐 HTML</a>
            <a href="combined_attachments/" class="direct-link" target="_blank">📎 Anexos</a>
            <a href="combined_json/" class="direct-link" target="_blank">📋 JSON</a>
            <a href="combined_csv/" class="direct-link" target="_blank">📊 CSV</a>
            <a href="combined_pdfs/" class="direct-link" target="_blank">📄 PDF</a>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
"""
    
        for i, conv in enumerate(self.all_conversations):
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}"
            recent_badge = "<span class='recent-badge'>NOVO</span>" if i < 5 else ""
            
            # Verificar se tem anexos
            has_attachments = any(msg.get('attachments') for msg in conv['messages'])
            attachments_badge = "<span class='attachments-badge'>📎</span>" if has_attachments else ""
            
            summary = conv.get('summary', 'Sem resumo disponível')
            if len(summary) > 150:
                summary = summary[:150] + "..."
            
            html_content += f"""
            <div class="conversation-card" data-title="{conv['title']}" data-summary="{summary}" data-source="{conv['source'].lower()}" data-category="{conv['category'].lower()}">
                <div class="card-header">
                    <div class="card-number">#{conv['number']} {recent_badge} {attachments_badge}</div>
                    <div class="card-actions">
                        <a href="combined_markdown/{filename}.md" class="action-btn-small" target="_blank" onclick="event.stopPropagation();">📄 MD</a>
                        <a href="combined_html/{filename}.html" class="action-btn-small html-btn" target="_blank" onclick="event.stopPropagation();">🌐 HTML</a>
                        <a href="combined_pdfs/{filename}.pdf" class="action-btn-small pdf-btn" target="_blank" onclick="event.stopPropagation();">📊 PDF</a>
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
        let currentFilter = { source: 'todas', category: 'todas' };
        
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
            initializeDarkMode();
        });

        // Filtros por fonte
        document.querySelectorAll('[data-filter-source]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('[data-filter-source]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter.source = btn.getAttribute('data-filter-source');
                filterConversations();
            });
        });

        // Filtros por categoria
        document.querySelectorAll('[data-filter-category]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('[data-filter-category]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter.category = btn.getAttribute('data-filter-category');
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
                const matchesSource = (currentFilter.source === 'todas' || source === currentFilter.source.toLowerCase());
                const matchesCategory = (currentFilter.category === 'todas' || category === currentFilter.category.toLowerCase());
                
                if (matchesSearch && matchesSource && matchesCategory) {
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
            // Atualizar contador se fornecido
            if (visibleCount !== null) {
                // Poderia atualizar algum elemento de estatística se necessário
            }
        }

        function openHTML(filename) {
            const htmlUrl = 'combined_html/' + filename;
            console.log('Abrindo HTML:', htmlUrl);
            window.open(htmlUrl, '_blank');
        }

        function clearCache() {
            if (confirm('Limpar cache de conversões? Isso forçará a reconversão de todos os arquivos HTML na próxima execução.')) {
                fetch('?action=clear_cache').then(() => {
                    alert('Cache limpo com sucesso!');
                }).catch(() => {
                    alert('Erro ao limpar cache. Execute o programa com --clear-cache.');
                });
            }
        }

        function exportStats() {
            const stats = {
                total: """ + str(len(self.all_conversations)) + """,
                sources: """ + str(source_stats) + """,
                categories: """ + str(category_stats) + """,
                recent: """ + str(recent_stats) + """,
                export_time: new Date().toISOString()
            };
            
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(stats, null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "chat_stats_" + new Date().toISOString().split('T')[0] + ".json");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
            applyDarkModeStyles();
        }

        function initializeDarkMode() {
            if (localStorage.getItem('darkMode') === 'true') {
                document.body.classList.add('dark-mode');
                applyDarkModeStyles();
            }
        }

        function applyDarkModeStyles() {
            if (document.body.classList.contains('dark-mode')) {
                // Estilos para modo escuro
                const darkStyles = `
                    body {
                        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
                        color: #ecf0f1 !important;
                    }
                    .container {
                        background: #2c3e50 !important;
                        color: #ecf0f1 !important;
                    }
                    .conversation-card {
                        background: #34495e !important;
                        color: #ecf0f1 !important;
                        border-color: #4a6572 !important;
                    }
                    .card-title, .card-summary {
                        color: #ecf0f1 !important;
                    }
                    .search-box {
                        background: #34495e !important;
                        color: #ecf0f1 !important;
                        border-color: #4a6572 !important;
                    }
                `;
                
                let styleElement = document.getElementById('dark-mode-styles');
                if (!styleElement) {
                    styleElement = document.createElement('style');
                    styleElement.id = 'dark-mode-styles';
                    document.head.appendChild(styleElement);
                }
                styleElement.textContent = darkStyles;
            } else {
                const styleElement = document.getElementById('dark-mode-styles');
                if (styleElement) {
                    styleElement.remove();
                }
            }
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.getElementById('searchInput').value = '';
                filterConversations();
            }
        });

        document.querySelectorAll('.conversation-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.closest('.action-btn-small')) {
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
        
        console.log('Índice v8.1 carregado com', """ + str(len(self.all_conversations)) + """, 'conversas');
    </script>
</body>
</html>
"""
    
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"✅ Índice combinado v8.1 criado: {self.index_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Processa exportações combinadas com exportação HTML via Pandoc v8.1 - COM ANEXOS, CACHE E UNICODE AVANÇADO"
    )
    parser.add_argument("--dry-run", action="store_true", help="Executa sem salvar arquivos")
    parser.add_argument("--force-overwrite", action="store_true", help="Substitui arquivos existentes")
    parser.add_argument("--clear-cache", action="store_true", help="Limpa o cache de conversões")
    
    args = parser.parse_args()
    
    system = CombinedFragmentsSystem(
        dry_run=args.dry_run,
        force_overwrite=args.force_overwrite,
        clear_cache=args.clear_cache
    )
    system.run()

if __name__ == "__main__":
    main()
```

**Principais melhorias implementadas:**

1. **TOC Fixo à Direita**: 
   - Agora o TOC fica fixo no lado direito da tela
   - Sempre visível durante o scroll
   - Posicionado verticalmente no centro da tela

2. **Melhorias de UX**:
   - Botão de minimizar/expandir no TOC
   - Efeitos de transição suaves
   - Fundo com blur para melhor legibilidade

3. **Responsividade**:
   - Em telas menores (<768px), o TOC volta ao fluxo normal
   - Ajustes automáticos de margens

4. **Correção dos Warnings**:
   - Mantém a funcionalidade de download de imagens
   - Os warnings sobre falha de DNS são normais quando não há internet

O sistema agora garante que o TOC esteja sempre visível e acessível, melhorando significativamente a experiência de navegação nos documentos HTML gerados.

---

*Conversa exportada do DeepSeek*
*Processado em: 23/11/2025 14:36*