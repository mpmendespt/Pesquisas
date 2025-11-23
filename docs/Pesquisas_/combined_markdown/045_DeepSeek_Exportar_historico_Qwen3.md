# Exportar historico Qwen3

## 📊 Informações
- **Número:** #45
- **Origem:** DeepSeek
- **Categoria:** IA
- **ID:** bbe6d4ca-9051-4045-a94a-9cb1f26cf6a8
- **Criada em:** 2025-11-02 23:14:55
- **Atualizada em:** 2025-11-02 23:32:11
- **Total de mensagens:** 4
- **Resumo:** Pretendia um sistema adaptado o "Export chat" do  chat.qwen.ai : o file com os dados é: chat-export....

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-02 23:14:57)* *[deepseek-chat]*

Pretendia um sistema adaptado o "Export chat" do  chat.qwen.ai : o file com os dados é: chat-export.json  
(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas_Qwen3-Max>file chat-export.json
chat-export.json: JSON text data

(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas_Qwen3-Max>dir
 Volume in drive D is _Work_
 Volume Serial Number is 3CB7-A082

 Directory of D:\Downloads\_DOCS_\_DOCS_\Pesquisas_Qwen3-Max

11/02/2025  03:07 PM    <DIR>          .
11/02/2025  03:07 PM    <DIR>          ..
11/02/2025  03:00 PM           148,556 chat-export.json
               1 File(s)        148,556 bytes

O sistema de ser idêntico ao produzido anteriormente com um file para processar o sistema e outro para converter de md para html e depois para pdf
grok_processor_optimized.py
grok_pdf_converter_optimized.py

---

### 🤖 DeepSeek *(2025-11-02 23:14:57)* *[deepseek-chat]*

Com base no seu arquivo `chat-export.json` do Qwen AI, vou criar um sistema adaptado idêntico ao anterior. Aqui estão os dois arquivos necessários:

## Arquivo 1: Processador do Qwen AI

```python
# qwen_processor_optimized.py
import json
import os
from datetime import datetime
import webbrowser

class QwenProcessorOptimized:
    def __init__(self, json_file="chat-export.json"):
        self.json_file = json_file
        self.markdown_folder = "qwen_markdown"
        self.conversations = []
        self.index_file = "qwen_index.html"
        self.pdf_folder = "qwen_pdfs"
        
    def extract_qwen_conversations(self):
        """Extrai conversas do arquivo JSON do Qwen AI"""
        print("🔧 Extraindo conversas do Qwen AI...")
        
        if not os.path.exists(self.json_file):
            print(f"❌ Arquivo não encontrado: {self.json_file}")
            return False
        
        try:
            print("📖 Lendo chat-export.json...")
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data.get('success', False):
                print("❌ JSON não contém dados válidos")
                return False
            
            conversations_data = data.get('data', [])
            
            if not isinstance(conversations_data, list):
                print("❌ Formato inválido")
                return False
            
            print(f"🎯 Processando {len(conversations_data)} conversas...")
            
            # Processa cada conversa
            self.conversations = []
            for i, conv_data in enumerate(conversations_data):
                conversation = self.process_conversation(conv_data, i+1)
                if conversation and conversation['messages']:
                    self.conversations.append(conversation)
                    print(f"✅ {i+1:02d}: '{conversation['title']}' - {len(conversation['messages'])} mensagens")
                else:
                    print(f"⚠️  {i+1:02d}: '{conv_data.get('title', 'Sem título')}' - SEM MENSAGENS")
            
            # ORDENAÇÃO: do mais novo para o mais antigo
            print("🔄 Ordenando conversas do mais novo para o mais antigo...")
            self.conversations.sort(key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('created_at')
            ), reverse=True)
            
            # Reenumera as conversas após ordenação
            for i, conv in enumerate(self.conversations):
                conv['number'] = i + 1
            
            print(f"📊 Total de conversas com mensagens: {len(self.conversations)}")
            
            if self.conversations:
                self.save_as_markdown()
            
            return len(self.conversations) > 0
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def parse_timestamp_for_sorting(self, timestamp):
        """Converte timestamp para objeto datetime para ordenação"""
        if not timestamp:
            return datetime.min
        
        try:
            # Se for timestamp Unix
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
            elif isinstance(timestamp, str):
                # Tentar converter string para datetime
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except Exception as e:
            print(f"⚠️  Erro ao converter timestamp '{timestamp}': {e}")
        
        return datetime.min
    
    def process_conversation(self, conv_data, number):
        """Processa uma conversa individual do Qwen AI"""
        try:
            title = conv_data.get('title', f'Conversa {number}')
            conv_id = conv_data.get('id', f'conv_{number}')
            created_at = conv_data.get('created_at')
            updated_at = conv_data.get('updated_at')
            
            # Extrai mensagens do histórico
            chat_data = conv_data.get('chat', {})
            history = chat_data.get('history', {})
            messages_data = history.get('messages', {})
            
            messages = self.extract_messages_from_history(messages_data)
            
            return {
                'number': number,
                'id': conv_id,
                'title': title,
                'created_at': self.format_timestamp(created_at),
                'updated_at': self.format_timestamp(updated_at),
                'messages': messages,
                'message_count': len(messages),
                'summary': self.generate_summary(messages),
                'raw_timestamp': updated_at or created_at  # Para ordenação
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao processar conversa {number}: {e}")
            return None
    
    def extract_messages_from_history(self, messages_data):
        """Extrai mensagens do histórico do Qwen AI"""
        messages = []
        
        # Converte o dicionário para lista ordenada
        message_list = []
        for msg_id, msg_data in messages_data.items():
            if isinstance(msg_data, dict):
                msg_data['_id'] = msg_id
                message_list.append(msg_data)
        
        # Ordena pela timestamp
        message_list.sort(key=lambda x: x.get('timestamp', 0))
        
        for msg_data in message_list:
            message = self.parse_message(msg_data)
            if message and message['content']:  # Só adiciona se tiver conteúdo
                messages.append(message)
        
        return messages
    
    def parse_message(self, message_data):
        """Analisa uma mensagem do Qwen AI"""
        try:
            role = message_data.get('role', '')
            
            if role == 'assistant':
                author_display = '🤖 Qwen AI'
                # Tenta extrair o nome do modelo
                model = message_data.get('model', '')
                if 'qwen' in model.lower():
                    model_display = f" ({model})"
                else:
                    model_display = f" ({message_data.get('modelName', '')})"
                author_display += model_display
            else:
                author_display = '👤 Você'
            
            # Extrai conteúdo da mensagem
            content = self.extract_content(message_data)
            
            if not content or content.isspace():
                return None
            
            # Timestamp
            timestamp = message_data.get('timestamp')
            
            return {
                'node_id': message_data.get('_id', ''),
                'author': author_display,
                'role': role,
                'content': content,
                'timestamp': self.format_timestamp(timestamp),
                'model': message_data.get('model', '')
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar mensagem: {e}")
            return None
    
    def extract_content(self, message_data):
        """Extrai conteúdo da mensagem do Qwen AI"""
        # Tenta diferentes formatos de conteúdo
        content = message_data.get('content', '')
        
        # Se content estiver vazio, tenta content_list
        if not content and 'content_list' in message_data:
            content_list = message_data['content_list']
            if content_list and isinstance(content_list, list):
                for item in content_list:
                    if isinstance(item, dict) and 'content' in item:
                        content = item['content']
                        break
        
        # Limpa o conteúdo
        if isinstance(content, str):
            return content.strip()
        elif isinstance(content, (list, dict)):
            return str(content)
        
        return ''
    
    def format_timestamp(self, timestamp):
        """Formata timestamp para exibição"""
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, (int, float)):
                # Converter timestamp Unix para formato legível
                return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
            elif isinstance(timestamp, str):
                # Tentar converter string
                return timestamp.replace('T', ' ').split('.')[0]
        except:
            pass
        
        return str(timestamp)
    
    def generate_summary(self, messages):
        """Gera resumo da conversa"""
        if not messages:
            return "Sem conteúdo"
        
        # Procura primeira mensagem do usuário
        for msg in messages:
            if msg.get('role') == 'user':
                content = msg['content']
                if len(content) > 100:
                    return content[:100] + "..."
                return content
        
        # Ou usa primeira mensagem qualquer
        first_msg = messages[0]['content']
        if len(first_msg) > 100:
            return first_msg[:100] + "..."
        return first_msg
    
    def save_as_markdown(self):
        """Salva como Markdown"""
        print(f"📤 Salvando {len(self.conversations)} conversas...")
        
        os.makedirs(self.markdown_folder, exist_ok=True)
        
        for conversation in self.conversations:
            md_content = self.create_markdown_content(conversation)
            
            safe_title = "".join(c for c in conversation['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conversation['number']:03d}_{safe_title}.md"
            filepath = os.path.join(self.markdown_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"✅ {filename} (📅 {conversation['updated_at'] or conversation['created_at']})")
        
        print(f"🎉 {len(self.conversations)} arquivos criados em '{self.markdown_folder}'")
    
    def create_markdown_content(self, conversation):
        """Cria conteúdo Markdown"""
        md = f"# 💬 {conversation['title']}\n\n"
        
        # Metadados
        md += "## 📊 Informações\n\n"
        md += f"- **Número:** #{conversation['number']}\n"
        md += f"- **ID:** {conversation['id']}\n"
        md += f"- **Criada em:** {conversation['created_at'] or 'N/A'}\n"
        if conversation['updated_at']:
            md += f"- **Atualizada em:** {conversation['updated_at']}\n"
        md += f"- **Total de mensagens:** {conversation['message_count']}\n"
        md += f"- **Resumo:** {conversation['summary']}\n\n"
        
        md += "---\n\n"
        
        # Mensagens
        md += "## 🗨️ Conversa\n\n"
        
        for j, message in enumerate(conversation['messages'], 1):
            timestamp = f" *({message['timestamp']})*" if message['timestamp'] else ""
            model_info = f" *[{message['model']}]*" if message.get('model') else ""
            md += f"### {message['author']}{timestamp}{model_info}\n\n"
            md += f"{message['content']}\n\n"
            
            if j < len(conversation['messages']):
                md += "---\n\n"
        
        # Rodapé
        md += "\n---\n\n"
        md += "*Conversa exportada do Qwen AI*  \n"
        md += f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        
        return md
    
    def create_searchable_index(self):
        """Cria índice HTML pesquisável"""
        print("🎯 Criando índice pesquisável...")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📚 Índice de Conversas - Qwen AI</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%); min-height: 100vh; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #0052d4, #4364f7); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
                .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 20px; flex-wrap: wrap; }}
                .stat-item {{ background: rgba(255,255,255,0.1); padding: 15px 25px; border-radius: 10px; backdrop-filter: blur(10px); }}
                .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
                .search-box {{ width: 100%; padding: 15px 20px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; }}
                .search-box:focus {{ border-color: #0052d4; box-shadow: 0 0 0 3px rgba(0, 82, 212, 0.1); }}
                .conversations-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; padding: 30px; }}
                .conversation-card {{ background: white; border: 1px solid #e9ecef; border-radius: 12px; padding: 20px; transition: all 0.3s ease; cursor: pointer; position: relative; }}
                .conversation-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: #0052d4; }}
                .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }}
                .card-number {{ background: #0052d4; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em; font-weight: bold; }}
                .card-title {{ font-size: 1.2em; font-weight: bold; color: #2c3e50; margin-bottom: 10px; line-height: 1.4; }}
                .card-summary {{ color: #6c757d; font-size: 0.95em; line-height: 1.5; margin-bottom: 15px; }}
                .card-meta {{ display: flex; justify-content: space-between; font-size: 0.85em; color: #868e96; border-top: 1px solid #e9ecef; padding-top: 15px; }}
                .card-actions {{ position: absolute; top: 15px; right: 15px; display: flex; gap: 5px; opacity: 0; transition: opacity 0.3s ease; }}
                .conversation-card:hover .card-actions {{ opacity: 1; }}
                .action-btn {{ background: white; border: 1px solid #e9ecef; border-radius: 5px; padding: 5px 10px; font-size: 0.8em; cursor: pointer; transition: all 0.3s ease; }}
                .action-btn:hover {{ background: #0052d4; color: white; border-color: #0052d4; }}
                .recent-badge {{ background: #ff6b6b; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; margin-left: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 Índice de Conversas</h1>
                    <p>Qwen AI - Histórico Completo (Mais Recentes Primeiro)</p>
                    <div class="stats">
                        <div class="stat-item">
                            <strong>Total:</strong> <span id="total-count">{len(self.conversations)}</span> conversas
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
                    <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo ou palavras-chave...">
                </div>
                
                <div class="conversations-grid" id="conversationsGrid">
        """
        
        # Adiciona cards (já ordenados do mais novo para o mais antigo)
        for i, conv in enumerate(self.conversations):
            safe_title = "".join(c for c in conv['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conv['number']:03d}_{safe_title}.md"
            
            recent_badge = ""
            if i < 3:  # Marca as 3 mais recentes
                recent_badge = "<span class='recent-badge'>NOVO</span>"
            
            html_content += f"""
                    <div class="conversation-card" data-title="{conv['title']}" data-summary="{conv['summary']}">
                        <div class="card-header">
                            <div class="card-number">#{conv['number']} {recent_badge}</div>
                            <div class="card-actions">
                                <button class="action-btn" onclick="openMD('{filename}')">MD</button>
                                <button class="action-btn" onclick="openPDF('{filename}')">PDF</button>
                            </div>
                        </div>
                        <div class="card-title">{conv['title']}</div>
                        <div class="card-summary">{conv['summary']}</div>
                        <div class="card-meta">
                            <span>📅 {conv['updated_at'] or conv['created_at'] or 'N/A'}</span>
                            <span>💬 {conv['message_count']} mensagens</span>
                        </div>
                    </div>
            """
        
        html_content += """
                </div>
            </div>

            <script>
                document.getElementById('searchInput').addEventListener('input', function(e) {
                    const searchTerm = e.target.value.toLowerCase();
                    const cards = document.querySelectorAll('.conversation-card');
                    let visibleCount = 0;
                    
                    cards.forEach(card => {
                        const title = card.getAttribute('data-title').toLowerCase();
                        const summary = card.getAttribute('data-summary').toLowerCase();
                        
                        if (title.includes(searchTerm) || summary.includes(searchTerm)) {
                            card.style.display = 'block';
                            visibleCount++;
                        } else {
                            card.style.display = 'none';
                        }
                    });
                    
                    document.getElementById('total-count').textContent = visibleCount;
                });
                
                function openMD(filename) {
                    window.open('""" + self.markdown_folder + """/' + filename, '_blank');
                }
                
                function openPDF(filename) {
                    const pdfFile = filename.replace('.md', '.pdf');
                    window.open('""" + self.pdf_folder + """/' + pdfFile, '_blank');
                }
                
                document.querySelectorAll('.conversation-card').forEach(card => {
                    card.addEventListener('click', function(e) {
                        if (!e.target.classList.contains('action-btn')) {
                            const filename = this.querySelector('.card-actions button').getAttribute('onclick').split("'")[1];
                            openMD(filename);
                        }
                    });
                });
            </script>
        </body>
        </html>
        """
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Índice criado: {self.index_file}")
    
    def generate_complete_system(self):
        """Gera sistema completo"""
        print("🚀 SISTEMA QWEN AI - Iniciando")
        print("=" * 50)
        
        success = self.extract_qwen_conversations()
        
        if not success:
            print("❌ Não foi possível extrair conversas")
            return
        
        self.create_searchable_index()
        
        print(f"\n🎉 SISTEMA COMPLETO!")
        print(f"📁 Conversas: {len(self.conversations)}")
        print(f"📄 Índice: {self.index_file}")
        print(f"📊 Ordenação: Mais Recentes Primeiro ✓")
        
        # Mostra as 3 mais recentes para verificação
        print(f"\n📋 TOP 3 MAIS RECENTES:")
        for i, conv in enumerate(self.conversations[:3]):
            print(f"   #{conv['number']}: {conv['title']} ({conv['updated_at'] or conv['created_at']})")
        
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')

if __name__ == "__main__":
    system = QwenProcessorOptimized()
    system.generate_complete_system()
```

## Arquivo 2: Conversor PDF (Adaptado)

```python
# qwen_pdf_converter_optimized.py
import os
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile
import sys
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class PDFConverterOptimized:
    def __init__(self):
        self.md_dir = "qwen_markdown"
        self.pdf_dir = "qwen_pdfs"
        self.batch_size = 3
        
    def check_dependencies(self):
        """Verifica se todas as dependências estão instaladas"""
        print("🔍 Verificando dependências...")
        
        dependencies = {
            'pandoc': self.check_pandoc(),
            'selenium': self.check_selenium(),
            'chrome_driver': self.check_chrome_driver()
        }
        
        all_ok = all(dependencies.values())
        
        if not all_ok:
            print("\n⚠️  Dependências faltando:")
            for dep, installed in dependencies.items():
                if not installed:
                    print(f"   ❌ {dep}")
            
            print("\n📦 Instale as dependências faltantes:")
            if not dependencies['pandoc']:
                print("   Ubuntu/Debian: sudo apt-get install pandoc")
                print("   macOS: brew install pandoc")
                print("   Windows: choco install pandoc")
            
            if not dependencies['selenium']:
                print("   pip install selenium")
            
            if not dependencies['chrome_driver']:
                print("   Baixe ChromeDriver: https://chromedriver.chromium.org/")
                print("   Ou instale: pip install webdriver-manager")
        
        return all_ok

    def check_pandoc(self):
        """Verifica se pandoc está instalado"""
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ Pandoc: {version_line}")
                return True
        except:
            pass
        print("❌ Pandoc não encontrado")
        return False

    def check_selenium(self):
        """Verifica se selenium está disponível"""
        try:
            import selenium
            print("✅ Selenium: Disponível")
            return True
        except ImportError:
            print("❌ Selenium não instalado")
            return False

    def check_chrome_driver(self):
        """Verifica se ChromeDriver está disponível"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=chrome_options)
            driver.quit()
            print("✅ ChromeDriver: Disponível")
            return True
        except Exception as e:
            print(f"❌ ChromeDriver: {str(e)[:100]}...")
            return False

    def setup_chrome_driver(self):
        """Configura e retorna o driver do Chrome otimizado"""
        chrome_options = Options()
        
        # Otimizações para PDF com melhor qualidade
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        # Configurações para melhor qualidade de impressão
        chrome_options.add_argument('--enable-print-browser')
        chrome_options.add_argument('--disable-logging')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            print(f"❌ Erro ao iniciar ChromeDriver: {e}")
            return None

    def convert_with_pandoc_optimized(self, md_file):
        """Converte Markdown para HTML usando Pandoc otimizado"""
        try:
            # Template HTML com CORREÇÃO DE CONTRASTE
            html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{TITLE}}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        /* CORREÇÃO CRÍTICA: Garantir contraste adequado */
        * {
            color: #000000 !important; /* FORÇAR PRETO em todos os elementos */
        }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            line-height: 1.6;
            color: #000000 !important; /* PRETO para contraste máximo */
            background: #ffffff !important; /* BRANCO para fundo */
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important; 
            padding: 30px; 
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1, h2, h3, h4, h5, h6 { 
            color: #000000 !important; /* PRETO para todos os títulos */
            border-bottom: 2px solid #3498db; 
            padding-bottom: 8px;
            margin-top: 30px;
        }
        
        h1 { 
            color: #000000 !important;
            font-size: 28px;
        }
        
        h2 { 
            color: #000000 !important;
            font-size: 24px;
            border-bottom: 1px solid #3498db;
        }
        
        h3 { 
            color: #000000 !important;
            font-size: 20px;
        }
        
        .message { 
            margin: 15px 0; 
            padding: 15px; 
            border-radius: 8px;
            border-left: 4px solid #ccc;
            color: #000000 !important;
            background: #f8f9fa !important;
        }
        
        .user { 
            background: #e8f4fd !important; 
            border-left-color: #1976d2 !important;
            color: #000000 !important;
        }
        
        .assistant { 
            background: #f5e8f7 !important; 
            border-left-color: #7b1fa2 !important;
            color: #000000 !important;
        }
        
        code { 
            background: #2c3e50 !important; 
            color: #ffffff !important; /* Texto branco em fundo escuro */
            padding: 2px 6px; 
            border-radius: 4px; 
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }
        
        pre { 
            background: #2c3e50 !important; 
            color: #ffffff !important; /* Texto branco em fundo escuro */
            padding: 15px; 
            border-radius: 6px; 
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            line-height: 1.4;
            border: 1px solid #1a252f;
        }
        
        blockquote { 
            border-left: 4px solid #3498db !important; 
            padding-left: 20px; 
            margin-left: 0; 
            color: #000000 !important;
            background: #f8f9fa !important;
            padding: 10px 15px;
            border-radius: 4px;
        }
        
        hr { 
            border: none; 
            height: 2px; 
            background: linear-gradient(90deg, transparent, #3498db, transparent) !important;
            margin: 25px 0;
        }
        
        .footer { 
            text-align: center; 
            margin-top: 40px; 
            padding: 20px; 
            color: #000000 !important; 
            border-top: 2px solid #3498db;
            background: #f8f9fa !important;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: #ffffff !important;
            color: #000000 !important;
        }
        
        th, td {
            border: 2px solid #3498db !important;
            padding: 12px;
            text-align: left;
            color: #000000 !important;
        }
        
        th {
            background-color: #e8f4fd !important;
            color: #000000 !important;
            font-weight: bold;
        }
        
        td {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        p, div, span, li {
            color: #000000 !important;
        }
        
        strong, b {
            color: #000000 !important;
            font-weight: bold;
        }
        
        em, i {
            color: #000000 !important;
            font-style: italic;
        }
        
        a {
            color: #0066cc !important;
            text-decoration: underline;
        }
        
        /* Garantir que tudo seja visível na impressão */
        @media print {
            * {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color: #000000 !important;
            }
            body {
                background: white !important;
                color: black !important;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{TITLE}}</h1>
        <p>Conversa exportada do Qwen AI - PDF Otimizado</p>
    </div>
    
    {{CONTENT}}
    
    <div class="footer">
        <p>Gerado em {{DATE}}</p>
    </div>
    
    <script>
        // Forçar cores antes da impressão
        window.onload = function() {
            document.querySelectorAll('*').forEach(el => {
                el.style.color = '#000000';
                el.style.backgroundColor = el.classList.contains('header') ? '' : '#ffffff';
            });
        };
    </script>
</body>
</html>"""
            
            # Converter com Pandoc
            result = subprocess.run([
                'pandoc', str(md_file),
                '--from', 'markdown+emoji',
                '--to', 'html',
                '--standalone',
                '--mathjax'
            ], capture_output=True, text=True, encoding='utf-8', timeout=30)
            
            if result.returncode == 0:
                # Aplicar template personalizado
                html_content = html_template.replace('{{TITLE}}', md_file.stem)
                html_content = html_content.replace('{{CONTENT}}', result.stdout)
                html_content = html_content.replace('{{DATE}}', datetime.now().strftime('%d/%m/%Y %H:%M'))
                return html_content
            else:
                print(f"⚠️  Pandoc falhou: {result.stderr}")
                return self.convert_with_fallback(md_file)
                
        except subprocess.TimeoutExpired:
            print("⚠️  Timeout no Pandoc, usando fallback")
            return self.convert_with_fallback(md_file)
        except Exception as e:
            print(f"⚠️  Erro no Pandoc: {e}")
            return self.convert_with_fallback(md_file)

    def convert_with_fallback(self, md_file):
        """Conversão fallback sem Pandoc - otimizada"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Processamento mais simples e rápido
            html_content = self.simple_markdown_to_html(markdown_content, md_file.stem)
            return html_content
            
        except Exception as e:
            print(f"❌ Erro no fallback: {e}")
            return None

    def simple_markdown_to_html(self, markdown_text, title):
        """Conversor simples e rápido de Markdown para HTML com contraste garantido"""
        # Template com CONTRASTE GARANTIDO
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        /* GARANTIR CONTRASTE MÁXIMO */
        * {{
            color: #000000 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 25px; 
            line-height: 1.6; 
            color: #000000 !important; 
            background: #ffffff !important;
        }}
        
        .header {{ 
            background: #2c5aa0 !important; 
            color: #ffffff !important; 
            padding: 25px; 
            text-align: center; 
            border-radius: 8px;
            margin-bottom: 25px;
        }}
        
        .message {{ 
            margin: 15px 0; 
            padding: 15px; 
            border-radius: 6px;
            border-left: 4px solid #ccc;
            color: #000000 !important;
            background: #f8f9fa !important;
        }}
        
        .user {{ 
            background: #e3f2fd !important; 
            border-left-color: #1976d2 !important;
            color: #000000 !important;
        }}
        
        .assistant {{ 
            background: #f3e5f5 !important; 
            border-left-color: #7b1fa2 !important;
            color: #000000 !important;
        }}
        
        code {{ 
            background: #2c3e50 !important; 
            color: #ffffff !important;
            padding: 2px 6px; 
            border-radius: 3px; 
        }}
        
        pre {{ 
            background: #2c3e50 !important; 
            color: #ffffff !important;
            padding: 12px; 
            border-radius: 5px; 
            overflow-x: auto;
        }}
        
        .footer {{ 
            text-align: center; 
            margin-top: 30px; 
            padding: 15px; 
            color: #000000 !important; 
            border-top: 2px solid #2c5aa0;
            background: #f8f9fa !important;
        }}
        
        @media print {{
            * {{
                color: #000000 !important;
                background: transparent !important;
            }}
            body {{
                background: white !important;
                color: black !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Conversa exportada do Qwen AI</p>
    </div>
    
    {self.basic_markdown_processing(markdown_text)}
    
    <div class="footer">
        <p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
</body>
</html>"""

    def basic_markdown_processing(self, text):
        """Processamento básico de Markdown"""
        lines = text.split('\n')
        html_lines = []
        
        for line in lines:
            # Títulos
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            # Mensagens de usuário/assistente
            elif '👤 Você' in line or '🤖 Qwen AI' in line:
                if '👤 Você' in line:
                    html_lines.append(f'<div class="message user"><strong>{line}</strong></div>')
                else:
                    html_lines.append(f'<div class="message assistant"><strong>{line}</strong></div>')
            # Código
            elif line.strip().startswith('```'):
                html_lines.append('<pre><code>')
            elif line.strip() == '```':
                html_lines.append('</code></pre>')
            # Linha horizontal
            elif line.strip() == '---':
                html_lines.append('<hr>')
            # Parágrafo normal
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('<br>')
        
        return '\n'.join(html_lines)

    def html_to_pdf_selenium(self, html_content, pdf_path):
        """Converte HTML para PDF usando Selenium com configurações otimizadas"""
        driver = None
        try:
            driver = self.setup_chrome_driver()
            if not driver:
                return False
            
            # Criar arquivo HTML temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html = f.name
            
            # Carregar HTML
            driver.get(f'file://{temp_html}')
            
            # Aguardar carregamento
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Configurações de impressão otimizadas
            print_options = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'paperWidth': 8.27,  # A4
                'paperHeight': 11.69,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
                'scale': 1.0
            }
            
            # Executar comando de impressão
            result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
            pdf_data = base64.b64decode(result['data'])
            
            # Salvar PDF
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
            
            # Limpar arquivo temporário
            os.unlink(temp_html)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no Selenium: {e}")
            if driver:
                driver.quit()
            return False
        finally:
            if driver:
                driver.quit()

    def convert_batch(self):
        """Converte arquivos em lote"""
        print("🚀 INICIANDO CONVERSÃO EM LOTE")
        print("=" * 50)
        
        if not self.check_dependencies():
            print("\n❌ Dependências não atendidas. Instale as dependências faltantes.")
            return
        
        if not os.path.exists(self.md_dir):
            print(f"❌ Diretório não encontrado: {self.md_dir}")
            print("Execute primeiro: python qwen_processor_optimized.py")
            return
        
        os.makedirs(self.pdf_dir, exist_ok=True)
        
        md_files = list(Path(self.md_dir).glob("*.md"))
        md_files.sort()
        
        if not md_files:
            print("❌ Nenhum arquivo .md encontrado")
            return
        
        print(f"📁 Encontrados {len(md_files)} arquivos .md")
        print(f"📊 Tamanho do lote: {self.batch_size}")
        print(f"📁 PDFs serão salvos em: {self.pdf_dir}")
        
        successful = 0
        failed = 0
        
        for i, md_file in enumerate(md_files):
            print(f"\n🔄 [{i+1}/{len(md_files)}] Convertendo: {md_file.name}")
            
            pdf_filename = md_file.stem + '.pdf'
            pdf_path = Path(self.pdf_dir) / pdf_filename
            
            if pdf_path.exists():
                print(f"   ⏭️  PDF já existe, pulando...")
                successful += 1
                continue
            
            try:
                # Converter para HTML
                html_content = self.convert_with_pandoc_optimized(md_file)
                
                if not html_content:
                    print(f"   ❌ Falha na conversão HTML")
                    failed += 1
                    continue
                
                # Converter para PDF
                if self.html_to_pdf_selenium(html_content, pdf_path):
                    print(f"   ✅ PDF criado: {pdf_filename}")
                    successful += 1
                else:
                    print(f"   ❌ Falha na conversão PDF")
                    failed += 1
                
                # Pausa entre lotes
                if (i + 1) % self.batch_size == 0 and i + 1 < len(md_files):
                    print(f"\n⏸️  Pausa de 2 segundos...")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ Erro inesperado: {e}")
                failed += 1
        
        print(f"\n🎉 CONVERSÃO CONCLUÍDA!")
        print(f"✅ Sucessos: {successful}")
        print(f"❌ Falhas: {failed}")
        print(f"📁 Diretório: {self.pdf_dir}")
        
        if successful > 0:
            print(f"\n📋 PDFs criados:")
            pdf_files = list(Path(self.pdf_dir).glob("*.pdf"))
            for pdf in pdf_files:
                size_kb = pdf.stat().st_size / 1024
                print(f"   📄 {pdf.name} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    converter = PDFConverterOptimized()
    converter.convert_batch()
```

## Como usar:

1. **Primeiro, execute o processador:**
```bash
python qwen_processor_optimized.py
```

2. **Depois, execute o conversor:**
```bash
python qwen_pdf_converter_optimized.py
```

## Características do sistema:

- ✅ **Processamento otimizado** para arquivos JSON do Qwen AI
- ✅ **Ordenação automática** das conversas (mais recentes primeiro)
- ✅ **Índice HTML pesquisável** com interface moderna
- ✅ **Conversão para PDF** com qualidade otimizada
- ✅ **Suporte a emojis e formatação**
- ✅ **Processamento em lote** com pausas automáticas
- ✅ **Detecção de dependências** automática
- ✅ **Correção de contraste** nos PDFs

O sistema criará:
- `qwen_markdown/` - Arquivos Markdown organizados
- `qwen_pdfs/` - PDFs convertidos  
- `qwen_index.html` - Índice pesquisável

Execute os comandos na ordem e você terá um sistema completo para exportar e converter suas conversas do Qwen AI!

---

### 👤 Utilizador *(2025-11-02 23:29:26)* *[deepseek-chat]*

Está quase perfeito.  (Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas_Qwen3-Max>python qwen_processor_optimized.py
🚀 SISTEMA QWEN AI - Iniciando
==================================================
🔧 Extraindo conversas do Qwen AI...
📖 Lendo chat-export.json...
🎯 Processando 4 conversas...
✅ 01: 'Convert MD to HTML and PDF' - 8 mensagens
✅ 02: 'Acesso ao DeepSeek em Portugal' - 2 mensagens
✅ 03: 'Automóveis Diesel Fiáveis em Portugal' - 2 mensagens
✅ 04: 'Perguntas em Português' - 8 mensagens
🔄 Ordenando conversas do mais novo para o mais antigo...
⚠️  Erro ao converter timestamp '02/11/2025 14:57:41': Invalid isoformat string: '02/11/2025 14:57:41'
⚠️  Erro ao converter timestamp '06/02/2025 18:40:58': Invalid isoformat string: '06/02/2025 18:40:58'
⚠️  Erro ao converter timestamp '06/02/2025 18:39:06': Invalid isoformat string: '06/02/2025 18:39:06'
⚠️  Erro ao converter timestamp '04/02/2025 20:23:07': Invalid isoformat string: '04/02/2025 20:23:07'
📊 Total de conversas com mensagens: 4
📤 Salvando 4 conversas...
✅ 001_Convert_MD_to_HTML_and_PDF.md (📅 02/11/2025 14:57:41)
✅ 002_Acesso_ao_DeepSeek_em_Portugal.md (📅 06/02/2025 18:40:58)
✅ 003_Automóveis_Diesel_Fiáveis_em_Portugal.md (📅 06/02/2025 18:39:06)
✅ 004_Perguntas_em_Português.md (📅 04/02/2025 20:23:07)
🎉 4 arquivos criados em 'qwen_markdown'
🎯 Criando índice pesquisável...
✅ Índice criado: qwen_index.html

🎉 SISTEMA COMPLETO!
📁 Conversas: 4
📄 Índice: qwen_index.html
📊 Ordenação: Mais Recentes Primeiro ✓

📋 TOP 3 MAIS RECENTES:
   #1: Convert MD to HTML and PDF (02/11/2025 14:57:41)
   #2: Acesso ao DeepSeek em Portugal (06/02/2025 18:40:58)
   #3: Automóveis Diesel Fiáveis em Portugal (06/02/2025 18:39:06)

---

### 🤖 DeepSeek *(2025-11-02 23:29:26)* *[deepseek-chat]*

Perfeito! O sistema está funcionando bem, mas preciso corrigir a ordenação das datas. O problema é que as timestamps já estão formatadas como strings legíveis ("02/11/2025 14:57:41") em vez de timestamps Unix. Vou corrigir o parser de datas:

## Arquivo Corrigido: qwen_processor_optimized.py

```python
# qwen_processor_optimized.py
import json
import os
from datetime import datetime
import webbrowser
import re

class QwenProcessorOptimized:
    def __init__(self, json_file="chat-export.json"):
        self.json_file = json_file
        self.markdown_folder = "qwen_markdown"
        self.conversations = []
        self.index_file = "qwen_index.html"
        self.pdf_folder = "qwen_pdfs"
        
    def extract_qwen_conversations(self):
        """Extrai conversas do arquivo JSON do Qwen AI"""
        print("🔧 Extraindo conversas do Qwen AI...")
        
        if not os.path.exists(self.json_file):
            print(f"❌ Arquivo não encontrado: {self.json_file}")
            return False
        
        try:
            print("📖 Lendo chat-export.json...")
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data.get('success', False):
                print("❌ JSON não contém dados válidos")
                return False
            
            conversations_data = data.get('data', [])
            
            if not isinstance(conversations_data, list):
                print("❌ Formato inválido")
                return False
            
            print(f"🎯 Processando {len(conversations_data)} conversas...")
            
            # Processa cada conversa
            self.conversations = []
            for i, conv_data in enumerate(conversations_data):
                conversation = self.process_conversation(conv_data, i+1)
                if conversation and conversation['messages']:
                    self.conversations.append(conversation)
                    print(f"✅ {i+1:02d}: '{conversation['title']}' - {len(conversation['messages'])} mensagens")
                else:
                    print(f"⚠️  {i+1:02d}: '{conv_data.get('title', 'Sem título')}' - SEM MENSAGENS")
            
            # ORDENAÇÃO: do mais novo para o mais antigo
            print("🔄 Ordenando conversas do mais novo para o mais antigo...")
            self.conversations.sort(key=lambda x: self.parse_timestamp_for_sorting(
                x.get('raw_timestamp')
            ), reverse=True)
            
            # Reenumera as conversas após ordenação
            for i, conv in enumerate(self.conversations):
                conv['number'] = i + 1
            
            print(f"📊 Total de conversas com mensagens: {len(self.conversations)}")
            
            if self.conversations:
                self.save_as_markdown()
            
            return len(self.conversations) > 0
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def parse_timestamp_for_sorting(self, timestamp):
        """Converte timestamp para objeto datetime para ordenação"""
        if not timestamp:
            return datetime.min
        
        try:
            # Se for timestamp Unix (número)
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
            
            # Se já for string formatada (DD/MM/YYYY HH:MM:SS)
            elif isinstance(timestamp, str):
                # Tentar parse do formato DD/MM/YYYY HH:MM:SS
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', timestamp):
                    return datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
                # Tentar parse do formato ISO
                elif 'T' in timestamp:
                    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                # Tentar parse como timestamp Unix string
                else:
                    try:
                        return datetime.fromtimestamp(float(timestamp))
                    except:
                        pass
        except Exception as e:
            print(f"⚠️  Erro ao converter timestamp '{timestamp}': {e}")
        
        return datetime.min
    
    def process_conversation(self, conv_data, number):
        """Processa uma conversa individual do Qwen AI"""
        try:
            title = conv_data.get('title', f'Conversa {number}')
            conv_id = conv_data.get('id', f'conv_{number}')
            created_at = conv_data.get('created_at')
            updated_at = conv_data.get('updated_at')
            
            # Extrai mensagens do histórico
            chat_data = conv_data.get('chat', {})
            history = chat_data.get('history', {})
            messages_data = history.get('messages', {})
            
            messages = self.extract_messages_from_history(messages_data)
            
            # Usar o timestamp raw para ordenação
            raw_timestamp = updated_at or created_at
            
            return {
                'number': number,
                'id': conv_id,
                'title': title,
                'created_at': self.format_timestamp(created_at),
                'updated_at': self.format_timestamp(updated_at),
                'messages': messages,
                'message_count': len(messages),
                'summary': self.generate_summary(messages),
                'raw_timestamp': raw_timestamp  # Para ordenação (mantém formato original)
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao processar conversa {number}: {e}")
            return None
    
    def extract_messages_from_history(self, messages_data):
        """Extrai mensagens do histórico do Qwen AI"""
        messages = []
        
        # Converte o dicionário para lista ordenada
        message_list = []
        for msg_id, msg_data in messages_data.items():
            if isinstance(msg_data, dict):
                msg_data['_id'] = msg_id
                message_list.append(msg_data)
        
        # Ordena pela timestamp
        message_list.sort(key=lambda x: x.get('timestamp', 0))
        
        for msg_data in message_list:
            message = self.parse_message(msg_data)
            if message and message['content']:  # Só adiciona se tiver conteúdo
                messages.append(message)
        
        return messages
    
    def parse_message(self, message_data):
        """Analisa uma mensagem do Qwen AI"""
        try:
            role = message_data.get('role', '')
            
            if role == 'assistant':
                author_display = '🤖 Qwen AI'
                # Tenta extrair o nome do modelo
                model = message_data.get('model', '')
                if 'qwen' in model.lower():
                    model_display = f" ({model})"
                else:
                    model_display = f" ({message_data.get('modelName', '')})"
                author_display += model_display
            else:
                author_display = '👤 Você'
            
            # Extrai conteúdo da mensagem
            content = self.extract_content(message_data)
            
            if not content or content.isspace():
                return None
            
            # Timestamp
            timestamp = message_data.get('timestamp')
            
            return {
                'node_id': message_data.get('_id', ''),
                'author': author_display,
                'role': role,
                'content': content,
                'timestamp': self.format_timestamp(timestamp),
                'model': message_data.get('model', '')
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar mensagem: {e}")
            return None
    
    def extract_content(self, message_data):
        """Extrai conteúdo da mensagem do Qwen AI"""
        # Tenta diferentes formatos de conteúdo
        content = message_data.get('content', '')
        
        # Se content estiver vazio, tenta content_list
        if not content and 'content_list' in message_data:
            content_list = message_data['content_list']
            if content_list and isinstance(content_list, list):
                for item in content_list:
                    if isinstance(item, dict) and 'content' in item:
                        content = item['content']
                        break
        
        # Limpa o conteúdo
        if isinstance(content, str):
            return content.strip()
        elif isinstance(content, (list, dict)):
            return str(content)
        
        return ''
    
    def format_timestamp(self, timestamp):
        """Formata timestamp para exibição"""
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, (int, float)):
                # Converter timestamp Unix para formato legível
                return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
            elif isinstance(timestamp, str):
                # Se já estiver formatado, retorna como está
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', timestamp):
                    return timestamp
                # Tentar converter string ISO
                elif 'T' in timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return dt.strftime('%d/%m/%Y %H:%M:%S')
        except:
            pass
        
        return str(timestamp)
    
    def generate_summary(self, messages):
        """Gera resumo da conversa"""
        if not messages:
            return "Sem conteúdo"
        
        # Procura primeira mensagem do usuário
        for msg in messages:
            if msg.get('role') == 'user':
                content = msg['content']
                if len(content) > 100:
                    return content[:100] + "..."
                return content
        
        # Ou usa primeira mensagem qualquer
        first_msg = messages[0]['content']
        if len(first_msg) > 100:
            return first_msg[:100] + "..."
        return first_msg
    
    def save_as_markdown(self):
        """Salva como Markdown"""
        print(f"📤 Salvando {len(self.conversations)} conversas...")
        
        os.makedirs(self.markdown_folder, exist_ok=True)
        
        for conversation in self.conversations:
            md_content = self.create_markdown_content(conversation)
            
            safe_title = "".join(c for c in conversation['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conversation['number']:03d}_{safe_title}.md"
            filepath = os.path.join(self.markdown_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"✅ {filename} (📅 {conversation['updated_at'] or conversation['created_at']})")
        
        print(f"🎉 {len(self.conversations)} arquivos criados em '{self.markdown_folder}'")
    
    def create_markdown_content(self, conversation):
        """Cria conteúdo Markdown"""
        md = f"# 💬 {conversation['title']}\n\n"
        
        # Metadados
        md += "## 📊 Informações\n\n"
        md += f"- **Número:** #{conversation['number']}\n"
        md += f"- **ID:** {conversation['id']}\n"
        md += f"- **Criada em:** {conversation['created_at'] or 'N/A'}\n"
        if conversation['updated_at']:
            md += f"- **Atualizada em:** {conversation['updated_at']}\n"
        md += f"- **Total de mensagens:** {conversation['message_count']}\n"
        md += f"- **Resumo:** {conversation['summary']}\n\n"
        
        md += "---\n\n"
        
        # Mensagens
        md += "## 🗨️ Conversa\n\n"
        
        for j, message in enumerate(conversation['messages'], 1):
            timestamp = f" *({message['timestamp']})*" if message['timestamp'] else ""
            model_info = f" *[{message['model']}]*" if message.get('model') else ""
            md += f"### {message['author']}{timestamp}{model_info}\n\n"
            
            # Formata o conteúdo para melhor legibilidade
            content = message['content']
            # Adiciona quebras de linha para parágrafos longos
            content = content.replace('\n', '\n\n')
            md += f"{content}\n\n"
            
            if j < len(conversation['messages']):
                md += "---\n\n"
        
        # Rodapé
        md += "\n---\n\n"
        md += "*Conversa exportada do Qwen AI*  \n"
        md += f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        
        return md
    
    def create_searchable_index(self):
        """Cria índice HTML pesquisável"""
        print("🎯 Criando índice pesquisável...")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📚 Índice de Conversas - Qwen AI</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%); min-height: 100vh; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #0052d4, #4364f7); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
                .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 20px; flex-wrap: wrap; }}
                .stat-item {{ background: rgba(255,255,255,0.1); padding: 15px 25px; border-radius: 10px; backdrop-filter: blur(10px); }}
                .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }}
                .search-box {{ width: 100%; padding: 15px 20px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; }}
                .search-box:focus {{ border-color: #0052d4; box-shadow: 0 0 0 3px rgba(0, 82, 212, 0.1); }}
                .conversations-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; padding: 30px; }}
                .conversation-card {{ background: white; border: 1px solid #e9ecef; border-radius: 12px; padding: 20px; transition: all 0.3s ease; cursor: pointer; position: relative; }}
                .conversation-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: #0052d4; }}
                .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }}
                .card-number {{ background: #0052d4; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em; font-weight: bold; }}
                .card-title {{ font-size: 1.2em; font-weight: bold; color: #2c3e50; margin-bottom: 10px; line-height: 1.4; }}
                .card-summary {{ color: #6c757d; font-size: 0.95em; line-height: 1.5; margin-bottom: 15px; }}
                .card-meta {{ display: flex; justify-content: space-between; font-size: 0.85em; color: #868e96; border-top: 1px solid #e9ecef; padding-top: 15px; }}
                .card-actions {{ position: absolute; top: 15px; right: 15px; display: flex; gap: 5px; opacity: 0; transition: opacity 0.3s ease; }}
                .conversation-card:hover .card-actions {{ opacity: 1; }}
                .action-btn {{ background: white; border: 1px solid #e9ecef; border-radius: 5px; padding: 5px 10px; font-size: 0.8em; cursor: pointer; transition: all 0.3s ease; }}
                .action-btn:hover {{ background: #0052d4; color: white; border-color: #0052d4; }}
                .recent-badge {{ background: #ff6b6b; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; margin-left: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 Índice de Conversas</h1>
                    <p>Qwen AI - Histórico Completo (Mais Recentes Primeiro)</p>
                    <div class="stats">
                        <div class="stat-item">
                            <strong>Total:</strong> <span id="total-count">{len(self.conversations)}</span> conversas
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
                    <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo ou palavras-chave...">
                </div>
                
                <div class="conversations-grid" id="conversationsGrid">
        """
        
        # Adiciona cards (já ordenados do mais novo para o mais antigo)
        for i, conv in enumerate(self.conversations):
            safe_title = "".join(c for c in conv['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conv['number']:03d}_{safe_title}.md"
            
            recent_badge = ""
            if i < 3:  # Marca as 3 mais recentes
                recent_badge = "<span class='recent-badge'>NOVO</span>"
            
            html_content += f"""
                    <div class="conversation-card" data-title="{conv['title']}" data-summary="{conv['summary']}">
                        <div class="card-header">
                            <div class="card-number">#{conv['number']} {recent_badge}</div>
                            <div class="card-actions">
                                <button class="action-btn" onclick="openMD('{filename}')">MD</button>
                                <button class="action-btn" onclick="openPDF('{filename}')">PDF</button>
                            </div>
                        </div>
                        <div class="card-title">{conv['title']}</div>
                        <div class="card-summary">{conv['summary']}</div>
                        <div class="card-meta">
                            <span>📅 {conv['updated_at'] or conv['created_at'] or 'N/A'}</span>
                            <span>💬 {conv['message_count']} mensagens</span>
                        </div>
                    </div>
            """
        
        html_content += """
                </div>
            </div>

            <script>
                document.getElementById('searchInput').addEventListener('input', function(e) {
                    const searchTerm = e.target.value.toLowerCase();
                    const cards = document.querySelectorAll('.conversation-card');
                    let visibleCount = 0;
                    
                    cards.forEach(card => {
                        const title = card.getAttribute('data-title').toLowerCase();
                        const summary = card.getAttribute('data-summary').toLowerCase();
                        
                        if (title.includes(searchTerm) || summary.includes(searchTerm)) {
                            card.style.display = 'block';
                            visibleCount++;
                        } else {
                            card.style.display = 'none';
                        }
                    });
                    
                    document.getElementById('total-count').textContent = visibleCount;
                });
                
                function openMD(filename) {
                    window.open('""" + self.markdown_folder + """/' + filename, '_blank');
                }
                
                function openPDF(filename) {
                    const pdfFile = filename.replace('.md', '.pdf');
                    window.open('""" + self.pdf_folder + """/' + pdfFile, '_blank');
                }
                
                document.querySelectorAll('.conversation-card').forEach(card => {
                    card.addEventListener('click', function(e) {
                        if (!e.target.classList.contains('action-btn')) {
                            const filename = this.querySelector('.card-actions button').getAttribute('onclick').split("'")[1];
                            openMD(filename);
                        }
                    });
                });
            </script>
        </body>
        </html>
        """
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Índice criado: {self.index_file}")
    
    def generate_complete_system(self):
        """Gera sistema completo"""
        print("🚀 SISTEMA QWEN AI - Iniciando")
        print("=" * 50)
        
        success = self.extract_qwen_conversations()
        
        if not success:
            print("❌ Não foi possível extrair conversas")
            return
        
        self.create_searchable_index()
        
        print(f"\n🎉 SISTEMA COMPLETO!")
        print(f"📁 Conversas: {len(self.conversations)}")
        print(f"📄 Índice: {self.index_file}")
        print(f"📊 Ordenação: Mais Recentes Primeiro ✓")
        
        # Mostra as 3 mais recentes para verificação
        print(f"\n📋 TOP 3 MAIS RECENTES:")
        for i, conv in enumerate(self.conversations[:3]):
            print(f"   #{conv['number']}: {conv['title']} ({conv['updated_at'] or conv['created_at']})")
        
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')

if __name__ == "__main__":
    system = QwenProcessorOptimized()
    system.generate_complete_system()
```

## Principais correções:

1. **Parser de datas melhorado** - Agora reconhece o formato "DD/MM/YYYY HH:MM:SS"
2. **Mantém raw_timestamp** - Preserva o timestamp original para ordenação
3. **Formatação de conteúdo** - Melhor tratamento de quebras de linha no Markdown
4. **Detecção de formato** - Usa regex para identificar diferentes formatos de data

Agora a ordenação deve funcionar corretamente! Execute novamente:

```bash
python qwen_processor_optimized.py
```

E depois:

```bash
python qwen_pdf_converter_optimized.py
```

O sistema agora deve ordenar as conversas corretamente do mais recente para o mais antigo sem erros de parsing de datas!

---

*Conversa exportada do DeepSeek*
*Processado em: 23/11/2025 14:36*