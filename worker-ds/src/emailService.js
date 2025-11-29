// --------- BEGIN emailService.js ---------
// emailService.js
// Gmail API email service for Cloudflare Workers
// Exports EmailService class with methods used by index.js:
// - constructor(env)
// - sendEmail(to, subject, htmlContent, textContent)
// - getEmailConfirmationHTML, getEmailConfirmationText
// - getPasswordResetHTML, getPasswordResetText
// - getAccountApprovedHTML, getAccountApprovedText

export class EmailService {
  /**
   * env: the Cloudflare env object (contains secrets as properties)
   * expects:
   *   env.GMAIL_CLIENT_ID
   *   env.GMAIL_CLIENT_SECRET
   *   env.GMAIL_REFRESH_TOKEN
   *   env.GMAIL_SENDER
   *   env.PUBLIC_BASE_URL (optional) - base URL for links (fallback to https://mpmendespt.github.io/Pesquisas)
   */
  constructor(env = {}) {
    this.env = env;
    this.sender = env.GMAIL_SENDER || 'mpmendespt@gmail.com';
    this.baseUrl = env.PUBLIC_BASE_URL || 'https://mpmendespt.github.io/Pesquisas';
  }

  // Obtain OAuth2 access token using refresh token
  async getAccessToken() {
    const { GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN } = this.env;
    if (!GMAIL_CLIENT_ID || !GMAIL_CLIENT_SECRET || !GMAIL_REFRESH_TOKEN) {
      throw new Error('Gmail API credentials missing (GMAIL_CLIENT_ID|GMAIL_CLIENT_SECRET|GMAIL_REFRESH_TOKEN)');
    }

    const params = new URLSearchParams({
      client_id: GMAIL_CLIENT_ID,
      client_secret: GMAIL_CLIENT_SECRET,
      refresh_token: GMAIL_REFRESH_TOKEN,
      grant_type: 'refresh_token'
    });

    const res = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString()
    });

    const data = await res.json();
    if (!res.ok) {
      console.error('❌ Erro ao obter access token:', data);
      throw new Error(data.error_description || data.error || 'Failed to obtain access token');
    }
    return data.access_token;
  }

  // send email using Gmail API
  async sendEmail(to, subject, htmlContent, textContent = '') {
    console.log(`📧 Enviando email via Gmail API para: ${to}`);
    try {
      const accessToken = await this.getAccessToken();
      console.log('🔐 Access token obtido');

      // construct MIME message (multipart/alternative)
      const boundary = '----=_Boundary_' + Math.random().toString(36).slice(2,10);
      const rawLines = [];
      rawLines.push(`From: ${this.sender}`);
      rawLines.push(`To: ${to}`);
      rawLines.push(`Subject: ${subject}`);
      rawLines.push('MIME-Version: 1.0');
      rawLines.push(`Content-Type: multipart/alternative; boundary="${boundary}"`);
      rawLines.push('');
      rawLines.push(`--${boundary}`);
      rawLines.push('Content-Type: text/plain; charset="UTF-8"');
      rawLines.push('');
      rawLines.push(textContent || this.plainFromHtml(htmlContent));
      rawLines.push('');
      rawLines.push(`--${boundary}`);
      rawLines.push('Content-Type: text/html; charset="UTF-8"');
      rawLines.push('');
      rawLines.push(htmlContent);
      rawLines.push('');
      rawLines.push(`--${boundary}--`);

      const raw = rawLines.join('\r\n');

      // base64url
      const base64 = btoa(raw).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

      const res = await fetch('https://gmail.googleapis.com/gmail/v1/users/me/messages/send', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ raw: base64 })
      });

      const json = await res.json();
      if (!res.ok) {
        console.error('❌ Erro Gmail API send:', json);
        throw new Error(json.error?.message || 'Gmail send failed');
      }

      console.log('✅ Email enviado, id:', json.id);
      return { success: true, id: json.id };
    } catch (err) {
      console.error('❌ Erro no envio via Gmail API:', err);
      return { success: false, error: err.message || String(err) };
    }
  }

  // fallback to generate plain text from HTML
  plainFromHtml(html) {
    return html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  }

  // Templates used by index.js (kept compatible)
  getEmailConfirmationHTML(username, token, confirmLink) {
    return `
      <div style="font-family: sans-serif; line-height:1.4;">
        <h2>Confirme seu email</h2>
        <p>Olá ${escapeHtml(username)},</p>
        <p>Por favor confirme o seu email clicando no link abaixo:</p>
        <p><a href="${confirmLink}">${confirmLink}</a></p>
        <p>Se não solicitou, ignore esta mensagem.</p>
        <p>Obrigado,<br/>Pesquisas DS</p>
      </div>
    `;
  }

  getEmailConfirmationText(username, token, confirmLink) {
    return `Olá ${username},\n\nConfirme o seu email: ${confirmLink}\n\nObrigado,\nPesquisas DS`;
  }

  getPasswordResetHTML(username, token, resetLink) {
    return `
      <div style="font-family: sans-serif; line-height:1.4;">
        <h2>Recuperação de Password</h2>
        <p>Olá ${escapeHtml(username)},</p>
        <p>Recebemos um pedido para redefinir a sua password. Clique no link abaixo:</p>
        <p><a href="${resetLink}">${resetLink}</a></p>
        <p>Se não fez este pedido, ignore este email.</p>
        <p>Obrigado,<br/>Pesquisas DS</p>
      </div>
    `;
  }

  getPasswordResetText(username, token, resetLink) {
    return `Recuperação de password para ${username}\n\nUse o link: ${resetLink}\n\nSe não pediu, ignore.`;
  }

  getAccountApprovedHTML(username, loginLink) {
    return `
      <div style="font-family: sans-serif; line-height:1.4;">
        <h2>Conta Aprovada</h2>
        <p>Olá ${escapeHtml(username)},</p>
        <p>A sua conta foi aprovada! Faça login aqui:</p>
        <p><a href="${loginLink}">${loginLink}</a></p>
        <p>Obrigado,<br/>Pesquisas DS</p>
      </div>
    `;
  }

  getAccountApprovedText(username, loginLink) {
    return `Olá ${username},\nA sua conta foi aprovada.\nLogin: ${loginLink}`;
  }
}

// small helper
function escapeHtml(s = '') {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039');
}
// --------- END emailService.js ---------
