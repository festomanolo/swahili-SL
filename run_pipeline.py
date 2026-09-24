import sys
import os
import time
import datetime
import traceback
import nbformat
from nbclient import NotebookClient

NOTEBOOK_PATH = '/Volumes/MacX/Sw/SwSL_Reviewer_Response_Pipeline_FIXED_(1).ipynb'
LOG_PATH = '/Volumes/MacX/Sw/pipeline_execution.log'

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(formatted + '\n')
        f.flush()

class StreamingNotebookClient(NotebookClient):
    def output(self, outs, msg, display_id, cell_index):
        out = super().output(outs, msg, display_id, cell_index)
        if out and out.get('output_type') == 'stream':
            text = out.get('text', '')
            for line in text.splitlines():
                if line.strip():
                    log(f"  [stdout] {line}")
        elif out and out.get('output_type') == 'error':
            log(f"  [error] {out.get('ename')}: {out.get('evalue')}")
        return out

def main():
    start_cell = 0
    end_cell = None
    if len(sys.argv) > 1:
        start_cell = int(sys.argv[1])
    if len(sys.argv) > 2:
        end_cell = int(sys.argv[2])

    log(f"Starting SwSL pipeline execution from cell {start_cell} to {end_cell or 'END'}")
    log(f"Notebook: {NOTEBOOK_PATH}")
    log(f"Python: {sys.executable}")

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    total_cells = len(nb.cells)
    log(f"Total cells in notebook: {total_cells}")

    client = StreamingNotebookClient(nb, timeout=None, kernel_name='python3', record_timing=True)
    
    with client.setup_kernel():
        for i, cell in enumerate(nb.cells):
            if i < start_cell:
                continue
            if end_cell is not None and i >= end_cell:
                log(f"Reached end_cell limit {end_cell}. Stopping.")
                break

            ctype = cell.cell_type
            src = cell.source.strip()
            first_line = src.split('\n')[0] if src else '(empty)'
            
            if ctype == 'markdown':
                if first_line.startswith('#'):
                    log(f"--- [Cell {i:2d}/{total_cells}] {first_line}")
                continue

            log(f"=== [Cell {i:2d}/{total_cells} CODE] Running: {first_line[:65]}...")
            t0 = time.time()
            try:
                client.execute_cell(cell, i)
                elapsed = time.time() - t0
                
                # Check for errors in outputs
                has_error = False
                error_msg = ""
                for out in cell.get('outputs', []):
                    if out.output_type == 'error':
                        has_error = True
                        error_msg = f"{out.ename}: {out.evalue}"
                
                if has_error:
                    log(f"FAILED Cell {i} in {elapsed:.1f}s: {error_msg}")
                    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                        nbformat.write(nb, f)
                    sys.exit(1)
                else:
                    log(f"COMPLETED Cell {i} in {elapsed:.1f}s")
                    
                # Save notebook state after each successful cell
                with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                    nbformat.write(nb, f)
                    
            except Exception as e:
                elapsed = time.time() - t0
                log(f"EXCEPTION in Cell {i} after {elapsed:.1f}s: {type(e).__name__}: {e}")
                traceback.print_exc()
                with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                    nbformat.write(nb, f)
                sys.exit(1)

    log("Pipeline run finished successfully!")

if __name__ == '__main__':
    main()
