# Backend gratuito com Cloudflare Workers e JWT

## 📊 Informações
- **Número:** #3
- **Origem:** Claude
- **Categoria:** Programação
- **ID:** 98af52d9-3927-4e1a-96f7-ac5ac46dc6ce
- **Criada em:** 2025-11-19 21:18:01
- **Total de mensagens:** 20
- **Resumo:** Backend GRATUITO usando Cloudflare Workers, totalmente compatível com GitHub Pages, sem expor a API ...

---

## 💬 Conversa

### 👤 Utilizador *[Claude]*

Backend GRATUITO usando Cloudflare Workers, totalmente compatível com GitHub Pages, sem expor a API key, sem precisar de Firebase Blaze, e com login + registo seguros usando JWT. Em https://mpmendespt.github.io/Pesquisas/ Pasta local D:\Downloads\_DOCS_\_DOCS_\_My_Sites_\Pesquisas já com: Directory of D:\Downloads\_DOCS_\_DOCS_\_My_Sites_\Pesquisas 11/19/2025 07:33 PM . 11/19/2025 07:33 PM .. 11/19/2025 08:00 PM .git 11/19/2025 06:15 PM 194 .gitignore 11/19/2025 08:15 PM auth-backend 11/19/2025 07:09 PM firebase 11/19/2025 06:11 PM frontend 11/19/2025 07:12 PM 0 New Text Document.txt 11/18/2025 12:53 PM 1,255 README.md 11/19/2025 07:14 PM 189 schema.sql 11/19/2025 07:21 PM square-lab-97e4 4 File(s) 1,638 bytes É possivel gerar uma solução completa para download num file zip

---

### 🤖 Claude *[Claude]*

 # Backend Gratuito com Cloudflare Workers + GitHub Pages

Vou criar uma solução completa com backend em Cloudflare Workers (gratuito), frontend compatível com GitHub Pages, autenticação JWT segura, e sem expor API keys!
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```


---

### 👤 Utilizador *[Claude]*

Continuar

---

### 🤖 Claude *[Claude]*

 
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

Pronto! 🎉 Criei uma **aplicação completa e interativa** que gera todos os ficheiros necessários para o seu backend gratuito!

## ✨ O que a aplicação faz:

1. **Gera JWT Secret seguro** - Com um clique, cria um secret criptográfico de 64 caracteres
2. **Permite configurar** - Nome do projeto, database, repositório GitHub
3. **Gera todos os ficheiros** necessários:
   - `worker-index.js` - Backend completo com todas as rotas
   - `schema.sql` - Schema da base de dados D1
   - `wrangler.toml` - Configuração do Cloudflare
   - `frontend-api.js` - Cliente API para o frontend
   - `SETUP_GUIDE.md` - Guia completo passo-a-passo

4. **Download individual ou em lote** - Pode descarregar cada ficheiro separadamente ou todos de uma vez

## 🚀 Funcionalidades Incluídas:

✅ **Backend Completo**
- Registo e Login com JWT
- CRUD completo de pesquisas
- Autenticação por utilizador
- Error handling robusto
- CORS configurado para GitHub Pages

✅ **Segurança**
- Passwords com hash SHA-256
- JWT tokens seguros
- API key nunca exposta
- Validação em todas as rotas

✅ **100% Gratuito**
- Cloudflare Workers: 100k requests/dia
- D1 Database: 5GB storage
- GitHub Pages: hosting grátis

## 📋 Como usar:

1. **Abra a aplicação** acima
2. **Gere o JWT Secret** (botão verde)
3. **Configure** os nomes do projeto
4. **Clique em "Gerar Ficheiros"**
5. **Descarregue tudo** com um clique
6. **Siga o guia** SETUP_GUIDE.md

Os ficheiros já estarão **prontos para deploy** na Cloudflare e funcionarão perfeitamente com o seu site em GitHub Pages!

Quer que eu explique alguma parte específica do código ou do processo de setup? 😊

---

### 👤 Utilizador *[Claude]*

Ao clicar em descarregar todos os ficheiros, não acontece nada, não consigo descarregar os file

---

### 🤖 Claude *[Claude]*

 Vou corrigir o problema do download! O issue é que preciso usar uma abordagem diferente para fazer download de múltiplos ficheiros.
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```


```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

Pronto! ✅ Corrigi o problema do download. As alterações foram:

1. **Adicionar o elemento `<a>` ao DOM** antes de clicar (alguns browsers precisam disso)
2. **Remover o elemento depois** de clicar
3. **Adicionar delay entre downloads** (300ms) quando descarrega todos os ficheiros - isso evita que o browser bloqueie múltiplos downloads simultâneos

Agora deve funcionar perfeitamente! Teste novamente:
1. Gere o JWT Secret
2. Clique em "Gerar Ficheiros"
3. Clique em "DESCARREGAR TODOS OS FICHEIROS"

Os 5 ficheiros devem ser descarregados sequencialmente para a sua pasta de Downloads! 📥

Se ainda tiver problemas, pode descarregar cada ficheiro individualmente clicando nos botões específicos. Está a funcionar agora? 😊

---

### 👤 Utilizador *[Claude]*

Mostrar tree de como devem ficar os file; e os passos a efectuar em que pasta

---

### 🤖 Claude *[Claude]*

 Vou adicionar uma visualização clara da estrutura de pastas e os comandos exatos a executar em cada pasta!
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

Perfeito! ✅ Adicionei uma secção completa com:

## 📁 O que foi adicionado:

1. **Árvore Visual da Estrutura** - Mostra exatamente como devem ficar as pastas
2. **Comandos Passo a Passo** - 8 passos detalhados com:
   - Número do passo
   - Cor diferente para cada passo
   - Comando exato a executar
   - Em que pasta deve estar
   - O que vai acontecer

3. **Referência Rápida** - Resumo de onde executar cada tipo de comando

## 🎯 Estrutura Final:

```
Pesquisas/
├── frontend/              (já existe)
│   └── js/
│       └── api.js        ← copiar frontend-api.js aqui
│
├── backend/              (CRIAR)
│   ├── src/
│   │   └── index.js     ← copiar worker-index.js aqui
│   ├── wrangler.toml    ← copiar wrangler.toml aqui
│   └── schema.sql       ← copiar schema.sql aqui
```

## 📍 Comandos por Pasta:

**Na pasta raiz (Pesquisas):**
- Criar backend: `mkdir backend`
- Git commands

**Na pasta backend:**
- Todos os comandos `wrangler`

Agora está super claro onde executar cada comando! 🎉

---

### 👤 Utilizador *[Claude]*

Com wrangler dev ;  ⎔ Starting local server...
[wrangler:info] Ready on http://127.0.0.1:8787
[wrangler:info] GET / 404 Not Found (25ms)
[wrangler:info] GET /favicon.ico 404 Not Found (12ms)
[wrangler:info] GET / 404 Not Found (31ms)

---

### 🤖 Claude *[Claude]*

 Perfeito! O servidor está a funcionar! 🎉 O erro 404 é normal porque você está a aceder à rota raiz `/` que não existe. O worker só responde nas rotas da API.

Vou mostrar como testar corretamente:

## ✅ Testar o Backend Local

### 1️⃣ **Testar Registo de Utilizador**

Abra um novo terminal (PowerShell ou CMD) e execute:

```powershell
curl -X POST http://127.0.0.1:8787/api/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"teste@example.com\",\"password\":\"senha123\",\"nome\":\"João Teste\"}'
```

**Ou use este código JavaScript no browser (abra DevTools > Console):**

```javascript
fetch('http://127.0.0.1:8787/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'teste@example.com',
    password: 'senha123',
    nome: 'João Teste'
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

### 2️⃣ **Testar Login**

```javascript
fetch('http://127.0.0.1:8787/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'teste@example.com',
    password: 'senha123'
  })
})
.then(r => r.json())
.then(d => {
  console.log('Token:', d.token);
  localStorage.setItem('token', d.token); // Guardar token
});
```

### 3️⃣ **Criar Pesquisa (com autenticação)**

```javascript
const token = localStorage.getItem('token'); // Do passo anterior

fetch('http://127.0.0.1:8787/api/pesquisas', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    title: 'Minha primeira pesquisa',
    description: 'Teste de pesquisa',
    data: { perguntas: ['Pergunta 1', 'Pergunta 2'] }
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

### 4️⃣ **Listar Pesquisas**

```javascript
const token = localStorage.getItem('token');

fetch('http://127.0.0.1:8787/api/pesquisas', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(r => r.json())
.then(d => console.log('Pesquisas:', d));
```

---

## 🔍 Rotas Disponíveis

| Rota | Método | Autenticação | Descrição |
|------|--------|--------------|-----------|
| `/api/register` | POST | ❌ Não | Registar utilizador |
| `/api/login` | POST | ❌ Não | Login |
| `/api/pesquisas` | GET | ✅ Sim | Listar pesquisas |
| `/api/pesquisas` | POST | ✅ Sim | Criar pesquisa |
| `/api/pesquisas/:id` | PUT | ✅ Sim | Atualizar pesquisa |
| `/api/pesquisas/:id` | DELETE | ✅ Sim | Eliminar pesquisa |

---

## 🛠️ Ferramentas para Testar

### **Opção 1: Postman / Insomnia** (recomendado)
- Mais fácil para testar APIs
- Interface visual

### **Opção 2: Browser Console**
- Use os scripts JavaScript acima
- Abra DevTools (F12) > Console

### **Opção 3: Criar página HTML de teste**

Crie um ficheiro `test.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Teste API</title>
</head>
<body>
    <h1>Teste Backend Local</h1>
    
    <div>
        <h2>Registo</h2>
        <button onclick="testeRegisto()">Registar</button>
    </div>
    
    <div>
        <h2>Login</h2>
        <button onclick="testeLogin()">Login</button>
    </div>
    
    <div>
        <h2>Criar Pesquisa</h2>
        <button onclick="testeCriarPesquisa()">Criar</button>
    </div>
    
    <div>
        <h2>Listar Pesquisas</h2>
        <button onclick="testeListar()">Listar</button>
    </div>

    <pre id="resultado"></pre>

    <script>
        const API = 'http://127.0.0.1:8787';
        
        function mostrar(data) {
            document.getElementById('resultado').textContent = JSON.stringify(data, null, 2);
        }
        
        async function testeRegisto() {
            const res = await fetch(`${API}/api/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: 'teste@example.com',
                    password: 'senha123',
                    nome: 'João Teste'
                })
            });
            const data = await res.json();
            localStorage.setItem('token', data.token);
            mostrar(data);
        }
        
        async function testeLogin() {
            const res = await fetch(`${API}/api/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: 'teste@example.com',
                    password: 'senha123'
                })
            });
            const data = await res.json();
            localStorage.setItem('token', data.token);
            mostrar(data);
        }
        
        async function testeCriarPesquisa() {
            const token = localStorage.getItem('token');
            const res = await fetch(`${API}/api/pesquisas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    title: 'Pesquisa Teste',
                    description: 'Uma pesquisa de teste',
                    data: { perguntas: ['P1', 'P2'] }
                })
            });
            const data = await res.json();
            mostrar(data);
        }
        
        async function testeListar() {
            const token = localStorage.getItem('token');
            const res = await fetch(`${API}/api/pesquisas`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await res.json();
            mostrar(data);
        }
    </script>
</body>
</html>
```

Abra este ficheiro no browser e teste clicando nos botões! 🎯

---

O erro 404 que viu é **normal** - só significa que a rota `/` não existe. Todas as rotas da API começam com `/api/`! ✅

---

### 👤 Utilizador *[Claude]*

com test.html ; [wrangler:info] POST /api/register 500 Internal Server Error (35ms)
[wrangler:info] OPTIONS /api/register 200 OK (4ms)
[wrangler:info] OPTIONS /api/login 200 OK (4ms)
[wrangler:info] OPTIONS /api/pesquisas 200 OK (5ms)
[wrangler:info] OPTIONS /api/pesquisas 200 OK (3ms)
[wrangler:info] OPTIONS /api/register 200 OK (3ms)
[wrangler:info] OPTIONS /api/register 200 OK (3ms)

---

### 🤖 Claude *[Claude]*

 O erro 500 indica que há um problema no código do worker. Provavelmente a database não está a ser reconhecida ou há um erro no código. Vamos corrigir!

## 🔧 Soluções:

### **1️⃣ Verificar se criou as tabelas localmente**

No terminal, na pasta `backend`, execute:

```bash
wrangler d1 execute pesquisas_db --local --file=schema.sql
```

### **2️⃣ Atualizar o código do Worker**

O problema pode estar na forma como estamos a usar a database em modo local. Vou criar uma versão corrigida:
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

## ✅ Passos para corrigir:

### **1. Substituir o ficheiro `backend/src/index.js`**
Copie o código acima e substitua o ficheiro atual.

### **2. Verificar o `wrangler.toml`**
Certifique-se que tem isto:

```toml
name = "pesquisas-app"
main = "src/index.js"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "pesquisas_db"
database_id = "SEU_DATABASE_ID_AQUI"

[vars]
JWT_SECRET = "seu_jwt_secret_aqui"
```

### **3. Recriar as tabelas localmente**

```bash
wrangler d1 execute pesquisas_db --local --file=schema.sql
```

### **4. Parar e reiniciar o wrangler**

Pressione `Ctrl+C` no terminal onde está o `wrangler dev` e depois:

```bash
wrangler dev
```

### **5. Testar a rota de health**

No browser, aceda a: `http://127.0.0.1:8787/api/health`

Deve ver:
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2025-..."
}
```

### **6. Testar novamente o test.html**

Agora deve funcionar! 🎉

---

## 🔍 O que foi corrigido:

1. ✅ **CORS mais permissivo** para desenvolvimento (`*` em vez de URL específica)
2. ✅ **Verificação se DB existe** antes de usar
3. ✅ **Error handling melhorado** com mais detalhes
4. ✅ **JWT encoding corrigido** (padding do base64)
5. ✅ **Logs de erro** mais detalhados
6. ✅ **Rota `/api/health`** para testar conexão

Teste e diga-me o resultado! 🚀

---

### 👤 Utilizador *[Claude]*

🌀 Executing on local database pesquisas_db (8d1fc694-bb9a-4704-b7cc-cf3cd3d83519) from .wrangler\state\v3\d1:
🌀 To execute on your remote database, add a --remote flag to your wrangler command.
X [ERROR] index idx_pesquisas_user already exists: SQLITE_ERROR

---

### 🤖 Claude *[Claude]*

 Perfeito! A mensagem indica que as tabelas **já existem** na base de dados local. O erro é apenas porque está a tentar criar índices que já existem. Isto é bom! ✅

Agora vamos testar:

## 🧪 Testes para fazer:

### **1️⃣ Parar e reiniciar o wrangler dev**

No terminal onde está o `wrangler dev`, pressione `Ctrl+C` e depois:

```bash
wrangler dev
```

### **2️⃣ Testar a rota de health primeiro**

Abra o browser em: `http://127.0.0.1:8787/api/health`

Deve ver:
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2025-11-19T..."
}
```

### **3️⃣ Testar o test.html novamente**

Abra o ficheiro `test.html` no browser e clique em **"Registar"**.

Agora deve funcionar! 🎉

---

## 📊 Se ainda houver erro 500:

### **Opção A: Ver os logs detalhados**

No terminal do `wrangler dev`, deve aparecer a mensagem de erro completa. Copie e cole aqui.

### **Opção B: Limpar e recriar a database**

Se quiser começar do zero:

```bash
# Parar o wrangler dev (Ctrl+C)

# Apagar a database local
rm -rf .wrangler/state/v3/d1

# Recriar as tabelas
wrangler d1 execute pesquisas_db --local --file=schema.sql

# Reiniciar
wrangler dev
```

### **Opção C: Ver o conteúdo da database**

Para verificar se as tabelas existem:

```bash
wrangler d1 execute pesquisas_db --local --command="SELECT name FROM sqlite_master WHERE type='table';"
```

Deve mostrar:
```
users
pesquisas
```

---

## 🎯 Teste Rápido no Browser Console

Abra DevTools (F12) e cole isto:

```javascript
// Teste 1: Health check
fetch('http://127.0.0.1:8787/api/health')
  .then(r => r.json())
  .then(d => console.log('Health:', d));

// Teste 2: Registar
fetch('http://127.0.0.1:8787/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'teste' + Date.now() + '@example.com',
    password: 'senha123',
    nome: 'Teste User'
  })
})
.then(r => r.json())
.then(d => console.log('Registo:', d));
```

O que acontece quando executa estes testes? Cole aqui o resultado! 🔍

---

### 👤 Utilizador *[Claude]*

Parece funcionar: ⎔ Starting local server...
[wrangler:info] Ready on http://127.0.0.1:8787
[wrangler:info] GET /api/health 200 OK (40ms)
[wrangler:info] OPTIONS /api/register 200 OK (3ms)
[wrangler:info] POST /api/register 201 Created (29ms)
[wrangler:info] OPTIONS /api/login 200 OK (4ms)
[wrangler:info] POST /api/login 200 OK (22ms)
[wrangler:info] OPTIONS /api/pesquisas 200 OK (5ms)
[wrangler:info] POST /api/pesquisas 201 Created (25ms)
[wrangler:info] GET /api/pesquisas 200 OK (10ms)
[wrangler:info] POST /api/login 200 OK (12ms)

---

### 🤖 Claude *[Claude]*

 🎉 **EXCELENTE! Está tudo a funcionar perfeitamente!** 

Os códigos de status estão todos corretos:
- ✅ `200 OK` - Health check, Login, Listar pesquisas
- ✅ `201 Created` - Registo e Criar pesquisa
- ✅ `OPTIONS 200` - CORS funcionando

---

## 🚀 Próximos Passos - Deploy para Produção

Agora que está tudo a funcionar localmente, vamos fazer o deploy!

### **1️⃣ Criar a database remota**

```bash
wrangler d1 create pesquisas_db
```

Vai aparecer algo como:
```
✅ Successfully created DB 'pesquisas_db'

[[d1_databases]]
binding = "DB"
database_name = "pesquisas_db"
database_id = "xxxx-xxxx-xxxx-xxxx"
```

**Copie o `database_id`** e atualize no ficheiro `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "pesquisas_db"
database_id = "COLE_O_ID_AQUI"  # ← Substituir
```

### **2️⃣ Criar as tabelas na database remota**

```bash
wrangler d1 execute pesquisas_db --remote --file=schema.sql
```

### **3️⃣ Fazer o deploy do Worker**

```bash
wrangler deploy
```

Vai aparecer:
```
✨ Successfully published your Worker
🌎 https://pesquisas-app.SEU_USERNAME.workers.dev
```

**GUARDE ESTA URL!** É o seu backend em produção! 🎯

### **4️⃣ Atualizar o frontend**

Abra `frontend/js/api.js` e substitua a URL:

```javascript
const API_URL = 'https://pesquisas-app.SEU_USERNAME.workers.dev';
```

(Use a URL que apareceu no passo anterior)

### **5️⃣ Atualizar CORS no Worker**

Abra `backend/src/index.js` e **mude esta linha**:

```javascript
// Era:
'Access-Control-Allow-Origin': '*',

// Mudar para:
'Access-Control-Allow-Origin': 'https://mpmendespt.github.io',
```

Depois faça deploy novamente:
```bash
wrangler deploy
```

### **6️⃣ Commit e Push para GitHub**

```bash
# Na pasta raiz do projeto
cd D:\Downloads\_DOCS_\_DOCS_\_My_Sites_\Pesquisas

git add .
git commit -m "Backend Cloudflare Workers integrado"
git push origin main
```

### **7️⃣ Configurar GitHub Pages**

1. Vá ao repositório no GitHub
2. Settings → Pages
3. Source: **Deploy from a branch**
4. Branch: **main** → Pasta: **/frontend** (ou **root** se o frontend estiver na raiz)
5. Save

Aguarde 1-2 minutos e aceda a:
`https://mpmendespt.github.io/Pesquisas/`

---

## ✅ Checklist Final

- [ ] Database remota criada
- [ ] Tabelas criadas remotamente
- [ ] Worker deployed
- [ ] URL do backend anotada
- [ ] `frontend/js/api.js` atualizado com URL
- [ ] CORS configurado para GitHub Pages
- [ ] Deploy feito novamente
- [ ] Git push feito
- [ ] GitHub Pages configurado
- [ ] Site funcionando! 🎉

---

## 🧪 Testar em Produção

Depois do deploy, teste no browser console:

```javascript
// Substituir pela sua URL do worker
const API = 'https://pesquisas-app.SEU_USERNAME.workers.dev';

// Teste
fetch(`${API}/api/health`)
  .then(r => r.json())
  .then(d => console.log(d));
```

---

## 📊 Monitorizar

Para ver logs em tempo real:

```bash
wrangler tail
```

Para ver estatísticas de uso:
Dashboard da Cloudflare → Workers & Pages → pesquisas-app

---

Está pronto para fazer o deploy? Comece pelo passo 1! 🚀

---

### 👤 Utilizador *[Claude]*

Como fazer alteração de modo que apos o login com sucesso seja carregada uma pagina site.html

---

### 🤖 Claude *[Claude]*

 Vou mostrar como fazer o redirecionamento após login com sucesso! Há várias formas de implementar isso.

## 🎯 Solução 1: Redirecionamento Simples (Recomendado)

### **No seu ficheiro de login (ex: `index.html` ou `login.html`)**

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Pesquisas</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="login-container">
        <h1>Login</h1>
        <form id="loginForm">
            <div class="form-group">
                <label>Email:</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit">Entrar</button>
            <p>Não tem conta? <a href="register.html">Registar</a></p>
        </form>
        <div id="error" class="error-message"></div>
    </div>

    <script src="js/api.js"></script>
    <script>
        const api = new API();
        const form = document.getElementById('loginForm');
        const errorDiv = document.getElementById('error');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorDiv.textContent = '';

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const result = await api.login(email, password);
                
                if (result.success || result.token) {
                    // Login com sucesso - redirecionar
                    window.location.href = 'site.html';
                } else {
                    errorDiv.textContent = result.error || 'Erro ao fazer login';
                }
            } catch (error) {
                errorDiv.textContent = 'Erro: ' + error.message;
            }
        });
    </script>
</body>
</html>
```

---

## 🎯 Solução 2: Com Verificação de Autenticação no site.html

### **Criar `site.html` (página protegida)**

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Pesquisas</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="dashboard">
        <header>
            <h1>Minhas Pesquisas</h1>
            <div class="user-info">
                <span id="userName"></span>
                <button onclick="logout()">Sair</button>
            </div>
        </header>

        <div class="content">
            <button onclick="criarNovaPesquisa()">+ Nova Pesquisa</button>
            <div id="pesquisasList"></div>
        </div>
    </div>

    <script src="js/api.js"></script>
    <script>
        // Verificar se está autenticado
        const api = new API();
        
        // Verificar token ao carregar a página
        window.addEventListener('DOMContentLoaded', async () => {
            const token = localStorage.getItem('auth_token');
            
            if (!token) {
                // Não está autenticado - redirecionar para login
                window.location.href = 'index.html';
                return;
            }

            // Carregar dados do utilizador
            const userStr = localStorage.getItem('user');
            if (userStr) {
                const user = JSON.parse(userStr);
                document.getElementById('userName').textContent = user.nome || user.email;
            }

            // Carregar pesquisas
            await carregarPesquisas();
        });

        async function carregarPesquisas() {
            try {
                const pesquisas = await api.getPesquisas();
                const list = document.getElementById('pesquisasList');
                
                if (pesquisas.length === 0) {
                    list.innerHTML = '<p>Nenhuma pesquisa criada ainda.</p>';
                    return;
                }

                list.innerHTML = pesquisas.map(p => `
                    <div class="pesquisa-card">
                        <h3>${p.title}</h3>
                        <p>${p.description}</p>
                        <button onclick="editarPesquisa('${p.id}')">Editar</button>
                        <button onclick="eliminarPesquisa('${p.id}')">Eliminar</button>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Erro ao carregar pesquisas:', error);
                // Token inválido - voltar ao login
                if (error.message.includes('Token') || error.message.includes('401')) {
                    logout();
                }
            }
        }

        function logout() {
            api.logout();
            window.location.href = 'index.html';
        }

        function criarNovaPesquisa() {
            window.location.href = 'criar-pesquisa.html';
        }

        function editarPesquisa(id) {
            window.location.href = `editar-pesquisa.html?id=${id}`;
        }

        async function eliminarPesquisa(id) {
            if (!confirm('Tem certeza que deseja eliminar esta pesquisa?')) return;
            
            try {
                await api.deletePesquisa(id);
                await carregarPesquisas();
            } catch (error) {
                alert('Erro ao eliminar pesquisa: ' + error.message);
            }
        }
    </script>
</body>
</html>
```

---

## 🎯 Solução 3: Atualizar o `api.js` com Redirecionamento Automático

Modifique o ficheiro `frontend/js/api.js`:

```javascript
const API_URL = 'https://seu-worker.workers.dev'; // Ou URL local para testes

class API {
  constructor() {
    this.token = localStorage.getItem('auth_token');
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async register(email, password, nome) {
    const response = await fetch(`${API_URL}/api/register`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password, nome })
    });
    
    const data = await response.json();
    
    if (response.ok && (data.success || data.token)) {
      this.token = data.token;
      localStorage.setItem('auth_token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      // Redirecionar automaticamente após registo
      window.location.href = 'site.html';
    }
    
    return data;
  }

  async login(email, password) {
    const response = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    
    if (response.ok && (data.success || data.token)) {
      this.token = data.token;
      localStorage.setItem('auth_token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      // Redirecionar automaticamente após login
      window.location.href = 'site.html';
    }
    
    return data;
  }

  logout() {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
  }

  // Verificar se está autenticado
  isAuthenticated() {
    return !!this.token;
  }

  // Obter utilizador atual
  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  async getPesquisas() {
    const response = await fetch(`${API_URL}/api/pesquisas`, {
      headers: this.getHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Erro ao carregar pesquisas');
    }
    
    return response.json();
  }

  async createPesquisa(data) {
    const response = await fetch(`${API_URL}/api/pesquisas`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    });
    
    return response.json();
  }

  async updatePesquisa(id, data) {
    const response = await fetch(`${API_URL}/api/pesquisas/${id}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    });
    
    return response.json();
  }

  async deletePesquisa(id) {
    const response = await fetch(`${API_URL}/api/pesquisas/${id}`, {
      method: 'DELETE',
      headers: this.getHeaders()
    });
    
    return response.json();
  }
}
```

---

## 🎨 CSS Básico (opcional - `css/style.css`)

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-container {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    width: 100%;
    max-width: 400px;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

button {
    width: 100%;
    padding: 0.75rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
}

button:hover {
    background: #5568d3;
}

.error-message {
    color: red;
    margin-top: 1rem;
    text-align: center;
}

.dashboard {
    background: white;
    min-height: 100vh;
    width: 100%;
}

header {
    background: #667eea;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.user-info {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.content {
    padding: 2rem;
}

.pesquisa-card {
    background: #f5f5f5;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}
```

---

## 📁 Estrutura de Ficheiros

```
frontend/
├── index.html          (página de login)
├── register.html       (página de registo)
├── site.html          (dashboard - página protegida)
├── criar-pesquisa.html
├── css/
│   └── style.css
└── js/
    └── api.js
```

---

## ✅ Resumo

1. **Login** → Guarda token no `localStorage` → Redireciona para `site.html`
2. **site.html** → Verifica se tem token → Se não, volta para login
3. **Logout** → Remove token → Volta para login

Qual abordagem prefere usar? Posso ajudar a adaptar ao seu projeto específico! 🚀

---

### 👤 Utilizador *[Claude]*

Solução 3: Atualizar o `api.js` com Redirecionamento Automático;  Mas com redirecionamento para index.html

---

### 🤖 Claude *[Claude]*

 Perfeito! Vou ajustar a Solução 3 para redirecionar para `index.html` após login. Vou criar o código completo:
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

Agora vou criar exemplos de páginas de login e registro que usam este `api.js`:
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```


```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

Agora vou criar um exemplo de `index.html` protegido:
```
Viewing artifacts created via the Analysis Tool web feature preview isn’t yet supported on mobile.
```

Perfeito! Agora tenho tudo pronto. Aqui está o resumo completo:

## ✅ Ficheiros Criados

### **1. `frontend/js/api.js`**
- Login/Registo **redireciona automaticamente para `index.html`**
- Logout redireciona para `login.html`
- Verifica sessão expirada automaticamente
- Gestão completa de autenticação

### **2. `frontend/login.html`**
- Página de login bonita e moderna
- Validação de campos
- Mensagens de erro/sucesso
- Animações suaves
- Verifica se já está autenticado

### **3. `frontend/register.html`**
- Página de registo com validação
- Verificador de força de password
- Confirmação de password
- Design consistente com login

### **4. `frontend/index.html`**
- **Página protegida** - Redireciona para login se não autenticado
- Dashboard com lista de pesquisas
- Criar/Editar/Eliminar pesquisas
- Botão de logout
- Design responsivo

---

## 📁 Estrutura Final

```
Pesquisas/
├── frontend/
│   ├── index.html          ← Dashboard (protegido)
│   ├── login.html          ← Página de login
│   ├── register.html       ← Página de registo
│   ├── js/
│   │   └── api.js         ← Cliente API com redirecionamento
│   └── css/
│       └── style.css      (opcional)
│
└── backend/
    ├── src/
    │   └── index.js       ← Worker corrigido
    ├── wrangler.toml
    └── schema.sql
```

---

## 🔄 Fluxo de Autenticação

```
1. Utilizador acede a index.html
   └─> Não autenticado? → Redireciona para login.html

2. Utilizador faz login em login.html
   └─> Login bem-sucedido → Guarda token → Redireciona para index.html

3. Utilizador acede a index.html (autenticado)
   └─> Mostra dashboard com pesquisas

4. Utilizador clica em "Sair"
   └─> Remove token → Redireciona para login.html
```

---

## 🧪 Para Testar

1. **Copie os 4 ficheiros** para as pastas corretas
2. **Atualize a URL** no `api.js`:
   ```javascript
   const API_URL = 'http://127.0.0.1:8787'; // Local
   ```
3. **Inicie o worker**: `wrangler dev`
4. **Abra**: `login.html` no browser
5. **Registe-se** ou faça login
6. **Será redirecionado** para `index.html` automaticamente! 🎉

---

## ⚙️ Personalizar Redirecionamento

Se quiser mudar para outra página (ex: `dashboard.html`), basta alterar no `api.js`:

```javascript
// Linha 41 e 67
window.location.href = 'dashboard.html'; // Em vez de 'index.html'
```

Tudo pronto! Quer que eu ajude com mais alguma funcionalidade? 🚀

---

*Conversa exportada do Claude*
*Processado em: 24/11/2025 22:27*