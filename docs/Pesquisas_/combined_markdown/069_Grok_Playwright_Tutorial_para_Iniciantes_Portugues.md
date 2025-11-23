# Playwright Tutorial para Iniciantes Portugues

## 📊 Informações
- **Número:** #69
- **Origem:** Grok
- **Categoria:** Programação
- **ID:** 068b64ee-5abb-4282-9797-7aa3a1b909f0
- **Criada em:** 2025-10-30 17:25:37Z
- **Atualizada em:** 2025-10-30 17:46:13Z
- **Total de mensagens:** 6
- **Resumo:** Playwright tutorial for beginners...

---

## 💬 Conversa

### 👤 Utilizador *(2025-10-30 17:25:37)* *[Grok]*

Playwright tutorial for beginners

---

### 🤖 Grok *(2025-10-30 17:26:01)* *[Grok]*

# Playwright Tutorial for Beginners

Welcome to this beginner-friendly tutorial on Playwright! Playwright is a powerful, open-source automation library developed by Microsoft for end-to-end testing of web applications. It allows you to automate interactions with browsers like Chromium (Chrome/Edge), Firefox, and WebKit (Safari) across Windows, Linux, and macOS. Whether you're testing a simple webpage or a complex single-page app (SPA), Playwright handles it reliably, supporting headless mode (invisible browser) or headed mode (visible browser) for debugging.

This tutorial is based on the official Playwright documentation and focuses on Node.js setup, as it's the most common starting point. By the end, you'll have a basic test running. No prior experience with testing frameworks is required—just basic JavaScript knowledge.

## Why Playwright?
- **Cross-browser support**: Test on multiple browsers out of the box.
- **Fast and reliable**: Auto-waits for elements, handles dynamic content, and runs tests in parallel.
- **Rich features**: Built-in assertions, screenshots, videos, tracing, and mobile emulation.
- **Easy to learn**: Simple API with powerful locators (e.g., by text, role, or CSS).

Let's dive in!

## Step 1: System Requirements
Before installing, ensure your machine meets these basics:
- **Node.js**: Version 20.x, 22.x, or 24.x (download from [nodejs.org](https://nodejs.org)).
- **OS**:
  - Windows: 11+ or Server 2019+ (or WSL).
  - macOS: 14 (Ventura) or later.
  - Linux: Debian 12/13, Ubuntu 22.04/24.04 (x86-64 or arm64).

Run `node --version` in your terminal to check.

## Step 2: Installation
We'll use npm (Node Package Manager) to set up a new project. Open your terminal and navigate to a folder where you want your project.

1. Initialize a new Playwright project:
   ```
   npm init playwright@latest
   ```

2. During setup, you'll be prompted:
   - **Language**: Choose TypeScript (recommended for beginners) or JavaScript.
   - **Tests folder**: Default is `tests` (or `e2e` if `tests` exists).
   - **GitHub Actions**: Yes, for easy CI integration.
   - **Install browsers**: Yes (downloads Chromium, Firefox, WebKit).

This command creates a project scaffold:
```
my-project/
├── playwright.config.ts      # Configuration file
├── package.json
├── tests/
│   └── example.spec.ts      # Your first test file
└── tests-examples/
    └── demo-todo-app.spec.ts # Advanced example
```

If you have an existing Node.js project, run `npm install -D @playwright/test` instead, then `npx playwright install`.

**Pro Tip**: Install the official [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) for code snippets, IntelliSense, and a test runner UI.

## Step 3: Understanding Basic Concepts
Before writing code, let's cover the fundamentals. Playwright revolves around a few core ideas:

- **Browser**: Launches a full browser instance (e.g., Chromium). Tests run in isolated contexts for speed and reliability.
- **Page**: Represents a single tab or webpage where you interact with elements.
- **Locator**: A way to find elements on the page (e.g., by text, CSS selector, or ARIA role). Playwright auto-waits for them to appear.
- **Actions**: Methods to interact, like `click()`, `fill()`, or `check()`.
- **Assertions**: Built-in checks like `toBeVisible()` or `toHaveText()` to verify results.

These are demonstrated in the example files created during installation. Here's a peek at a minimal test from `example.spec.ts` (TypeScript version):

```typescript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  
  // Expect a title "to contain" a substring
  await expect(page).toHaveTitle(/Playwright/);
  
  // Create a locator
  const getStarted = page.getByText('Get started');
  
  // Expect an element "to be visible"
  await expect(getStarted).toBeVisible();
  
  // Click it
  await getStarted.click();
  
  // Expect navigation
  await expect(page).toHaveURL(/docs\/intro/);
});
```

- `test()`: Defines a test block.
- `page`: A fixture (pre-configured object) for the webpage.
- `goto()`: Navigates to a URL.
- `expect()`: Asserts conditions.

Run this test to see it in action (Step 4)!

For a richer example, check `demo-todo-app.spec.ts` in `tests-examples/`, which tests a todo list app with actions like adding items and assertions on the list length.

## Step 4: Running Your First Test
From your project root, run:
```
npx playwright test
```

- This executes all tests in `tests/` across all browsers (Chromium, Firefox, WebKit) in headless mode, in parallel.
- Output shows pass/fail status in the terminal.

**Customize Runs**:
- Headed mode (see the browser): `npx playwright test --headed`
- Single browser: `npx playwright test --project=chromium`
- One file: `npx playwright test tests/example.spec.ts`
- Debug with UI: `npx playwright test --ui` (opens a dashboard for watch mode, step-by-step debugging, and time travel).

If tests fail, Playwright captures screenshots and videos automatically in `test-results/`.

## Step 5: Generating Reports
After running tests, view an interactive HTML report:
```
npx playwright show-report
```

It includes:
- Dashboard with filters (by browser, status: passed/failed/skipped).
- Detailed traces: Errors, console logs, network requests, and DOM snapshots.
- Attachments: Screenshots/videos on failure.

## Step 6: Writing Your Own Test
Let's create a simple test for a search on example.com.

1. In `tests/`, create `search.spec.ts`:
   ```typescript
   import { test, expect } from '@playwright/test';

   test('search for Playwright', async ({ page }) => {
     await page.goto('https://example.com');
     
     // Locate and fill the search input
     await page.fill('input[name="q"]', 'Playwright');
     
     // Click search
     await page.click('input[type="submit"]');
     
     // Assert results
     await expect(page.locator('h3')).toContainText('Playwright');
   });
   ```

2. Run it: `npx playwright test search.spec.ts`

**Key Takeaways**:
- Use `page.locator()` for robust element selection (e.g., `page.getByRole('button', { name: 'Submit' })`).
- Always use `await` for async actions.
- Assertions prevent flaky tests.

## Step 7: Configuration Tweaks
Edit `playwright.config.ts` for custom setups:
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',  // For your app
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Add more projects for other browsers
  ],
});
```

## Next Steps
- **Learn More**: Dive into [Locators](https://playwright.dev/docs/locators) and [Actions](https://playwright.dev/docs/api/class-page#page-click).
- **Advanced Topics**: API testing, mobile emulation, CI/CD with GitHub Actions.
- **Practice**: Clone the [Playwright Examples repo](https://github.com/microsoft/playwright/tree/main/examples) or test your own site.
- **Update Playwright**: `npx playwright install --with-deps` for latest browsers.

If you run into issues, check the [official docs](https://playwright.dev/docs/intro) or community forums. Happy testing! 🚀

---

### 👤 Utilizador *(2025-10-30 17:27:12)* *[Grok]*

Playwright tutorial for beginners. Em Portugues

---

### 🤖 Grok *(2025-10-30 17:27:55)* *[Grok]*

Aqui está um tutorial básico de Playwright para iniciantes em português. O Playwright é uma ferramenta de automação de testes para navegadores, que permite testar aplicações web de forma eficiente em Chromium, Firefox e WebKit. Este tutorial cobre os conceitos iniciais e exemplos práticos.

---

### **Tutorial de Playwright para Iniciantes (em Português)**

#### **O que é o Playwright?**
O Playwright é uma biblioteca de automação de testes de código aberto, mantida pela Microsoft, que permite interagir com navegadores para realizar ações como clicar em botões, preencher formulários, tirar screenshots e testar funcionalidades de sites. Ele é amplamente utilizado para testes de ponta a ponta (end-to-end) e suporta JavaScript/TypeScript, Python, Java e C#.

#### **Pré-requisitos**
- **Node.js** instalado (versão 14 ou superior). Baixe em [nodejs.org](https://nodejs.org).
- Conhecimento básico de JavaScript ou TypeScript.
- Um editor de código, como Visual Studio Code.

---

### **Passo 1: Instalando o Playwright**
1. **Crie um novo projeto**:
   Crie uma pasta para o projeto e inicialize um projeto Node.js:
   ```bash
   mkdir playwright-tutorial
   cd playwright-tutorial
   npm init -y
   ```

2. **Instale o Playwright**:
   Execute o comando abaixo para instalar o Playwright e suas dependências:
   ```bash
   npm install --save-dev playwright
   ```

3. **Instale os navegadores**:
   O Playwright precisa baixar os binários dos navegadores (Chromium, Firefox e WebKit). Execute:
   ```bash
   npx playwright install
   ```

---

### **Passo 2: Criando seu primeiro script**
Crie um arquivo chamado `exemplo.js` na pasta do projeto. Este script abrirá um site, navegará e tirará um screenshot.

```javascript
const { chromium } = require('playwright');

(async () => {
  // Inicia o navegador Chromium
  const browser = await chromium.launch({ headless: false }); // headless: false mostra o navegador
  const page = await browser.newPage();

  // Navega até um site
  await page.goto('https://www.example.com');

  // Tira um screenshot da página
  await page.screenshot({ path: 'screenshot.png' });

  // Fecha o navegador
  await browser.close();
})();
```

**Explicação do código**:
- `chromium.launch`: Inicia o navegador Chromium. Use `headless: true` para rodar sem interface gráfica.
- `browser.newPage`: Cria uma nova aba no navegador.
- `page.goto`: Navega até a URL especificada.
- `page.screenshot`: Salva uma captura de tela da página.
- `browser.close`: Fecha o navegador.

**Executando o script**:
No terminal, execute:
```bash
node exemplo.js
```
Isso abrirá o navegador, acessará o site `example.com` e salvará um screenshot como `screenshot.png`.

---

### **Passo 3: Interagindo com elementos da página**
O Playwright permite interagir com elementos HTML, como botões, campos de texto e links. Aqui está um exemplo que preenche um formulário de busca no Google:

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  // Navega até o Google
  await page.goto('https://www.google.com');

  // Preenche o campo de busca
  await page.fill('input[name="q"]', 'Playwright tutorial');

  // Pressiona Enter
  await page.press('input[name="q"]', 'Enter');

  // Aguarda os resultados carregarem
  await page.waitForTimeout(2000); // Espera 2 segundos

  // Tira um screenshot
  await page.screenshot({ path: 'google_search.png' });

  await browser.close();
})();
```

**Explicação**:
- `page.fill`: Preenche um campo de texto com base em um seletor CSS.
- `page.press`: Simula pressionar uma tecla (neste caso, Enter).
- `page.waitForTimeout`: Aguarda um tempo específico (em milissegundos).

Execute o script com `node exemplo.js`.

---

### **Passo 4: Testando com Playwright Test**
O Playwright também oferece uma ferramenta de teste chamada `@playwright/test`, ideal para escrever testes automatizados.

1. **Instale o Playwright Test**:
   ```bash
   npm install --save-dev @playwright/test
   ```

2. **Crie um teste**:
   Crie um arquivo chamado `teste.spec.js`:
   ```javascript
   const { test, expect } = require('@playwright/test');

   test('Verifica o título do Google', async ({ page }) => {
     await page.goto('https://www.google.com');
     const title = await page.title();
     expect(title).toBe('Google');
   });
   ```

3. **Execute o teste**:
   ```bash
   npx playwright test
   ```
   Isso rodará o teste e verificará se o título da página é "Google". O resultado será exibido no terminal.

---

### **Passo 5: Recursos úteis do Playwright**
- **Seletores**: Use seletores CSS ou XPath para encontrar elementos:
  ```javascript
  await page.click('button >> text="Clique aqui"'); // Clica em um botão com texto específico
  ```
- **Navegação em múltiplos navegadores**:
  ```javascript
  const { firefox, webkit } = require('playwright');
  const browser = await firefox.launch(); // ou webkit.launch()
  ```
- **Gravar interações**: Gere scripts automaticamente com o comando:
  ```bash
  npx playwright codegen https://www.example.com
  ```
  Isso abre um navegador e grava suas ações em um script.

- **Relatórios de teste**: O Playwright Test gera relatórios detalhados:
  ```bash
  npx playwright test --reporter=html
  ```
  Após executar, abra o relatório com:
  ```bash
  npx playwright show-report
  ```

---

### **Dicas adicionais**
- **Headless vs. Headful**: Use `headless: true` para testes mais rápidos em servidores CI/CD, ou `headless: false` para depuração.
- **Timeouts**: Configure tempos limite para ações com `page.setDefaultTimeout(5000)` (em milissegundos).
- **Documentação oficial**: Consulte a [documentação do Playwright](https://playwright.dev/docs/intro) para mais detalhes.
- **Comunidade**: Participe de fóruns no X ou Stack Overflow para tirar dúvidas.

---

### **Exemplo avançado: Testando um login**
Aqui está um exemplo que testa um formulário de login:

```javascript
const { test, expect } = require('@playwright/test');

test('Teste de login', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('#username', 'meu_usuario');
  await page.fill('#password', 'minha_senha');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('https://example.com/dashboard');
});
```

Substitua as URLs e seletores pelos valores reais do site que você está testando.

---

### **Próximos passos**
- Explore recursos como testes paralelos, manipulação de cookies e interceptação de requisições HTTP.
- Use o Playwright para testar APIs com `page.request`.
- Integre com ferramentas de CI/CD, como GitHub Actions.

Se precisar de exemplos mais específicos ou explicações detalhadas sobre algum tópico, é só pedir!

---

### 👤 Utilizador *(2025-10-30 17:45:17)* *[Grok]*

Diferenças entre Playwright e Selenium

---

### 🤖 Grok *(2025-10-30 17:46:13)* *[Grok]*

Aqui, I can provide a detailed comparison between Playwright and Selenium in Portuguese, focusing on their key differences to help you understand which tool might better suit your needs for web automation and testing.

---

### **Diferenças entre Playwright e Selenium**

O Playwright e o Selenium são ferramentas populares para automação de testes e interação com navegadores, mas possuem abordagens, recursos e casos de uso distintos. Abaixo está uma comparação detalhada em português, cobrindo aspectos como arquitetura, funcionalidades, desempenho e facilidade de uso.

---

### **1. Introdução às Ferramentas**
- **Playwright**:
  - Desenvolvido pela Microsoft, lançado em 2020.
  - Biblioteca moderna para automação de testes em navegadores (Chromium, Firefox e WebKit).
  - Suporta Node.js, Python, Java e C#.
  - Focado em testes de ponta a ponta (end-to-end) com APIs simples e robustas.

- **Selenium**:
  - Projeto de código aberto com uma longa história (lançado em 2004).
  - Conjunto de ferramentas para automação de navegadores, com destaque para o Selenium WebDriver.
  - Suporta múltiplas linguagens (Java, Python, C#, Ruby, JavaScript, etc.).
  - Amplamente usado para testes web e automação de tarefas em navegadores.

---

### **2. Comparação Detalhada**

| **Aspecto**                  | **Playwright**                                                                 | **Selenium**                                                                 |
|------------------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Arquitetura**              | Usa uma conexão direta com os navegadores via protocolo DevTools, oferecendo maior controle e confiabilidade. | Usa WebDriver, que depende de drivers específicos para cada navegador (ChromeDriver, GeckoDriver, etc.), o que pode levar a problemas de compatibilidade. |
| **Suporte a navegadores**    | Suporta Chromium (Chrome, Edge), Firefox e WebKit (Safari) nativamente, com comportamento consistente. | Suporta uma ampla gama de navegadores, incluindo Chrome, Firefox, Safari, Edge e outros, mas requer configuração de drivers. |
| **Headless e Headful**       | Suporta modos headless e headful com configuração simples. O modo headless é otimizado para CI/CD. | Suporta headless e headful, mas o suporte headless pode ser menos estável em versões mais antigas. |
| **Velocidade**               | Geralmente mais rápido devido à conexão direta e menos overhead. | Pode ser mais lento devido à comunicação via drivers e maior latência em algumas operações. |
| **APIs e facilidade de uso** | API moderna, intuitiva e consistente. Inclui recursos como auto-waiting (espera automática por elementos). | API mais antiga, requer configuração manual de esperas (ex.: WebDriverWait) para evitar falhas em elementos não carregados. |
| **Auto-waiting**             | Possui espera automática para ações como cliques e preenchimentos, reduzindo flakiness (testes instáveis). | Não possui auto-waiting nativo; exige waits explícitos ou implícitos, o que pode complicar a escrita de testes. |
| **Suporte a múltiplas abas/janelas** | Excelente suporte para múltiplas abas, janelas e contextos de navegação (ex.: modo anônimo). | Suporta múltiplas abas/janelas, mas a configuração pode ser mais complexa e menos robusta. |
| **Testes multiplataforma**   | Suporta testes em desktop, mobile (emulação) e navegadores WebKit diretamente. | Suporta emulação mobile, mas o suporte ao Safari/WebKit é menos robusto e depende do ambiente macOS. |
| **Integração com CI/CD**     | Fácil integração com ferramentas como GitHub Actions, Jenkins, etc., com relatórios embutidos (HTML, JSON). | Integra bem com CI/CD, mas requer mais configuração para relatórios e gerenciamento de drivers. |
| **Capturas de tela e vídeos** | Captura de screenshots, vídeos e rastreamento (traces) nativamente, com configuração simples. | Suporta screenshots, mas vídeos e traces exigem ferramentas externas ou configurações adicionais. |
| **Testes de API**            | Suporta chamadas de API diretamente com `page.request`. | Suporta testes de API, mas geralmente requer bibliotecas externas como `requests` (Python) ou `RestAssured` (Java). |
| **Comunidade e ecossistema** | Comunidade crescente, mas menor devido à sua relativa novidade. Boa documentação oficial. | Comunidade muito grande e madura, com amplo suporte em fóruns, bibliotecas e ferramentas de terceiros. |
| **Suporte a linguagens**     | Node.js, Python, Java, C#. Menos opções, mas APIs consistentes. | Java, Python, C#, Ruby, JavaScript, PHP, etc. Maior variedade, mas APIs podem variar entre linguagens. |
| **Ferramenta de geração de código** | Inclui `codegen`, que grava interações em tempo real para gerar scripts automaticamente. | Não possui ferramenta nativa de geração de código; depende de ferramentas externas como Selenium IDE. |
| **Custo e licença**          | Gratuito, de código aberto (Apache 2.0). | Gratuito, de código aberto (Apache 2.0). |
| **Manutenção de drivers**    | Não requer gerenciamento de drivers; os binários dos navegadores são incluídos automaticamente. | Requer configuração e atualização manual de drivers (ex.: ChromeDriver), o que pode ser trabalhoso. |

---

### **3. Vantagens e Desvantagens**

#### **Playwright**
**Vantagens**:
- **Moderno e eficiente**: API simplificada, auto-waiting e conexão direta com navegadores reduzem a complexidade e flakiness.
- **Suporte a WebKit**: Ideal para testar em Safari sem configurações complexas.
- **Ferramentas embutidas**: Captura de vídeos, traces e relatórios sem dependências externas.
- **Gerenciamento simplificado**: Não precisa de drivers separados, facilitando a configuração.
- **Suporte a mobile**: Emulação de dispositivos móveis é robusta e fácil de configurar.

**Desvantagens**:
- Menor comunidade em comparação com o Selenium, o que pode limitar recursos e suporte em fóruns.
- Relativamente novo, então algumas integrações ou plugins podem estar menos maduros.

#### **Selenium**
**Vantagens**:
- **Comunidade ampla**: Grande base de usuários, muitos tutoriais, plugins e suporte em fóruns como Stack Overflow.
- **Suporte a navegadores legados**: Útil para testar em navegadores antigos ou menos comuns.
- **Flexibilidade**: Suporta mais linguagens e frameworks, ideal para equipes com stacks diversos.
- **Maturidade**: Ferramenta consolidada, amplamente adotada em empresas.

**Desvantagens**:
- Configuração mais complexa devido à necessidade de drivers e gerenciamento manual.
- Testes podem ser mais propensos a falhas (flaky) sem waits explícitos.
- Menos eficiente para testes modernos, como emulação mobile ou WebKit.

---

### **4. Casos de Uso**
- **Use Playwright se**:
  - Você precisa de uma ferramenta moderna com configuração mínima.
  - Está testando aplicações em Chrome, Firefox e Safari (especialmente WebKit).
  - Quer evitar gerenciamento de drivers e escrever testes mais robustos com auto-waiting.
  - Precisa de recursos como gravação de vídeos ou emulação mobile nativa.

- **Use Selenium se**:
  - Sua equipe já usa Selenium e tem uma base de testes estabelecida.
  - Você precisa suportar navegadores legados ou ambientes muito específicos.
  - Sua equipe usa linguagens menos comuns (ex.: Ruby, PHP) ou frameworks específicos.
  - Você depende de uma comunidade grande para suporte e plugins.

---

### **5. Exemplo Prático: Código Comparado**
Ambas as ferramentas podem realizar tarefas semelhantes, mas a sintaxe e abordagem diferem. Aqui está um exemplo de como abrir uma página e clicar em um botão:

**Playwright**:
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://www.example.com');
  await page.click('text="Clique aqui"');
  await browser.close();
})();
```

**Selenium**:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.example.com')
driver.find_element(By.LINK_TEXT, 'Clique aqui').click()
driver.quit()
```

**Observações**:
- O Playwright usa seletores baseados em texto ou CSS de forma mais fluida e tem espera automática.
- O Selenium exige configuração do driver e pode precisar de waits explícitos para evitar erros.

---

### **6. Conclusão**
- **Playwright** é ideal para projetos novos ou equipes que buscam uma ferramenta moderna, com menos configuração e maior robustez em testes multiplataforma.
- **Selenium** é mais adequado para projetos legados, equipes com conhecimento prévio da ferramenta ou que precisam suportar uma ampla gama de navegadores e linguagens.

Se você está começando um projeto do zero e prioriza facilidade de uso e suporte a navegadores modernos, o Playwright é geralmente a melhor escolha. No entanto, se sua equipe já está investida no ecossistema Selenium ou precisa de suporte a casos específicos, o Selenium ainda é uma opção sólida.

Se precisar de exemplos práticos, ajuda com configuração ou mais detalhes sobre algum aspecto, é só pedir!

---

*Conversa exportada do Grok*
*Processado em: 15/11/2025 22:27*