import json
import re

with open('SwSL_Reviewer_Response_Pipeline_FIXED_(1).ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"Initial cells count: {len(cells)}")

# 1. Fix Cell 3 (Drive Mount)
cell3_src = "".join(cells[3]['source'])
cell3_fixed = """try:
    from google.colab import drive
    drive.mount('/content/drive')
    IN_COLAB = True
    print("Google Drive mounted successfully.")
except Exception as e:
    print(f"Running locally / outside Google Colab ({type(e).__name__}); skipping Drive mount.")
    IN_COLAB = False
"""
cells[3]['source'] = [line + '\n' for line in cell3_fixed.splitlines()]

# 2. Fix Cell 5 (Paths & Configuration)
cell5_src = "".join(cells[5]['source'])
# Replace the hardcoded paths section in Cell 5
old_paths_pat = r"DRIVE_ROOT\s*=\s*'/content/drive/MyDrive'[\s\S]*?RUN_DIR\s*=\s*f'\{PROJECT_DIR\}/runs'"
new_paths = """IN_COLAB = ('google.colab' in sys.modules) or os.path.exists('/content')
if IN_COLAB:
    DRIVE_ROOT   = '/content/drive/MyDrive'
    DRIVE_ZIP    = None
    DRIVE_FOLDER = f'{DRIVE_ROOT}/Sw/raw_videos'
    LOCAL_VIDEOS = '/content/raw_videos'
    PROJECT_DIR  = f'{DRIVE_ROOT}/SwSL_JCTA_Revision'
    OUT_DIR      = '/content/outputs'
    CACHE_DIR    = f'{PROJECT_DIR}/landmark_cache'
    FRAME_CACHE  = '/content/frame_cache'
    RUN_DIR      = f'{PROJECT_DIR}/runs'
    CKPT_DIR     = '/content/ckpt'
else:
    BASE_DIR     = Path('/Volumes/MacX/Sw').resolve() if os.path.exists('/Volumes/MacX/Sw') else Path.cwd()
    DRIVE_ROOT   = str(BASE_DIR)
    DRIVE_ZIP    = None
    DRIVE_FOLDER = str(BASE_DIR / 'raw_videos')
    LOCAL_VIDEOS = str(BASE_DIR / 'raw_videos')
    PROJECT_DIR  = str(BASE_DIR / 'SwSL_JCTA_Revision')
    OUT_DIR      = str(BASE_DIR / 'outputs')
    CACHE_DIR    = str(BASE_DIR / 'landmark_cache')
    FRAME_CACHE  = str(BASE_DIR / 'frame_cache')
    RUN_DIR      = str(BASE_DIR / 'runs')
    CKPT_DIR     = str(BASE_DIR / 'ckpt')"""

if re.search(old_paths_pat, cell5_src):
    cell5_src = re.sub(old_paths_pat, new_paths, cell5_src)
    print("Successfully patched paths in Cell 5.")
else:
    print("WARNING: Could not find old paths pattern in Cell 5.")

cells[5]['source'] = [line + '\n' for line in cell5_src.splitlines()]

# Let's inspect cells to delete
# Cell 6 is 'BALANCE_PER_SIGNER = 60'
# Cell 7 is '```markdown'
# Cell 8 is 'try: from google.colab import drive ...'
# Let's verify what cells 6, 7, 8 are:
print(f"Cell 6 first line: {''.join(cells[6]['source'])[:40]}")
print(f"Cell 7 first line: {''.join(cells[7]['source'])[:40]}")
print(f"Cell 8 first line: {''.join(cells[8]['source'])[:40]}")

# We will construct new_cells list
