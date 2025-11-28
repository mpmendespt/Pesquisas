export default {
  async fetch(request, env) {
    // Permitir requisições OPTIONS para CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    // Aceitar apenas POST
    if (request.method !== 'POST') {
      return new Response('Método não permitido. Use POST.', { 
        status: 405,
        headers: { 'Access-Control-Allow-Origin': '*' }
      });
    }

    try {
      // Parse do corpo da requisição
      const body = await request.json().catch(() => ({}));
      const to = body.to || 'test@example.com';
      
      console.log(`📧 Testando envio para: ${to}`);
      
      // ✅ Estrutura CORRETA para MailChannels
      const mailMessage = {
        personalizations: [{
          to: [{ email: to }],
          subject: 'Teste MailChannels - Worker Funcional'
        }],
        from: {
          email: 'no-reply@worker-ds-test.mpmendespt.workers.dev',
          name: 'Worker Teste'
        },
        content: [{
          type: 'text/plain',
          value: '✅ Este é um teste do MailChannels funcionando no Cloudflare Worker!'
        }]
      };
      
      // ✅ Headers CRÍTICOS para funcionar
      const headers = {
        'Content-Type': 'application/json',
        'X-MailChannels-Integration': 'workers'
      };

      console.log('📤 Enviando requisição para MailChannels...');
      
      // ✅ Chamada para a API do MailChannels
      const response = await fetch('https://api.mailchannels.net/tx/v1/send', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(mailMessage)
      });

      // ✅ Tratamento da resposta
      const responseData = await response.text();
      
      if (response.ok) {
        console.log('✅ Email enviado com sucesso!');
        return new Response(JSON.stringify({
          success: true,
          message: 'Email de teste enviado com sucesso!',
          to: to,
          response: responseData
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
      } else {
        console.error(`❌ Erro MailChannels (${response.status}):`, responseData);
        return new Response(JSON.stringify({
          success: false,
          error: `MailChannels retornou status ${response.status}`,
          details: responseData
        }), {
          status: response.status || 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }
    } catch (error) {
      console.error('🔥 Erro fatal no Worker:', error);
      return new Response(JSON.stringify({
        success: false,
        error: 'Erro interno no servidor',
        details: error.message
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  }
};