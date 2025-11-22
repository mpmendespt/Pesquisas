-- Dropar tabelas existentes
DROP TABLE IF EXISTS research_data;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS email_confirmations;
DROP TABLE IF EXISTS password_resets;
DROP TABLE IF EXISTS admin_approvals;

-- Tabela de usuários com novos campos
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_active BOOLEAN DEFAULT FALSE,
  is_approved BOOLEAN DEFAULT FALSE,
  is_email_verified BOOLEAN DEFAULT FALSE,
  role TEXT DEFAULT 'user',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para confirmações de email
CREATE TABLE IF NOT EXISTS email_confirmations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  token TEXT UNIQUE NOT NULL,
  expires_at DATETIME NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Tabela para reset de password
CREATE TABLE IF NOT EXISTS password_resets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  token TEXT UNIQUE NOT NULL,
  expires_at DATETIME NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Tabela para aprovações administrativas
CREATE TABLE IF NOT EXISTS admin_approvals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  approved_by INTEGER,
  status TEXT DEFAULT 'pending', -- pending, approved, rejected
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (approved_by) REFERENCES users (id)
);

-- Tabela de pesquisas
CREATE TABLE IF NOT EXISTS research_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  title TEXT NOT NULL,
  data TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Inserir usuário administrador padrão (senha: Admin123!)
INSERT OR IGNORE INTO users (username, email, password_hash, is_active, is_approved, is_email_verified, role) 
VALUES (
  'admin', 
  'admin@pesquisas.com', 
  '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', -- hash de 'admin'
  TRUE, 
  TRUE, 
  TRUE, 
  'admin'
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_email_confirmations_token ON email_confirmations(token);
CREATE INDEX IF NOT EXISTS idx_password_resets_token ON password_resets(token);
CREATE INDEX IF NOT EXISTS idx_admin_approvals_status ON admin_approvals(status);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);