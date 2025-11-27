import { JWT } from './auth.js';
import { EmailService } from './emailService.js';

// Rate limiting storage
const rateLimitStore = new Map();

// EmailService será inicializado dentro do fetch para acessar env
let emailService = null;

// ========== FUNÇÃO PARA VERIFICAR EMAIL MANUALMENTE (ADMIN) ==========
async function handleAdminVerifyEmail(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return jsonResponse({ error: 'Acesso negado' }, 403, corsHeaders);

    const { userId } = await request.json();
    
    if (!userId) {
      return jsonResponse({ error: 'ID do utilizador é obrigatório' }, 400, corsHeaders);
    }

    const user = await env.DB.prepare(
      'SELECT id, username, email, is_email_verified FROM users WHERE id = ?'
    ).bind(userId).first();

    if (!user) {
      return jsonResponse({ error: 'Utilizador não encontrado' }, 404, corsHeaders);
    }

    // Alterar o status de verificação de email
    const newStatus = !user.is_email_verified;
    
    await env.DB.prepare(
      'UPDATE users SET is_email_verified = ? WHERE id = ?'
    ).bind(newStatus, userId).run();

    console.log(`📧 Admin ${admin.username} ${newStatus ? 'verificou' : 'removeu verificação do'} email de ${user.username}`);

    return jsonResponse({ 
      message: `Email ${newStatus ? 'verificado' : 'marcado como não verificado'} com sucesso`,
      is_email_verified: newStatus
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Admin verify email error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const jwt = new JWT(env.JWT_SECRET);

    // ✅ Inicializar EmailService com a API key do environment
    if (!emailService) {
      emailService = new EmailService(env.RESEND_API_KEY);
    }

    // ✅ CRÍTICO: CORS Headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
      'Access-Control-Expose-Headers': '*',
    };

    // ✅ CRÍTICO: Responder OPTIONS imediatamente
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders
      });
    }

    // Aplicar rate limiting
    const rateLimitResult = await checkRateLimit(request, corsHeaders);
    if (rateLimitResult) return rateLimitResult;

    // Rotas públicas
    if (url.pathname === '/api/health') {
      return jsonResponse({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        service: 'Pesquisas DS API',
        version: '1.0.0',
        endpoints: [
          '/api/register', '/api/login', '/api/confirm-email',
          '/api/forgot-password', '/api/reset-password', '/api/profile',
          '/api/admin/users', '/api/admin/users/pending', '/api/admin/users/approve'
        ]
      }, 200, corsHeaders);
    }

    // Rotas de autenticação
    if (url.pathname === '/api/register' && request.method === 'POST') {
      return await handleRegister(request, env, jwt, corsHeaders, emailService);
    }

    if (url.pathname === '/api/login' && request.method === 'POST') {
      return await handleLogin(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/confirm-email' && request.method === 'POST') {
      return await handleConfirmEmail(request, env, corsHeaders);
    }

    if (url.pathname === '/api/forgot-password' && request.method === 'POST') {
      return await handleForgotPassword(request, env, corsHeaders, emailService);
    }

    if (url.pathname === '/api/reset-password' && request.method === 'POST') {
      return await handleResetPassword(request, env, corsHeaders);
    }

    if (url.pathname === '/api/resend-confirmation' && request.method === 'POST') {
      return await handleResendConfirmation(request, env, jwt, corsHeaders, emailService);
    }

    // Rotas protegidas
    if (url.pathname === '/api/protected' && request.method === 'GET') {
      return await handleProtected(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/profile' && request.method === 'GET') {
      return await handleGetProfile(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/profile' && request.method === 'PUT') {
      return await handleUpdateProfile(request, env, jwt, corsHeaders, emailService);
    }

    if (url.pathname === '/api/change-password' && request.method === 'POST') {
      return await handleChangePassword(request, env, jwt, corsHeaders);
    }

    // Rotas administrativas
    if (url.pathname === '/api/admin/users/pending' && request.method === 'GET') {
      return await handleGetPendingUsers(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/admin/users/approve' && request.method === 'POST') {
      return await handleApproveUser(request, env, jwt, corsHeaders, emailService);
    }

    if (url.pathname === '/api/admin/users' && request.method === 'GET') {
      return await handleGetAllUsers(request, env, jwt, corsHeaders);
    }

    if (url.pathname === '/api/admin/users/update' && request.method === 'PUT') {
      return await handleAdminUpdateUser(request, env, jwt, corsHeaders);
    }
    
    if (url.pathname === '/api/admin/users/delete' && request.method === 'DELETE') {
      return await handleDeleteUser(request, env, jwt, corsHeaders);
    }
    
    // Dentro do export default { async fetch(...) }
    // Adicione esta linha junto com as outras rotas admin:

    if (url.pathname === '/api/admin/users/verify-email' && request.method === 'POST') {
      return await handleAdminVerifyEmail(request, env, jwt, corsHeaders);
    }

    // Rota não encontrada
    return jsonResponse({ error: 'Endpoint não encontrado' }, 404, corsHeaders);
  }
};

// ========== FUNÇÃO AUXILIAR PARA JSON RESPONSES ==========
function jsonResponse(data, status = 200, corsHeaders = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders
    }
  });
}

// ========== FUNÇÕES DE AUTENTICAÇÃO ==========

async function handleRegister(request, env, jwt, corsHeaders, emailService) {
  try {
    const { username, email, password } = await request.json();
    
    if (!username || !email || !password) {
      return jsonResponse({ error: 'Todos os campos são obrigatórios' }, 400, corsHeaders);
    }

    if (username.length < 3) {
      return jsonResponse({ error: 'Username deve ter pelo menos 3 caracteres' }, 400, corsHeaders);
    }

    if (password.length < 8) {
      return jsonResponse({ error: 'A password deve ter pelo menos 8 caracteres' }, 400, corsHeaders);
    }

    if (!validateEmail(email)) {
      return jsonResponse({ error: 'Email inválido' }, 400, corsHeaders);
    }

    const passwordHash = await hashPassword(password);
    
    try {
      const result = await env.DB.prepare(
        `INSERT INTO users (username, email, password_hash, is_active, is_approved) 
         VALUES (?, ?, ?, ?, ?)`
      ).bind(username, email, passwordHash, false, false).run();

      if (result.success) {
        await env.DB.prepare(
          'INSERT INTO admin_approvals (user_id, status) VALUES (?, ?)'
        ).bind(result.meta.last_row_id, 'pending').run();

        const emailToken = generateToken();
        await env.DB.prepare(
          `INSERT INTO email_confirmations (user_id, token, expires_at) 
           VALUES (?, ?, datetime('now', '+1 day'))`
        ).bind(result.meta.last_row_id, emailToken).run();

        // ✅ ENVIAR EMAIL DE CONFIRMAÇÃO
        const confirmLink = `https://mpmendespt.github.io/Pesquisas/app/confirm-email.html?token=${emailToken}`;
        const htmlContent = emailService.getEmailConfirmationHTML(username, emailToken, confirmLink);
        const textContent = emailService.getEmailConfirmationText(username, emailToken, confirmLink);
        
        await emailService.sendEmail(
          email,
          'Confirme seu Email - Pesquisas DS',
          htmlContent,
          textContent
        );

        console.log(`📧 Email de confirmação enviado para ${email}`);

        return jsonResponse({
          message: 'Registro realizado! Aguarde aprovação do administrador.',
          requires_approval: true,
          user_id: result.meta.last_row_id
        }, 201, corsHeaders);
      }
    } catch (dbError) {
      if (dbError.message.includes('UNIQUE constraint failed')) {
        if (dbError.message.includes('username')) {
          return jsonResponse({ error: 'Nome de usuário já existe' }, 409, corsHeaders);
        } else if (dbError.message.includes('email')) {
          return jsonResponse({ error: 'Email já está em uso' }, 409, corsHeaders);
        }
      }
      throw dbError;
    }

  } catch (error) {
    console.error('Registration error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleLogin(request, env, jwt, corsHeaders) {
  try {
    const { username, password } = await request.json();
    
    if (!username || !password) {
      return jsonResponse({ error: 'Username e password são obrigatórios' }, 400, corsHeaders);
    }
    
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE username = ?'
    ).bind(username).first();
    
    if (!user) {
      return jsonResponse({ error: 'Credenciais inválidas' }, 401, corsHeaders);
    }
    
    const isValid = await verifyPassword(password, user.password_hash);
    if (!isValid) {
      return jsonResponse({ error: 'Credenciais inválidas' }, 401, corsHeaders);
    }

    if (!user.is_approved) {
      return jsonResponse({ error: 'Conta aguardando aprovação do administrador' }, 403, corsHeaders);
    }

    if (!user.is_active) {
      return jsonResponse({ error: 'Conta desativada. Contacte o administrador.' }, 403, corsHeaders);
    }
    
    const expiration = Math.floor(Date.now() / 1000) + (24 * 60 * 60);
    const token = await jwt.sign({
      userId: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      exp: expiration
    });
    
    return jsonResponse({
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
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleConfirmEmail(request, env, corsHeaders) {
  try {
    const { token } = await request.json();
    
    if (!token) {
      return jsonResponse({ error: 'Token é obrigatório' }, 400, corsHeaders);
    }

    const confirmation = await env.DB.prepare(
      `SELECT ec.*, u.id as user_id 
       FROM email_confirmations ec 
       JOIN users u ON ec.user_id = u.id 
       WHERE ec.token = ? AND ec.expires_at > datetime('now')`
    ).bind(token).first();

    if (!confirmation) {
      return jsonResponse({ error: 'Token inválido ou expirado' }, 400, corsHeaders);
    }

    await env.DB.prepare(
      'UPDATE users SET is_email_verified = TRUE WHERE id = ?'
    ).bind(confirmation.user_id).run();

    await env.DB.prepare(
      'DELETE FROM email_confirmations WHERE token = ?'
    ).bind(token).run();

    return jsonResponse({ message: 'Email confirmado com sucesso!' }, 200, corsHeaders);

  } catch (error) {
    console.error('Confirm email error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleResendConfirmation(request, env, jwt, corsHeaders, emailService) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return jsonResponse({ error: 'Não autorizado' }, 401, corsHeaders);

    const emailToken = generateToken();
    
    await env.DB.prepare(
      'DELETE FROM email_confirmations WHERE user_id = ?'
    ).bind(user.userId).run();

    await env.DB.prepare(
      `INSERT INTO email_confirmations (user_id, token, expires_at) 
       VALUES (?, ?, datetime('now', '+1 day'))`
    ).bind(user.userId, emailToken).run();

    // ✅ ENVIAR EMAIL DE CONFIRMAÇÃO
    const confirmLink = `https://mpmendespt.github.io/Pesquisas/app/confirm-email.html?token=${emailToken}`;
    const htmlContent = emailService.getEmailConfirmationHTML(user.username, emailToken, confirmLink);
    const textContent = emailService.getEmailConfirmationText(user.username, emailToken, confirmLink);
    
    await emailService.sendEmail(
      user.email,
      'Confirme seu Email - Pesquisas DS',
      htmlContent,
      textContent
    );

    console.log(`📧 Email de confirmação reenviado para ${user.email}`);

    return jsonResponse({ 
      message: 'Email de confirmação reenviado!'
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Resend confirmation error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleForgotPassword(request, env, corsHeaders, emailService) {
  try {
    const { email } = await request.json();
    
    if (!email) {
      return jsonResponse({ error: 'Email é obrigatório' }, 400, corsHeaders);
    }

    // Buscar usuário
    const user = await env.DB.prepare(
      'SELECT id, username, email FROM users WHERE email = ? AND is_active = TRUE'
    ).bind(email).first();

    if (user) {
      // Gerar token de reset
      const resetToken = generateToken();
      await env.DB.prepare(
        `INSERT INTO password_resets (user_id, token, expires_at) 
         VALUES (?, ?, datetime('now', '+1 hour'))`
      ).bind(user.id, resetToken).run();

      // ✅ ENVIAR EMAIL REAL
      const resetLink = `https://mpmendespt.github.io/Pesquisas/app/reset-password.html?token=${resetToken}`;
      
      const htmlContent = emailService.getPasswordResetHTML(user.username, resetToken, resetLink);
      const textContent = emailService.getPasswordResetText(user.username, resetToken, resetLink);
      
      const emailResult = await emailService.sendEmail(
        user.email,
        'Recuperação de Password - Pesquisas DS',
        htmlContent,
        textContent
      );

      if (emailResult.success) {
        console.log(`✅ Email de recuperação enviado para ${email}`);
      } else {
        console.error(`❌ Falha ao enviar email para ${email}:`, emailResult.error);
      }
    }

    // Sempre retornar sucesso (segurança)
    return jsonResponse({ 
      message: 'Se o email existir, enviaremos instruções de recuperação.'
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Forgot password error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleResetPassword(request, env, corsHeaders) {
  try {
    const { token, newPassword } = await request.json();
    
    if (!token || !newPassword) {
      return jsonResponse({ error: 'Token e nova password são obrigatórios' }, 400, corsHeaders);
    }

    if (newPassword.length < 8) {
      return jsonResponse({ error: 'A password deve ter pelo menos 8 caracteres' }, 400, corsHeaders);
    }

    const resetRequest = await env.DB.prepare(
      `SELECT pr.*, u.id as user_id 
       FROM password_resets pr 
       JOIN users u ON pr.user_id = u.id 
       WHERE pr.token = ? AND pr.expires_at > datetime('now') AND pr.used = FALSE`
    ).bind(token).first();

    if (!resetRequest) {
      return jsonResponse({ error: 'Token inválido ou expirado' }, 400, corsHeaders);
    }

    const passwordHash = await hashPassword(newPassword);

    await env.DB.prepare(
      'UPDATE users SET password_hash = ? WHERE id = ?'
    ).bind(passwordHash, resetRequest.user_id).run();

    await env.DB.prepare(
      'UPDATE password_resets SET used = TRUE WHERE token = ?'
    ).bind(token).run();

    return jsonResponse({ message: 'Password alterada com sucesso!' }, 200, corsHeaders);

  } catch (error) {
    console.error('Reset password error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

// ========== FUNÇÕES DE PERFIL ==========

async function handleGetProfile(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return jsonResponse({ error: 'Não autorizado' }, 401, corsHeaders);

    const userData = await env.DB.prepare(
      'SELECT id, username, email, role, is_email_verified, created_at FROM users WHERE id = ?'
    ).bind(user.userId).first();

    if (!userData) {
      return jsonResponse({ error: 'Utilizador não encontrado' }, 404, corsHeaders);
    }

    return jsonResponse({ user: userData }, 200, corsHeaders);

  } catch (error) {
    console.error('Get profile error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleUpdateProfile(request, env, jwt, corsHeaders, emailService) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return jsonResponse({ error: 'Não autorizado' }, 401, corsHeaders);

    const { username, email } = await request.json();
    
    if (!username || !email) {
      return jsonResponse({ error: 'Username e email são obrigatórios' }, 400, corsHeaders);
    }

    if (!validateEmail(email)) {
      return jsonResponse({ error: 'Email inválido' }, 400, corsHeaders);
    }

    await env.DB.prepare(
      `UPDATE users 
       SET username = ?, email = ?, updated_at = datetime('now') 
       WHERE id = ?`
    ).bind(username, email, user.userId).run();

    if (email !== user.email) {
      await env.DB.prepare(
        'UPDATE users SET is_email_verified = FALSE WHERE id = ?'
      ).bind(user.userId).run();
      
      const emailToken = generateToken();
      await env.DB.prepare(
        `INSERT INTO email_confirmations (user_id, token, expires_at) 
         VALUES (?, ?, datetime('now', '+1 day'))`
      ).bind(user.userId, emailToken).run();

      // ✅ ENVIAR EMAIL DE CONFIRMAÇÃO
      const confirmLink = `https://mpmendespt.github.io/Pesquisas/app/confirm-email.html?token=${emailToken}`;
      const htmlContent = emailService.getEmailConfirmationHTML(username, emailToken, confirmLink);
      const textContent = emailService.getEmailConfirmationText(username, emailToken, confirmLink);
      
      await emailService.sendEmail(
        email,
        'Confirme seu Novo Email - Pesquisas DS',
        htmlContent,
        textContent
      );

      console.log(`📧 Novo email de confirmação enviado para ${email}`);
    }

    return jsonResponse({ 
      message: 'Perfil atualizado com sucesso',
      user: { username, email },
      requires_email_verification: email !== user.email
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Update profile error:', error);
    if (error.message.includes('UNIQUE constraint failed')) {
      return jsonResponse({ error: 'Username ou email já existe' }, 409, corsHeaders);
    }
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleChangePassword(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return jsonResponse({ error: 'Não autorizado' }, 401, corsHeaders);

    const { currentPassword, newPassword } = await request.json();
    
    if (!currentPassword || !newPassword) {
      return jsonResponse({ error: 'Password atual e nova password são obrigatórias' }, 400, corsHeaders);
    }

    if (newPassword.length < 8) {
      return jsonResponse({ error: 'A nova password deve ter pelo menos 8 caracteres' }, 400, corsHeaders);
    }

    const userData = await env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(user.userId).first();
    
    if (!userData) {
      return jsonResponse({ error: 'Utilizador não encontrado' }, 404, corsHeaders);
    }

    const isCurrentValid = await verifyPassword(currentPassword, userData.password_hash);
    if (!isCurrentValid) {
      return jsonResponse({ error: 'Password atual incorreta' }, 401, corsHeaders);
    }

    const newPasswordHash = await hashPassword(newPassword);

    await env.DB.prepare(
      'UPDATE users SET password_hash = ?, updated_at = datetime("now") WHERE id = ?'
    ).bind(newPasswordHash, user.userId).run();

    return jsonResponse({ message: 'Password alterada com sucesso!' }, 200, corsHeaders);

  } catch (error) {
    console.error('Change password error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

// ========== FUNÇÕES ADMINISTRATIVAS ==========

async function handleGetPendingUsers(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return jsonResponse({ error: 'Acesso negado' }, 403, corsHeaders);

    const users = await env.DB.prepare(
      `SELECT u.id, u.username, u.email, u.created_at, a.created_at as approval_requested
       FROM users u 
       LEFT JOIN admin_approvals a ON u.id = a.user_id 
       WHERE u.is_approved = FALSE AND a.status = 'pending'`
    ).all();

    return jsonResponse({ users: users.results }, 200, corsHeaders);

  } catch (error) {
    console.error('Get pending users error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleApproveUser(request, env, jwt, corsHeaders, emailService) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return jsonResponse({ error: 'Acesso negado' }, 403, corsHeaders);

    const { userId, approve } = await request.json();
    
    if (typeof approve === 'undefined') {
      return jsonResponse({ error: 'Parâmetro "approve" é obrigatório' }, 400, corsHeaders);
    }

    // Buscar dados do usuário
    const user = await env.DB.prepare(
      'SELECT username, email FROM users WHERE id = ?'
    ).bind(userId).first();

    if (!user) {
      return jsonResponse({ error: 'Utilizador não encontrado' }, 404, corsHeaders);
    }

    const status = approve ? 'approved' : 'rejected';
    
    await env.DB.prepare(
      `UPDATE admin_approvals 
       SET status = ?, approved_by = ?, updated_at = datetime('now') 
       WHERE user_id = ?`
    ).bind(status, admin.userId, userId).run();

    if (approve) {
      await env.DB.prepare(
        `UPDATE users 
         SET is_approved = TRUE, is_active = TRUE, updated_at = datetime('now') 
         WHERE id = ?`
      ).bind(userId).run();

      // ✅ ENVIAR EMAIL DE APROVAÇÃO
      const loginLink = 'https://mpmendespt.github.io/Pesquisas/app/login.html';
      const htmlContent = emailService.getAccountApprovedHTML(user.username, loginLink);
      const textContent = emailService.getAccountApprovedText(user.username, loginLink);
      
      await emailService.sendEmail(
        user.email,
        'Conta Aprovada - Pesquisas DS',
        htmlContent,
        textContent
      );

      console.log(`✅ Email de aprovação enviado para ${user.email}`);
    }

    return jsonResponse({ 
      message: `Usuário ${approve ? 'aprovado' : 'rejeitado'} com sucesso` 
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Approve user error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleGetAllUsers(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return jsonResponse({ error: 'Acesso negado' }, 403, corsHeaders);

    const users = await env.DB.prepare(
      `SELECT id, username, email, role, is_active, is_approved, is_email_verified, created_at 
       FROM users 
       ORDER BY created_at DESC`
    ).all();

    return jsonResponse({ users: users.results }, 200, corsHeaders);

  } catch (error) {
    console.error('Get all users error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleAdminUpdateUser(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return jsonResponse({ error: 'Acesso negado' }, 403, corsHeaders);

    const { userId, username, email, role, is_active, is_approved } = await request.json();
    
    if (!userId) {
      return jsonResponse({ error: 'ID do utilizador é obrigatório' }, 400, corsHeaders);
    }

    const userExists = await env.DB.prepare(
      'SELECT id FROM users WHERE id = ?'
    ).bind(userId).first();

    if (!userExists) {
      return jsonResponse({ error: 'Utilizador não encontrado' }, 404, corsHeaders);
    }

    await env.DB.prepare(
      `UPDATE users 
       SET username = ?, email = ?, role = ?, is_active = ?, is_approved = ?, updated_at = datetime('now') 
       WHERE id = ?`
    ).bind(username, email, role, is_active, is_approved, userId).run();

    return jsonResponse({ message: 'Utilizador atualizado com sucesso' }, 200, corsHeaders);

  } catch (error) {
    console.error('Admin update user error:', error);
    if (error.message.includes('UNIQUE constraint failed')) {
      return jsonResponse({ error: 'Username ou email já existe' }, 409, corsHeaders);
    }
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
  }
}

async function handleDeleteUser(request, env, jwt, corsHeaders) {
  try {
    const admin = await authenticateAdmin(request, env, jwt);
    if (!admin) return jsonResponse({ error: 'Acesso negado' }, 403, corsHeaders);

    const { userId } = await request.json();
    
    if (!userId) {
      return jsonResponse({ error: 'ID do utilizador é obrigatório' }, 400, corsHeaders);
    }

    // Verificar se o usuário existe
    const userToDelete = await env.DB.prepare(
      'SELECT id, username, role FROM users WHERE id = ?'
    ).bind(userId).first();

    if (!userToDelete) {
      return jsonResponse({ error: 'Utilizador não encontrado' }, 404, corsHeaders);
    }

    // Impedir que o admin delete a si mesmo
    if (userToDelete.id === admin.userId) {
      return jsonResponse({ 
        error: 'Não é possível remover sua própria conta enquanto está logado' 
      }, 400, corsHeaders);
    }

    // Verificar se é o último admin (opcional - para segurança)
    if (userToDelete.role === 'admin') {
      const adminCount = await env.DB.prepare(
        'SELECT COUNT(*) as count FROM users WHERE role = ? AND is_active = TRUE'
      ).bind('admin').first();

      if (adminCount.count <= 1) {
        return jsonResponse({ 
          error: 'Não é possível remover o último administrador do sistema' 
        }, 400, corsHeaders);
      }
    }

    // Deletar registros relacionados primeiro (integridade referencial)
    
    // 1. Deletar confirmações de email
    await env.DB.prepare(
      'DELETE FROM email_confirmations WHERE user_id = ?'
    ).bind(userId).run();

    // 2. Deletar resets de password
    await env.DB.prepare(
      'DELETE FROM password_resets WHERE user_id = ?'
    ).bind(userId).run();

    // 3. Deletar aprovações admin
    await env.DB.prepare(
      'DELETE FROM admin_approvals WHERE user_id = ?'
    ).bind(userId).run();

    // 4. Finalmente, deletar o usuário
    const result = await env.DB.prepare(
      'DELETE FROM users WHERE id = ?'
    ).bind(userId).run();

    if (result.success) {
      console.log(`🗑️ Usuário ${userToDelete.username} (ID: ${userId}) removido por ${admin.username}`);
      
      return jsonResponse({ 
        message: 'Utilizador removido com sucesso',
        deletedUser: {
          id: userToDelete.id,
          username: userToDelete.username
        }
      }, 200, corsHeaders);
    } else {
      return jsonResponse({ 
        error: 'Erro ao remover utilizador' 
      }, 500, corsHeaders);
    }

  } catch (error) {
    console.error('Delete user error:', error);
    return jsonResponse({ 
      error: 'Erro interno no servidor' 
    }, 500, corsHeaders);
  }
}

async function handleProtected(request, env, jwt, corsHeaders) {
  try {
    const user = await authenticateUser(request, env, jwt);
    if (!user) return jsonResponse({ error: 'Não autorizado' }, 401, corsHeaders);

    return jsonResponse({ 
      message: 'Acesso autorizado a dados protegidos!',
      user: user,
      serverTime: new Date().toISOString()
    }, 200, corsHeaders);

  } catch (error) {
    console.error('Protected route error:', error);
    return jsonResponse({ error: 'Erro interno no servidor' }, 500, corsHeaders);
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

async function checkRateLimit(request, corsHeaders) {
  const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
  const key = `${clientIP}:${new Date().getMinutes()}`;
  const limit = 100;

  const current = rateLimitStore.get(key) || 0;
  if (current >= limit) {
    return jsonResponse({ 
      error: 'Muitas requisições. Tente novamente em alguns minutos.' 
    }, 429, corsHeaders);
  }

  rateLimitStore.set(key, current + 1);
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