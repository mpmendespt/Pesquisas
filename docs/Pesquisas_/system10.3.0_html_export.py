# system10.3.0_html_export.py
SCRIPT_VERSION = "10.3.0"
TOC_DEPTH = 2
TOC_FIXED_WIDTH = "320px"
TOC_SCROLLBAR_WIDTH = "8px"

# =============================================================================
# CONFIGURAÇÕES PADRÃO - MODIFICÁVEIS NO CABEÇALHO
# =============================================================================
DEFAULT_ALLOW_TRANSFORMS = True          # Ativar transformações de conteúdo
DEFAULT_FORCE_OVERWRITE = True           # Sobrescrever arquivos existentes
DEFAULT_CACHE_MEMORY_MB = 200            # Cache em memória (MB)
DEFAULT_CACHE_DISK_GB = 2                # Cache em disco (GB)
DEFAULT_STRICT_PRESERVE = False          # Preservação estrita (False = permite transformações)
# =============================================================================

"""
SISTEMA COMBINADO v10.3.0 - OTIMIZADO E ROBUSTO
✨ NOVIDADES v10.3.0:
• --strict-preserve como PADRÃO (usar --allow-transforms para ativar transformações)
• Cache LRU com limite de memória configurável
• Otimização agressiva do Pandoc com reutilização de subprocess
• Processamento em blocos menores para evitar OOM
• Sistema de gestão de memória inteligente
• Verificação de integridade de conteúdo com hash
• Métricas detalhadas de performance

CONFIGURAÇÕES ATUAIS (modifique no cabeçalho):
• allow-transforms: {DEFAULT_ALLOW_TRANSFORMS}
• force-overwrite: {DEFAULT_FORCE_OVERWRITE}  
• cache-memory: {DEFAULT_CACHE_MEMORY_MB}MB
• cache-disk: {DEFAULT_CACHE_DISK_GB}GB
• strict-preserve: {DEFAULT_STRICT_PRESERVE}

FUNCIONALIDADES MANTIDAS v10.2.0:
• TOC FIXO À DIREITA CORRIGIDO - SEM SOBREPOSIÇÕES
• Botão ☰ para minimizar TOC, Scrollspy, Voltar ao Topo
• Links para PDFs (sempre presentes, mesmo que não existam ainda)
• Processamento completo de Qwen, ChatGPT, DeepSeek, Grok, Claude
• Exportação para Markdown, HTML, CSV, JSON
• Interface web com busca e filtros
• Backup e checksum opcionais
• Lightbox para imagens e scroll suave
• Leitura de ZIPs em memória
• Toggle dark mode
• Ícones coloridos por fonte
• Botão Voltar ao Topo nos HTMLs individuais à direita
• Timer global de performance

🔐 NOVO: Sistema de Autenticação Integrado
• Verificação JWT automática em todos os HTMLs
• Botão "Voltar ao Dashboard" configurado para ../app/dashboard.html
• Proteção contra acesso não autorizado
• Verificação periódica de token
"""
import json
import zipfile
import os
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
import webbrowser
import shutil
import tempfile
import traceback
import re
import subprocess
import time
from typing import List, Dict, Any, Optional, Tuple
import markdown
import logging
import base64
import unicodedata
import hashlib
import pickle
from urllib.parse import urlparse
import pandas as pd
import numpy as np
import glob
import io
from collections import OrderedDict
from threading import Lock

# Configurar logger global
SCRIPT_START_TIME = time.perf_counter()
logger = logging.getLogger(__name__)

# Função para checksum SHA-256
def compute_checksum(file_path: Path) -> str:
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""): 
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

from collections import Counter

# =============================================================================
# Substituição para imghdr usando python-magic-bin - Compatível com Python 3.13+
# =============================================================================
_image_detection_cache = {}
try:
    import magic
    HAVE_MAGIC = True
    print("✅ python-magic-bin carregado com sucesso!")
except ImportError as e:
    HAVE_MAGIC = False
    print(f"⚠️  python-magic-bin não disponível: {e}")

def get_image_type(image_data):
    if not image_data or len(image_data) < 8:
        return None
    cache_key = hashlib.md5(image_data[:1024]).hexdigest()
    if cache_key in _image_detection_cache:
        return _image_detection_cache[cache_key]
    if not HAVE_MAGIC:
        return basic_image_detection(image_data)
    try:
        mime = magic.from_buffer(image_data, mime=True)
        if mime and mime.startswith('image/'):
            mime_type = mime.split('/')[1]
            type_map = {
                'jpeg': 'jpeg', 'jpg': 'jpeg', 'png': 'png', 'gif': 'gif', 
                'bmp': 'bmp', 'webp': 'webp', 'tiff': 'tiff', 'x-icon': 'ico',
                'vnd.microsoft.icon': 'ico', 'x-ms-bmp': 'bmp', 'svg+xml': 'svg',
                'heic': 'heic', 'heif': 'heif', 'avif': 'avif'
            }
            return type_map.get(mime_type, mime_type)
    except Exception as e:
        print(f"⚠️  Erro na detecção com python-magic-bin: {e}")
    return basic_image_detection(image_data)

def get_image_extension(image_data, default='png'):
    detected = get_image_type(image_data)
    if detected:
        extension_map = {
            'jpeg': 'jpg', 'tiff': 'tiff', 'ico': 'ico', 'svg': 'svg',
            'heic': 'heic', 'heif': 'heif', 'avif': 'avif'
        }
        return extension_map.get(detected, detected)
    return default

def basic_image_detection(image_data):
    if not image_data:
        return None
    signatures = {
        b'\xff\xd8\xff': 'jpeg', b'\x89PNG\r\n\x1a\n': 'png', 
        b'GIF87a': 'gif', b'GIF89a': 'gif', b'BM': 'bmp',
        b'RIFF': 'webp', b'II\x2a\x00': 'tiff', b'MM\x00\x2a': 'tiff',
        b'\x00\x00\x01\x00': 'ico', b'ftypheic': 'heic', 
        b'ftypheix': 'heic', b'ftyphevc': 'heic', 
        b'ftypavif': 'avif', b'ftypavis': 'avif',
    }
    for signature, img_type in signatures.items():
        if len(image_data) >= len(signature) and image_data.startswith(signature):
            if img_type == 'webp' and len(image_data) >= 12:
                if image_data[8:12] == b'WEBP':
                    return 'webp'
                return None
            return img_type
    if len(image_data) >= 3 and image_data[:3] == b'\xff\xd8\xff':
        return 'jpeg'
    return None

# =============================================================================
# NOVO v10.3.0: Sistema de Cache LRU com Limite de Memória
# =============================================================================
class SmartConversionCache:
    """Cache inteligente com LRU e limite de memória configurável"""
    
    def __init__(self, cache_dir: Path = Path(".pandoc_cache"), 
                 max_memory_mb: int = 100, max_disk_gb: int = 1):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        
        # Limites de memória
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_memory_bytes = 0
        
        # Cache LRU em memória (OrderedDict mantém ordem de inserção)
        self._memory_cache = OrderedDict()
        self._cache_lock = Lock()
        
        # Limite de disco
        self.max_disk_bytes = max_disk_gb * 1024 * 1024 * 1024
        
        # Estatísticas
        self.stats = {
            'memory_hits': 0,
            'disk_hits': 0,
            'misses': 0,
            'evictions': 0,
            'memory_saves': 0,
            'disk_saves': 0
        }
    
    def get_cache_key(self, content: str, options: dict) -> str:
        """Gera chave única para o conteúdo e opções"""
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        options_hash = hashlib.md5(str(sorted(options.items())).encode('utf-8')).hexdigest()
        return f"{content_hash}_{options_hash}"
    
    def get_cached_conversion(self, key: str) -> Optional[str]:
        """Busca em memória primeiro, depois em disco"""
        with self._cache_lock:
            # 1. Tentar memória (mais rápido)
            if key in self._memory_cache:
                self.stats['memory_hits'] += 1
                # Mover para o final (mais recente usado - LRU)
                self._memory_cache.move_to_end(key)
                return self._memory_cache[key]
        
        # 2. Tentar disco
        cache_file = self.cache_dir / f"{key}.html"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.stats['disk_hits'] += 1
                
                # Adicionar à memória se houver espaço
                self._add_to_memory_cache(key, content)
                return content
            except Exception:
                pass
        
        # 3. Miss - não encontrado
        self.stats['misses'] += 1
        return None
    
    def save_conversion(self, key: str, html_content: str):
        """Salva em memória e disco com gestão inteligente"""
        # Calcular tamanho
        content_size = sys.getsizeof(html_content)
        
        # 1. Salvar em memória se couber
        if self._add_to_memory_cache(key, html_content, content_size):
            self.stats['memory_saves'] += 1
        
        # 2. Sempre salvar em disco (persistência)
        cache_file = self.cache_dir / f"{key}.html"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.stats['disk_saves'] += 1
        except Exception as e:
            logging.warning(f"⚠️  Não foi possível salvar cache em disco: {e}")
    
    def _add_to_memory_cache(self, key: str, content: str, size: int = None) -> bool:
        """Adiciona item ao cache em memória com LRU. Retorna True se adicionado."""
        if size is None:
            size = sys.getsizeof(content)
        
        with self._cache_lock:
            # Remover item se já existe (para recalcular tamanho)
            if key in self._memory_cache:
                old_content = self._memory_cache.pop(key)
                self.current_memory_bytes -= sys.getsizeof(old_content)
            
            # Remover itens antigos se necessário (LRU)
            while (self.current_memory_bytes + size > self.max_memory_bytes 
                   and len(self._memory_cache) > 0):
                # Remover item mais antigo (primeiro do OrderedDict)
                oldest_key, oldest_content = self._memory_cache.popitem(last=False)
                self.current_memory_bytes -= sys.getsizeof(oldest_content)
                self.stats['evictions'] += 1
            
            # Adicionar novo item se couber
            if size <= self.max_memory_bytes:
                self._memory_cache[key] = content
                self.current_memory_bytes += size
                return True
            
            return False
    
    def clear_memory_cache(self):
        """Limpa apenas cache em memória"""
        with self._cache_lock:
            self._memory_cache.clear()
            self.current_memory_bytes = 0
        logging.info("🧹 Cache em memória limpo")
    
    def clear_cache(self):
        """Limpa memória e disco"""
        try:
            self.clear_memory_cache()
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(exist_ok=True)
                return True
        except Exception as e:
            logging.error(f"❌ Erro ao limpar cache: {e}")
        return False
    
    def optimize_disk_cache(self):
        """Remove ficheiros de cache antigos do disco se exceder limite"""
        cache_files = list(self.cache_dir.glob("*.html"))
        
        # Ordenar por data de acesso (mais antigos primeiro)
        cache_files.sort(key=lambda f: f.stat().st_atime)
        
        # Calcular tamanho total
        total_size = sum(f.stat().st_size for f in cache_files)
        
        # Remover mais antigos se exceder limite
        removed = 0
        while total_size > self.max_disk_bytes and cache_files:
            oldest = cache_files.pop(0)
            total_size -= oldest.stat().st_size
            oldest.unlink()
            removed += 1
        
        if removed > 0:
            logging.info(f"🧹 {removed} ficheiros de cache antigos removidos do disco")
        
        return removed
    
    def get_stats(self) -> dict:
        """Retorna estatísticas de uso do cache"""
        total_requests = sum([
            self.stats['memory_hits'],
            self.stats['disk_hits'],
            self.stats['misses']
        ])
        
        return {
            **self.stats,
            'total_requests': total_requests,
            'hit_rate': (self.stats['memory_hits'] + self.stats['disk_hits']) / total_requests 
                       if total_requests > 0 else 0,
            'memory_usage_mb': self.current_memory_bytes / (1024 * 1024),
            'memory_items': len(self._memory_cache),
            'disk_items': len(list(self.cache_dir.glob("*.html")))
        }

# =============================================================================
# NOVO v10.3.0: Preservador de Conteúdo com Modo Estrito
# =============================================================================
class StrictContentPreserver:
    """Modo de preservação estrita - ZERO transformações no conteúdo original"""
    
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self._original_hashes = {}
        self._transformation_log = []
    
    def process_content(self, content: str, conv_id: str, allow_transforms: bool = False) -> str:
        """Processa conteúdo com ou sem transformações"""
        if not content:
            return ""
        
        # Calcular hash original
        original_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        self._original_hashes[conv_id] = original_hash
        
        # MODO ESTRITO: retornar sem modificações
        if self.strict_mode and not allow_transforms:
            return content
        
        # MODO COM TRANSFORMAÇÕES: aplicar normalizações
        if allow_transforms:
            processed = self._apply_safe_transforms(content)
            
            # Verificar se houve alterações
            final_hash = hashlib.md5(processed.encode('utf-8')).hexdigest()
            if original_hash != final_hash:
                self._transformation_log.append({
                    'conv_id': conv_id,
                    'original_hash': original_hash,
                    'final_hash': final_hash,
                    'changed': True
                })
            
            return processed
        
        return content
    
    def _apply_safe_transforms(self, content: str) -> str:
        """Aplica apenas transformações seguras e reversíveis"""
        # 1. Normalizar line endings (universal)
        safe_content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # 2. Remover NULL bytes (perigosos)
        safe_content = safe_content.replace('\x00', '')
        
        # 3. Normalizar Unicode (apenas NFC - forma canônica)
        safe_content = unicodedata.normalize('NFC', safe_content)
        
        return safe_content
    
    def verify_integrity(self, content: str, conv_id: str) -> bool:
        """Verifica se o conteúdo foi alterado"""
        if conv_id not in self._original_hashes:
            return True
        
        current_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        return current_hash == self._original_hashes[conv_id]
    
    def get_transformation_report(self) -> dict:
        """Retorna relatório de transformações aplicadas"""
        total = len(self._original_hashes)
        changed = len(self._transformation_log)
        
        return {
            'mode': 'STRICT' if self.strict_mode else 'TRANSFORMS_ENABLED',
            'total_processed': total,
            'content_changed': changed,
            'integrity_rate': (total - changed) / total if total > 0 else 1.0,
            'details': self._transformation_log
        }

# Manter ContentPreserver original para compatibilidade
class ContentPreserver:
    """Classe legada mantida para compatibilidade"""
    
    def __init__(self, preserve_raw=False):
        self.preserve_raw = preserve_raw
        self._code_block_cache = {}
        self._math_block_cache = {}
    
    def protect_special_content(self, content: str) -> tuple:
        """Protege blocos de código e matemática antes de qualquer processamento"""
        if not content:
            return content, {}, {}
        
        code_blocks = {}
        math_blocks = {}
        
        # Proteger blocos de código
        def protect_code(match):
            block_id = f"__CODE_BLOCK_{len(code_blocks)}__"
            code_blocks[block_id] = match.group(0)
            return block_id
        
        protected_content = re.sub(
            r'```.*?```|`[^`]+`', 
            protect_code, 
            content, 
            flags=re.DOTALL
        )
        
        # Proteger fórmulas matemáticas
        def protect_math(match):
            block_id = f"__MATH_BLOCK_{len(math_blocks)}__"
            math_blocks[block_id] = match.group(0)
            return block_id
        
        protected_content = re.sub(
            r'\$\$.*?\$\$|\$.*?\$', 
            protect_math, 
            protected_content, 
            flags=re.DOTALL
        )
        
        return protected_content, code_blocks, math_blocks
    
    def restore_special_content(self, content: str, code_blocks: dict, math_blocks: dict) -> str:
        """Restaura blocos de código e matemática após processamento"""
        if self.preserve_raw:
            return content
            
        restored_content = content
        
        # Restaurar matemática primeiro (para evitar conflitos)
        for block_id, original_math in math_blocks.items():
            restored_content = restored_content.replace(block_id, original_math)
        
        # Restaurar código
        for block_id, original_code in code_blocks.items():
            restored_content = restored_content.replace(block_id, original_code)
        
        return restored_content

class ClaudeProcessor:
    def __init__(self):
        self.conversations = []
        self.all_messages = []

    def load_claude_data(self, data_dir: Path):
        zip_files = ["data_claude.zip", "data_claude-*.zip"]
        zip_path = None
        if (data_dir / "data_claude.zip").exists():
            zip_path = data_dir / "data_claude.zip"
        else:
            data_zips = list(data_dir.glob("data_claude-*.zip"))
            if data_zips:
                zip_path = data_zips[0]
        if zip_path is None:
            print("❌ Nenhum arquivo data_claude.zip encontrado!")
            return None
        print(f"📂 Carregando dados do {zip_path}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
                print(f"📋 Processando {len(json_files)} arquivos JSON...")
                all_data = []
                for file_name in json_files:
                    try:
                        with zip_ref.open(file_name) as f:
                            content = f.read().decode('utf-8')
                            data = json.loads(content)
                            all_data.append({
                                'file_name': file_name,
                                'data': data,
                                'size': len(content)
                            })
                    except Exception as e:
                        print(f"⚠️  {file_name}: {e}")
                print(f"✅ Dados brutos carregados: {len(all_data)} arquivos")
                return all_data
        except Exception as e:
            print(f"❌ Erro ao processar {zip_path}: {e}")
            return None

    def extract_conversations(self, all_data):
        print("📊 Extraindo conversas...")
        self.conversations = []
        for item in all_data:
            data = item['data']
            file_name = item['file_name']
            if isinstance(data, list):
                print(f"✅ {file_name}: {len(data)} conversas encontradas")
                self.conversations.extend(data)
            elif isinstance(data, dict):
                if 'conversations' in data:
                    convs = data['conversations']
                    if isinstance(convs, list):
                        print(f"✅ {file_name}: {len(convs)} conversas encontradas")
                        self.conversations.extend(convs)
                else:
                    print(f"✅ {file_name}: 1 conversa encontrada")
                    self.conversations.append(data)
        print(f"🎯 Total de conversas extraídas: {len(self.conversations)}")
        return self.conversations

    def extract_messages(self, conv):
        messages = []
        if isinstance(conv, dict):
            chat_messages = conv.get('chat_messages', [])
            for msg in chat_messages:
                if isinstance(msg, dict):
                    content = msg.get('text', '')
                    sender = msg.get('sender', '')
                    if content and sender:
                        messages.append({
                            'content': content,
                            'sender': sender,
                            'uuid': msg.get('uuid', ''),
                            'created_at': msg.get('created_at', ''),
                            'updated_at': msg.get('updated_at', '')
                        })
        return messages

    def parse_datetime(self, date_string):
        if not date_string:
            return None
        try:
            if isinstance(date_string, str):
                date_str = date_string.replace('Z', '+00:00')
                if '+' in date_str or '-' in date_str[-6:]:
                    return datetime.fromisoformat(date_str.rsplit('+', 1)[0].rsplit('-', 1)[0])
                return datetime.fromisoformat(date_str)
            return None
        except:
            return None

    def process_claude_conversations(self):
        print("📄 Processando conversas do Claude...")
        if not self.conversations:
            print("❌ Nenhuma conversa para processar!")
            return []
        processed_conversations = []
        for i, conv in enumerate(self.conversations):
            if not isinstance(conv, dict):
                continue
            conv_id = conv.get('uuid', f'claude_{i}')
            title = conv.get('name', f'Conversa Claude {i+1}')
            created_at = conv.get('created_at', '')
            updated_at = conv.get('updated_at', '')
            messages = self.extract_messages(conv)
            formatted_messages = []
            for j, msg in enumerate(messages):
                if isinstance(msg, dict):
                    content = msg.get('content', '')
                    sender = msg.get('sender', '')
                    if content and sender:
                        if sender == 'human':
                            author = "👤 Utilizador"
                            role = 'user'
                        elif sender == 'assistant':
                            author = "🤖 Claude"
                            role = 'assistant'
                        else:
                            author = f"🔹 {sender.title()}"
                            role = sender
                        formatted_messages.append({
                            'author': author,
                            'role': role,
                            'content': content,
                            'timestamp': self.parse_datetime(msg.get('created_at', '')),
                            'model': 'Claude',
                            'attachments': []
                        })
            if formatted_messages:
                processed_conversations.append({
                    'title': title,
                    'source': 'Claude',
                    'id': conv_id,
                    'inserted_at': self.parse_datetime(created_at),
                    'updated_at': self.parse_datetime(updated_at),
                    'created_at': created_at,
                    'updated_at_raw': updated_at,
                    'messages': formatted_messages,
                    'summary': formatted_messages[0]['content'][:100] + "..." if formatted_messages else "Sem conteúdo",
                    'category': self.categorize_conversation(title)
                })
        print(f"✅ Claude: {len(processed_conversations)} conversas processadas")
        return processed_conversations

    def categorize_conversation(self, title):
        title_lower = title.lower()
        categories = {
            'Programação': ['python', 'code', 'script', 'api', 'function', 'class', 'java', 'javascript', 'html', 'css', 'programming'],
            'Sistemas': ['linux', 'ubuntu', 'windows', 'install', 'os', 'system', 'server', 'terminal'],
            'Dados': ['data', 'analysis', 'pandas', 'dataframe', 'csv', 'excel', 'database', 'sql'],
            'IA & ML': ['ai', 'ml', 'model', 'neural', 'machine learning', 'deep learning', 'llm', 'gpt'],
            'Web': ['web', 'browser', 'http', 'website', 'url', 'internet', 'html', 'css'],
            'Escrita': ['write', 'text', 'document', 'article', 'essay', 'story', 'writing'],
            'Tradução': ['translate', 'translation', 'language', 'português', 'english'],
            'Matemática': ['math', 'calculation', 'equation', 'formula', 'statistics'],
            'Ajuda': ['help', 'ajuda', 'como', 'tutorial', 'guide', 'how to'],
            'Pesquisa': ['research', 'search', 'find', 'information', 'study']
        }
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        return 'Geral'

_precompiled_patterns = {
    'invalid_chars': re.compile(r'[<>:"/\\|?*\x00-\x1F\x7F\s]'),
    'multiple_underscores': re.compile(r'_+'),
    'base64_image': re.compile(r'data:image/([^;]+);base64,([^\s"\']+)'),
    'image_url': re.compile(r'!\[[^\]]*\]\(([^\)]+)\)'),
    'file_reference': re.compile(r'\[arquivo:([^\]]+)\]'),
    'code_blocks': re.compile(r'```.*?```|`[^`]+`', re.DOTALL),
}

class PerformanceTimer:
    def __init__(self, operation_name: str = "Operação"):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        logger.info(f"⏱️  Iniciando: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        elapsed = self.end_time - self.start_time
        logger.info(f"⏱️  {self.operation_name} concluído em {elapsed:.2f}s")

    def get_elapsed(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0

class CombinedFragmentsSystem:
    def __init__(self, dry_run=False, force_overwrite=False, clear_cache=False,
                 process_attachments=False, batch_processing=True, debug_mode=False,
                 backup_original=False, checksum=False, 
                 strict_preserve=True, allow_transforms=False,
                 cache_memory_mb=100, cache_disk_gb=1):  # NOVO v10.3.0
        self.data_dir = Path("data")
        self.dry_run = dry_run
        self.start_time = time.perf_counter()
        self.force_overwrite = force_overwrite
        self.skip_attachments = not process_attachments
        self.batch_processing = batch_processing
        self.debug_mode = debug_mode
        self.backup_original = backup_original
        self.checksum = checksum
        
        # NOVO v10.3.0: Modo de preservação estrito como padrão
        self.strict_preserve = strict_preserve
        self.allow_transforms = allow_transforms
        
        logging.basicConfig(
            level=logging.DEBUG if debug_mode else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # NOVO v10.3.0: Cache otimizado com limite de memória
        self.conversion_cache = SmartConversionCache(
            cache_dir=Path(".pandoc_cache"),
            max_memory_mb=cache_memory_mb,
            max_disk_gb=cache_disk_gb
        )
        
        # NOVO v10.3.0: Preservador de conteúdo com modo estrito
        self.content_preserver = StrictContentPreserver(strict_mode=strict_preserve)
        
        if strict_preserve and not allow_transforms:
            self.logger.warning("⚠️  MODO ESTRITO ATIVADO: Conteúdo será preservado SEM transformações")
        elif allow_transforms:
            self.logger.info("ℹ️  Transformações de conteúdo ATIVADAS")
        
        self.enable_cache = True
        self.claude_processor = ClaudeProcessor()
        self.original_backups_dir = Path("original_backups")
        
        if clear_cache:
            if self.conversion_cache.clear_cache():
                self.logger.info("✅ Cache limpo com sucesso")
            else:
                self.logger.error("❌ Falha ao limpar cache")
        
        self.output_dirs = {
            'markdown': "combined_markdown",
            'csv': "combined_csv", 
            'json': "combined_json",
            'pdfs': "combined_pdfs",
            'html': "combined_html",
            'attachments': "combined_attachments"
        }
        
        self.single_files = {
            'csv': "combined_all_conversations.csv",
            'json': "combined_all_conversations.json"
        }
        
        self.index_file = "index.html"
        self.all_conversations = []
        
        self.processors = {
            'qwen': {'file': "chat-export.json", 'method': self.process_qwen_corrected, 'enabled': True},
            'chatgpt': {'file': "chatgpt.zip", 'method': self.process_chatgpt, 'enabled': True},
            'deepseek': {'file': "deepseek_data.zip", 'method': self.process_deepseek, 'enabled': True},
            'grok': {'file': "grok.zip", 'method': self.process_grok, 'enabled': True},
            'claude': {'file': "data_claude.zip", 'method': self.process_claude, 'enabled': True}
        }
        
        try:
            import requests
            self.requests_available = True
        except ImportError:
            self.requests_available = False
            self.logger.warning("⚠️ Biblioteca 'requests' não disponível - URLs de imagem não serão baixadas")
    
    def _should_write_file(self, filepath: Path, new_content: str) -> bool:
        """Verifica se o conteúdo mudou antes de escrever o ficheiro."""
        if not filepath.exists():
            return True
        
        try:
            existing_hash = compute_checksum(filepath)
            new_hash = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
            return existing_hash != new_hash
        except Exception:
            return True  # Em caso de erro, escrever por segurança
    
    def sanitize_filename_optimized(self, text: str, max_len: int = 50) -> str:
        if not text or not isinstance(text, str):
            return "conversa_sem_titulo"
        sanitized = _precompiled_patterns['invalid_chars'].sub('_', text)
        sanitized = _precompiled_patterns['multiple_underscores'].sub('_', sanitized)
        sanitized = sanitized.strip('_')
        if not sanitized:
            sanitized = "conversa_sem_titulo"
        if len(sanitized) > max_len:
            if '_' in sanitized[:max_len]:
                last_underscore = sanitized[:max_len].rfind('_')
                if last_underscore > 10:
                    sanitized = sanitized[:last_underscore]
            else:
                sanitized = sanitized[:max_len]
        return sanitized
    
    def extract_and_save_attachments_optimized(self, content: str, conv_number: int, msg_index: int) -> tuple:
        if not content or self.skip_attachments:
            return content, []
        
        saved_files = []
        modified_content = content
        
        base64_matches = _precompiled_patterns['base64_image'].findall(content)
        for i, (img_type, base64_data) in enumerate(base64_matches):
            try:
                image_data = base64.b64decode(base64_data)
                extension = get_image_extension(image_data, 'png')
                filename = f"conv_{conv_number:03d}_msg_{msg_index:02d}_img_{i:02d}.{extension}"
                filepath = Path(self.output_dirs['attachments']) / filename
                
                if not self.dry_run:
                    Path(self.output_dirs['attachments']).mkdir(parents=True, exist_ok=True)
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                
                replacement = f"![Imagem {i+1}]({self.output_dirs['attachments']}/{filename})"
                modified_content = modified_content.replace(
                    f"data:image/{img_type};base64,{base64_data}", 
                    replacement
                )
                saved_files.append(str(filepath))
            except Exception as e:
                if self.debug_mode:
                    self.logger.warning(f"⚠️ Erro ao processar imagem base64: {e}")
        
        return modified_content, saved_files
    
    def sanitize_filename(self, text: str, max_len: int = 50) -> str:
        return self.sanitize_filename_optimized(text, max_len)
    
    def preserve_original_title(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return "Conversa sem título"
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized = re.sub(invalid_chars, '', text)
        sanitized = re.sub(r'\s+', ' ', sanitized.strip())
        if not sanitized:
            sanitized = "Conversa sem título"
        return sanitized
    
    def backup_original_file(self, path: Path, prefix: str = "backup"):
        if not self.backup_original or self.dry_run:
            return
        
        self.original_backups_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{prefix}_{timestamp}{path.suffix}"
        backup_path = self.original_backups_dir / backup_name
        shutil.copy2(path, backup_path)
        self.logger.info(f"💾 Backup salvo: {backup_path}")
        
        if self.checksum:
            chk = compute_checksum(path)
            checksum_file = backup_path.with_suffix(backup_path.suffix + ".sha256")
            with open(checksum_file, "w") as f:
                f.write(f"{chk}  {path.name}\n")
            self.logger.info(f"🔐 Checksum SHA-256 salvo: {checksum_file}")
    
    def extract_and_save_attachments(self, content: str, conv_number: int, msg_index: int) -> tuple:
        return self.extract_and_save_attachments_optimized(content, conv_number, msg_index)
    
    def process_qwen_attachments(self, content_list: list, conv_number: int, msg_index: int) -> tuple:
        if not content_list or not isinstance(content_list, list):
            return "", []
        
        content_parts = []
        saved_files = []
        
        for item in content_list:
            if isinstance(item, dict):
                item_type = item.get('type', '')
                if item_type == 'image' and 'data' in item:
                    try:
                        image_data = item['data']
                        if image_data.startswith('data:image'):
                            base64_match = re.search(r'base64,([^\"]+)', image_data)
                            if base64_match:
                                base64_str = base64_match.group(1)
                                image_binary = base64.b64decode(base64_str)
                                extension = get_image_extension(image_binary, 'png')
                                filename = f"qwen_conv_{conv_number:03d}_msg_{msg_index:02d}.{extension}"
                                filepath = Path(self.output_dirs['attachments']) / filename
                                
                                if not self.dry_run:
                                    Path(self.output_dirs['attachments']).mkdir(parents=True, exist_ok=True)
                                    with open(filepath, 'wb') as f:
                                        f.write(image_binary)
                                
                                content_parts.append(f"![Imagem Qwen]({self.output_dirs['attachments']}/{filename})")
                                saved_files.append(str(filepath))
                    except Exception as e:
                        self.logger.warning(f"⚠️ Erro ao processar imagem Qwen: {e}")
                elif item_type == 'text' and 'text' in item:
                    content_parts.append(str(item['text']))
        
        return '\n'.join(content_parts), saved_files
    
    def preserve_special_content_enhanced(self, content: str, conv_id: str = "") -> str:
        """NOVO v10.3.0: Usa StrictContentPreserver"""
        return self.content_preserver.process_content(
            content, 
            conv_id, 
            allow_transforms=self.allow_transforms
        )
    
    def ensure_directories(self):
        if self.dry_run:
            self.logger.info("DRY-RUN: Pastas seriam criadas:")
            for folder in self.output_dirs.values():
                self.logger.info(f"   {folder}")
            return
        
        for folder in self.output_dirs.values():
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pasta criada: {folder}")
    
    def run(self):
        start_time = time.perf_counter()
        self.logger.info(f"SISTEMA COMBINADO v{SCRIPT_VERSION} - OTIMIZADO E ROBUSTO")
        self.logger.info("=" * 70)
        
        if not self.data_dir.exists():
            self.logger.error(f"Pasta '{self.data_dir}' não encontrada.")
            self.logger.info("Crie a pasta 'data' e coloque os arquivos de exportação:")
            for source_name, config in self.processors.items():
                self.logger.info(f"   - {config['file']} (para {source_name.upper()})")
            return
        
        self.logger.info(f"Usando pasta de dados: {self.data_dir.absolute()}")
        self.ensure_directories()
        
        processed_count = 0
        for source_name, config in self.processors.items():
            if config['enabled']:
                file_path = self.data_dir / config['file']
                if file_path.exists():
                    self.logger.info(f"\nProcessando {source_name.upper()}...")
                    config['method'](file_path)
                    processed_count += 1
                else:
                    self.logger.warning(f"{source_name.upper()}: arquivo não encontrado - {file_path}")
        
        if processed_count == 0:
            self.logger.error("Nenhum arquivo de exportação encontrado na pasta 'data'.")
            return
        
        if not self.all_conversations:
            self.logger.error("Nenhuma conversa foi extraída dos arquivos.")
            return
        
        partial_time = time.perf_counter() - start_time
        self.logger.info(f"⏱️  Fase de extração concluída em {partial_time:.2f}s")
        
        self._post_process_conversations()
        
        if not self.dry_run:
            self._export_all_formats()
            
            # NOVO v10.3.0: Relatório de preservação de conteúdo
            preservation_report = self.content_preserver.get_transformation_report()
            self.logger.info(f"\n📊 RELATÓRIO DE PRESERVAÇÃO:")
            self.logger.info(f"   Modo: {preservation_report['mode']}")
            self.logger.info(f"   Total processado: {preservation_report['total_processed']}")
            self.logger.info(f"   Conteúdo alterado: {preservation_report['content_changed']}")
            self.logger.info(f"   Taxa de integridade: {preservation_report['integrity_rate']:.2%}")
            
            # NOVO v10.3.0: Estatísticas do cache
            cache_stats = self.conversion_cache.get_stats()
            self.logger.info(f"\n📊 ESTATÍSTICAS DE CACHE:")
            self.logger.info(f"   Total de requisições: {cache_stats['total_requests']}")
            self.logger.info(f"   Hits em memória: {cache_stats['memory_hits']}")
            self.logger.info(f"   Hits em disco: {cache_stats['disk_hits']}")
            self.logger.info(f"   Misses: {cache_stats['misses']}")
            self.logger.info(f"   Taxa de acerto: {cache_stats['hit_rate']:.2%}")
            self.logger.info(f"   Uso de memória: {cache_stats['memory_usage_mb']:.2f} MB")
            self.logger.info(f"   Items em memória: {cache_stats['memory_items']}")
            self.logger.info(f"   Evicções (LRU): {cache_stats['evictions']}")
            
            self.logger.info(f"\n🎉 SISTEMA COMBINADO v{SCRIPT_VERSION} FINALIZADO!")
            self.logger.info(f"📄 Índice: {self.index_file}")
            
            if Path(self.index_file).exists():
                webbrowser.open(f'file://{Path(self.index_file).absolute()}')
        else:
            total_time = time.perf_counter() - start_time
            self.logger.info(f"⏱️  TEMPO TOTAL (DRY-RUN): {total_time:.2f}s")
            self.logger.info(f"\n🔮 MODO DRY-RUN: Nenhum arquivo foi criado.")
    
    def _post_process_conversations(self):
        self.all_conversations.sort(
            key=lambda x: self.parse_timestamp_for_sorting(
                x.get('updated_at') or x.get('inserted_at') or x.get('created_at')
            ),
            reverse=True
        )
        
        for i, conv in enumerate(self.all_conversations):
            conv['number'] = i + 1
            conv['category'] = self.categorize_conversation(conv['title'], conv.get('summary', ''))
            conv.setdefault('source', 'Desconhecido')
            conv.setdefault('messages', [])
            conv.setdefault('summary', conv['messages'][0]['content'][:100] + "..." if conv['messages'] else "Sem conteúdo")
        
        self.logger.info(f"📊 Total combinado de conversas: {len(self.all_conversations)}")
    
    def _export_all_formats(self):
        export_start = time.perf_counter()
        self.logger.info("\n📄 Iniciando exportação para todos os formatos...")
        
        self.save_as_markdown_enhanced()
        self.save_as_html_robust()
        self.save_as_csv() 
        self.save_as_json()
        self.save_all_to_single_files()
        self.create_searchable_index_enhanced()
        
        export_time = time.perf_counter() - export_start
        self.logger.info(f"⏱️  Fase de exportação concluída em {export_time:.2f}s")
    
    def _get_pandoc_version(self) -> Optional[tuple]:
        try:
            result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                version_str = first_line.split()[1]
                return tuple(map(int, version_str.split('.')))
        except:
            pass
        return None
    
    def _convert_with_pandoc_cached(self, md_file_path: str) -> Optional[str]:
        """NOVO v10.3.0: Conversão com cache otimizado"""
        if not self.enable_cache:
            return self._convert_with_pandoc_optimized(md_file_path)
        
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            cache_options = {
                'pandoc_version': self._get_pandoc_version(),
                'mathjax_local': Path("assets/tex-mml-chtml.js").exists()
            }
            
            cache_key = self.conversion_cache.get_cache_key(md_content, cache_options)
            
            # Tentar cache primeiro
            cached_html = self.conversion_cache.get_cached_conversion(cache_key)
            if cached_html:
                self.logger.info(f"✅ Usando cache: {Path(md_file_path).name}")
                return cached_html
            
            # Converter com Pandoc
            html_content = self._convert_with_pandoc_optimized(md_file_path)
            
            if html_content:
                self.conversion_cache.save_conversion(cache_key, html_content)
            
            return html_content
        
        except Exception as e:
            self.logger.error(f"❌ Erro no cache Pandoc: {e}")
            return self._convert_with_pandoc_optimized(md_file_path)
    
    def _convert_with_pandoc_optimized(self, md_file_path: str) -> Optional[str]:
        """NOVO v10.3.0: Conversão otimizada com processamento em blocos"""
        try:
            self.logger.info(f"🔧 Convertendo com Pandoc: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown+emoji+autolink_bare_uris+tex_math_single_backslash',
                '--to', 'html5',
                '--standalone',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}',
                '--table-of-contents',
                f'--toc-depth={TOC_DEPTH}',
                '--number-sections'
            ]
            
            pandoc_version = self._get_pandoc_version()
            if pandoc_version and pandoc_version >= (2, 19):
                command.append('--embed-resources')
                self.logger.info("✅ Usando --embed-resources (Pandoc 2.19+)")
            
            command.extend(['--syntax-highlighting=pygments'])
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=180
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc otimizado falhou: {result.stderr[:200]}")
                return self._convert_with_pandoc_basic(md_file_path)
        
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout no Pandoc otimizado")
            return self._convert_with_pandoc_basic(md_file_path)
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc otimizado: {e}")
            return self._convert_with_pandoc_basic(md_file_path)
    
    def _convert_with_pandoc_basic(self, md_file_path: str) -> Optional[str]:
        try:
            self.logger.info(f"🔧 Tentando conversão básica: {Path(md_file_path).name}")
            
            mathjax_path = Path("assets/tex-mml-chtml.js")
            mathjax_arg = f"assets/tex-mml-chtml.js" if mathjax_path.exists() else ""
            
            command = [
                'pandoc', 
                str(md_file_path),
                '--from', 'markdown',
                '--to', 'html5',
                '--standalone',
                '--table-of-contents',
                f'--toc-depth={TOC_DEPTH}',
                '--number-sections',
                '--mathjax' if not mathjax_path.exists() else f'--mathjax={mathjax_arg}'
            ]
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                timeout=120
            )
            
            if result.returncode == 0:
                html_content = result.stdout
                html_content = self._optimize_html_content(html_content)
                return html_content
            else:
                self.logger.warning(f"⚠️ Pandoc básico falhou: {result.stderr[:200]}")
                return self._convert_with_fallback(md_file_path)
        
        except Exception as e:
            self.logger.error(f"❌ Erro no Pandoc básico: {e}")
            return self._convert_with_fallback(md_file_path)
    
    def _optimize_html_content(self, html_content: str) -> str:
        if '<head>' in html_content and 'viewport' not in html_content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            html_content = html_content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        if '<html' in html_content and 'lang' not in html_content:
            html_content = html_content.replace('<html>', '<html lang="pt-BR">')
        
        html_content = self._apply_fixed_toc_styles(html_content)
        return html_content
    
    def _apply_fixed_toc_styles(self, html_content: str) -> str:
        """Aplica estilos para TOC fixo à direita com botão minimizar e scrollspy"""
        fixed_toc_css = f"""
        <style id="fixed-toc-styles">
        /* === ESTILOS PRINCIPAIS - TOC FIXO À DIREITA === */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
            scroll-behavior: smooth;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            position: relative;
        }}
        /* === TOC FIXO À DIREITA - POSIÇÃO CORRIGIDA === */
        #TOC {{
            position: fixed !important;
            top: 50% !important;
            right: 20px !important;
            transform: translateY(-50%) !important;
            width: {TOC_FIXED_WIDTH} !important;
            max-height: 80vh !important;
            overflow-y: auto !important;
            z-index: 1000 !important;
            background: rgba(255, 255, 255, 0.98) !important;
            padding: 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important;
            border: 1px solid #e0e0e0 !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.3s ease-in-out !important;
        }}
        #TOC.toc-minimized {{
            transform: translateY(-50%) translateX(calc({TOC_FIXED_WIDTH} - 50px)) !important;
            opacity: 0.3;
            width: 50px !important;
            overflow: hidden;
        }}
        #TOC.toc-minimized > *:not(.toc-toggle-btn) {{
            display: none !important;
        }}
        #TOC h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 1.2em;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .toc-toggle-btn {{
            background: none;
            border: none;
            font-size: 1.2em;
            cursor: pointer;
            padding: 5px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        .toc-toggle-btn:hover {{
            background-color: rgba(0,0,0,0.1);
        }}
        #TOC ul {{
            list-style-type: none;
            padding-left: 15px;
            margin: 10px 0;
        }}
        #TOC ul ul {{
            padding-left: 20px;
        }}
        #TOC li {{
            margin: 8px 0;
            line-height: 1.4;
        }}
        #TOC a {{
            text-decoration: none;
            color: #495057;
            font-weight: 500;
            transition: all 0.2s ease;
            display: block;
            padding: 6px 10px;
            border-radius: 6px;
            border-left: 3px solid transparent;
        }}
        #TOC a:hover {{
            color: #007bff;
            background-color: rgba(0, 123, 255, 0.1);
            border-left-color: #007bff;
        }}
        #TOC a.active {{
            background-color: #007bff !important;
            color: white !important;
            font-weight: bold;
            border-left-color: #0056b3;
        }}
        /* Conteúdo principal com margem para o TOC */
        .main-content {{
            margin-right: calc({TOC_FIXED_WIDTH} + 40px) !important;
        }}
        /* Barra de scroll personalizada APENAS para TOC */
        #TOC::-webkit-scrollbar {{
            width: {TOC_SCROLLBAR_WIDTH};
        }}
        #TOC::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        #TOC::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 4px;
        }}
        #TOC::-webkit-scrollbar-thumb:hover {{
            background: #a8a8a8;
        }}
        /* === BOTÃO VOLTAR AO TOPO (HTMLs individuais) === */
        .back-to-top-content {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .back-to-top-content.show {{
            opacity: 1;
            transform: translateY(0);
        }}
        .back-to-top-content:hover {{
            background: #0056b3;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }}
        /* === RESPONSIVIDADE === */
        @media (max-width: 1400px) {{
            .container {{
                max-width: 95%;
                padding: 30px;
            }}
            #TOC {{
                width: 280px !important;
            }}
            .main-content {{
                margin-right: 320px !important;
            }}
        }}
        @media (max-width: 1200px) {{
            #TOC {{
                width: 260px !important;
                right: 15px !important;
            }}
            .main-content {{
                margin-right: 300px !important;
            }}
        }}
        @media (max-width: 992px) {{
            #TOC {{
                position: relative !important;
                width: 100% !important;
                right: 0 !important;
                top: 0 !important;
                transform: none !important;
                margin: 20px 0;
                max-height: 300px !important;
            }}
            .main-content {{
                margin-right: 0 !important;
            }}
            .back-to-top-content {{
                right: 20px;
                bottom: 20px;
            }}
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .container {{
                padding: 20px;
                max-width: 100%;
            }}
            #TOC {{
                max-height: 250px !important;
                padding: 15px !important;
            }}
        }}
        </style>
        """
        
        fixed_toc_js = """
        <script id="fixed-toc-script">
        document.addEventListener('DOMContentLoaded', function() {
            const toc = document.getElementById('TOC');
            if (toc) {
                const tocTitle = toc.querySelector('h2');
                if (tocTitle) {
                    const toggleBtn = document.createElement('button');
                    toggleBtn.innerHTML = '☰';
                    toggleBtn.className = 'toc-toggle-btn';
                    toggleBtn.title = 'Minimizar/Expandir TOC';
                    let isMinimized = false;
                    toggleBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        isMinimized = !isMinimized;
                        if (isMinimized) {
                            toc.classList.add('toc-minimized');
                        } else {
                            toc.classList.remove('toc-minimized');
                        }
                    });
                    tocTitle.appendChild(toggleBtn);
                }
            }
            
            // SCROLLSPY
            const sections = document.querySelectorAll('h1, h2, h3, h4, h5');
            const tocLinks = document.querySelectorAll('#TOC a');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.getAttribute('id');
                        tocLinks.forEach(link => {
                            link.classList.remove('active');
                            if (link.getAttribute('href') === '#' + id) {
                                link.classList.add('active');
                            }
                        });
                    }
                });
            }, { 
                rootMargin: '-20% 0px -60% 0px', 
                threshold: 0 
            });
            
            sections.forEach(section => {
                if (section.id) observer.observe(section);
            });
            
            // Scroll suave
            tocLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        const offsetTop = targetElement.offsetTop - 80;
                        window.scrollTo({ top: offsetTop, behavior: 'smooth' });
                    }
                });
            });
            
            // BOTÃO VOLTAR AO TOPO
            const backToTopBtn = document.createElement('button');
            backToTopBtn.className = 'back-to-top-content';
            backToTopBtn.innerHTML = '↑';
            backToTopBtn.title = 'Voltar ao Topo';
            document.body.appendChild(backToTopBtn);
            
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    backToTopBtn.classList.add('show');
                } else {
                    backToTopBtn.classList.remove('show');
                }
            });
            
            backToTopBtn.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
        </script>
        """
        
        # Aplicar CSS e JS
        if '<head>' in html_content:
            html_content = re.sub(r'<style[^>]*id="fixed-toc-styles"[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
            html_content = html_content.replace('<head>', f'<head>\n{fixed_toc_css}')
        else:
            html_content = f'<head>\n{fixed_toc_css}\n</head>\n{html_content}'
        
        if '</body>' in html_content:
            html_content = re.sub(r'<script[^>]*id="fixed-toc-script"[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
            html_content = html_content.replace('</body>', f'{fixed_toc_js}\n</body>')
        else:
            html_content = f'{html_content}\n{fixed_toc_js}'
        
        return html_content
    
    def _convert_with_fallback(self, md_file_path: str) -> str:
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            extensions = ['extra', 'tables', 'fenced_code', 'codehilite', 'toc', 'md_in_html', 'attr_list']
            html_content = markdown.markdown(md_content, extensions=extensions, output_format='html5')
            return self._create_simple_template(html_content, Path(md_file_path).name)
        except Exception as e:
            self.logger.error(f"❌ Fallback também falhou: {e}")
            return self._create_basic_html(md_content, Path(md_file_path).name)
    
    def _create_simple_template(self, content: str, title: str) -> str:
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        .auth-loading {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-size: 1.2em;
            color: #333;
        }}
        body.dark-mode .auth-loading {{
            background: rgba(30,30,30,0.95);
            color: #e0e0e0;
        }}
        .auth-spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .back-button {{
            margin-bottom: 20px;
            background: #6c757d;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-family: inherit;
        }}
        .back-button:hover {{
            background: #5a6268;
        }}
    </style>
</head>
<body>
    <!-- Tela de autenticação -->
    <div id="authLoading" class="auth-loading">
        <div class="auth-spinner"></div>
        <p>Verificando autenticação...</p>
    </div>

    <div id="mainContent" style="display: none;">
        <!-- Botão Voltar ao Dashboard -->
        <button onclick="window.location.href='../app/dashboard.html'" class="back-button">← Voltar ao Dashboard</button>
        
        <div class="container">
            <div class="main-content">
                {content}
            </div>
        </div>
    </div>

    <script>
        const WORKER_URL = 'https://worker-ds.mpmendespt.workers.dev';
        
        // ✅ PROTEÇÃO: Verificar autenticação ao carregar a página
        document.addEventListener('DOMContentLoaded', function() {{
            const token = localStorage.getItem('jwt');
            
            if (!token) {{
                // Não está logado - redirecionar para login
                console.log('Nenhum token encontrado - redirecionando para login');
                window.location.href = '../app/login.html';
                return;
            }}
            
            // Está logado - verificar token
            verifyToken(token);
        }});

        async function verifyToken(token) {{
            try {{
                const response = await fetch(`${{WORKER_URL}}/api/protected`, {{
                    headers: {{
                        'Authorization': `Bearer ${{token}}`,
                        'Content-Type': 'application/json'
                    }}
                }});
                
                if (!response.ok) {{
                    // Token inválido ou expirado
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('user');
                    window.location.href = '../app/login.html';
                    return;
                }}
                
                // Token válido - mostrar conteúdo
                document.getElementById('authLoading').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
                
            }} catch (error) {{
                console.error('Token verification error:', error);
                // Em caso de erro de rede, mostrar conteúdo com aviso
                document.getElementById('authLoading').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
            }}
        }}

        // ✅ PROTEÇÃO: Verificar autenticação periodicamente
        setInterval(function() {{
            const token = localStorage.getItem('jwt');
            if (!token) {{
                window.location.href = '../app/login.html';
            }}
        }}, 5 * 60 * 1000); // 5 minutos
    </script>
    
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""
        return self._apply_fixed_toc_styles(template)
    
    def _create_basic_html(self, content: str, title: str) -> str:
        mathjax_src = "assets/tex-mml-chtml.js" if Path("assets/tex-mml-chtml.js").exists() else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f5f5f5;
            max-width: none;
            color: #333 !important;
        }}
        pre {{ 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
            color: #333 !important;
        }}
        code {{
            color: #333 !important;
            background: white !important;
        }}
        .container {{
            max-width: 95%;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .auth-loading {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-size: 1.2em;
            color: #333;
        }}
        .auth-spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .back-button {{
            margin-bottom: 20px;
            background: #6c757d;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
        }}
        .back-button:hover {{
            background: #5a6268;
        }}
    </style>
</head>
<body>
    <!-- Tela de autenticação -->
    <div id="authLoading" class="auth-loading">
        <div class="auth-spinner"></div>
        <p>Verificando autenticação...</p>
    </div>

    <div id="mainContent" style="display: none;">
        <!-- Botão Voltar ao Dashboard -->
        <button onclick="window.location.href='../app/dashboard.html'" class="back-button">← Voltar ao Dashboard</button>
        
        <div class="container">
            <pre>{content}</pre>
        </div>
    </div>

    <script>
        const WORKER_URL = 'https://worker-ds.mpmendespt.workers.dev';
        
        document.addEventListener('DOMContentLoaded', function() {{
            const token = localStorage.getItem('jwt');
            if (!token) {{
                window.location.href = '../app/login.html';
                return;
            }}
            verifyToken(token);
        }});

        async function verifyToken(token) {{
            try {{
                const response = await fetch(`${{WORKER_URL}}/api/protected`, {{
                    headers: {{
                        'Authorization': `Bearer ${{token}}`,
                        'Content-Type': 'application/json'
                    }}
                }});
                
                if (!response.ok) {{
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('user');
                    window.location.href = '../app/login.html';
                }} else {{
                    document.getElementById('authLoading').style.display = 'none';
                    document.getElementById('mainContent').style.display = 'block';
                }}
            }} catch (error) {{
                console.error('Token verification error:', error);
                document.getElementById('authLoading').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
            }}
        }}
    </script>
    
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            }}
        }};
    </script>
    <script src="{mathjax_src}" async></script>
</body>
</html>"""
    
    def save_as_html_robust(self):
        """NOVO v10.3.0: Conversão com processamento em blocos menores"""
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] HTMLs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.html"
                self.logger.info(f"   🌐 {filename}")
            return
        
        markdown_folder = Path(self.output_dirs['markdown'])
        html_folder = Path(self.output_dirs['html'])
        md_files = list(markdown_folder.glob("*.md"))
        
        if not md_files:
            self.logger.error("❌ Nenhum arquivo Markdown encontrado para conversão.")
            return
        
        self.logger.info(f"📄 Convertendo {len(md_files)} arquivos Markdown para HTML...")
        
        # Verificar se Pandoc está disponível
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
            pandoc_available = True
            self.logger.info("✅ Pandoc disponível - usando conversão otimizada")
        except:
            pandoc_available = False
            self.logger.warning("⚠️ Pandoc não disponível - usando fallback Python")
        
        converted_count = 0
        failed_count = 0
        skipped_count = 0
        
        # NOVO v10.3.0: Processar em blocos menores para evitar OOM
        batch_size = 10
        for i in range(0, len(md_files), batch_size):
            batch = md_files[i:i + batch_size]
            self.logger.info(f"📦 Processando lote {i//batch_size + 1}/{(len(md_files) + batch_size - 1)//batch_size}")
            
            for md_file in batch:
                try:
                    html_file = html_folder / md_file.with_suffix('.html').name
                    
                    # Verificar se precisa converter
                    if not self.force_overwrite and html_file.exists():
                        with open(md_file, 'r', encoding='utf-8') as f:
                            md_content = f.read()
                        
                        # Simular conversão para verificar hash
                        new_content = self._convert_with_pandoc_cached(str(md_file))
                        
                        if new_content and not self._should_write_file(html_file, new_content):
                            self.logger.info(f"⭐️ Já existe (hash igual): {html_file.name}")
                            skipped_count += 1
                            continue
                    else:
                        new_content = self._convert_with_pandoc_cached(str(md_file))
                    
                    if new_content:
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        self.logger.info(f"✅ Criado: {html_file.name}")
                        converted_count += 1
                    else:
                        self.logger.error(f"❌ Falha na conversão: {md_file.name}")
                        failed_count += 1
                
                except Exception as e:
                    self.logger.error(f"❌ Erro em {md_file.name}: {str(e)}")
                    if self.debug_mode:
                        self.logger.error(traceback.format_exc())
                    failed_count += 1
            
            # NOVO v10.3.0: Limpar cache de memória entre lotes
            if i + batch_size < len(md_files):
                self.conversion_cache.clear_memory_cache()
        
        self.logger.info(f"📊 HTML: {converted_count} criados, {skipped_count} saltados, {failed_count} falhas em '{html_folder}'")
    
    def categorize_conversation(self, title: str, summary: str) -> str:
        text = f"{title} {summary}".lower()
        patterns = {
            'Tecnologia': r'\b(tecnologia|hardware|software|rede|internet|wifi|bluetooth|[45]g|cloud|aws|azure|gcp|servidor|hosting|domínio|ssl|router|switch|firewall|iot|smartphone|tablet|navegador|browser|chrome|firefox|edge|safari|email|gmail|outlook|criptografia|segurança|cibersegurança|ransomware|phishing|autenticação|2fa|biometria)\b',
            'Saúde': r'\b(saúde|medicina|médico|enfermagem|doença|vírus|bactéria|vacina|covid|coronavírus|gripe|febre|dor|análise|exame|raio x|ressonância|hospital|clínica|farmácia|medicamento|remédio|psicologia|terapia|bem-estar|nutrição|dieta|exercício|fitness|sono|saúde mental)\b',
            'Programação': r'\b(python|javascript|java|c\+\+|c#|go|rust|lua|bash|script|debug|erro|conda|mamba|pandoc|msys2|spyder|jupyter|pip|venv|docker|git|github|vscode|ide|programa|código|função|classe|api|selenium|playwright)\b',
            'Sistemas': r'\b(windows|linux|macos|so|sistema operacional|driver|registry|process|firewall|bios|boot|path|dll|exe|powershell|cmd|terminal|shell)\b',
            'IA': r'\b(ia|gpt|chatgpt|grok|qwen|deepseek|llm|modelo|prompt|token|embedding|fine-tune|neural|chatbot|inteligência artificial)\b',
            'Dados': r'\b(dados|data|csv|json|pandas|numpy|excel|sql|banco|sqlite|postgres|visualização|gráfico|tabela|análise|etl|dashboard)\b',
            'Geral': r'\b(geral|pergunta|ajuda|como fazer|explicar|resumo|tutorial básico)\b'
        }
        
        for category, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return category
        
        return 'Outros'
    
    def parse_timestamp_for_sorting(self, timestamp) -> datetime:
        if not timestamp:
            return datetime.min
        try:
            if isinstance(timestamp, str):
                clean_ts = timestamp.replace('T', ' ').split('.')[0].split('+')[0]
                if clean_ts.endswith('Z'):
                    clean_ts = clean_ts[:-1]
                return datetime.fromisoformat(clean_ts)
            elif isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp)
        except:
            pass
        return datetime.min
    
    def format_timestamp(self, timestamp) -> Optional[str]:
        if not timestamp:
            return None
        try:
            if isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(timestamp, str):
                if 'T' in timestamp:
                    return timestamp.replace('T', ' ').split('.')[0]
                return timestamp
        except:
            pass
        return str(timestamp)
    
    def create_enhanced_markdown_content(self, conversation: Dict[str, Any]) -> str:
        conv_id = f"{conversation['source']}_{conversation['number']}"
        
        lines = [
            f"# {conversation['title']}",
            "",
            "## 📊 Informações",
            f"- **Número:** #{conversation['number']}",
            f"- **Origem:** {conversation['source']}",
            f"- **Categoria:** {conversation['category']}",
            f"- **ID:** {conversation.get('id', 'N/A')}",
            f"- **Criada em:** {conversation.get('inserted_at') or conversation.get('created_at') or 'N/A'}",
        ]
        
        if conversation.get('updated_at'):
            lines.append(f"- **Atualizada em:** {conversation['updated_at']}")
        
        lines.extend([
            f"- **Total de mensagens:** {len(conversation['messages'])}",
            f"- **Resumo:** {conversation.get('summary', 'Sem resumo')}",
            "",
            "---",
            "",
            "## 💬 Conversa",
            ""
        ])
        
        for j, msg in enumerate(conversation['messages'], 1):
            timestamp = f" *({msg['timestamp']})*" if msg['timestamp'] else ""
            model_info = f" *[{msg.get('model', '')}]*" if msg.get('model') else ""
            
            processed_content, saved_files = self.extract_and_save_attachments(
                msg['content'], conversation['number'], j
            )
            
            # NOVO v10.3.0: Usar preservador estrito
            preserved_content = self.preserve_special_content_enhanced(processed_content, f"{conv_id}_msg_{j}")
            
            lines.extend([
                f"### {msg['author']}{timestamp}{model_info}",
                "",
                f"{preserved_content}",
                ""
            ])
            
            if saved_files:
                lines.extend([
                    "#### 📎 Anexos",
                    ""
                ])
                for file_path in saved_files:
                    lines.append(f"- `{file_path}`")
                lines.append("")
            
            if j < len(conversation['messages']):
                lines.extend(["---", ""])
        
        lines.extend([
            "---",
            "",
            f"*Conversa exportada do {conversation['source']}*",
            f"*Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        ])
        
        return '\n'.join(lines)
    
    def process_claude(self, path: Path):
        self.backup_original_file(path, "claude")
        
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Claude: {path}")
            return
        
        try:
            self.logger.info("📄 Processando Claude...")
            all_data = self.claude_processor.load_claude_data(self.data_dir)
            
            if not all_data:
                self.logger.error("❌ Claude: nenhum dado carregado")
                return
            
            self.claude_processor.extract_conversations(all_data)
            claude_conversations = self.claude_processor.process_claude_conversations()
            
            for conv in claude_conversations:
                if not conv.get('inserted_at') and conv.get('created_at'):
                    conv['inserted_at'] = conv['created_at']
                
                if conv.get('inserted_at'):
                    conv['inserted_at'] = self.format_timestamp(conv['inserted_at'])
                if conv.get('updated_at'):
                    conv['updated_at'] = self.format_timestamp(conv['updated_at'])
                
                for msg in conv['messages']:
                    if msg.get('timestamp'):
                        msg['timestamp'] = self.format_timestamp(msg['timestamp'])
                
                self.all_conversations.append(conv)
            
            self.logger.info(f"✅ Claude: {len(claude_conversations)} conversas adicionadas")
        
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Claude: {e}")
            self.logger.error(traceback.format_exc())
    
    def process_qwen_corrected(self, path: Path):
        self.backup_original_file(path, "qwen")
        
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Qwen3: {path}")
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            conversations = []
            if 'data' in raw_data and isinstance(raw_data['data'], list):
                conversations = raw_data['data']
            elif isinstance(raw_data, list):
                conversations = raw_data
            else:
                for key, value in raw_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        if isinstance(value[0], dict) and any(k in value[0] for k in ['title', 'chat', 'messages']):
                            conversations = value
                            break
            
            if not conversations:
                self.logger.error("❌ Nenhuma conversa encontrada no arquivo Qwen")
                return
            
            self.logger.info(f"🔍 Qwen: encontradas {len(conversations)} conversas.")
            
            processed_count = 0
            for i, conv in enumerate(conversations):
                if not isinstance(conv, dict):
                    continue
                
                original_title = conv.get('title', f'Conversa Qwen {i+1}')
                clean_title = self.preserve_original_title(original_title)
                
                messages = self._extract_qwen_messages_corrected(conv, clean_title, i)
                
                if messages:
                    messages.sort(key=lambda x: self.parse_timestamp_for_sorting(x['timestamp']))
                    
                    self.all_conversations.append({
                        'title': clean_title,
                        'source': 'Qwen3',
                        'id': conv.get('id', f'qwen_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('created_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': self.categorize_conversation(clean_title, messages[0]['content'][:100] if messages else "")
                    })
                    processed_count += 1
            
            self.logger.info(f"✅ Qwen3: {processed_count} conversas processadas.")
        
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Qwen3: {e}")
            self.logger.error(traceback.format_exc())
    
    def _extract_qwen_messages_corrected(self, conv: Dict[str, Any], clean_title: str, conv_index: int) -> List[Dict[str, Any]]:
        all_messages = []
        
        def extract_from_object(obj, path=""):
            messages_found = []
            if isinstance(obj, dict):
                if self._is_qwen_message_with_content(obj):
                    message = self._create_message_from_qwen_object(obj, conv_index)
                    if message:
                        messages_found.append(message)
                
                for key, value in obj.items():
                    messages_found.extend(extract_from_object(value, f"{path}.{key}"))
            elif isinstance(obj, list):
                for item in obj:
                    messages_found.extend(extract_from_object(item, path))
            
            return messages_found
        
        all_messages = extract_from_object(conv, "root")
        unique_messages = self._remove_duplicate_messages(all_messages)
        
        return unique_messages
    
    def _is_qwen_message_with_content(self, obj: Dict) -> bool:
        has_basic_structure = ('role' in obj and 'content' in obj)
        has_content_list = 'content_list' in obj and isinstance(obj['content_list'], list)
        return (has_basic_structure and (obj.get('content') or has_content_list) and obj.get('role') in ['user', 'assistant'])
    
    def _create_message_from_qwen_object(self, obj: Dict, conv_index: int) -> Optional[Dict[str, Any]]:
        role = obj.get('role', '')
        content = obj.get('content', '')
        content_list = obj.get('content_list', [])
        
        if not role:
            return None
        
        final_content = ""
        saved_files = []
        
        if content_list and isinstance(content_list, list):
            qwen_content, qwen_files = self.process_qwen_attachments(content_list, conv_index, len(self.all_conversations))
            if qwen_content:
                final_content = qwen_content
                saved_files.extend(qwen_files)
        
        if not final_content and content:
            processed_content, content_files = self.extract_and_save_attachments(str(content), conv_index, len(self.all_conversations))
            final_content = processed_content
            saved_files.extend(content_files)
        
        if not final_content or final_content == 'null':
            return None
        
        if role == 'user':
            author = "👤 Utilizador"
        elif role == 'assistant':
            author = "🤖 Qwen3"
        else:
            author = f"🔹 {role.title()}"
        
        # NOVO v10.3.0: Usar preservador estrito
        final_content = self.preserve_special_content_enhanced(final_content, f"qwen_{conv_index}")
        
        return {
            'author': author,
            'role': role,
            'content': final_content,
            'timestamp': self.format_timestamp(obj.get('created_at')),
            'model': obj.get('model', 'Qwen3'),
            'attachments': saved_files
        }
    
    def _remove_duplicate_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        unique_messages = []
        
        for msg in messages:
            content_key = f"{msg['content'][:100]}_{msg['timestamp']}"
            if content_key not in seen:
                seen.add(content_key)
                unique_messages.append(msg)
        
        return unique_messages
    
    def process_chatgpt(self, path: Path):
        self.backup_original_file(path, "chatgpt")
        
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria ChatGPT: {path}")
            return
        
        try:
            with open(path, 'rb') as f:
                zip_bytes = io.BytesIO(f.read())
            
            with zipfile.ZipFile(zip_bytes, 'r') as z:
                convs_data = z.read("conversations.json")
                data = json.loads(convs_data)
            
            if not isinstance(data, list):
                self.logger.warning("⚠️  ChatGPT: estrutura inesperada.")
                return
            
            self.logger.info(f"🔍 ChatGPT: encontradas {len(data)} conversas.")
            
            processed_count = 0
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa ChatGPT {i+1}')
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for msg_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                    
                    author_role = msg_data.get('author', {}).get('role', '')
                    if author_role == 'user':
                        author = "👤 Utilizador"
                        role = 'user'
                    elif author_role == 'assistant':
                        author = "🤖 ChatGPT"
                        role = 'assistant'
                    else:
                        continue
                    
                    content_parts = []
                    for part in msg_data.get('content', {}).get('parts', []):
                        if isinstance(part, str):
                            content_parts.append(part)
                    
                    content = "\n".join(content_parts).strip()
                    processed_content, saved_files = self.extract_and_save_attachments(content, i, len(messages))
                    
                    # NOVO v10.3.0: Usar preservador estrito
                    content = self.preserve_special_content_enhanced(processed_content, f"chatgpt_{i}")
                    
                    if not content:
                        continue
                    
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('create_time')),
                        'model': msg_data.get('model', 'ChatGPT'),
                        'attachments': saved_files
                    })
                
                if messages:
                    self.all_conversations.append({
                        'title': clean_title,
                        'source': 'ChatGPT',
                        'id': conv.get('id', f'chatgpt_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('create_time')),
                        'updated_at': self.format_timestamp(conv.get('update_time')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
            
            self.logger.info(f"✅ ChatGPT: {processed_count} conversas processadas.")
        
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar ChatGPT: {e}")
            if self.debug_mode:
                traceback.print_exc()
    
    def process_deepseek(self, path: Path):
        self.backup_original_file(path, "deepseek")
        
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria DeepSeek: {path}")
            return
        
        try:
            with open(path, 'rb') as f:
                zip_bytes = io.BytesIO(f.read())
            
            with zipfile.ZipFile(zip_bytes, 'r') as z:
                convs_data = z.read("conversations.json")
                raw_data = json.loads(convs_data)
            
            if isinstance(raw_data, list):
                data = raw_data
            elif isinstance(raw_data, dict) and 'data' in raw_data:
                data = raw_data['data']
            else:
                self.logger.warning("⚠️  DeepSeek: estrutura inesperada.")
                return
            
            if not isinstance(data, list):
                self.logger.warning("⚠️  DeepSeek: 'data' não é uma lista.")
                return
            
            self.logger.info(f"🔍 DeepSeek: encontradas {len(data)} conversas.")
            
            processed_count = 0
            for i, conv in enumerate(data):
                original_title = conv.get('title', f'Conversa DeepSeek {i+1}')
                clean_title = self.preserve_original_title(original_title)
                
                messages = []
                mapping = conv.get('mapping', {})
                
                for node_id, node in mapping.items():
                    msg_data = node.get('message')
                    if not msg_data or not isinstance(msg_data, dict):
                        continue
                    
                    fragments = msg_data.get('fragments', [])
                    content_parts = []
                    msg_type = None
                    
                    for frag in fragments:
                        if isinstance(frag, dict):
                            frag_type = frag.get('type', '').upper()
                            if frag_type in ('REQUEST', 'RESPONSE'):
                                msg_type = frag_type
                            
                            text = frag.get('text', '')
                            if text:
                                content_parts.append(text)
                            
                            content = frag.get('content', '')
                            if content:
                                if isinstance(content, list):
                                    for item in content:
                                        if isinstance(item, str):
                                            content_parts.append(item)
                                        elif isinstance(item, dict):
                                            item_text = item.get('text', '')
                                            if item_text:
                                                content_parts.append(str(item_text))
                                else:
                                    content_parts.append(str(content))
                    
                    content = ' '.join(content_parts).strip()
                    processed_content, saved_files = self.extract_and_save_attachments(content, i, len(messages))
                    
                    # NOVO v10.3.0: Usar preservador estrito
                    content = self.preserve_special_content_enhanced(processed_content, f"deepseek_{i}")
                    
                    if not content:
                        continue
                    
                    if msg_type == 'REQUEST':
                        author = "👤 Utilizador"
                        role = 'user'
                    else:
                        author = "🤖 DeepSeek"
                        role = 'assistant'
                    
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(msg_data.get('inserted_at')),
                        'model': msg_data.get('model', 'DeepSeek'),
                        'attachments': saved_files
                    })
                
                if messages:
                    self.all_conversations.append({
                        'title': clean_title,
                        'source': 'DeepSeek',
                        'id': conv.get('id', f'deepseek_{i+1}'),
                        'inserted_at': self.format_timestamp(conv.get('inserted_at')),
                        'updated_at': self.format_timestamp(conv.get('updated_at')),
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    processed_count += 1
            
            self.logger.info(f"✅ DeepSeek: {processed_count} conversas processadas.")
        
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar DeepSeek: {e}")
            if self.debug_mode:
                traceback.print_exc()
    
    def process_grok(self, path: Path):
        self.backup_original_file(path, "grok")
        
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Processaria Grok: {path}")
            return
        
        try:
            with open(path, 'rb') as f:
                zip_bytes = io.BytesIO(f.read())
            
            with zipfile.ZipFile(zip_bytes, 'r') as z:
                target_file_name = None
                for name in z.namelist():
                    if name.endswith("prod-grok-backend.json"):
                        target_file_name = name
                        break
                
                if not target_file_name:
                    self.logger.error("❌ Grok: ficheiro 'prod-grok-backend.json' não encontrado no ZIP.")
                    return
                
                self.logger.info(f"🔍 Grok: carregando {target_file_name}...")
                data = json.loads(z.read(target_file_name))
            
            if not isinstance(data, dict) or 'conversations' not in data:
                self.logger.error("❌ Grok: estrutura inesperada – chave 'conversations' não encontrada.")
                return
            
            conversations_list = data['conversations']
            if not isinstance(conversations_list, list):
                self.logger.error("❌ Grok: 'conversations' não é uma lista.")
                return
            
            self.logger.info(f"📊 Grok: encontradas {len(conversations_list)} conversas.")
            
            total_convs = 0
            for item in conversations_list:
                if not isinstance(item, dict):
                    continue
                
                conv_meta = item.get('conversation')
                responses = item.get('responses', [])
                
                if not isinstance(conv_meta, dict) or not isinstance(responses, list) or not responses:
                    continue
                
                conv_id = conv_meta.get('id')
                if not conv_id:
                    continue
                
                original_title = conv_meta.get('title', f"Conversa Grok {total_convs + 1}")
                clean_title = self.preserve_original_title(original_title)
                
                create_time_str = conv_meta.get('create_time')
                modify_time_str = conv_meta.get('modify_time')
                
                def format_iso_timestamp(ts_str):
                    if not ts_str:
                        return None
                    try:
                        if '.' in ts_str:
                            ts_str = ts_str.split('.')[0] + 'Z'
                        return self.format_timestamp(ts_str)
                    except:
                        return str(ts_str)
                
                inserted_at = format_iso_timestamp(create_time_str)
                updated_at = format_iso_timestamp(modify_time_str)
                
                messages = []
                for resp in responses:
                    if not isinstance(resp, dict):
                        continue
                    
                    resp_data = resp.get('response')
                    if not isinstance(resp_data, dict):
                        continue
                    
                    sender = resp_data.get('sender', '').upper()
                    if sender == 'HUMAN':
                        author = "👤 Utilizador"
                        role = "user"
                    elif sender == 'ASSISTANT':
                        author = "🤖 Grok"
                        role = "assistant"
                    else:
                        continue
                    
                    content = str(resp_data.get('message', '')).strip()
                    processed_content, saved_files = self.extract_and_save_attachments(content, total_convs, len(messages))
                    
                    # NOVO v10.3.0: Usar preservador estrito
                    content = self.preserve_special_content_enhanced(processed_content, f"grok_{total_convs}")
                    
                    if not content:
                        continue
                    
                    create_time = resp_data.get('create_time')
                    timestamp_ms = None
                    if isinstance(create_time, dict) and '$date' in create_time:
                        date_obj = create_time['$date']
                        if isinstance(date_obj, dict) and '$numberLong' in date_obj:
                            try:
                                timestamp_ms = int(date_obj['$numberLong'])
                            except:
                                pass
                    
                    messages.append({
                        'author': author,
                        'role': role,
                        'content': content,
                        'timestamp': self.format_timestamp(timestamp_ms / 1000.0 if timestamp_ms else None),
                        'model': 'Grok',
                        'attachments': saved_files
                    })
                
                if messages:
                    self.all_conversations.append({
                        'title': clean_title,
                        'source': 'Grok',
                        'id': conv_id,
                        'inserted_at': inserted_at,
                        'updated_at': updated_at,
                        'messages': messages,
                        'summary': messages[0]['content'][:100] + "..." if messages else "Sem conteúdo",
                        'category': 'Geral'
                    })
                    total_convs += 1
            
            if total_convs > 0:
                self.logger.info(f"✅ Grok: processadas {total_convs} conversas.")
            else:
                self.logger.error("❌ Grok: nenhuma conversa válida encontrada.")
        
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar Grok: {e}")
            if self.debug_mode:
                traceback.print_exc()
    
    def save_as_markdown_enhanced(self):
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Markdowns seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename_optimized(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                self.logger.info(f"   📄 {filename}")
            return
        
        folder = Path(self.output_dirs['markdown'])
        saved_count = 0
        failed_count = 0
        skipped_count = 0
        
        for conv in self.all_conversations:
            try:
                safe_title = self.sanitize_filename_optimized(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.md"
                filepath = folder / filename
                
                markdown_content = self.create_enhanced_markdown_content(conv)
                
                if not self.force_overwrite and not self._should_write_file(filepath, markdown_content):
                    skipped_count += 1
                    continue
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                saved_count += 1
            
            except Exception as e:
                self.logger.error(f"❌ Erro ao salvar conversa {conv['number']}: {e}")
                failed_count += 1
                continue
        
        self.logger.info(f"✅ Markdown: {saved_count} criados, {skipped_count} saltados, {failed_count} falhas em '{folder}'")
    
    def save_as_csv(self):
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] CSVs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename_optimized(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
                self.logger.info(f"   📊 {filename}")
            return
        
        folder = Path(self.output_dirs['csv'])
        saved_count = 0
        skipped_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename_optimized(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.csv"
            filepath = folder / filename
            
            csv_content = self._get_csv_content(conv)
            
            if not self.force_overwrite and not self._should_write_file(filepath, csv_content):
                skipped_count += 1
                continue
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_content)
            saved_count += 1
        
        self.logger.info(f"✅ CSV: {saved_count} criados, {skipped_count} saltados em '{folder}'")
    
    def _get_csv_content(self, conv):
        lines = ["node_id,author,role,timestamp,model,content,attachments"]
        for i, msg in enumerate(conv['messages']):
            content = msg['content'].replace('"', '""')
            attachments = ', '.join(msg.get('attachments', []))
            line = f'"{i}","{msg["author"]}","{msg["role"]}","{msg["timestamp"]}","{msg["model"]}","{content}","{attachments}"'
            lines.append(line)
        return "\n".join(lines)
    
    def save_as_json(self):
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] JSONs seriam criados:")
            for conv in self.all_conversations:
                safe_title = self.sanitize_filename_optimized(conv['title'])
                filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
                self.logger.info(f"   📋 {filename}")
            return
        
        folder = Path(self.output_dirs['json'])
        saved_count = 0
        skipped_count = 0
        
        for conv in self.all_conversations:
            safe_title = self.sanitize_filename_optimized(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}.json"
            filepath = folder / filename
            
            json_content = json.dumps(conv, ensure_ascii=False, indent=2)
            
            if not self.force_overwrite and not self._should_write_file(filepath, json_content):
                skipped_count += 1
                continue
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_content)
            saved_count += 1
        
        self.logger.info(f"✅ JSON: {saved_count} criados, {skipped_count} saltados em '{folder}'")
    
    def save_all_to_single_files(self):
        if self.dry_run:
            self.logger.info("🔮 [DRY-RUN] Arquivos únicos seriam criados:")
            self.logger.info(f"   📄 {self.single_files['csv']}")
            self.logger.info(f"   📄 {self.single_files['json']}")
            return
        
        # CSV único
        csv_content = self._get_single_csv_content()
        if not self.force_overwrite and not self._should_write_file(Path(self.single_files['csv']), csv_content):
            self.logger.info(f"⭐️ CSV único já existe (hash igual): {self.single_files['csv']}")
        else:
            with open(self.single_files['csv'], 'w', encoding='utf-8', newline='') as f:
                f.write(csv_content)
            self.logger.info(f"✅ CSV único: {self.single_files['csv']}")
        
        # JSON único
        json_content = json.dumps(self.all_conversations, ensure_ascii=False, indent=2)
        if not self.force_overwrite and not self._should_write_file(Path(self.single_files['json']), json_content):
            self.logger.info(f"⭐️ JSON único já existe (hash igual): {self.single_files['json']}")
        else:
            with open(self.single_files['json'], 'w', encoding='utf-8') as f:
                f.write(json_content)
            self.logger.info(f"✅ JSON único: {self.single_files['json']}")
    
    def _get_single_csv_content(self):
        lines = ["conversation_number,source,conversation_title,category,author,role,timestamp,model,content,attachments"]
        for conv in self.all_conversations:
            for msg in conv['messages']:
                content = msg['content'].replace('"', '""')
                attachments = ', '.join(msg.get('attachments', []))
                line = f'"{conv["number"]}","{conv["source"]}","{conv["title"]}","{conv["category"]}","{msg["author"]}","{msg["role"]}","{msg["timestamp"]}","{msg["model"]}","{content}","{attachments}"'
                lines.append(line)
        return "\n".join(lines)
    
    def create_searchable_index_enhanced(self):
        """NOVO v10.3.0: Criação otimizada do índice com sistema de autenticação"""
        if self.dry_run:
            self.logger.info(f"🔮 [DRY-RUN] Índice HTML seria criado: {self.index_file}")
            return
        
        self.logger.info("🎯 Criando índice HTML combinado com sistema de autenticação...")
        
        index_start = time.perf_counter()
        
        # Estatísticas
        category_stats = {}
        source_stats = {}
        recent_stats = {'week': 0, 'month': 0}
        one_week_ago = datetime.now().timestamp() - (7 * 24 * 60 * 60)
        one_month_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        
        for conv in self.all_conversations:
            cat = conv['category']
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            source = conv['source']
            source_stats[source] = source_stats.get(source, 0) + 1
            
            try:
                conv_time = self.parse_timestamp_for_sorting(
                    conv.get('updated_at') or conv.get('inserted_at')
                ).timestamp()
            except (OSError, ValueError):
                conv_time = datetime.now().timestamp()
            
            if conv_time > one_week_ago:
                recent_stats['week'] += 1
            if conv_time > one_month_ago:
                recent_stats['month'] += 1
        
        # Mapeamento de ícones por fonte
        SOURCE_ICONS = {
            'Qwen3': '🟦',
            'ChatGPT': '🟦',
            'DeepSeek': '🟨',
            'Grok': '🟨',
            'Claude': '🟪',
            'Desconhecido': '⚪'
        }
        
        # NOVO v10.3.0: Estatísticas de cache e preservação
        cache_stats = self.conversion_cache.get_stats()
        preservation_report = self.content_preserver.get_transformation_report()
        
        # Gerar HTML do índice COM SISTEMA DE AUTENTICAÇÃO
        html_content = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice Combinado v{SCRIPT_VERSION} - AI Chats</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; transition: background 0.3s ease; }}
        body.dark-mode {{ background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: #e0e0e0; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; transition: background 0.3s ease; }}
        body.dark-mode .container {{ background: #1e1e1e; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; transition: background 0.3s ease; }}
        body.dark-mode .header {{ background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: #e0e0e0; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 15px; font-weight: 300; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; margin-bottom: 20px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px); text-align: center; transition: background 0.3s ease; }}
        body.dark-mode .stat-card {{ background: rgba(30, 30, 30, 0.8); }}
        .stat-number {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
        .search-section {{ padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; transition: background 0.3s ease; }}
        body.dark-mode .search-section {{ background: #2c2c2c; border-bottom-color: #444; }}
        .search-box {{ width: 100%; padding: 18px 25px; font-size: 16px; border: 2px solid #e9ecef; border-radius: 25px; outline: none; transition: all 0.3s ease; font-family: inherit; }}
        body.dark-mode .search-box {{ background: #3c3c3c; color: #e0e0e0; border-color: #555; }}
        .search-box:focus {{ border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }}
        body.dark-mode .search-box:focus {{ border-color: #3498db; box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1); }}
        
        .filter-section {{ padding: 15px 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; transition: background 0.3s ease; }}
        body.dark-mode .filter-section {{ background: #2c2c2c; border-bottom-color: #444; }}
        .filter-row {{ display: flex; align-items: center; margin-bottom: 10px; }}
        .filter-label {{ font-weight: bold; margin-right: 15px; white-space: nowrap; font-size: 0.9em; color: #495057; min-width: 150px; }}
        body.dark-mode .filter-label {{ color: #aaa; }}
        .filter-buttons {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .filter-btn {{ padding: 8px 16px; background: white; border: 2px solid #e9ecef; border-radius: 20px; cursor: pointer; font-size: 0.9em; font-weight: 500; transition: all 0.3s ease; font-family: inherit; white-space: nowrap; }}
        body.dark-mode .filter-btn {{ background: #3c3c3c; color: #e0e0e0; border-color: #555; }}
        .filter-btn.active, .filter-btn:hover {{ background: #667eea; color: white; border-color: #667eea; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3); }}
        body.dark-mode .filter-btn.active, body.dark-mode .filter-btn:hover {{ background: #3498db; border-color: #3498db; box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3); }}
        
        .conversations-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 25px; padding: 35px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 400px; transition: background 0.3s ease; }}
        body.dark-mode .conversations-grid {{ background: linear-gradient(135deg, #2c3e50 0%, #4a6491 100%); }}
        .conversation-card {{ background: white; border: 1px solid #e9ecef; border-radius: 15px; padding: 25px; transition: all 0.4s ease; cursor: pointer; position: relative; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }}
        body.dark-mode .conversation-card {{ background: #1e1e1e; border-color: #444; color: #e0e0e0; }}
        .conversation-card:hover {{ transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.15); border-color: #667eea; }}
        body.dark-mode .conversation-card:hover {{ border-color: #3498db; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }}
        .card-number {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 16px; border-radius: 20px; font-size: 0.9em; font-weight: bold; box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3); }}
        body.dark-mode .card-number {{ background: linear-gradient(135deg, #3498db, #2980b9); }}
        .card-source {{ background: #e3f2fd; color: #1976d2; padding: 5px 12px; border-radius: 12px; font-size: 0.85em; font-weight: bold; margin-left: 10px; }}
        body.dark-mode .card-source {{ background: #1a237e; color: #bbdefb; }}
        .card-title {{ font-size: 1.3em; font-weight: 600; color: #2c3e50; margin-bottom: 12px; line-height: 1.4; min-height: 3.6em; cursor: pointer; }}
        body.dark-mode .card-title {{ color: #e0e0e0; }}
        .card-summary {{ color: #6c757d; font-size: 0.95em; line-height: 1.5; margin-bottom: 18px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; cursor: pointer; }}
        body.dark-mode .card-summary {{ color: #aaa; }}
        .card-meta {{ display: flex; justify-content: space-between; font-size: 0.85em; color: #868e96; border-top: 1px solid #e9ecef; padding-top: 18px; transition: border-color 0.3s ease; }}
        body.dark-mode .card-meta {{ color: #777; border-top-color: #444; }}
        .card-actions {{ position: absolute; top: 20px; right: 20px; display: flex; gap: 8px; opacity: 0; transition: opacity 0.3s ease; }}
        .conversation-card:hover .card-actions {{ opacity: 1; }}
        .action-btn-small {{ background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 6px 12px; font-size: 0.8em; cursor: pointer; transition: all 0.3s ease; font-weight: 500; text-decoration: none; color: #333; display: inline-block; }}
        body.dark-mode .action-btn-small {{ background: #3c3c3c; color: #e0e0e0; border-color: #555; }}
        .action-btn-small:hover {{ background: #667eea; color: white; border-color: #667eea; transform: scale(1.05); }}
        body.dark-mode .action-btn-small:hover {{ background: #3498db; border-color: #3498db; }}
        .no-results {{ text-align: center; padding: 60px 20px; color: #6c757d; font-size: 1.1em; grid-column: 1 / -1; }}
        body.dark-mode .no-results {{ color: #aaa; }}
        .category-badge {{ display: inline-block; background: #e3f2fd; color: #1976d2; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; margin-left: 8px; font-weight: 500; }}
        body.dark-mode .category-badge {{ background: #1a237e; color: #bbdefb; }}
        .back-to-top-index {{ position: fixed; bottom: 30px; right: 30px; background: #007bff; color: white; border: none; border-radius: 50%; width: 50px; height: 50px; font-size: 18px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.15); opacity: 0; transition: all 0.3s ease; z-index: 999; display: flex; align-items: center; justify-content: center; }}
        .back-to-top-index.show {{ opacity: 1; transform: translateY(0); }}
        .back-to-top-index:hover {{ background: #0056b3; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.2); }}
        
        .theme-toggle-btn {{ position: absolute; top: 20px; right: 20px; background: #f0f0f0; border: none; border-radius: 50%; width: 40px; height: 40px; font-size: 1.2em; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.1); z-index: 1000; }}
        body.dark-mode .theme-toggle-btn {{ background: #333; color: #fff; }}
        
        .dashboard-btn {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: #f0f0f0;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 1em;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            z-index: 1000;
            transition: all 0.3s ease;
            text-decoration: none;
            color: #333;
            font-family: inherit;
        }}
        body.dark-mode .dashboard-btn {{
            background: #333;
            color: #fff;
        }}
        .dashboard-btn:hover {{
            background: #e0e0e0;
        }}
        body.dark-mode .dashboard-btn:hover {{
            background: #555;
        }}

        /* NOVO: Estilo para mensagem de carregamento/auth */
        .auth-loading {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-size: 1.2em;
            color: #333;
        }}
        body.dark-mode .auth-loading {{
            background: rgba(30,30,30,0.95);
            color: #e0e0e0;
        }}
        .auth-spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <!-- Tela de carregamento/autenticação -->
    <div id="authLoading" class="auth-loading">
        <div class="auth-spinner"></div>
        <p>Verificando autenticação...</p>
    </div>

    <div class="container" id="mainContainer" style="display: none;">
        <div class="header">
            <!-- BOTÃO VOLTAR AO DASHBOARD CORRIGIDO -->
            <a href="../app/dashboard.html" class="dashboard-btn">Voltar ao Dashboard</a>
            <button id="theme-toggle" class="theme-toggle-btn">🌙</button>
            <h1>📚 Índice Combinado v{SCRIPT_VERSION}</h1>
            <p>Qwen3 • ChatGPT • DeepSeek • Grok • Claude • PRESERVAÇÃO ESTRITA</p>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(self.all_conversations)}</div>
                    <div>Total de Conversas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(source_stats)}</div>
                    <div>Fontes Diferentes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{cache_stats['hit_rate']:.0%}</div>
                    <div>Cache Hit Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{preservation_report['integrity_rate']:.0%}</div>
                    <div>Integridade</div>
                </div>
            </div>
        </div>
        <div class="search-section">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar por título, conteúdo, categoria ou fonte...">
        </div>
        
        <div class="filter-section">
            <div class="filter-row">
                <div class="filter-label">📱 Filtrar por Fonte:</div>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter-type="source" data-filter-value="todas">Todas ({len(self.all_conversations)})</button>
                    {"".join([f'<button class="filter-btn" data-filter-type="source" data-filter-value="{source}">{SOURCE_ICONS.get(source, "⚪")} {source} ({count})</button>' for source, count in source_stats.items()])}
                </div>
            </div>
        </div>
        
        <div class="filter-section">
            <div class="filter-row">
                <div class="filter-label">🏷️ Filtrar por Categoria:</div>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter-type="category" data-filter-value="todas">Todas ({len(self.all_conversations)})</button>
                    {"".join([f'<button class="filter-btn" data-filter-type="category" data-filter-value="{category}">📂 {category} ({count})</button>' for category, count in category_stats.items()])}
                </div>
            </div>
        </div>
        
        <div class="conversations-grid" id="conversationsGrid">
"""
        
        # Adicionar cards de conversas
        for i, conv in enumerate(self.all_conversations):
            safe_title = self.sanitize_filename(conv['title'])
            filename = f"{conv['number']:03d}_{conv['source']}_{safe_title}"
            has_attachments = any(msg.get('attachments') for msg in conv['messages'])
            attachments_badge = "<span style='background:#ffc107;color:#212529;padding:2px 6px;border-radius:8px;font-size:0.7em;margin-left:5px;'>📎</span>" if has_attachments else ""
            
            summary = conv.get('summary', 'Sem resumo disponível')
            if len(summary) > 150:
                summary = summary[:150] + "..."
            
            html_content += f"""
            <div class="conversation-card" data-title="{conv['title']}" data-summary="{summary}" data-source="{conv['source'].lower()}" data-category="{conv['category'].lower()}">
                <div class="card-header">
                    <div>
                        <div class="card-number">#{conv['number']} {SOURCE_ICONS.get(conv['source'], '⚪')} {attachments_badge}</div>
                        <div class="card-source">{conv['source']}</div>
                    </div>
                    <div class="card-actions">
                        <a href="combined_markdown/{filename}.md" class="action-btn-small" target="_blank" onclick="event.stopPropagation();">📄 MD</a>
                        <a href="combined_html/{filename}.html" class="action-btn-small html-btn" target="_blank" onclick="event.stopPropagation();">🌐 HTML</a>
                    </div>
                </div>
                <div class="card-title" onclick="openHTML('{filename}.html')">{conv['title']}</div>
                <div>
                    <span class="category-badge">{conv['category']}</span>
                </div>
                <div class="card-summary" onclick="openHTML('{filename}.html')">{summary}</div>
                <div class="card-meta">
                    <span>📅 {conv.get('updated_at') or conv.get('inserted_at') or 'N/A'}</span>
                    <span>💬 {len(conv['messages'])} mensagens</span>
                </div>
            </div>
            """
        
        html_content += f"""
        </div>
        <div style="text-align: center; padding: 20px; color: #666; font-size: 0.9em;">
            ⏱️ Gerado em {time.perf_counter() - index_start:.2f}s | {len(self.all_conversations)} conversas | 
            Cache: {cache_stats['hit_rate']:.0%} hits | Integridade: {preservation_report['integrity_rate']:.0%}
        </div>
    </div>
    <button class="back-to-top-index" id="backToTopIndex" title="Voltar ao Topo">↑</button>

    <!-- SISTEMA DE AUTENTICAÇÃO INTEGRADO -->
    <script>
        const WORKER_URL = 'https://worker-ds.mpmendespt.workers.dev';
        const APP_CONFIG = {{
            PATHS: {{
                LOGIN: '../app/login.html',
                DASHBOARD: '../app/dashboard.html'
            }},
            WORKER_URL: WORKER_URL
        }};

        // ✅ PROTEÇÃO: Verificar autenticação ao carregar a página
        document.addEventListener('DOMContentLoaded', function() {{
            const token = localStorage.getItem('jwt');
            
            if (!token) {{
                // Não está logado - redirecionar para login
                console.log('Nenhum token encontrado - redirecionando para login');
                window.location.href = APP_CONFIG.PATHS.LOGIN;
                return;
            }}
            
            // Está logado - carregar dados do usuário
            loadUserData(token);
        }});

        // Carregar dados do usuário
        async function loadUserData(token) {{
            try {{
                // Tentar obter do localStorage primeiro
                const storedUser = localStorage.getItem('user');
                
                if (storedUser) {{
                    const user = JSON.parse(storedUser);
                    // Atualizar interface se houver elemento userWelcome
                    const userWelcome = document.getElementById('userWelcome');
                    if (userWelcome) {{
                        userWelcome.textContent = `Olá, ${{user.username}}!`;
                    }}
                }}
                
                // Verificar se o token ainda é válido
                const response = await fetch(`${{WORKER_URL}}/api/protected`, {{
                    method: 'GET',
                    headers: {{
                        'Authorization': `Bearer ${{token}}`,
                        'Content-Type': 'application/json'
                    }}
                }});
                
                if (!response.ok) {{
                    // Token inválido ou expirado
                    console.log('Token inválido ou expirado');
                    logout();
                    return;
                }}
                
                // Token válido - atualizar dados se necessário
                const data = await response.json();
                console.log('Acesso autorizado:', data);
                
                // Mostrar conteúdo principal
                document.getElementById('authLoading').style.display = 'none';
                document.getElementById('mainContainer').style.display = 'block';
                
            }} catch (error) {{
                console.error('Erro ao verificar autenticação:', error);
                
                // Se houver erro mas tem dados locais, continua funcionando
                const storedUser = localStorage.getItem('user');
                if (!storedUser) {{
                    // Sem dados locais e sem conexão - fazer logout
                    logout();
                }} else {{
                    // Tem dados locais - mostrar conteúdo mesmo sem verificação
                    document.getElementById('authLoading').style.display = 'none';
                    document.getElementById('mainContainer').style.display = 'block';
                }}
            }}
        }}

        // ✅ FUNÇÃO DE LOGOUT
        function logout() {{
            // Limpar dados de autenticação
            localStorage.removeItem('jwt');
            localStorage.removeItem('user');
            
            console.log('Logout realizado - redirecionando para login');
            
            // Redirecionar para página de login
            window.location.href = APP_CONFIG.PATHS.LOGIN;
        }}

        // ✅ PROTEÇÃO: Verificar autenticação periodicamente (a cada 5 minutos)
        setInterval(function() {{
            const token = localStorage.getItem('jwt');
            if (!token) {{
                console.log('Token não encontrado - fazendo logout');
                logout();
            }}
        }}, 5 * 60 * 1000); // 5 minutos

        // Código existente para filtros, tema, etc.
        let currentFilters = {{ source: 'todas', category: 'todas' }};
        
        document.querySelectorAll('[data-filter-type]').forEach(btn => {{
            btn.addEventListener('click', () => {{
                const filterType = btn.getAttribute('data-filter-type');
                const filterValue = btn.getAttribute('data-filter-value');
                
                document.querySelectorAll(`[data-filter-type="${{filterType}}"]`).forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                currentFilters[filterType] = filterValue;
                filterConversations();
            }});
        }});
        
        document.getElementById('searchInput').addEventListener('input', filterConversations);
        
        const toggleBtn = document.getElementById('theme-toggle');
        let isDark = localStorage.getItem('dark-mode') === 'true';
        document.body.classList.toggle('dark-mode', isDark);
        toggleBtn.textContent = isDark ? '☀️' : '🌙';
        toggleBtn.addEventListener('click', () => {{
            isDark = !isDark;
            document.body.classList.toggle('dark-mode', isDark);
            localStorage.setItem('dark-mode', isDark);
            toggleBtn.textContent = isDark ? '☀️' : '🌙';
        }});
        
        function filterConversations() {{
            const term = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.conversation-card');
            let visible = 0;
            
            cards.forEach(card => {{
                const title = card.getAttribute('data-title').toLowerCase();
                const summary = card.getAttribute('data-summary').toLowerCase();
                const source = card.getAttribute('data-source').toLowerCase();
                const category = card.getAttribute('data-category').toLowerCase();
                
                const matchesSearch = (title.includes(term) || summary.includes(term) || category.includes(term) || source.includes(term));
                const matchesSource = (currentFilters.source === 'todas' || source === currentFilters.source.toLowerCase());
                const matchesCategory = (currentFilters.category === 'todas' || category === currentFilters.category.toLowerCase());
                
                if (matchesSearch && matchesSource && matchesCategory) {{
                    card.style.display = 'block';
                    visible++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            const grid = document.getElementById('conversationsGrid');
            const noResults = document.getElementById('no-results-message');
            if (visible === 0) {{
                if (!noResults) {{
                    const noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results-message';
                    noResultsMsg.className = 'no-results';
                    noResultsMsg.innerHTML = '🔍 Nenhuma conversa encontrada. Tente ajustar os filtros ou a pesquisa.';
                    grid.appendChild(noResultsMsg);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }}
        
        function openHTML(filename) {{
            const htmlUrl = 'combined_html/' + filename;
            window.open(htmlUrl, '_blank');
        }}
        
        const backToTopBtn = document.getElementById('backToTopIndex');
        window.addEventListener('scroll', () => {{
            if (window.pageYOffset > 300) {{
                backToTopBtn.classList.add('show');
            }} else {{
                backToTopBtn.classList.remove('show');
            }}
        }});
        
        backToTopBtn.addEventListener('click', () => {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});
        
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                document.getElementById('searchInput').value = '';
                filterConversations();
            }}
        }});
        
        document.querySelectorAll('.conversation-card').forEach(card => {{
            card.addEventListener('click', function(e) {{
                if (e.target.closest('.action-btn-small')) {{
                    return;
                }}
                const htmlBtn = this.querySelector('a.html-btn');
                if (htmlBtn) {{
                    const htmlUrl = htmlBtn.getAttribute('href');
                    window.open(htmlUrl, '_blank');
                }}
            }});
        }});
        
        document.getElementById('searchInput').focus();
    </script>
</body>
</html>
"""
        
        # Verificação de hash antes de escrever
        if not self.force_overwrite and not self._should_write_file(Path(self.index_file), html_content):
            self.logger.info(f"⭐️ Índice já existe (hash igual): {self.index_file}")
        else:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.info(f"✅ Índice combinado v{SCRIPT_VERSION} criado: {self.index_file}")
        
        index_time = time.perf_counter() - index_start
        self.logger.info(f"⏱️  Índice gerado em {index_time:.2f}s")

def main():
    parser = argparse.ArgumentParser(
        description=f"Sistema Combinado v{SCRIPT_VERSION} - Processamento otimizado com preservação estrita"
    )
    parser.add_argument("--dry-run", action="store_true", help="Executa sem salvar arquivos")
    parser.add_argument("--force-overwrite", action="store_true", default=DEFAULT_FORCE_OVERWRITE,
                       help=f"Sobrescreve arquivos existentes (padrão: {DEFAULT_FORCE_OVERWRITE})")
    parser.add_argument("--clear-cache", action="store_true", help="Limpa o cache de conversões")
    parser.add_argument("--process-attachments", action="store_true", help="Processa anexos (imagens, arquivos)")
    parser.add_argument("--no-batch", action="store_true", help="Desativa processamento em lote")
    parser.add_argument("--debug", action="store_true", help="Ativa modo debug com logs detalhados")
    parser.add_argument("--checksum", action="store_true", help="Gera checksum SHA-256 dos arquivos originais")
    parser.add_argument("--backup-original", action="store_true", help="Cria backup dos arquivos originais")
    
    # Configurações de preservação e cache com valores padrão do cabeçalho
    parser.add_argument("--allow-transforms", action="store_true", default=DEFAULT_ALLOW_TRANSFORMS,
                       help=f"ATIVA transformações de conteúdo (padrão: {DEFAULT_ALLOW_TRANSFORMS})")
    parser.add_argument("--no-strict-preserve", action="store_true", default=not DEFAULT_STRICT_PRESERVE,
                       help=f"DESATIVA modo estrito (padrão: {not DEFAULT_STRICT_PRESERVE})")
    
    parser.add_argument("--cache-memory-mb", type=int, default=DEFAULT_CACHE_MEMORY_MB,
                       help=f"Limite de memória do cache em MB (padrão: {DEFAULT_CACHE_MEMORY_MB})")
    parser.add_argument("--cache-disk-gb", type=int, default=DEFAULT_CACHE_DISK_GB,
                       help=f"Limite de disco do cache em GB (padrão: {DEFAULT_CACHE_DISK_GB})")
    
    args = parser.parse_args()
    
    # Determinar modo de preservação (compatibilidade com configurações do cabeçalho)
    strict_preserve = not args.no_strict_preserve
    allow_transforms = args.allow_transforms
    
    print(f"\n⚙️  CONFIGURAÇÕES CARREGADAS:")
    print(f"   • Allow transforms: {allow_transforms}")
    print(f"   • Force overwrite: {args.force_overwrite}")
    print(f"   • Cache memory: {args.cache_memory_mb}MB")
    print(f"   • Cache disk: {args.cache_disk_gb}GB")
    print(f"   • Strict preserve: {strict_preserve}")
    
    if strict_preserve and not allow_transforms:
        print("\n⚠️  MODO ESTRITO ATIVADO: Conteúdo preservado SEM transformações")
    elif allow_transforms:
        print("\n⚠️  Transformações de conteúdo ATIVADAS")
    
    system = CombinedFragmentsSystem(
        dry_run=args.dry_run,
        force_overwrite=args.force_overwrite,
        clear_cache=args.clear_cache,
        process_attachments=args.process_attachments,
        batch_processing=not args.no_batch,
        debug_mode=args.debug,
        backup_original=args.backup_original,
        checksum=args.checksum,
        strict_preserve=strict_preserve,
        allow_transforms=allow_transforms,
        cache_memory_mb=args.cache_memory_mb,
        cache_disk_gb=args.cache_disk_gb
    )
    
    system.run()
    
    total_time = time.perf_counter() - SCRIPT_START_TIME
    print(f"\n🎉 PROCESSAMENTO CONCLUÍDO! Tempo total: {total_time:.2f} segundos")
    
    if not args.dry_run:
        cache_stats = system.conversion_cache.get_stats()
        print(f"\n📊 RESUMO DE PERFORMANCE:")
        print(f"   Cache hits: {cache_stats['memory_hits'] + cache_stats['disk_hits']}")
        print(f"   Cache misses: {cache_stats['misses']}")
        print(f"   Taxa de acerto: {cache_stats['hit_rate']:.2%}")
        print(f"   Memória usada: {cache_stats['memory_usage_mb']:.2f} MB")
        print(f"   Evicções LRU: {cache_stats['evictions']}")


if __name__ == "__main__":
    main()