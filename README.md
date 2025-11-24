# 🚀 Sistema de Pesquisas DS

Sistema completo com frontend no GitHub Pages e backend no Cloudflare Workers, oferecendo autenticação segura JWT e banco de dados D1 - totalmente gratuito.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Deploy](#deploy)
- [Desenvolvimento](#desenvolvimento)
- [API](#api)
- [Segurança](#segurança)

## 🎯 Visão Geral

Este projeto implementa uma aplicação web completa utilizando:
- **Frontend**: GitHub Pages (estático)
- **Backend**: Cloudflare Workers (serverless)
- **Banco de Dados**: Cloudflare D1 (SQLite)
- **Autenticação**: JWT tokens seguros

## 🏗️ Arquitetura
```bash
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ GitHub Pages    │ ←→ │ Cloudflare Worker│ ←→ │ D1 Database     │
│ (Frontend)      │    │ (Backend)        │    │ (SQLite)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## ✨ Funcionalidades

### 🔐 Autenticação
- [x] Registro de usuários seguro
- [x] Login com JWT
- [x] Logout automático
- [x] Proteção de rotas no frontend
- [x] Tokens com expiração

### 📊 Sistema
- [x] Páginas separadas (login, registro, dashboard)
- [x] Interface responsiva
- [x] Validação de formulários
- [x] Mensagens de feedback
- [x] Dados protegidos por JWT

### Estrutura de Pastas
```bash
Pesquisas_DS/
├──  assets/
│   ├──  css/
│   │   ├──  site.css
│   │   └──  style.css
│   ├──  images/
│   └──  js/
├──  docs/
│   ├──  Pesquisas_/
│   │   └──  index.html
│   ├──  app/
│   │   ├──  admin.html
│   │   ├──  confirm-email.html
│   │   ├──  dashboard.html
│   │   ├──  forgot-password.html
│   │   ├──  login.html
│   │   ├──  register.html
│   │   └──  reset-password.html
│   ├──  assets/
│   ├──  .gitignore
│   ├──  .nojekyll
│   └──  index.html
├──  worker-ds/
├──  .gitignore
├──  .nojekyll
└──  README.md
```


## ⚙️ Configuração

### Pré-requisitos
- Conta no [Cloudflare](https://dash.cloudflare.com)
- Conta no [GitHub](https://github.com)
- Node.js e npm instalados

### Backend (Cloudflare Worker)

1. **Configurar o Worker**:
   ```bash
   cd worker-ds
   npm install
