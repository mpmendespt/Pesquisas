# Combined Fragments System comb_fragments_system4_html_export.py 2

## 📊 Informações
- **Número:** #20
- **Origem:** DeepSeek
- **Categoria:** Outros
- **ID:** 5d283780-dc00-4bac-9e1d-10aaea5c2bdf
- **Criada em:** 2025-11-08 06:10:01
- **Atualizada em:** 2025-11-08 08:04:13
- **Total de mensagens:** 16
- **Resumo:** Aqui está...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-08 06:10:04)* *[deepseek-reasoner]*

Aqui está

---

### 🤖 DeepSeek *(2025-11-08 06:10:04)* *[deepseek-reasoner]*

Vamos extrair o comando final em uma única linha, sem quebras, que foi discutido no histórico de conversa.

No histórico, o usuário pediu para converter o arquivo `exemplo_completo3.md` para HTML usando Pandoc, com várias opções para preservar o conteúdo (fórmulas matemáticas, código, emojis, etc.) e que o comando fosse apresentado em uma única linha, sem usar a barra invertida para quebras.

O comando final em uma única linha, que atende a essas necessidades, é:

```bash
pandoc exemplo_completo3.md --standalone --mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js --embed-resources --syntax-highlighting=pygments --to=html5 -o exemplo_completo3.html
```

Este comando:
- Usa `--standalone` para gerar um documento HTML completo.
- Usa `--mathjax` com uma URL específica para renderizar fórmulas matemáticas.
- Usa `--embed-resources` para incorporar CSS, JavaScript e outros recursos no arquivo HTML.
- Usa `--syntax-highlighting=pygments` para realce de sintaxe do código (substitui o `--highlight-style` obsoleto).
- Usa `--to=html5` para gerar HTML

---

### 👤 Utilizador *(2025-11-08 06:11:24)* *[deepseek-reasoner]*

A questão é https://chat.deepseek.com/a/chat/s/bbc9c651-5f18-4138-8cc0-8b1107919c28   e  https://chat.deepseek.com/a/chat/s/29e5a40c-3d03-4dd2-82df-68f392158534

---

### 🤖 DeepSeek *(2025-11-08 06:11:24)* *[deepseek-reasoner]*

First, the user has provided two links to DeepSeek chats. I need to understand what the question is. Since the links are from DeepSeek, I should assume that the user wants me to refer to those chats or perhaps summarize or continue from them. But I don't have access to those links directly because they are specific to the DeepSeek platform. As an AI, I can only work with the text provided.

The user said: "A questão é" which means "The question is" in Portuguese, and then provided two URLs. But the URLs are not the question itself; they point to previous chats. I need to infer what the user is asking.

Perhaps the user wants me to look at those chats and answer based on them, but since I can't access them, I might need to ask for more information. However, the user might have copied the content from those chats into this message, but in this case, only the links are provided.

Let me check the links: they are from "chat.deepseek.com" which is the platform I'm on, but as an AI, I don't have browsing capabilities to open those links. My system prompt says I can only process text and files uploaded by the user.

So, I should respond by stating that I cannot access external links and request that the user paste the relevant content from those chats here.

But let's think about the context. The user might be referring to previous conversations we had, but since this is a new session, I don't have memory of those chats. The links might be to other chats that the user had with me, but in this instance, I don't have access to that history.

Therefore, the best approach is to politely explain that I cannot access the links and ask the user to provide the question or the content directly.

My response should be in Portuguese since the user started in Portuguese.

So, I'll say: "Desculpe, mas não consigo acessar links externos. Por favor, copie e cole o conteúdo das conversas ou me diga qual é a sua pergunta diretamente aqui."

That means: "Sorry, but I cannot access external links. Please copy and paste the content of the conversations or tell me your question directly here."

This seems reasonable. I don't want to assume anything about the question without more information. Desculpe, mas não consigo acessar links externos, incluindo os que você forneceu do chat.deepseek.com. Como assistente de IA, só posso processar textos e arquivos enviados diretamente aqui.

Para que eu possa ajudá-lo, por favor, copie e cole o conteúdo relevante dessas conversas ou me diga qual é a sua pergunta diretamente nesta mensagem. Estou aqui para ajudar!

---

### 👤 Utilizador *(2025-11-08 06:12:57)* *[deepseek-reasoner]*

Continuando a analise anterior. Pretende-se a correcção relativa a Qwen on algumas partes das conversa não aparecem. Mas pretende-se manter todas as outras funcionalidades que funcionam bem, com deepseek, chatgpt ou grok.

---

### 🤖 DeepSeek *(2025-11-08 06:12:57)* *[deepseek-reasoner]*

Vamos focar na correção do processador Qwen, mantendo as outras funcionalidades intactas.
 O problema reportado é que algumas partes das conversas do Qwen não aparecem.

 Analisando o código, o método `process_qwen_enhanced` é responsável por processar o Qwen.
 Nele, há uma chamada para `_extract_all_qwen_messages` que usa múltiplas estratégias para extrair mensagens.

 No entanto, notei que na estratégia 1 (Histórico de chat) há uma sub-estratégia 1A que extrai mensagens de um dicionário e 1B de uma lista.
 Mas observei que a função `_extract_from_messages_dict` e `_extract_from_messages_list` podem não estar capturando toda a estrutura.

 Além disso, notei que o método `_process_qwen_content` pode não estar lidando com todos os tipos de conteúdo, especialmente quando o conteúdo é uma lista de blocos.

 Vamos revisar a função `_process_qwen_content` para garantir que está extraindo todo o texto dos blocos.

 Outro ponto: a função `_extract_all_qwen_messages` pode não estar considerando todas as possíveis localizações das mensagens.

 Vamos também adicionar mais logs para debug e tentar extrair de mais locais.

 No entanto, como o problema é específico do Qwen e não queremos afetar os outros, vamos focar apenas no processador Qwen.

 Proposta de alterações:

 1. Melhorar a função `_process_qwen_content` para lidar com todos os tipos de blocos que podem aparecer no Qwen.
    Atualmente, ela só processa blocos do tipo 'text' e 'image'. Vamos tentar extrair texto de qualquer bloco que tenha um campo 'text' ou 'content'.

 2. Na extração de mensagens, vamos também tentar extrair de mais campos, como 'content' direto da mensagem, além de 'parts'.

 3. Vamos adicionar uma estratégia de fallback que tenta extrair mensagens de qualquer campo que seja uma lista e que contenha objetos com 'role' e 'content'.

 4. Vamos também melhorar a remoção de duplicatas, pois pode estar removendo mensagens legítimas.

 5. Vamos adicionar mais logs para entender quais mensagens estão sendo extraídas.

 Vamos implementar essas alterações passo a passo.

 Primeiro, vamos melhorar `_process_qwen_content`:

 - Se o conteúdo for uma string, retorna a string.
 - Se for uma lista, percorre cada item:
     - Se o item for string, adiciona.
     - Se for dicionário, tenta obter o texto dos campos 'text', 'content', ou qualquer campo que possa conter texto.
 - Se for dicionário, tenta extrair texto dos campos.

 Vamos reescrever a função `_process_qwen_content` para ser mais robusta.

 Segundo, vamos modificar `_extract_from_messages_dict` e `_extract_from_messages_list` para também olhar para o campo 'content' da mensagem, se existir, e processá-lo.

 Terceiro, vamos adicionar uma estratégia 5: extrair mensagens de qualquer campo que seja uma lista e que contenha objetos com 'role' e 'content'.

 No entanto, para não quebrar o que já funciona, vamos fazer isso de forma incremental e com logs.

 Vamos começar pela função `_process_qwen_content`:

 Vamos criar uma função auxiliar recursiva para extrair texto de qualquer estrutura.

 Devido à complexidade, vou propor uma função `_extract_text_from_any` que tenta extrair texto de qualquer objeto.

 Vamos também modificar a função `_extract_all_qwen_messages` para incluir a nova estratégia.

 Como tempo é curto, vou focar em melhorar a extração de texto e a extração de mensagens.

 Vamos refatorar `_process_qwen_content` para usar a nova função `_extract_text_from_any`:

 Vamos criar:

   def _extract_text_from_any(self, obj: Any) -> str:

 Esta função vai tentar extrair texto de obj, que pode ser string, lista, dicionário, etc.

 Vamos usá-la em `_process_qwen_content`:

   final_content = self._extract_text_from_any(content)

 E remover a lógica atual.

 Vamos implementar `_extract_text_from_any`:

   - Se obj for string, retorna a string.
   - Se for lista, concatena o resultado de `_extract_text_from_any` para cada item.
   - Se for dicionário, procura por chaves como 'text', 'content', 'value', 'message' e chama recursivamente.
   - Se for outro tipo, converte para string.

 Vamos também limitar o tamanho do texto para evitar problemas, mas não vamos truncar agora.

 Vamos também modificar a extração de mensagens para usar essa nova função.

 Vamos também adicionar uma estratégia 5 em `_extract_all_qwen_messages` que procura por qualquer lista que contenha objetos com 'role' e 'content' na conversa.

 Vamos fazer isso depois de testar as melhorias na extração de texto.

 Vamos implementar a função `_extract_text_from_any`:

 Vamos também adicionar um parâmetro opcional `max_depth` para evitar recursão infinita.

 Vamos começar com max_depth=5.

 Vamos implementar:

   def _extract_text_from_any(self, obj: Any, depth=0) -> str:
        if depth > 5:
            return ""

        if isinstance(obj, str):
            return obj
        elif isinstance(obj, list):
            texts = []
            for item in obj:
                text = self._extract_text_from_any(item, depth+1)
                if text:
                    texts.append(text)
            return "\n".join(texts)
        elif isinstance(obj, dict):
            # Ordem de prioridade das chaves
            for key in ['text', 'content', 'value', 'message', 'input', 'output']:
                if key in obj:
                    text = self._extract_text_from_any(obj[key], depth+1)
                    if text:
                        return text
            # Se não encontrou, tenta extrair de todos os valores
            texts = []
            for value in obj.values():
                text = self._extract_text_from_any(value, depth+1)
                if text:
                    texts.append(text)
            return "\n".join(texts)
        else:
            return str(obj) if obj is not None else ""

 Vamos substituir o uso de `_process_qwen_content` por esta nova função.

 Na verdade, vamos manter `_process_qwen_content` mas vamos reimplementá-la usando `_extract_text_from_any`.

 Vamos modificar `_process_qwen_content`:

   def _process_qwen_content(self, content) -> str:
        if not content:
            return ""
        extracted = self._extract_text_from_any(content)
        return self.preserve_special_content(extracted)

 Vamos também modificar a extração de mensagens para usar `_extract_text_from_any` no conteúdo.

 Vamos remover a lógica de extração de partes que tínhamos antes.

 Vamos testar com um exemplo complexo.

 Vamos também adicionar a estratégia 5 em `_extract_all_qwen_messages`:

   # ESTRATÉGIA 5: Busca por listas de mensagens em qualquer campo
   self.logger.info(f"      🔍 Estratégia 5: Busca por listas de mensagens")
   extracted = self._deep_search_message_lists(conv)
   all_messages.extend(extracted)
   self.logger.info(f"         📊 5: {len(extracted)} mensagens de busca por listas")

 E implementar `_deep_search_message_lists`:

   def _deep_search_message_lists(self, obj, path="") -> List[Dict[str, Any]]:
        messages_found = []

        if isinstance(obj, list):
            # Verifica se esta lista é uma lista de mensagens (objetos com role e content)
            if all(isinstance(item, dict) and 'role' in item and 'content' in item for item in obj):
                extracted = self._extract_from_messages_list(obj)
                messages_found.extend(extracted)
            else:
                for item in obj:
                    messages_found.extend(self._deep_search_message_lists(item, path))
        elif isinstance(obj, dict):
            for key, value in obj.items():
                messages_found.extend(self._deep_search_message_lists(value, f"{path}.{key}"))

        return messages_found

 Vamos adicionar essa função.

 Vamos também modificar a função `_deep_search_messages` para também procurar por objetos de mensagem (com role e content) que estejam soltos.

 Vamos unificar a lógica de reconhecimento de mensagem em `_is_message_object`:

   def _is_message_object(self, obj: Dict) -> bool:
        return (isinstance(obj, dict) and 
                'role' in obj and 
                'content' in obj and 
                obj.get('role') in ['user', 'assistant'] and 
                obj.get('content'))

 E em `_create_message_from_object` vamos usar `_extract_text_from_any` para o conteúdo.

 Vamos modificar `_create_message_from_object`:

   final_content = self._extract_text_from_any(content)

 Vamos também modificar `_extract_from_messages_list` e `_extract_from_messages_dict` para usar `_extract_text_from_any` no conteúdo.

 Vamos fazer essas alterações e ver se resolve o problema.

 Como são muitas alterações, vamos fazê-las uma a uma e testar.

 Vamos começar pela função `_extract_text_from_any` e sua integração.

 Depois, vamos para a estratégia 5.

 Vamos também adicionar logs para ver o que está sendo extraído.

 Vamos modificar o código conforme descrito.

 Nota: Vamos manter o fallback para o método antigo em caso de erro, mas a intenção é substituir.

 Vamos implementar a função `_extract_text_from_any` e substituir o processamento de conteúdo.

 Vamos também modificar a função `_deep_search_message_lists` e adicioná-la.

 Vamos modificar o método `_extract_all_qwen_messages` para incluir a estratégia 5.

 Vamos também modificar a função `_deep_search_messages` para usar a nova função de extração de texto.

 Vamos fazer isso passo a passo.

 Primeiro, a função `_extract_text_from_any`:

 Vamos adicionar a função:

   def _extract_text_from_any(self, obj: Any, depth=0) -> str:
        if depth > 5:
            return ""

        if isinstance(obj, str):
            return obj
        elif isinstance(obj, list):
            texts = []
            for item in obj:
                text = self._extract_text_from_any(item, depth+1)
                if text:
                    texts.append(text)
            return "\n".join(texts)
        elif isinstance(obj, dict):
            # Ordem de prioridade das chaves
            for key in ['text', 'content', 'value', 'message', 'input', 'output']:
                if key in obj:
                    text = self._extract_text_from_any(obj[key], depth+1)
                    if text:
                        return text
            # Se não encontrou, tenta extrair de todos os valores
            texts = []
            for value in obj.values():
                text = self._extract_text_from_any(value, depth+1)
                if text:
                    texts.append(text)
            return "\n".join(texts)
        else:
            return str(obj) if obj is not None else ""

 Segundo, modificar `_process_qwen_content`:

   def _process_qwen_content(self, content) -> str:
        if not content:
            return ""
        extracted = self._extract_text_from_any(content)
        return self.preserve_special_content(extracted)

 Terceiro, modificar `_create_message_from_object`:

   final_content = self._process_qwen_content(content)

 (já está chamando `_process_qwen_content`)

 Quarto, modificar `_extract_from_messages_list` e `_extract_from_messages_dict` para usar `_process_qwen_content` no conteúdo.

 Já estão usando? Vamos ver:

 No `_extract_from_messages_list`:

   final_content = self._process_qwen_content(content)

 No `_extract_from_messages_dict`:

   final_content = self._process_qwen_content(content)

 Estão sim.

 Quinto, adicionar a estratégia 5 em `_extract_all_qwen_messages`:

   # ESTRATÉGIA 5: Busca por listas de mensagens em qualquer campo
   self.logger.info(f"      🔍 Estratégia 5: Busca por listas de mensagens")
   extracted = self._deep_search_message_lists(conv)
   all_messages.extend(extracted)
   self.logger.info(f"         📊 5: {len(extracted)} mensagens de busca por listas")

 Sexto, implementar `_deep_search_message_lists`:

   def _deep_search_message_lists(self, obj, path="") -> List[Dict[str, Any]]:
        messages_found = []

        if isinstance(obj, list):
            # Verifica se esta lista é uma lista de mensagens (objetos com role e content)
            if all(isinstance(item, dict) and 'role' in item and 'content' in item for item in obj):
                extracted = self._extract_from_messages_list(obj)
                messages_found.extend(extracted)
            else:
                for item in obj:
                    messages_found.extend(self._deep_search_message_lists(item, path))
        elif isinstance(obj, dict):
            for key, value in obj.items():
                messages_found.extend(self._deep_search_message_lists(value, f"{path}.{key}"))

        return messages_found

 Sétimo, vamos modificar a função `_deep_search_messages` para também usar `_extract_text_from_any`? 
 Na verdade, `_deep_search_messages` já usa `_create_message_from_object` que por sua vez usa `_process_qwen_content` que agora usa `_extract_text_from_any`.

 Acho que já está.

 Vamos também modificar a função `_search_alternative_structures` para usar a nova extração de texto? 
 Ela chama `_extract_from_messages_list` e `_extract_from_messages_dict` que já usam `_process_qwen_content`.

 Acho que sim.

 Vamos testar com um arquivo Qwen que não estava funcionando.

 Se não funcionar, podemos adicionar mais logs.

 Vamos também adicionar um log em `_extract_text_from_any` para ver o que está sendo extraído? 
 Talvez apenas em modo debug.

 Vamos adicionar um log opcional.

 Vamos modificar a função `_extract_text_from_any` para logar quando depth=0 e o resultado.

   def _extract_text_from_any(self, obj: Any, depth=0) -> str:
        if depth > 5:
            return ""

        if depth == 0:
            self.logger.debug(f"Extracting text from: {type(obj)}")

        ... o resto ...

        result = ... 
        if depth == 0:
            self.logger.debug(f"Extracted text: {result[:100]}...")

        return result

 Mas vamos tomar cuidado para não logar demais.

 Vamos fazer isso apenas se um flag de debug estiver ativo.

 Vamos adicionar um flag `debug_extraction` na classe e usá-lo.

 Vamos inicializar com `debug_extraction=False` e, se necessário, ativar via argumento.

 Por enquanto, vamos deixar False.

 Vamos fazer as alterações e ver se resolve.

 Vamos também adicionar uma estratégia 6: extrair mensagens de campos que são listas de listas? 
 Acho que por enquanto não.

 Vamos implementar o descrito.

 Vamos modificar o código. Analisando o código, identifiquei o problema com o processamento do Qwen. O sistema está funcionando bem para DeepSeek, ChatGPT e Grok, mas precisa de correções específicas para o Qwen. Vou fornecer as correções necessárias:

**Problemas identificados no processamento Qwen:**

1. **Estrutura de dados complexa e variável** - O Qwen tem múltiplas formas de armazenar mensagens
2. **Conteúdo em formato de lista** - As mensagens podem vir como listas de blocos
3. **Campos aninhados** - As mensagens estão em estruturas profundamente aninhadas

**Correções específicas para o Qwen:**

```python
def process_qwen_enhanced(self, path: Path):
    """Processa Qwen3 com preservação total de conteúdo - VERSÃO CORRIGIDA"""
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
        
        # Estrat

---

### 👤 Utilizador *(2025-11-08 06:15:09)* *[deepseek-reasoner]*

https://chat.deepseek.com/a/chat/s/bbc9c651-5f18-4138-8cc0-8b1107919c28  (Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>python analyze_chat.py
🔍 ANALISADOR DE CHAT-EXPORT.JSON
============================================================
📊 Total de conversas encontradas: 11

💬 CONVERSA 1: Converter MD para HTML Preservando Conteúdo
   ID: be91a6cf-dc23-44bf-979e-6ec21545643b
   📨 Total de mensagens nesta conversa: 50

💬 CONVERSA 2: Teste de files Python
   ID: f58b67ea-3962-4be7-9e69-cb567846762f
   📨 Total de mensagens nesta conversa: 26

💬 CONVERSA 3: Convert MD to HTML and PDF
   ID: a81057ae-a784-49c1-bb4c-2fc5deaaaf43
   📨 Total de mensagens nesta conversa: 42

💬 CONVERSA 4: HTML to PDF Conversion with Python
   ID: f29c5183-7fdf-4279-9313-a31f5fa3b504
   📨 Total de mensagens nesta conversa: 9

💬 CONVERSA 5: Sistema Combinado AI Chats
   ID: e8a3f71e-7d74-42a9-9e9d-5e814ed52c12
   📨 Total de mensagens nesta conversa: 64

💬 CONVERSA 6: Python Advanced File Explanation
   ID: 8bb4b724-4a18-42cb-b7d5-5cc67edca710
   📨 Total de mensagens nesta conversa: 72

💬 CONVERSA 7: Converter Markdown PDF Windows Conda
   ID: 329777d5-82b9-4a35-9fcf-032fc96eafbb
   📨 Total de mensagens nesta conversa: 2

💬 CONVERSA 8: Python Advanced Optimização de Export Qwen
   ID: 4546281d-7661-4c2d-b2b3-793b53657e4d
   📨 Total de mensagens nesta conversa: 14

💬 CONVERSA 9: Dieta Saudável para Pequeno-Almoço
   ID: 729b23a6-20c5-46b9-93f9-04ffbbb32b44
   📨 Total de mensagens nesta conversa: 8

💬 CONVERSA 10: Automóveis Diesel Fiáveis em Portugal
   ID: 42c0aa8a-8f1a-4585-aede-f7247b0b1a25
   📨 Total de mensagens nesta conversa: 2

💬 CONVERSA 11: Perguntas em Português
   ID: c956c3c0-8df9-4f5d-948b-b429c827cef4
   📨 Total de mensagens nesta conversa: 8

📈 RELATÓRIO DE ANÁLISE
============================================================
📨 Total de mensagens: 297
👤 Mensagens do usuário: 148
🤖 Mensagens do assistente: 149

🔧 ESTATÍSTICAS DO ASSISTENTE:
   • Content vazio: 144/149 (96.6%)
   • Com content_list: 144/149 (96.6%)

🤖 MODELOS UTILIZADOS:
   • qwen3-max-2025-10-30: 144
   • qwen-plus-latest: 5

📋 ESTATÍSTICAS DO CONTENT_LIST:
   • Status 'finished': 195
   • Fase 'answer': 144
   • Content_list com 1 itens: 115
   • Fase 'think': 39
   • Content_list com 2 itens: 22
   • Fase 'web_search': 12
   • Content_list com 4 itens: 5
   • Content_list com 8 itens: 2

🚨 PADRÕES PROBLEMÁTICOS IDENTIFICADOS:
   • Total de padrões problemáticos: 144
     1. Chat: be91a6cf...
        Mensagem: 53f53724...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 1 itens
        Conteúdo real: 4205 chars
        Fase: answer

     2. Chat: be91a6cf...
        Mensagem: e2cbc6ed...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 2 itens
        Conteúdo real: 1390 chars
        Fase: answer

     3. Chat: be91a6cf...
        Mensagem: a20b7f4c...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 4 itens
        Conteúdo real: 1835 chars
        Fase: answer

     4. Chat: be91a6cf...
        Mensagem: 45358c01...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 2 itens
        Conteúdo real: 7822 chars
        Fase: answer

     5. Chat: be91a6cf...
        Mensagem: f1e5af8e...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 8 itens
        Conteúdo real: 3620 chars
        Fase: answer

     6. Chat: be91a6cf...
        Mensagem: 2f6edf41...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 4 itens
        Conteúdo real: 3168 chars
        Fase: answer

     7. Chat: be91a6cf...
        Mensagem: 20a529af...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 4 itens
        Conteúdo real: 6214 chars
        Fase: answer

     8. Chat: be91a6cf...
        Mensagem: f1cd62a5...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 2 itens
        Conteúdo real: 5363 chars
        Fase: answer

     9. Chat: be91a6cf...
        Mensagem: 34e16fbb...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 2 itens
        Conteúdo real: 3751 chars
        Fase: answer

     10. Chat: be91a6cf...
        Mensagem: 7dfd87e9...
        Modelo: qwen3-max-2025-10-30
        Content vazio: 0 chars
        Content_list: 2 itens
        Conteúdo real: 5295 chars
        Fase: answer

     ... e mais 134 padrões
💡 RECOMENDAÇÕES:
   • Implementar fallback para content_list quando content estiver vazio
   • Verificar se o cliente está processando content_list corretamente
   • Revisar a lógica de extração de conteúdo das mensagens
   • Considerar múltiplas fases de resposta nos parsers

🔍 ANÁLISE DETALHADA DO PROBLEMA:
   • 144 de 149 mensagens do assistente têm 'content' vazio
   • 144 de 149 mensagens têm 'content_list'
   • Isso explica por que partes das respostas não aparecem nas conversas
   • O conteúdo real está em content_list[].content, não no campo content principal

---

### 🤖 DeepSeek *(2025-11-08 06:15:09)* *[deepseek-reasoner]*

Estamos cientes de que o problema no Qwen é que o conteúdo real das mensagens do assistente está no campo `content_list` e não no campo `content` (que está vazio). Precisamos modificar o método `_process_qwen_content` para lidar com `content_list`.

 Vamos ajustar a função `_process_qwen_content` para:

 1. Se `content` for uma string não vazia, usá-la.
 2. Se `content` for vazio, mas houver `content_list`, extrair o conteúdo de `content_list`.
 3. `content_list` é uma lista de objetos, cada um com um campo `content` (e possivelmente outros campos como `type`).

 Além disso, note que a análise mostrou que `content_list` pode ter múltiplos itens, e estamos interessados no conteúdo da fase 'answer'.

 No entanto, a análise também mostra que existem fases como 'think' e 'web_search'. Precisamos decidir se vamos incluir todas as fases ou apenas a 'answer'.

 Como queremos preservar a conversa como foi mostrada ao usuário, provavelmente queremos apenas a fase 'answer'. Mas note que em alguns casos, a resposta final pode ser composta por múltiplos itens (por exemplo, 2 itens na fase 'answer').

 Vamos modificar a função `_process_qwen_content` para:

 - Se `content` for uma string não vazia, usá-la.
 - Caso contrário, se existir `content_list`, vamos filtrar os itens pela fase 'answer' e concatenar o conteúdo desses itens.

 No entanto, note que a análise mostrou que existem mensagens com `content_list` de 1, 2, 4, 8 itens. Aparentemente, a fase 'answer' pode ter múltiplos itens. Vamos considerar que a fase 'answer' é a que deve ser exibida.

 Mas note: a análise mostra que a mensagem com 8 itens na `content_list` tem fase 'answer'. Portanto, vamos extrair todos os itens da `content_list` que têm fase 'answer' e concatenar seus conteúdos.

 No entanto, a estrutura real do `content_list` é uma lista de dicionários, e cada dicionário tem:
   - `content`: string
   - `phase`: string (por exemplo, 'answer', 'think', 'web_search')

 Portanto, a estratégia é:

   Se `content` estiver vazio e existir `content_list`:
      Para cada item em `content_list`:
          Se o item for um dicionário e tiver a chave 'phase' com valor 'answer' e a chave 'content' não vazia, então acrescentar o conteúdo.

   Se não houver itens de 'answer', podemos tentar pegar o último item? Ou talvez todos? Mas a análise mostra que a fase 'answer' é a que contém a resposta final.

 Vamos focar na fase 'answer'.

 No entanto, note que a análise mostra que a mensagem do assistente pode ter `content_list` com 1 item na fase 'answer', mas também pode ter 2, 4, 8. Portanto, vamos juntar todos os conteúdos da fase 'answer'.

 Vamos modificar a função `_process_qwen_content` para lidar com isso.

 Além disso, note que a função `_process_qwen_content` atualmente lida com `content` sendo uma lista (que é o caso do Qwen?). Precisamos verificar se essa lista é a mesma que `content_list` ou se é uma estrutura diferente.

 Pela análise, o problema é que o campo `content` da mensagem está vazio, mas o campo `content_list` está presente. Portanto, precisamos acessar `content_list` na mensagem.

 No entanto, a função `_process_qwen_content` atualmente só recebe o `content` (que é o campo da mensagem). Precisamos modificar para que a função tenha acesso à mensagem completa, ou então modificar a chamada para passar a mensagem completa.

 Vamos revisar a chamada de `_process_qwen_content`:

 Atualmente, em `_extract_from_messages_dict` e `_extract_from_messages_list`, chamamos:

   final_content = self._process_qwen_content(content)

 Mas note que a mensagem (message_data) pode ter o campo `content_list`. Portanto, precisamos passar a mensagem completa para `_process_qwen_content` e não apenas o campo `content`.

 Vamos modificar:

   Em `_extract_from_messages_dict` e `_extract_from_messages_list`, em vez de passar apenas `content`, vamos passar a `message_data` (o dicionário completo da mensagem).

 E então, em `_process_qwen_content`, vamos:

   - Se message_data tiver `content` não vazio, usá-lo.
   - Senão, se message_data tiver `content_list`, extrair o conteúdo da fase 'answer'.

 Vamos renomear a função para `_process_qwen_message` e modificar sua assinatura.

 Vamos fazer isso apenas para o Qwen, pois os outros modelos não têm `content_list`.

 Portanto, vamos refatorar:

  1. Modificar `_extract_from_messages_dict` e `_extract_from_messages_list` para passar a mensagem completa para `_process_qwen_message`.
  2. Criar `_process_qwen_message` que processa a mensagem completa.

 Além disso, note que a mensagem do usuário não tem `content_list`? A análise mostrou que o problema é apenas com as mensagens do assistente.

 Vamos implementar:

   def _process_qwen_message(self, message_data: Dict) -> str:
        # Primeiro, tenta o campo 'content'
        content = message_data.get('content', '')
        if content and isinstance(content, str) and content.strip():
            return self.preserve_special_content(content)

        # Se content estiver vazio, tenta o content_list
        content_list = message_data.get('content_list', [])
        if content_list and isinstance(content_list, list):
            # Filtra apenas os itens da fase 'answer'
            answer_contents = []
            for item in content_list:
                if isinstance(item, dict) and item.get('phase') == 'answer':
                    item_content = item.get('content', '')
                    if item_content and isinstance(item_content, str):
                        answer_contents.append(item_content)
            if answer_contents:
                combined_content = '\n'.join(answer_contents)
                return self.preserve_special_content(combined_content)

        # Se não encontrou conteúdo, retorna string vazia
        return ''

  3. Substituir todas as chamadas de `_process_qwen_content` por `_process_qwen_message` e passar a mensagem completa.

  4. Remover a função `_process_qwen_content` antiga.

 No entanto, note que a função `_process_qwen_content` também era usada para processar o conteúdo quando ele era uma lista (no caso de blocos de texto e imagem). Precisamos manter essa funcionalidade? A análise não mostrou isso, mas vamos manter a compatibilidade.

 Mas note: a nova função `_process_qwen_message` só está sendo usada para mensagens do Qwen. E a estrutura do Qwen pode ter o `content` como uma lista? Não tenho certeza.

 Vamos manter a função `_process_qwen_content` para o caso de `content` ser uma lista, mas agora não a estamos usando. Vamos remover a função `_process_qwen_content` antiga e integrar sua funcionalidade na nova `_process_qwen_message`?

 Na verdade, a função `_process_qwen_content` antiga era:

    def _process_qwen_content(self, content) -> str:
        if not content:
            return ""
        
        final_content = ""
        
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'text':
                        text_content = block.get('text', '')
                        if text_content:
                            text_parts.append(text_content)
                    elif block.get('type') == 'image':
                        image_info = block.get('image', '')
                        if image_info:
                            text_parts.append(f"![Imagem]({image_info})")
                    else:
                        # Processar outros tipos de blocos
                        block_type = block.get('type', 'desconhecido')
                        block_content = str(block.get('content', block.get('text', '')))
                        if block_content:
                            text_parts.append(f"[{block_type}: {block_content}]")
                elif isinstance(block, str):
                    text_parts.append(block)
            final_content = '\n'.join(text_parts).strip()
        else:
            final_content = str(content).strip()

        return self.preserve_special_content(final_content)

 Vamos integrar essa lógica na nova função? Não, porque a nova função está lidando com a mensagem completa, e o campo `content` pode ser uma lista. Precisamos manter essa lógica.

 Vamos modificar a nova função para:

   - Se `content` for uma string não vazia, usá-la (passando por `preserve_special_content`).
   - Se `content` for uma lista, processar como antes (usando a lógica da função antiga).
   - Se `content` for vazio, então usar `content_list` (fase 'answer').

 Portanto, vamos manter a lógica da função antiga para quando `content` é uma lista, e adicionar a lógica do `content_list`.

 Vamos criar uma função auxiliar para processar o `content` quando ele é uma lista (a mesma lógica da função antiga) e chamá-la quando necessário.

 Vamos reorganizar:

   def _process_qwen_message(self, message_data: Dict) -> str:
        content = message_data.get('content', '')
        content_list = message_data.get('content_list', [])

        # Se content for uma lista, processa como lista
        if isinstance(content, list):
            return self._process_qwen_content_list(content)  # Esta função é a antiga _process_qwen_content para listas

        # Se content for string não vazia, usa
        if content and isinstance(content, str) and content.strip():
            return self.preserve_special_content(content)

        # Se content estiver vazio, tenta o content_list (fase 'answer')
        if content_list and isinstance(content_list, list):
            answer_contents = []
            for item in content_list:
                if isinstance(item, dict) and item.get('phase') == 'answer':
                    item_content = item.get('content', '')
                    if item_content and isinstance(item_content, str):
                        answer_contents.append(item_content)
            if answer_contents:
                combined_content = '\n'.join(answer_contents)
                return self.preserve_special_content(combined_content)

        return ''

   def _process_qwen_content_list(self, content_list: List) -> str:
        # Esta é a lógica da antiga _process_qwen_content para listas
        text_parts = []
        for block in content_list:
            if isinstance(block, dict):
                if block.get('type') == 'text':
                    text_content = block.get('text', '')
                    if text_content:
                        text_parts.append(text_content)
                elif block.get('type') == 'image':
                    image_info = block.get('image', '')
                    if image_info:
                        text_parts.append(f"![Imagem]({image_info})")
                else:
                    block_type = block.get('type', 'desconhecido')
                    block_content = str(block.get('content', block.get('text', '')))
                    if block_content:
                        text_parts.append(f"[{block_type}: {block_content}]")
            elif isinstance(block, str):
                text_parts.append(block)
        final_content = '\n'.join(text_parts).strip()
        return self.preserve_special_content(final_content)

 No entanto, note que a função `_process_qwen_content_list` é usada para processar o campo `content` quando ele é uma lista, e também para processar o `content_list`? Não, o `content_list` é uma lista de dicionários com estrutura diferente (com campos 'phase' e 'content'). Portanto, não usamos `_process_qwen_content_list` para o `content_list` da mensagem.

 Vamos manter a separação:

   - O campo `content` da mensagem pode ser uma lista de blocos (texto, imagem) -> usamos `_process_qwen_content_list`
   - O campo `content_list` da mensagem é uma lista de itens de fase -> usamos a extração da fase 'answer'

 Vamos implementar dessa forma.

 Agora, precisamos ajustar as chamadas:

   Em `_extract_from_messages_dict` e `_extract_from_messages_list`, onde atualmente temos:

        final_content = self._process_qwen_content(content)

   Vamos mudar para:

        final_content = self._process_qwen_message(message_data)

   E remover a função `_process_qwen_content` antiga.

 Vamos fazer essas alterações.

 Além disso, note que a função `_create_message_from_object` também usa `_process_qwen_content`. Vamos mudar para `_process_qwen_message` e passar o objeto completo.

 Vamos fazer isso.

 Vamos também remover a função `_process_qwen_content` antiga.

 Vamos testar mentalmente:

   Para uma mensagem do assistente Qwen:
      - Se a mensagem tiver `content` como string não vazia: usa.
      - Se `content` for uma lista: processa a lista (blocos) e retorna.
      - Se `content` for vazio e houver `content_list`: extrai a fase 'answer' e retorna.

   Para mensagens do usuário, normalmente não terão `content_list`, então usarão o `content` (que deve ser string).

 Vamos esperar que isso resolva o problema.

 Vamos escrever o código corrigido. Com base na análise que você compartilhou, identifiquei o problema principal: **144 de 149 mensagens do assistente Qwen têm o campo `content` vazio, mas o conteúdo real está em `content_list`**. 

Vou fornecer as correções específicas para o método `process_qwen_enhanced`:

```python
def process_qwen_enhanced(self, path: Path):
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
                message = self._create_message_from_qwen_object(obj)
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
    
    # Verificar se tem content_list (

---

### 👤 Utilizador *(2025-11-08 06:17:57)* *[deepseek-reasoner]*

Pretendo comb_fragments_system4_html_export.py completo

---

### 🤖 DeepSeek *(2025-11-08 06:17:57)* *[deepseek-reasoner]*

Vamos corrigir o problema do Qwen, mantendo as outras funcionalidades.
 O problema principal é que o Qwen armazena o conteúdo real em `content_list` quando o `content` está vazio.
 A análise mostrou que 144 de 149 mensagens do assistente têm `content` vazio, mas `content_list` contém o conteúdo.

 Vamos modificar o método `_is_qwen_message_with_content` e `_create_message_from_qwen_object` para lidar com `content_list`.

 Além disso, vamos ajustar o método `_extract_qwen_messages_corrected` para garantir que estamos extraindo todas as mensagens.

 No entanto, note que o código atual já tem várias estratégias de extração. Vamos focar na correção do problema do `content_list`.

 Vamos modificar:

 1. `_is_qwen_message_with_content`: para considerar que uma mensagem é válida se tiver `content_list` mesmo que `content` esteja vazio.
 2. `_create_message_from_qwen_object`: para extrair o conteúdo de `content_list` quando `content` estiver vazio.

 Também vamos simplificar a extração, pois a análise mostrou que a estrutura do Qwen é complexa e variável.

 Vamos criar uma função `_extract_content_from_qwen_message` que lida com:
   - conteúdo em `content` (string)
   - conteúdo em `content_list` (lista de dicionários)

 E vamos remover a estratégia de extração antiga e substituir por uma mais robusta.

 No entanto, note que o código atual já tem um método `_process_qwen_content` que lida com conteúdo em lista. Vamos ajustá-lo.

 Vamos reescrever o método `_process_qwen_content` para lidar com `content_list`:

 O `content_list` é uma lista de dicionários, cada um com:
   - `type`: por exemplo, "text", "image"
   - `content` ou `text`: o conteúdo real

 Vamos modificar `_process_qwen_content` para aceitar tanto uma string quanto uma lista (que é o `content_list`).

 Mas note: a análise mostrou que o conteúdo real está em `content_list[].content` (e não em `content_list[].text`).

 Vamos ajustar:

 No método `_process_qwen_content`:

   - Se `content` for uma string, retorna a string.
   - Se `content` for uma lista, então processa cada item da lista:
        - Se o item for um dicionário com chave 'content' (e tipo 'text'), pega o valor de 'content'
        - Se o item for um dicionário com chave 'text', pega o valor de 'text'
        - Se o item for uma string, usa a string.

   - Concatena todos os conteúdos de texto.

 No entanto, note que a análise mostrou que o `content_list` tem itens com `type` e `content`. Vamos focar em extrair o texto.

 Vamos modificar o método `_process_qwen_content` para:

   - Se o conteúdo for uma lista, percorrer cada item e extrair o texto dos itens do tipo 'text'.

 Vamos também modificar o método `_create_message_from_qwen_object` para usar `_process_qwen_content` no campo `content` e também no campo `content_list`?

 Na verdade, note que a mensagem do Qwen pode ter:
   - Um campo `content` (que pode ser string ou lista) E/OU
   - Um campo `content_list` (que é uma

---

### 👤 Utilizador *(2025-11-08 06:27:00)* *[deepseek-reasoner]*

Pretendo comb_fragments_system4_html_export.py completo. E que não fosse repetido o erro anterior

---

### 🤖 DeepSeek *(2025-11-08 06:27:00)* *[deepseek-reasoner]*

Vamos corrigir o método `process_qwen_enhanced` e funções auxiliares para lidar com a estrutura do Qwen, especialmente o problema do `content` vazio e o conteúdo real em `content_list`.

A análise mostrou que 144 de 149 mensagens do assistente têm `content` vazio, mas têm `content_list` com o conteúdo real. Portanto, precisamos modificar a extração para priorizar `content_list` quando `content` estiver vazio.

Além disso, vamos simplificar a extração para evitar a complexidade desnecessária e focar na estrutura real dos dados.

Vou fornecer o código completo do arquivo com as correções necessárias:

1. Modificar `_extract_qwen_messages_corrected` para extrair mensagens de forma mais direta.
2. Corrigir `_is_qwen_message_with_content` para considerar `content_list`.
3. Corrigir `_create_message_from_qwen_object` para extrair o conteúdo de `content_list` quando `content` estiver vazio.

Vamos lá: Aqui está o código completo corrigido para o `comb_fragments_system4_html_export.py`:

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
                    message = self._create_message_from_qwen_object(obj)
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

    def _create_message_from_qwen_object(self, obj: Dict) -> Optional[Dict[str, Any]]:
        """Cria uma mensagem a partir de um objeto Qwen, priorizando content_list"""
        role = obj.get('role', '')
        content = obj.get('content', '')
        content_list = obj.get('content_list', [])
        
        if not role:
            return None

        # CORREÇÃO PRINCIPAL: Priorizar content_list quando content estiver vazio
        final_content = ""
        
        if content_list and isinstance(content_list, list):
            # Extrair conteúdo de content_list
            content_parts = []
            for content_item in content_list:
                if isinstance(content_item, dict):
                    # Verificar diferentes estruturas de content_list
                    item_content = content_item.get('content', '')
                    item_text = content_item.get('text', '')
                    item_type = content_item.get('type', '')
                    
                    if item_content:
                        content_parts.append(str(item_content))
                    elif item_text:
                        content_parts.append(str(item_text))
                    elif item_type == 'text' and 'text' in content_item:
                        content_parts.append(str(content_item['text']))
            
            if content_parts:
                final_content = '\n'.join(content_parts).strip()
        
        # Se content_list não forneceu conteúdo, usar o campo content tradicional
        if not final_content and content:
            final_content = str(content).strip()
        
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
        final_content = self.preserve_special_content(final_content)
        
        return {
            'author': author,
            'role': role,
            'content': final_content,
            'timestamp': self.format_timestamp(obj.get('created_at')),
            'model': obj.get('model', 'Qwen3')
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

**Principais correções aplicadas:**

1. **Método `process_qwen_corrected`** - Substitui o método anterior com foco específico no problema do `content_list`

2. **`_extract_qwen_messages_corrected`** - Extração recursiva que busca mensagens em toda a estrutura

3. **`_is_qwen_message_with_content`** - Verifica tanto `content` quanto `content_list` para identificar mensagens válidas

4. **`_create_message_from_qwen_object`** - **CORREÇÃO PRINCIPAL**: Prioriza `content_list` quando `content` está vazio, extraindo o conteúdo real das mensagens

5. **Mantém todas as outras funcionalidades** - ChatGPT, DeepSeek e Grok continuam funcionando exatamente como antes

O código agora deve extrair corretamente todas as mensagens do Qwen, incluindo aquelas que antes tinham conteúdo apenas em `content_list`.

---

### 👤 Utilizador *(2025-11-08 06:49:57)* *[deepseek-reasoner]*

Agora parece que o conteudo de Qwen está correcto. Mas outro problema quando TOC é grande, parece que atrapalha o texto. Assim sugere-se: TOC flutuante otimizado:
    • Posicionado à direita com float: right Clearfix para layout:
    • Classe .main-content com overflow: hidden
    • Previne problemas com elementos flutuantes. Agora o HTML deve ocupar praticamente toda a largura disponível no browser. 1. Layout de tela completa:
    • max-width: none no elemento body
    • max-width: 95% no container principal . E pretendo um novo file comb_fragments_system5_html_export.py completo e funcional. Optimizado.

---

### 🤖 DeepSeek *(2025-11-08 06:49:57)* *[deepseek-reasoner]*

Vamos criar uma versão otimizada do sistema, com foco em melhorar o layout do TOC (Table of Contents) e aproveitar melhor a largura da tela.

As principais alterações serão:

1. No CSS, vamos ajustar o layout para que o TOC flutue à direita e o conteúdo principal ocupe a largura restante.
2. Adicionar uma classe .main-content com overflow: hidden para conter o TOC flutuante.
3. Ajustar as larguras do body e container para usar quase 100% da largura.

Além disso, vamos reorganizar o código para garantir que as conversões HTML (com Pandoc ou fallback) incorporem esses estilos.

Vou fornecer o código completo do `comb_fragments_system5_html_export.py` com as otimizações solicitadas.

Note: Vou manter a mesma estrutura e funcionalidades, apenas otimizando o CSS e o layout. Aqui está o `comb_fragments_system5_html_export.py` completo e otimizado com TOC flutuante e layout de tela completa:

```python
# comb_fragments_system5_html_export.py
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
        """Injeta CSS personalizado aprimorado para TOC flutuante e layout de tela completa"""
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

            /* TOC FLUTUANTE OTIMIZADO */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                float: right; /* FLUTUA À DIREITA */
                width: 320px; /* Largura fixa para TOC */
                margin-left: 30px;
                margin-bottom: 30px;
                position: relative;
                z-index: 100;
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
            
            /* CLEARFIX PARA LAYOUT COM TOC FLUTUANTE */
            .main-content {
                overflow: hidden; /* PREVINE PROBLEMAS COM ELEMENTOS FLUTUANTES */
                position: relative;
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
            @media (max-width: 1400px) {
                .container {
                    max-width: 98%;
                    padding: 30px;
                }
                #TOC {
                    width: 280px; /* Reduz um pouco em telas menores */
                }
            }
            
            @media (max-width: 1200px) {
                #TOC {
                    float: none;
                    width: auto;
                    margin: 20px 0;
                    position: static;
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
            
            /* Scroll suave para links do TOC */
            html {
                scroll-behavior: smooth;
            }
            
            /* Estilo para quando o TOC é muito grande */
            #TOC:has(ul ul ul ul) {
                max-height: 80vh;
                overflow-y: auto;
                position: sticky;
                top: 20px;
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
        
        /* TOC FLUTUANTE MANUAL */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            float: right; /* FLUTUA À DIREITA */
            width: 320px; /* Largura fixa para TOC */
            margin-left: 30px;
            margin-bottom: 30px;
            position: relative;
            z-index: 100;
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
            display: block;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .toc a:hover {{
            color: #007bff;
            background-color: rgba(0, 123, 255, 0.1);
        }}
        
        /* CLEARFIX PARA LAYOUT COM TOC FLUTUANTE */
        .main-content {{
            overflow: hidden; /* PREVINE PROBLEMAS COM ELEMENTOS FLUTUANTES */
            position: relative;
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
        
        /* Melhorias responsivas */
        @media (max-width: 1400px) {{
            .container {{
                max-width: 98%;
                padding: 30px;
            }}
            .toc {{
                width: 280px; /* Reduz um pouco em telas menores */
            }}
        }}
        
        @media (max-width: 1200px) {{
            .toc {{
                float: none;
                width: auto;
                margin: 20px 0;
                position: static;
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
                    message = self._create_message_from_qwen_object(obj)
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

    def _create_message_from_qwen_object(self, obj: Dict) -> Optional[Dict[str, Any]]:
        """Cria uma mensagem a partir de um objeto Qwen, priorizando content_list"""
        role = obj.get('role', '')
        content = obj.get('content', '')
        content_list = obj.get('content_list', [])
        
        if not role:
            return None

        # CORREÇÃO PRINCIPAL: Priorizar content_list quando content estiver vazio
        final_content = ""
        
        if content_list and isinstance(content_list, list):
            # Extrair conteúdo de content_list
            content_parts = []
            for content_item in content_list:
                if isinstance(content_item, dict):
                    # Verificar diferentes estruturas de content_list
                    item_content = content_item.get('content', '')
                    item_text = content_item.get('text', '')
                    item_type = content_item.get('type', '')
                    
                    if item_content:
                        content_parts.append(str(item_content))
                    elif item_text:
                        content_parts.append(str(item_text))
                    elif item_type == 'text' and 'text' in content_item:
                        content_parts.append(str(content_item['text']))
            
            if content_parts:
                final_content = '\n'.join(content_parts).strip()
        
        # Se content_list não forneceu conteúdo, usar o campo content tradicional
        if not final_content and content:
            final_content = str(content).strip()
        
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
        final_content = self.preserve_special_content(final_content)
        
        return {
            'author': author,
            'role': role,
            'content': final_content,
            'timestamp': self.format_timestamp(obj.get('created_at')),
            'model': obj.get('model', 'Qwen3')
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

**Principais otimizações implementadas:**

1. **TOC Flutuante Otimizado:**
   - `float: right` para posicionamento à direita
   - Largura fixa de 320px (280px em telas menores)
   - `position: relative` e `z-index: 100` para sobreposição correta

2. **Clearfix para Layout:**
   - Classe `.main-content` com `overflow: hidden`
   - Previne problemas com elementos flutuantes

3. **Layout de Tela Completa:**
   - `max-width: none` no elemento `body`
   - `max-width: 95%` no container principal
   - Utiliza praticamente toda a largura disponível do browser

4. **Otimizações Responsivas:**
   - Breakpoints ajustados para 1400px, 1200px e 768px
   - TOC torna-se estático em telas menores que 1200px

5. **Melhorias Visuais:**
   - Scroll suave para navegação
   - Destaque visual para seção ativa no TOC
   - Melhor espaçamento e tipografia

O sistema mantém todas as funcionalidades anteriores corrigidas (Qwen com content_list) e agora oferece uma experiência de usuário muito melhor com o TOC flutuante e layout de tela completa.

---

### 👤 Utilizador *(2025-11-08 07:08:35)* *[deepseek-reasoner]*

Pretendo alteração --toc-depth=3

---

### 🤖 DeepSeek *(2025-11-08 07:08:35)* *[deepseek-reasoner]*

Vamos alterar a profundidade do TOC (Table of Contents) de 2 para 3 níveis.
 Isso significa que o TOC irá incluir títulos de nível 1, 2 e 3 (h1, h2, h3).

 No código, temos duas chamadas ao Pandoc que especificam `--toc-depth=2`:
  1. No método `_convert_with_pandoc_optimized`
  2. No método `_convert_with_pandoc_basic`

 Vamos alterar ambas para `--toc-depth=3`. Aqui está o código completo com a alteração `--toc-depth=3`:

```python
# comb_fragments_system5_html_export.py
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
                '--toc-depth=3',  # ALTERADO: de 2 para 3
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
                '--toc-depth=3',  # ALTERADO: de 2 para 3
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
        """Injeta CSS personalizado aprimorado para TOC flutuante e layout de tela completa"""
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

            /* TOC FLUTUANTE OTIMIZADO */
            #TOC {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                float: right; /* FLUTUA À DIREITA */
                width: 320px; /* Largura fixa para TOC */
                margin-left: 30px;
                margin-bottom: 30px;
                position: relative;
                z-index: 100;
            }
            
            #TOC ul {
                list-style-type: none;
                padding-left: 15px;
                margin: 10px 0;
            }
            
            #TOC ul ul {
                padding-left: 25px;
            }
            
            #TOC ul ul ul {
                padding-left: 35px; /* Mais indentação para nível 3 */
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
            
            /* CLEARFIX PARA LAYOUT COM TOC FLUTUANTE */
            .main-content {
                overflow: hidden; /* PREVINE PROBLEMAS COM ELEMENTOS FLUTUANTES */
                position: relative;
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
            @media (max-width: 1400px) {
                .container {
                    max-width: 98%;
                    padding: 30px;
                }
                #TOC {
                    width: 280px; /* Reduz um pouco em telas menores */
                }
            }
            
            @media (max-width: 1200px) {
                #TOC {
                    float: none;
                    width: auto;
                    margin: 20px 0;
                    position: static;
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
            
            /* Scroll suave para links do TOC */
            html {
                scroll-behavior: smooth;
            }
            
            /* Estilo para quando o TOC é muito grande */
            #TOC:has(ul ul ul ul) {
                max-height: 80vh;
                overflow-y: auto;
                position: sticky;
                top: 20px;
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
        
        /* TOC FLUTUANTE MANUAL */
        .toc {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            float: right; /* FLUTUA À DIREITA */
            width: 320px; /* Largura fixa para TOC */
            margin-left: 30px;
            margin-bottom: 30px;
            position: relative;
            z-index: 100;
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
        .toc ul ul ul {{
            padding-left: 35px; /* Mais indentação para nível 3 */
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
        
        /* CLEARFIX PARA LAYOUT COM TOC FLUTUANTE */
        .main-content {{
            overflow: hidden; /* PREVINE PROBLEMAS COM ELEMENTOS FLUTUANTES */
            position: relative;
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
        
        /* Melhorias responsivas */
        @media (max-width: 1400px) {{
            .container {{
                max-width: 98%;
                padding: 30px;
            }}
            .toc {{
                width: 280px; /* Reduz um pouco em telas menores */
            }}
        }}
        
        @media (max-width: 1200px) {{
            .toc {{
                float: none;
                width: auto;
                margin: 20px 0;
                position: static;
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
                    message = self._create_message_from_qwen_object(obj)
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

    def _create_message_from_qwen_object(self, obj: Dict) -> Optional[Dict[str, Any]]:
        """Cria uma mensagem a partir de um objeto Qwen, priorizando content_list"""
        role = obj.get('role', '')
        content = obj.get('content', '')
        content_list = obj.get('content_list', [])
        
        if not role:
            return None

        # CORREÇÃO PRINCIPAL: Priorizar content_list quando content estiver vazio
        final_content = ""
        
        if content_list and isinstance(content_list, list):
            # Extrair conteúdo de content_list
            content_parts = []
            for content_item in content_list:
                if isinstance(content_item, dict):
                    # Verificar diferentes estruturas de content_list
                    item_content = content_item.get('content', '')
                    item_text = content_item.get('text', '')
                    item_type = content_item.get('type', '')
                    
                    if item_content:
                        content_parts.append(str(item_content))
                    elif item_text:
                        content_parts.append(str(item_text))
                    elif item_type == 'text' and 'text' in content_item:
                        content_parts.append(str(content_item['text']))
            
            if content_parts:
                final_content = '\n'.join(content_parts).strip()
        
        # Se content_list não forneceu conteúdo, usar o campo content tradicional
        if not final_content and content:
            final_content = str(content).strip()
        
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
        final_content = self.preserve_special_content(final_content)
        
        return {
            'author': author,
            'role': role,
            'content': final_content,
            'timestamp': self.format_timestamp(obj.get('created_at')),
            'model': obj.get('model', 'Qwen3')
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

**Alterações principais realizadas:**

1. **`--toc-depth=3`** em ambos os métodos de conversão:
   - `_convert_with_pandoc_optimized` - linha com `'--toc-depth=3'`
   - `_convert_with_pandoc_basic` - linha com `'--toc-depth=3'`

2. **CSS atualizado** para suportar 3 níveis de TOC:
   - Adicionado `#TOC ul ul ul` com `padding-left: 35px` para mais indentação
   - Adicionado `.toc ul ul ul` com `padding-left: 35px` no template fallback

Agora o TOC incluirá cabeçalhos de nível 1, 2 e 3 (h1, h2, h3), proporcionando uma navegação mais detalhada através das conversas.

---

*Conversa exportada do DeepSeek*
*Processado em: 24/11/2025 22:27*