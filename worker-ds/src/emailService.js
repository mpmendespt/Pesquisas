// ============================================================================
// emailService.js - Serviço de Email com MailChannels
// ============================================================================
// Local: worker-ds/src/emailService.js
// Usar com: Cloudflare Workers + MailChannels (100% GRATUITO)
// ============================================================================

export class EmailService {
  constructor(
    fromEmail = 'noreply@mpmendespt.workers.dev',  // ← Email de envio (Workers ou seu domínio)
    fromName = 'Pesquisas DS'                       // ← Nome que aparece no remetente
  ) {
    this.fromEmail = fromEmail;
    this.fromName = fromName;
    this.mailChannelsAPI = 'https://api.mailchannels.net/tx/v1/send';
  }

  /**
   * Envia um email usando MailChannels
   * @param {string} to - Email do destinatário
   * @param {string} subject - Assunto do email
   * @param {string} htmlContent - Conteúdo HTML do email
   * @param {string} textContent - Conteúdo texto (opcional)
   * @returns {Promise<{success: boolean, error?: string}>}
   */
  async sendEmail(to, subject, htmlContent, textContent = null) {
    try {
      // Montar estrutura do email
      const emailData = {
        personalizations: [{
          to: [{ email: to }]
        }],
        from: {
          email: this.fromEmail,
          name: this.fromName
        },
        subject: subject,
        content: [
          {
            type: 'text/html',
            value: htmlContent
          }
        ]
      };

      // Adicionar versão texto se fornecida
      if (textContent) {
        emailData.content.push({
          type: 'text/plain',
          value: textContent
        });
      }

      // Enviar via MailChannels
      const response = await fetch(this.mailChannelsAPI, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(emailData)
      });

      if (response.ok) {
        console.log(`✅ Email enviado para ${to}: ${subject}`);
        return { success: true };
      } else {
        const error = await response.text();
        console.error(`❌ Erro ao enviar email para ${to}:`, error);
        return { success: false, error };
      }

    } catch (error) {
      console.error('❌ Erro crítico ao enviar email:', error);
      return { success: false, error: error.message };
    }
  }

  // ========================================================================
  // TEMPLATE 1: Reset de Password
  // ========================================================================
  
  /**
   * Template HTML para reset de password
   */
  getPasswordResetHTML(username, resetToken, resetLink) {
    return `
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Recuperação de Password</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .email-container {
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 30px 20px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
    }
    .content {
      padding: 30px;
    }
    .content p {
      margin: 0 0 15px;
      font-size: 16px;
    }
    .token-box {
      background: #f8f9fa;
      border: 2px dashed #667eea;
      padding: 20px;
      border-radius: 8px;
      font-family: 'Courier New', monospace;
      font-size: 20px;
      text-align: center;
      margin: 25px 0;
      letter-spacing: 2px;
      word-break: break-all;
    }
    .button {
      display: inline-block;
      background: #667eea;
      color: white !important;
      padding: 14px 40px;
      text-decoration: none;
      border-radius: 8px;
      margin: 20px 0;
      font-weight: 600;
      text-align: center;
    }
    .button-container {
      text-align: center;
    }
    .warning {
      background: #fff3cd;
      border-left: 4px solid #ffc107;
      padding: 15px;
      margin: 20px 0;
      border-radius: 4px;
    }
    .warning strong {
      color: #856404;
    }
    .footer {
      text-align: center;
      padding: 20px;
      background: #f8f9fa;
      color: #666;
      font-size: 12px;
    }
    .footer p {
      margin: 5px 0;
    }
    .divider {
      border: 0;
      border-top: 1px solid #e9ecef;
      margin: 20px 0;
    }
    .secondary-text {
      color: #666;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <h1>🔐 Recuperação de Password</h1>
    </div>
    
    <div class="content">
      <p>Olá <strong>${username}</strong>,</p>
      
      <p>Recebemos uma solicitação para redefinir a password da sua conta no <strong>Pesquisas DS</strong>.</p>
      
      <p>Para sua segurança, use o token abaixo para criar uma nova password:</p>
      
      <div class="token-box">
        ${resetToken}
      </div>
      
      <div class="button-container">
        <a href="${resetLink}" class="button">Redefinir Password Agora</a>
      </div>
      
      <div class="warning">
        <strong>⚠️ Atenção:</strong> Este token expira em <strong>1 hora</strong>.
      </div>
      
      <p class="secondary-text">Se você não solicitou esta alteração, pode ignorar este email com segurança. Sua password permanecerá inalterada.</p>
      
      <hr class="divider">
      
      <p class="secondary-text">
        <strong>Precisa de ajuda?</strong><br>
        Você também pode copiar e colar o token manualmente na página:<br>
        <a href="${resetLink}" style="color: #667eea;">${resetLink}</a>
      </p>
    </div>
    
    <div class="footer">
      <p><strong>© 2024 Pesquisas DS</strong></p>
      <p>Sistema de Gestão de Pesquisas</p>
      <p>Este é um email automático. Por favor, não responda.</p>
    </div>
  </div>
</body>
</html>`;
  }

  /**
   * Template TEXTO para reset de password
   */
  getPasswordResetText(username, resetToken, resetLink) {
    return `
RECUPERAÇÃO DE PASSWORD - Pesquisas DS
=======================================

Olá ${username},

Recebemos uma solicitação para redefinir a password da sua conta.

TOKEN DE RECUPERAÇÃO:
${resetToken}

LINK PARA REDEFINIR:
${resetLink}

⚠️ ATENÇÃO: Este token expira em 1 hora.

Se você não solicitou esta alteração, ignore este email.
Sua password permanecerá inalterada.

---
© 2024 Pesquisas DS - Sistema de Gestão de Pesquisas
Este é um email automático. Por favor, não responda.
    `.trim();
  }

  // ========================================================================
  // TEMPLATE 2: Confirmação de Email
  // ========================================================================
  
  /**
   * Template HTML para confirmação de email
   */
  getEmailConfirmationHTML(username, confirmToken, confirmLink) {
    return `
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Confirme seu Email</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .email-container {
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 30px 20px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
    }
    .content {
      padding: 30px;
    }
    .content p {
      margin: 0 0 15px;
      font-size: 16px;
    }
    .button {
      display: inline-block;
      background: #667eea;
      color: white !important;
      padding: 14px 40px;
      text-decoration: none;
      border-radius: 8px;
      margin: 20px 0;
      font-weight: 600;
    }
    .button-container {
      text-align: center;
    }
    .token-box {
      background: #f8f9fa;
      border: 2px solid #e9ecef;
      padding: 15px;
      border-radius: 8px;
      font-family: 'Courier New', monospace;
      font-size: 18px;
      text-align: center;
      margin: 20px 0;
      word-break: break-all;
    }
    .footer {
      text-align: center;
      padding: 20px;
      background: #f8f9fa;
      color: #666;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <h1>📧 Confirme seu Email</h1>
    </div>
    
    <div class="content">
      <p>Olá <strong>${username}</strong>,</p>
      
      <p>Bem-vindo ao <strong>Pesquisas DS</strong>! 🎉</p>
      
      <p>Para ativar sua conta e começar a usar nosso sistema, por favor confirme seu endereço de email clicando no botão abaixo:</p>
      
      <div class="button-container">
        <a href="${confirmLink}" class="button">Confirmar Email</a>
      </div>
      
      <p>Ou use o token de confirmação:</p>
      
      <div class="token-box">
        ${confirmToken}
      </div>
      
      <p style="color: #666; font-size: 14px;">
        ⏰ <strong>Este link expira em 24 horas.</strong>
      </p>
      
      <p style="color: #666; font-size: 14px;">
        Se você não se cadastrou no Pesquisas DS, pode ignorar este email com segurança.
      </p>
    </div>
    
    <div class="footer">
      <p><strong>© 2024 Pesquisas DS</strong></p>
      <p>Sistema de Gestão de Pesquisas</p>
    </div>
  </div>
</body>
</html>`;
  }

  /**
   * Template TEXTO para confirmação de email
   */
  getEmailConfirmationText(username, confirmToken, confirmLink) {
    return `
CONFIRME SEU EMAIL - Pesquisas DS
==================================

Olá ${username},

Bem-vindo ao Pesquisas DS! 🎉

Para ativar sua conta, por favor confirme seu email.

TOKEN DE CONFIRMAÇÃO:
${confirmToken}

LINK PARA CONFIRMAR:
${confirmLink}

⏰ Este link expira em 24 horas.

Se você não se cadastrou, ignore este email.

---
© 2024 Pesquisas DS - Sistema de Gestão de Pesquisas
    `.trim();
  }

  // ========================================================================
  // TEMPLATE 3: Conta Aprovada
  // ========================================================================
  
  /**
   * Template HTML para conta aprovada
   */
  getAccountApprovedHTML(username, loginLink) {
    return `
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Conta Aprovada</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .email-container {
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header {
      background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
      color: white;
      padding: 30px 20px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
    }
    .content {
      padding: 30px;
    }
    .content p {
      margin: 0 0 15px;
      font-size: 16px;
    }
    .button {
      display: inline-block;
      background: #27ae60;
      color: white !important;
      padding: 14px 40px;
      text-decoration: none;
      border-radius: 8px;
      margin: 20px 0;
      font-weight: 600;
    }
    .button-container {
      text-align: center;
    }
    .success-box {
      background: #d4edda;
      border-left: 4px solid #28a745;
      padding: 15px;
      margin: 20px 0;
      border-radius: 4px;
    }
    .footer {
      text-align: center;
      padding: 20px;
      background: #f8f9fa;
      color: #666;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <h1>✅ Conta Aprovada!</h1>
    </div>
    
    <div class="content">
      <p>Olá <strong>${username}</strong>,</p>
      
      <div class="success-box">
        <strong>🎉 Ótimas notícias!</strong><br>
        Sua conta foi aprovada pelo administrador do sistema.
      </div>
      
      <p>Agora você pode fazer login e começar a usar todas as funcionalidades do <strong>Pesquisas DS</strong>.</p>
      
      <div class="button-container">
        <a href="${loginLink}" class="button">Fazer Login Agora</a>
      </div>
      
      <p>Estamos felizes em tê-lo conosco! Se precisar de ajuda, não hesite em entrar em contato.</p>
    </div>
    
    <div class="footer">
      <p><strong>© 2024 Pesquisas DS</strong></p>
      <p>Sistema de Gestão de Pesquisas</p>
    </div>
  </div>
</body>
</html>`;
  }

  /**
   * Template TEXTO para conta aprovada
   */
  getAccountApprovedText(username, loginLink) {
    return `
CONTA APROVADA - Pesquisas DS
==============================

Olá ${username},

🎉 Ótimas notícias!

Sua conta foi aprovada pelo administrador do sistema.

Agora você pode fazer login e começar a usar o Pesquisas DS.

FAZER LOGIN:
${loginLink}

Estamos felizes em tê-lo conosco!

---
© 2024 Pesquisas DS - Sistema de Gestão de Pesquisas
    `.trim();
  }

  // ========================================================================
  // MÉTODOS DE CONVENIÊNCIA (Envio rápido com templates)
  // ========================================================================

  /**
   * Envia email de reset de password (conveniência)
   */
  async sendPasswordReset(userEmail, username, resetToken) {
    const resetLink = `https://mpmendespt.github.io/Pesquisas/app/reset-password.html?token=${resetToken}`;
    
    const htmlContent = this.getPasswordResetHTML(username, resetToken, resetLink);
    const textContent = this.getPasswordResetText(username, resetToken, resetLink);
    
    return await this.sendEmail(
      userEmail,
      'Recuperação de Password - Pesquisas DS',
      htmlContent,
      textContent
    );
  }

  /**
   * Envia email de confirmação (conveniência)
   */
  async sendEmailConfirmation(userEmail, username, confirmToken) {
    const confirmLink = `https://mpmendespt.github.io/Pesquisas/app/confirm-email.html?token=${confirmToken}`;
    
    const htmlContent = this.getEmailConfirmationHTML(username, confirmToken, confirmLink);
    const textContent = this.getEmailConfirmationText(username, confirmToken, confirmLink);
    
    return await this.sendEmail(
      userEmail,
      'Confirme seu Email - Pesquisas DS',
      htmlContent,
      textContent
    );
  }

  /**
   * Envia email de conta aprovada (conveniência)
   */
  async sendAccountApproved(userEmail, username) {
    const loginLink = 'https://mpmendespt.github.io/Pesquisas/app/login.html';
    
    const htmlContent = this.getAccountApprovedHTML(username, loginLink);
    const textContent = this.getAccountApprovedText(username, loginLink);
    
    return await this.sendEmail(
      userEmail,
      'Sua conta foi aprovada - Pesquisas DS',
      htmlContent,
      textContent
    );
  }
}