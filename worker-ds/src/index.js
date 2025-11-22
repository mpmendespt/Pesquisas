import { JWT } from './auth.js';

// Rate limiting storage (usando Memory Storage - em produção use KV)
const rateLimitStore = new Map();

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const jwt = new JWT(env.JWT_SECRET);

    // Aplicar rate limiting
    const rateLimitResult = await checkRateLimit(request, env);
    if (rateLimitResult) return rateLimitResult;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': 'https://mpmendespt.github.io',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
      'Access-Control-Allow-Credentials': 'true'
    };

    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Rotas públicas
    if (url.pathname === '/api/health') {
      return new Response(JSON.stringify({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        service: 'Pesquisas DS API'
      }), { headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    // Rotas de autenticação
    if (url.pathname === '/api/register' && request.method === 'POST') {
      return await handleRegister(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/login' && request.method === 'POST') {
      return await handleLogin(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/confirm-email' && request.method === 'POST') {
      return await handleConfirmEmail(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/forgot-password' && request.method === 'POST') {
      return await handleForgotPassword(request, env, corsHeaders);
    }

    if (url.pathname === '/api/reset-password' && request.method === 'POST') {
      return await handleResetPassword(request, env, corsHeaders);
    }

    // Rotas protegidas
    if (url.pathname === '/api/protected' && request.method === 'GET') {
      return await handleProtected(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/profile' && request.method === 'GET') {
      return await handleGetProfile(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/profile' && request.method === 'PUT') {
      return await handleUpdateProfile(request, env, jwt, corsHeaders);
    }

    // Rotas administrativas
    if (url.pathname === '/api/admin/users/pending' && request.method === 'GET') {
      return await handleGetPendingUsers(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/admin/users/approve' && request.method === 'POST') {
      return await handleApproveUser(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/admin/users' && request.method === 'GET') {
      return await handleGetAllUsers(request, env, jwt, corsHeaders);
    }

    return new Response(JSON.stringify({ error: 'Endpoint não encontrado' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
};

// ========== FUNÇÕES DE AUTENTICAÇÃO ==========

async function handleRegister(request, env, jwt, corsHeaders) {
  try {
    const { username, email, password } = await request.json();
    
    // Validações
    if (!username || !email || !password) {
      return errorResponse('Todos os campos são obrigatórios', 400, corsHeaders);
    }

    if (password.length < 8) {
      return errorResponse('A senha deve ter pelo menos 8 caracteres', 400, corsHeaders);
    }

    if (!validateEmail(email)) {
      return errorResponse('Email inválido', 400, corsHeaders);
    }

    // Hash da password
    const passwordHash = await hashPassword(password);
    
    // Inserir usuário (não aprovado por padrão)
    try {
      const result = await env.DB.prepare(
        `INSERT INTO users (username, email, password_hash, is_active, is_approved) 
         VALUES (?, ?, ?, ?, ?)`
      ).bind(username, email, passwordHash, false, false).run();

      if (result.success) {
        // Criar registro de aprovação pendente
        await env.DB.prepare(
          'INSERT INTO admin_approvals (user_id, status) VALUES (?, ?)'
        ).bind(result.meta.last_row_id, 'pending').run();

        // Gerar token de confirmação de email (simulado)
        const emailToken = generateToken();
        await env.DB.prepare(
          `INSERT INTO email_confirmations (user_id, token, expires_at) 
           VALUES (?, ?, datetime('now', '+1 day'))`
        ).bind(result.meta.last_row_id, emailToken).run();

        return successResponse({
          message: 'Registro realizado! Aguarde aprovação do administrador e verifique seu email.',
          requires_approval: true,
          user_id: result.meta.last_row_id
        }, 201, corsHeaders);
      }
    } catch (dbError) {
      if (dbError.message.includes('UNIQUE constraint failed')) {
        if (dbError.message.includes('username')) {
          return errorResponse('Nome de usuário já existe', 409, corsHeaders);
        } else if (dbError.message.includes('email')) {
          return errorResponse('Email já está em uso', 409, corsHeaders);
        }
      }
      throw dbError;
    }

  } catch (error) {
    console.error('Registration error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

async function handleLogin(request, env, jwt, corsHeaders) {
  try {
    const { username, password } = await request.json();
    
    if (!username || !password) {
      return errorResponse('Username e password são obrigatórios', 400, corsHeaders);
    }
    
    // Buscar usuário
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE username = ?'
    ).bind(username).first();
    
    if (!user) {
      return errorResponse('Credenciais inválidas', 401, corsHeaders);
    }
    
    // Verificar password
    const isValid = await verifyPassword(password, user.password_hash);
    if (!isValid) {
      return errorResponse('Credenciais inválidas', 401, corsHeaders);
    }

    // Verificar se está aprovado
    if (!user.is_approved) {
      return errorResponse('Conta aguardando aprovação do administrador', 403, corsHeaders);
    }

    // Verificar se email está confirmado
    if (!user.is_email_verified) {
      return errorResponse('Por favor, confirme seu email antes de fazer login', 403, corsHeaders);
    }

    // Verificar se está ativo
    if (!user.is_active) {
      return errorResponse('Conta desativada. Contacte o administrador.', 403, corsHeaders);
    }
    
    // Gerar JWT
    const expiration = Math.floor(Date.now() / 1000) + (24 * 60 * 60);
    const token = await jwt.sign({
      userId: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      exp: expiration
    });
    
    return successResponse({
      token: token,
      user: { 
        id: user.id, 
        username: user.username,
        email: user.email,
        role: user.role,
        is_email_verified: user.is_email_verified
      },
      expiresIn: expiration
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Login error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

// ========== FUNÇÕES ADMINISTRATIVAS ==========

async function handleGetPendingUsers(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateAdmin(request, env, jwt);
    if (!user) return errorResponse('Acesso negado', 403, corsHeaders);

    const users = await env.DB.prepare(
      `SELECT u.id, u.username, u.email, u.created_at, a.created_at as approval_requested
       FROM users u 
       LEFT JOIN admin_approvals a ON u.id = a.user_id 
       WHERE u.is_approved = FALSE AND a.status = 'pending'`
    ).all();

    return successResponse({ users: users.results }, 200, corsHeaders);

  } catch (error) {
    console.error('Get pending users error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

async function handleApproveUser(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return errorResponse('Acesso negado', 403, corsHeaders);

    const { userId, approve } = await request.json();
    
    if (typeof approve === 'undefined') {
      return errorResponse('Parâmetro "approve" é obrigatório', 400, corsHeaders);
    }

    const status = approve ? 'approved' : 'rejected';
    
    // Atualizar aprovação
    await env.DB.prepare(
      `UPDATE admin_approvals 
       SET status = ?, approved_by = ?, updated_at = datetime('now') 
       WHERE user_id = ?`
    ).bind(status, admin.userId, userId).run();

    if (approve) {
      // Ativar usuário se aprovado
      await env.DB.prepare(
        `UPDATE users 
         SET is_approved = TRUE, is_active = TRUE, updated_at = datetime('now') 
         WHERE id = ?`
      ).bind(userId).run();
    }

    return successResponse({ 
      message: `Usuário ${approve ? 'aprovado' : 'rejeitado'} com sucesso` 
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Approve user error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

async function handleGetAllUsers(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return errorResponse('Acesso negado', 403, corsHeaders);

    const users = await env.DB.prepare(
      `SELECT id, username, email, role, is_active, is_approved, is_email_verified, created_at 
       FROM users 
       ORDER BY created_at DESC`
    ).all();

    return successResponse({ users: users.results }, 200, corsHeaders);

  } catch (error) {
    console.error('Get all users error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

// ========== FUNÇÕES DE PERFIL ==========

async function handleGetProfile(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return errorResponse('Não autorizado', 401, corsHeaders);

    const userData = await env.DB.prepare(
      'SELECT id, username, email, role, is_email_verified, created_at FROM users WHERE id = ?'
    ).bind(user.userId).first();

    return successResponse({ user: userData }, 200, corsHeaders);

  } catch (error) {
    console.error('Get profile error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

async function handleUpdateProfile(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return errorResponse('Não autorizado', 401, corsHeaders);

    const { username, email } = await request.json();
    
    // Validações
    if (!username || !email) {
      return errorResponse('Username e email são obrigatórios', 400, corsHeaders);
    }

    if (!validateEmail(email)) {
      return errorResponse('Email inválido', 400, corsHeaders);
    }

    // Atualizar perfil
    await env.DB.prepare(
      `UPDATE users 
       SET username = ?, email = ?, updated_at = datetime('now') 
       WHERE id = ?`
    ).bind(username, email, user.userId).run();

    return successResponse({ 
      message: 'Perfil atualizado com sucesso',
      user: { username, email }
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Update profile error:', error);
    if (error.message.includes('UNIQUE constraint failed')) {
      return errorResponse('Username ou email já existe', 409, corsHeaders);
    }
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

// ========== FUNÇÕES DE EMAIL E PASSWORD ==========

async function handleConfirmEmail(request, env, jwt, corsHeaders) {
  try {
    const { token } = await request.json();
    
    if (!token) {
      return errorResponse('Token é obrigatório', 400, corsHeaders);
    }

    // Verificar token
    const confirmation = await env.DB.prepare(
      `SELECT ec.*, u.id as user_id 
       FROM email_confirmations ec 
       JOIN users u ON ec.user_id = u.id 
       WHERE ec.token = ? AND ec.expires_at > datetime('now')`
    ).bind(token).first();

    if (!confirmation) {
      return errorResponse('Token inválido ou expirado', 400, corsHeaders);
    }

    // Marcar email como verificado
    await env.DB.prepare(
      'UPDATE users SET is_email_verified = TRUE WHERE id = ?'
    ).bind(confirmation.user_id).run();

    // Remover token usado
    await env.DB.prepare(
      'DELETE FROM email_confirmations WHERE token = ?'
    ).bind(token).run();

    return successResponse({ message: 'Email confirmado com sucesso!' }, 200, corsHeaders);

  } catch (error) {
    console.error('Confirm email error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

async function handleForgotPassword(request, env, corsHeaders) {
  try {
    const { email } = await request.json();
    
    if (!email) {
      return errorResponse('Email é obrigatório', 400, corsHeaders);
    }

    // Buscar usuário
    const user = await env.DB.prepare(
      'SELECT id FROM users WHERE email = ? AND is_active = TRUE'
    ).bind(email).first();

    if (user) {
      // Gerar token de reset (simulado)
      const resetToken = generateToken();
      await env.DB.prepare(
        `INSERT INTO password_resets (user_id, token, expires_at) 
         VALUES (?, ?, datetime('now', '+1 hour'))`
      ).bind(user.id, resetToken).run();

      // Em produção, enviar email aqui
      console.log(`Reset token for ${email}: ${resetToken}`);
    }

    // Sempre retornar sucesso por segurança
    return successResponse({ 
      message: 'Se o email existir, enviaremos instruções de reset' 
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Forgot password error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

async function handleResetPassword(request, env, corsHeaders) {
  try {
    const { token, newPassword } = await request.json();
    
    if (!token || !newPassword) {
      return errorResponse('Token e nova senha são obrigatórios', 400, corsHeaders);
    }

    if (newPassword.length < 8) {
      return errorResponse('A senha deve ter pelo menos 8 caracteres', 400, corsHeaders);
    }

    // Verificar token
    const reset = await env.DB.prepare(
      `SELECT pr.*, u.id as user_id 
       FROM password_resets pr 
       JOIN users u ON pr.user_id = u.id 
       WHERE pr.token = ? AND pr.expires_at > datetime('now') AND pr.used = FALSE`
    ).bind(token).first();

    if (!reset) {
      return errorResponse('Token inválido ou expirado', 400, corsHeaders);
    }

    // Hash da nova password
    const passwordHash = await hashPassword(newPassword);

    // Atualizar password
    await env.DB.prepare(
      'UPDATE users SET password_hash = ? WHERE id = ?'
    ).bind(passwordHash, reset.user_id).run();

    // Marcar token como usado
    await env.DB.prepare(
      'UPDATE password_resets SET used = TRUE WHERE token = ?'
    ).bind(token).run();

    return successResponse({ message: 'Password alterada com sucesso!' }, 200, corsHeaders);

  } catch (error) {
    console.error('Reset password error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}

// ========== FUNÇÕES AUXILIARES ==========

async function authenticateUser(request, env, jwt) {
  const authHeader = request.headers.get('Authorization');
  if (!authHeader?.startsWith('Bearer ')) return null;

  const token = authHeader.substring(7);
  try {
    return await jwt.verify(token);
  } catch {
    return null;
  }
}

async function authenticateAdmin(request, env, jwt) {
  const user = await authenticateUser(request, env, jwt);
  if (!user || user.role !== 'admin') return null;
  return user;
}

async function checkRateLimit(request, env) {
  const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
  const key = `${clientIP}:${new Date().getMinutes()}`;
  const limit = 100; // 100 requests por minuto

  const current = rateLimitStore.get(key) || 0;
  if (current >= limit) {
    return new Response(JSON.stringify({ 
      error: 'Muitas requisições. Tente novamente em alguns minutos.' 
    }), {
      status: 429,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://mpmendespt.github.io'
      }
    });
  }

  rateLimitStore.set(key, current + 1);
  // Limpar dados antigos (em produção use KV com TTL)
  setTimeout(() => rateLimitStore.delete(key), 60000);
  return null;
}

function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function generateToken() {
  return Array.from(crypto.getRandomValues(new Uint8Array(32)))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

async function verifyPassword(password, hash) {
  const newHash = await hashPassword(password);
  return newHash === hash;
}

function successResponse(data, status = 200, corsHeaders) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

function errorResponse(message, status = 400, corsHeaders) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// Função protegida mantida
async function handleProtected(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return errorResponse('Não autorizado', 401, corsHeaders);

    return successResponse({ 
      message: 'Acesso autorizado a dados protegidos!',
      user: user,
      serverTime: new Date().toISOString()
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Protected route error:', error);
    return errorResponse('Erro interno no servidor', 500, corsHeaders);
  }
}