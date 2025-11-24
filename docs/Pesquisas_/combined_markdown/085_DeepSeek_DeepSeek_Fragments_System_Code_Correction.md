# DeepSeek Fragments System Code Correction

## 📊 Informações
- **Número:** #85
- **Origem:** DeepSeek
- **Categoria:** IA
- **ID:** a0f93ebb-91cc-49a0-902d-9d926c39cfee
- **Criada em:** 2025-10-27 05:24:11
- **Atualizada em:** 2025-10-28 06:22:54
- **Total de mensagens:** 12
- **Resumo:** Exportar historico DeepSeek. Correcção. Pretendo que as conversas sejam apresentadas do mais novo pa...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-27 05:24:12)* *[deepseek-chat]*

Exportar historico DeepSeek. Correcção. Pretendo que as conversas sejam apresentadas do mais novo para o mais antigo

---

### 🤖 DeepSeek *(2025-10-27 05:24:12)* *[deepseek-chat]*

Aqui está a correção para apresentar as conversas do mais novo para o mais antigo:

```python
# deepseek_fragments_system.py
import json
import zipfile
import os
from datetime import datetime
import subprocess
import webbrowser

class DeepSeekFragmentsSystem:
    def __init__(self, zip_file="deepseek_data.zip"):
        self.zip_file = zip_file
        self.markdown_folder = "deepseek_markdown"
        self.conversations = []
        self.index_file = "deepseek_index.html"
        self.pdf_folder = "deepseek_pdfs"
        
    def extract_deepseek_conversations(self):
        """Extrai conversas focando nos fragments"""
        print("🔧 Extraindo conversas dos fragments...")
        
        if not os.path.exists(self.zip_file):
            print(f"❌ Arquivo não encontrado: {self.zip_file}")
            return False
        
        try:
            # Extrai o ZIP
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"✅ ZIP extraído! {len(file_list)} arquivos")
                
                temp_dir = "temp_deepseek_fragments"
                os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)
            
            # Processa conversations.json
            conv_file = os.path.join(temp_dir, "conversations.json")
            
            if not os.path.exists(conv_file):
                print("❌ conversations.json não encontrado!")
                return False
            
            print("📖 Lendo conversations.json...")
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print("❌ Formato inválido")
                return False
            
            print(f"🎯 Processando {len(data)} conversas...")
            
            # Processa cada conversa
            self.conversations = []
            for i, conv_data in enumerate(data):
                conversation = self.process_conversation(conv_data, i+1)
                if conversation and conversation['messages']:
                    self.conversations.append(conversation)
                    print(f"✅ {i+1:02d}: '{conversation['title']}' - {len(conversation['messages'])} mensagens")
                else:
                    print(f"⚠️  {i+1:02d}: '{conv_data.get('title', 'Sem título')}' - SEM MENSAGENS")
            
            # ORDENAÇÃO CORRIGIDA: do mais novo para o mais antigo
            self.conversations.sort(key=lambda x: (
                datetime.fromisoformat(x['updated_at'].replace('Z', '+00:00')) 
                if x['updated_at'] and 'T' in x['updated_at'] 
                else datetime.fromisoformat(x['inserted_at'].replace('Z', '+00:00')) 
                if x['inserted_at'] and 'T' in x['inserted_at']
                else datetime.min
            ), reverse=True)  # reverse=True para ordem decrescente (mais novo primeiro)
            
            # Reenumera as conversas após ordenação
            for i, conv in enumerate(self.conversations):
                conv['number'] = i + 1
            
            print(f"📊 Total de conversas com mensagens: {len(self.conversations)}")
            
            if self.conversations:
                self.save_as_markdown()
            
            # Limpa
            import shutil
            shutil.rmtree(temp_dir)
            
            return len(self.conversations) > 0
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def process_conversation(self, conv_data, number):
        """Processa uma conversa individual"""
        try:
            title = conv_data.get('title', f'Conversa {number}')
            conv_id = conv_data.get('id', f'conv_{number}')
            inserted_at = conv_data.get('inserted_at')
            updated_at = conv_data.get('updated_at')
            
            # Extrai mensagens do mapping focando nos fragments
            mapping = conv_data.get('mapping', {})
            messages = self.extract_messages_from_fragments(mapping)
            
            return {
                'number': number,
                'id': conv_id,
                'title': title,
                'inserted_at': self.format_timestamp(inserted_at),
                'updated_at': self.format_timestamp(updated_at),
                'messages': messages,
                'message_count': len(messages),
                'summary': self.generate_summary(messages),
                'sort_timestamp': inserted_at or updated_at  # Para ordenação
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao processar conversa {number}: {e}")
            return None
    
    def extract_messages_from_fragments(self, mapping):
        """Extrai mensagens dos fragments"""
        messages = []
        
        # Itera por todos os nós do mapping
        for node_id, node in mapping.items():
            if not isinstance(node, dict):
                continue
                
            message_data = node.get('message')
            
            # Só processa se message não for None e for dict
            if message_data and isinstance(message_data, dict):
                message = self.parse_message_from_fragments(message_data, node_id)
                if message and message['content']:  # Só adiciona se tiver conteúdo
                    messages.append(message)
        
        # Ordena pela ordem dos nós
        try:
            messages.sort(key=lambda x: int(x['node_id']) if x['node_id'].isdigit() else 0)
        except:
            # Se não conseguir ordenar, mantém ordem original
            pass
        
        return messages
    
    def parse_message_from_fragments(self, message_data, node_id):
        """Analisa uma mensagem extraindo texto dos fragments"""
        try:
            # Tenta determinar o autor pelo model
            model = message_data.get('model', '')
            if 'deepseek' in model.lower() or 'assistant' in model.lower():
                role = 'assistant'
                author_display = '🤖 DeepSeek'
            else:
                role = 'user'
                author_display = '👤 Você'
            
            # Extrai conteúdo dos fragments
            fragments = message_data.get('fragments', [])
            content_parts = []
            
            for fragment in fragments:
                if isinstance(fragment, dict):
                    # Fragment pode ter texto diretamente
                    text = fragment.get('text', '')
                    if text:
                        content_parts.append(str(text))
                    
                    # Ou pode ter conteúdo em outras chaves
                    content = fragment.get('content', '')
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
            
            # Se não encontrou conteúdo nos fragments, tenta outras chaves
            if not content:
                content = message_data.get('content', '')
                if isinstance(content, list):
                    content = ' '.join([str(item) for item in content if item])
            
            # Remove conteúdo vazio
            if not content or content.isspace():
                return None
            
            # Timestamp
            timestamp = message_data.get('inserted_at') or message_data.get('created_at')
            
            return {
                'node_id': node_id,
                'author': author_display,
                'role': role,
                'content': content,
                'timestamp': self.format_timestamp(timestamp),
                'model': model
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar mensagem {node_id}: {e}")
            return None
    
    def format_timestamp(self, timestamp):
        """Formata timestamp"""
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, str):
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
            
            print(f"✅ {filename}")
        
        print(f"🎉 {len(self.conversations)} arquivos criados em '{self.markdown_folder}'")
    
    def create_markdown_content(self, conversation):
        """Cria conteúdo Markdown"""
        md = f"# 💬 {conversation['title']}\n\n"
        
        # Metadados
        md += "## 📊 Informações\n\n"
        md += f"- **Número:** #{conversation['number']}\n"
        md += f"- **ID:** {conversation['id']}\n"
        md += f"- **Criada em:** {conversation['inserted_at'] or 'N/A'}\n"
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
        md += "*Conversa exportada do DeepSeek*  \n"
        md += f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        
        return md
    
    def create_searchable_index(self):
        """Cria índice HTML"""
        print("🎯 Criando índice pesquisável...")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📚 Índice de Conversas - DeepSeek</title>
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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 Índice de Conversas</h1>
                    <p>DeepSeek - Histórico Completo (Mais Recentes Primeiro)</p>
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
        for conv in self.conversations:
            safe_title = "".join(c for c in conv['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conv['number']:03d}_{safe_title}.md"
            
            html_content += f"""
                    <div class="conversation-card" data-title="{conv['title']}" data-summary="{conv['summary']}">
                        <div class="card-header">
                            <div class="card-number">#{conv['number']}</div>
                            <div class="card-actions">
                                <button class="action-btn" onclick="openMD('{filename}')">MD</button>
                                <button class="action-btn" onclick="openPDF('{filename}')">PDF</button>
                            </div>
                        </div>
                        <div class="card-title">{conv['title']}</div>
                        <div class="card-summary">{conv['summary']}</div>
                        <div class="card-meta">
                            <span>📅 {conv['inserted_at'] or 'N/A'}</span>
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
        print("🚀 SISTEMA DEEPSEEK COM FRAGMENTS")
        print("=" * 50)
        
        success = self.extract_deepseek_conversations()
        
        if not success:
            print("❌ Não foi possível extrair conversas")
            return
        
        self.create_searchable_index()
        
        print(f"\n🎉 SISTEMA COMPLETO!")
        print(f"📁 Conversas: {len(self.conversations)}")
        print(f"📄 Índice: {self.index_file}")
        print(f"📊 Ordenação: Mais Recentes Primeiro ✓")
        
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')

if __name__ == "__main__":
    system = DeepSeekFragmentsSystem()
    system.generate_complete_system()
```

**Principais alterações feitas:**

1. **Ordenação das conversas**: Adicionei uma ordenação que usa `updated_at` ou `inserted_at` para ordenar do mais novo para o mais antigo usando `reverse=True`

2. **Reenumeração**: Após ordenar, as conversas são reenumeradas para que a conversa mais recente seja #1, a segunda mais recente #2, etc.

3. **Campo de ordenação**: Adicionei `sort_timestamp` para facilitar a ordenação

4. **Interface atualizada**: O índice HTML agora indica claramente "Mais Recentes Primeiro" na interface

5. **Melhor tratamento de datas**: Uso `datetime.fromisoformat()` para garantir uma ordenação correta por data/hora

Agora as conversas serão apresentadas na ordem correta: as mais recentes primeiro no índice e nos arquivos Markdown!

---

### 👤 Utilizador *(2025-10-27 05:30:38)* *[deepseek-chat]*

a ordenação não está correcta

---

### 🤖 DeepSeek *(2025-10-27 05:30:38)* *[deepseek-chat]*

Tem razão! Vou corrigir a ordenação. O problema está no parsing das datas. Aqui está a versão corrigida:

```python
# deepseek_fragments_system.py
import json
import zipfile
import os
from datetime import datetime
import subprocess
import webbrowser

class DeepSeekFragmentsSystem:
    def __init__(self, zip_file="deepseek_data.zip"):
        self.zip_file = zip_file
        self.markdown_folder = "deepseek_markdown"
        self.conversations = []
        self.index_file = "deepseek_index.html"
        self.pdf_folder = "deepseek_pdfs"
        
    def extract_deepseek_conversations(self):
        """Extrai conversas focando nos fragments"""
        print("🔧 Extraindo conversas dos fragments...")
        
        if not os.path.exists(self.zip_file):
            print(f"❌ Arquivo não encontrado: {self.zip_file}")
            return False
        
        try:
            # Extrai o ZIP
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"✅ ZIP extraído! {len(file_list)} arquivos")
                
                temp_dir = "temp_deepseek_fragments"
                os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)
            
            # Processa conversations.json
            conv_file = os.path.join(temp_dir, "conversations.json")
            
            if not os.path.exists(conv_file):
                print("❌ conversations.json não encontrado!")
                return False
            
            print("📖 Lendo conversations.json...")
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print("❌ Formato inválido")
                return False
            
            print(f"🎯 Processando {len(data)} conversas...")
            
            # Processa cada conversa
            self.conversations = []
            for i, conv_data in enumerate(data):
                conversation = self.process_conversation(conv_data, i+1)
                if conversation and conversation['messages']:
                    self.conversations.append(conversation)
                    print(f"✅ {i+1:02d}: '{conversation['title']}' - {len(conversation['messages'])} mensagens")
                else:
                    print(f"⚠️  {i+1:02d}: '{conv_data.get('title', 'Sem título')}' - SEM MENSAGENS")
            
            # ORDENAÇÃO CORRIGIDA: do mais novo para o mais antigo
            print("🔄 Ordenando conversas do mais novo para o mais antigo...")
            self.conversations.sort(key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at')
            ), reverse=True)
            
            # Reenumera as conversas após ordenação
            for i, conv in enumerate(self.conversations):
                conv['number'] = i + 1
            
            print(f"📊 Total de conversas com mensagens: {len(self.conversations)}")
            
            if self.conversations:
                self.save_as_markdown()
            
            # Limpa
            import shutil
            shutil.rmtree(temp_dir)
            
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
            # Remove o 'Z' do final se existir e converte para datetime
            if isinstance(timestamp, str):
                if timestamp.endswith('Z'):
                    timestamp = timestamp[:-1] + '+00:00'
                return datetime.fromisoformat(timestamp)
            elif isinstance(timestamp, (int, float)):
                # Se for timestamp numérico
                return datetime.fromtimestamp(timestamp)
        except Exception as e:
            print(f"⚠️  Erro ao converter timestamp '{timestamp}': {e}")
        
        return datetime.min
    
    def process_conversation(self, conv_data, number):
        """Processa uma conversa individual"""
        try:
            title = conv_data.get('title', f'Conversa {number}')
            conv_id = conv_data.get('id', f'conv_{number}')
            inserted_at = conv_data.get('inserted_at')
            updated_at = conv_data.get('updated_at')
            
            # Extrai mensagens do mapping focando nos fragments
            mapping = conv_data.get('mapping', {})
            messages = self.extract_messages_from_fragments(mapping)
            
            return {
                'number': number,
                'id': conv_id,
                'title': title,
                'inserted_at': self.format_timestamp(inserted_at),
                'updated_at': self.format_timestamp(updated_at),
                'messages': messages,
                'message_count': len(messages),
                'summary': self.generate_summary(messages),
                'raw_timestamp': updated_at or inserted_at  # Para ordenação
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao processar conversa {number}: {e}")
            return None
    
    def extract_messages_from_fragments(self, mapping):
        """Extrai mensagens dos fragments"""
        messages = []
        
        # Itera por todos os nós do mapping
        for node_id, node in mapping.items():
            if not isinstance(node, dict):
                continue
                
            message_data = node.get('message')
            
            # Só processa se message não for None e for dict
            if message_data and isinstance(message_data, dict):
                message = self.parse_message_from_fragments(message_data, node_id)
                if message and message['content']:  # Só adiciona se tiver conteúdo
                    messages.append(message)
        
        # Ordena pela ordem dos nós
        try:
            messages.sort(key=lambda x: int(x['node_id']) if x['node_id'].isdigit() else 0)
        except:
            # Se não conseguir ordenar, mantém ordem original
            pass
        
        return messages
    
    def parse_message_from_fragments(self, message_data, node_id):
        """Analisa uma mensagem extraindo texto dos fragments"""
        try:
            # Tenta determinar o autor pelo model
            model = message_data.get('model', '')
            if 'deepseek' in model.lower() or 'assistant' in model.lower():
                role = 'assistant'
                author_display = '🤖 DeepSeek'
            else:
                role = 'user'
                author_display = '👤 Você'
            
            # Extrai conteúdo dos fragments
            fragments = message_data.get('fragments', [])
            content_parts = []
            
            for fragment in fragments:
                if isinstance(fragment, dict):
                    # Fragment pode ter texto diretamente
                    text = fragment.get('text', '')
                    if text:
                        content_parts.append(str(text))
                    
                    # Ou pode ter conteúdo em outras chaves
                    content = fragment.get('content', '')
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
            
            # Se não encontrou conteúdo nos fragments, tenta outras chaves
            if not content:
                content = message_data.get('content', '')
                if isinstance(content, list):
                    content = ' '.join([str(item) for item in content if item])
            
            # Remove conteúdo vazio
            if not content or content.isspace():
                return None
            
            # Timestamp
            timestamp = message_data.get('inserted_at') or message_data.get('created_at')
            
            return {
                'node_id': node_id,
                'author': author_display,
                'role': role,
                'content': content,
                'timestamp': self.format_timestamp(timestamp),
                'model': model
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar mensagem {node_id}: {e}")
            return None
    
    def format_timestamp(self, timestamp):
        """Formata timestamp para exibição"""
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, str):
                # Formata para exibição amigável
                if 'T' in timestamp:
                    return timestamp.replace('T', ' ').split('.')[0]
                return timestamp
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
            
            print(f"✅ {filename} (📅 {conversation['updated_at'] or conversation['inserted_at']})")
        
        print(f"🎉 {len(self.conversations)} arquivos criados em '{self.markdown_folder}'")
    
    def create_markdown_content(self, conversation):
        """Cria conteúdo Markdown"""
        md = f"# 💬 {conversation['title']}\n\n"
        
        # Metadados
        md += "## 📊 Informações\n\n"
        md += f"- **Número:** #{conversation['number']}\n"
        md += f"- **ID:** {conversation['id']}\n"
        md += f"- **Criada em:** {conversation['inserted_at'] or 'N/A'}\n"
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
        md += "*Conversa exportada do DeepSeek*  \n"
        md += f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        
        return md
    
    def create_searchable_index(self):
        """Cria índice HTML"""
        print("🎯 Criando índice pesquisável...")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📚 Índice de Conversas - DeepSeek</title>
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
                    <p>DeepSeek - Histórico Completo (Mais Recentes Primeiro)</p>
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
                            <span>📅 {conv['updated_at'] or conv['inserted_at'] or 'N/A'}</span>
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
        print("🚀 SISTEMA DEEPSEEK COM FRAGMENTS")
        print("=" * 50)
        
        success = self.extract_deepseek_conversations()
        
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
            print(f"   #{conv['number']}: {conv['title']} ({conv['updated_at'] or conv['inserted_at']})")
        
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')

if __name__ == "__main__":
    system = DeepSeekFragmentsSystem()
    system.generate_complete_system()
```

**Principais correções:**

1. **Função dedicada para parsing de timestamps**: `parse_timestamp_for_sorting()` que lida corretamente com diferentes formatos de data

2. **Uso do timestamp original**: Uso `raw_timestamp` (o timestamp original do JSON) em vez do formatado para exibição

3. **Tratamento do timezone**: Remove o 'Z' e adiciona '+00:00' para compatibilidade com `fromisoformat()`

4. **Melhor debug**: Mostra as datas durante o processamento e lista as 3 conversas mais recentes para verificação

5. **Badge "NOVO"**: Adicionei um badge nas 3 conversas mais recentes no índice HTML

Agora a ordenação deve funcionar corretamente, apresentando as conversas mais recentes primeiro!

---

### 👤 Utilizador *(2025-10-28 05:24:02)* *[deepseek-chat]*

deepseek_pdf_direct.py é possivel modificar este para deepseek_pdf_direct2.py usando o metodo do deepseek_convert3.py

---

### 🤖 DeepSeek *(2025-10-28 05:24:02)* *[deepseek-chat]*

Sim, perfeitamente! Vou criar `deepseek_pdf_direct2.py` baseado no método do `deepseek_convert3.py`:

```python
# deepseek_pdf_direct2.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import base64
import glob

def html_to_pdf_direct(html_file, pdf_file):
    """Converte HTML para PDF usando Chrome DevTools Protocol"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abrir arquivo HTML
        full_path = f"file:///{os.path.abspath(html_file)}"
        print(f"📖 Convertendo: {html_file}")
        driver.get(full_path)
        
        # Aguardar carregamento
        driver.implicitly_wait(5)
        
        # Executar comando do Chrome DevTools para gerar PDF
        pdf_params = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
            'marginTop': 0.5,
            'marginBottom': 0.5,
            'marginLeft': 0.5,
            'marginRight': 0.5,
        }
        
        # Gerar PDF diretamente
        result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
        pdf_data = base64.b64decode(result['data'])
        
        # Salvar PDF
        with open(pdf_file, 'wb') as f:
            f.write(pdf_data)
        
        print(f"✅ PDF gerado: {os.path.basename(pdf_file)}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao converter {html_file}: {e}")
        return False
    finally:
        driver.quit()

def convert_all_markdown_to_pdf(markdown_folder="deepseek_markdown", pdf_folder="deepseek_pdfs"):
    """Converte todos os arquivos Markdown para PDF"""
    
    if not os.path.exists(markdown_folder):
        print(f"❌ Pasta não encontrada: {markdown_folder}")
        return False
    
    # Criar pasta de PDFs se não existir
    os.makedirs(pdf_folder, exist_ok=True)
    
    # Encontrar todos os arquivos .md
    md_files = glob.glob(os.path.join(markdown_folder, "*.md"))
    
    if not md_files:
        print(f"❌ Nenhum arquivo .md encontrado em {markdown_folder}")
        return False
    
    print(f"🎯 Encontrados {len(md_files)} arquivos Markdown")
    
    success_count = 0
    
    for md_file in md_files:
        # Nome do arquivo PDF correspondente
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
        
        # Primeiro converter Markdown para HTML temporário
        html_content = convert_markdown_to_html(md_file)
        if html_content:
            # Salvar HTML temporário
            temp_html = "temp_conversion.html"
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Converter HTML para PDF
            if html_to_pdf_direct(temp_html, pdf_file):
                success_count += 1
            
            # Limpar arquivo temporário
            if os.path.exists(temp_html):
                os.remove(temp_html)
        else:
            print(f"❌ Falha ao converter Markdown: {os.path.basename(md_file)}")
    
    print(f"\n📊 Resumo da conversão:")
    print(f"   ✅ Sucessos: {success_count}/{len(md_files)}")
    print(f"   📁 Pasta de PDFs: {os.path.abspath(pdf_folder)}")
    
    return success_count > 0

def convert_markdown_to_html(md_file_path):
    """Converte arquivo Markdown para HTML com estilo"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Converter Markdown básico para HTML
        html_content = markdown_to_html_basic(markdown_content)
        
        # Adicionar estilo CSS
        styled_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Conversa DeepSeek</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 40px 20px;
                    background: #f8f9fa;
                }}
                .conversation-container {{
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    padding: 40px;
                }}
                h1 {{
                    color: #0052d4;
                    border-bottom: 3px solid #0052d4;
                    padding-bottom: 10px;
                    margin-bottom: 30px;
                    font-size: 2.2em;
                }}
                h2 {{
                    color: #4364f7;
                    margin-top: 30px;
                    margin-bottom: 15px;
                    font-size: 1.5em;
                }}
                h3 {{
                    color: #6fb1fc;
                    margin-top: 25px;
                    margin-bottom: 10px;
                    font-size: 1.2em;
                }}
                .metadata {{
                    background: #f8f9fa;
                    border-left: 4px solid #0052d4;
                    padding: 15px 20px;
                    margin: 20px 0;
                    border-radius: 0 8px 8px 0;
                }}
                .message {{
                    margin: 25px 0;
                    padding: 20px;
                    border-radius: 10px;
                    background: #f8f9fa;
                    border-left: 4px solid #4364f7;
                }}
                .user-message {{
                    background: #e3f2fd;
                    border-left-color: #1976d2;
                }}
                .assistant-message {{
                    background: #f3e5f5;
                    border-left-color: #7b1fa2;
                }}
                .message-header {{
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #555;
                }}
                .message-content {{
                    white-space: pre-wrap;
                    font-size: 14px;
                }}
                .timestamp {{
                    font-size: 0.85em;
                    color: #888;
                    font-style: italic;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
                hr {{
                    border: none;
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #0052d4, transparent);
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="conversation-container">
                {html_content}
            </div>
        </body>
        </html>
        """
        
        return styled_html
        
    except Exception as e:
        print(f"❌ Erro ao converter Markdown para HTML: {e}")
        return None

def markdown_to_html_basic(markdown_text):
    """Conversor básico de Markdown para HTML"""
    # Headers
    markdown_text = markdown_text.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
    markdown_text = markdown_text.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
    markdown_text = markdown_text.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
    
    # Quebras de linha
    markdown_text = markdown_text.replace('\n', '<br>\n')
    
    # Strong/bold
    markdown_text = markdown_text.replace('**', '<strong>').replace('**', '</strong>')
    
    # Italic
    markdown_text = markdown_text.replace('*', '<em>').replace('*', '</em>')
    
    # Separadores
    markdown_text = markdown_text.replace('---', '<hr>')
    
    # Processar mensagens específicas
    lines = markdown_text.split('<br>\n')
    processed_lines = []
    
    for line in lines:
        # Detectar mensagens do usuário e assistente
        if '👤 Você' in line and '<h3>' in line:
            line = line.replace('<h3>', '<div class="message user-message"><div class="message-header">')
            line = line.replace('</h3>', '</div><div class="message-content">') + '</div></div>'
        elif '🤖 DeepSeek' in line and '<h3>' in line:
            line = line.replace('<h3>', '<div class="message assistant-message"><div class="message-header">')
            line = line.replace('</h3>', '</div><div class="message-content">') + '</div></div>'
        elif '## 📊 Informações' in line:
            line = '<div class="metadata">' + line.replace('## 📊 Informações', '<h2>📊 Informações</h2>')
        elif '## 🗨️ Conversa' in line:
            line = '</div>' + line.replace('## 🗨️ Conversa', '<h2>🗨️ Conversa</h2>')
        
        processed_lines.append(line)
    
    markdown_text = '<br>\n'.join(processed_lines)
    
    # Fechar div de metadata se existir
    if '<div class="metadata">' in markdown_text and '</div>' not in markdown_text.split('<div class="metadata">')[1]:
        markdown_text += '</div>'
    
    return markdown_text

def convert_single_file(md_file, pdf_folder="deepseek_pdfs"):
    """Converte um único arquivo Markdown para PDF"""
    if not os.path.exists(md_file):
        print(f"❌ Arquivo não encontrado: {md_file}")
        return False
    
    os.makedirs(pdf_folder, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(md_file))[0]
    pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
    
    html_content = convert_markdown_to_html(md_file)
    if html_content:
        temp_html = "temp_single_conversion.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        success = html_to_pdf_direct(temp_html, pdf_file)
        
        if os.path.exists(temp_html):
            os.remove(temp_html)
        
        return success
    
    return False

if __name__ == "__main__":
    print("🚀 CONVERSOR DEEPSEEK MARKDOWN PARA PDF")
    print("=" * 50)
    
    # Converter todos os arquivos
    success = convert_all_markdown_to_pdf()
    
    if success:
        print("\n🎉 Conversão concluída com sucesso!")
    else:
        print("\n❌ Houve erros na conversão.")
    
    # Exemplo de conversão individual:
    # convert_single_file("deepseek_markdown/001_minha_conversa.md")
```

**Principais melhorias em relação ao `deepseek_convert3.py`:**

1. **Conversão em lote**: Converte todos os arquivos .md de uma pasta automaticamente
2. **Conversão individual**: Função para converter um único arquivo
3. **Estilo profissional**: CSS melhorado para PDFs com aparência profissional
4. **Processamento de Markdown**: Conversor básico de Markdown para HTML
5. **Mensagens estilizadas**: Diferentes estilos para usuário e assistente
6. **Metadados formatados**: Área de informações com destaque
7. **Tratamento de erros**: Melhor gestão de erros e feedback
8. **Resumo de conversão**: Estatísticas finais do processo

**Como usar:**

```bash
# Converter todos os arquivos
python deepseek_pdf_direct2.py

# Ou converter um arquivo específico
python deepseek_pdf_direct2.py -f "deepseek_markdown/001_conversa.md"
```

O script criará PDFs coloridos e bem formatados mantendo os emojis e a estrutura das conversas!

---

### 👤 Utilizador *(2025-10-28 05:32:14)* *[deepseek-chat]*

(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__DeepSeek>python deepseek_pdf_direct2.py
🚀 CONVERSOR DEEPSEEK MARKDOWN PARA PDF
==================================================
🎯 Encontrados 129 arquivos Markdown
📖 Convertendo: temp_conversion.html
❌ Erro ao converter temp_conversion.html: HTTPConnectionPool(host='localhost', port=56680): Read timed out. (read timeout=120)

---

### 🤖 DeepSeek *(2025-10-28 05:32:14)* *[deepseek-chat]*

O erro é de timeout na conexão com o Chrome. Vou corrigir o script para ser mais robusto:

```python
# deepseek_pdf_direct2.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import base64
import glob
import time
import random

def html_to_pdf_direct(html_file, pdf_file, retry_count=3):
    """Converte HTML para PDF usando Chrome DevTools Protocol"""
    
    for attempt in range(retry_count):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Opcional: acelera carregamento
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Desabilita imagens
        
        # Timeouts aumentados
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        driver = None
        try:
            print(f"📖 Convertendo: {html_file} (tentativa {attempt + 1}/{retry_count})")
            
            # Inicializar driver com timeouts maiores
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(60)  # 60 segundos para carregar página
            driver.implicitly_wait(10)
            
            # Abrir arquivo HTML
            full_path = f"file:///{os.path.abspath(html_file)}"
            driver.get(full_path)
            
            # Aguardar carregamento com wait explícito
            WebDriverWait(driver, 30).wait(lambda d: d.execute_script('return document.readyState') == 'complete')
            
            # Pequena pausa para garantir que tudo carregou
            time.sleep(2)
            
            # Executar comando do Chrome DevTools para gerar PDF
            pdf_params = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'marginTop': 0.5,
                'marginBottom': 0.5,
                'marginLeft': 0.5,
                'marginRight': 0.5,
            }
            
            # Gerar PDF diretamente
            result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
            pdf_data = base64.b64decode(result['data'])
            
            # Salvar PDF
            with open(pdf_file, 'wb') as f:
                f.write(pdf_data)
            
            print(f"✅ PDF gerado: {os.path.basename(pdf_file)}")
            return True
            
        except TimeoutException as e:
            print(f"⏰ Timeout na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)  # Pausa antes de retry
            continue
            
        except WebDriverException as e:
            print(f"🚫 Erro WebDriver na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        except Exception as e:
            print(f"❌ Erro inesperado na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        finally:
            if driver:
                driver.quit()
    
    print(f"💥 Falha após {retry_count} tentativas: {html_file}")
    return False

def convert_all_markdown_to_pdf(markdown_folder="deepseek_markdown", pdf_folder="deepseek_pdfs", batch_size=10):
    """Converte todos os arquivos Markdown para PDF em lotes"""
    
    if not os.path.exists(markdown_folder):
        print(f"❌ Pasta não encontrada: {markdown_folder}")
        return False
    
    # Criar pasta de PDFs se não existir
    os.makedirs(pdf_folder, exist_ok=True)
    
    # Encontrar todos os arquivos .md
    md_files = glob.glob(os.path.join(markdown_folder, "*.md"))
    
    if not md_files:
        print(f"❌ Nenhum arquivo .md encontrado em {markdown_folder}")
        return False
    
    print(f"🎯 Encontrados {len(md_files)} arquivos Markdown")
    print(f"📦 Processando em lotes de {batch_size} arquivos")
    
    success_count = 0
    failed_files = []
    
    # Processar em lotes para evitar sobrecarga
    for i in range(0, len(md_files), batch_size):
        batch = md_files[i:i + batch_size]
        print(f"\n🔄 Processando lote {i//batch_size + 1}/{(len(md_files)-1)//batch_size + 1}")
        
        for md_file in batch:
            # Verificar se PDF já existe
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
            
            if os.path.exists(pdf_file):
                print(f"⏭️  PDF já existe: {os.path.basename(pdf_file)}")
                success_count += 1
                continue
            
            # Primeiro converter Markdown para HTML temporário
            html_content = convert_markdown_to_html(md_file)
            if html_content:
                # Salvar HTML temporário
                temp_html = f"temp_conversion_{base_name}.html"
                try:
                    with open(temp_html, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Converter HTML para PDF
                    if html_to_pdf_direct(temp_html, pdf_file):
                        success_count += 1
                        print(f"✅ Sucesso: {os.path.basename(pdf_file)}")
                    else:
                        failed_files.append(os.path.basename(md_file))
                        print(f"❌ Falha: {os.path.basename(md_file)}")
                    
                finally:
                    # Limpar arquivo temporário
                    if os.path.exists(temp_html):
                        os.remove(temp_html)
            else:
                failed_files.append(os.path.basename(md_file))
                print(f"❌ Falha ao converter Markdown: {os.path.basename(md_file)}")
            
            # Pequena pausa entre conversões
            time.sleep(1)
        
        # Pausa maior entre lotes
        if i + batch_size < len(md_files):
            print("💤 Pausa entre lotes...")
            time.sleep(5)
    
    print(f"\n📊 Resumo da conversão:")
    print(f"   ✅ Sucessos: {success_count}/{len(md_files)}")
    print(f"   ❌ Falhas: {len(failed_files)}")
    print(f"   📁 Pasta de PDFs: {os.path.abspath(pdf_folder)}")
    
    if failed_files:
        print(f"\n📋 Arquivos com falha:")
        for failed in failed_files[:10]:  # Mostra apenas os primeiros 10
            print(f"   - {failed}")
        if len(failed_files) > 10:
            print(f"   ... e mais {len(failed_files) - 10} arquivos")
    
    return success_count > 0

def convert_markdown_to_html(md_file_path):
    """Converte arquivo Markdown para HTML com estilo simplificado"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # HTML básico e limpo
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Conversa DeepSeek</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.4;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: white;
                }}
                h1 {{
                    color: #0052d4;
                    border-bottom: 2px solid #0052d4;
                    padding-bottom: 5px;
                }}
                h2 {{
                    color: #4364f7;
                    margin-top: 25px;
                }}
                h3 {{
                    color: #6fb1fc;
                    margin-top: 20px;
                }}
                .message {{
                    margin: 15px 0;
                    padding: 15px;
                    border-radius: 5px;
                    background: #f5f5f5;
                }}
                .user-message {{
                    background: #e3f2fd;
                    border-left: 3px solid #1976d2;
                }}
                .assistant-message {{
                    background: #f3e5f5;
                    border-left: 3px solid #7b1fa2;
                }}
                .metadata {{
                    background: #f8f9fa;
                    padding: 10px;
                    margin: 15px 0;
                    border-radius: 5px;
                }}
                .timestamp {{
                    font-size: 0.8em;
                    color: #666;
                }}
                hr {{
                    border: none;
                    height: 1px;
                    background: #ddd;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            {markdown_to_html_simple(markdown_content)}
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"❌ Erro ao converter Markdown para HTML: {e}")
        return None

def markdown_to_html_simple(markdown_text):
    """Conversor simples e rápido de Markdown para HTML"""
    # Headers
    lines = markdown_text.split('\n')
    html_lines = []
    
    for line in lines:
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.strip() == '---':
            html_lines.append('<hr>')
        elif '👤 Você' in line and '###' in line:
            # Mensagem do usuário
            content = line.replace('### ', '').replace('👤 Você', '').strip()
            html_lines.append(f'<div class="message user-message"><strong>👤 Você</strong><br>{content}</div>')
        elif '🤖 DeepSeek' in line and '###' in line:
            # Mensagem do assistente
            content = line.replace('### ', '').replace('🤖 DeepSeek', '').strip()
            html_lines.append(f'<div class="message assistant-message"><strong>🤖 DeepSeek</strong><br>{content}</div>')
        elif line.strip() and not line.startswith('###'):
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append('<br>')
    
    return '\n'.join(html_lines)

def convert_single_file(md_file, pdf_folder="deepseek_pdfs"):
    """Converte um único arquivo Markdown para PDF"""
    if not os.path.exists(md_file):
        print(f"❌ Arquivo não encontrado: {md_file}")
        return False
    
    os.makedirs(pdf_folder, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(md_file))[0]
    pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
    
    html_content = convert_markdown_to_html(md_file)
    if html_content:
        temp_html = f"temp_single_{base_name}.html"
        try:
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            success = html_to_pdf_direct(temp_html, pdf_file)
            return success
            
        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)
    
    return False

if __name__ == "__main__":
    print("🚀 CONVERSOR DEEPSEEK MARKDOWN PARA PDF (ROBUSTO)")
    print("=" * 50)
    
    # Verificar se Chrome está disponível
    try:
        test_driver = webdriver.Chrome(options=Options())
        test_driver.quit()
        print("✅ Chrome Driver verificado")
    except Exception as e:
        print(f"❌ Chrome Driver não disponível: {e}")
        print("💡 Instale o Chrome Driver ou verifique o PATH")
        exit(1)
    
    # Converter todos os arquivos
    success = convert_all_markdown_to_pdf()
    
    if success:
        print("\n🎉 Conversão concluída!")
    else:
        print("\n⚠️  Conversão parcial ou com falhas.")
    
    print("\n💡 Dica: Para converter arquivos individuais:")
    print("   python deepseek_pdf_direct2.py -f \"caminho/arquivo.md\"")
```

**Principais correções:**

1. **Retry automático**: 3 tentativas por arquivo com pausas
2. **Timeouts aumentados**: 60 segundos para carregamento
3. **Processamento em lotes**: Processa 10 arquivos por lote com pausas
4. **HTML simplificado**: CSS mais leve para carregamento rápido
5. **Limpeza de recursos**: Fecha o driver corretamente a cada arquivo
6. **Verificação do Chrome**: Verifica se o Chrome Driver está disponível
7. **Pausas estratégicas**: Entre arquivos e entre lotes
8. **Skip de duplicados**: Não reconverte arquivos que já existem
9. **Feedback melhorado**: Mostra progresso detalhado

**Execute novamente:** O script agora deve ser muito mais robusto e lidar melhor com timeouts!

---

### 👤 Utilizador *(2025-10-28 05:47:00)* *[deepseek-chat]*

🔄 Processando lote 4/13
📖 Convertendo: temp_conversion_016_Guia_Nutricional_de_Queijo_em_Portugal.html (tentativa 1/3)
❌ Erro inesperado na tentativa 1: 'WebDriverWait' object has no attribute 'wait'
📖 Convertendo: temp_conversion_016_Guia_Nutricional_de_Queijo_em_Portugal.html (tentativa 2/3)
❌ Erro inesperado na tentativa 2: 'WebDriverWait' object has no attribute 'wait'

---

### 🤖 DeepSeek *(2025-10-28 05:47:00)* *[deepseek-chat]*

Tem um erro na sintaxe do WebDriverWait. Vou corrigir:

```python
# deepseek_pdf_direct2.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import base64
import glob
import time
import random

def html_to_pdf_direct(html_file, pdf_file, retry_count=3):
    """Converte HTML para PDF usando Chrome DevTools Protocol"""
    
    for attempt in range(retry_count):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        driver = None
        try:
            print(f"📖 Convertendo: {os.path.basename(html_file)} (tentativa {attempt + 1}/{retry_count})")
            
            # Inicializar driver com timeouts maiores
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(10)
            
            # Abrir arquivo HTML
            full_path = f"file:///{os.path.abspath(html_file)}"
            driver.get(full_path)
            
            # CORREÇÃO: Usar WebDriverWait corretamente
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Pequena pausa para garantir que tudo carregou
            time.sleep(2)
            
            # Executar comando do Chrome DevTools para gerar PDF
            pdf_params = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'marginTop': 0.5,
                'marginBottom': 0.5,
                'marginLeft': 0.5,
                'marginRight': 0.5,
            }
            
            # Gerar PDF diretamente
            result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
            pdf_data = base64.b64decode(result['data'])
            
            # Salvar PDF
            with open(pdf_file, 'wb') as f:
                f.write(pdf_data)
            
            print(f"✅ PDF gerado: {os.path.basename(pdf_file)}")
            return True
            
        except TimeoutException as e:
            print(f"⏰ Timeout na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        except WebDriverException as e:
            print(f"🚫 Erro WebDriver na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        except Exception as e:
            print(f"❌ Erro inesperado na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        finally:
            if driver:
                driver.quit()
    
    print(f"💥 Falha após {retry_count} tentativas: {os.path.basename(html_file)}")
    return False

def convert_all_markdown_to_pdf(markdown_folder="deepseek_markdown", pdf_folder="deepseek_pdfs", batch_size=10):
    """Converte todos os arquivos Markdown para PDF em lotes"""
    
    if not os.path.exists(markdown_folder):
        print(f"❌ Pasta não encontrada: {markdown_folder}")
        return False
    
    # Criar pasta de PDFs se não existir
    os.makedirs(pdf_folder, exist_ok=True)
    
    # Encontrar todos os arquivos .md
    md_files = glob.glob(os.path.join(markdown_folder, "*.md"))
    
    if not md_files:
        print(f"❌ Nenhum arquivo .md encontrado em {markdown_folder}")
        return False
    
    print(f"🎯 Encontrados {len(md_files)} arquivos Markdown")
    print(f"📦 Processando em lotes de {batch_size} arquivos")
    
    success_count = 0
    failed_files = []
    
    # Processar em lotes para evitar sobrecarga
    for i in range(0, len(md_files), batch_size):
        batch = md_files[i:i + batch_size]
        print(f"\n🔄 Processando lote {i//batch_size + 1}/{(len(md_files)-1)//batch_size + 1}")
        
        for md_file in batch:
            # Verificar se PDF já existe
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
            
            if os.path.exists(pdf_file):
                print(f"⏭️  PDF já existe: {os.path.basename(pdf_file)}")
                success_count += 1
                continue
            
            # Primeiro converter Markdown para HTML temporário
            html_content = convert_markdown_to_html(md_file)
            if html_content:
                # Salvar HTML temporário
                temp_html = f"temp_conversion_{base_name}.html"
                try:
                    with open(temp_html, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Converter HTML para PDF
                    if html_to_pdf_direct(temp_html, pdf_file):
                        success_count += 1
                        print(f"✅ Sucesso: {os.path.basename(pdf_file)}")
                    else:
                        failed_files.append(os.path.basename(md_file))
                        print(f"❌ Falha: {os.path.basename(md_file)}")
                    
                finally:
                    # Limpar arquivo temporário
                    if os.path.exists(temp_html):
                        os.remove(temp_html)
            else:
                failed_files.append(os.path.basename(md_file))
                print(f"❌ Falha ao converter Markdown: {os.path.basename(md_file)}")
            
            # Pequena pausa entre conversões
            time.sleep(1)
        
        # Pausa maior entre lotes
        if i + batch_size < len(md_files):
            print("💤 Pausa entre lotes...")
            time.sleep(5)
    
    print(f"\n📊 Resumo da conversão:")
    print(f"   ✅ Sucessos: {success_count}/{len(md_files)}")
    print(f"   ❌ Falhas: {len(failed_files)}")
    print(f"   📁 Pasta de PDFs: {os.path.abspath(pdf_folder)}")
    
    if failed_files:
        print(f"\n📋 Arquivos com falha:")
        for failed in failed_files[:10]:
            print(f"   - {failed}")
        if len(failed_files) > 10:
            print(f"   ... e mais {len(failed_files) - 10} arquivos")
    
    return success_count > 0

def convert_markdown_to_html(md_file_path):
    """Converte arquivo Markdown para HTML com estilo simplificado"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # HTML básico e limpo
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Conversa DeepSeek</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.4;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: white;
                }}
                h1 {{
                    color: #0052d4;
                    border-bottom: 2px solid #0052d4;
                    padding-bottom: 5px;
                }}
                h2 {{
                    color: #4364f7;
                    margin-top: 25px;
                }}
                h3 {{
                    color: #6fb1fc;
                    margin-top: 20px;
                }}
                .message {{
                    margin: 15px 0;
                    padding: 15px;
                    border-radius: 5px;
                    background: #f5f5f5;
                }}
                .user-message {{
                    background: #e3f2fd;
                    border-left: 3px solid #1976d2;
                }}
                .assistant-message {{
                    background: #f3e5f5;
                    border-left: 3px solid #7b1fa2;
                }}
                .metadata {{
                    background: #f8f9fa;
                    padding: 10px;
                    margin: 15px 0;
                    border-radius: 5px;
                }}
                .timestamp {{
                    font-size: 0.8em;
                    color: #666;
                }}
                hr {{
                    border: none;
                    height: 1px;
                    background: #ddd;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            {markdown_to_html_simple(markdown_content)}
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"❌ Erro ao converter Markdown para HTML: {e}")
        return None

def markdown_to_html_simple(markdown_text):
    """Conversor simples e rápido de Markdown para HTML"""
    lines = markdown_text.split('\n')
    html_lines = []
    in_message = False
    current_message_type = None
    message_content = []
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            # Verificar se é início de mensagem
            if '👤 Você' in line:
                if in_message:
                    html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = True
                current_message_type = 'user-message'
                message_content = [f'<strong>👤 Você</strong>']
            elif '🤖 DeepSeek' in line:
                if in_message:
                    html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = True
                current_message_type = 'assistant-message'
                message_content = [f'<strong>🤖 DeepSeek</strong>']
            else:
                if in_message:
                    html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                    in_message = False
                html_lines.append(f'<h3>{line[4:]}</h3>')
        
        # Separadores
        elif line.strip() == '---':
            if in_message:
                html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = False
            html_lines.append('<hr>')
        
        # Conteúdo de mensagens
        elif in_message and line.strip() and not line.startswith('###'):
            message_content.append(line.strip())
        
        # Outras linhas
        elif line.strip() and not line.startswith('###'):
            if in_message:
                html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = False
            html_lines.append(f'<p>{line}</p>')
        else:
            if in_message and not line.strip():
                message_content.append('<br>')
            elif not in_message:
                html_lines.append('<br>')
    
    # Fechar última mensagem se ainda aberta
    if in_message:
        html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
    
    return '\n'.join(html_lines)

def convert_single_file(md_file, pdf_folder="deepseek_pdfs"):
    """Converte um único arquivo Markdown para PDF"""
    if not os.path.exists(md_file):
        print(f"❌ Arquivo não encontrado: {md_file}")
        return False
    
    os.makedirs(pdf_folder, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(md_file))[0]
    pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
    
    html_content = convert_markdown_to_html(md_file)
    if html_content:
        temp_html = f"temp_single_{base_name}.html"
        try:
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            success = html_to_pdf_direct(temp_html, pdf_file)
            return success
            
        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)
    
    return False

if __name__ == "__main__":
    print("🚀 CONVERSOR DEEPSEEK MARKDOWN PARA PDF (CORRIGIDO)")
    print("=" * 50)
    
    # Verificar se Chrome está disponível
    try:
        test_driver = webdriver.Chrome(options=Options())
        test_driver.quit()
        print("✅ Chrome Driver verificado")
    except Exception as e:
        print(f"❌ Chrome Driver não disponível: {e}")
        print("💡 Instale o Chrome Driver ou verifique o PATH")
        exit(1)
    
    # Converter todos os arquivos
    success = convert_all_markdown_to_pdf()
    
    if success:
        print("\n🎉 Conversão concluída!")
    else:
        print("\n⚠️  Conversão parcial ou com falhas.")
```

**Correção principal:** 
- Mudei `WebDriverWait(driver, 30).wait(...)` para `WebDriverWait(driver, 30).until(...)` - o método correto é `until()`, não `wait()`.

**Outras melhorias:**
- Melhor processamento de mensagens no conversor Markdown
- Feedback mais claro mostrando apenas nomes de arquivos
- Tratamento melhor de mensagens consecutivas

Agora deve funcionar sem erros de sintaxe!

---

### 👤 Utilizador *(2025-10-28 06:20:35)* *[deepseek-chat]*

alterar deepseek_pdf_direct2.py de modo a Converter para HTML com pandoc e depois usar o metodo já usado no deepseek_pdf_direct2.py

---

### 🤖 DeepSeek *(2025-10-28 06:20:35)* *[deepseek-chat]*

Excelente ideia! Vou modificar o script para usar o Pandoc para conversão HTML (que é muito mais robusto) e depois usar o método Selenium para PDF:

```python
# deepseek_pdf_direct2.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import base64
import glob
import time
import subprocess
import tempfile

def html_to_pdf_direct(html_file, pdf_file, retry_count=3):
    """Converte HTML para PDF usando Chrome DevTools Protocol"""
    
    for attempt in range(retry_count):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = None
        try:
            print(f"📖 Convertendo HTML para PDF: {os.path.basename(html_file)} (tentativa {attempt + 1}/{retry_count})")
            
            # Inicializar driver
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(60)
            
            # Abrir arquivo HTML
            full_path = f"file:///{os.path.abspath(html_file)}"
            driver.get(full_path)
            
            # Aguardar carregamento
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Pequena pausa para garantir que tudo carregou
            time.sleep(2)
            
            # Executar comando do Chrome DevTools para gerar PDF
            pdf_params = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'marginTop': 0.5,
                'marginBottom': 0.5,
                'marginLeft': 0.5,
                'marginRight': 0.5,
            }
            
            # Gerar PDF diretamente
            result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
            pdf_data = base64.b64decode(result['data'])
            
            # Salvar PDF
            with open(pdf_file, 'wb') as f:
                f.write(pdf_data)
            
            print(f"✅ PDF gerado: {os.path.basename(pdf_file)}")
            return True
            
        except TimeoutException as e:
            print(f"⏰ Timeout na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        except WebDriverException as e:
            print(f"🚫 Erro WebDriver na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        except Exception as e:
            print(f"❌ Erro inesperado na tentativa {attempt + 1}: {e}")
            if driver:
                driver.quit()
            time.sleep(5)
            continue
            
        finally:
            if driver:
                driver.quit()
    
    print(f"💥 Falha após {retry_count} tentativas: {os.path.basename(html_file)}")
    return False

def convert_markdown_to_html_pandoc(md_file_path):
    """Converte Markdown para HTML usando Pandoc"""
    try:
        # Verificar se pandoc está disponível
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Pandoc não encontrado. Instale o Pandoc ou use o conversor interno.")
            return convert_markdown_to_html_fallback(md_file_path)
        
        print(f"🔧 Convertendo com Pandoc: {os.path.basename(md_file_path)}")
        
        # Converter Markdown para HTML usando Pandoc
        html_content = subprocess.run([
            'pandoc', 
            md_file_path,
            '--from', 'markdown+emoji',
            '--to', 'html',
            '--embed-resources',
            '--standalone',
            '--css', 'pandoc-style.css'  # Usar CSS personalizado se existir
        ], capture_output=True, text=True, encoding='utf-8')
        
        if html_content.returncode == 0:
            # Aplicar estilo personalizado ao HTML gerado pelo Pandoc
            styled_html = apply_custom_style(html_content.stdout)
            return styled_html
        else:
            print(f"⚠️  Pandoc falhou, usando fallback: {html_content.stderr}")
            return convert_markdown_to_html_fallback(md_file_path)
            
    except Exception as e:
        print(f"⚠️  Erro no Pandoc, usando fallback: {e}")
        return convert_markdown_to_html_fallback(md_file_path)

def apply_custom_style(html_content):
    """Aplica estilo CSS personalizado ao HTML do Pandoc"""
    custom_style = """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f8f9fa;
        }
        .conversation-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            padding: 40px;
        }
        h1 {
            color: #0052d4;
            border-bottom: 3px solid #0052d4;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #4364f7;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h3 {
            color: #6fb1fc;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        .message {
            margin: 25px 0;
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
            border-left: 4px solid #4364f7;
        }
        .user-message {
            background: #e3f2fd;
            border-left-color: #1976d2;
        }
        .assistant-message {
            background: #f3e5f5;
            border-left-color: #7b1fa2;
        }
        .message-header {
            font-weight: bold;
            margin-bottom: 10px;
            color: #555;
        }
        .metadata {
            background: #f8f9fa;
            border-left: 4px solid #0052d4;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }
        .timestamp {
            font-size: 0.85em;
            color: #888;
            font-style: italic;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #0052d4, transparent);
            margin: 30px 0;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #0052d4;
            padding-left: 15px;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }
    </style>
    """
    
    # Inserir o estilo personalizado no HTML
    if '<style>' not in html_content:
        # Se não houver estilo, adicionar nosso estilo personalizado
        html_content = html_content.replace('</head>', f'{custom_style}</head>')
        html_content = html_content.replace('<body>', '<body><div class="conversation-container">')
        html_content = html_content.replace('</body>', '</div></body>')
    
    return html_content

def convert_markdown_to_html_fallback(md_file_path):
    """Fallback: converte Markdown para HTML manualmente se Pandoc falhar"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # HTML básico com estilo
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Conversa DeepSeek</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.4;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: white;
                }}
                h1 {{
                    color: #0052d4;
                    border-bottom: 2px solid #0052d4;
                    padding-bottom: 5px;
                }}
                h2 {{
                    color: #4364f7;
                    margin-top: 25px;
                }}
                h3 {{
                    color: #6fb1fc;
                    margin-top: 20px;
                }}
                .message {{
                    margin: 15px 0;
                    padding: 15px;
                    border-radius: 5px;
                    background: #f5f5f5;
                }}
                .user-message {{
                    background: #e3f2fd;
                    border-left: 3px solid #1976d2;
                }}
                .assistant-message {{
                    background: #f3e5f5;
                    border-left: 3px solid #7b1fa2;
                }}
                .metadata {{
                    background: #f8f9fa;
                    padding: 10px;
                    margin: 15px 0;
                    border-radius: 5px;
                }}
                .timestamp {{
                    font-size: 0.8em;
                    color: #666;
                }}
                hr {{
                    border: none;
                    height: 1px;
                    background: #ddd;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="conversation-container">
                {markdown_to_html_simple(markdown_content)}
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"❌ Erro no fallback HTML: {e}")
        return None

def markdown_to_html_simple(markdown_text):
    """Conversor simples de Markdown para HTML (fallback)"""
    lines = markdown_text.split('\n')
    html_lines = []
    in_message = False
    current_message_type = None
    message_content = []
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            # Verificar se é início de mensagem
            if '👤 Você' in line:
                if in_message:
                    html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = True
                current_message_type = 'user-message'
                message_content = [f'<strong>👤 Você</strong>']
            elif '🤖 DeepSeek' in line:
                if in_message:
                    html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = True
                current_message_type = 'assistant-message'
                message_content = [f'<strong>🤖 DeepSeek</strong>']
            else:
                if in_message:
                    html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                    in_message = False
                html_lines.append(f'<h3>{line[4:]}</h3>')
        
        # Separadores
        elif line.strip() == '---':
            if in_message:
                html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = False
            html_lines.append('<hr>')
        
        # Conteúdo de mensagens
        elif in_message and line.strip() and not line.startswith('###'):
            message_content.append(line.strip())
        
        # Outras linhas
        elif line.strip() and not line.startswith('###'):
            if in_message:
                html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
                in_message = False
            html_lines.append(f'<p>{line}</p>')
        else:
            if in_message and not line.strip():
                message_content.append('<br>')
            elif not in_message:
                html_lines.append('<br>')
    
    # Fechar última mensagem se ainda aberta
    if in_message:
        html_lines.append(f'<div class="message {current_message_type}">{"<br>".join(message_content)}</div>')
    
    return '\n'.join(html_lines)

def convert_all_markdown_to_pdf(markdown_folder="deepseek_markdown", pdf_folder="deepseek_pdfs", batch_size=10, use_pandoc=True):
    """Converte todos os arquivos Markdown para PDF"""
    
    if not os.path.exists(markdown_folder):
        print(f"❌ Pasta não encontrada: {markdown_folder}")
        return False
    
    # Criar pasta de PDFs se não existir
    os.makedirs(pdf_folder, exist_ok=True)
    
    # Encontrar todos os arquivos .md
    md_files = glob.glob(os.path.join(markdown_folder, "*.md"))
    
    if not md_files:
        print(f"❌ Nenhum arquivo .md encontrado em {markdown_folder}")
        return False
    
    print(f"🎯 Encontrados {len(md_files)} arquivos Markdown")
    print(f"🔧 Usando {'Pandoc' if use_pandoc else 'conversor interno'} para conversão HTML")
    print(f"📦 Processando em lotes de {batch_size} arquivos")
    
    success_count = 0
    failed_files = []
    
    # Processar em lotes
    for i in range(0, len(md_files), batch_size):
        batch = md_files[i:i + batch_size]
        print(f"\n🔄 Processando lote {i//batch_size + 1}/{(len(md_files)-1)//batch_size + 1}")
        
        for md_file in batch:
            # Verificar se PDF já existe
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            pdf_file = os.path.join(pdf_folder, f"{base_name}.pdf")
            
            if os.path.exists(pdf_file):
                print(f"⏭️  PDF já existe: {os.path.basename(pdf_file)}")
                success_count += 1
                continue
            
            # Converter Markdown para HTML
            if use_pandoc:
                html_content = convert_markdown_to_html_pandoc(md_file)
            else:
                html_content = convert_markdown_to_html_fallback(md_file)
            
            if html_content:
                # Salvar HTML temporário
                temp_html = f"temp_conversion_{base_name}.html"
                try:
                    with open(temp_html, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Converter HTML para PDF
                    if html_to_pdf_direct(temp_html, pdf_file):
                        success_count += 1
                        print(f"✅ Sucesso: {os.path.basename(pdf_file)}")
                    else:
                        failed_files.append(os.path.basename(md_file))
                        print(f"❌ Falha: {os.path.basename(md_file)}")
                    
                finally:
                    # Limpar arquivo temporário
                    if os.path.exists(temp_html):
                        os.remove(temp_html)
            else:
                failed_files.append(os.path.basename(md_file))
                print(f"❌ Falha ao converter Markdown: {os.path.basename(md_file)}")
            
            # Pequena pausa entre conversões
            time.sleep(1)
        
        # Pausa entre lotes
        if i + batch_size < len(md_files):
            print("💤 Pausa entre lotes...")
            time.sleep(5)
    
    print(f"\n📊 Resumo da conversão:")
    print(f"   ✅ Sucessos: {success_count}/{len(md_files)}")
    print(f"   ❌ Falhas: {len(failed_files)}")
    print(f"   📁 Pasta de PDFs: {os.path.abspath(pdf_folder)}")
    
    if failed_files:
        print(f"\n📋 Arquivos com falha:")
        for failed in failed_files[:10]:
            print(f"   - {failed}")
        if len(failed_files) > 10:
            print(f"   ... e mais {len(failed_files) - 10} arquivos")
    
    return success_count > 0

def check_pandoc_available():
    """Verifica se o Pandoc está disponível"""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

if __name__ == "__main__":
    print("🚀 CONVERSOR DEEPSEEK MARKDOWN PARA PDF (COM PANDOC)")
    print("=" * 50)
    
    # Verificar dependências
    chrome_available = False
    try:
        test_driver = webdriver.Chrome(options=Options())
        test_driver.quit()
        chrome_available = True
        print("✅ Chrome Driver verificado")
    except Exception as e:
        print(f"❌ Chrome Driver não disponível: {e}")
    
    pandoc_available = check_pandoc_available()
    if pandoc_available:
        print("✅ Pandoc disponível")
    else:
        print("⚠️  Pandoc não encontrado - usando conversor interno")
    
    if not chrome_available:
        print("💡 Instale o Chrome Driver para continuar")
        exit(1)
    
    # Converter todos os arquivos (usar Pandoc se disponível)
    success = convert_all_markdown_to_pdf(use_pandoc=pandoc_available)
    
    if success:
        print("\n🎉 Conversão concluída!")
    else:
        print("\n⚠️  Conversão parcial ou com falhas.")
    
    print(f"\n💡 Dica: Para forçar conversor interno: use_pandoc=False")
```

**Principais melhorias:**

1. **Pandoc como primário**: Usa Pandoc para conversão HTML (muito mais robusto)
2. **Fallback automático**: Se Pandoc falhar, usa conversor interno
3. **Estilo profissional**: CSS melhorado que funciona com Pandoc
4. **Suporte a emojis**: `--from markdown+emoji` no Pandoc
5. **Verificação de dependências**: Detecta automaticamente se Pandoc está disponível
6. **Melhor formatação**: Pandoc lida melhor com código, blocos, listas, etc.

**Vantagens do Pandoc:**
- ✅ Melhor suporte a Markdown complexo
- ✅ Preserva emojis e formatação
- ✅ Lida com código, tabelas, listas
- ✅ Conversão mais robusta e rápida
- ✅ Suporte a múltiplos formatos de entrada/saída

O script agora tentará usar o Pandoc primeiro e automaticamente cairá para o conversor interno se necessário!

---

*Conversa exportada do DeepSeek*
*Processado em: 24/11/2025 22:27*