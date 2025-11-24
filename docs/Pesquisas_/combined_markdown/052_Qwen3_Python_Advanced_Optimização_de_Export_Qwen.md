# Python Advanced Optimização de Export Qwen

## 📊 Informações
- **Número:** #52
- **Origem:** Qwen3
- **Categoria:** Programação
- **ID:** 4546281d-7661-4c2d-b2b3-793b53657e4d
- **Criada em:** 2025-11-03 10:36:50
- **Atualizada em:** 2025-11-03 11:19:08
- **Total de mensagens:** 14
- **Resumo:** Tutorial Python Avançado. Pretendo uma explicação mais ou menos detalhada do file qwen_processor_opt...

---

## 💬 Conversa

### 👤 Utilizador *[Qwen3]*

Tutorial Python Avançado. Pretendo uma explicação mais ou menos detalhada do file qwen_processor_optimized.py.txt (python)

---

### 🤖 Qwen3 *[Qwen3]*

Claro! O arquivo `qwen_processor_optimized.py` é um script Python bem estruturado cujo objetivo principal é **processar um arquivo JSON de exportação de conversas do Qwen AI**, transformando essas conversas em arquivos **Markdown (.md)** organizados, além de gerar um **índice HTML pesquisável** para navegação fácil. Abaixo está uma explicação detalhada (mas clara) do seu funcionamento:

---

### 🎯 **Objetivo Geral**
Converter o histórico de conversas do Qwen AI (em formato JSON) em:
- Arquivos Markdown individuais (um por conversa)
- Um índice HTML interativo com:
  - Busca em tempo real
  - Links para abrir Markdown ou PDF (se existirem)
  - Destaque para conversas mais recentes

---

### 🔧 **Classe Principal: `QwenProcessorOptimized`**

#### **Atributos Iniciais**
```python
self.json_file = "chat-export.json"       # Arquivo de entrada
self.markdown_folder = "qwen_markdown"    # Pasta para saída Markdown
self.index_file = "qwen_index.html"       # Índice HTML gerado
self.pdf_folder = "qwen_pdfs"             # Pasta sugerida para PDFs (não gerada aqui)
self.conversations = []                   # Lista em memória das conversas processadas
```

---

### 📥 **Método Principal: `generate_complete_system()`**
Orquestra todo o fluxo:
1. Extrai conversas do JSON → `extract_qwen_conversations()`
2. Cria o índice HTML → `create_searchable_index()`
3. Abre o índice no navegador

---

### 📂 **1. Extração de Conversas (`extract_qwen_conversations`)**
- Verifica se `chat-export.json` existe.
- Carrega o JSON e valida sua estrutura (`data` deve ser uma lista).
- Para cada conversa:
  - Extrai **título**, **ID**, **timestamps** (`created_at`, `updated_at`)
  - Extrai todas as **mensagens** via `extract_messages_from_history()`
  - Filtra mensagens vazias
- **Ordena** as conversas **do mais novo para o mais antigo** usando `parse_timestamp_for_sorting()`.
- Reenumera após ordenação.
- Salva como Markdown com `save_as_markdown()`.

---

### 📝 **2. Processamento de Mensagens**
- `extract_messages_from_history()`: converte o dicionário de mensagens (com IDs como chaves) em uma **lista ordenada por timestamp**.
- `parse_message()`: monta um dicionário com:
  - `author`: "👤 Você" ou "🤖 Qwen AI (modelo)"
  - `content`: texto da mensagem
  - `timestamp`: formatado como `dd/mm/yyyy hh:mm:ss`
- `extract_content()`: lida com diferentes formatos de conteúdo (ex: `content` direto ou `content_list`).

---

### 🗂️ **3. Geração de Markdown (`save_as_markdown` + `create_markdown_content`)**
- Cada conversa vira um arquivo `.md` nomeado como:
  ```
  001_Título_da_Conversa.md
  ```
- O conteúdo inclui:
  - Título e metadados (número, ID, datas, resumo)
  - Todas as mensagens com autor e timestamp
  - Rodapé com data de processamento
- Caracteres especiais no título são removidos para evitar problemas no nome do arquivo.

---

### 🔍 **4. Índice HTML Pesquisável (`create_searchable_index`)**
Gera um arquivo `qwen_index.html` com:
- **Design moderno** (gradientes, cards, hover effects)
- **Barra de busca** que filtra conversas por título ou resumo em tempo real
- **Cards por conversa**, mostrando:
  - Número e título
  - Resumo (primeiros 100 caracteres da primeira pergunta)
  - Data e contagem de mensagens
  - Badge "NOVO" para as 3 mais recentes
- **Botões** para abrir o `.md` ou um `.pdf` (embora os PDFs não sejam gerados por este script)
- Clicar no card abre o arquivo Markdown

> ✅ O índice abre **automaticamente no navegador** após a execução.

---

### 🕒 **Tratamento de Timestamps**
O script é robusto ao lidar com diferentes formatos de data/hora:
- Unix timestamp (número)
- String ISO (`2025-03-10T14:30:00Z`)
- String legível (`10/03/2025 14:30:00`)

Usa `parse_timestamp_for_sorting()` para ordenar corretamente, mesmo com formatos mistos.

---

### 🔁 **Resumo de Conversa (`generate_summary`)**
Extrai os primeiros 100 caracteres da **primeira mensagem do usuário** como resumo. Se não houver, usa a primeira mensagem disponível.

---

### 📌 **Como Usar**
1. Tenha um arquivo `chat-export.json` no mesmo diretório.
2. Execute o script:
   ```bash
   python qwen_processor_optimized.py
   ```
3. Resultados:
   - Pasta `qwen_markdown/` com arquivos `.md`
   - Arquivo `qwen_index.html` aberto no navegador

---

### 💡 **Pontos Fortes**
- Código **bem comentado** e **modular**
- Tratamento de erros com `try/except`
- Saída limpa e organizada
- Interface HTML amigável e funcional
- Foco em **ordenação cronológica inversa** (mais recente primeiro)

---

### ⚠️ **Limitações / Observações**
- **Não gera PDFs**: só prevê uma pasta `qwen_pdfs` e links HTML para `.pdf` (você precisaria de outro script para conversão)
- Assume estrutura específica do JSON do Qwen AI (pode quebrar se o formato mudar)
- Não suporta imagens ou conteúdo rico — apenas texto

---

Se quiser, posso sugerir melhorias, como:
- Gerar PDFs automaticamente (com `markdown` + `pdfkit`)
- Adicionar exportação para CSV
- Suportar múltiplos arquivos de entrada

Deseja alguma dessas extensões?

---

### 👤 Utilizador *[Qwen3]*

Sim. Adicionar exportação para CSV, colocados numa pasta  qwen_CSV

---

### 🤖 Qwen3 *[Qwen3]*

Claro! Abaixo está a **versão atualizada da classe `QwenProcessorOptimized`** com a funcionalidade de **exportação para CSV**, incluindo:

- Uma nova pasta de saída: `qwen_csv`
- Um método `save_as_csv()` que gera um arquivo `.csv` por conversa
- Cada CSV contém as colunas: `node_id`, `author`, `role`, `timestamp`, `model`, `content`
- Integração com o fluxo principal (`generate_complete_system`)

---

### ✅ Passos realizados:
1. Adicionado atributo `self.csv_folder = "qwen_csv"`
2. Criado método `save_as_csv()`
3. Chamado esse método logo após salvar os Markdowns
4. Garantido que nomes de arquivos sejam seguros (mesma lógica do Markdown)

---

### 🔧 Trecho do código modificado e explicação

Você só precisa **substituir ou adicionar** os trechos abaixo ao seu arquivo original `qwen_processor_optimized.py`.

#### 1. Atualize o `__init__`:
```python
def __init__(self, json_file="chat-export.json"):
    self.json_file = json_file
    self.markdown_folder = "qwen_markdown"
    self.csv_folder = "qwen_csv"          # ← nova linha
    self.conversations = []
    self.index_file = "qwen_index.html"
    self.pdf_folder = "qwen_pdfs"
```

#### 2. Adicione o método `save_as_csv`:
```python
def save_as_csv(self):
    """Salva cada conversa como um arquivo CSV"""
    print(f"📤 Exportando {len(self.conversations)} conversas para CSV...")
    os.makedirs(self.csv_folder, exist_ok=True)
    import csv

    for conversation in self.conversations:
        safe_title = "".join(c for c in conversation['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:50].replace(' ', '_')
        filename = f"{conversation['number']:03d}_{safe_title}.csv"
        filepath = os.path.join(self.csv_folder, filename)

        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['node_id', 'author', 'role', 'timestamp', 'model', 'content'])
            writer.writeheader()
            for message in conversation['messages']:
                writer.writerow({
                    'node_id': message.get('node_id', ''),
                    'author': message['author'],
                    'role': message['role'],
                    'timestamp': message['timestamp'],
                    'model': message.get('model', ''),
                    'content': message['content']
                })
        print(f"✅ {filename}")
    print(f"🎉 {len(self.conversations)} arquivos CSV criados em '{self.csv_folder}'")
```

> ℹ️ Observação: o campo `author` é o nome amigável (`👤 Você` / `🤖 Qwen AI`), mas se quiser o `role` puro (`user`/`assistant`) para análise automatizada, basta usar `role` no CSV — já está incluso.

#### 3. Atualize o método `extract_qwen_conversations` para chamar `save_as_csv`:
Localize esta parte:
```python
            if self.conversations:
                self.save_as_markdown()
```

E substitua por:
```python
            if self.conversations:
                self.save_as_markdown()
                self.save_as_csv()  # ← nova linha
```

---

### 📁 Estrutura final de pastas após execução:
```
seu_diretorio/
├── chat-export.json
├── qwen_markdown/
│   ├── 001_Titulo_da_Conversa.md
│   └── ...
├── qwen_csv/
│   ├── 001_Titulo_da_Conversa.csv
│   └── ...
├── qwen_pdfs/               # (pasta não usada, mas linkada no HTML)
└── qwen_index.html
```

---

### ✅ Benefícios do CSV:
- Ideal para análise em **Python (pandas)**, **Excel**, **Google Sheets**, **Power BI**, etc.
- Estrutura tabular clara e padronizada
- Fácil filtragem por autor, data ou conteúdo

Se desejar, posso também:
- Gerar um **CSV único com todas as conversas** (com coluna de `conversation_id`)
- Incluir metadados da conversa em cada linha (ex: título, número)

Quer essa opção adicional?

---

### 👤 Utilizador *[Qwen3]*

Pretendo um file qwen_processor_optimized2.py completo com a actualização de codigo acima

---

### 🤖 Qwen3 *[Qwen3]*

Claro! Abaixo está o **arquivo completo `qwen_processor_optimized2.py`**, atualizado com a funcionalidade de **exportação para CSV** (em uma nova pasta `qwen_csv`), mantendo toda a lógica original e adicionando o suporte solicitado.

Você pode copiar e salvar este código como `qwen_processor_optimized2.py`:

```python
# qwen_processor_optimized2.py
import json
import os
import csv
from datetime import datetime
import webbrowser
import re


class QwenProcessorOptimized:
    def __init__(self, json_file="chat-export.json"):
        self.json_file = json_file
        self.markdown_folder = "qwen_markdown"
        self.csv_folder = "qwen_csv"          # Nova pasta para CSVs
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
                conversation = self.process_conversation(conv_data, i + 1)
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
                self.save_as_csv()  # ← Nova chamada para exportar CSV
            return len(self.conversations) > 0
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return False

    def save_as_csv(self):
        """Salva cada conversa como um arquivo CSV"""
        print(f"📤 Exportando {len(self.conversations)} conversas para CSV...")
        os.makedirs(self.csv_folder, exist_ok=True)

        for conversation in self.conversations:
            safe_title = "".join(c for c in conversation['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conversation['number']:03d}_{safe_title}.csv"
            filepath = os.path.join(self.csv_folder, filename)

            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['node_id', 'author', 'role', 'timestamp', 'model', 'content'])
                writer.writeheader()
                for message in conversation['messages']:
                    writer.writerow({
                        'node_id': message.get('node_id', ''),
                        'author': message['author'],
                        'role': message['role'],
                        'timestamp': message['timestamp'],
                        'model': message.get('model', ''),
                        'content': message['content']
                    })
            print(f"✅ {filename}")
        print(f"🎉 {len(self.conversations)} arquivos CSV criados em '{self.csv_folder}'")

    def parse_timestamp_for_sorting(self, timestamp):
        """Converte timestamp para objeto datetime para ordenação"""
        if not timestamp:
            return datetime.min
        try:
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
            elif isinstance(timestamp, str):
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', timestamp):
                    return datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
                elif 'T' in timestamp:
                    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
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
            chat_data = conv_data.get('chat', {})
            history = chat_data.get('history', {})
            messages_data = history.get('messages', {})
            messages = self.extract_messages_from_history(messages_data)
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
                'raw_timestamp': raw_timestamp
            }
        except Exception as e:
            print(f"⚠️  Erro ao processar conversa {number}: {e}")
            return None

    def extract_messages_from_history(self, messages_data):
        """Extrai mensagens do histórico do Qwen AI"""
        messages = []
        message_list = []
        for msg_id, msg_data in messages_data.items():
            if isinstance(msg_data, dict):
                msg_data['_id'] = msg_id
                message_list.append(msg_data)
        message_list.sort(key=lambda x: x.get('timestamp', 0))
        for msg_data in message_list:
            message = self.parse_message(msg_data)
            if message and message['content']:
                messages.append(message)
        return messages

    def parse_message(self, message_data):
        """Analisa uma mensagem do Qwen AI"""
        try:
            role = message_data.get('role', '')
            if role == 'assistant':
                author_display = '🤖 Qwen AI'
                model = message_data.get('model', '')
                if 'qwen' in model.lower():
                    model_display = f" ({model})"
                else:
                    model_display = f" ({message_data.get('modelName', '')})"
                author_display += model_display
            else:
                author_display = '👤 Você'
            content = self.extract_content(message_data)
            if not content or content.isspace():
                return None
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
        content = message_data.get('content', '')
        if not content and 'content_list' in message_
            content_list = message_data['content_list']
            if content_list and isinstance(content_list, list):
                for item in content_list:
                    if isinstance(item, dict) and 'content' in item:
                        content = item['content']
                        break
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
                return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
            elif isinstance(timestamp, str):
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', timestamp):
                    return timestamp
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
        for msg in messages:
            if msg.get('role') == 'user':
                content = msg['content']
                if len(content) > 100:
                    return content[:100] + "..."
                return content
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
        md = f"# 💬 {conversation['title']}\n"
        md += "## 📊 Informações\n"
        md += f"- **Número:** #{conversation['number']}\n"
        md += f"- **ID:** {conversation['id']}\n"
        md += f"- **Criada em:** {conversation['created_at'] or 'N/A'}\n"
        if conversation['updated_at']:
            md += f"- **Atualizada em:** {conversation['updated_at']}\n"
        md += f"- **Total de mensagens:** {conversation['message_count']}\n"
        md += f"- **Resumo:** {conversation['summary']}\n"
        md += "---\n"
        md += "## 🗨️ Conversa\n"
        for j, message in enumerate(conversation['messages'], 1):
            timestamp = f" *({message['timestamp']})*" if message['timestamp'] else ""
            model_info = f" *[{message['model']}]*" if message.get('model') else ""
            md += f"### {message['author']}{timestamp}{model_info}\n"
            content = message['content'].replace('\n', '\n')
            md += f"{content}\n"
            if j < len(conversation['messages']):
                md += "---\n"
        md += "\n---\n"
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
        for i, conv in enumerate(self.conversations):
            safe_title = "".join(c for c in conv['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conv['number']:03d}_{safe_title}.md"
            recent_badge = ""
            if i < 3:
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
        print(f"\n📋 TOP 3 MAIS RECENTES:")
        for i, conv in enumerate(self.conversations[:3]):
            print(f"   #{conv['number']}: {conv['title']} ({conv['updated_at'] or conv['created_at']})")
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')


if __name__ == "__main__":
    system = QwenProcessorOptimized()
    system.generate_complete_system()
```

---

### ✅ O que este script faz agora:
- Gera pastas:  
  - `qwen_markdown/` → `.md`  
  - `qwen_csv/` → `.csv` (um por conversa, com todas as mensagens em linha)
- Mantém o índice HTML funcional
- Abre o índice automaticamente
- Exporta dados estruturados prontos para análise

Se quiser **um único CSV com todas as conversas**, posso adicionar isso também — é só pedir!

---

### 👤 Utilizador *[Qwen3]*

sim. Tambem um único CSV com todas as conversas

---

### 🤖 Qwen3 *[Qwen3]*

Perfeito! Abaixo está o **arquivo completo `qwen_processor_optimized2.py`**, atualizado com **duas funcionalidades de exportação CSV**:

1. ✅ **Um CSV por conversa** (na pasta `qwen_csv/`)  
2. ✅ **Um CSV único com todas as conversas** (arquivo `qwen_all_conversations.csv` na raiz)

Todos os dados estão estruturados com as colunas:  
`conversation_number`, `conversation_title`, `node_id`, `author`, `role`, `timestamp`, `model`, `content`

---

### ✅ O que foi adicionado:
- Método `save_all_conversations_to_single_csv()`
- Chamada desse método em `extract_qwen_conversations()`
- Atributo `self.single_csv_file = "qwen_all_conversations.csv"`

---

### 📄 Código final (`qwen_processor_optimized2.py`):

```python
# qwen_processor_optimized2.py
import json
import os
import csv
from datetime import datetime
import webbrowser
import re


class QwenProcessorOptimized:
    def __init__(self, json_file="chat-export.json"):
        self.json_file = json_file
        self.markdown_folder = "qwen_markdown"
        self.csv_folder = "qwen_csv"
        self.single_csv_file = "qwen_all_conversations.csv"  # novo
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
            self.conversations = []
            for i, conv_data in enumerate(conversations_data):
                conversation = self.process_conversation(conv_data, i + 1)
                if conversation and conversation['messages']:
                    self.conversations.append(conversation)
                    print(f"✅ {i+1:02d}: '{conversation['title']}' - {len(conversation['messages'])} mensagens")
                else:
                    print(f"⚠️  {i+1:02d}: '{conv_data.get('title', 'Sem título')}' - SEM MENSAGENS")
            print("🔄 Ordenando conversas do mais novo para o mais antigo...")
            self.conversations.sort(key=lambda x: self.parse_timestamp_for_sorting(
                x.get('raw_timestamp')
            ), reverse=True)
            for i, conv in enumerate(self.conversations):
                conv['number'] = i + 1
            print(f"📊 Total de conversas com mensagens: {len(self.conversations)}")
            if self.conversations:
                self.save_as_markdown()
                self.save_as_csv()
                self.save_all_conversations_to_single_csv()  # novo
            return len(self.conversations) > 0
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return False

    def save_as_csv(self):
        """Salva cada conversa como um arquivo CSV separado"""
        print(f"📤 Exportando {len(self.conversations)} conversas individuais para CSV...")
        os.makedirs(self.csv_folder, exist_ok=True)
        for conversation in self.conversations:
            safe_title = "".join(c for c in conversation['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conversation['number']:03d}_{safe_title}.csv"
            filepath = os.path.join(self.csv_folder, filename)
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['node_id', 'author', 'role', 'timestamp', 'model', 'content'])
                writer.writeheader()
                for message in conversation['messages']:
                    writer.writerow({
                        'node_id': message.get('node_id', ''),
                        'author': message['author'],
                        'role': message['role'],
                        'timestamp': message['timestamp'],
                        'model': message.get('model', ''),
                        'content': message['content']
                    })
            print(f"✅ {filename}")
        print(f"🎉 {len(self.conversations)} arquivos CSV criados em '{self.csv_folder}'")

    def save_all_conversations_to_single_csv(self):
        """Salva todas as conversas em um único arquivo CSV"""
        print("📊 Exportando todas as conversas para um único CSV...")
        fieldnames = [
            'conversation_number',
            'conversation_title',
            'node_id',
            'author',
            'role',
            'timestamp',
            'model',
            'content'
        ]
        with open(self.single_csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for conv in self.conversations:
                for msg in conv['messages']:
                    writer.writerow({
                        'conversation_number': conv['number'],
                        'conversation_title': conv['title'],
                        'node_id': msg.get('node_id', ''),
                        'author': msg['author'],
                        'role': msg['role'],
                        'timestamp': msg['timestamp'],
                        'model': msg.get('model', ''),
                        'content': msg['content']
                    })
        print(f"✅ Arquivo único criado: {self.single_csv_file}")

    # ========== Métodos auxiliares (sem alterações) ==========

    def parse_timestamp_for_sorting(self, timestamp):
        if not timestamp:
            return datetime.min
        try:
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
            elif isinstance(timestamp, str):
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', timestamp):
                    return datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
                elif 'T' in timestamp:
                    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    try:
                        return datetime.fromtimestamp(float(timestamp))
                    except:
                        pass
        except Exception as e:
            print(f"⚠️  Erro ao converter timestamp '{timestamp}': {e}")
        return datetime.min

    def process_conversation(self, conv_data, number):
        try:
            title = conv_data.get('title', f'Conversa {number}')
            conv_id = conv_data.get('id', f'conv_{number}')
            created_at = conv_data.get('created_at')
            updated_at = conv_data.get('updated_at')
            chat_data = conv_data.get('chat', {})
            history = chat_data.get('history', {})
            messages_data = history.get('messages', {})
            messages = self.extract_messages_from_history(messages_data)
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
                'raw_timestamp': raw_timestamp
            }
        except Exception as e:
            print(f"⚠️  Erro ao processar conversa {number}: {e}")
            return None

    def extract_messages_from_history(self, messages_data):
        messages = []
        message_list = []
        for msg_id, msg_data in messages_data.items():
            if isinstance(msg_data, dict):
                msg_data['_id'] = msg_id
                message_list.append(msg_data)
        message_list.sort(key=lambda x: x.get('timestamp', 0))
        for msg_data in message_list:
            message = self.parse_message(msg_data)
            if message and message['content']:
                messages.append(message)
        return messages

    def parse_message(self, message_data):
        try:
            role = message_data.get('role', '')
            if role == 'assistant':
                author_display = '🤖 Qwen AI'
                model = message_data.get('model', '')
                if 'qwen' in model.lower():
                    model_display = f" ({model})"
                else:
                    model_display = f" ({message_data.get('modelName', '')})"
                author_display += model_display
            else:
                author_display = '👤 Você'
            content = self.extract_content(message_data)
            if not content or content.isspace():
                return None
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
        content = message_data.get('content', '')
        if not content and 'content_list' in message_
            content_list = message_data['content_list']
            if content_list and isinstance(content_list, list):
                for item in content_list:
                    if isinstance(item, dict) and 'content' in item:
                        content = item['content']
                        break
        if isinstance(content, str):
            return content.strip()
        elif isinstance(content, (list, dict)):
            return str(content)
        return ''

    def format_timestamp(self, timestamp):
        if not timestamp:
            return None
        try:
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
            elif isinstance(timestamp, str):
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', timestamp):
                    return timestamp
                elif 'T' in timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return dt.strftime('%d/%m/%Y %H:%M:%S')
        except:
            pass
        return str(timestamp)

    def generate_summary(self, messages):
        if not messages:
            return "Sem conteúdo"
        for msg in messages:
            if msg.get('role') == 'user':
                content = msg['content']
                if len(content) > 100:
                    return content[:100] + "..."
                return content
        first_msg = messages[0]['content']
        if len(first_msg) > 100:
            return first_msg[:100] + "..."
        return first_msg

    def save_as_markdown(self):
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
        md = f"# 💬 {conversation['title']}\n"
        md += "## 📊 Informações\n"
        md += f"- **Número:** #{conversation['number']}\n"
        md += f"- **ID:** {conversation['id']}\n"
        md += f"- **Criada em:** {conversation['created_at'] or 'N/A'}\n"
        if conversation['updated_at']:
            md += f"- **Atualizada em:** {conversation['updated_at']}\n"
        md += f"- **Total de mensagens:** {conversation['message_count']}\n"
        md += f"- **Resumo:** {conversation['summary']}\n"
        md += "---\n"
        md += "## 🗨️ Conversa\n"
        for j, message in enumerate(conversation['messages'], 1):
            timestamp = f" *({message['timestamp']})*" if message['timestamp'] else ""
            model_info = f" *[{message['model']}]*" if message.get('model') else ""
            md += f"### {message['author']}{timestamp}{model_info}\n"
            content = message['content'].replace('\n', '\n')
            md += f"{content}\n"
            if j < len(conversation['messages']):
                md += "---\n"
        md += "\n---\n"
        md += "*Conversa exportada do Qwen AI*  \n"
        md += f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        return md

    def create_searchable_index(self):
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
        for i, conv in enumerate(self.conversations):
            safe_title = "".join(c for c in conv['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50].replace(' ', '_')
            filename = f"{conv['number']:03d}_{safe_title}.md"
            recent_badge = ""
            if i < 3:
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
        print(f"📁 Pastas geradas:")
        print(f"   - {self.markdown_folder}/")
        print(f"   - {self.csv_folder}/")
        print(f"📄 Arquivos extras:")
        print(f"   - {self.single_csv_file}")
        print(f"\n📋 TOP 3 MAIS RECENTES:")
        for i, conv in enumerate(self.conversations[:3]):
            print(f"   #{conv['number']}: {conv['title']} ({conv['updated_at'] or conv['created_at']})")
        if os.path.exists(self.index_file):
            webbrowser.open(f'file://{os.path.abspath(self.index_file)}')


if __name__ == "__main__":
    system = QwenProcessorOptimized()
    system.generate_complete_system()
```

---

### 📂 Resultado após execução:
```
.
├── chat-export.json
├── qwen_markdown/           → .md por conversa
├── qwen_csv/                → .csv por conversa
├── qwen_all_conversations.csv  → ÚNICO CSV com tudo
├── qwen_index.html
└── qwen_pdfs/               → (não usado, mas linkado)
```

Pronto para análise em **pandas**, **Excel**, **Power BI**, etc.!

Se quiser incluir campos extras (ex: data da conversa, ID completo, etc.) no CSV único, posso ajustar. Deseja isso?

---

### 👤 Utilizador *[Qwen3]*

Ok. Por agora estou satisfeito com o resultado. Agora pretendo uma analise do file qwen_pdf_converter_optimized.py.txt (python)

---

### 🤖 Qwen3 *[Qwen3]*

Claro! Abaixo está uma **análise detalhada do arquivo `qwen_pdf_converter_optimized.py`**, cujo propósito é converter os arquivos Markdown gerados pelo `qwen_processor_optimized.py` em **PDFs de alta qualidade, legíveis e com bom contraste**, usando uma abordagem robusta e otimizada.

---

## 🎯 **Objetivo Geral**
Converter arquivos Markdown (`.md`) do histórico do Qwen AI em PDFs:
- Visualmente agradáveis
- Com **contraste máximo** (preto sobre branco)
- Preservando formatação (títulos, código, mensagens, etc.)
- Com suporte a fórmulas matemáticas (via MathJax)
- Com fallback caso dependências faltem

---

## 🔧 **Arquitetura e Fluxo Principal**

### Classe: `PDFConverterOptimized`
Gerencia todo o processo de conversão em lote.

#### Atributos:
```python
self.md_dir = "qwen_markdown"   # Pasta de entrada (Markdown)
self.pdf_dir = "qwen_pdfs"      # Pasta de saída (PDF)
self.batch_size = 3             # Lote para pausas (evitar sobrecarga)
```

#### Fluxo de Execução (`convert_batch()`):
1. **Verifica dependências** (`pandoc`, `selenium`, `ChromeDriver`)
2. Lista todos os `.md` em `qwen_markdown/`
3. Para cada arquivo:
   - Verifica se PDF já existe → pula se sim
   - Converte `.md` → HTML (com `pandoc` ou fallback)
   - Converte HTML → PDF (usando **Selenium + Chrome DevTools Protocol**)
   - Salva em `qwen_pdfs/`
4. Pausa a cada 3 conversões (para estabilidade)

---

## 🔌 **Dependências Verificadas**

O script verifica **três componentes essenciais**:

| Dependência      | Finalidade |
|------------------|-----------|
| **Pandoc**       | Conversão avançada de Markdown → HTML (com suporte a emojis, MathJax, etc.) |
| **Selenium**     | Automação do navegador para renderização fiel |
| **ChromeDriver** | Interface entre Selenium e o Chrome (necessária para `printToPDF`) |

> ✅ Se faltar algo, o script **explica como instalar** em cada sistema (Linux, macOS, Windows).

---

## 📄 **Conversão Markdown → HTML**

### 1. **Modo Principal: `pandoc`**
- Usa linha de comando:  
  ```bash
  pandoc arquivo.md --from markdown+emoji --to html --standalone --mathjax
  ```
- Aplica um **template HTML personalizado** com:
  - Cores forçadas para **preto (#000000)** em todos os elementos
  - Fundo branco garantido
  - Estilos diferenciados para:
    - Mensagens do usuário (azul claro)
    - Respostas do Qwen (roxo claro)
    - Código (fundo escuro, texto branco)
  - Suporte a impressão (`@media print`)
  - Cabeçalho e rodapé com metadados

### 2. **Modo Fallback: Conversão manual**
Se o Pandoc falhar:
- Usa um conversor simples baseado em regex/string
- Reconhece:
  - Títulos (`#`, `##`, `###`)
  - Mensagens com "👤 Você" / "🤖 Qwen AI"
  - Blocos de código (```)
  - Linhas horizontais (`---`)
- Aplica **mesmas regras de contraste**
- Menos rico, mas funcional

> 💡 **Destaque**: O script prioriza **legibilidade em PDF**, forçando `color: #000000 !important` em **todos os elementos**, evitando o problema comum de textos cinza/branco que somem ao imprimir.

---

## 🖨️ **Conversão HTML → PDF**

### Método: `html_to_pdf_selenium()`
- Usa **Chrome em modo headless** via Selenium
- Cria um **arquivo HTML temporário**
- Carrega no navegador
- Usa o comando do **Chrome DevTools Protocol**:  
  `Page.printToPDF`
- Configurações otimizadas:
  ```python
  'printBackground': True,     # Fundos de cor são impressos
  'preferCSSPageSize': True,   # Respeita o tamanho do CSS
  'paperWidth': 8.27,          # A4 em polegadas
  'paperHeight': 11.69,
  'margins': 0.4 polegadas
  ```
- Converte o resultado (base64) em arquivo `.pdf`
- Remove o HTML temporário

> ✅ Vantagem: renderização **exata** do que o usuário vê no navegador  
> ⚠️ Requer Chrome instalado e ChromeDriver compatível

---

## 🛡️ **Robustez e Tratamento de Erros**

- **Timeouts**: Pandoc tem limite de 30s
- **Fallback automático**: se Pandoc falhar, usa conversor simples
- **Verificação de existência**: não sobrescreve PDFs existentes
- **Pausas entre lotes**: evita travamentos em máquinas com pouca RAM
- **Mensagens claras**: cada etapa mostra ✅ ou ❌

---

## 📁 **Estrutura Esperada e Resultado**

**Entrada**:
```
qwen_markdown/
├── 001_Consulta_sobre_saúde.md
├── 002_Dicas_de_programação.md
└── ...
```

**Saída**:
```
qwen_pdfs/
├── 001_Consulta_sobre_saúde.pdf
├── 002_Dicas_de_programação.pdf
└── ...
```

Cada PDF inclui:
- Cabeçalho com título
- Diferenciação clara entre você e o Qwen
- Código legível
- Fórmulas matemáticas (se usadas)
- Data de geração
- Margens adequadas para impressão

---

## ⚙️ **Pontos Fortes**

| Característica | Benefício |
|----------------|----------|
| **Forçar contraste máximo** | Evita PDFs ilegíveis (problema comum em conversões) |
| **Uso do CDP do Chrome** | PDFs com fidelidade visual alta |
| **Fallback inteligente** | Funciona mesmo sem Pandoc |
| **Lotes com pausa** | Estável em grandes conjuntos |
| **Template modular** | Estilo consistente e profissional |

---

## ⚠️ **Limitações Potenciais**

1. **Dependência do Chrome**: não funciona em ambientes sem navegador (ex: servidores Linux headless sem Chrome).
2. **Tamanho dos PDFs**: podem ser maiores devido ao uso de imagens base64 ou fontes embutidas.
3. **Performance**: conversão 1 a 1 é mais lenta que bibliotecas como `weasyprint` ou `pdfkit`, mas mais fiel.
4. **Reconhecimento de mensagens no fallback**: baseado em strings ("👤 Você"), o que pode falhar se o formato do Markdown mudar.

---

## 🚀 **Sugestões Futuras (opcionais)**

- Adicionar opção para usar `wkhtmltopdf` como alternativa ao Selenium
- Permitir configuração de tema (claro/escuro) via argumento
- Incluir metadados do PDF (título, autor) via `--metadata`
- Compactar PDFs após geração (ex: com `ghostscript`)

---

Se desejar, posso gerar uma versão **lightweight** (sem Selenium) ou uma que gere **um único PDF com todas as conversas**. Basta pedir!

---

### 👤 Utilizador *[Qwen3]*

Verifica se PDF já existe → pula se sim; acrescentar uma opção que possar forçar a substitução de pdf existente. A nova versão deve ter o nome de qwen_pdf_converter_optimized2.py

---

### 🤖 Qwen3 *[Qwen3]*

Claro! Abaixo está a **versão atualizada** do script com o nome **`qwen_pdf_converter_optimized2.py`**, incluindo uma **nova opção para forçar a substituição de PDFs já existentes**.

A implementação adiciona:
- Um parâmetro opcional `force=False` na classe `PDFConverterOptimized`
- Um argumento de linha de comando (`--force`) para ativar a substituição
- Verificação condicional no loop de conversão

---

### ✅ Arquivo completo: `qwen_pdf_converter_optimized2.py`

```python
# qwen_pdf_converter_optimized2.py
import os
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile
import sys
import time
import base64
import argparse  # ← Novo: para suportar --force
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class PDFConverterOptimized:
    def __init__(self, force=False):
        self.md_dir = "qwen_markdown"
        self.pdf_dir = "qwen_pdfs"
        self.batch_size = 3
        self.force = force  # ← Nova flag

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
        try:
            import selenium
            print("✅ Selenium: Disponível")
            return True
        except ImportError:
            print("❌ Selenium não instalado")
            return False

    def check_chrome_driver(self):
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
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
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
        try:
            html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{TITLE}}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {
            color: #000000 !important;
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            line-height: 1.6;
            color: #000000 !important;
            background: #ffffff !important;
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
            color: #000000 !important;
            border-bottom: 2px solid #3498db; 
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h1 { color: #000000 !important; font-size: 28px; }
        h2 { color: #000000 !important; font-size: 24px; border-bottom: 1px solid #3498db; }
        h3 { color: #000000 !important; font-size: 20px; }
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
            color: #ffffff !important;
            padding: 2px 6px; 
            border-radius: 4px; 
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }
        pre { 
            background: #2c3e50 !important; 
            color: #ffffff !important;
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
        window.onload = function() {
            document.querySelectorAll('*').forEach(el => {
                el.style.color = '#000000';
                el.style.backgroundColor = el.classList.contains('header') ? '' : '#ffffff';
            });
        };
    </script>
</body>
</html>"""
            result = subprocess.run([
                'pandoc', str(md_file),
                '--from', 'markdown+emoji',
                '--to', 'html',
                '--standalone',
                '--mathjax'
            ], capture_output=True, text=True, encoding='utf-8', timeout=30)
            if result.returncode == 0:
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
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            html_content = self.simple_markdown_to_html(markdown_content, md_file.stem)
            return html_content
        except Exception as e:
            print(f"❌ Erro no fallback: {e}")
            return None

    def simple_markdown_to_html(self, markdown_text, title):
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
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
        lines = text.split('\n')
        html_lines = []
        for line in lines:
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif '👤 Você' in line or '🤖 Qwen AI' in line:
                if '👤 Você' in line:
                    html_lines.append(f'<div class="message user"><strong>{line}</strong></div>')
                else:
                    html_lines.append(f'<div class="message assistant"><strong>{line}</strong></div>')
            elif line.strip().startswith('```'):
                html_lines.append('<pre><code>')
            elif line.strip() == '```':
                html_lines.append('</code></pre>')
            elif line.strip() == '---':
                html_lines.append('<hr>')
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('<br>')
        return '\n'.join(html_lines)

    def html_to_pdf_selenium(self, html_content, pdf_path):
        driver = None
        try:
            driver = self.setup_chrome_driver()
            if not driver:
                return False
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html = f.name
            driver.get(f'file://{temp_html}')
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print_options = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'paperWidth': 8.27,
                'paperHeight': 11.69,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
                'scale': 1.0
            }
            result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
            pdf_data = base64.b64decode(result['data'])
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
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

        mode = "FORÇANDO SUBSTITUIÇÃO" if self.force else "PULANDO EXISTENTES"
        print(f"🔄 Modo: {mode}")
        print(f"📁 Encontrados {len(md_files)} arquivos .md")
        print(f"📊 Tamanho do lote: {self.batch_size}")
        print(f"📁 PDFs serão salvos em: {self.pdf_dir}")

        successful = 0
        failed = 0
        for i, md_file in enumerate(md_files):
            print(f"\n🔄 [{i+1}/{len(md_files)}] Convertendo: {md_file.name}")
            pdf_filename = md_file.stem + '.pdf'
            pdf_path = Path(self.pdf_dir) / pdf_filename

            # ←←← VERIFICAÇÃO ATUALIZADA
            if pdf_path.exists() and not self.force:
                print(f"   ⏭️  PDF já existe, pulando...")
                successful += 1
                continue
            elif pdf_path.exists() and self.force:
                print(f"   ♻️  PDF existente será substituído...")

            try:
                html_content = self.convert_with_pandoc_optimized(md_file)
                if not html_content:
                    print(f"   ❌ Falha na conversão HTML")
                    failed += 1
                    continue
                if self.html_to_pdf_selenium(html_content, pdf_path):
                    print(f"   ✅ PDF criado: {pdf_filename}")
                    successful += 1
                else:
                    print(f"   ❌ Falha na conversão PDF")
                    failed += 1
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
    parser = argparse.ArgumentParser(description="Converte conversas Qwen (.md) em PDFs otimizados.")
    parser.add_argument('--force', action='store_true', help="Força a substituição de PDFs já existentes")
    args = parser.parse_args()

    converter = PDFConverterOptimized(force=args.force)
    converter.convert_batch()
```

---

### 🚀 Como usar:

- **Modo padrão** (pula PDFs existentes):
  ```bash
  python qwen_pdf_converter_optimized2.py
  ```

- **Modo forçado** (recria todos os PDFs):
  ```bash
  python qwen_pdf_converter_optimized2.py --force
  ```

---

### ✅ Benefícios:
- Mantém toda a lógica original (contraste, fallback, Pandoc, Selenium)
- Adiciona controle explícito sobre sobrescrita
- Interface de linha de comando limpa e autoexplicativa

Se quiser, posso também adicionar opções como:
- `--only-new` (só converter .md sem .pdf correspondente)
- `--single <file.md>` (converter só um arquivo)

Deseja algo assim?

---

### 👤 Utilizador *[Qwen3]*

sim. Pretendo esta opção: --only-new (só converter .md sem .pdf correspondente)

---

### 🤖 Qwen3 *[Qwen3]*

Perfeito! Abaixo está a **versão atualizada do script `qwen_pdf_converter_optimized2.py`**, agora com **duas opções de linha de comando**:

- `--force` → **substitui** PDFs já existentes  
- `--only-new` → **converte apenas** os `.md` que **não têm** `.pdf` correspondente (comportamento padrão, mas agora explícito)

> ✅ Por padrão (sem argumentos), o script usa o modo **`--only-new`** (ou seja, pula PDFs existentes).  
> 🔁 `--force` sobrepõe qualquer PDF existente.  
> ❌ Os dois argumentos são **mutuamente exclusivos** (não podem ser usados juntos).

---

### 📄 Arquivo: `qwen_pdf_converter_optimized2.py`

```python
# qwen_pdf_converter_optimized2.py
import os
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile
import time
import base64
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class PDFConverterOptimized:
    def __init__(self, mode='only_new'):
        """
        mode: 'only_new' (padrão), 'force'
        """
        self.md_dir = "qwen_markdown"
        self.pdf_dir = "qwen_pdfs"
        self.batch_size = 3
        self.mode = mode

    def check_dependencies(self):
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
        try:
            import selenium
            print("✅ Selenium: Disponível")
            return True
        except ImportError:
            print("❌ Selenium não instalado")
            return False

    def check_chrome_driver(self):
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
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
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
        try:
            html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{TITLE}}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * { color: #000000 !important; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            line-height: 1.6;
            color: #000000 !important;
            background: #ffffff !important;
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
            color: #000000 !important;
            border-bottom: 2px solid #3498db; 
            padding-bottom: 8px;
            margin-top: 30px;
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
            color: #ffffff !important;
            padding: 2px 6px; 
            border-radius: 4px; 
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }
        pre { 
            background: #2c3e50 !important; 
            color: #ffffff !important;
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
        table { border-collapse: collapse; width: 100%; margin: 20px 0; background: #ffffff !important; color: #000000 !important; }
        th, td { border: 2px solid #3498db !important; padding: 12px; text-align: left; color: #000000 !important; }
        th { background-color: #e8f4fd !important; color: #000000 !important; font-weight: bold; }
        td { background-color: #ffffff !important; color: #000000 !important; }
        p, div, span, li { color: #000000 !important; }
        strong, b { color: #000000 !important; font-weight: bold; }
        em, i { color: #000000 !important; font-style: italic; }
        a { color: #0066cc !important; text-decoration: underline; }
        @media print {
            * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color: #000000 !important; }
            body { background: white !important; color: black !important; }
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
        window.onload = function() {
            document.querySelectorAll('*').forEach(el => {
                el.style.color = '#000000';
                el.style.backgroundColor = el.classList.contains('header') ? '' : '#ffffff';
            });
        };
    </script>
</body>
</html>"""
            result = subprocess.run([
                'pandoc', str(md_file),
                '--from', 'markdown+emoji',
                '--to', 'html',
                '--standalone',
                '--mathjax'
            ], capture_output=True, text=True, encoding='utf-8', timeout=30)
            if result.returncode == 0:
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
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            html_content = self.simple_markdown_to_html(markdown_content, md_file.stem)
            return html_content
        except Exception as e:
            print(f"❌ Erro no fallback: {e}")
            return None

    def simple_markdown_to_html(self, markdown_text, title):
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
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
        lines = text.split('\n')
        html_lines = []
        for line in lines:
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif '👤 Você' in line or '🤖 Qwen AI' in line:
                if '👤 Você' in line:
                    html_lines.append(f'<div class="message user"><strong>{line}</strong></div>')
                else:
                    html_lines.append(f'<div class="message assistant"><strong>{line}</strong></div>')
            elif line.strip().startswith('```'):
                html_lines.append('<pre><code>')
            elif line.strip() == '```':
                html_lines.append('</code></pre>')
            elif line.strip() == '---':
                html_lines.append('<hr>')
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('<br>')
        return '\n'.join(html_lines)

    def html_to_pdf_selenium(self, html_content, pdf_path):
        driver = None
        try:
            driver = self.setup_chrome_driver()
            if not driver:
                return False
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html = f.name
            driver.get(f'file://{temp_html}')
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print_options = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'paperWidth': 8.27,
                'paperHeight': 11.69,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
                'scale': 1.0
            }
            result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
            pdf_data = base64.b64decode(result['data'])
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
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
        print("🚀 INICIANDO CONVERSÃO EM LOTE")
        print("=" * 50)
        if not self.check_dependencies():
            print("\n❌ Dependências não atendidas.")
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

        mode_desc = {
            'only_new': "CONVERTER APENAS NOVOS (.md sem .pdf)",
            'force': "FORÇAR SUBSTITUIÇÃO DE TODOS OS PDFs"
        }
        print(f"🔄 Modo: {mode_desc[self.mode]}")
        print(f"📁 Encontrados {len(md_files)} arquivos .md")
        print(f"📁 Saída: {self.pdf_dir}")

        successful = 0
        failed = 0
        for i, md_file in enumerate(md_files):
            pdf_path = Path(self.pdf_dir) / (md_file.stem + '.pdf')

            # Lógica de decisão principal
            should_skip = False
            if self.mode == 'only_new' and pdf_path.exists():
                print(f"   ⏭️  [{i+1}/{len(md_files)}] {md_file.name} → PDF já existe, pulando...")
                successful += 1
                continue
            elif self.mode == 'force':
                if pdf_path.exists():
                    print(f"   ♻️  [{i+1}/{len(md_files)}] {md_file.name} → Substituindo PDF existente...")
                else:
                    print(f"   🆕 [{i+1}/{len(md_files)}] {md_file.name} → Criando novo PDF...")

            try:
                html_content = self.convert_with_pandoc_optimized(md_file)
                if not html_content:
                    print(f"   ❌ [{i+1}] Falha na conversão HTML")
                    failed += 1
                    continue
                if self.html_to_pdf_selenium(html_content, pdf_path):
                    print(f"   ✅ [{i+1}] PDF criado: {pdf_path.name}")
                    successful += 1
                else:
                    print(f"   ❌ [{i+1}] Falha na conversão PDF")
                    failed += 1
                if (i + 1) % self.batch_size == 0 and i + 1 < len(md_files):
                    print("\n⏸️  Pausa de 2 segundos...")
                    time.sleep(2)
            except Exception as e:
                print(f"   ❌ [{i+1}] Erro inesperado: {e}")
                failed += 1

        print(f"\n🎉 CONVERSÃO CONCLUÍDA!")
        print(f"✅ Sucessos: {successful}")
        print(f"❌ Falhas: {failed}")

        if successful > 0:
            print(f"\n📋 PDFs no diretório '{self.pdf_dir}':")
            for pdf in Path(self.pdf_dir).glob("*.pdf"):
                size_kb = pdf.stat().st_size / 1024
                print(f"   📄 {pdf.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converte conversas Qwen (.md) em PDFs otimizados.",
        epilog="Exemplo: python qwen_pdf_converter_optimized2.py --only-new"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Força a substituição de PDFs já existentes")
    group.add_argument('--only-new', action='store_true', help="Converte apenas arquivos sem PDF correspondente (padrão)")

    args = parser.parse_args()

    # Define modo: --only-new é o padrão se nenhum for especificado
    if args.force:
        mode = 'force'
    else:
        mode = 'only_new'  # inclui caso --only-new seja usado ou nenhum argumento

    converter = PDFConverterOptimized(mode=mode)
    converter.convert_batch()
```

---

### ✅ Como usar:

```bash
# Modo padrão (equivalente a --only-new)
python qwen_pdf_converter_optimized2.py

# Explícito: só converter os que ainda não têm PDF
python qwen_pdf_converter_optimized2.py --only-new

# Forçar reconversão de todos
python qwen_pdf_converter_optimized2.py --force
```

> 📌 **Observação**: os argumentos `--force` e `--only-new` **não podem ser usados juntos** (o script impede isso com `add_mutually_exclusive_group`).

Se quiser adicionar mais opções (ex: `--single <arquivo.md>`), posso implementar também!

---

*Conversa exportada do Qwen3*
*Processado em: 24/11/2025 22:27*