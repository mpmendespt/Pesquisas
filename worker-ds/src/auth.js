export class JWT {
  constructor(secret) {
    this.secret = secret;
  }

  base64UrlEncode(str) {
    return btoa(str)
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }

  base64UrlDecode(str) {
    str = str.replace(/-/g, '+').replace(/_/g, '/');
    while (str.length % 4) {
      str += '=';
    }
    return atob(str);
  }

  async createSignature(data) {
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
      'raw',
      encoder.encode(this.secret),
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign']
    );
    
    const signature = await crypto.subtle.sign(
      'HMAC',
      key,
      encoder.encode(data)
    );
    
    return this.base64UrlEncode(String.fromCharCode(...new Uint8Array(signature)));
  }

  async sign(payload) {
    const header = { alg: 'HS256', typ: 'JWT' };
    const headerEncoded = this.base64UrlEncode(JSON.stringify(header));
    const payloadEncoded = this.base64UrlEncode(JSON.stringify(payload));
    const signature = await this.createSignature(`${headerEncoded}.${payloadEncoded}`);
    
    return `${headerEncoded}.${payloadEncoded}.${signature}`;
  }

  async verify(token) {
    const [headerEncoded, payloadEncoded, signature] = token.split('.');
    const expectedSignature = await this.createSignature(`${headerEncoded}.${payloadEncoded}`);
    
    if (signature !== expectedSignature) {
      throw new Error('Invalid signature');
    }
    
    const payload = JSON.parse(this.base64UrlDecode(payloadEncoded));
    
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
      throw new Error('Token expired');
    }
    
    return payload;
  }
}