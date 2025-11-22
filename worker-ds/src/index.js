import { JWT } from './auth.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const jwt = new JWT(env.JWT_SECRET);

    // CORS headers para GitHub Pages
    const corsHeaders = {
      'Access-Control-Allow-Origin': 'https://mpmendespt.github.io',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
      'Access-Control-Allow-Credentials': 'true'
    };

    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, { 
        headers: corsHeaders 
      });
    }

    // Rota de health check
    if (url.pathname === '/' || url.pathname === '/api') {
      return new Response(JSON.stringify({ 
        message: 'Worker DS API está funcionando!',
        endpoints: ['/api/register', '/api/login', '/api/protected'],
        timestamp: new Date().toISOString()
      }), {
        headers: { 
          ...corsHeaders,
          'Content-Type': 'application/json' 
        }
      });
    }

    // Rota de registro
    if (url.pathname === '/api/register' && request.method === 'POST') {
      return await handleRegister(request, env, jwt, corsHeaders);
    }

    // Rota de login
    if (url.pathname === '/api/login' && request.method === 'POST') {
      return await handleLogin(request, env, jwt, corsHeaders);
    }

    // Rota protegida
    if (url.pathname === '/api/protected' && request.method === 'GET') {
      return await handleProtected(request, env, jwt, corsHeaders);
    }

    // Rota não encontrada
    return new Response(JSON.stringify({ 
      error: 'Endpoint não encontrado',
      available_endpoints: ['/api/register', '/api/login', '/api/protected']
    }), {
      status: 404,
      headers: { 
        ...corsHeaders,
        'Content-Type': 'application/json' 
      }
    });
  }
};

// Função de registro
async function handleRegister(request, env, jwt, corsHeaders) {
  try {
    // Verificar Content-Type
    const contentType = request.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      return new Response(JSON.stringify({ error: 'Content-Type deve ser application/json' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    const { username, password } = await request.json();
    
    // Validações
    if (!username || !password) {
      return new Response(JSON.stringify({ error: 'Username e password são obrigatórios' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    if (username.length < 3) {
      return new Response(JSON.stringify({ error: 'Username deve ter pelo menos 3 caracteres' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    if (password.length < 3) {
      return new Response(JSON.stringify({ error: 'Password deve ter pelo menos 3 caracteres' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // Hash da password
    const passwordHash = await hashPassword(password);
    
    // Inserir no banco
    try {
      const result = await env.DB.prepare(
        'INSERT INTO users (username, password_hash) VALUES (?, ?)'
      ).bind(username, passwordHash).run();

      if (result.success) {
        return new Response(JSON.stringify({ 
          success: true, 
          message: 'Usuário registrado com sucesso',
          user: { username }
        }), {
          status: 201,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      } else {
        throw new Error('Falha ao inserir usuário');
      }
      
    } catch (dbError) {
      // Verificar se é erro de usuário duplicado
      if (dbError.message.includes('UNIQUE constraint failed') || 
          dbError.message.includes('already exists')) {
        return new Response(JSON.stringify({ error: 'Username já existe' }), {
          status: 409,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
      
      console.error('Database error:', dbError);
      throw dbError;
    }

  } catch (error) {
    console.error('Registration error:', error);
    return new Response(JSON.stringify({ error: 'Erro interno no servidor' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}

// Função de login
async function handleLogin(request, env, jwt, corsHeaders) {
  try {
    // Verificar Content-Type
    const contentType = request.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      return new Response(JSON.stringify({ error: 'Content-Type deve ser application/json' }), {
        status: 400,
        headers: corsHeaders
      });
    }

    const { username, password } = await request.json();
    
    // Validações básicas
    if (!username || !password) {
      return new Response(JSON.stringify({ error: 'Username e password são obrigatórios' }), {
        status: 400,
        headers: corsHeaders
      });
    }
    
    // Buscar usuário
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE username = ?'
    ).bind(username).first();
    
    if (!user) {
      return new Response(JSON.stringify({ error: 'Credenciais inválidas' }), {
        status: 401,
        headers: corsHeaders
      });
    }
    
    // Verificar password
    const isValid = await verifyPassword(password, user.password_hash);
    if (!isValid) {
      return new Response(JSON.stringify({ error: 'Credenciais inválidas' }), {
        status: 401,
        headers: corsHeaders
      });
    }
    
    // Gerar JWT (24 horas de expiração)
    const expiration = Math.floor(Date.now() / 1000) + (24 * 60 * 60);
    const token = await jwt.sign({
      userId: user.id,
      username: user.username,
      exp: expiration
    });
    
    return new Response(JSON.stringify({ 
      success: true,
      token: token,
      user: { 
        id: user.id, 
        username: user.username 
      },
      expiresIn: expiration
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('Login error:', error);
    return new Response(JSON.stringify({ error: 'Erro interno no servidor' }), {
      status: 500,
      headers: corsHeaders
    });
  }
}

// Função de rota protegida
async function handleProtected(request, env, jwt, corsHeaders) {
  try {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return new Response(JSON.stringify({ error: 'Token de autorização não fornecido' }), {
        status: 401,
        headers: corsHeaders
      });
    }
    
    const token = authHeader.substring(7); // Remove "Bearer "
    
    if (!token) {
      return new Response(JSON.stringify({ error: 'Token não fornecido' }), {
        status: 401,
        headers: corsHeaders
      });
    }

    const payload = await jwt.verify(token);
    
    // Buscar dados atualizados do usuário
    const user = await env.DB.prepare(
      'SELECT id, username, created_at FROM users WHERE id = ?'
    ).bind(payload.userId).first();
    
    if (!user) {
      return new Response(JSON.stringify({ error: 'Usuário não encontrado' }), {
        status: 401,
        headers: corsHeaders
      });
    }
    
    return new Response(JSON.stringify({ 
      success: true,
      message: 'Acesso autorizado a dados protegidos!',
      user: user,
      serverTime: new Date().toISOString(),
      tokenInfo: {
        issuedFor: payload.username,
        expiresAt: new Date(payload.exp * 1000).toISOString()
      }
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('Protected route error:', error);
    
    let errorMessage = 'Token inválido';
    if (error.message.includes('expired')) {
      errorMessage = 'Token expirado';
    } else if (error.message.includes('signature')) {
      errorMessage = 'Assinatura do token inválida';
    }
    
    return new Response(JSON.stringify({ error: errorMessage }), {
      status: 401,
      headers: corsHeaders
    });
  }
}

// Funções auxiliares de password
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