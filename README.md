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

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ GitHub Pages    │ ←→ │ Cloudflare Worker│ ←→ │ D1 Database     │
│ (Frontend)      │    │ (Backend)        │    │ (SQLite)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘


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

## 📁 Estrutura do Projeto
Pesquisas/
├── docs/
│   ├── index.html           # Página inicial pública
│   ├── about.html           # Sobre (mantido)
│   ├── contact.html         # Contacto (mantido)
│   ├── app/
│   │   ├── index.html   # Dashboard (COM botão acesso pesquisas)
│   │   ├── login.html       # Login (redirecionamento corrigido)
│   │   ├── register.html # Registro (redirecionamento corrigido)
│   │   └── admin.html       # Admin (redirecionamento corrigido)
│   ├── Pesquisas_/
│   │   └── index.html       # Nova página de pesquisas
│   └── assets/
│       └── css/
│           ├── site.css     # CSS para página inicial
│           └── style.css    # CSS para dashboard e páginas internas
└── worker-ds/               # Mantido como está
└── 📄 README.md


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
