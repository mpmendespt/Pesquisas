// src/index.ts
import JWTAuth from './auth';

export interface Env {
  JWT_SECRET: string;
  // You can add D1 database binding here later
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const auth = new JWTAuth(env.JWT_SECRET);

    // Public login route
    if (url.pathname === '/api/login' && request.method === 'POST') {
      try {
        const { username, password } = await request.json();
        
        // TODO: Validate credentials against your database (e.g., D1)
        // This is a simple example - always check against stored user data
        if (username === 'user' && password === 'pass') {
          const token = await auth.sign({ 
            sub: 'user123', 
            username: username
          }, { expiresIn: '1d' });

          return new Response(JSON.stringify({ token }), {
            headers: { 
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': 'https://mpmendespt.github.io',
              'Access-Control-Allow-Methods': 'POST, OPTIONS',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
          });
        }
        return new Response(JSON.stringify({ error: 'Invalid credentials' }), { status: 401 });
      } catch (err) {
        return new Response(JSON.stringify({ error: 'Login failed' }), { status: 500 });
      }
    }

    // Protected API route example
    if (url.pathname === '/api/protected') {
      try {
        const authHeader = request.headers.get('Authorization');
        if (!authHeader?.startsWith('Bearer ')) {
          return new Response(JSON.stringify({ error: 'Missing token' }), { status: 401 });
        }

        const token = authHeader.split(' ')[1];
        const payload = await auth.verify(token); // Throws an error if invalid

        // Token is valid, proceed with the request
        return new Response(JSON.stringify({ 
          message: 'Access granted to protected data',
          user: payload 
        }), { 
          headers: { 'Content-Type': 'application/json' } 
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: 'Invalid or expired token' }), { status: 401 });
      }
    }

    // Handle preflight CORS requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': 'https://mpmendespt.github.io',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        }
      });
    }

    return new Response('Not Found', { status: 404 });
  },
};