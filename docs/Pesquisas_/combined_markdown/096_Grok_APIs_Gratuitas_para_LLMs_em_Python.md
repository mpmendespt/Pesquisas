# APIs Gratuitas para LLMs em Python

## 📊 Informações
- **Número:** #96
- **Origem:** Grok
- **Categoria:** Programação
- **ID:** 92511678-a824-43ae-aead-b39a861012ad
- **Criada em:** 2025-10-22 14:26:26Z
- **Atualizada em:** 2025-10-22 14:26:45Z
- **Total de mensagens:** 2
- **Resumo:** Existe alguma alguma api gratuita de chatgpt, deepseek, gork, ou semelhante que possa ser instalada ...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-22 15:26:26)* *[Grok]*

Existe alguma alguma api gratuita de chatgpt, deepseek, gork, ou semelhante que possa ser instalada e integrada com python. Para produzir uma aplicação inteligente para pesquisa.

---

### 🤖 Grok *(2025-10-22 15:26:43)* *[Grok]*

Sim, existem várias opções de APIs gratuitas ou com tiers gratuitos para modelos semelhantes ao ChatGPT, como DeepSeek, Grok (da xAI) e outros LLMs open-source. Vou focar nas que podem ser integradas facilmente com Python, ideais para uma aplicação de pesquisa inteligente (por exemplo, usando RAG - Retrieval-Augmented Generation, onde o LLM processa consultas baseadas em dados pesquisados). Algumas são APIs hospedadas (com limites gratuitos), enquanto outras envolvem instalação local para uso ilimitado e privado.

Vou listar as principais opções viáveis, com instruções de instalação e integração em Python. Priorizei as gratuitas e open-source, evitando custos recorrentes. Para pesquisa, recomendo modelos que suportem raciocínio avançado (como DeepSeek ou Llama).

### 1. **DeepSeek API (Gratuita com limites, open-source)**
   DeepSeek é um modelo chinês poderoso para chat e raciocínio, similar ao GPT-4, com custo baixo (quase 2% do OpenAI em alguns casos). É gratuito via proxies como OpenRouter (tier free com limites diários) ou instalação local. Perfeito para pesquisa por seu suporte a "deep thinking" e busca integrada.

   - **Via OpenRouter (hospedado, gratuito com limites)**:
     - Crie conta gratuita em [openrouter.ai](https://openrouter.ai) e pegue a API key (tier free: ~1M tokens/mês).
     - Instale: `pip install openai requests`
     - Exemplo de código Python para chat/pesquisa:
       ```python
       import os
       from openai import OpenAI

       client = OpenAI(
           base_url="https://openrouter.ai/api/v1",
           api_key=os.getenv("OPENROUTER_API_KEY"),  # Sua key
       )

       response = client.chat.completions.create(
           model="deepseek/deepseek-chat:free",  # Modelo free
           messages=[
               {"role": "system", "content": "Você é um assistente de pesquisa inteligente."},
               {"role": "user", "content": "Pesquise e resuma os impactos da IA na educação."}
           ],
           max_tokens=500
       )
       print(response.choices[0].message.content)
       ```
     - Para app de pesquisa: Integre com bibliotecas como `langchain` para adicionar busca web (ex: via SerpAPI free tier).

   - **Instalação local (ilimitada, via Ollama)**:
     - Instale Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
     - Rode: `ollama pull deepseek-coder` (ou similar).
     - Use com Python: `pip install ollama`
       ```python
       import ollama
       response = ollama.chat(model='deepseek-coder', messages=[
           {'role': 'user', 'content': 'Resuma artigos sobre IA ética.'}
       ])
       print(response['message']['content'])
       ```
     - Vantagem: Roda no seu PC (GPU recomendada), sem limites.

### 2. **Grok API (da xAI, com créditos gratuitos)**
   Grok é o modelo da xAI (de Elon Musk), focado em raciocínio e busca real-time. Não é totalmente gratuito, mas oferece US$25 em créditos mensais grátis durante beta (até fim de 2024, prorrogável). Compatível com OpenAI SDK.

   - Instale: `pip install xai-sdk` (ou use OpenAI SDK).
   - Crie conta em [console.x.ai](https://console.x.ai) e pegue API key.
   - Exemplo Python:
     ```python
     import os
     from xai_sdk import Client

     client = Client(api_key=os.getenv("XAI_API_KEY"))
     response = client.chat.completions.create(
         model="grok-beta",
         messages=[
             {"role": "system", "content": "Assistente para pesquisa avançada."},
             {"role": "user", "content": "Analise tendências em IA para 2025."}
         ]
     )
     print(response.choices[0].message.content)
     ```
   - Para pesquisa: Suporta tool calling nativo para integrar buscas (ex: web search via API externa).
   - Limite: ~128k tokens de contexto, ideal para documentos longos.

   **Nota**: Para acesso 100% free, use via OpenRouter (mesmo setup do DeepSeek, model="xai/grok-3:free").

### 3. **Hugging Face Inference API (Gratuita para open-source LLMs)**
   Plataforma open-source com APIs gratuitas para modelos como Llama 3, Mistral ou Phi-3. Limites: ~1k requests/dia free. Ótimo para pesquisa, com suporte a embeddings para busca semântica.

   - Crie conta em [huggingface.co](https://huggingface.co) e gere token em Settings > Access Tokens.
   - Instale: `pip install huggingface_hub requests`
   - Exemplo para Llama 3 (similar a ChatGPT):
     ```python
     import requests
     API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3-8B-Instruct"
     headers = {"Authorization": f"Bearer SEU_TOKEN_AQUI"}

     def query(payload):
         response = requests.post(API_URL, headers=headers, json=payload)
         return response.json()

     output = query({
         "inputs": "Você é um pesquisador. Resuma os avanços em LLMs open-source.",
         "parameters": {"max_new_tokens": 200}
     })
     print(output)
     ```
   - Para app de pesquisa: Use `sentence-transformers` para embeddings e busque em vetores locais.

### 4. **Opções Locais Open-Source (Instaláveis, Ilimitadas)**
   Para privacidade total e sem custos, instale LLMs localmente com APIs compatíveis. Roda em CPU/GPU.

   - **Ollama (Recomendado para iniciantes)**:
     - Instale como acima.
     - Modelos free: Llama 3, Mistral, Gemma.
     - Integração Python via `ollama` package (exemplo acima).
     - Para pesquisa: Combine com `chromadb` para banco de vetores.

   - **LocalAI (API compatível com OpenAI)**:
     - Instale: `docker run -p 8080:8080 --name local-ai -ti localai/localai`
     - Baixe modelo: Via web UI.
     - Python: Use OpenAI SDK apontando para `http://localhost:8080/v1`.
       ```python
       from openai import OpenAI
       client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")
       # Resto igual ao OpenAI
       ```

   - **OpenLLM (Da BentoML)**:
     - `pip install openllm`
     - Rode: `openllm serve deepseek-coder:7b --port 3000`
     - Acesse via OpenAI SDK em `http://localhost:3000`.

### Dicas para Aplicação de Pesquisa Inteligente
- **Framework**: Use `langchain` ou `llama-index` (`pip install langchain`) para integrar LLM + busca (ex: web scraping com `beautifulsoup` + embeddings).
- **Exemplo simples de app**: Crie um script que pesquisa via Google Custom Search (free tier) e resume com DeepSeek.
- **Limites e custos**: Tiers free têm quotas (ex: 10k tokens/dia). Para produção, migre para paid ou local.
- **Recursos extras**: Consulte [Hugging Face Models](https://huggingface.co/models) para mais LLMs free, ou [cheahjs/free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources) para listas atualizadas.

Se precisar de código mais específico ou ajuda com um modelo, me diga!

---

*Conversa exportada do Grok*
*Processado em: 23/11/2025 14:36*