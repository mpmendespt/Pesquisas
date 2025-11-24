// Adicione esta rota no worker-ds/src/index.js
// Logo após as outras rotas administrativas

// Rota para deletar usuário (ADMIN)
if (url.pathname === '/api/admin/users/delete' && request.method === 'DELETE') {
  return await handleDeleteUser(request, env, jwt, corsHeaders);
}

// ========== NOVA FUNÇÃO: DELETAR USUÁRIO ==========

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