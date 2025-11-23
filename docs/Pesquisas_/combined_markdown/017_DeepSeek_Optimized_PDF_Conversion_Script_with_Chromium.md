# Optimized PDF Conversion Script with Chromium

## 📊 Informações
- **Número:** #17
- **Origem:** DeepSeek
- **Categoria:** Programação
- **ID:** 40ecd2f0-3893-4b6b-9579-6bedc83dc8ea
- **Criada em:** 2025-11-07 04:59:56
- **Atualizada em:** 2025-11-07 18:52:23
- **Total de mensagens:** 18
- **Resumo:** Optimização comb_pdf_direct6_html_based_optimized_live_benchmark.py Pretende-se optimização do file ...

---

## 💬 Conversa

### 👤 Utilizador *(2025-11-07 04:59:57)* *[deepseek-reasoner]*

Optimização comb_pdf_direct6_html_based_optimized_live_benchmark.py Pretende-se optimização do file comb_pdf_direct6_html_based_optimized_live_benchmark.py Pretendo: Reutilização de uma instância do Chromium por processo (abre/fecha browser por batch).

Paralelismo seguro via multiprocessing.Pool.  Retry por arquivo (2 tentativas padrão).  Tratamento de para cancelamento limpo via Ctrl+C  Limite de workers:
3–4 é ótimo em 4 núcleos / 8 GB RAM.  Pretendo que sejam analisados so dois files. E se for possivel optimizar para aperfeiçoar algo recomendado que seja apresentado um file  comb_pdf_direct6_html_based_optimized_live_benchmark.py completo

---

### 🤖 DeepSeek *(2025-11-07 04:59:57)* *[deepseek-reasoner]*

Vamos analisar os dois arquivos fornecidos e focar na otimização do `comb_pdf_direct6_html_based_optimized_live_benchmark.py` com base nos requisitos:

1. Reutilização de uma instância do Chromium por processo (abre/fecha browser por batch).
2. Paralelismo seguro via multiprocessing.Pool.
3. Retry por arquivo (2 tentativas padrão).
4. Tratamento de cancelamento limpo via Ctrl+C.
5. Limite de workers: 3–4 é ótimo em 4 núcleos / 8 GB RAM.

Além disso, vamos considerar as melhores práticas do segundo arquivo (`comb_pdf_direct6_html_based.py`) que usa ThreadPoolExecutor e tem uma estrutura de classe, mas o foco será no primeiro arquivo que já está mais orientado a multiprocessamento.

Observações sobre o primeiro arquivo (comb_pdf_direct6_html_based_optimized_live_benchmark.py):

- Já usa multiprocessing.Pool.
- Já tem um sistema de interrupção com sinal.
- Já faz a abertura e fechamento do browser por batch (no worker `worker_process_batch_simple`).

No entanto, note que no worker atual, o browser é aberto e fechado para cada batch, o que está de acordo com a reutilização por processo (cada processo do pool abre um browser e processa um batch, depois fecha). Mas note que o batch é um conjunto de arquivos, então estamos reutilizando o browser para vários arquivos no mesmo batch, o que é bom.

O que podemos melhorar:

1. No worker atual, o browser é lançado com opções mínimas. Podemos adicionar opções de linha de comando para melhor desempenho e confiabilidade, semelhantes às do segundo arquivo.

2. No worker, a cada arquivo é criado um novo context e uma nova page. Isso é o ideal para isolar cada conversão.

3. O segundo arquivo usa `wait_for_function` para garantir que a página está carregada e uma espera adicional de 1 segundo. No primeiro arquivo, usamos `wait_until='networkidle'` e `page.wait_for_timeout(1000)`. Podemos considerar adicionar o `wait_for_function` para maior confiabilidade.

4. O segundo arquivo tem mais opções de PDF (como `prefer_css_page_size` e `scale`). Podemos adotar essas opções.

5. No primeiro arquivo, o retry é feito por arquivo, mas o browser é recriado a cada tentativa? Não, o browser é o mesmo para o batch, mas para cada arquivo é criado um context. Em caso de falha, o context é fechado e tentamos novamente com um novo context. Isso é aceitável.

6. O primeiro arquivo já usa uma fila de mensagens e um listener em thread para reportar o progresso.

7. O primeiro arquivo já tem um sistema de interrupção que tenta matar processos órfãos.

Vamos então ajustar o worker para usar opções de browser semelhantes às do segundo arquivo, e adicionar as opções de PDF do segundo arquivo.

Alterações propostas:

1. Ao lançar o browser, adicionar argumentos para desabilitar features desnecessárias e melhorar a estabilidade.

2. No PDF, adicionar `prefer_css_page_size` e `scale`.

3. Considerar adicionar `wait_for_function` para garantir que a página está pronta.

4. Manter o retry por arquivo (já está implementado).

5. Manter o mesmo sistema de interrupção.

6. Ajustar o número de workers para um padrão de 3, mas permitir que o usuário configure.

Vamos modificar o worker `worker_process_batch_simple`:

- Adicionar args ao lançar o browser.
- Adicionar `wait_for_function` após o `wait_for_timeout` (ou em vez dele) para garantir que a página está carregada.
- Ajustar as opções do PDF.

Além disso, note que o primeiro arquivo já está usando `page.goto` com `wait_until='networkidle'` e um timeout de 30 segundos. Isso é bom.

Vamos também ajustar o número padrão de workers para 3, já que é um bom valor para 4 núcleos.

Outra otimização: no primeiro arquivo, o batch size é 3. Isso significa que cada worker processa 3 arquivos. Podemos manter, mas note que o batch size é o número de arquivos por batch, e cada batch é atribuído a um worker. Com 3 workers e batch size 3, teríamos 9 arquivos sendo processados simultaneamente? Não, porque o pool tem 3 workers e cada worker pega um batch de 3 arquivos, então são 3 workers * 1 batch cada, mas cada batch tem 3 arquivos, então 3 workers * 3 arquivos = 9 arquivos em paralelo? Não, porque cada worker processa um batch de 3 arquivos sequencialmente. Portanto, o paralelismo real é o número de workers (3) e cada worker processa um arquivo por vez (mas o batch é uma lista de arquivos que o worker processa em sequência). Portanto, o batch size não afeta o paralelismo, apenas a granularidade da tarefa. Um batch size muito pequeno pode aumentar a sobrecarga de comunicação, e um muito grande pode tornar a interrupção menos responsiva. Podemos manter o batch size 3.

Vamos então reescrever o worker com as otimizações:

- Browser launch com args.
- Contexto com viewport (como no segundo arquivo).
- wait_for_function para readyState.
- Opções de PDF completas.

Além disso, vamos ajustar o número padrão de workers para 3.

Vamos também ajustar o timeout para o goto e wait_for_function para 30 segundos (já está).

Vamos ao código:

1. Modificar a função `worker_process_batch_simple`:

   - Adicionar args ao browser.
   - Adicionar viewport no contexto.
   - Adicionar wait_for_function.
   - Ajustar opções do PDF.

2. Alterar o número padrão de workers para 3.

3. Manter o retry_count padrão como 2.

4. Manter o batch_size padrão como 3.

Vamos também remover o `page.wait_for_timeout(1000)` e substituir pelo `wait_for_function`? Ou manter ambos? O wait_for_function já espera pelo readyState, então talvez o timeout extra não seja necessário. Mas o segundo arquivo usa um sleep de 1 segundo após o wait_for_function. Vamos manter o wait_for_function e remover o wait_for_timeout, pois o wait_for_function já espera até que a página esteja pronta.

No entanto, note que o wait_for_function pode falhar se a página não tiver o JavaScript habilitado? Mas como estamos convertendo HTML, é razoável supor que tenhamos um ambiente com JavaScript. Vamos tentar usar apenas o wait_for_function.

Outro ponto: o segundo arquivo usa `page.goto` com `wait_until='networkidle'` e depois `wait_for_function` para readyState. Isso é redundante? O `networkidle` já espera pela rede, mas o readyState pode ser verificado para garantir que a página está pronta. Vamos manter ambos.

Vamos também adicionar um try-except para o wait_for_function, e em caso de timeout, podemos tentar prosseguir ou falhar? Vamos manter a mesma lógica de retry: se qualquer passo falhar, vamos para a próxima tentativa.

Vamos reescrever a parte de conversão no worker:

```python
# Dentro do for attempt...
context = None
try:
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 segundos

    full_path = f"file:///{html_path.absolute()}"
    page.goto(full_path, wait_until='networkidle', timeout=30000)

    # Wait for complete load
    page.wait_for_function(
        'document.readyState === "complete"',
        timeout=30000
    )

    # Generate PDF with optimized settings
    pdf_params = {
        'path': str(pdf_path),
        'format': 'A4',
        'print_background': True,
        'margin': {'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
        'prefer_css_page_size': True,
        'display_header_footer': False,
        'scale': 1.0
    }
    page.pdf(**pdf_params)

    success = True
    msg_queue.put(("ok", pdf_path.name))
    break

except Exception as e:
    last_error = str(e)
    if attempt < retry_count - 1:
        time.sleep(1)
finally:
    if context:
        try:
            context.close()
        except:
            pass
```

Além disso, ao lançar o browser, vamos adicionar os args:

```python
browser = p.chromium.launch(
    headless=headless,
    args=[
        '--disable-web-security',
        '--disable-features=VizDisplayCompositor',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding'
    ]
)
```

Vamos também ajustar o número padrão de workers para 3 no argument parser.

Outra melhoria: no segundo arquivo, o PDF é gerado com `prefer_css_page_size` e `scale`. Vamos adicionar essas opções.

Vamos agora gerar o código completo com as alterações.

Nota: O código atual do worker já faz retry por arquivo. Vamos manter.

Vamos também ajustar o timeout para o wait_for_function para 30 segundos.

Vamos ao código completo do arquivo otimizado: Aqui está a versão otimizada do `comb_pdf_direct6_html_based_optimized_live_benchmark.py` com as melhorias solicitadas:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento limpo via Ctrl+C
- Workers otimizados (3-4 para 4 núcleos/8GB RAM)
- Browser management aprimorado
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False


# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception:
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - para TUDO imediatamente"""
    global _should_stop
    print(f"\n!!! EMERGENCY STOP !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando {len(_active_processes)} processos...")
    
    _should_stop = True
    
    # Terminar processos de forma agressiva
    for pid in list(_active_processes):
        try:
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                try:
                    child.kill()
                except:
                    pass
            parent.kill()
        except:
            pass
    
    kill_orphaned_chromium()
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificar parada ANTES de cada arquivo
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificar parada ANTES de cada tentativa
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1:
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                if not success:
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                else:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 10 arquivos ou no final
            if processed % 10 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(pool.imap_unordered(worker_wrapper_optimized, args_list)):
            if _should_stop or stop_event.is_set():
                print("🛑 Parada de emergência ativada!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificar parada entre batches
            if _should_stop or stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO RECEBIDA !!!")
        _should_stop = True
        stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        stop_event.set()
    finally:
        print("🧹 LIMPEZA FINAL...")
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if pool:
            try:
                pool.terminate()
            except:
                pass
            try:
                pool.join(timeout=1)
            except:
                pass
        
        # Limpeza final agressiva
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)

    # Relatório DETALHADO
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL OTIMIZADO:")
    print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
    print(f" ❌ Falhas: {len(failed)}")
    
    if failed:
        print("\n📋 Arquivos com falha (primeiros 10):")
        for fname, error in failed[:10]:
            print(f"   ‣ {fname}: {error}")
        if len(failed) > 10:
            print(f"   ... e mais {len(failed) - 10} falhas")
    
    if benchmark and success_count > 0 and elapsed > 0:
        rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
        rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
        print(f"⏱️  Tempo total: {elapsed:.1f}s")
        print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
        print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=3, 
                       help="Número de processos (padrão: 3 otimizado para 4 núcleos)")
    parser.add_argument('--batch-size', type=int, default=4, 
                       help="Arquivos por batch (padrão: 4 para balanceamento)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=45, help="Timeout por página (segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 6)),  # Limite máximo de 6 workers
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Principais Otimizações Implementadas:

### 1. **Reutilização de Browser por Processo**
- Uma instância do Chromium é criada por processo e reutilizada para todo o batch
- Fechamento adequado ao final de cada batch

### 2. **Configuração Otimizada do Browser**
- Args de linha de comando para melhor performance
- Viewport consistente para renderização
- Timeouts configuráveis

### 3. **Paralelismo Seguro**
- `multiprocessing.Pool` com número otimizado de workers (3 padrão)
- Batch size balanceado (4 arquivos por batch)
- Limite máximo de 6 workers para evitar sobrecarga

### 4. **Sistema de Retry Robusto**
- 2 tentativas padrão por arquivo
- Mensagens de retry no listener
- Pausa entre tentativas

### 5. **Cancelamento Melhorado**
- Verificação constante de interrupção
- Limpeza agressiva de processos órfãos
- Terminação segura do pool

### 6. **Monitoramento em Tempo Real**
- Listener com estatísticas de progresso
- Taxas de conversão em tempo real
- Relatório detalhado final

### 7. **Valores Padrão Otimizados**
- Workers: 3 (ideal para 4 núcleos)
- Batch size: 4
- Timeout: 45s
- Retry count: 2

### 8. **Performance**
- Redução de overhead por reutilização de browser
- Balanceamento entre paralelismo e uso de memória
- Limpeza agressiva de recursos

Esta versão oferece o melhor equilíbrio entre performance, estabilidade e capacidade de resposta a interrupções.

---

### 👤 Utilizador *(2025-11-07 05:17:24)* *[deepseek-reasoner]*

Está optimo. Pretendo uma pequena adição que a ser iniciado o processo de conversão de html para pdf que seja mostrado o metodo usado para a conversão. E o file comb_pdf_direct6_html_based_optimized_live_benchmark.py completo

---

### 🤖 DeepSeek *(2025-11-07 05:17:24)* *[deepseek-reasoner]*

Vamos adicionar uma mensagem no início da conversão que mostra o método utilizado (ou seja, a estratégia de paralelismo e reutilização do browser).
 A ideia é informar que estamos usando uma instância do Chromium por processo (worker) e que os arquivos são processados em batches.

 Vamos modificar a função `generate_pdfs_optimized` para incluir essa informação.

 Além disso, vamos ajustar a mensagem de início para destacar as otimizações.

 Já temos a mensagem de início que mostra o número de workers e o batch size, mas podemos ser mais explícitos sobre a reutilização do browser.

 Vamos adicionar uma linha explicativa:

 "Método: Paralelismo com reutilização de instância do Chromium por processo (worker)"

 Vamos colocar isso logo após a exibição dos parâmetros (workers, batch size, etc.) e antes do aviso do Ctrl+C.

 Vou também ajustar a mensagem de início para incluir a versão "ALTAMENTE OTIMIZADA".

 Vamos lá. Aqui está o arquivo completo com a adição solicitada, mostrando o método de conversão utilizado:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento limpo via Ctrl+C
- Workers otimizados (3-4 para 4 núcleos/8GB RAM)
- Browser management aprimorado
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False


# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception:
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - para TUDO imediatamente"""
    global _should_stop
    print(f"\n!!! EMERGENCY STOP !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando {len(_active_processes)} processos...")
    
    _should_stop = True
    
    # Terminar processos de forma agressiva
    for pid in list(_active_processes):
        try:
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                try:
                    child.kill()
                except:
                    pass
            parent.kill()
        except:
            pass
    
    kill_orphaned_chromium()
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificar parada ANTES de cada arquivo
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificar parada ANTES de cada tentativa
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1:
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                if not success:
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                else:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 10 arquivos ou no final
            if processed % 10 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")
    
    # MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
    print("\n🔄 MÉTODO DE CONVERSÃO:")
    print("   • Playwright + Chromium headless")
    print("   • 1 instância do browser por processo worker")
    print("   • Contexto separado por arquivo HTML")
    print("   • Paralelismo seguro com multiprocessing.Pool")
    print("   • Sistema de retry com múltiplas tentativas")
    print("   • Timeouts configuráveis por página")
    print("   • Interrupção imediata via Ctrl+C\n")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(pool.imap_unordered(worker_wrapper_optimized, args_list)):
            if _should_stop or stop_event.is_set():
                print("🛑 Parada de emergência ativada!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificar parada entre batches
            if _should_stop or stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO RECEBIDA !!!")
        _should_stop = True
        stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        stop_event.set()
    finally:
        print("🧹 LIMPEZA FINAL...")
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if pool:
            try:
                pool.terminate()
            except:
                pass
            try:
                pool.join(timeout=1)
            except:
                pass
        
        # Limpeza final agressiva
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)

    # Relatório DETALHADO
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL OTIMIZADO:")
    print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
    print(f" ❌ Falhas: {len(failed)}")
    
    if failed:
        print("\n📋 Arquivos com falha (primeiros 10):")
        for fname, error in failed[:10]:
            print(f"   ‣ {fname}: {error}")
        if len(failed) > 10:
            print(f"   ... e mais {len(failed) - 10} falhas")
    
    if benchmark and success_count > 0 and elapsed > 0:
        rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
        rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
        print(f"⏱️  Tempo total: {elapsed:.1f}s")
        print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
        print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=3, 
                       help="Número de processos (padrão: 3 otimizado para 4 núcleos)")
    parser.add_argument('--batch-size', type=int, default=4, 
                       help="Arquivos por batch (padrão: 4 para balanceamento)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=45, help="Timeout por página (segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 6)),  # Limite máximo de 6 workers
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Adição Principal Realizada:

Adicionei uma seção **"MÉTODO DE CONVERSÃO"** que é exibida quando o processo de conversão é iniciado:

```python
# MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
print("\n🔄 MÉTODO DE CONVERSÃO:")
print("   • Playwright + Chromium headless")
print("   • 1 instância do browser por processo worker")
print("   • Contexto separado por arquivo HTML")
print("   • Paralelismo seguro com multiprocessing.Pool")
print("   • Sistema de retry com múltiplas tentativas")
print("   • Timeouts configuráveis por página")
print("   • Interrupção imediata via Ctrl+C\n")
```

Esta adição fornece transparência total sobre a tecnologia e estratégia utilizada para a conversão, permitindo que o usuário entenda exatamente como o processo funciona.

## Características do Método Explicado:

1. **Playwright + Chromium headless** - Tecnologia base
2. **1 instância do browser por processo worker** - Otimização de recursos
3. **Contexto separado por arquivo HTML** - Isolamento e segurança
4. **Paralelismo seguro com multiprocessing.Pool** - Escalabilidade
5. **Sistema de retry com múltiplas tentativas** - Robustez
6. **Timeouts configuráveis por página** - Controle de performance
7. **Interrupção imediata via Ctrl+C** - Responsividade

O arquivo está completo e pronto para uso!

---

### 👤 Utilizador *(2025-11-07 05:32:58)* *[deepseek-reasoner]*

Tudo certo. Mas por vezes ainda existe problema  com Ctrl+C e estou a usar --batch-size 3 e --workers 2, por isso gostaria que fosse esse o default. E se possivel melhorar o a Interrupção imediata via Ctrl+C

---

### 🤖 DeepSeek *(2025-11-07 05:32:59)* *[deepseek-reasoner]*

Vamos ajustar os valores padrão para `--batch-size 3` e `--workers 2` e melhorar a interrupção via Ctrl+C.

Além disso, vamos revisar o tratamento de sinal para garantir que a interrupção seja a mais rápida e confiável possível.

Modificações:
1. Alterar o default de `--workers` para 2 e `--batch-size` para 3.
2. Revisar o mecanismo de interrupção para garantir que o sinal seja capturado e propagado mais rapidamente.

Vamos também adicionar uma verificação mais frequente da flag de parada dentro dos loops dos workers.

Obs: O código atual já usa `stop_event` e `_should_stop` para controlar a parada. Vamos garantir que a verificação dessas flags seja feita em pontos estratégicos.

Vamos modificar a função `worker_process_batch_optimized` para verificar a parada também durante o processamento de um batch, não apenas entre arquivos.

Além disso, no loop principal de processamento de batches, vamos verificar a flag de parada com mais frequência.

Vamos também ajustar o handler de sinal para definir `_should_stop` e `stop_event` imediatamente.

Vamos ao código: Aqui está o arquivo completo com os defaults ajustados para `--batch-size 3` e `--workers 2`, e com uma melhoria significativa no sistema de interrupção via Ctrl+C:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento IMEDIATO E CONFIÁVEL via Ctrl+C
- Workers otimizados (2 padrão) e batch-size 3
- Browser management aprimorado
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção MELHORADO
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False
_stop_event = None
_pool = None


# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Limpeza adicional para garantir
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-9", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception:
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - PARA TUDO IMEDIATAMENTE"""
    global _should_stop, _stop_event, _pool
    
    print(f"\n!!! EMERGENCY STOP SOLICITADO !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando processos...")
    
    _should_stop = True
    
    # Sinalizar parada para todos os processos
    if _stop_event:
        _stop_event.set()
    
    # Parar pool AGressivamente
    if _pool:
        try:
            print("🛑 Terminando pool de workers...")
            _pool.terminate()
            _pool.join(timeout=2)
        except:
            pass
    
    # Terminar processos filhos de forma agressiva
    current_pid = os.getpid()
    try:
        parent = psutil.Process(current_pid)
        children = parent.children(recursive=True)
        print(f"🔪 Terminando {len(children)} processos filhos...")
        
        for child in children:
            try:
                child_pid = child.pid
                if child_pid != current_pid and child_pid in _active_processes:
                    child.kill()
                    _active_processes.discard(child_pid)
            except:
                pass
    except:
        pass
    
    # Limpeza final de processos órfãos
    kill_orphaned_chromium()
    
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    print("⚠️ PROGRAMA INTERROMPIDO PELO UTILIZADOR")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificação MAIS FREQUENTE de parada
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificação MAIS FREQUENTE de parada
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Verificação de parada DURANTE o carregamento
                        if stop_event.is_set():
                            break
                            
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Verificação de parada DURANTE a espera
                        if stop_event.is_set():
                            break
                            
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Verificação de parada ANTES do PDF
                        if stop_event.is_set():
                            break
                            
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        # Não reportar retry se foi por interrupção
                        if not stop_event.is_set():
                            msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1 and not stop_event.is_set():
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                # Se foi interrompido, sair imediatamente
                if stop_event.is_set():
                    break
                    
                if not success and not stop_event.is_set():
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                elif success:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        if not stop_event.is_set():
            msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 5 arquivos para feedback mais frequente
            if processed % 5 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop, _stop_event, _pool
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")
    
    # MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
    print("\n🔄 MÉTODO DE CONVERSÃO:")
    print("   • Playwright + Chromium headless")
    print("   • 1 instância do browser por processo worker")
    print("   • Contexto separado por arquivo HTML")
    print("   • Paralelismo seguro com multiprocessing.Pool")
    print("   • Sistema de retry com múltiplas tentativas")
    print("   • Timeouts configuráveis por página")
    print("   • INTERRUPÇÃO IMEDIATA via Ctrl+C (SIGINT)\n")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    _stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, _stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    _pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        _pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        print("💡 Dica: Pressione Ctrl+C a qualquer momento para PARAR IMEDIATAMENTE")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(_pool.imap_unordered(worker_wrapper_optimized, args_list)):
            # Verificação MAIS FREQUENTE de parada
            if _should_stop or _stop_event.is_set():
                print("🛑 Parada de emergência ativada durante o processamento!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificação de parada entre batches
            if _should_stop or _stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO POR TECLADO DETECTADA !!!")
        _should_stop = True
        _stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        _stop_event.set()
    finally:
        print("\n🧹 LIMPEZA FINAL EM ANDAMENTO...")
        
        # Sinalizar parada para todos
        _should_stop = True
        _stop_event.set()
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if _pool:
            try:
                print("🔪 Terminando pool de workers...")
                _pool.terminate()
            except:
                pass
            try:
                _pool.join(timeout=2)
            except:
                pass
        
        # Limpeza final agressiva
        print("🗑️  Limpando processos órfãos...")
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)
        print("✅ Limpeza concluída")

    # Relatório DETALHADO (apenas se não foi interrompido abruptamente)
    if not _should_stop or success_count > 0:
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL OTIMIZADO:")
        print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
        print(f" ❌ Falhas: {len(failed)}")
        
        if failed and not _should_stop:
            print("\n📋 Arquivos com falha (primeiros 10):")
            for fname, error in failed[:10]:
                print(f"   ‣ {fname}: {error}")
            if len(failed) > 10:
                print(f"   ... e mais {len(failed) - 10} falhas")
        
        if benchmark and success_count > 0 and elapsed > 0:
            rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
            rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
            print(f"⏱️  Tempo total: {elapsed:.1f}s")
            print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
            print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0 and not _should_stop


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=2, 
                       help="Número de processos (padrão: 2 otimizado para estabilidade)")
    parser.add_argument('--batch-size', type=int, default=3, 
                       help="Arquivos por batch (padrão: 3 para resposta rápida)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=45, help="Timeout por página (segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO IMEDIATAMENTE !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 4)),  # Limite máximo de 4 workers para estabilidade
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL DETECTADA !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Principais Melhorias na Interrupção Ctrl+C:

### 1. **Defaults Otimizados**
- `--workers 2` (em vez de 3)
- `--batch-size 3` (em vez de 4)

### 2. **Sistema de Interrupção Melhorado**
- **Verificações mais frequentes** de parada em todos os pontos críticos
- **Variáveis globais** para `_stop_event` e `_pool` para acesso direto no handler
- **Limpeza mais agressiva** de processos filhos
- **Terminação imediata** do pool com `terminate() + join()`

### 3. **Melhorias no Handler de Emergência**
- Acesso direto ao pool global para terminação imediata
- Kill seletivo de processos filhos
- Limpeza dupla de processos Chromium
- Mensagens mais claras sobre o estado da interrupção

### 4. **Verificações de Parada Adicionais**
- Durante o carregamento de páginas
- Antes da geração de PDF
- Entre tentativas de retry
- A cada 5 arquivos processados (feedback mais frequente)

### 5. **Limpeza Mais Robusta**
- Múltiplas tentativas de kill de processos
- Timeouts mais curtos para finalização
- Verificação de processos órfãos adicional

### 6. **Feedback Melhorado**
- Mensagens mais explícitas sobre interrupção
- Indicadores visuais de limpeza em andamento
- Confirmação de limpeza concluída

Agora o Ctrl+C deve ser **quase instantâneo** e **extremamente confiável**, mesmo com os parâmetros `--workers 2 --batch-size 3` que você está usando. O sistema verifica a interrupção em praticamente todos os pontos do código onde poderia haver bloqueio.

---

### 👤 Utilizador *(2025-11-07 05:46:11)* *[deepseek-reasoner]*

Pretendo a seguinte alteração no comb_pdf_direct6_html_based_optimized_live_benchmark.py    Detecção de conda activate Pesquisas. Isto é, que foi activado o ambiente Pesquisas; e se não mostrar a mensagem Use: conda activate Pesquisas antes de executar este script. E parar o script.

---

### 🤖 DeepSeek *(2025-11-07 05:46:11)* *[deepseek-reasoner]*

Vamos adicionar uma verificação para detectar se o ambiente Conda "Pesquisas" está ativo.
 Se não estiver, exibiremos uma mensagem e pararemos o script.

 Podemos fazer isso verificando a variável de ambiente CONDA_DEFAULT_ENV ou CONDA_PREFIX.
 No Windows e Linux, a variável CONDA_DEFAULT_ENV deve conter o nome do ambiente atual.

 No entanto, note que o script pode ser executado em qualquer ambiente Conda, ou até mesmo sem Conda.
 Vamos verificar se o Conda está ativo e se o ambiente é "Pesquisas".

 Se não estiver no ambiente "Pesquisas", exiba a mensagem e saia.

 Vamos também adicionar uma opção para pular essa verificação, caso o usuário queira.

 Mas note: o script original não tem essa verificação. Vamos adicionar no início do main().

 Passos:
 1. Verificar se a variável de ambiente CONDA_DEFAULT_ENV existe e é igual a "Pesquisas".
 2. Se não for, verificar se o usuário passou uma opção para ignorar (vamos adicionar um argumento opcional --ignore-conda-env).
 3. Se não ignorar, exibir mensagem e sair.

 No entanto, o usuário pode não estar usando Conda. Vamos apenas avisar se estiver em um Conda environment que não é o "Pesquisas".

 Mas note: se o usuário não estiver em um ambiente Conda, CONDA_DEFAULT_ENV não estará definida. Nesse caso, não vamos fazer nada?
 A intenção é garantir que o ambiente correto seja ativado. Se o usuário não estiver no Conda, talvez não tenha as dependências?

 Vamos pensar: o script precisa do Playwright e do Chromium. Se o usuário tiver instalado globalmente, pode funcionar.

 Mas como o objetivo é forçar o uso do ambiente "Pesquisas", vamos verificar apenas se o Conda está ativo (ou seja, se a variável CONDA_DEFAULT_ENV existe) e se não é o ambiente "Pesquisas".

 Se a variável CONDA_DEFAULT_ENV existir e não for "Pesquisas", então avisamos.

 Se não existir, assumimos que o usuário não está usando Conda e, portanto, não podemos garantir o ambiente. Mas talvez queiramos forçar o Conda?

 Vamos ajustar: a mensagem diz "Use: cond

---

### 👤 Utilizador *(2025-11-07 05:47:08)* *[deepseek-reasoner]*

Pretendo a seguinte alteração no comb_pdf_direct6_html_based_optimized_live_benchmark.py    Detecção de conda activate Pesquisas. Isto é, que foi activado o ambiente Pesquisas; e se não mostrar a mensagem Use: conda activate Pesquisas antes de executar este script. E parar o script. (No windows)

---

### 🤖 DeepSeek *(2025-11-07 05:47:08)* *[deepseek-reasoner]*

Vamos adicionar uma verificação no início do script para verificar se o ambiente conda "Pesquisas" está ativo.
 No Windows, podemos verificar a variável de ambiente CONDA_DEFAULT_ENV ou CONDA_PREFIX.
 Se não estiver no ambiente "Pesquisas", exibimos a mensagem e saímos.

 No Windows, o conda altera a variável de ambiente CONDA_DEFAULT_ENV para o nome do ambiente atual.
 Vamos verificar se CONDA_DEFAULT_ENV é "Pesquisas". Se não for, exibimos a mensagem e saímos.

 No entanto, note que o usuário pode ter ativado o ambiente via `conda activate` apenas no terminal atual.
 Mas no script, podemos verificar a variável de ambiente.

 Vamos fazer:
   - Se a variável de ambiente CONDA_DEFAULT_ENV existir e for "Pesquisas", continuamos.
   - Caso contrário, exibimos a mensagem e saímos.

 Mas note: é possível que o usuário não esteja usando conda? Sim, mas o requisito é que use o ambiente "Pesquisas".
 Se não estiver usando conda, a variável CONDA_DEFAULT_ENV não existirá.

 Outra abordagem: verificar CONDA_PREFIX, que aponta para o diretório do ambiente. Mas não temos o caminho fixo.

 Vamos optar por verificar CONDA_DEFAULT_ENV.

 No Windows, a variável de ambiente é acessível via os.environ.

 Vamos adicionar esta verificação no início do main(). Aqui está o arquivo completo com a detecção do ambiente Conda "Pesquisas" para Windows:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento IMEDIATO E CONFIÁVEL via Ctrl+C
- Workers otimizados (2 padrão) e batch-size 3
- Browser management aprimorado
- Detecção de ambiente Conda "Pesquisas"
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção MELHORADO
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False
_stop_event = None
_pool = None


# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def check_conda_environment():
    """Verifica se o ambiente Conda 'Pesquisas' está ativo no Windows"""
    if platform.system() != "Windows":
        return True  # Skip check on non-Windows systems
    
    try:
        # Método 1: Verificar variável de ambiente CONDA_DEFAULT_ENV
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
        if 'Pesquisas' in conda_env:
            print(f"✅ Ambiente Conda detectado: {conda_env}")
            return True
        
        # Método 2: Verificar via comando conda info
        result = subprocess.run(
            ['conda', 'info', '--json'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            import json
            conda_info = json.loads(result.stdout)
            active_env = conda_info.get('active_prefix_name', '')
            if 'Pesquisas' in active_env:
                print(f"✅ Ambiente Conda detectado: {active_env}")
                return True
        
        # Método 3: Verificar no prompt via conda env list
        result = subprocess.run(
            ['conda', 'env', 'list'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0 and 'Pesquisas' in result.stdout:
            print("⚠️  Ambiente 'Pesquisas' existe mas não está ativo!")
            return False
        
        # Se nenhum método encontrou o ambiente Pesquisas
        print("❌ AMBIENTE CONDA 'PESQUISAS' NÃO DETECTADO!")
        print("\n🔧 USE O SEGUINTE COMANDO ANTES DE EXECUTAR:")
        print("   conda activate Pesquisas")
        print("\n💡 Se o ambiente não existir, crie com:")
        print("   conda create -n Pesquisas python=3.8")
        print("   conda activate Pesquisas")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return False
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Conda não encontrado ou comando falhou!")
        print("\n🔧 VERIFIQUE SE O CONDA ESTÁ INSTALADO E CONFIGURADO")
        print("   E USE: conda activate Pesquisas")
        return False
    except Exception as e:
        print(f"❌ Erro na verificação do Conda: {e}")
        print("\n🔧 USE: conda activate Pesquisas antes de executar este script")
        return False


def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Limpeza adicional para garantir
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-9", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception:
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - PARA TUDO IMEDIATAMENTE"""
    global _should_stop, _stop_event, _pool
    
    print(f"\n!!! EMERGENCY STOP SOLICITADO !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando processos...")
    
    _should_stop = True
    
    # Sinalizar parada para todos os processos
    if _stop_event:
        _stop_event.set()
    
    # Parar pool AGressivamente
    if _pool:
        try:
            print("🛑 Terminando pool de workers...")
            _pool.terminate()
            _pool.join(timeout=2)
        except:
            pass
    
    # Terminar processos filhos de forma agressiva
    current_pid = os.getpid()
    try:
        parent = psutil.Process(current_pid)
        children = parent.children(recursive=True)
        print(f"🔪 Terminando {len(children)} processos filhos...")
        
        for child in children:
            try:
                child_pid = child.pid
                if child_pid != current_pid and child_pid in _active_processes:
                    child.kill()
                    _active_processes.discard(child_pid)
            except:
                pass
    except:
        pass
    
    # Limpeza final de processos órfãos
    kill_orphaned_chromium()
    
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    print("⚠️ PROGRAMA INTERROMPIDO PELO UTILIZADOR")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificação MAIS FREQUENTE de parada
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificação MAIS FREQUENTE de parada
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Verificação de parada DURANTE o carregamento
                        if stop_event.is_set():
                            break
                            
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Verificação de parada DURANTE a espera
                        if stop_event.is_set():
                            break
                            
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Verificação de parada ANTES do PDF
                        if stop_event.is_set():
                            break
                            
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        # Não reportar retry se foi por interrupção
                        if not stop_event.is_set():
                            msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1 and not stop_event.is_set():
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                # Se foi interrompido, sair imediatamente
                if stop_event.is_set():
                    break
                    
                if not success and not stop_event.is_set():
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                elif success:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        if not stop_event.is_set():
            msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 5 arquivos para feedback mais frequente
            if processed % 5 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop, _stop_event, _pool
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")
    
    # MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
    print("\n🔄 MÉTODO DE CONVERSÃO:")
    print("   • Playwright + Chromium headless")
    print("   • 1 instância do browser por processo worker")
    print("   • Contexto separado por arquivo HTML")
    print("   • Paralelismo seguro com multiprocessing.Pool")
    print("   • Sistema de retry com múltiplas tentativas")
    print("   • Timeouts configuráveis por página")
    print("   • INTERRUPÇÃO IMEDIATA via Ctrl+C (SIGINT)\n")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    _stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, _stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    _pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        _pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        print("💡 Dica: Pressione Ctrl+C a qualquer momento para PARAR IMEDIATAMENTE")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(_pool.imap_unordered(worker_wrapper_optimized, args_list)):
            # Verificação MAIS FREQUENTE de parada
            if _should_stop or _stop_event.is_set():
                print("🛑 Parada de emergência ativada durante o processamento!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificação de parada entre batches
            if _should_stop or _stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO POR TECLADO DETECTADA !!!")
        _should_stop = True
        _stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        _stop_event.set()
    finally:
        print("\n🧹 LIMPEZA FINAL EM ANDAMENTO...")
        
        # Sinalizar parada para todos
        _should_stop = True
        _stop_event.set()
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if _pool:
            try:
                print("🔪 Terminando pool de workers...")
                _pool.terminate()
            except:
                pass
            try:
                _pool.join(timeout=2)
            except:
                pass
        
        # Limpeza final agressiva
        print("🗑️  Limpando processos órfãos...")
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)
        print("✅ Limpeza concluída")

    # Relatório DETALHADO (apenas se não foi interrompido abruptamente)
    if not _should_stop or success_count > 0:
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL OTIMIZADO:")
        print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
        print(f" ❌ Falhas: {len(failed)}")
        
        if failed and not _should_stop:
            print("\n📋 Arquivos com falha (primeiros 10):")
            for fname, error in failed[:10]:
                print(f"   ‣ {fname}: {error}")
            if len(failed) > 10:
                print(f"   ... e mais {len(failed) - 10} falhas")
        
        if benchmark and success_count > 0 and elapsed > 0:
            rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
            rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
            print(f"⏱️  Tempo total: {elapsed:.1f}s")
            print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
            print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0 and not _should_stop


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=2, 
                       help="Número de processos (padrão: 2 otimizado para estabilidade)")
    parser.add_argument('--batch-size', type=int, default=3, 
                       help="Arquivos por batch (padrão: 3 para resposta rápida)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=45, help="Timeout por página (segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # VERIFICAÇÃO DO AMBIENTE CONDA - APENAS NO WINDOWS
    if platform.system() == "Windows":
        print("🔍 Verificando ambiente Conda 'Pesquisas'...")
        if not check_conda_environment():
            print("\n❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!")
            print("💡 Use o comando abaixo antes de executar este script:")
            print("   conda activate Pesquisas")
            return 1
    else:
        print("🔍 Sistema não-Windows detectado, pulando verificação do Conda...")
    
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO IMEDIATAMENTE !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 4)),  # Limite máximo de 4 workers para estabilidade
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL DETECTADA !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Principais Adições:

### 1. **Função `check_conda_environment()`**
- Verifica se o ambiente Conda "Pesquisas" está ativo no Windows
- Usa múltiplos métodos para detecção:
  - Variável de ambiente `CONDA_DEFAULT_ENV`
  - Comando `conda info --json`
  - Comando `conda env list`

### 2. **Integração na Função `main()`**
```python
# VERIFICAÇÃO DO AMBIENTE CONDA - APENAS NO WINDOWS
if platform.system() == "Windows":
    print("🔍 Verificando ambiente Conda 'Pesquisas'...")
    if not check_conda_environment():
        print("\n❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!")
        print("💡 Use o comando abaixo antes de executar este script:")
        print("   conda activate Pesquisas")
        return 1
```

### 3. **Mensagens de Erro Detalhadas**
- Detecta se o ambiente existe mas não está ativo
- Fornece instruções claras para ativação
- Inclui comandos para criar o ambiente se não existir

### 4. **Comportamento por Sistema**
- Apenas verifica no Windows
- Ignora a verificação em outros sistemas operacionais

## Funcionamento:

1. **No Windows**: Verifica se o ambiente "Pesquisas" está ativo
2. **Se não estiver ativo**: Mostra mensagem clara e para a execução
3. **Se estiver ativo**: Continua normalmente com a conversão
4. **Em outros SOs**: Pula a verificação e continua normalmente

Agora o script garantirá que o ambiente Conda correto esteja ativo antes de prosseguir com a conversão!

---

### 👤 Utilizador *(2025-11-07 05:54:42)* *[deepseek-reasoner]*

Não é detectado por isso (base) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>python comb_pdf_direct6_html_based_optimized_live_benchmark.py --benchmark
Traceback (most recent call last):
  File "D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op\comb_pdf_direct6_html_based_optimized_live_benchmark.py", line 28, in <module>
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
ModuleNotFoundError: No module named 'playwright'

Tambem pretendo que --timeout 50 seja o default

---

### 🤖 DeepSeek *(2025-11-07 05:54:42)* *[deepseek-reasoner]*

Vamos ajustar o script para que o timeout padrão seja 50 e também melhorar a detecção do ambiente Conda.
 O problema é que o ambiente Conda não está sendo detectado corretamente. Vamos tentar uma abordagem mais direta.

 Além disso, o erro "ModuleNotFoundError: No module named 'playwright'" indica que o playwright não está instalado no ambiente ativo.
 A verificação do Conda deve ser feita antes de importar o playwright, mas não podemos evitar a importação porque a verificação do Conda está no main.

 Vamos reestruturar:

 1. Mover a verificação do Conda para o início do main, antes de importar o playwright?
    Não, porque a importação do playwright já está no topo. Vamos tentar uma abordagem diferente.

 2. Em vez de verificar o Conda no main, vamos verificar no início do script, mas isso não é possível porque a importação do playwright já falha.

 3. Solução: Adiar a importação do playwright até depois da verificação do Conda.

 Porém, a verificação do Conda está no main, e as funções que usam playwright estão definidas antes do main.

 Vamos reorganizar:

 - Mover a importação do playwright para dentro das funções que o usam? Isso é possível, mas tornaria o código mais lento e menos legível.

 4. Outra ideia: Verificar o ambiente Conda e, se estiver no Windows e o ambiente não for o Pesquisas, exibir a mensagem e sair, mas sem dependender da importação do playwright.

 5. Vamos tentar uma verificação simples: se estiver no Windows, verificar a variável de ambiente CONDA_DEFAULT_ENV.

 6. Se a variável existir e for "Pesquisas", então continuamos. Caso contrário, exibimos a mensagem e saímos.

 7. Mas note: o usuário pode não estar usando Conda, então se a variável não existir, não podemos assumir que está no ambiente correto.

 8. Vamos ajustar a função check_conda_environment para ser mais simples e confiável.

 9. E também mudar o default do timeout para 50.

 Vamos fazer:

 - A função check_conda_environment vai verificar a variável de ambiente CONDA_DEFAULT_ENV.
 - Se a variável existir e for "Pesquisas", retorna True.
 - Se não, tenta usar o comando `conda info --envs` para verificar o ambiente ativo? Mas isso é mais lento.

 10. Vamos manter simples: apenas a variável de ambiente.

 11. E adicionar uma opção para pular a verificação? Não, porque o objetivo é garantir que está no ambiente correto.

 12. Se a variável não existir, então assumimos que não está no Conda e exibimos a mensagem.

 13. Mas e se o usuário estiver em outro ambiente Conda? A variável existirá e terá o nome do ambiente.

 14. Vamos modificar a função para:

     - No Windows, se a variável CONDA_DEFAULT_ENV existir e for "Pesquisas", retorna True.
     - Se existir e não for "Pesquisas", imprime a mensagem e retorna False.
     - Se não existir, imprime a mensagem e retorna False.

 15. E se não for Windows, não faz a verificação? Sim, porque o problema é específico do Windows.

 16. Vamos também alterar o default do timeout para 50.

 17. E corrigir: a verificação do Conda deve ser a primeira coisa no main, mas a importação do playwright já falhou.

 18. Para resolver o problema da importação, temos que adiar a importação do playwright até depois da verificação.

 19. Vamos mover a importação do playwright para dentro da função check_playwright_available? Sim, porque essa função é chamada depois da verificação do Conda.

 20. E também mover a importação para dentro das funções que usam playwright? Isso é possível, mas vai espalhar as importações.

 21. Vamos tentar mover a importação do playwright para dentro da função check_playwright_available e da worker function.

 22. Na função check_playwright_available, vamos importar sync_playwright dentro da função.

 23. Na worker function, vamos importar sync_playwright e PlaywrightTimeoutError dentro da função.

 24. E na função generate_pdfs_optimized, a importação do playwright não é usada diretamente, então não precisamos mover.

 25. Vamos fazer:

     - Remover a importação do playwright no topo.
     - Em check_playwright_available, importar sync_playwright dentro do try.
     - Na worker_process_batch_optimized, importar sync_playwright e PlaywrightTimeoutError dentro da função.

 26. Mas note: a worker function é executada em outro processo, então a importação lá dentro não afeta o processo principal.

 27. No processo principal, a função check_playwright_available é chamada depois da verificação do Conda, então se o ambiente estiver correto, a importação deve funcionar.

 28. Vamos tentar.

 29. Além disso, alterar o default do timeout para 50.

 30. E também ajustar a verificação do Conda para ser mais tolerante? Não, queremos que seja rigorosa.

 Vamos reescrever o código:

 - Remover a importação do playwright no topo.
 - Mover a importação para dentro das funções que usam.

 No entanto, isso pode causar overhead, mas é aceitável porque as funções são chamadas apenas uma vez.

 Vamos fazer:

   - check_playwright_available: importar sync_playwright dentro do try.
   - worker_process_batch_optimized: importar sync_playwright e PlaywrightTimeoutError dentro da função.

 31. E na função emergency_stop_handler, não usamos playwright, então não precisa.

 32. Vamos testar.

 33. Além disso, na função check_conda_environment, vamos simplificar:

     - No Windows, verificar a variável CONDA_DEFAULT_ENV.
     - Se for "Pesquisas", retorna True.
     - Caso contrário, retorna False.

 34. E no main, se for Windows e a verificação retornar False, sair com mensagem.

 35. Se não for Windows, não verificar.

 36. Vamos também alterar o default do timeout para 50.

 37. E ajustar a ajuda do argumento timeout.

 Vamos implementar. Aqui está o arquivo corrigido com a detecção melhorada do ambiente Conda e o timeout padrão de 50:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento IMEDIATO E CONFIÁVEL via Ctrl+C
- Workers otimizados (2 padrão) e batch-size 3
- Browser management aprimorado
- Detecção de ambiente Conda "Pesquisas"
- Timeout padrão de 50 segundos
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional

# Importação do Playwright adiada para depois da verificação do Conda
# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção MELHORADO
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False
_stop_event = None
_pool = None


# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def check_conda_environment():
    """Verifica se o ambiente Conda 'Pesquisas' está ativo no Windows"""
    if platform.system() != "Windows":
        return True  # Skip check on non-Windows systems
    
    try:
        # Método 1: Verificar variável de ambiente CONDA_DEFAULT_ENV (mais confiável)
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
        print(f"🔍 Ambiente Conda detectado: {conda_env}")
        
        if 'Pesquisas' in conda_env:
            print(f"✅ Ambiente Conda correto: {conda_env}")
            return True
        
        # Método 2: Verificar se estamos em qualquer ambiente conda (não base)
        if conda_env and conda_env != 'base':
            print(f"⚠️  Ambiente Conda detectado: {conda_env} (mas não é 'Pesquisas')")
            return False
        
        # Método 3: Tentar detectar via conda info
        try:
            result = subprocess.run(
                ['conda', 'info', '--json'], 
                capture_output=True, 
                text=True, 
                timeout=5,
                shell=True
            )
            if result.returncode == 0:
                import json
                conda_info = json.loads(result.stdout)
                active_env = conda_info.get('active_prefix_name', '')
                if active_env:
                    print(f"🔍 Ambiente ativo via conda info: {active_env}")
                    if 'Pesquisas' in active_env:
                        print(f"✅ Ambiente Conda correto: {active_env}")
                        return True
        except:
            pass
        
        # Se chegou aqui, não detectou o ambiente Pesquisas
        print("❌ AMBIENTE CONDA 'PESQUISAS' NÃO DETECTADO!")
        print("\n🔧 USE O SEGUINTE COMANDO ANTES DE EXECUTAR:")
        print("   conda activate Pesquisas")
        print("\n💡 Se o ambiente não existir, crie com:")
        print("   conda create -n Pesquisas python=3.8")
        print("   conda activate Pesquisas")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return False
        
    except Exception as e:
        print(f"❌ Erro na verificação do Conda: {e}")
        print("\n🔧 USE: conda activate Pesquisas antes de executar este script")
        return False


def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Limpeza adicional para garantir
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-9", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Playwright: {e}")
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - PARA TUDO IMEDIATAMENTE"""
    global _should_stop, _stop_event, _pool
    
    print(f"\n!!! EMERGENCY STOP SOLICITADO !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando processos...")
    
    _should_stop = True
    
    # Sinalizar parada para todos os processos
    if _stop_event:
        _stop_event.set()
    
    # Parar pool AGressivamente
    if _pool:
        try:
            print("🛑 Terminando pool de workers...")
            _pool.terminate()
            _pool.join(timeout=2)
        except:
            pass
    
    # Terminar processos filhos de forma agressiva
    current_pid = os.getpid()
    try:
        parent = psutil.Process(current_pid)
        children = parent.children(recursive=True)
        print(f"🔪 Terminando {len(children)} processos filhos...")
        
        for child in children:
            try:
                child_pid = child.pid
                if child_pid != current_pid and child_pid in _active_processes:
                    child.kill()
                    _active_processes.discard(child_pid)
            except:
                pass
    except:
        pass
    
    # Limpeza final de processos órfãos
    kill_orphaned_chromium()
    
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    print("⚠️ PROGRAMA INTERROMPIDO PELO UTILIZADOR")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    from playwright.sync_api import sync

---

### 👤 Utilizador *(2025-11-07 06:02:00)* *[deepseek-reasoner]*

Não me parece boa ideia     Remover a importação do playwright no topo.

    Mover a importação para dentro das funções que usam. Por cusa do 
  overhead. Poque não fazer com que a primeira função usada seja a deteção de ambinte. E depois fazer o import de playwright  ou outras. Proceguir com o resto do script.

---

### 🤖 DeepSeek *(2025-11-07 06:02:00)* *[deepseek-reasoner]*

Vamos ajustar a estratégia:

1. Manter a importação do playwright no topo, mas protegê-la com uma verificação condicional.
2. Primeiro, verificar o ambiente Conda (apenas no Windows) e só então importar o playwright.
3. Se a verificação do Conda falhar, o script termina antes de tentar importar o playwright.

No entanto, o erro que você está tendo é porque o playwright não está instalado no ambiente base. A verificação do Conda está falhando em detectar que você não está no ambiente 'Pesquisas'. Vamos melhorar a verificação do Conda.

Além disso, vamos mudar o timeout padrão para 50.

Vamos reorganizar o código:

- Primeiro, verificar o ambiente Conda (apenas Windows) e sair se não for o ambiente correto.
- Só então importar o playwright (e outras dependências) para evitar ModuleNotFoundError.

Mas note: se o playwright não estiver instalado no ambiente 'Pesquisas', o mesmo erro ocorrerá. A verificação do Conda deve garantir que estamos no ambiente correto, e a verificação do playwright (que vem depois) deve garantir que as dependências estão instaladas.

Vamos ajustar a função `check_conda_environment` para ser mais rigorosa.

Outra ideia: em vez de verificar se o ambiente é "Pesquisas", podemos verificar se o playwright está instalado. Se não estiver, avisamos para ativar o ambiente correto. Mas isso pode ser enganoso se o playwright não estiver instalado no ambiente 'Pesquisas'.

Vamos tentar:

1. Verificar se estamos no Windows.
2. Se sim, verificar a variável de ambiente CONDA_DEFAULT_ENV. Se não for "Pesquisas", avisar e sair.
3. Se não for Windows, não fazemos a verificação.

Mas note: o erro que você teve foi porque o playwright não estava instalado no ambiente base. Portanto, a verificação do Conda deve ser feita antes de importar o playwright.

Vamos mover a importação do playwright para depois da verificação do Conda. Vamos também adicionar uma verificação da instalação do playwright usando a função `check_playwright_available` que já temos.

Vamos reestruturar o main:

- Verificar Conda (Windows apenas)
- Importar playwright (e outras dependências) após a verificação do Conda
- Verificar se o playwright está disponível (usando a função existente)

No entanto, não podemos mover todas as importações de playwright para depois da verificação do Conda porque o código depende dele em várias funções. Vamos então:

- Deixar a importação do playwright no topo, mas dentro de um bloco condicional que só é executado se a verificação do Conda passar? Não, porque o import é no topo e é executado antes do main.

Uma solução alternativa é:

- Não importar o playwright no topo, mas sim dentro das funções que o usam. Isso pode ser feito, mas pode causar overhead? Na verdade, o import é custoso, mas como essas funções são chamadas apenas uma vez por processo, e são poucas, pode ser aceitável.

Outra solução:

- Fazer a verificação do Conda no início do main, e se passar, então importar o playwright e outros módulos. Mas isso exigiria que todo o código que usa playwright estivesse dentro de funções que só são chamadas após o import.

Vamos adotar a seguinte estratégia:

1. Remover as importações de playwright do topo.
2. Fazer a verificação do Conda no início do main.
3. Se a verificação do Conda for bem-sucedida (ou se não for Windows), então importar o playwright.
4. Colocar as importações do playwright dentro das funções que o utilizam.

Isso evita o erro de importação se o ambiente Conda não estiver ativo.

Vamos fazer isso, e também ajustar o timeout padrão para 50.

Vou reescrever o código para:

- Remover a importação do playwright no topo.
- Mover a importação para dentro das funções `check_playwright_available`, `worker_process_batch_optimized` e `generate_pdfs_optimized` (que é chamada por main).

Além disso, a função `check_playwright_available` já faz um teste de importação, então podemos usar essa função para verificar a instalação do playwright.

Vamos ajustar:

- A função `check_playwright_available` deve tentar importar o playwright e, se falhar, retornar False.

Vamos modificar a função `check_playwright_available` para:

```python
def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless_test)
            browser.close()
        return True
    except Exception:
        return False
```

E então, no main, após a verificação do Conda, chamamos `check_playwright_available` e, se falhar, avisamos para instalar.

Vamos reescrever o código conforme abaixo.

Nota: Vamos também alterar o timeout padrão para 50 no argument parser.

Vamos lá. Aqui está o arquivo corrigido com a detecção do ambiente Conda no início e importação do Playwright apenas após a verificação, mantendo a performance:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento IMEDIATO E CONFIÁVEL via Ctrl+C
- Workers otimizados (2 padrão) e batch-size 3
- Browser management aprimorado
- Detecção de ambiente Conda "Pesquisas"
- Timeout padrão de 50 segundos
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção MELHORADO
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False
_stop_event = None
_pool = None

# ---------------------------------------------------------------------
# DETECÇÃO DO AMBIENTE CONDA - DEVE SER A PRIMEIRA COISA A EXECUTAR
# ---------------------------------------------------------------------
def check_conda_environment():
    """Verifica se o ambiente Conda 'Pesquisas' está ativo no Windows"""
    if platform.system() != "Windows":
        return True  # Skip check on non-Windows systems
    
    try:
        # Método 1: Verificar variável de ambiente CONDA_DEFAULT_ENV (mais confiável)
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
        print(f"🔍 Ambiente Conda detectado: {conda_env}")
        
        if 'Pesquisas' in conda_env:
            print(f"✅ Ambiente Conda correto: {conda_env}")
            return True
        
        # Método 2: Verificar se estamos em qualquer ambiente conda (não base)
        if conda_env and conda_env != 'base':
            print(f"⚠️  Ambiente Conda detectado: {conda_env} (mas não é 'Pesquisas')")
            return False
        
        # Método 3: Tentar detectar via conda info
        try:
            result = subprocess.run(
                ['conda', 'info', '--json'], 
                capture_output=True, 
                text=True, 
                timeout=5,
                shell=True
            )
            if result.returncode == 0:
                import json
                conda_info = json.loads(result.stdout)
                active_env = conda_info.get('active_prefix_name', '')
                if active_env:
                    print(f"🔍 Ambiente ativo via conda info: {active_env}")
                    if 'Pesquisas' in active_env:
                        print(f"✅ Ambiente Conda correto: {active_env}")
                        return True
        except:
            pass
        
        # Se chegou aqui, não detectou o ambiente Pesquisas
        print("❌ AMBIENTE CONDA 'PESQUISAS' NÃO DETECTADO!")
        print("\n🔧 USE O SEGUINTE COMANDO ANTES DE EXECUTAR:")
        print("   conda activate Pesquisas")
        print("\n💡 Se o ambiente não existir, crie com:")
        print("   conda create -n Pesquisas python=3.8")
        print("   conda activate Pesquisas")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return False
        
    except Exception as e:
        print(f"❌ Erro na verificação do Conda: {e}")
        print("\n🔧 USE: conda activate Pesquisas antes de executar este script")
        return False

# ---------------------------------------------------------------------
# VERIFICAÇÃO INICIAL DO AMBIENTE
# ---------------------------------------------------------------------
if platform.system() == "Windows":
    print("🔍 Verificando ambiente Conda 'Pesquisas'...")
    if not check_conda_environment():
        print("\n❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!")
        print("💡 Use o comando abaixo antes de executar este script:")
        print("   conda activate Pesquisas")
        sys.exit(1)
else:
    print("🔍 Sistema não-Windows detectado, pulando verificação do Conda...")

# ---------------------------------------------------------------------
# AGORA IMPORTAMOS AS DEPENDÊNCIAS (APÓS VERIFICAÇÃO DO CONDA)
# ---------------------------------------------------------------------
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Limpeza adicional para garantir
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-9", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Playwright: {e}")
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - PARA TUDO IMEDIATAMENTE"""
    global _should_stop, _stop_event, _pool
    
    print(f"\n!!! EMERGENCY STOP SOLICITADO !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando processos...")
    
    _should_stop = True
    
    # Sinalizar parada para todos os processos
    if _stop_event:
        _stop_event.set()
    
    # Parar pool AGressivamente
    if _pool:
        try:
            print("🛑 Terminando pool de workers...")
            _pool.terminate()
            _pool.join(timeout=2)
        except:
            pass
    
    # Terminar processos filhos de forma agressiva
    current_pid = os.getpid()
    try:
        parent = psutil.Process(current_pid)
        children = parent.children(recursive=True)
        print(f"🔪 Terminando {len(children)} processos filhos...")
        
        for child in children:
            try:
                child_pid = child.pid
                if child_pid != current_pid and child_pid in _active_processes:
                    child.kill()
                    _active_processes.discard(child_pid)
            except:
                pass
    except:
        pass
    
    # Limpeza final de processos órfãos
    kill_orphaned_chromium()
    
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    print("⚠️ PROGRAMA INTERROMPIDO PELO UTILIZADOR")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificação MAIS FREQUENTE de parada
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificação MAIS FREQUENTE de parada
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Verificação de parada DURANTE o carregamento
                        if stop_event.is_set():
                            break
                            
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Verificação de parada DURANTE a espera
                        if stop_event.is_set():
                            break
                            
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Verificação de parada ANTES do PDF
                        if stop_event.is_set():
                            break
                            
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        # Não reportar retry se foi por interrupção
                        if not stop_event.is_set():
                            msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1 and not stop_event.is_set():
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                # Se foi interrompido, sair imediatamente
                if stop_event.is_set():
                    break
                    
                if not success and not stop_event.is_set():
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                elif success:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        if not stop_event.is_set():
            msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 5 arquivos para feedback mais frequente
            if processed % 5 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop, _stop_event, _pool
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")
    
    # MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
    print("\n🔄 MÉTODO DE CONVERSÃO:")
    print("   • Playwright + Chromium headless")
    print("   • 1 instância do browser por processo worker")
    print("   • Contexto separado por arquivo HTML")
    print("   • Paralelismo seguro com multiprocessing.Pool")
    print("   • Sistema de retry com múltiplas tentativas")
    print("   • Timeouts configuráveis por página")
    print("   • INTERRUPÇÃO IMEDIATA via Ctrl+C (SIGINT)\n")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    _stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, _stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    _pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        _pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        print("💡 Dica: Pressione Ctrl+C a qualquer momento para PARAR IMEDIATAMENTE")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(_pool.imap_unordered(worker_wrapper_optimized, args_list)):
            # Verificação MAIS FREQUENTE de parada
            if _should_stop or _stop_event.is_set():
                print("🛑 Parada de emergência ativada durante o processamento!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificação de parada entre batches
            if _should_stop or _stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO POR TECLADO DETECTADA !!!")
        _should_stop = True
        _stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        _stop_event.set()
    finally:
        print("\n🧹 LIMPEZA FINAL EM ANDAMENTO...")
        
        # Sinalizar parada para todos
        _should_stop = True
        _stop_event.set()
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if _pool:
            try:
                print("🔪 Terminando pool de workers...")
                _pool.terminate()
            except:
                pass
            try:
                _pool.join(timeout=2)
            except:
                pass
        
        # Limpeza final agressiva
        print("🗑️  Limpando processos órfãos...")
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)
        print("✅ Limpeza concluída")

    # Relatório DETALHADO (apenas se não foi interrompido abruptamente)
    if not _should_stop or success_count > 0:
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL OTIMIZADO:")
        print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
        print(f" ❌ Falhas: {len(failed)}")
        
        if failed and not _should_stop:
            print("\n📋 Arquivos com falha (primeiros 10):")
            for fname, error in failed[:10]:
                print(f"   ‣ {fname}: {error}")
            if len(failed) > 10:
                print(f"   ... e mais {len(failed) - 10} falhas")
        
        if benchmark and success_count > 0 and elapsed > 0:
            rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
            rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
            print(f"⏱️  Tempo total: {elapsed:.1f}s")
            print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
            print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0 and not _should_stop


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=2, 
                       help="Número de processos (padrão: 2 otimizado para estabilidade)")
    parser.add_argument('--batch-size', type=int, default=3, 
                       help="Arquivos por batch (padrão: 3 para resposta rápida)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=50, help="Timeout por página (padrão: 50 segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO IMEDIATAMENTE !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 4)),  # Limite máximo de 4 workers para estabilidade
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL DETECTADA !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Principais Melhorias:

### 1. **Detecção do Conda no Início**
- A verificação do ambiente Conda é a **primeira coisa** que o script executa
- Se falhar no Windows, o script para **imediatamente** antes de importar qualquer dependência
- Mensagens claras de erro e instruções

### 2. **Importação do Playwright após Verificação**
- O Playwright só é importado **depois** da verificação bem-sucedida do ambiente Conda
- Evita o erro `ModuleNotFoundError` quando o ambiente está incorreto

### 3. **Timeout Padrão de 50 Segundos**
- Alterado de 45 para 50 segundos como solicitado:
```python
parser.add_argument('--timeout', type=int, default=50, help="Timeout por página (padrão: 50 segundos)")
```

### 4. **Estrutura Otimizada**
- **Código de verificação** → **Importações** → **Funções principais**
- Mantém a performance sem overhead desnecessário
- Preserva todas as otimizações anteriores

### 5. **Fluxo Corrigido**
1. Verifica Conda (apenas Windows)
2. Se falhar → Mensagem de erro → Sai do script
3. Se suceder → Importa Playwright → Continua execução normal

Agora o script irá:
- **Detectar corretamente** se você está no ambiente Conda "Pesquisas"
- **Parar imediatamente** com mensagem clara se não estiver
- **Continuar normalmente** se estiver no ambiente correto
- Usar **timeout de 50s** como padrão

---

### 👤 Utilizador *(2025-11-07 06:11:14)* *[deepseek-reasoner]*

(base) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>python comb_pdf_direct6_html_based_optimized_live_benchmark.py --benchmark
🔍 Verificando ambiente Conda 'Pesquisas'...
🔍 Ambiente Conda detectado: base
🔍 Ambiente ativo via conda info: base
❌ AMBIENTE CONDA 'PESQUISAS' NÃO DETECTADO!

🔧 USE O SEGUINTE COMANDO ANTES DE EXECUTAR:
   conda activate Pesquisas

💡 Se o ambiente não existir, crie com:
   conda create -n Pesquisas python=3.8
   conda activate Pesquisas
   pip install playwright psutil
   playwright install chromium

❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!
💡 Use o comando abaixo antes de executar este script:
   conda activate Pesquisas

(base) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>conda activate Pesquisas

(Pesquisas) D:\Downloads\_DOCS_\_DOCS_\Pesquisas__D_C_G_Qwen_Op>python comb_pdf_direct6_html_based_optimized_live_benchmark.py --benchmark
🔍 Verificando ambiente Conda 'Pesquisas'...
🔍 Ambiente Conda detectado: Pesquisas
✅ Ambiente Conda correto: Pesquisas
🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA
!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO IMEDIATAMENTE !!!
=================================================================
🔧 Workers: 2 (OTIMIZADO) | Batch: 3
🔄 Retry: 2 | Timeout: 50s
🧹 Limpando processos Chromium órfãos...
🎯 Encontrados 206 arquivos HTML
🔧 Workers: 2 | Batch: 3 | Timeout: 50s
🔄 Retry: 2 tentativas por arquivo
⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE

🔄 MÉTODO DE CONVERSÃO:
   • Playwright + Chromium headless
   • 1 instância do browser por processo worker
   • Contexto separado por arquivo HTML
   • Paralelismo seguro com multiprocessing.Pool
   • Sistema de retry com múltiplas tentativas
   • Timeouts configuráveis por página
   • INTERRUPÇÃO IMEDIATA via Ctrl+C (SIGINT)

🆕 85 arquivos novos para processar (de 206 total)
📦 29 batches preparados
🔍 Verificando ambiente Conda 'Pesquisas'...
🔍 Ambiente Conda detectado: Pesquisas
✅ Ambiente Conda correto: Pesquisas
🔄 Iniciando conversão OTIMIZADA...
💡 Dica: Pressione Ctrl+C a qualquer momento para PARAR IMEDIATAMENTE
🔍 Verificando ambiente Conda 'Pesquisas'...
🔍 Ambiente Conda detectado: Pesquisas
✅ Ambiente Conda correto: Pesquisas
🔍 Verificando ambiente Conda 'Pesquisas'...
🔍 Ambiente Conda detectado: Pesquisas
✅ Ambiente Conda correto: Pesquisas
✅ 116_Grok_Update_menuinst_for_Jupyter_Notebook.pdf
✅ 117_Grok_Abrir_Arquivos_Markdown_no_Windows.pdf
✅ 118_Grok_Windows_10_Support_Ends_2025.pdf  ; Porque Verificando ambiente Conda 'Pesquisas'.. aparece varias vezes?

---

### 🤖 DeepSeek *(2025-11-07 06:11:14)* *[deepseek-reasoner]*

O problema é que a verificação do ambiente Conda está sendo executada várias vezes porque o script é executado em múltiplos processos (devido ao uso de multiprocessing). Cada processo filho importa o script e executa o código no topo, incluindo a verificação do Conda.

Para corrigir isso, precisamos garantir que a verificação do Conda seja executada apenas no processo principal. Vamos reorganizar o código para que a verificação seja feita apenas quando o script é executado como principal e não quando é importado por um processo filho.

Além disso, note que a verificação do Conda está sendo feita no topo do script, mas também dentro da função `main` (que é chamada apenas no processo principal). A verificação no topo do script será executada em todos os processos, o que não é desejado.

Vamos remover a verificação do topo do script e deixar apenas na função `main`. Dessa forma, apenas o processo principal fará a verificação.

Outro ponto: a verificação do Conda deve ser feita apenas no Windows, então vamos manter a lógica dentro da função `main` e não no topo do script.

Vamos ajustar:

1. Remover a verificação do topo do script (o bloco que chama `check_conda_environment` e sai se falhar).
2. Manter a verificação dentro da função `main` (após a análise de argumentos) e antes de qualquer outra coisa.

Além disso, note que a função `check_conda_environment` está sendo chamada várias vezes porque cada processo filho (criado pelo multiprocessing) importa o módulo e, no Windows, o multiprocessing usa `spawn` que recria o ambiente do zero, então cada processo filho tentará verificar o Conda novamente.

Para evitar isso, podemos usar a proteção `if __name__ == "__main__":` para a verificação do Conda, mas note que a verificação deve ser feita apenas no processo principal, e não nos filhos.

Vamos mover a verificação para dentro de `main` e garantir que não seja executada nos processos filhos.

No entanto, os processos filhos não passam pela função `main`, então isso deve resolver.

Vamos reestruturar:

- Remover o código de verificação do topo do script (linhas 73-80).
- Manter a verificação dentro da função `main` (após `parse_args` e antes de qualquer outra coisa).

Além disso, note que a função `check_conda_environment` está sendo chamada em `main` apenas no Windows. Vamos manter isso.

Vamos fazer essas alterações e testar.

Outro ponto: o código de verificação do Conda no topo do script estava sendo executado mesmo quando o script era importado por um processo filho. Agora, ao mover para `main`, que é chamada apenas no processo principal, evitamos a verificação nos filhos.

Vamos também ajustar a mensagem de verificação para que não apareça múltiplas vezes.

Além disso, note que o multiprocessing no Windows usa a criação de processos via `spawn`, o que significa que cada processo filho vai importar o módulo novamente. Se houver código no topo do módulo que não esteja protegido por `if __name__ == "__main__":`, ele será executado novamente. Portanto, é importante proteger a execução do código no topo do módulo que não deve ser executado nos processos filhos.

No entanto, a verificação do Conda não é necessária nos processos filhos, apenas no principal.

Vamos remover a verificação do topo do script e colocar em `main`:

```python
# Remover este bloco (linhas 73-80):
#if platform.system() == "Windows":
#    print("🔍 Verificando ambiente Conda 'Pesquisas'...")
#    if not check_conda_environment():
#        print("\n❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!")
#        print("💡 Use o comando abaixo antes de executar este script:")
#        print("   conda activate Pesquisas")
#        sys.exit(1)
#else:
#    print("🔍 Sistema não-Windows detectado, pulando verificação do Conda...")
```

E na função `main`, após a análise de argumentos, adicionar a verificação:

```python
def main():
    # VERIFICAÇÃO DO AMBIENTE CONDA - APENAS NO WINDOWS
    if platform.system() == "Windows":
        print("🔍 Verificando ambiente Conda 'Pesquisas'...")
        if not check_conda_environment():
            print("\n❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!")
            print("💡 Use o comando abaixo antes de executar este script:")
            print("   conda activate Pesquisas")
            return 1

    # ... restante do código da main ...
```

Dessa forma, a verificação só ocorre no processo principal e apenas uma vez.

Vamos também ajustar o timeout padrão para 50 segundos, como solicitado.

Agora, vamos gerar o código completo com essas alterações. O problema é que a verificação do Conda está sendo executada múltiplas vezes porque o script está sendo importado/re-executado nos processos filhos do multiprocessing. Vou corrigir isso garantindo que a verificação só aconteça no processo principal:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento IMEDIATO E CONFIÁVEL via Ctrl+C
- Workers otimizados (2 padrão) e batch-size 3
- Browser management aprimorado
- Detecção de ambiente Conda "Pesquisas" (apenas no processo principal)
- Timeout padrão de 50 segundos
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção MELHORADO
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False
_stop_event = None
_pool = None

# ---------------------------------------------------------------------
# DETECÇÃO DO AMBIENTE CONDA - APENAS NO PROCESSO PRINCIPAL
# ---------------------------------------------------------------------
def check_conda_environment():
    """Verifica se o ambiente Conda 'Pesquisas' está ativo no Windows - APENAS NO PROCESSO PRINCIPAL"""
    if platform.system() != "Windows":
        return True  # Skip check on non-Windows systems
    
    try:
        # Método 1: Verificar variável de ambiente CONDA_DEFAULT_ENV (mais confiável)
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
        print(f"🔍 Ambiente Conda detectado: {conda_env}")
        
        if 'Pesquisas' in conda_env:
            print(f"✅ Ambiente Conda correto: {conda_env}")
            return True
        
        # Método 2: Verificar se estamos em qualquer ambiente conda (não base)
        if conda_env and conda_env != 'base':
            print(f"⚠️  Ambiente Conda detectado: {conda_env} (mas não é 'Pesquisas')")
            return False
        
        # Método 3: Tentar detectar via conda info
        try:
            result = subprocess.run(
                ['conda', 'info', '--json'], 
                capture_output=True, 
                text=True, 
                timeout=5,
                shell=True
            )
            if result.returncode == 0:
                import json
                conda_info = json.loads(result.stdout)
                active_env = conda_info.get('active_prefix_name', '')
                if active_env:
                    print(f"🔍 Ambiente ativo via conda info: {active_env}")
                    if 'Pesquisas' in active_env:
                        print(f"✅ Ambiente Conda correto: {active_env}")
                        return True
        except:
            pass
        
        # Se chegou aqui, não detectou o ambiente Pesquisas
        print("❌ AMBIENTE CONDA 'PESQUISAS' NÃO DETECTADO!")
        print("\n🔧 USE O SEGUINTE COMANDO ANTES DE EXECUTAR:")
        print("   conda activate Pesquisas")
        print("\n💡 Se o ambiente não existir, crie com:")
        print("   conda create -n Pesquisas python=3.8")
        print("   conda activate Pesquisas")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return False
        
    except Exception as e:
        print(f"❌ Erro na verificação do Conda: {e}")
        print("\n🔧 USE: conda activate Pesquisas antes de executar este script")
        return False

# ---------------------------------------------------------------------
# VERIFICAÇÃO INICIAL DO AMBIENTE - APENAS NO PROCESSO PRINCIPAL
# ---------------------------------------------------------------------
if __name__ == "__main__" and platform.system() == "Windows":
    print("🔍 Verificando ambiente Conda 'Pesquisas'...")
    if not check_conda_environment():
        print("\n❌ EXECUÇÃO INTERROMPIDA: Ambiente Conda 'Pesquisas' não está ativo!")
        print("💡 Use o comando abaixo antes de executar este script:")
        print("   conda activate Pesquisas")
        sys.exit(1)
elif __name__ == "__main__":
    print("🔍 Sistema não-Windows detectado, pulando verificação do Conda...")

# ---------------------------------------------------------------------
# AGORA IMPORTAMOS AS DEPENDÊNCIAS (APÓS VERIFICAÇÃO DO CONDA)
# ---------------------------------------------------------------------
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Limpeza adicional para garantir
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-9", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Playwright: {e}")
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - PARA TUDO IMEDIATAMENTE"""
    global _should_stop, _stop_event, _pool
    
    print(f"\n!!! EMERGENCY STOP SOLICITADO !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando processos...")
    
    _should_stop = True
    
    # Sinalizar parada para todos os processos
    if _stop_event:
        _stop_event.set()
    
    # Parar pool AGressivamente
    if _pool:
        try:
            print("🛑 Terminando pool de workers...")
            _pool.terminate()
            _pool.join(timeout=2)
        except:
            pass
    
    # Terminar processos filhos de forma agressiva
    current_pid = os.getpid()
    try:
        parent = psutil.Process(current_pid)
        children = parent.children(recursive=True)
        print(f"🔪 Terminando {len(children)} processos filhos...")
        
        for child in children:
            try:
                child_pid = child.pid
                if child_pid != current_pid and child_pid in _active_processes:
                    child.kill()
                    _active_processes.discard(child_pid)
            except:
                pass
    except:
        pass
    
    # Limpeza final de processos órfãos
    kill_orphaned_chromium()
    
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    print("⚠️ PROGRAMA INTERROMPIDO PELO UTILIZADOR")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificação MAIS FREQUENTE de parada
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificação MAIS FREQUENTE de parada
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Verificação de parada DURANTE o carregamento
                        if stop_event.is_set():
                            break
                            
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Verificação de parada DURANTE a espera
                        if stop_event.is_set():
                            break
                            
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Verificação de parada ANTES do PDF
                        if stop_event.is_set():
                            break
                            
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        # Não reportar retry se foi por interrupção
                        if not stop_event.is_set():
                            msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1 and not stop_event.is_set():
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                # Se foi interrompido, sair imediatamente
                if stop_event.is_set():
                    break
                    
                if not success and not stop_event.is_set():
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                elif success:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        if not stop_event.is_set():
            msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 5 arquivos para feedback mais frequente
            if processed % 5 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop, _stop_event, _pool
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")
    
    # MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
    print("\n🔄 MÉTODO DE CONVERSÃO:")
    print("   • Playwright + Chromium headless")
    print("   • 1 instância do browser por processo worker")
    print("   • Contexto separado por arquivo HTML")
    print("   • Paralelismo seguro com multiprocessing.Pool")
    print("   • Sistema de retry com múltiplas tentativas")
    print("   • Timeouts configuráveis por página")
    print("   • INTERRUPÇÃO IMEDIATA via Ctrl+C (SIGINT)\n")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    _stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, _stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    _pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        _pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        print("💡 Dica: Pressione Ctrl+C a qualquer momento para PARAR IMEDIATAMENTE")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(_pool.imap_unordered(worker_wrapper_optimized, args_list)):
            # Verificação MAIS FREQUENTE de parada
            if _should_stop or _stop_event.is_set():
                print("🛑 Parada de emergência ativada durante o processamento!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificação de parada entre batches
            if _should_stop or _stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO POR TECLADO DETECTADA !!!")
        _should_stop = True
        _stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        _stop_event.set()
    finally:
        print("\n🧹 LIMPEZA FINAL EM ANDAMENTO...")
        
        # Sinalizar parada para todos
        _should_stop = True
        _stop_event.set()
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if _pool:
            try:
                print("🔪 Terminando pool de workers...")
                _pool.terminate()
            except:
                pass
            try:
                _pool.join(timeout=2)
            except:
                pass
        
        # Limpeza final agressiva
        print("🗑️  Limpando processos órfãos...")
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)
        print("✅ Limpeza concluída")

    # Relatório DETALHADO (apenas se não foi interrompido abruptamente)
    if not _should_stop or success_count > 0:
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL OTIMIZADO:")
        print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
        print(f" ❌ Falhas: {len(failed)}")
        
        if failed and not _should_stop:
            print("\n📋 Arquivos com falha (primeiros 10):")
            for fname, error in failed[:10]:
                print(f"   ‣ {fname}: {error}")
            if len(failed) > 10:
                print(f"   ... e mais {len(failed) - 10} falhas")
        
        if benchmark and success_count > 0 and elapsed > 0:
            rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
            rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
            print(f"⏱️  Tempo total: {elapsed:.1f}s")
            print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
            print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0 and not _should_stop


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=2, 
                       help="Número de processos (padrão: 2 otimizado para estabilidade)")
    parser.add_argument('--batch-size', type=int, default=3, 
                       help="Arquivos por batch (padrão: 3 para resposta rápida)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=50, help="Timeout por página (padrão: 50 segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO IMEDIATAMENTE !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 4)),  # Limite máximo de 4 workers para estabilidade
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL DETECTADA !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Principais Correções:

### 1. **Verificação do Conda Apenas no Processo Principal**
```python
if __name__ == "__main__" and platform.system() == "Windows":
    print("🔍 Verificando ambiente Conda 'Pesquisas'...")
    if not check_conda_environment():
        # ... código de erro
```

### 2. **Proteção com `__name__ == "__main__"`**
- A verificação só acontece quando o script é executado diretamente
- Não acontece quando o script é importado por processos filhos do multiprocessing

### 3. **Mantém Todas as Otimizações Anteriores**
- Timeout padrão de 50 segundos
- Workers: 2, Batch-size: 3
- Sistema de interrupção robusto

### 4. **Fluxo Corrigido**
1. **Processo Principal**: Verifica Conda → Importa Playwright → Executa conversão
2. **Processos Filhos**: Pulam verificação do Conda → Importam Playwright → Processam batches

Agora a verificação do Conda aparecerá **apenas uma vez** no início, e os processos filhos não repetirão a verificação!

---

### 👤 Utilizador *(2025-11-07 06:25:44)* *[deepseek-reasoner]*

Funciona. Mas Por uma questão de eficiência solicito a remoção da detecção do ambiente conda. E assim voltar à versão anterior sem detecção. Fica responsabilidade do utilizador fazer isso.

---

### 🤖 DeepSeek *(2025-11-07 06:25:44)* *[deepseek-reasoner]*

Vamos remover a detecção do ambiente Conda e voltar à versão anterior, mas mantendo as outras otimizações (timeout 50, workers 2, batch-size 3, etc.).
 Além disso, vamos garantir que a importação do Playwright está no topo, pois não há mais a verificação do Conda que exigia a importação tardia. Aqui está a versão sem a detecção do ambiente Conda, voltando à versão anterior mais eficiente:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comb_pdf_direct6_html_based_optimized_live_benchmark.py

Versão ALTAMENTE OTIMIZADA com:
- Reutilização de instância do Chromium por processo
- Paralelismo seguro via multiprocessing.Pool
- Retry por arquivo (2 tentativas padrão)
- Cancelamento IMEDIATO E CONFIÁVEL via Ctrl+C
- Workers otimizados (2 padrão) e batch-size 3
- Browser management aprimorado
- Timeout padrão de 50 segundos
"""

import argparse
import multiprocessing
import sys
import time
import threading
import platform
import subprocess
import signal
import os
import psutil
from pathlib import Path
from typing import List, Tuple, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ---------------------------------------------------------------------
# Variáveis globais para controle de interrupção MELHORADO
# ---------------------------------------------------------------------
_active_processes = set()
_should_stop = False
_stop_event = None
_pool = None


# ---------------------------------------------------------------------
# Funções utilitárias OTIMIZADAS
# ---------------------------------------------------------------------
def kill_orphaned_chromium():
    """Encerra processos Chromium órfãos de forma agressiva."""
    try:
        print("🧹 Limpando processos Chromium órfãos...")
        current_pid = os.getpid()
        
        if platform.system() == "Windows":
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromium.exe", "/IM", "msedge.exe"],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        else:
            subprocess.run(["pkill", "-9", "-f", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "chrome"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-9", "-f", "playwright"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        # Limpeza adicional para garantir
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-9", "chromium"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Aviso na limpeza: {e}")


def chunkify(seq: List[str], size: int) -> List[List[str]]:
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def check_playwright_available(headless_test: bool = True) -> bool:
    """Verifica se o Playwright + Chromium estão instalados."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_test,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            browser.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Playwright: {e}")
        return False


def emergency_stop_handler(signum, frame):
    """Handler de emergência para Ctrl+C - PARA TUDO IMEDIATAMENTE"""
    global _should_stop, _stop_event, _pool
    
    print(f"\n!!! EMERGENCY STOP SOLICITADO !!!")
    print(f"🚨 INTERRUPÇÃO DE EMERGÊNCIA - Terminando processos...")
    
    _should_stop = True
    
    # Sinalizar parada para todos os processos
    if _stop_event:
        _stop_event.set()
    
    # Parar pool AGressivamente
    if _pool:
        try:
            print("🛑 Terminando pool de workers...")
            _pool.terminate()
            _pool.join(timeout=2)
        except:
            pass
    
    # Terminar processos filhos de forma agressiva
    current_pid = os.getpid()
    try:
        parent = psutil.Process(current_pid)
        children = parent.children(recursive=True)
        print(f"🔪 Terminando {len(children)} processos filhos...")
        
        for child in children:
            try:
                child_pid = child.pid
                if child_pid != current_pid and child_pid in _active_processes:
                    child.kill()
                    _active_processes.discard(child_pid)
            except:
                pass
    except:
        pass
    
    # Limpeza final de processos órfãos
    kill_orphaned_chromium()
    
    print("💀 TODOS OS PROCESSOS FORAM TERMINADOS")
    print("⚠️ PROGRAMA INTERROMPIDO PELO UTILIZADOR")
    os._exit(1)  # Saída de emergência


# ---------------------------------------------------------------------
# Worker de processamento OTIMIZADO - REUTILIZA BROWSER POR PROCESSO
# ---------------------------------------------------------------------
def worker_process_batch_optimized(batch_files, pdf_dir, timeout, headless, force_overwrite, retry_count, stop_event, msg_queue):
    """Worker OTIMIZADO que reutiliza uma instância do Chromium por processo"""
    my_pid = os.getpid()
    _active_processes.add(my_pid)
    
    try:
        results = []
        out_dir = Path(pdf_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Verificar parada ANTES de iniciar o browser
        if stop_event.is_set():
            return []

        with sync_playwright() as p:
            # Configuração OTIMIZADA do browser - UMA INSTÂNCIA POR PROCESSO
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-extensions'
                ]
            )
            
            for html_path_str in batch_files:
                # Verificação MAIS FREQUENTE de parada
                if stop_event.is_set():
                    break
                    
                html_path = Path(html_path_str)
                pdf_path = out_dir / f"{html_path.stem}.pdf"

                if pdf_path.exists() and not force_overwrite:
                    results.append((html_path_str, True, "Já existe"))
                    msg_queue.put(("skip", f"{html_path.name}"))
                    continue

                success = False
                last_error = ""
                context = None
                
                for attempt in range(retry_count):
                    # Verificação MAIS FREQUENTE de parada
                    if stop_event.is_set():
                        break
                        
                    try:
                        # NOVO CONTEXT por arquivo (mas mesmo browser)
                        context = browser.new_context(
                            viewport={'width': 1920, 'height': 1080},
                            ignore_https_errors=True
                        )
                        page = context.new_page()
                        
                        # Timeouts otimizados
                        page.set_default_timeout(timeout * 1000)
                        page.set_default_navigation_timeout(timeout * 1000)
                        
                        full_path = f"file:///{html_path.absolute()}"
                        page.goto(full_path, wait_until='networkidle', timeout=timeout * 1000)
                        
                        # Verificação de parada DURANTE o carregamento
                        if stop_event.is_set():
                            break
                            
                        # Wait for complete load - MAIS CONFIÁVEL
                        page.wait_for_function(
                            'document.readyState === "complete"',
                            timeout=timeout * 1000
                        )
                        
                        # Verificação de parada DURANTE a espera
                        if stop_event.is_set():
                            break
                            
                        # Pequena espera para conteúdo dinâmico
                        page.wait_for_timeout(500)
                        
                        # Verificação de parada ANTES do PDF
                        if stop_event.is_set():
                            break
                            
                        # Geração de PDF com configurações OTIMIZADAS
                        page.pdf(
                            path=str(pdf_path),
                            format='A4',
                            print_background=True,
                            margin={'top': '0.5in', 'bottom': '0.5in', 'left': '0.5in', 'right': '0.5in'},
                            prefer_css_page_size=True,
                            display_header_footer=False,
                            scale=1.0
                        )
                        
                        success = True
                        msg_queue.put(("ok", pdf_path.name))
                        break
                        
                    except Exception as e:
                        last_error = str(e)
                        # Não reportar retry se foi por interrupção
                        if not stop_event.is_set():
                            msg_queue.put(("retry", f"{html_path.name} (tentativa {attempt + 1}/{retry_count}): {e}"))
                        if attempt < retry_count - 1 and not stop_event.is_set():
                            time.sleep(1)  # Pequena pausa entre tentativas
                    finally:
                        if context:
                            try:
                                context.close()
                            except:
                                pass

                # Se foi interrompido, sair imediatamente
                if stop_event.is_set():
                    break
                    
                if not success and not stop_event.is_set():
                    msg_queue.put(("fail", f"{html_path.name}: {last_error}"))
                    results.append((html_path_str, False, last_error))
                elif success:
                    results.append((html_path_str, True, "Sucesso"))

            # Fechar browser ao final do batch
            try:
                browser.close()
            except:
                pass
                
    except Exception as e:
        if not stop_event.is_set():
            msg_queue.put(("error", f"Erro no worker: {e}"))
    finally:
        _active_processes.discard(my_pid)
    
    return results


def worker_wrapper_optimized(args):
    """Wrapper para o worker otimizado"""
    try:
        return worker_process_batch_optimized(*args)
    except Exception as e:
        return []


# ---------------------------------------------------------------------
# Listener de mensagens APRIMORADO
# ---------------------------------------------------------------------
def queue_listener_optimized(msg_queue, listener_stop_flag, total_files):
    """Listener com barra de progresso e estatísticas"""
    start_time = time.time()
    processed = 0
    successes = 0
    skips = 0
    failures = 0
    
    while not listener_stop_flag.is_set():
        try:
            obj = msg_queue.get(timeout=0.1)
            if obj is None:
                break
            typ, text = obj
            processed += 1
            
            if typ == "ok":
                successes += 1
                print(f"✅ {text}")
            elif typ == "skip":
                skips += 1
                print(f"⏭️ {text}")
            elif typ == "fail":
                failures += 1
                print(f"❌ {text}")
            elif typ == "error":
                failures += 1
                print(f"🚫 {text}")
            elif typ == "retry":
                print(f"🔄 {text}")
            
            # Mostrar progresso a cada 5 arquivos para feedback mais frequente
            if processed % 5 == 0 or processed == total_files:
                elapsed = time.time() - start_time
                if successes > 0 and elapsed > 0:
                    rate = successes / (elapsed / 60)
                    print(f"📊 Progresso: {successes+skips+failures}/{total_files} | "
                          f"✅{successes} ⏭️{skips} ❌{failures} | "
                          f"{rate:.1f} PDFs/min")
                        
        except:
            continue


# ---------------------------------------------------------------------
# Conversão principal - VERSÃO ALTAMENTE OTIMIZADA
# ---------------------------------------------------------------------
def generate_pdfs_optimized(source_dir, output_dir, workers, batch_size, headless, timeout,
                           force_overwrite, dry_run, single_file=None, retry_count=2, benchmark=False):
    """Função principal OTIMIZADA com interrupção robusta e performance máxima"""
    global _should_stop, _stop_event, _pool
    
    src = Path(source_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if single_file:
        html_files = [str(src / single_file)]
        if not Path(html_files[0]).exists():
            print(f"❌ Arquivo não encontrado: {single_file}")
            return False
    else:
        html_files = sorted([str(p) for p in src.glob("*.html")])

    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado.")
        return False

    print(f"🎯 Encontrados {len(html_files)} arquivos HTML")
    print(f"🔧 Workers: {workers} | Batch: {batch_size} | Timeout: {timeout}s")
    print(f"🔄 Retry: {retry_count} tentativas por arquivo")
    print(f"⏹️  Pressione Ctrl+C para PARAR IMEDIATAMENTE")
    
    # MOSTRAR MÉTODO DE CONVERSÃO UTILIZADO
    print("\n🔄 MÉTODO DE CONVERSÃO:")
    print("   • Playwright + Chromium headless")
    print("   • 1 instância do browser por processo worker")
    print("   • Contexto separado por arquivo HTML")
    print("   • Paralelismo seguro com multiprocessing.Pool")
    print("   • Sistema de retry com múltiplas tentativas")
    print("   • Timeouts configuráveis por página")
    print("   • INTERRUPÇÃO IMEDIATA via Ctrl+C (SIGINT)\n")

    if dry_run:
        print("🧪 MODO SIMULAÇÃO - Nenhum arquivo será criado")
        for f in html_files[:5]:
            print(f"   📄 {Path(f).name}")
        if len(html_files) > 5:
            print(f"   ... e mais {len(html_files) - 5} arquivos")
        return True

    if not force_overwrite:
        original_count = len(html_files)
        html_files = [f for f in html_files if not (out / f"{Path(f).stem}.pdf").exists()]
        print(f"🆕 {len(html_files)} arquivos novos para processar (de {original_count} total)")

    if not html_files:
        print("✅ Nenhum arquivo novo para processar")
        return True

    batches = chunkify(html_files, batch_size)
    print(f"📦 {len(batches)} batches preparados")

    # Sistema de comunicação OTIMIZADO
    manager = multiprocessing.Manager()
    _stop_event = manager.Event()
    msg_queue = manager.Queue()
    listener_stop_flag = threading.Event()
    
    # Listener COM ESTATÍSTICAS
    listener_thread = threading.Thread(
        target=queue_listener_optimized, 
        args=(msg_queue, listener_stop_flag, len(html_files)), 
        daemon=True
    )
    listener_thread.start()

    # Preparar argumentos
    args_list = [
        (batch, str(out), timeout, headless, force_overwrite, retry_count, _stop_event, msg_queue) 
        for batch in batches
    ]

    success_count, failed = 0, []
    _pool = None
    start_time = time.time()

    try:
        # Criar pool com número OTIMIZADO de workers
        _pool = multiprocessing.Pool(processes=workers)
        
        print("🔄 Iniciando conversão OTIMIZADA...")
        print("💡 Dica: Pressione Ctrl+C a qualquer momento para PARAR IMEDIATAMENTE")
        
        # Processar batches - com verificação CONSTANTE de parada
        for i, result in enumerate(_pool.imap_unordered(worker_wrapper_optimized, args_list)):
            # Verificação MAIS FREQUENTE de parada
            if _should_stop or _stop_event.is_set():
                print("🛑 Parada de emergência ativada durante o processamento!")
                break
                
            # Relatório de progresso por batch
            batch_progress = f"📦 Batch {i+1}/{len(batches)} processado"
            if len(result) > 0:
                batch_success = sum(1 for _, success, _ in result if success)
                batch_progress += f" - ✅ {batch_success}/{len(result)}"
            print(batch_progress)
            
            for html_file, success, msg in result:
                if success:
                    success_count += 1
                else:
                    failed.append((Path(html_file).name, msg))
                    
            # Verificação de parada entre batches
            if _should_stop or _stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO POR TECLADO DETECTADA !!!")
        _should_stop = True
        _stop_event.set()
    except Exception as e:
        print(f"Erro no pool principal: {e}")
        _stop_event.set()
    finally:
        print("\n🧹 LIMPEZA FINAL EM ANDAMENTO...")
        
        # Sinalizar parada para todos
        _should_stop = True
        _stop_event.set()
        
        # Parar listener
        listener_stop_flag.set()
        try:
            msg_queue.put(None)
        except:
            pass
        listener_thread.join(timeout=1.0)
        
        # Terminar pool AGressivamente
        if _pool:
            try:
                print("🔪 Terminando pool de workers...")
                _pool.terminate()
            except:
                pass
            try:
                _pool.join(timeout=2)
            except:
                pass
        
        # Limpeza final agressiva
        print("🗑️  Limpando processos órfãos...")
        kill_orphaned_chromium()
        
        # Pequena pausa para garantir que tudo foi limpo
        time.sleep(1)
        print("✅ Limpeza concluída")

    # Relatório DETALHADO (apenas se não foi interrompido abruptamente)
    if not _should_stop or success_count > 0:
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL OTIMIZADO:")
        print(f" ✅ Sucessos: {success_count}/{len(html_files)}")
        print(f" ❌ Falhas: {len(failed)}")
        
        if failed and not _should_stop:
            print("\n📋 Arquivos com falha (primeiros 10):")
            for fname, error in failed[:10]:
                print(f"   ‣ {fname}: {error}")
            if len(failed) > 10:
                print(f"   ... e mais {len(failed) - 10} falhas")
        
        if benchmark and success_count > 0 and elapsed > 0:
            rate_total = len(html_files) / (elapsed / 60) if elapsed > 0 else 0
            rate_success = success_count / (elapsed / 60) if elapsed > 0 else 0
            print(f"⏱️  Tempo total: {elapsed:.1f}s")
            print(f"📈 Taxa: {rate_total:.1f} PDFs/min (total)")
            print(f"📈 Taxa: {rate_success:.1f} PDFs/min (sucessos)")
    
    return success_count > 0 and not _should_stop


# ---------------------------------------------------------------------
# CLI OTIMIZADA
# ---------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Conversão HTML → PDF ALTAMENTE OTIMIZADA com INTERRUPÇÃO IMEDIATA"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', help="Sobrescreve PDFs já existentes")
    group.add_argument('--only-new', action='store_true', default=True, help="Apenas novos (padrão)")

    parser.add_argument('--dry-run', action='store_true', help="Simula sem criar arquivos")
    parser.add_argument('--source', default="combined_html", help="Pasta com arquivos .html")
    parser.add_argument('--output', default="combined_pdfs", help="Pasta de saída para PDFs")
    parser.add_argument('--workers', type=int, default=2, 
                       help="Número de processos (padrão: 2 otimizado para estabilidade)")
    parser.add_argument('--batch-size', type=int, default=3, 
                       help="Arquivos por batch (padrão: 3 para resposta rápida)")
    parser.add_argument('--no-headless', action='store_true', help="Mostra navegador (debug)")
    parser.add_argument('--single-file', type=str, help="Converte apenas um arquivo HTML específico")
    parser.add_argument('--timeout', type=int, default=50, help="Timeout por página (padrão: 50 segundos)")
    parser.add_argument('--retry-count', type=int, default=2, help="Tentativas por arquivo (padrão: 2)")
    parser.add_argument('--benchmark', action='store_true', help="Mostra tempo total e PDFs/minuto")
    return parser.parse_args()


# ---------------------------------------------------------------------
# Main OTIMIZADA
# ---------------------------------------------------------------------
def main():
    # Configurar handler de EMERGÊNCIA para Ctrl+C
    signal.signal(signal.SIGINT, emergency_stop_handler)
    
    args = parse_args()
    
    print("🚀 PDF GENERATOR - VERSÃO ALTAMENTE OTIMIZADA")
    print("!!! EMERGENCY STOP ENABLED - Ctrl+C para PARAR TUDO IMEDIATAMENTE !!!")
    print("=" * 65)
    print(f"🔧 Workers: {args.workers} (OTIMIZADO) | Batch: {args.batch_size}")
    print(f"🔄 Retry: {args.retry_count} | Timeout: {args.timeout}s")

    # Limpeza inicial agressiva
    kill_orphaned_chromium()

    # Verificações
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Pasta não encontrada: {source_dir}")
        return 1

    if not check_playwright_available(headless_test=not args.no_headless):
        print("❌ Playwright não disponível.")
        print("   pip install playwright psutil")
        print("   playwright install chromium")
        return 1

    # Executar versão OTIMIZADA
    success = generate_pdfs_optimized(
        source_dir=str(args.source),
        output_dir=str(args.output),
        workers=max(1, min(args.workers, 4)),  # Limite máximo de 4 workers para estabilidade
        batch_size=max(1, args.batch_size),
        headless=not args.no_headless,
        timeout=max(15, args.timeout),
        force_overwrite=args.force,
        dry_run=args.dry_run,
        single_file=args.single_file,
        retry_count=max(1, args.retry_count),
        benchmark=args.benchmark
    )

    # Resultado final
    if args.dry_run:
        print("🧪 SIMULAÇÃO CONCLUÍDA")
        return 0
    elif success:
        print("🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        return 0
    else:
        print("⚠️ CONVERSÃO INTERROMPIDA OU COM FALHAS")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Handler global para garantir que Ctrl+C sempre funcione
    original_sigint = signal.getsignal(signal.SIGINT)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n!!! INTERRUPÇÃO GLOBAL DETECTADA !!!")
        emergency_stop_handler(None, None)
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        sys.exit(1)
    finally:
        # Restaurar handler original
        signal.signal(signal.SIGINT, original_sigint)
```

## Principais Mudanças:

### 1. **Remoção Completa da Detecção do Conda**
- Eliminada toda a lógica de verificação do ambiente Conda
- Removidas as funções `check_conda_environment()`
- Removidas as verificações iniciais do ambiente

### 2. **Importação do Playwright no Topo**
- O Playwright é importado normalmente no início do arquivo
- Sem overhead de importação tardia
- Mais simples e eficiente

### 3. **Mantém Todas as Otimizações**
- Timeout padrão de 50 segundos
- Workers: 2, Batch-size: 3
- Sistema de interrupção robusto via Ctrl+C
- Reutilização de instância do Chromium por processo
- Paralelismo seguro com multiprocessing.Pool
- Sistema de retry (2 tentativas)

### 4. **Responsabilidade do Utilizador**
- Cabe ao utilizador garantir que está no ambiente correto
- Mensagem clara se o Playwright não estiver disponível
- Instruções de instalação mantidas

Agora o script é mais eficiente e direto, sem verificações desnecessárias, mantendo toda a funcionalidade e performance das versões anteriores!

---

*Conversa exportada do DeepSeek*
*Processado em: 23/11/2025 14:36*