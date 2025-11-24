# Notepad++ slow startup troubleshooting

## 📊 Informações
- **Número:** #35
- **Origem:** Claude
- **Categoria:** Outros
- **ID:** 777f4ef8-6ea7-4267-8fdc-0d94e13bd124
- **Criada em:** 2025-11-06 20:37:41
- **Total de mensagens:** 2
- **Resumo:** Notepad++ com inicio muito lento porque e como resolver...

---

## 💬 Conversa

### 👤 Utilizador *[Claude]*

Notepad++ com inicio muito lento porque e como resolver

---

### 🤖 Claude *[Claude]*

 O início lento do Notepad++ geralmente tem algumas causas comuns. Vou ajudá-lo a resolver:

## Causas mais comuns:

1. **Muitos plugins instalados** - Cada plugin carrega ao iniciar
2. **Arquivos grandes abertos na sessão anterior** - O Notepad++ tenta reabrir todos
3. **Muitos arquivos na sessão** - Centenas de abas abertas
4. **Problemas com plugins específicos** - Alguns podem travar ou demorar
5. **Antivírus bloqueando temporariamente** - Verifica os arquivos ao abrir

## Soluções:

**1. Desativar restauração de sessão:**
- Vá em `Configurações` → `Preferências` → `Backup`
- Desmarque "Lembrar sessão atual para a próxima vez"
- Reinicie o Notepad++

**2. Desativar plugins desnecessários:**
- Vá em `Plugins` → `Gestor de Plugins`
- Desinstale plugins que não usa
- Ou renomeie a pasta `plugins` temporariamente para testar

**3. Limpar arquivos de sessão:**
- Feche o Notepad++
- Vá para: `%APPDATA%\Notepad++`
- Delete ou renomeie o arquivo `session.xml`

**4. Modo de inicialização limpa:**
- Abra o Notepad++ com: `notepad++ -nosession -multiInst`
- Isso inicia sem carregar a sessão anterior

**5. Adicionar exceção no antivírus:**
- Adicione o Notepad++ às exceções do seu antivírus
- Especialmente a pasta de instalação

**6. Reinstalar em modo portátil:**
- Faça backup das suas configurações
- Reinstale em modo portátil (mais rápido)

Qual dessas situações parece mais próxima do seu caso? Posso dar mais detalhes sobre qualquer solução específica.

---

*Conversa exportada do Claude*
*Processado em: 24/11/2025 22:27*