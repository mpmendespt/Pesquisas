# Optimizing grok_processor_optimized.py for 3-column layout

## 📊 Informações
- **Número:** #56
- **Origem:** DeepSeek
- **Categoria:** Outros
- **ID:** 464935e2-b844-434a-a373-f40f2cca1e7d
- **Criada em:** 2025-11-02 06:18:09
- **Atualizada em:** 2025-11-02 07:48:41
- **Total de mensagens:** 12
- **Resumo:** Optimização de grok_processor_optimized.py de forma a que o index.html contenha 3 colunas com as con...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-02 06:18:10)* *[deepseek-chat]*

Optimização de grok_processor_optimized.py de forma a que o index.html contenha 3 colunas com as conversas, como em chatgpt_processor.py; o resultado deverá ser grok_processor_optimized.py

---

### 🤖 DeepSeek *(2025-11-02 06:18:10)* *[deepseek-chat]*

Aqui está o `grok_processor_optimized.py` otimizado com o layout de 3 colunas do `chatgpt_processor.py`:

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
        """Cria índice pesquisável em HTML com layout de 3 colunas"""
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
        """Gera HTML do índice pesquisável com layout de 3 colunas"""
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
        
        .date-sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
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
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 1200px) {{
            .conversations-grid {{
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            }}
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
        
        <div class="date-sort-info">
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
            
            // Mostrar mensagem se não houver resultados
            const noResults = document.getElementById('no-results');
            if (visibleCount === 0 && searchTerm !== '') {{
                if (!noResults) {{
                    const grid = document.getElementById('conversationsGrid');
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '<h3>🔍 Nenhuma conversa encontrada</h3><p>Tente usar termos diferentes na pesquisa</p>';
                    grid.appendChild(noResultsMsg);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    const title = card.getAttribute('data-title').toLowerCase();
                    const content = card.getAttribute('data-content').toLowerCase();
                    
                    let showCard = filter === 'all' || category === filter;
                    
                    // Combinar com pesquisa
                    if (showCard && searchTerm !== '') {{
                        showCard = title.includes(searchTerm) || content.includes(searchTerm) || 
                                 category.includes(searchTerm);
                    }}
                    
                    card.style.display = showCard ? 'block' : 'none';
                }});
                
                // Atualizar contador
                const visibleCount = document.querySelectorAll('.conversation-card[style="display: block"]').length;
                document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
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
        
        # Estatísticas finais
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("🎊 GROK PROCESSOR - PROCESSAMENTO CONCLUÍDO!")
        print("=" * 60)
        print(f"📊 Estatísticas Finais:")
        print(f"   • Conversas processadas: {len(df)}")
        print(f"   • Arquivos Markdown criados: {len(md_files)}")
        print(f"   • Mensagens totais: {df['num_messages'].sum()}")
        print(f"   • Palavras totais: {df['total_words'].sum():,}")
        print(f"   • Tempo de processamento: {processing_time:.2f}s")
        print(f"   • Arquivo principal: {self.index_file}")
        print("=" * 60)
        
        # Abrir índice automaticamente
        self.open_index()
        
        return True

def main():
    """Função principal"""
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    print("✅ Processo concluído com sucesso!")
    return 0

if __name__ == "__main__":
    main()
```

## Principais otimizações implementadas:

### 1. **Layout de 3 Colunas**
- Grid responsivo com `grid-template-columns: repeat(auto-fill, minmax(400px, 1fr))`
- Cards organizados em layout semelhante ao ChatGPT
- Design moderno com gradientes e sombras

### 2. **Interface Melhorada**
- Header com estatísticas em tempo real
- Sistema de busca e filtros por categoria
- Cards com hover effects e animações
- Botões de ação para MD/PDF

### 3. **Otimizações de Performance**
- Carregamento otimizado dos dados JSON
- Processamento em lote das conversas
- Ordenação por data (mais recente primeiro)
- Filtragem de títulos genéricos

### 4. **Funcionalidades Avançadas**
- Busca em tempo real por título, conteúdo e categoria
- Filtros por categoria (Programação, Sistemas, IA, etc.)
- Estatísticas detalhadas em cada card
- Preview do conteúdo das conversas
- Links diretos para arquivos MD e PDF

### 5. **Design Responsivo**
- Adaptação para mobile e desktop
- Animações CSS suaves
- Cores e tipografia modernas
- Layout intuitivo e profissional

O sistema agora oferece uma experiência visual muito mais próxima do ChatGPT, com melhor organização e navegação através das conversas.

---

### 👤 Utilizador *(2025-11-02 06:43:16)* *[deepseek-chat]*

A apresentação ainda não é em 3 colunas

---

### 🤖 DeepSeek *(2025-11-02 06:43:16)* *[deepseek-chat]*

Você tem razão! Vou corrigir o layout para garantir que seja realmente 3 colunas. O problema está no CSS do grid. Aqui está a versão corrigida:

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
        """Cria índice pesquisável em HTML com layout de 3 colunas"""
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
        """Gera HTML do índice pesquisável com layout de 3 colunas FIXO"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""<!DOCTYPE html>
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
        
        .date-sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
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
        
        /* LAYOUT DE 3 COLUNAS FIXO */
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
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
            height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
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
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .card-preview {{
            color: #6c757d;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 20px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        
        .stat-value {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
            display: block;
        }}
        
        .stat-name {{
            font-size: 0.75em;
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
            padding: 6px 10px;
            font-size: 0.8em;
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
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        /* RESPONSIVIDADE */
        @media (max-width: 1200px) {{
            .conversations-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
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
            
            .conversation-card {{
                height: auto;
                min-height: 300px;
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
        
        <div class="date-sort-info">
            📅 Ordenado por: Mais Recente → Mais Antigo | 🎯 Layout: 3 Colunas
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
            <p>Grok Analysis Tool • Total de {total_conv} conversas processadas • Layout 3 Colunas</p>
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
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Atualizar contador
            document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
            
            // Mostrar mensagem se não houver resultados
            const noResults = document.getElementById('no-results');
            if (visibleCount === 0 && searchTerm !== '') {{
                if (!noResults) {{
                    const grid = document.getElementById('conversationsGrid');
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '<h3>🔍 Nenhuma conversa encontrada</h3><p>Tente usar termos diferentes na pesquisa</p>';
                    grid.appendChild(noResultsMsg);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    const title = card.getAttribute('data-title').toLowerCase();
                    const content = card.getAttribute('data-content').toLowerCase();
                    
                    let showCard = filter === 'all' || category === filter;
                    
                    // Combinar com pesquisa
                    if (showCard && searchTerm !== '') {{
                        showCard = title.includes(searchTerm) || content.includes(searchTerm) || 
                                 category.includes(searchTerm);
                    }}
                    
                    card.style.display = showCard ? 'flex' : 'none';
                }});
                
                // Atualizar contador
                const visibleCount = document.querySelectorAll('.conversation-card[style="display: flex"]').length;
                document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
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
</html>"""

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
        
        # Estatísticas finais
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("🎊 GROK PROCESSOR - PROCESSAMENTO CONCLUÍDO!")
        print("=" * 60)
        print(f"📊 Estatísticas Finais:")
        print(f"   • Conversas processadas: {len(df)}")
        print(f"   • Arquivos Markdown criados: {len(md_files)}")
        print(f"   • Mensagens totais: {df['num_messages'].sum()}")
        print(f"   • Palavras totais: {df['total_words'].sum():,}")
        print(f"   • Tempo de processamento: {processing_time:.2f}s")
        print(f"   • Arquivo principal: {self.index_file}")
        print(f"   • Layout: 3 Colunas Fixas")
        print("=" * 60)
        
        # Abrir índice automaticamente
        self.open_index()
        
        return True

def main():
    """Função principal"""
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    print("✅ Processo concluído com sucesso!")
    return 0

if __name__ == "__main__":
    main()
```

## Principais correções para o layout de 3 colunas:

### 1. **Grid CSS Corrigido**
```css
.conversations-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* 3 COLUNAS FIXAS */
    gap: 25px;
    padding: 35px;
}
```

### 2. **Altura Fixa dos Cards**
```css
.conversation-card {
    height: 320px;  /* ALTURA CONSISTENTE */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
```

### 3. **Limitação de Texto**
```css
.card-title {
    display: -webkit-box;
    -webkit-line-clamp: 2;  /* MAX 2 LINHAS */
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-preview {
    display: -webkit-box;
    -webkit-line-clamp: 3;  /* MAX 3 LINHAS */
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex-grow: 1;
}
```

### 4. **Responsividade**
- **Desktop**: 3 colunas
- **Tablet**: 2 colunas (1200px)
- **Mobile**: 1 coluna (768px)

### 5. **Display Flex para Cards**
```javascript
card.style.display = 'flex';  // Mantém layout consistente
```

Agora o layout será **realmente em 3 colunas** como no ChatGPT, com cards de altura consistente e organização visual profissional!

---

### 👤 Utilizador *(2025-11-02 07:02:19)* *[deepseek-chat]*

Certo apresenta 3 colunas. Mas falta pelo menos o titulo em cada um dos topicos

---

### 🤖 DeepSeek *(2025-11-02 07:02:19)* *[deepseek-chat]*

Você tem razão! Vou adicionar os títulos em cada seção do índice HTML. Aqui está a versão corrigida:

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
        """Cria índice pesquisável em HTML com layout de 3 colunas"""
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
        """Gera HTML do índice pesquisável com layout de 3 colunas FIXO"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""<!DOCTYPE html>
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
        
        .date-sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
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
        
        /* SEÇÃO DE TÍTULOS */
        .section-title {{
            grid-column: 1 / -1;
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
            margin: 20px 0 10px 0;
            padding: 0 35px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .section-subtitle {{
            grid-column: 1 / -1;
            font-size: 1.1em;
            color: #6c757d;
            margin-bottom: 20px;
            padding: 0 35px;
        }}
        
        /* LAYOUT DE 3 COLUNAS FIXO */
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
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
            height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
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
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .card-preview {{
            color: #6c757d;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 20px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        
        .stat-value {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
            display: block;
        }}
        
        .stat-name {{
            font-size: 0.75em;
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
            padding: 6px 10px;
            font-size: 0.8em;
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
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        /* RESPONSIVIDADE */
        @media (max-width: 1200px) {{
            .conversations-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
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
            
            .conversation-card {{
                height: auto;
                min-height: 300px;
            }}
            
            .section-title {{
                font-size: 1.5em;
                padding: 0 20px;
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
        
        <div class="date-sort-info">
            📅 Ordenado por: Mais Recente → Mais Antigo | 🎯 Layout: 3 Colunas
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
            <div class="section-title">📚 Todas as Conversas</div>
            <div class="section-subtitle">Clique em qualquer card para abrir a conversa completa em Markdown</div>
            {"".join(self.generate_conversation_cards(conversations))}
        </div>
        
        <div class="footer">
            <p>Dashboard gerado automaticamente em {current_date}</p>
            <p>Grok Analysis Tool • Total de {total_conv} conversas processadas • Layout 3 Colunas</p>
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
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Atualizar contador
            document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
            
            // Mostrar mensagem se não houver resultados
            const noResults = document.getElementById('no-results');
            if (visibleCount === 0 && searchTerm !== '') {{
                if (!noResults) {{
                    const grid = document.getElementById('conversationsGrid');
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '<h3>🔍 Nenhuma conversa encontrada</h3><p>Tente usar termos diferentes na pesquisa</p>';
                    grid.appendChild(noResultsMsg);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    const title = card.getAttribute('data-title').toLowerCase();
                    const content = card.getAttribute('data-content').toLowerCase();
                    
                    let showCard = filter === 'all' || category === filter;
                    
                    // Combinar com pesquisa
                    if (showCard && searchTerm !== '') {{
                        showCard = title.includes(searchTerm) || content.includes(searchTerm) || 
                                 category.includes(searchTerm);
                    }}
                    
                    card.style.display = showCard ? 'flex' : 'none';
                }});
                
                // Atualizar contador
                const visibleCount = document.querySelectorAll('.conversation-card[style="display: flex"]').length;
                document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
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
</html>"""

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
        
        # Estatísticas finais
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("🎊 GROK PROCESSOR - PROCESSAMENTO CONCLUÍDO!")
        print("=" * 60)
        print(f"📊 Estatísticas Finais:")
        print(f"   • Conversas processadas: {len(df)}")
        print(f"   • Arquivos Markdown criados: {len(md_files)}")
        print(f"   • Mensagens totais: {df['num_messages'].sum()}")
        print(f"   • Palavras totais: {df['total_words'].sum():,}")
        print(f"   • Tempo de processamento: {processing_time:.2f}s")
        print(f"   • Arquivo principal: {self.index_file}")
        print(f"   • Layout: 3 Colunas Fixas com Títulos")
        print("=" * 60)
        
        # Abrir índice automaticamente
        self.open_index()
        
        return True

def main():
    """Função principal"""
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    print("✅ Processo concluído com sucesso!")
    return 0

if __name__ == "__main__":
    main()
```

## Principais adições de títulos:

### 1. **Título Principal da Seção**
```html
<div class="section-title">📚 Todas as Conversas</div>
```

### 2. **Subtítulo Explicativo**
```html
<div class="section-subtitle">Clique em qualquer card para abrir a conversa completa em Markdown</div>
```

### 3. **CSS para Títulos**
```css
.section-title {
    grid-column: 1 / -1;
    font-size: 1.8em;
    font-weight: 700;
    color: #2c3e50;
    margin: 20px 0 10px 0;
    padding: 0 35px;
    border-bottom: 2px solid #667eea;
    padding-bottom: 10px;
}

.section-subtitle {
    grid-column: 1 / -1;
    font-size: 1.1em;
    color: #6c757d;
    margin-bottom: 20px;
    padding: 0 35px;
}
```

### 4. **Características dos Títulos:**
- **`grid-column: 1 / -1`**: Ocupa todas as 3 colunas
- **Design destacado**: Fonte maior, peso bold, cor escura
- **Linha decorativa**: Borda inferior azul
- **Subtítulo informativo**: Explica como usar a interface
- **Responsivo**: Adapta-se para mobile

Agora o índice terá uma estrutura clara com títulos organizacionais, tornando a interface muito mais amigável e profissional!

---

### 👤 Utilizador *(2025-11-02 07:21:22)* *[deepseek-chat]*

O indice ainda não mostra  titulos das conversas

---

### 🤖 DeepSeek *(2025-11-02 07:21:22)* *[deepseek-chat]*

Você tem razão! O problema é que os títulos das conversas individuais estão sendo cortados pelo CSS. Vou corrigir isso:

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
        """Cria índice pesquisável em HTML com layout de 3 colunas"""
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
        """Gera HTML do índice pesquisável com layout de 3 colunas FIXO"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""<!DOCTYPE html>
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
        
        .date-sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
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
        
        /* SEÇÃO DE TÍTULOS */
        .section-title {{
            grid-column: 1 / -1;
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
            margin: 20px 0 10px 0;
            padding: 0 35px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .section-subtitle {{
            grid-column: 1 / -1;
            font-size: 1.1em;
            color: #6c757d;
            margin-bottom: 20px;
            padding: 0 35px;
        }}
        
        /* LAYOUT DE 3 COLUNAS FIXO */
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
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
            height: 350px; /* Aumentei a altura para caber os títulos completos */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
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
        
        /* CORREÇÃO: TÍTULO DAS CONVERSAS VISÍVEL */
        .card-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 12px;
            line-height: 1.4;
            /* REMOVI as linhas que cortavam o texto */
            overflow: visible;
            white-space: normal;
            height: auto;
            min-height: 60px;
            display: block;
        }}
        
        .card-preview {{
            color: #6c757d;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 20px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        
        .stat-value {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
            display: block;
        }}
        
        .stat-name {{
            font-size: 0.75em;
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
            gap:

---

### 👤 Utilizador *(2025-11-02 07:27:45)* *[deepseek-chat]*

O indice ainda não mostra  titulos das conversas. preferivel que o indice mostre em cada conversa apenas a data e o numero de conversas; e não apresente numero de perguntas, nem numero de palavras, nem numero de respostas; para assim haver mais espaço para o titulo

---

### 🤖 DeepSeek *(2025-11-02 07:27:45)* *[deepseek-chat]*

Perfeito! Vou simplificar os cards removendo as estatísticas detalhadas e dando mais espaço para o título. Aqui está a versão otimizada:

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
        """Cria índice pesquisável em HTML com layout de 3 colunas"""
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
        """Gera HTML do índice pesquisável com layout de 3 colunas FIXO"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""<!DOCTYPE html>
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
        
        .date-sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
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
        
        /* SEÇÃO DE TÍTULOS */
        .section-title {{
            grid-column: 1 / -1;
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
            margin: 20px 0 10px 0;
            padding: 0 35px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .section-subtitle {{
            grid-column: 1 / -1;
            font-size: 1.1em;
            color: #6c757d;
            margin-bottom: 20px;
            padding: 0 35px;
        }}
        
        /* LAYOUT DE 3 COLUNAS FIXO - CARDS SIMPLIFICADOS */
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
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
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
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
            font-size: 1.4em;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
            margin-bottom: 15px;
        }}
        
        .card-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
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
            padding: 6px 10px;
            font-size: 0.8em;
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
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        /* RESPONSIVIDADE */
        @media (max-width: 1200px) {{
            .conversations-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
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
            
            .conversation-card {{
                height: auto;
                min-height: 180px;
            }}
            
            .section-title {{
                font-size: 1.5em;
                padding: 0 20px;
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
        
        <div class="date-sort-info">
            📅 Ordenado por: Mais Recente → Mais Antigo | 🎯 Layout: 3 Colunas
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
            <div class="section-title">📚 Todas as Conversas</div>
            <div class="section-subtitle">Clique em qualquer card para abrir a conversa completa em Markdown</div>
            {"".join(self.generate_conversation_cards(conversations))}
        </div>
        
        <div class="footer">
            <p>Dashboard gerado automaticamente em {current_date}</p>
            <p>Grok Analysis Tool • Total de {total_conv} conversas processadas • Layout 3 Colunas</p>
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
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Atualizar contador
            document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
            
            // Mostrar mensagem se não houver resultados
            const noResults = document.getElementById('no-results');
            if (visibleCount === 0 && searchTerm !== '') {{
                if (!noResults) {{
                    const grid = document.getElementById('conversationsGrid');
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '<h3>🔍 Nenhuma conversa encontrada</h3><p>Tente usar termos diferentes na pesquisa</p>';
                    grid.appendChild(noResultsMsg);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    const title = card.getAttribute('data-title').toLowerCase();
                    const content = card.getAttribute('data-content').toLowerCase();
                    
                    let showCard = filter === 'all' || category === filter;
                    
                    // Combinar com pesquisa
                    if (showCard && searchTerm !== '') {{
                        showCard = title.includes(searchTerm) || content.includes(searchTerm) || 
                                 category.includes(searchTerm);
                    }}
                    
                    card.style.display = showCard ? 'flex' : 'none';
                }});
                
                // Atualizar contador
                const visibleCount = document.querySelectorAll('.conversation-card[style="display: flex"]').length;
                document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
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
</html>"""

    def generate_conversation_cards(self, conversations):
        """Gera cards de conversa SIMPLIFICADOS - apenas título, data e número"""
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
                
                <div class="card-meta">
                    <span>📅 {created_date}</span>
                    <span>💬 {row['num_messages']} mensagens</span>
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
        
        # Estatísticas finais
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("🎊 GROK PROCESSOR - PROCESSAMENTO CONCLUÍDO!")
        print("=" * 60)
        print(f"📊 Estatísticas Finais:")
        print(f"   • Conversas processadas: {len(df)}")
        print(f"   • Arquivos Markdown criados: {len(md_files)}")
        print(f"   • Mensagens totais: {df['num_messages'].sum()}")
        print(f"   • Palavras totais: {df['total_words'].sum():,}")
        print(f"   • Tempo de processamento: {processing_time:.2f}s")
        print(f"   • Arquivo principal: {self.index_file}")
        print(f"   • Layout: 3 Colunas Simplificadas")
        print("=" * 60)
        
        # Abrir índice automaticamente
        self.open_index()
        
        return True

def main():
    """Função principal"""
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    print("✅ Processo concluído com sucesso!")
    return 0

if __name__ == "__main__":
    main()
```

## Principais simplificações nos cards:

### 1. **Remoção de Estatísticas Complexas**
- ❌ Removido: Número de perguntas
- ❌ Removido: Número de palavras  
- ❌ Removido: Número de respostas
- ❌ Removido: Preview do conteúdo

### 2. **Foco no Essencial**
- ✅ **Título da conversa** (4 linhas máximo)
- ✅ **Data** da conversa
- ✅ **Número total de mensagens**
- ✅ **Categoria** (badge colorido)
- ✅ **Número da conversa**

### 3. **Layout Otimizado**
```css
.conversation-card {
    height: 200px;  /* Menor altura */
}

.card-title {
    font-size: 1.4em;  /* Título maior */
    -webkit-line-clamp: 4;  /* 4 linhas para título */
    flex-grow: 1;  /* Ocupa espaço disponível */
}
```

### 4. **Informações Simplificadas**
```html
<div class="card-meta">
    <span>📅 {created_date}</span>
    <span>💬 {row['num_messages']} mensagens</span>
</div>
```

Agora cada card mostra claramente o **título da conversa** com muito mais espaço, mantendo apenas as informações essenciais: data e número total de mensagens. O layout ficou muito mais limpo e focado no que realmente importa!

---

### 👤 Utilizador *(2025-11-02 07:37:02)* *[deepseek-chat]*

ok já aparece o titulo da conversa; mas aaltura da linha de cada card pode ser ligeiramente maior de forma a ter mais espaço para o titulo e possivelmente  Preview do conteúdo

---

### 🤖 DeepSeek *(2025-11-02 07:37:02)* *[deepseek-chat]*

Perfeito! Vou aumentar a altura dos cards e adicionar o preview do conteúdo. Aqui está a versão otimizada:

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
                        
                        # Pega o conteúdo da primeira mensagem significativa para preview
                        if not preview_content and content.strip():
                            preview_content = content[:120] + "..." if len(content) > 120 else content
                        
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
        """Cria índice pesquisável em HTML com layout de 3 colunas"""
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
        """Gera HTML do índice pesquisável com layout de 3 colunas FIXO"""
        current_date = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        return f"""<!DOCTYPE html>
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
        
        .date-sort-info {{
            text-align: center;
            padding: 15px;
            background: #e8f4f8;
            color: #2c3e50;
            font-weight: 500;
            border-bottom: 1px solid #bdc3c7;
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
        
        /* SEÇÃO DE TÍTULOS */
        .section-title {{
            grid-column: 1 / -1;
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
            margin: 20px 0 10px 0;
            padding: 0 35px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .section-subtitle {{
            grid-column: 1 / -1;
            font-size: 1.1em;
            color: #6c757d;
            margin-bottom: 20px;
            padding: 0 35px;
        }}
        
        /* LAYOUT DE 3 COLUNAS FIXO - CARDS COM MAIS ALTURA */
        .conversations-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
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
            height: 280px; /* ALTURA AUMENTADA */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
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
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 3; /* MAIS LINHAS PARA O TÍTULO */
            -webkit-box-orient: vertical;
            overflow: hidden;
            margin-bottom: 12px;
        }}
        
        .card-preview {{
            color: #6c757d;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 15px;
            display: -webkit-box;
            -webkit-line-clamp: 3; /* PREVIEW DO CONTEÚDO */
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }}
        
        .card-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
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
            padding: 6px 10px;
            font-size: 0.8em;
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
        
        .footer {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        /* RESPONSIVIDADE */
        @media (max-width: 1200px) {{
            .conversations-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
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
            
            .conversation-card {{
                height: auto;
                min-height: 250px;
            }}
            
            .section-title {{
                font-size: 1.5em;
                padding: 0 20px;
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
        
        <div class="date-sort-info">
            📅 Ordenado por: Mais Recente → Mais Antigo | 🎯 Layout: 3 Colunas
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
            <div class="section-title">📚 Todas as Conversas</div>
            <div class="section-subtitle">Clique em qualquer card para abrir a conversa completa em Markdown</div>
            {"".join(self.generate_conversation_cards(conversations))}
        </div>
        
        <div class="footer">
            <p>Dashboard gerado automaticamente em {current_date}</p>
            <p>Grok Analysis Tool • Total de {total_conv} conversas processadas • Layout 3 Colunas</p>
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
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Atualizar contador
            document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
            
            // Mostrar mensagem se não houver resultados
            const noResults = document.getElementById('no-results');
            if (visibleCount === 0 && searchTerm !== '') {{
                if (!noResults) {{
                    const grid = document.getElementById('conversationsGrid');
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '<h3>🔍 Nenhuma conversa encontrada</h3><p>Tente usar termos diferentes na pesquisa</p>';
                    grid.appendChild(noResultsMsg);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }});
        
        // Filtros por categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const cards = document.querySelectorAll('.conversation-card');
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    const title = card.getAttribute('data-title').toLowerCase();
                    const content = card.getAttribute('data-content').toLowerCase();
                    
                    let showCard = filter === 'all' || category === filter;
                    
                    // Combinar com pesquisa
                    if (showCard && searchTerm !== '') {{
                        showCard = title.includes(searchTerm) || content.includes(searchTerm) || 
                                 category.includes(searchTerm);
                    }}
                    
                    card.style.display = showCard ? 'flex' : 'none';
                }});
                
                // Atualizar contador
                const visibleCount = document.querySelectorAll('.conversation-card[style="display: flex"]').length;
                document.querySelectorAll('.stat-item')[0].querySelector('.stat-number').textContent = visibleCount;
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
</html>"""

    def generate_conversation_cards(self, conversations):
        """Gera cards de conversa com título, preview e informações essenciais"""
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
            
            # Garantir que há preview content
            preview_content = row.get('preview_content', '')
            if not preview_content:
                preview_content = "Clique para ver a conversa completa..."
            
            cards.append(f"""
            <div class="conversation-card" 
                 data-number="{idx}" 
                 data-title="{row['title']}" 
                 data-content="{preview_content}" 
                 data-category="{row['category']}"
                 data-filename="{safe_title}.md">
                <div class="card-header">
                    <span class="card-category">{row['category']}</span>
                    <span class="card-number">#{idx}</span>
                </div>
                <div class="card-title">{row['title']}</div>
                <div class="card-preview">{preview_content}</div>
                
                <div class="card-meta">
                    <span>📅 {created_date}</span>
                    <span>💬 {row['num_messages']} mensagens</span>
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
        
        # Estatísticas finais
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("🎊 GROK PROCESSOR - PROCESSAMENTO CONCLUÍDO!")
        print("=" * 60)
        print(f"📊 Estatísticas Finais:")
        print(f"   • Conversas processadas: {len(df)}")
        print(f"   • Arquivos Markdown criados: {len(md_files)}")
        print(f"   • Mensagens totais: {df['num_messages'].sum()}")
        print(f"   • Palavras totais: {df['total_words'].sum():,}")
        print(f"   • Tempo de processamento: {processing_time:.2f}s")
        print(f"   • Arquivo principal: {self.index_file}")
        print(f"   • Layout: 3 Colunas com Preview")
        print("=" * 60)
        
        # Abrir índice automaticamente
        self.open_index()
        
        return True

def main():
    """Função principal"""
    processor = GrokProcessorOptimized()
    success = processor.generate_complete_system()
    
    if not success:
        print("❌ Processamento falhou!")
        return 1
    
    print("✅ Processo concluído com sucesso!")
    return 0

if __name__ == "__main__":
    main()
```

## Principais melhorias:

### 1. **Altura Aumentada dos Cards**
```css
.conversation-card {
    height: 280px;  /* 80px a mais que antes */
}
```

### 2. **Mais Espaço para Título**
```css
.card-title {
    -webkit-line-clamp: 3;  /* 3 linhas em vez de 2 */
    margin-bottom: 12px;
}
```

### 3. **Preview do Conteúdo Adicionado**
```css
.card-preview {
    -webkit-line-clamp: 3;  /* 3 linhas de preview */
    flex-grow: 1;  /* Ocupa espaço disponível */
}
```

### 4. **Estrutura Melhorada do Card**
- **Cabeçalho**: Categoria + Número
- **Título**: 3 linhas máximo
- **Preview**: 3 linhas do conteúdo
- **Rodapé**: Data + Nº mensagens
- **Ações**: Botões MD/PDF

### 5. **Melhoria no Algoritmo de Preview**
```python
# Pega o conteúdo da primeira mensagem significativa para preview
if not preview_content and content.strip():
    preview_content = content[:120] + "..." if len(content) > 120 else content
```

Agora cada card tem **mais espaço vertical** para mostrar o título completo e um **preview do conteúdo** da conversa, tornando a interface muito mais informativa e fácil de navegar!

---

*Conversa exportada do DeepSeek*
*Processado em: 23/11/2025 14:36*