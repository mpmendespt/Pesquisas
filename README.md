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
Pesquisas_DS/
├── 📁 worker-ds/ # Backend Cloudflare Worker
│ ├── src/
│ │ ├── index.js # Worker principal
│ │ └── auth.js # Sistema JWT
│ ├── schemas/
│ │ └── init.sql # Schema do banco
│ ├── wrangler.jsonc # Configuração
│ └── package.json
├── 📁 site/ # Frontend GitHub Pages
│ ├── login.html # Página de login
│ ├── register.html # Página de registro
│ ├── index.html # Dashboard (protegido)
│ ├── assets/
│ │ └── css/
│ │ └── style.css # Estilos
│ └── .gitignore # Gitignore do site
├── 📁 schemas/ # Database schemas
│ └── init.sql # Tabelas do banco
├── .gitignore # Gitignore global
└── README.md # Esta documentação


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