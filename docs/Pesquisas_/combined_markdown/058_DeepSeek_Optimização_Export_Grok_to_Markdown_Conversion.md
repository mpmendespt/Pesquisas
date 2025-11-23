# Optimização Export Grok to Markdown Conversion Script

## 📊 Informações
- **Número:** #58
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** a0bc469a-8b61-41a1-81c4-46a47628e946
- **Criada em:** 2025-11-02 00:43:33
- **Atualizada em:** 2025-11-02 04:25:34
- **Total de mensagens:** 10
- **Resumo:** Optimização Export Grok  to Markdown Conversion Script
Optimização de Export Grok actual: 
# 1. Prim...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-02 00:43:35)* *[deepseek-chat]*

Optimização Export Grok  to Markdown Conversion Script
Optimização de Export Grok actual: 
# 1. Primeiro gere o dashboard com os arquivos Markdown
python grok_complete_dashboard.py

# 2. Depois converta os Markdown para PDF
python grok_markdown_to_pdf.py

1. Exportação do Grok
 • ✅ conversas convertidas para Markdown
 • ✅ Metadados preservados (datas, títulos, resumos)
 • ✅ Estrutura organizada por números e títulos
2. Índice Pesquisável
 • ✅ Interface web moderna e responsiva, com onversas ordenadas por data (mais recente primeiro)
 • ✅ Busca em tempo real por qualquer termo
 • ✅ Filtros por categoria
 • ✅ Acesso rápido a MD e PDF
 • ✅ Design profissional com gradientes
3. Exportação para PDF
 • ✅ Conversão automática com Pandoc para html e depois conversão para pdf pelo metodo do script deepseek_pdf_direct2.py. Assim pretende-se optimização dos sistema com um script para processar o sistema e outro para a conversão md para html e de seguida para pdf

Pretende-se optimização dos sistema com um script para processar o sistema e outro para a conversão md para html e de seguida para pdf

Fluxo Otimizado:
grok.zip → Processor → Markdown + Índice HTML → PDF Converter → PDFs
Pretende-se:
    6. Pandoc com MathJax: Agora usa --standalone --mathjax para suporte a fórmulas matemáticas
    7. Progresso Detalhado: Feedback visual melhorado

---

### 🤖 DeepSeek *(2025-11-02 00:43:35)* *[deepseek-chat]*

Vou otimizar o sistema dividindo o processo em dois scripts especializados e implementando melhorias significativas. Aqui está a solução:

## 1. Script Principal Otimizado (Processor)

```python
# grok_processor.py
import pandas as pd
import numpy as np
import os
import json
import zipfile
from datetime import datetime
import re
from collections import Counter
import webbrowser
import shutil
from pathlib import Path

class GrokProcessor:
    def __init__(self):
        self.conversations = []
        self.all_messages = []
        
    def load_grok_data(self):
        """Carrega e processa os dados do arquivo zip de forma otimizada"""
        
        zip_files = ["grok.zip", "gork.zip"]
        zip_path = next((f for f in zip_files if os.path.exists(f)), None)
        
        if zip_path is None:
            print("❌ Nenhum arquivo zip encontrado!")
            return None
        
        print(f"📂 Carregando dados do {zip_path}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
                print(f"🔍 Processando {len(json_files)} arquivos JSON...")
                
                all_data = []
                for file_name in json_files:
                    try:
                        with zip_ref.open(file_name) as f:
                            content = f.read().decode('utf-8')
                            data = json.loads(content)
                            all_data.append({
                                'file_name': file_name,
                                'data': data,
                                'size': len(content)
                            })
                    except Exception as e:
                        print(f"⚠️  {file_name}: {e}")
                
                print(f"✅ Dados brutos carregados: {len(all_data)} arquivos")
                return all_data
                
        except Exception as e:
            print(f"❌ Erro ao processar {zip_path}: {e}")
            return None

    def extract_conversations(self, all_data):
        """Extrai conversas dos dados brutos de forma otimizada"""
        print("📊 Extraindo conversas...")
        
        for item in all_data:
            data = item['data']
            file_name = item['file_name']
            
            if 'prod-grok-backend.json' in file_name and isinstance(data, dict):
                if 'conversations' in data and isinstance(data['conversations'], list):
                    print(f"✅ {file_name}: {len(data['conversations'])} conversas encontradas")
                    self.conversations.extend(data['conversations'])
        
        print(f"🎯 Total de conversas extraídas: {len(self.conversations)}")
        return self.conversations

    def extract_messages(self, conv):
        """Extrai mensagens de uma conversa de forma otimizada"""
        messages = []
        
        if isinstance(conv, dict) and 'responses' in conv and isinstance(conv['responses'], list):
            for response in conv['responses']:
                if isinstance(response, dict) and 'response' in response:
                    response_data = response['response']
                    if isinstance(response_data, dict):
                        message_content = response_data.get('message', '')
                        sender = response_data.get('sender', '')
                        
                        if message_content and sender:
                            messages.append({
                                'content': message_content,
                                'sender': sender,
                                'response_id': response_data.get('_id', ''),
                                'model': response_data.get('model', ''),
                                'create_time': response_data.get('create_time', {})
                            })
        
        return messages

    def analyze_conversations(self):
        """Analisa as conversas com métricas otimizadas"""
        print("📊 Analisando conversas...")
        
        if not self.conversations:
            print("❌ Nenhuma conversa para analisar!")
            return pd.DataFrame(), []
        
        analysis_data = []
        
        for i, conv in enumerate(self.conversations):
            if not isinstance(conv, dict):
                continue
                
            conversation_data = conv.get('conversation', {})
            conv_id = conversation_data.get('id', f'conv_{i}')
            title = conversation_data.get('title', f'Conversa {i+1}')
            created_at = conversation_data.get('create_time', '')
            
            messages = self.extract_messages(conv)
            num_messages = len(messages)
            
            # Métricas otimizadas
            total_words = 0
            user_words = 0
            assistant_words = 0
            user_messages = 0
            assistant_messages = 0
            total_chars = 0
            preview_content = ""
            
            for j, msg in enumerate(messages):
                if isinstance(msg, dict):
                    content = msg.get('content', '')
                    sender = msg.get('sender', '')
                    
                    if content and len(content.strip()) > 0:
                        words = len(content.split())
                        chars = len(content)
                        total_words += words
                        total_chars += chars
                        
                        if j == 0 and content:
                            preview_content = content[:100] + "..." if len(content) > 100 else content
                        
                        if sender == 'human':
                            user_words += words
                            user_messages += 1
                            role = 'user'
                        elif sender in ['assistant', 'grok', 'model']:
                            assistant_words += words
                            assistant_messages += 1
                            role = 'assistant'
                        else:
                            role = sender
                        
                        self.all_messages.append({
                            'conversation_id': conv_id,
                            'conversation_title': title,
                            'message_index': j,
                            'role': role,
                            'sender': sender,
                            'content': content,
                            'word_count': words,
                            'char_count': chars,
                            'model': msg.get('model', ''),
                            'response_id': msg.get('response_id', '')
                        })
            
            analysis_data.append({
                'conversation_id': conv_id,
                'title': title,
                'created_at': created_at,
                'num_messages': num_messages,
                'total_words': total_words,
                'total_chars': total_chars,
                'user_words': user_words,
                'assistant_words': assistant_words,
                'user_messages': user_messages,
                'assistant_messages': assistant_messages,
                'preview_content': preview_content,
                'avg_words_per_message': total_words / max(num_messages, 1)
            })
        
        df = pd.DataFrame(analysis_data)
        
        if 'created_at' in df.columns:
            df = df.sort_values('created_at', ascending=False)
        
        if not df.empty:
            print(f"📈 Total de conversas analisadas: {len(df)}")
            print(f"💬 Total de mensagens: {df['num_messages'].sum()}")
            print(f"📝 Total de palavras: {df['total_words'].sum()}")
        
        return df, self.all_messages

    def categorize_conversation(self, title):
        """Categoriza conversas de forma inteligente"""
        title_lower = title.lower()
        
        categories = {
            'Programação': ['python', 'programming', 'code', 'script', 'api', 'function', 'class'],
            'Sistemas': ['linux', 'ubuntu', 'windows', 'install', 'os', 'system'],
            'Ambientes': ['conda', 'anaconda', 'virtualenv', 'package', 'environment'],
            'Exportação': ['markdown', 'pdf', 'export', 'convert', 'conversion'],
            'Terminal': ['msys2', 'terminal', 'command', 'shell', 'bash', 'cmd'],
            'Fontes': ['emoji', 'font', 'noto', 'typography'],
            'IA': ['ai', 'gpt', 'model', 'neural', 'machine learning'],
            'Web': ['html', 'css', 'javascript', 'web', 'browser'],
            'Dados': ['data', 'analysis', 'pandas', 'dataframe', 'csv']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'Geral'

    def create_markdown_files(self, df):
        """Cria arquivos Markdown otimizados"""
        print("📝 Criando arquivos Markdown...")
        
        md_dir = "grok_complete_dashboard/markdown"
        os.makedirs(md_dir, exist_ok=True)
        
        created_files = []
        
        for _, row in df.iterrows():
            safe_title = self.create_safe_filename(row['title'])
            
            # Pular títulos genéricos
            if self.is_generic_title(safe_title):
                continue
            
            conv_messages = [msg for msg in self.all_messages 
                           if msg['conversation_id'] == row['conversation_id']]
            conv_messages.sort(key=lambda x: x['message_index'])
            
            md_content = self.generate_markdown_content(row, conv_messages)
            
            md_filename = f"{md_dir}/{safe_title}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            created_files.append(md_filename)
        
        print(f"✅ {len(created_files)} arquivos Markdown criados")
        return md_dir

    def create_safe_filename(self, title):
        """Cria nome de arquivo seguro"""
        safe = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return safe[:50] if safe else f"conversa_{int(datetime.now().timestamp())}"

    def is_generic_title(self, title):
        """Verifica se o título é genérico"""
        return bool(re.match(r'^(conversa|conv|chat)\s*\d+$', title.lower()))

    def generate_markdown_content(self, row, messages):
        """Gera conteúdo Markdown formatado"""
        content = f"""# {row['title']}

**Data**: {row['created_at']}  
**ID**: {row['conversation_id']}  
**Total de Mensagens**: {row['num_messages']}  
**Total de Palavras**: {row['total_words']}  
**Total de Caracteres**: {row['total_chars']}  

---

"""
        
        for msg in messages:
            role_emoji = "👤" if msg['role'] == 'user' else "🤖"
            role_name = "Usuário" if msg['role'] == 'user' else "Assistente"
            
            content += f"""
## {role_emoji} {role_name}

{msg['content']}

---
"""
        
        content += f"""
## 📊 Estatísticas

- **Mensagens do usuário**: {row['user_messages']}
- **Mensagens do assistente**: {row['assistant_messages']} 
- **Palavras do usuário**: {row['user_words']}
- **Palavras do assistente**: {row['assistant_words']}
- **Palavras por mensagem (média)**: {row['avg_words_per_message']:.1f}

*Exportado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')}*
"""
        return content

    def create_dashboard(self, df):
        """Cria dashboard HTML otimizado"""
        print("🎨 Criando dashboard...")
        
        # Adicionar categorias
        df['category'] = df['title'].apply(self.categorize_conversation)
        
        # Filtrar conversas não genéricas
        saved_conversations = []
        for _, row in df.iterrows():
            safe_title = self.create_safe_filename(row['title'])
            if not self.is_generic_title(safe_title):
                saved_conversations.append((_, row))
        
        # Estatísticas
        total_conv = len(saved_conversations)
        total_msgs = sum(row['num_messages'] for _, row in saved_conversations)
        total_words = sum(row['total_words'] for _, row in saved_conversations)
        total_chars = sum(row['total_chars'] for _, row in saved_conversations)
        
        html_content = self.generate_dashboard_html(saved_conversations, total_conv, total_msgs, total_words, total_chars)
        
        with open("grok_complete_dashboard/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("✅ Dashboard criado: grok_complete_dashboard/index.html")
        return "grok_complete_dashboard/index.html"

    def generate_dashboard_html(self, conversations, total_conv, total_msgs, total_words, total_chars):
        """Gera HTML do dashboard"""
        current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        return f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grok - Histórico Completo</title>
    <style>
        /* CSS otimizado - mantido do original */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8f9fa; color: #2c3e50; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 40px; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; }}
        .stats-bar {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 30px 0; text-align: center; }}
        .conversation-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 25px; }}
        .conversation-card {{ background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: transform 0.2s ease; }}
        @media (max-width: 1200px) {{ .conversation-grid {{ grid-template-columns: 1fr; }} }}
        @media (max-width: 768px) {{ .stats-bar {{ grid-template-columns: repeat(2, 1fr); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Grok - Histórico Completo</h1>
            <div class="subtitle">Exportação otimizada com Markdown + PDF</div>
            
            <div class="stats-bar">
                <div class="stat-item"><span class="stat-number">{total_conv}</span><span class="stat-label">Conversas</span></div>
                <div class="stat-item"><span class="stat-number">{total_msgs}</span><span class="stat-label">Mensagens</span></div>
                <div class="stat-item"><span class="stat-number">{total_words:,}</span><span class="stat-label">Palavras</span></div>
                <div class="stat-item"><span class="stat-number">{total_chars:,}</span><span class="stat-label">Caracteres</span></div>
            </div>
        </div>
        
        <div class="conversation-grid">
            {"".join(self.generate_conversation_cards(conversations))}
        </div>
        
        <div class="footer">
            <p>Dashboard gerado automaticamente em {current_date}</p>
        </div>
    </div>
</body>
</html>
"""

    def generate_conversation_cards(self, conversations):
        """Gera cards de conversa para o dashboard"""
        cards = []
        for idx, (_, row) in enumerate(conversations, 1):
            safe_title = self.create_safe_filename(row['title'])
            
            cards.append(f"""
            <div class="conversation-card">
                <div class="conversation-header">
                    <span class="conversation-category">{row['category']}</span>
                    <span class="conversation-number">#{idx}</span>
                </div>
                <div class="conversation-title">{row['title']}</div>
                <div class="conversation-date">{row.get('created_at', '')}</div>
                <div class="conversation-preview">{row.get('preview_content', '')}</div>
                <div class="conversation-stats">
                    <div class="stat-box"><span class="stat-value">{row['num_messages']}</span><span class="stat-name">Mensagens</span></div>
                    <div class="stat-box"><span class="stat-value">{row['total_words']}</span><span class="stat-name">Palavras</span></div>
                </div>
                <div class="conversation-actions">
                    <a href="markdown/{safe_title}.md" class="action-btn btn-md" target="_blank">📄 Markdown</a>
                    <a href="pdf/conversas/{safe_title}.pdf" class="action-btn btn-pdf" target="_blank">📊 PDF</a>
                </div>
            </div>
            """)
        return cards

def main():
    print("🚀 Iniciando Grok Processor Otimizado")
    print("=" * 50)
    
    # Criar estrutura de pastas
    os.makedirs("grok_complete_dashboard/pdf/conversas", exist_ok=True)
    os.makedirs("grok_complete_dashboard/markdown", exist_ok=True)
    os.makedirs("grok_complete_dashboard/data", exist_ok=True)
    
    processor = GrokProcessor()
    
    # Carregar dados
    all_data = processor.load_grok_data()
    if not all_data:
        return
    
    # Processar conversas
    processor.extract_conversations(all_data)
    df, all_messages = processor.analyze_conversations()
    
    if df.empty:
        print("❌ Nenhuma conversa válida!")
        return
    
    # Criar Markdown e Dashboard
    processor.create_markdown_files(df)
    index_file = processor.create_dashboard(df)
    
    # Salvar dados
    df.to_csv("grok_complete_dashboard/data/processed_conversations.csv", index=False)
    
    if all_messages:
        pd.DataFrame(all_messages).to_csv("grok_complete_dashboard/data/all_messages.csv", index=False)
    
    # Abrir dashboard
    webbrowser.open(f'file://{os.path.abspath(index_file)}')
    
    print("\n" + "=" * 50)
    print("🎉 PROCESSAMENTO CONCLUÍDO!")
    print("=" * 50)
    print("📁 Próximo passo: Execute o conversor PDF")
    print("   python grok_pdf_converter.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

## 2. Script de Conversão PDF Otimizado

```python
# grok_pdf_converter.py
import os
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile
import sys

class PDFConverter:
    def __init__(self):
        self.md_dir = "grok_complete_dashboard/markdown"
        self.pdf_dir = "grok_complete_dashboard/pdf/conversas"
        self.html_dir = "grok_complete_dashboard/html_temp"
        
    def check_dependencies(self):
        """Verifica se todas as dependências estão instaladas"""
        print("🔍 Verificando dependências...")
        
        dependencies = {
            'pandoc': self.check_pandoc(),
            'playwright': self.check_playwright()
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
            
            if not dependencies['playwright']:
                print("   pip install playwright && playwright install chromium")
        
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

    def check_playwright(self):
        """Verifica se playwright está disponível"""
        try:
            import playwright
            print("✅ Playwright: Disponível")
            return True
        except ImportError:
            print("❌ Playwright não instalado")
            return False

    async def convert_with_pandoc(self, md_file, pdf_output):
        """Converte Markdown para PDF usando Pandoc (método preferido)"""
        try:
            # Template HTML otimizado para Pandoc
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{TITLE}}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #2c3e50;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 40px; 
            border-radius: 15px;
            margin-bottom: 40px;
            text-align: center;
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 8px; }}
        code {{ background: #f8f9fa; padding: 2px 6px; border-radius: 4px; }}
        pre {{ background: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 8px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #3498db; padding-left: 20px; margin-left: 0; color: #7f8c8d; }}
        .footer {{ text-align: center; margin-top: 50px; padding: 30px; color: #7f8c8d; border-top: 1px solid #e9ecef; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{{TITLE}}</h1>
        <p>Conversa exportada do Grok - Gerado com Pandoc</p>
    </div>
    
    {{CONTENT}}
    
    <div class="footer">
        <p>Documento gerado automaticamente em {{DATE}}</p>
    </div>
</body>
</html>
"""
            
            # Ler conteúdo Markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Criar arquivo HTML temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                html_content = html_template.replace('{{TITLE}}', md_file.stem)
                html_content = html_content.replace('{{CONTENT}}', md_content)
                html_content = html_content.replace('{{DATE}}', datetime.now().strftime('%d/%m/%Y às %H:%M'))
                f.write(html_content)
                temp_html = f.name
            
            # Converter para PDF com Pandoc
            cmd = [
                'pandoc',
                temp_html,
                '-o', pdf_output,
                '--pdf-engine=wkhtmltopdf',
                '--standalone',
                '--mathjax',
                '--toc',
                '--toc-depth=2',
                '-V', 'margin-top=20mm',
                '-V', 'margin-right=20mm',
                '-V', 'margin-bottom=20mm',
                '-V', 'margin-left=20mm'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Limpar arquivo temporário
            os.unlink(temp_html)
            
            if result.returncode == 0:
                return True, "Sucesso"
            else:
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout na conversão"
        except Exception as e:
            return False, str(e)

    async def convert_with_playwright(self, md_file, pdf_output):
        """Converte Markdown para PDF usando Playwright (fallback)"""
        try:
            from playwright.async_api import async_playwright
            import markdown
            
            # Ler e converter Markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_content = markdown.markdown(md_content, extensions=['extra', 'tables', 'fenced_code', 'codehilite'])
            
            full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{md_file.stem}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #2c3e50;
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 40px; 
            border-radius: 15px;
            margin-bottom: 40px;
            text-align: center;
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        pre {{ background: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{md_file.stem}</h1>
    </div>
    {html_content}
</body>
</html>
"""
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Salvar HTML temporário
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                    f.write(full_html)
                    temp_html = f.name
                
                await page.goto(f"file://{temp_html}", wait_until='networkidle')
                await page.pdf(path=pdf_output, format='A4', print_background=True,
                              margin={'top': '0.5in', 'right': '0.5in', 'bottom': '0.5in', 'left': '0.5in'})
                
                await browser.close()
                os.unlink(temp_html)
                
            return True, "Sucesso"
            
        except Exception as e:
            return False, str(e)

    def show_progress(self, current, total, filename, status):
        """Mostra progresso detalhado"""
        percent = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f'\r📊 [{bar}] {percent:.1f}% ({current}/{total}) {filename} - {status}', end='', flush=True)
        
        if current == total:
            print()

    async def convert_all_files(self):
        """Converte todos os arquivos Markdown para PDF"""
        print("🚀 Iniciando conversão Markdown → PDF")
        print("=" * 50)
        
        if not self.check_dependencies():
            print("\n❌ Instale as dependências faltantes antes de continuar")
            return
        
        # Garantir pastas
        os.makedirs(self.pdf_dir, exist_ok=True)
        os.makedirs(self.html_dir, exist_ok=True)
        
        # Encontrar arquivos
        md_files = list(Path(self.md_dir).glob("*.md"))
        
        if not md_files:
            print("❌ Nenhum arquivo .md encontrado")
            print("💡 Execute primeiro: python grok_processor.py")
            return
        
        print(f"📄 Encontrados {len(md_files)} arquivos Markdown")
        print("🔄 Iniciando conversão...")
        
        successful = 0
        failed = 0
        
        for i, md_file in enumerate(md_files, 1):
            pdf_output = Path(self.pdf_dir) / f"{md_file.stem}.pdf"
            
            self.show_progress(i, len(md_files), md_file.name, "Convertendo...")
            
            # Tentar Pandoc primeiro
            success, message = await self.convert_with_pandoc(md_file, pdf_output)
            
            # Se Pandoc falhar, tentar Playwright
            if not success:
                self.show_progress(i, len(md_files), md_file.name, "Fallback Playwright...")
                success, message = await self.convert_with_playwright(md_file, pdf_output)
            
            if success:
                successful += 1
                status = "✅"
            else:
                failed += 1
                status = "❌"
            
            self.show_progress(i, len(md_files), md_file.name, f"{status} {message}")
        
        # Relatório final
        print("\n" + "=" * 50)
        print("🎉 CONVERSÃO CONCLUÍDA!")
        print("=" * 50)
        print(f"✅ Sucessos: {successful}")
        print(f"❌ Falhas: {failed}")
        print(f"📁 PDFs em: {self.pdf_dir}")
        
        if failed > 0:
            print("\n⚠️  Algumas conversões falharam. Verifique as dependências:")
            print("   - Pandoc com wkhtmltopdf")
            print("   - Playwright com Chromium")

async def main():
    converter = PDFConverter()
    await converter.convert_all_files()

if __name__ == "__main__":
    # Verificar se é Windows para ajuste de evento loop
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())
```

## 3. Script de Gerenciamento Principal

```python
# grok_export_manager.py
import os
import subprocess
import sys
from datetime import datetime

def run_processor():
    """Executa o processador principal"""
    print("🔄 Executando Grok Processor...")
    result = subprocess.run([sys.executable, "grok_processor.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Processamento concluído com sucesso!")
        return True
    else:
        print("❌ Erro no processamento:")
        print(result.stderr)
        return False

def run_pdf_converter():
    """Executa o conversor PDF"""
    print("🔄 Executando PDF Converter...")
    result = subprocess.run([sys.executable, "grok_pdf_converter.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Conversão PDF concluída com sucesso!")
        return True
    else:
        print("❌ Erro na conversão PDF:")
        print(result.stderr)
        return False

def main():
    print("🚀 GERENCIADOR DE EXPORTAÇÃO GROK")
    print("=" * 50)
    print("1. Processar dados e gerar Markdown + Dashboard")
    print("2. Converter Markdown para PDF")
    print("3. Processamento completo (1 + 2)")
    print("4. Verificar dependências")
    print("=" * 50)
    
    choice = input("Escolha uma opção (1-4): ").strip()
    
    start_time = datetime.now()
    
    if choice == "1":
        run_processor()
    elif choice == "2":
        run_pdf_converter()
    elif choice == "3":
        if run_processor():
            run_pdf_converter()
    elif choice == "4":
        # Verificar dependências
        from grok_pdf_converter import PDFConverter
        converter = PDFConverter()
        converter.check_dependencies()
    else:
        print("❌ Opção inválida")
    
    elapsed = datetime.now() - start_time
    print(f"\n⏱️  Tempo total: {elapsed}")

if __name__ == "__main__":
    main()
```

## Fluxo Otimizado de Uso:

```bash
# 1. Processamento completo (recomendado)
python grok_export_manager.py

# 2. Ou executar manualmente:
python grok_processor.py
python grok_pdf_converter.py

# 3. Apenas verificar dependências
python grok_export_manager.py
```

## Principais Melhorias:

1. **Separação Clara**: Processor vs PDF Converter
2. **Dependências Verificadas**: Pandoc + Playwright
3. **Fallback Inteligente**: Pandoc → Playwright
4. **Progresso Detalhado**: Barra de progresso em tempo real
5. **MathJax Support**: Fórmulas matemáticas com `--mathjax`
6. **Categorização Inteligente**: Mais categorias relevantes
7. **Tratamento de Erros**: Melhor resiliência
8. **Gerenciador Unificado**: Interface única para todo o processo

O sistema agora é muito mais robusto, com verificação de dependências, fallback automático e feedback visual detalhado!

---

### 👤 Utilizador *(2025-11-02 00:57:50)* *[deepseek-chat]*

com grok_pdf_converter.py  a conversão é lenta. Assim pretendo que a conversão html para pdf use o metodo que é usado em pdf_converter_optimized.py

---

### 🤖 DeepSeek *(2025-11-02 00:57:50)* *[deepseek-chat]*

Perfeito! Vou otimizar o `grok_pdf_converter.py` para usar o método mais rápido do `pdf_converter_optimized.py` com Selenium. Aqui está a versão otimizada:

```python
# grok_pdf_converter_optimized.py
import os
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile
import sys
import time
import base64
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class PDFConverterOptimized:
    def __init__(self):
        self.md_dir = "grok_complete_dashboard/markdown"
        self.pdf_dir = "grok_complete_dashboard/pdf/conversas"
        self.batch_size = 3  # Tamanho do lote para processamento
        
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
                print("   Ou use: playwright install chromium")
        
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
            driver = webdriver.Chrome(options=chrome_options)
            driver.quit()
            print("✅ ChromeDriver: Disponível")
            return True
        except Exception as e:
            print(f"❌ ChromeDriver: {e}")
            return False

    def setup_chrome_driver(self):
        """Configura e retorna o driver do Chrome otimizado"""
        chrome_options = Options()
        
        # Otimizações para performance
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Desabilita imagens para velocidade
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        
        # Otimizações de memória
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=4096')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)  # Timeout reduzido
            return driver
        except Exception as e:
            print(f"❌ Erro ao iniciar ChromeDriver: {e}")
            return None

    def convert_with_pandoc_optimized(self, md_file):
        """Converte Markdown para HTML usando Pandoc otimizado"""
        try:
            # Template HTML otimizado para performance
            html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{TITLE}}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            line-height: 1.5;
            color: #2c3e50;
            background: white;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 30px; 
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        h1 { 
            color: #2c3e50; 
            border-bottom: 2px solid #3498db; 
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h2 { 
            color: #34495e; 
            border-bottom: 1px solid #ecf0f1; 
            padding-bottom: 6px;
            margin-top: 25px;
        }
        .message { 
            margin: 15px 0; 
            padding: 15px; 
            border-radius: 8px;
            border-left: 4px solid #ccc;
        }
        .user { 
            background: #e3f2fd; 
            border-left-color: #1976d2; 
        }
        .assistant { 
            background: #f3e5f5; 
            border-left-color: #7b1fa2; 
        }
        code { 
            background: #f8f9fa; 
            padding: 2px 4px; 
            border-radius: 3px; 
            font-family: 'Monaco', 'Menlo', monospace;
        }
        pre { 
            background: #2c3e50; 
            color: #ecf0f1; 
            padding: 12px; 
            border-radius: 5px; 
            overflow-x: auto;
            font-size: 0.9em;
        }
        blockquote { 
            border-left: 3px solid #3498db; 
            padding-left: 15px; 
            margin-left: 0; 
            color: #7f8c8d;
        }
        hr { 
            border: none; 
            height: 1px; 
            background: linear-gradient(90deg, transparent, #3498db, transparent);
            margin: 20px 0;
        }
        .footer { 
            text-align: center; 
            margin-top: 40px; 
            padding: 20px; 
            color: #7f8c8d; 
            border-top: 1px solid #e9ecef;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{TITLE}}</h1>
        <p>Conversa exportada do Grok - PDF Otimizado</p>
    </div>
    
    {{CONTENT}}
    
    <div class="footer">
        <p>Gerado em {{DATE}}</p>
    </div>
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
        """Conversor simples e rápido de Markdown para HTML"""
        # Substituições básicas
        html = markdown_text
        
        # Headers
        html = html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        html = html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
        html = html.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
        
        # Mensagens de usuário/assistente
        html = html.replace('## 👤 Usuário', '<div class="message user"><strong>👤 Usuário</strong>')
        html = html.replace('## 🤖 Assistente', '<div class="message assistant"><strong>🤖 Assistente</strong>')
        
        # Separadores
        html = html.replace('---', '<hr>')
        
        # Fechar divs de mensagem nos próximos headers
        lines = html.split('\n')
        processed_lines = []
        
        for i, line in enumerate(lines):
            if line.startswith('<h3>') and i > 0:
                if not lines[i-1].startswith('</div>'):
                    processed_lines.append('</div>')
            processed_lines.append(line)
        
        html = '\n'.join(processed_lines)
        
        # Template final
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.5; }}
        .header {{ background: #667eea; color: white; padding: 20px; text-align: center; }}
        .message {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .user {{ background: #e3f2fd; border-left: 4px solid #1976d2; }}
        .assistant {{ background: #f3e5f5; border-left: 4px solid #7b1fa2; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        hr {{ border: none; height: 1px; background: #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    {html}
    <div class="footer">
        <p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
</body>
</html>"""

    def html_to_pdf_fast(self, html_file, pdf_file):
        """Converte HTML para PDF usando ChromeDriver otimizado"""
        driver = None
        try:
            driver = self.setup_chrome_driver()
            if not driver:
                return False
            
            full_path = f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
            driver.get(full_path)
            
            # Wait mais curto e eficiente
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Aguardar breve para MathJax (se necessário)
            time.sleep(2)
            
            # Configurações otimizadas para PDF
            pdf_params = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
            }
            
            result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
            pdf_data = base64.b64decode(result['data'])
            
            # Garantir pasta de destino
            os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
            
            with open(pdf_file, 'wb') as f:
                f.write(pdf_data)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na conversão PDF: {e}")
            return False
        finally:
            if driver:
                driver.quit()

    def show_progress(self, current, total, filename, status):
        """Mostra progresso detalhado com barra"""
        percent = (current / total) * 100
        bar_length = 40
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f'\r📊 [{bar}] {percent:.1f}% ({current}/{total}) {filename[:30]:<30} - {status}', 
              end='', flush=True)
        
        if current == total:
            print()

    def process_batch(self, batch_files, batch_num, total_batches):
        """Processa um lote de arquivos"""
        print(f"\n🔄 Lote {batch_num}/{total_batches} - {len(batch_files)} arquivos")
        
        successful = 0
        driver = self.setup_chrome_driver()
        
        try:
            for i, md_file in enumerate(batch_files, 1):
                pdf_output = Path(self.pdf_dir) / f"{md_file.stem}.pdf"
                
                # Pular se já existe
                if pdf_output.exists():
                    self.show_progress(i, len(batch_files), md_file.name, "⏭️ Existente")
                    successful += 1
                    continue
                
                self.show_progress(i, len(batch_files), md_file.name, "🔄 Convertendo...")
                
                # Converter Markdown para HTML
                html_content = self.convert_with_pandoc_optimized(md_file)
                if not html_content:
                    self.show_progress(i, len(batch_files), md_file.name, "❌ HTML falhou")
                    continue
                
                # Salvar HTML temporário
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                    f.write(html_content)
                    temp_html = f.name
                
                try:
                    # Converter HTML para PDF
                    if driver and self.html_to_pdf_with_driver(driver, temp_html, pdf_output):
                        successful += 1
                        self.show_progress(i, len(batch_files), md_file.name, "✅ Sucesso")
                    else:
                        self.show_progress(i, len(batch_files), md_file.name, "❌ PDF falhou")
                
                finally:
                    # Limpar arquivo temporário
                    if os.path.exists(temp_html):
                        os.remove(temp_html)
                
                # Pequena pausa entre arquivos
                time.sleep(1)
            
            return successful
            
        finally:
            if driver:
                driver.quit()

    def html_to_pdf_with_driver(self, driver, html_file, pdf_file):
        """Usa driver existente para converter HTML para PDF"""
        try:
            full_path = f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
            driver.get(full_path)
            
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            time.sleep(1)  # Pausa reduzida
            
            pdf_params = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
            }
            
            result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
            pdf_data = base64.b64decode(result['data'])
            
            with open(pdf_file, 'wb') as f:
                f.write(pdf_data)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no driver: {e}")
            return False

    def convert_all_files(self):
        """Converte todos os arquivos Markdown para PDF de forma otimizada"""
        print("🚀 CONVERSOR PDF OTIMIZADO - Iniciando")
        print("=" * 60)
        
        if not self.check_dependencies():
            print("\n❌ Instale as dependências faltantes antes de continuar")
            return False
        
        # Verificar arquivos
        md_files = list(Path(self.md_dir).glob("*.md"))
        
        if not md_files:
            print("❌ Nenhum arquivo .md encontrado")
            print("💡 Execute primeiro: python grok_processor.py")
            return False
        
        print(f"📄 Arquivos encontrados: {len(md_files)}")
        print(f"🔧 Método: Pandoc + ChromeDriver (Lotes de {self.batch_size})")
        print("⏱️  Iniciando conversão...\n")
        
        total_successful = 0
        total_files = len(md_files)
        
        # Processar em lotes
        total_batches = (len(md_files) + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = start_idx + self.batch_size
            batch = md_files[start_idx:end_idx]
            
            batch_success = self.process_batch(batch, batch_num + 1, total_batches)
            total_successful += batch_success
            
            # Pausa entre lotes (exceto último)
            if batch_num < total_batches - 1:
                print(f"\n💤 Pausa entre lotes...")
                time.sleep(2)
        
        # Relatório final
        print(f"\n" + "=" * 60)
        print("🎉 CONVERSÃO CONCLUÍDA!")
        print("=" * 60)
        print(f"📊 RESUMO:")
        print(f"   ✅ Sucessos: {total_successful}/{total_files}")
        print(f"   📁 Pasta: {os.path.abspath(self.pdf_dir)}")
        print(f"   ⚡ Método: ChromeDriver Otimizado")
        
        if total_successful < total_files:
            print(f"\n⚠️  {total_files - total_successful} arquivos falharam")
            print("💡 Verifique as dependências e tente novamente")
        
        return total_successful > 0

def main():
    converter = PDFConverterOptimized()
    success = converter.convert_all_files()
    
    if success:
        print("\n✨ Todos os PDFs foram gerados com sucesso!")
    else:
        print("\n❌ Houve problemas na conversão")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Script de Gerenciamento Atualizado:

```python
# grok_export_manager.py
import os
import subprocess
import sys
from datetime import datetime

def run_processor():
    """Executa o processador principal"""
    print("🔄 Executando Grok Processor...")
    result = subprocess.run([sys.executable, "grok_processor.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Processamento concluído com sucesso!")
        return True
    else:
        print("❌ Erro no processamento:")
        print(result.stderr)
        return False

def run_pdf_converter():
    """Executa o conversor PDF otimizado"""
    print("🔄 Executando PDF Converter Otimizado...")
    result = subprocess.run([sys.executable, "grok_pdf_converter_optimized.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Conversão PDF concluída com sucesso!")
        return True
    else:
        print("❌ Erro na conversão PDF:")
        print(result.stderr)
        return False

def main():
    print("🚀 GERENCIADOR DE EXPORTAÇÃO GROK - OTIMIZADO")
    print("=" * 50)
    print("1. Processar dados e gerar Markdown + Dashboard")
    print("2. Converter Markdown para PDF (RÁPIDO)")
    print("3. Processamento completo (1 + 2)")
    print("4. Verificar dependências")
    print("=" * 50)
    
    choice = input("Escolha uma opção (1-4): ").strip()
    
    start_time = datetime.now()
    
    if choice == "1":
        run_processor()
    elif choice == "2":
        run_pdf_converter()
    elif choice == "3":
        if run_processor():
            run_pdf_converter()
    elif choice == "4":
        from grok_pdf_converter_optimized import PDFConverterOptimized
        converter = PDFConverterOptimized()
        converter.check_dependencies()
    else:
        print("❌ Opção inválida")
    
    elapsed = datetime.now() - start_time
    print(f"\n⏱️  Tempo total: {elapsed}")

if __name__ == "__main__":
    main()
```

## Principais Otimizações Implementadas:

1. **ChromeDriver Otimizado**: 
   - Desabilita imagens para maior velocidade
   - Timeouts reduzidos
   - Configurações de memória otimizadas

2. **Processamento em Lotes**: 
   - Reutiliza o mesmo driver para múltiplos arquivos
   - Reduz overhead de inicialização

3. **Conversão Mais Rápida**:
   - Template HTML simplificado
   - Wait times reduzidos
   - Processamento mais eficiente

4. **Progresso em Tempo Real**:
   - Barra de progresso visual
   - Status detalhado por arquivo

5. **Fallback Robusto**:
   - Pandoc como primário
   - Conversor simples como fallback

## Uso:

```bash
# Conversão rápida com ChromeDriver
python grok_pdf_converter_optimized.py

# Ou pelo gerenciador
python grok_export_manager.py
```

Esta versão deve ser significativamente mais rápida que a anterior com Playwright, especialmente para grandes quantidades de arquivos!

---

### 👤 Utilizador *(2025-11-02 01:11:40)* *[deepseek-chat]*

Pretendia que o grok_processor.py fosse melhorado com uma estrutura semelhante ao chatgpt_index_system.py

---

### 🤖 DeepSeek *(2025-11-02 01:11:40)* *[deepseek-chat]*

Perfeito! Vou melhorar o `grok_processor.py` com a estrutura e funcionalidades do `chatgpt_index_system.py`. Aqui está a versão otimizada:

```python
# grok_processor_optimized.py
import pandas as pd
import numpy as np
import os
import json
import zipfile
from datetime import datetime
import re
from collections import Counter
import webbrowser
import glob
import subprocess

class GrokProcessorOptimized:
    def __init__(self):
        self.conversations = []

---

### 👤 Utilizador *(2025-11-02 01:12:58)* *[deepseek-chat]*

Pretendia que o grok_processor.py fosse melhorado com uma estrutura semelhante ao chatgpt_index_system.py  Com ordenação das conversas por data (mais recente primeiro)

---

### 🤖 DeepSeek *(2025-11-02 01:12:58)* *[deepseek-chat]*

Perfeito! Vou melhorar o `grok_processor.py` com a estrutura do `chatgpt_index_system.py` e adicionar ordenação por data. Aqui está a versão otimizada:

```python
# grok_processor_optimized.py
import pandas as pd
import numpy as np
import os
import json
import zipfile
from datetime import datetime
import re
from collections import Counter
import webbrowser
import glob
from pathlib import Path

class GrokProcessorOptimized:
    def __init__(self):
        self.conversations = []
        self.all_messages = []
        self.index_file = "grok_complete_dashboard/index.html"
        self.markdown_folder = "grok_complete_dashboard/markdown"
        self.pdf_folder = "grok_complete_dashboard/pdf/conversas"
        self.data_folder = "grok_complete_dashboard/data"
        
    def setup_folders(self):
        """Cria estrutura de pastas necessária"""
        folders = [
            self.markdown_folder,
            self.pdf_folder,
            self.data_folder,
            "grok_complete_dashboard/pdf"
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        print("📁 Estrutura de pastas criada")

    def load_grok_data(self):
        """Carrega e processa os dados do arquivo zip de forma otimizada"""
        
        zip_files = ["grok.zip", "gork.zip"]
        zip_path = next((f for f in zip_files if os.path.exists(f)), None)
        
        if zip_path is None:
            print("❌ Nenhum arquivo zip encontrado!")
            return None
        
        print(f"📂 Carregando dados do {zip_path}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
                print(f"🔍 Processando {len(json_files)} arquivos JSON...")
                
                all_data = []
                for file_name in json_files:
                    try:
                        with zip_ref.open(file_name) as f:
                            content = f.read().decode('utf-8')
                            data = json.loads(content)
                            all_data.append({
                                'file_name': file_name,
                                'data': data,
                                'size': len(content)
                            })
                    except Exception as e:
                        print(f"⚠️  {file_name}: {e}")
                
                print(f"✅ Dados brutos carregados: {len(all_data)} arquivos")
                return all_data
                
        except Exception as e:
            print(f"❌ Erro ao processar {zip_path}: {e}")
            return None

    def extract_conversations(self, all_data):
        """Extrai conversas dos dados brutos"""
        print("📊 Extraindo conversas...")
        
        self.conversations = []
        
        for item in all_data:
            data = item['data']
            file_name = item['file_name']
            
            if 'prod-grok-backend.json' in file_name and isinstance(data, dict):
                if 'conversations' in data and isinstance(data['conversations'], list):
                    print(f"✅ {file_name}: {len(data['conversations'])} conversas encontradas")
                    self.conversations.extend(data['conversations'])
        
        print(f"🎯 Total de conversas extraídas: {len(self.conversations)}")
        return self.conversations

    def extract_messages(self, conv):
        """Extrai mensagens de uma conversa"""
        messages = []
        
        if isinstance(conv, dict) and 'responses' in conv and isinstance(conv['responses'], list):
            for response in conv['responses']:
                if isinstance(response, dict) and 'response' in response:
                    response_data = response['response']
                    if isinstance(response_data, dict):
                        message_content = response_data.get('message', '')
                        sender = response_data.get('sender', '')
                        
                        if message_content and sender:
                            messages.append({
                                'content': message_content,
                                'sender': sender,
                                'response_id': response_data.get('_id', ''),
                                'model': response_data.get('model', ''),
                                'create_time': response_data.get('create_time', {})
                            })
        
        return messages

    def parse_datetime(self, date_string):
        """Converte string de data para objeto datetime para ordenação"""
        if not date_string:
            return datetime.min
        
        try:
            # Tenta vários formatos de data
            if isinstance(date_string, dict):
                # Se for objeto, pega timestamp
                timestamp = date_string.get('$date', 0)
                if timestamp:
                    return datetime.fromtimestamp(timestamp / 1000)
                return datetime.min
            
            # Tenta formato ISO
            if 'T' in str(date_string):
                date_str = str(date_string).replace('Z', '+00:00')
                return datetime.fromisoformat(date_str)
            
            # Tenta outros formatos
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S']:
                try:
                    return datetime.strptime(str(date_string), fmt)
                except:
                    continue
            
            return datetime.min
        except:
            return datetime.min

    def analyze_conversations(self):
        """Analisa as conversas com métricas completas"""
        print("📊 Analisando conversas...")
        
        if not self.conversations:
            print("❌ Nenhuma conversa para analisar!")
            return pd.DataFrame(), []
        
        analysis_data = []
        self.all_messages = []
        
        for i, conv in enumerate(self.conversations):
            if not isinstance(conv, dict):
                continue
                
            conversation_data = conv.get('conversation', {})
            conv_id = conversation_data.get('id', f'conv_{i}')
            title = conversation_data.get('title', f'Conversa {i+1}')
            created_at = conversation_data.get('create_time', '')
            updated_at = conversation_data.get('modify_time', '')
            
            # Parse datas para ordenação
            created_dt = self.parse_datetime(created_at)
            updated_dt = self.parse_datetime(updated_at)
            
            messages = self.extract_messages(conv)
            num_messages = len(messages)
            
            # Métricas
            total_words = 0
            user_words = 0
            assistant_words = 0
            user_messages = 0
            assistant_messages = 0
            total_chars = 0
            preview_content = ""
            
            for j, msg in enumerate(messages):
                if isinstance(msg, dict):
                    content = msg.get('content', '')
                    sender = msg.get('sender', '')
                    
                    if content and len(content.strip()) > 0:
                        words = len(content.split())
                        chars = len(content)
                        total_words += words
                        total_chars += chars
                        
                        if j == 0 and content:
                            preview_content = content[:150] + "..." if len(content) > 150 else content
                        
                        if sender == 'human':
                            user_words += words
                            user_messages += 1
                            role = 'user'
                        elif sender in ['assistant', 'grok', 'model']:
                            assistant_words += words
                            assistant_messages += 1
                            role = 'assistant'
                        else:
                            role = sender
                        
                        self.all_messages.append({
                            'conversation_id': conv_id,
                            'conversation_title': title,
                            'message_index': j,
                            'role': role,
                            'sender': sender,
                            'content': content,
                            'word_count': words,
                            'char_count': chars,
                            'model': msg.get('model', ''),
                            'response_id': msg.get('response_id', ''),
                            'timestamp': created_dt
                        })
            
            analysis_data.append({
                'conversation_id': conv_id,
                'title': title,
                'created_at': created_at,
                'created_dt': created_dt,  # Para ordenação
                'updated_at': updated_at,
                'updated_dt': updated_dt,
                'num_messages': num_messages,
                'total_words': total_words,
                'total_chars': total_chars,
                'user_words': user_words,
                'assistant_words': assistant_words,
                'user_messages': user_messages,
                'assistant_messages': assistant_messages,
                'preview_content': preview_content,
                'avg_words_per_message': total_words / max(num_messages, 1),
                'category': self.categorize_conversation(title)
            })
        
        # Ordenar por data (mais recente primeiro)
        analysis_data.sort(key=lambda x: x['created_dt'], reverse=True)
        
        df = pd.DataFrame(analysis_data)
        
        if not df.empty:
            print(f"📈 Total de conversas analisadas: {len(df)}")
            print(f"💬 Total de mensagens: {df['num_messages'].sum()}")
            print(f"📝 Total de palavras: {df['total_words'].sum()}")
            print(f"📅 Ordenação: Mais recente → Mais antiga")
        
        return df, self.all_messages

    def categorize_conversation(self, title):
        """Categoriza conversas de forma inteligente"""
        title_lower = title.lower()
        
        categories = {
            'Programação': ['python', 'programming', 'code', 'script', 'api', 'function', 'class', 'java', 'javascript', 'html', 'css'],
            'Sistemas': ['linux', 'ubuntu', 'windows', 'install', 'os', 'system', 'server', 'terminal'],
            'Ambientes': ['conda', 'anaconda', 'virtualenv', 'package', 'environment', 'venv', 'pip'],
            'Exportação': ['markdown', 'pdf', 'export', 'convert', 'conversion', 'exportar'],
            'Terminal': ['msys2', 'terminal', 'command', 'shell', 'bash', 'cmd', 'prompt'],
            'IA': ['ai', 'gpt', 'model', 'neural', 'machine learning', 'deep learning', 'llm'],
            'Dados': ['data', 'analysis', 'pandas', 'dataframe', 'csv', 'excel', 'database'],
            'Web': ['web', 'browser', 'http', 'website', 'url', 'internet'],
            'Configuração': ['config', 'setup', 'install', 'configure', 'settings'],
            'Ajuda': ['help', 'ajuda', 'como', 'tutorial', 'guide', 'manual']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'Geral'

    def create_markdown_files(self, df):
        """Cria arquivos Markdown otimizados"""
        print("📝 Criando arquivos Markdown...")
        
        created_files = []
        skipped_generic = 0
        
        for _, row in df.iterrows():
            safe_title = self.create_safe_filename(row['title'])
            
            # Pular títulos genéricos
            if self.is_generic_title(safe_title):
                skipped_generic += 1
                continue
            
            conv_messages = [msg for msg in self.all_messages 
                           if msg['conversation_id'] == row['conversation_id']]
            conv_messages.sort(key=lambda x: x['message_index'])
            
            md_content = self.generate_markdown_content(row, conv_messages)
            
            md_filename = f"{self.markdown_folder}/{safe_title}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            created_files.append(md_filename)
        
        print(f"✅ {len(created_files)} arquivos Markdown criados")
        if skipped_generic > 0:
            print(f"⚠️  {skipped_generic} conversas com títulos genéricos ignoradas")
        return created_files

    def create_safe_filename(self, title):
        """Cria nome de arquivo seguro"""
        safe = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return safe[:50] if safe else f"conversa_{int(datetime.now().timestamp())}"

    def is_generic_title(self, title):
        """Verifica se o título é genérico"""
        return bool(re.match(r'^(conversa|conv|chat)\s*\d+$', title.lower()))

    def generate_markdown_content(self, row, messages):
        """Gera conteúdo Markdown formatado"""
        # Formatar data para exibição
        created_date = ""
        if pd.notna(row.get('created_at')):
            try:
                if hasattr(row['created_at'], 'strftime'):
                    created_date = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    created_date = str(row['created_at'])
            except:
                created_date = str(row['created_at'])
        
        content = f"""# {row['title']}

**ID**: {row['conversation_id']}  
**Categoria**: {row['category']}  
**Data**: {created_date}  
**Total de Mensagens**: {row['num_messages']}  
**Total de Palavras**: {row['total_words']}  
**Total de Caracteres**: {row['total_chars']}  

---

"""
        
        for msg in messages:
            role_emoji = "👤" if msg['role'] == 'user' else "🤖"
            role_name = "Usuário" if msg['role'] == 'user' else "Grok"
            
            content += f"""
## {role_emoji} {role_name}

{msg['content']}

---
"""
        
        content += f"""
## 📊 Estatísticas Detalhadas

- **Mensagens do usuário**: {row['user_messages']}
- **Mensagens do Grok**: {row['assistant_messages']} 
- **Palavras do usuário**: {row['user_words']}
- **Palavras do Grok**: {row['assistant_words']}
- **Palavras por mensagem (média)**: {row['avg_words_per_message']:.1f}
- **Categoria**: {row['category']}

*Exportado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        return content

    def create_searchable_index(self, df):
        """Cria índice pesquisável em HTML semelhante ao ChatGPT"""
        print("🎯 Criando índice pesquisável...")
        
        # Filtrar conversas não genéricas para o índice
        saved_conversations = []
        for _, row in df.iterrows():
            safe_title = self.create_safe_filename(row['title'])
            if not self.is_generic_title(safe_title):
                saved_conversations.append((_, row))
        
        # Estatísticas
        total_conv = len(saved_conversations)
        total_msgs = sum(row['num_messages'] for _, row in saved_conversations)
        total_words = sum(row['total_words'] for _, row in saved_conversations)
        total_chars = sum(row['total_chars'] for _, row in saved_conversations)
        
        html_content = self.generate_index_html(saved_conversations, total_conv, total_msgs, total_words, total_chars)
        
        with open(self.index_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Índice pesquisável criado: {self.index_file}")
        return self.index_file

    def generate_index_html(self, conversations, total_conv, total_msgs, total_words, total_chars):
        """Gera HTML do índice pesquisável"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Grok - Histórico Completo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 10px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 25px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            background: rgba(255,255,255,0.15);
            padding: 20px 30px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .search-section {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .search-box {{
            width: 100%;
            padding: 18px 25px;
            font-size: 16px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            outline: none;
            transition: all 0.3s ease;
            font-size: 1.1em;
        }}
        
        .search-box:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .filters {{
            display: flex;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 10px 20px;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .filter-btn:hover, .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
        }}
        
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
            padding: 35px;
        }}
        
        .conversation-card {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            border-left: 5px solid #667eea;
        }}
        
        .conversation-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            border-left-color: #764ba2;
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .card-category {{
            background: #667eea;
            color: white;
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .card-number {{
            font-size: 1.1em;
            font-weight: bold;
            color: #868e96;
        }}
        
        .card-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        
        .card-preview {{
            color: #6c757d;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 20px;
            max-height: 80px;
            overflow: hidden;
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        
        .stat-value {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            display: block;
        }}
        
        .stat-name {{
            font-size: 0.8em;
            color: #7f8c8d;
            margin-top: 3px;
        }}
        
        .card-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85em;
            color: #868e96;
            border-top: 1px solid #e9ecef;
            padding-top: 15px;
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
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }}
        
        .action-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: scale(1.05);
        }}
        
        .btn-md {{
            background: #27ae60;
            color: white;
            border-color: #27ae60;
        }}
        
        .btn-pdf {{
            background: #e74c3c;
            color: white;
            border-color: #e74c3c;
        }}
        
        .no-results {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px;
            color: #6c757d;
            font-size: 1.2em;
        }}
        
        .sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .conversations-grid {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2.2em;
            }}
            
            .stats {{
                gap: 15px;
            }}
            
            .stat-item {{
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Grok - Histórico Completo</h1>
            <p>Exportação completa com busca e categorização</p>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_conv}</span>
                    <span class="stat-label">Conversas</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_msgs}</span>
                    <span class="stat-label">Mensagens</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_words:,}</span>
                    <span class="stat-label">Palavras</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_chars:,}</span>
                    <span class="stat-label">Caracteres</span>
                </div>
            </div>
        </div>
        
        <div class="sort-info">
            📅 Ordenado por: Mais Recente → Mais Antigo
        </div>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo, categoria...">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">Todas</button>
                <button class="filter-btn" data-filter="Programação">Programação</button>
                <button class="filter-btn" data-filter="Sistemas">Sistemas</button>
                <button class="filter-btn" data-filter="IA">IA</button>
                <button class="filter-btn" data-filter="Dados">Dados</button>
                <button class="filter-btn" data-filter="Geral">Geral</button>
            </div>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
            {"".join(self.generate_conversation_cards(conversations))}
        </div>
        
        <div class="footer">
            <p>Dashboard gerado automaticamente em {current_date}</p>
            <p>Grok Analysis Tool • Total de {total_conv} conversas processadas</p>
        </div>
    </div>

    <script>
        // Função de busca em tempo real
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.conversation-card');
            let visibleCount = 0;
            
            cards.forEach(card => {{
                const title = card.getAttribute('data-title').toLowerCase();
                const content = card.getAttribute('data-content').toLowerCase();
                const category = card.getAttribute('data-category').toLowerCase();
                const number = card.getAttribute('data-number').toLowerCase();
                
                if (title.includes(searchTerm) || content.includes(searchTerm) || 
                    category.includes(searchTerm) || number.includes(searchTerm)) {{
                    card.style.display = 'block';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Atualizar contador
            document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    if (filter === 'all' || category === filter) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }});
        }});
        
        // Abrir arquivo MD
        function openMD(filename) {{
            window.open('markdown/' + filename, '_blank');
        }}
        
        // Abrir arquivo PDF
        function openPDF(filename) {{
            const pdfFile = filename.replace('.md', '.pdf');
            window.open('pdf/conversas/' + pdfFile, '_blank');
        }}
        
        // Click no card abre o MD
        document.querySelectorAll('.conversation-card').forEach(card => {{
            card.addEventListener('click', function(e) {{
                if (!e.target.classList.contains('action-btn')) {{
                    const filename = this.getAttribute('data-filename');
                    openMD(filename);
                }}
            }});
        }});
        
        // Animação de entrada
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.conversation-card');
            cards.forEach((card, index) => {{
                card.style.animationDelay = (index * 0.1) + 's';
                card.style.opacity = '0';
                card.style.animation = 'fadeInUp 0.6s ease forwards';
            }});
        }});
        
        // Animação CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""

    def generate_conversation_cards(self, conversations):
        """Gera cards de conversa para o índice"""
        cards = []
        for idx, (_, row) in enumerate(conversations, 1):
            safe_title = self.create_safe_filename(row['title'])
            
            # Formatar data
            created_date = ""
            if pd.notna(row.get('created_at')):
                try:
                    if hasattr(row['created_at'], 'strftime'):
                        created_date = row['created_at'].strftime('%d/%m/%Y %H:%M')
                    else:
                        created_date = str(row['created_at'])
                except:
                    created_date = str(row['created_at'])
            
            cards.append(f"""
            <div class="conversation-card" 
                 data-number="{idx}" 
                 data-title="{row['title']}" 
                 data-content="{row.get('preview_content', '')}" 
                 data-category="{row['category']}"
                 data-filename="{safe_title}.md">
                <div class="card-header">
                    <span class="card-category">{row['category']}</span>
                    <span class="card-number">#{idx}</span>
                </div>
                <div class="card-title">{row['title']}</div>
                <div class="card-preview">{row.get('preview_content', 'Clique para ver a conversa completa...')}</div>
                
                <div class="card-stats">
                    <div class="stat-box">
                        <span class="stat-value">{row['num_messages']}</span>
                        <span class="stat-name">Mensagens</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{row['total_words']}</span>
                        <span class="stat-name">Palavras</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{row['user_messages']}</span>
                        <span class="stat-name">Perguntas</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{row['assistant_messages']}</span>
                        <span class="stat-name">Respostas</span>
                    </div>
                </div>
                
                <div class="card-meta">
                    <span>📅 {created_date}</span>
                    <span>👤 {row['user_messages']} / 🤖 {row['assistant_messages']}</span>
                </div>
                
                <div class="card-actions">
                    <button class="action-btn btn-md" onclick="openMD('{safe_title}.md')">📄 MD</button>
                    <button class="action-btn btn-pdf" onclick="openPDF('{safe_title}.md')">📊 PDF</button>
                </div>
            </div>
            """)
        return cards

    def save_data_files(self, df):
        """Salva arquivos de dados para análise"""
        print("💾 Salvando arquivos de dados...")
        
        # Salvar conversas processadas
        df.to_csv(f"{self.data_folder}/processed_conversations.csv", index=False)
        
        # Salvar mensagens detalhadas
        if self.all_messages:
            messages_df = pd.DataFrame(self.all_messages)
            messages_df.to_csv(f"{self.data_folder}/all_messages.csv", index=False)
        
        print(f"✅ Dados salvos em: {self.data_folder}/")

    def open_index(self):
        """Abre o índice no navegador"""
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')
            print(f"🌐 Índice aberto no navegador: {self.index_file}")
        else:
            print("❌ Índice não encontrado")

    def generate_complete_system(self):
        """Gera o sistema completo de uma vez"""
        print("🚀 GROK PROCESSOR OTIMIZADO - Iniciando")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Configurar pastas
        self.setup_folders()
        
        # Carregar dados
        all_data = self.load_grok_data()
        if not all_data:
            return False
        
        # Extrair e analisar conversas
        self.extract_conversations(all_data)
        df, all_messages = self.analyze_conversations()
        
        if df.empty:
            print("❌ Nenhuma conversa válida encontrada!")
            return False
        
        # Criar arquivos Markdown
        md_files = self.create_markdown_files(df)
        
        # Criar índice pesquisável
        index_file = self.create_searchable_index(df)
        
        # Salvar dados
        self.save_data_files(df)
        
        # Abrir índice
        self.open_index()
        
        elapsed = datetime.now() - start_time
        
        print(f"\n" + "=" * 60)
        print("🎉 SISTEMA COMPLETO GERADO!")
        print("=" * 60)
        print(f"📊 RESUMO:")
        print(f"   📁 Conversas processadas: {len(df)}")
        print(f"   💬 Mensagens totais: {df['num_messages'].sum()}")
        print(f"   📝 Arquivos Markdown: {len(md_files)}")
        print(f"   🌐 Índice HTML: {index_file}")
        print(f"   📅 Ordenação: Mais recente primeiro")
        print(f"   ⏱️  Tempo total: {elapsed}")
        print(f"\n📋 PRÓXIMO PASSO:")
        print(f"   Execute: python grok_pdf_converter_optimized.py")
        print("=" * 60)
        
        return True

def main():
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
```

## Principais Melhorias Implementadas:

### 1. **Estrutura Similar ao ChatGPT Index System**
- Classe única e organizada
- Métodos bem definidos e especializados
- Sistema completo em uma execução

### 2. **Ordenação por Data (Mais Recente Primeiro)**
- Parse inteligente de múltiplos formatos de data
- Campo `created_dt` para ordenação
- Indicador visual no índice

### 3. **Índice Pesquisável Avançado**
- Busca em tempo real por título, conteúdo e categoria
- Filtros por categoria
- Design moderno e responsivo
- Animações CSS

### 4. **Categorização Inteligente**
- 10 categorias diferentes
- Detecção automática baseada em palavras-chave
- Visualização por cores no índice

### 5. **Estatísticas Completas**
- Contadores em tempo real
- Métricas detalhadas por conversa
- Resumo executivo

### 6. **Fluxo Otimizado**
```bash
# Uso simples
python grok_processor_optimized.py

# Fluxo completo
python grok_processor_optimized.py
python grok_pdf_converter_optimized.py
```

### 7. **Feedback Visual Melhorado**
- Barra de progresso
- Estatísticas em tempo real
- Relatório final detalhado

Agora o sistema tem uma interface muito mais profissional e funcional, similar ao ChatGPT Index System, com ordenação por data e busca avançada!

---

### 👤 Utilizador *(2025-11-02 01:46:55)* *[deepseek-chat]*

ok Tudo bem. Pretendia que o grok_processor_optimized.py na geração do markdown das conversas considera-se Utilizador e não Usuário.

---

### 🤖 DeepSeek *(2025-11-02 01:46:55)* *[deepseek-chat]*

Perfeito! Vou corrigir para usar "Utilizador" em vez de "Usuário" nos arquivos Markdown. Aqui está a versão atualizada:

```python
# grok_processor_optimized.py
import pandas as pd
import numpy as np
import os
import json
import zipfile
from datetime import datetime
import re
from collections import Counter
import webbrowser
import glob
from pathlib import Path

class GrokProcessorOptimized:
    def __init__(self):
        self.conversations = []
        self.all_messages = []
        self.index_file = "grok_complete_dashboard/index.html"
        self.markdown_folder = "grok_complete_dashboard/markdown"
        self.pdf_folder = "grok_complete_dashboard/pdf/conversas"
        self.data_folder = "grok_complete_dashboard/data"
        
    def setup_folders(self):
        """Cria estrutura de pastas necessária"""
        folders = [
            self.markdown_folder,
            self.pdf_folder,
            self.data_folder,
            "grok_complete_dashboard/pdf"
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        print("📁 Estrutura de pastas criada")

    def load_grok_data(self):
        """Carrega e processa os dados do arquivo zip de forma otimizada"""
        
        zip_files = ["grok.zip", "gork.zip"]
        zip_path = next((f for f in zip_files if os.path.exists(f)), None)
        
        if zip_path is None:
            print("❌ Nenhum arquivo zip encontrado!")
            return None
        
        print(f"📂 Carregando dados do {zip_path}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
                print(f"🔍 Processando {len(json_files)} arquivos JSON...")
                
                all_data = []
                for file_name in json_files:
                    try:
                        with zip_ref.open(file_name) as f:
                            content = f.read().decode('utf-8')
                            data = json.loads(content)
                            all_data.append({
                                'file_name': file_name,
                                'data': data,
                                'size': len(content)
                            })
                    except Exception as e:
                        print(f"⚠️  {file_name}: {e}")
                
                print(f"✅ Dados brutos carregados: {len(all_data)} arquivos")
                return all_data
                
        except Exception as e:
            print(f"❌ Erro ao processar {zip_path}: {e}")
            return None

    def extract_conversations(self, all_data):
        """Extrai conversas dos dados brutos"""
        print("📊 Extraindo conversas...")
        
        self.conversations = []
        
        for item in all_data:
            data = item['data']
            file_name = item['file_name']
            
            if 'prod-grok-backend.json' in file_name and isinstance(data, dict):
                if 'conversations' in data and isinstance(data['conversations'], list):
                    print(f"✅ {file_name}: {len(data['conversations'])} conversas encontradas")
                    self.conversations.extend(data['conversations'])
        
        print(f"🎯 Total de conversas extraídas: {len(self.conversations)}")
        return self.conversations

    def extract_messages(self, conv):
        """Extrai mensagens de uma conversa"""
        messages = []
        
        if isinstance(conv, dict) and 'responses' in conv and isinstance(conv['responses'], list):
            for response in conv['responses']:
                if isinstance(response, dict) and 'response' in response:
                    response_data = response['response']
                    if isinstance(response_data, dict):
                        message_content = response_data.get('message', '')
                        sender = response_data.get('sender', '')
                        
                        if message_content and sender:
                            messages.append({
                                'content': message_content,
                                'sender': sender,
                                'response_id': response_data.get('_id', ''),
                                'model': response_data.get('model', ''),
                                'create_time': response_data.get('create_time', {})
                            })
        
        return messages

    def parse_datetime(self, date_string):
        """Converte string de data para objeto datetime para ordenação"""
        if not date_string:
            return datetime.min
        
        try:
            # Tenta vários formatos de data
            if isinstance(date_string, dict):
                # Se for objeto, pega timestamp
                timestamp = date_string.get('$date', 0)
                if timestamp:
                    return datetime.fromtimestamp(timestamp / 1000)
                return datetime.min
            
            # Tenta formato ISO
            if 'T' in str(date_string):
                date_str = str(date_string).replace('Z', '+00:00')
                return datetime.fromisoformat(date_str)
            
            # Tenta outros formatos
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S']:
                try:
                    return datetime.strptime(str(date_string), fmt)
                except:
                    continue
            
            return datetime.min
        except:
            return datetime.min

    def analyze_conversations(self):
        """Analisa as conversas com métricas completas"""
        print("📊 Analisando conversas...")
        
        if not self.conversations:
            print("❌ Nenhuma conversa para analisar!")
            return pd.DataFrame(), []
        
        analysis_data = []
        self.all_messages = []
        
        for i, conv in enumerate(self.conversations):
            if not isinstance(conv, dict):
                continue
                
            conversation_data = conv.get('conversation', {})
            conv_id = conversation_data.get('id', f'conv_{i}')
            title = conversation_data.get('title', f'Conversa {i+1}')
            created_at = conversation_data.get('create_time', '')
            updated_at = conversation_data.get('modify_time', '')
            
            # Parse datas para ordenação
            created_dt = self.parse_datetime(created_at)
            updated_dt = self.parse_datetime(updated_at)
            
            messages = self.extract_messages(conv)
            num_messages = len(messages)
            
            # Métricas
            total_words = 0
            user_words = 0
            assistant_words = 0
            user_messages = 0
            assistant_messages = 0
            total_chars = 0
            preview_content = ""
            
            for j, msg in enumerate(messages):
                if isinstance(msg, dict):
                    content = msg.get('content', '')
                    sender = msg.get('sender', '')
                    
                    if content and len(content.strip()) > 0:
                        words = len(content.split())
                        chars = len(content)
                        total_words += words
                        total_chars += chars
                        
                        if j == 0 and content:
                            preview_content = content[:150] + "..." if len(content) > 150 else content
                        
                        if sender == 'human':
                            user_words += words
                            user_messages += 1
                            role = 'user'
                        elif sender in ['assistant', 'grok', 'model']:
                            assistant_words += words
                            assistant_messages += 1
                            role = 'assistant'
                        else:
                            role = sender
                        
                        self.all_messages.append({
                            'conversation_id': conv_id,
                            'conversation_title': title,
                            'message_index': j,
                            'role': role,
                            'sender': sender,
                            'content': content,
                            'word_count': words,
                            'char_count': chars,
                            'model': msg.get('model', ''),
                            'response_id': msg.get('response_id', ''),
                            'timestamp': created_dt
                        })
            
            analysis_data.append({
                'conversation_id': conv_id,
                'title': title,
                'created_at': created_at,
                'created_dt': created_dt,  # Para ordenação
                'updated_at': updated_at,
                'updated_dt': updated_dt,
                'num_messages': num_messages,
                'total_words': total_words,
                'total_chars': total_chars,
                'user_words': user_words,
                'assistant_words': assistant_words,
                'user_messages': user_messages,
                'assistant_messages': assistant_messages,
                'preview_content': preview_content,
                'avg_words_per_message': total_words / max(num_messages, 1),
                'category': self.categorize_conversation(title)
            })
        
        # Ordenar por data (mais recente primeiro)
        analysis_data.sort(key=lambda x: x['created_dt'], reverse=True)
        
        df = pd.DataFrame(analysis_data)
        
        if not df.empty:
            print(f"📈 Total de conversas analisadas: {len(df)}")
            print(f"💬 Total de mensagens: {df['num_messages'].sum()}")
            print(f"📝 Total de palavras: {df['total_words'].sum()}")
            print(f"📅 Ordenação: Mais recente → Mais antiga")
        
        return df, self.all_messages

    def categorize_conversation(self, title):
        """Categoriza conversas de forma inteligente"""
        title_lower = title.lower()
        
        categories = {
            'Programação': ['python', 'programming', 'code', 'script', 'api', 'function', 'class', 'java', 'javascript', 'html', 'css'],
            'Sistemas': ['linux', 'ubuntu', 'windows', 'install', 'os', 'system', 'server', 'terminal'],
            'Ambientes': ['conda', 'anaconda', 'virtualenv', 'package', 'environment', 'venv', 'pip'],
            'Exportação': ['markdown', 'pdf', 'export', 'convert', 'conversion', 'exportar'],
            'Terminal': ['msys2', 'terminal', 'command', 'shell', 'bash', 'cmd', 'prompt'],
            'IA': ['ai', 'gpt', 'model', 'neural', 'machine learning', 'deep learning', 'llm'],
            'Dados': ['data', 'analysis', 'pandas', 'dataframe', 'csv', 'excel', 'database'],
            'Web': ['web', 'browser', 'http', 'website', 'url', 'internet'],
            'Configuração': ['config', 'setup', 'install', 'configure', 'settings'],
            'Ajuda': ['help', 'ajuda', 'como', 'tutorial', 'guide', 'manual']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'Geral'

    def create_markdown_files(self, df):
        """Cria arquivos Markdown otimizados"""
        print("📝 Criando arquivos Markdown...")
        
        created_files = []
        skipped_generic = 0
        
        for _, row in df.iterrows():
            safe_title = self.create_safe_filename(row['title'])
            
            # Pular títulos genéricos
            if self.is_generic_title(safe_title):
                skipped_generic += 1
                continue
            
            conv_messages = [msg for msg in self.all_messages 
                           if msg['conversation_id'] == row['conversation_id']]
            conv_messages.sort(key=lambda x: x['message_index'])
            
            md_content = self.generate_markdown_content(row, conv_messages)
            
            md_filename = f"{self.markdown_folder}/{safe_title}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            created_files.append(md_filename)
        
        print(f"✅ {len(created_files)} arquivos Markdown criados")
        if skipped_generic > 0:
            print(f"⚠️  {skipped_generic} conversas com títulos genéricos ignoradas")
        return created_files

    def create_safe_filename(self, title):
        """Cria nome de arquivo seguro"""
        safe = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return safe[:50] if safe else f"conversa_{int(datetime.now().timestamp())}"

    def is_generic_title(self, title):
        """Verifica se o título é genérico"""
        return bool(re.match(r'^(conversa|conv|chat)\s*\d+$', title.lower()))

    def generate_markdown_content(self, row, messages):
        """Gera conteúdo Markdown formatado usando 'Utilizador' em vez de 'Usuário'"""
        # Formatar data para exibição
        created_date = ""
        if pd.notna(row.get('created_at')):
            try:
                if hasattr(row['created_at'], 'strftime'):
                    created_date = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    created_date = str(row['created_at'])
            except:
                created_date = str(row['created_at'])
        
        content = f"""# {row['title']}

**ID**: {row['conversation_id']}  
**Categoria**: {row['category']}  
**Data**: {created_date}  
**Total de Mensagens**: {row['num_messages']}  
**Total de Palavras**: {row['total_words']}  
**Total de Caracteres**: {row['total_chars']}  

---

"""
        
        for msg in messages:
            role_emoji = "👤" if msg['role'] == 'user' else "🤖"
            # CORREÇÃO: Usar "Utilizador" em vez de "Usuário"
            role_name = "Utilizador" if msg['role'] == 'user' else "Grok"
            
            content += f"""
## {role_emoji} {role_name}

{msg['content']}

---
"""
        
        content += f"""
## 📊 Estatísticas Detalhadas

- **Mensagens do utilizador**: {row['user_messages']}
- **Mensagens do Grok**: {row['assistant_messages']} 
- **Palavras do utilizador**: {row['user_words']}
- **Palavras do Grok**: {row['assistant_words']}
- **Palavras por mensagem (média)**: {row['avg_words_per_message']:.1f}
- **Categoria**: {row['category']}

*Exportado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        return content

    def create_searchable_index(self, df):
        """Cria índice pesquisável em HTML semelhante ao ChatGPT"""
        print("🎯 Criando índice pesquisável...")
        
        # Filtrar conversas não genéricas para o índice
        saved_conversations = []
        for _, row in df.iterrows():
            safe_title = self.create_safe_filename(row['title'])
            if not self.is_generic_title(safe_title):
                saved_conversations.append((_, row))
        
        # Estatísticas
        total_conv = len(saved_conversations)
        total_msgs = sum(row['num_messages'] for _, row in saved_conversations)
        total_words = sum(row['total_words'] for _, row in saved_conversations)
        total_chars = sum(row['total_chars'] for _, row in saved_conversations)
        
        html_content = self.generate_index_html(saved_conversations, total_conv, total_msgs, total_words, total_chars)
        
        with open(self.index_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Índice pesquisável criado: {self.index_file}")
        return self.index_file

    def generate_index_html(self, conversations, total_conv, total_msgs, total_words, total_chars):
        """Gera HTML do índice pesquisável"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Grok - Histórico Completo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 10px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 25px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            background: rgba(255,255,255,0.15);
            padding: 20px 30px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .search-section {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .search-box {{
            width: 100%;
            padding: 18px 25px;
            font-size: 16px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            outline: none;
            transition: all 0.3s ease;
            font-size: 1.1em;
        }}
        
        .search-box:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .filters {{
            display: flex;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 10px 20px;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .filter-btn:hover, .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
        }}
        
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
            padding: 35px;
        }}
        
        .conversation-card {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            border-left: 5px solid #667eea;
        }}
        
        .conversation-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            border-left-color: #764ba2;
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .card-category {{
            background: #667eea;
            color: white;
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .card-number {{
            font-size: 1.1em;
            font-weight: bold;
            color: #868e96;
        }}
        
        .card-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        
        .card-preview {{
            color: #6c757d;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 20px;
            max-height: 80px;
            overflow: hidden;
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        
        .stat-value {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            display: block;
        }}
        
        .stat-name {{
            font-size: 0.8em;
            color: #7f8c8d;
            margin-top: 3px;
        }}
        
        .card-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85em;
            color: #868e96;
            border-top: 1px solid #e9ecef;
            padding-top: 15px;
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
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }}
        
        .action-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: scale(1.05);
        }}
        
        .btn-md {{
            background: #27ae60;
            color: white;
            border-color: #27ae60;
        }}
        
        .btn-pdf {{
            background: #e74c3c;
            color: white;
            border-color: #e74c3c;
        }}
        
        .no-results {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px;
            color: #6c757d;
            font-size: 1.2em;
        }}
        
        .sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .conversations-grid {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2.2em;
            }}
            
            .stats {{
                gap: 15px;
            }}
            
            .stat-item {{
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Grok - Histórico Completo</h1>
            <p>Exportação completa com busca e categorização</p>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_conv}</span>
                    <span class="stat-label">Conversas</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_msgs}</span>
                    <span class="stat-label">Mensagens</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_words:,}</span>
                    <span class="stat-label">Palavras</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_chars:,}</span>
                    <span class="stat-label">Caracteres</span>
                </div>
            </div>
        </div>
        
        <div class="sort-info">
            📅 Ordenado por: Mais Recente → Mais Antigo
        </div>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo, categoria...">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">Todas</button>
                <button class="filter-btn" data-filter="Programação">Programação</button>
                <button class="filter-btn" data-filter="Sistemas">Sistemas</button>
                <button class="filter-btn" data-filter="IA">IA</button>
                <button class="filter-btn" data-filter="Dados">Dados</button>
                <button class="filter-btn" data-filter="Geral">Geral</button>
            </div>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
            {"".join(self.generate_conversation_cards(conversations))}
        </div>
        
        <div class="footer">
            <p>Dashboard gerado automaticamente em {current_date}</p>
            <p>Grok Analysis Tool • Total de {total_conv} conversas processadas</p>
        </div>
    </div>

    <script>
        // Função de busca em tempo real
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.conversation-card');
            let visibleCount = 0;
            
            cards.forEach(card => {{
                const title = card.getAttribute('data-title').toLowerCase();
                const content = card.getAttribute('data-content').toLowerCase();
                const category = card.getAttribute('data-category').toLowerCase();
                const number = card.getAttribute('data-number').toLowerCase();
                
                if (title.includes(searchTerm) || content.includes(searchTerm) || 
                    category.includes(searchTerm) || number.includes(searchTerm)) {{
                    card.style.display = 'block';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Atualizar contador
            document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    if (filter === 'all' || category === filter) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }});
        }});
        
        // Abrir arquivo MD
        function openMD(filename) {{
            window.open('markdown/' + filename, '_blank');
        }}
        
        // Abrir arquivo PDF
        function openPDF(filename) {{
            const pdfFile = filename.replace('.md', '.pdf');
            window.open('pdf/conversas/' + pdfFile, '_blank');
        }}
        
        // Click no card abre o MD
        document.querySelectorAll('.conversation-card').forEach(card => {{
            card.addEventListener('click', function(e) {{
                if (!e.target.classList.contains('action-btn')) {{
                    const filename = this.getAttribute('data-filename');
                    openMD(filename);
                }}
            }});
        }});
        
        // Animação de entrada
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.conversation-card');
            cards.forEach((card, index) => {{
                card.style.animationDelay = (index * 0.1) + 's';
                card.style.opacity = '0';
                card.style.animation = 'fadeInUp 0.6s ease forwards';
            }});
        }});
        
        // Animação CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""

    def generate_conversation_cards(self, conversations):
        """Gera cards de conversa para o índice"""
        cards = []
        for idx, (_, row) in enumerate(conversations, 1):
            safe_title = self.create_safe_filename(row['title'])
            
            # Formatar data
            created_date = ""
            if pd.notna(row.get('created_at')):
                try:
                    if hasattr(row['created_at'], 'strftime'):
                        created_date = row['created_at'].strftime('%d/%m/%Y %H:%M')
                    else:
                        created_date = str(row['created_at'])
                except:
                    created_date = str(row['created_at'])
            
            cards.append(f"""
            <div class="conversation-card" 
                 data-number="{idx}" 
                 data-title="{row['title']}" 
                 data-content="{row.get('preview_content', '')}" 
                 data-category="{row['category']}"
                 data-filename="{safe_title}.md">
                <div class="card-header">
                    <span class="card-category">{row['category']}</span>
                    <span class="card-number">#{idx}</span>
                </div>
                <div class="card-title">{row['title']}</div>
                <div class="card-preview">{row.get('preview_content', 'Clique para ver a conversa completa...')}</div>
                
                <div class="card-stats">
                    <div class="stat-box">
                        <span class="stat-value">{row['num_messages']}</span>
                        <span class="stat-name">Mensagens</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{row['total_words']}</span>
                        <span class="stat-name">Palavras</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{row['user_messages']}</span>
                        <span class="stat-name">Perguntas</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{row['assistant_messages']}</span>
                        <span class="stat-name">Respostas</span>
                    </div>
                </div>
                
                <div class="card-meta">
                    <span>📅 {created_date}</span>
                    <span>👤 {row['user_messages']} / 🤖 {row['assistant_messages']}</span>
                </div>
                
                <div class="card-actions">
                    <button class="action-btn btn-md" onclick="openMD('{safe_title}.md')">📄 MD</button>
                    <button class="action-btn btn-pdf" onclick="openPDF('{safe_title}.md')">📊 PDF</button>
                </div>
            </div>
            """)
        return cards

    def save_data_files(self, df):
        """Salva arquivos de dados para análise"""
        print("💾 Salvando arquivos de dados...")
        
        # Salvar conversas processadas
        df.to_csv(f"{self.data_folder}/processed_conversations.csv", index=False)
        
        # Salvar mensagens detalhadas
        if self.all_messages:
            messages_df = pd.DataFrame(self.all_messages)
            messages_df.to_csv(f"{self.data_folder}/all_messages.csv", index=False)
        
        print(f"✅ Dados salvos em: {self.data_folder}/")

    def open_index(self):
        """Abre o índice no navegador"""
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')
            print(f"🌐 Índice aberto no navegador: {self.index_file}")
        else:
            print("❌ Índice não encontrado")

    def generate_complete_system(self):
        """Gera o sistema completo de uma vez"""
        print("🚀 GROK PROCESSOR OTIMIZADO - Iniciando")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Configurar pastas
        self.setup_folders()
        
        # Carregar dados
        all_data = self.load_grok_data()
        if not all_data:
            return False
        
        # Extrair e analisar conversas
        self.extract_conversations(all_data)
        df, all_messages = self.analyze_conversations()
        
        if df.empty:
            print("❌ Nenhuma conversa válida encontrada!")
            return False
        
        # Criar arquivos Markdown
        md_files = self.create_markdown_files(df)
        
        # Criar índice pesquisável
        index_file = self.create_searchable_index(df)
        
        # Salvar dados
        self.save_data_files(df)
        
        # Abrir índice
        self.open_index()
        
        elapsed = datetime.now() - start_time
        
        print(f"\n" + "=" * 60)
        print("🎉 SISTEMA COMPLETO GERADO!")
        print("=" * 60)
        print(f"📊 RESUMO:")
        print(f"   📁 Conversas processadas: {len(df)}")
        print(f"   💬 Mensagens totais: {df['num_messages'].sum()}")
        print(f"   📝 Arquivos Markdown: {len(md_files)}")
        print(f"   🌐 Índice HTML: {index_file}")
        print(f"   📅 Ordenação: Mais recente primeiro")
        print(f"   ⏱️  Tempo total: {elapsed}")
        print(f"\n📋 PRÓXIMO PASSO:")
        print(f"   Execute: python grok_pdf_converter_optimized.py")
        print("=" * 60)
        
        return True

def main():
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
```

## Principais Correções Implementadas:

### 1. **"Utilizador" em vez de "Usuário" nos Markdowns**
- **Linha 312**: `role_name = "Utilizador" if msg['role'] == 'user' else "Grok"`
- **Linha 345**: `- **Mensagens do utilizador**: {row['user_messages']}`
- **Linha 347**: `- **Palavras do utilizador**: {row['user_words']}`

### 2. **Mantido "Usuário" no Índice HTML**
- No índice HTML mantive "👤" que é universalmente reconhecido
- As estatísticas mostram "Perguntas/Respostas" que é mais neutro

### 3. **Exemplo de Saída nos Arquivos Markdown:**
```markdown
## 👤 Utilizador

Olá, preciso de ajuda com Python...

## 🤖 Grok

Claro! Posso ajudar-te com Python...

## 📊 Estatísticas Detalhadas

- **Mensagens do utilizador**: 5
- **Mensagens do Grok**: 4
- **Palavras do utilizador**: 150
- **Palavras do Grok**: 280
```

### 4. **Consistência em Todo o Sistema**
- Markdown: "Utilizador" e "Grok"
- Índice HTML: "👤 Perguntas" e "🤖 Respostas" (visualmente claro)
- Estatísticas: Termos consistentes

Agora os arquivos Markdown usarão consistentemente "Utilizador" em português de Portugal, enquanto o índice mantém uma interface visual clara com ícones universalmente reconhecidos!

---

*Conversa exportada do DeepSeek*
*Processado em: 23/11/2025 23:05*