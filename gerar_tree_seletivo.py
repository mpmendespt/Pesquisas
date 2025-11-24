import os
import sys
import io

# ==========================================================
# 🛑 Correção para o Erro UnicodeEncodeError no Windows 🛑
# Força o sys.stdout a usar a codificação UTF-8 ao redirecionar para um arquivo (>).
# ==========================================================
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception as e:
    # Captura a exceção caso a reconfiguração falhe em ambientes muito restritos
    print(f"# Aviso: Falha ao configurar a saída para UTF-8. Erro: {e}", file=sys.stderr)


# ----------------------------------------------------------
# Funções de Geração
# ----------------------------------------------------------

def gerar_tree_recursivo(caminho_atual, configuracoes_depth, inclusoes_seletivas, diretorio_raiz, nivel_atual=0, prefixo=''):
    """
    Gera a estrutura de árvore recursivamente com controlo de profundidade e inclusão seletiva.
    """
    
    # 1. Determinar o limite de profundidade (Depth Control)
    limite = float('inf') 
    
    # Obtém o caminho relativo da pasta atual em relação à raiz do projeto
    caminho_relativo = os.path.relpath(caminho_atual, diretorio_raiz)

    # Verifica se a pasta atual está no dicionário de configurações de profundidade
    for caminho_config, profundidade in configuracoes_depth.items():
        if caminho_relativo.startswith(caminho_config) or caminho_relativo == caminho_config:
            # Assumimos que o limite se aplica ao caminho mais específico correspondente
            limite = profundidade
            break
            
    # Aplica o limite: Se o nível atual exceder o limite, interrompe a recursão
    if nivel_atual > limite:
        return
    
    try:
        conteudo = os.listdir(caminho_atual)
    except Exception:
        # Ignora pastas sem permissão
        return

    # Itens padrão a ignorar
    itens_a_ignorar = ['.git', '__pycache__', 'node_modules', '.DS_Store']
    
    # 2. Lógica de Inclusão/Exclusão
    
    # Verifica se esta pasta tem regras de inclusão seletiva
    arquivos_a_incluir = inclusoes_seletivas.get(caminho_relativo, None)

    # Filtragem de conteúdo
    pastas = []
    arquivos = []
    
    for item in conteudo:
        if item in itens_a_ignorar:
            continue
        
        caminho_item = os.path.join(caminho_atual, item)
        
        if os.path.isdir(caminho_item):
            # Se há inclusão seletiva, não mostramos subpastas
            # Mas permitimos se o nível atual ainda está abaixo do limite configurado
            if arquivos_a_incluir is None and nivel_atual < limite:
                pastas.append(item)
        
        elif os.path.isfile(caminho_item):
            if arquivos_a_incluir is None:
                # Inclusão normal
                arquivos.append(item)
            elif item in arquivos_a_incluir:
                # Inclusão seletiva (mostra apenas o arquivo listado)
                arquivos.append(item)

    # Ordena o conteúdo
    pastas.sort()
    arquivos.sort()
    todos_itens = pastas + arquivos
    # Nova lógica (Pastas e Arquivos misturados alfabeticamente)
    #todos_itens = pastas + arquivos
    #todos_itens.sort()
    
    # 3. Exibir e Chamar Recursivamente
    
    for i, item in enumerate(todos_itens):
        caminho_item = os.path.join(caminho_atual, item)
        
        eh_ultimo = (i == len(todos_itens) - 1)
        ramo = "└── " if eh_ultimo else "├── "
        
        if os.path.isdir(caminho_item):
            yield f"{prefixo}{ramo} {item}/"
            
            novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
            
            # Chamada recursiva para subdiretório
            yield from gerar_tree_recursivo(caminho_item, configuracoes_depth, inclusoes_seletivas, diretorio_raiz, nivel_atual + 1, novo_prefixo)
            
        else: # É um arquivo
            yield f"{prefixo}{ramo} {item}"

# ----------------------------------------------------------
# Configurações de Uso e Execução
# ----------------------------------------------------------

# 1. Defina a pasta raiz do seu projeto (MUDAR ESTE CAMINHO PARA O SEU PROJETO REAL)
# O código abaixo usa a pasta onde o script está como raiz para facilitar o teste.
# Troque por um caminho absoluto, se necessário: PASTA_DO_PROJETO = r'D:\Caminho\para\o\seu\projeto'
PASTA_DO_PROJETO = os.path.dirname(os.path.abspath(__file__)) 

# 2. Configura a PROFUNDIDADE MÁXIMA (Depth Control)
# A profundidade é contada a partir da RAIZ do projeto.
# Exemplo: 'src': 3 -> Exibe a pasta 'src' + 2 níveis abaixo dela (níveis 0, 1, 2)
CONFIGURACOES = {
    'src': 3, 
    'docs': 2,
    '.': 3,         # Configura profundidade padrão de 3 níveis para a raiz
    'Pesquisas_': 1,
    'worker-ds': 0,
    'wrangler': 0,
}

# 3. Configura a INCLUSÃO SELETIVA de arquivos
# Chave: Caminho RELATIVO da pasta. Valor: LISTA de arquivos a INCLUIR (todos os outros são ignorados)
INCLUSOES_SELETIVAS = {
    # 'src/config': ['settings.py', 'config.json'],
    # 'docs/assets': ['logo.png'],
    'docs\Pesquisas_': 'index.html',
    'worker-ds\src': 'index.js',
    'worker-ds\src': 'auth.js',
    #
}

# 4. Execução e Formatação Markdown
print("```bash") # Abre o bloco de código Markdown

nome_raiz = os.path.basename(os.path.abspath(PASTA_DO_PROJETO))
print(f"{nome_raiz}/") 

# Inicia a geração da árvore
for linha in gerar_tree_recursivo(PASTA_DO_PROJETO, CONFIGURACOES, INCLUSOES_SELETIVAS, PASTA_DO_PROJETO, 0, ''):
    print(linha)

print("```") # Fecha o bloco de código Markdown