import json
import re

with open('SwSL_Reviewer_Response_Pipeline_FIXED_(1).ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

old_cells = nb['cells']
print(f"Old cell count: {len(old_cells)}")

new_cells = []

# Map of transformations by examining each cell
for idx, cell in enumerate(old_cells):
    ctype = cell['cell_type']
    src = "".join(cell.get('source', []))

    # Skip redundant Cell 6: '# Ensure BALANCE_PER_SIGNER is explicitly defined'
    if '# Ensure BALANCE_PER_SIGNER is explicitly defined' in src:
        print(f"Removing duplicate Cell {idx}: BALANCE_PER_SIGNER")
        continue

    # Skip stray Cell 7: '```markdown'
    if src.strip().startswith('```markdown'):
        print(f"Removing stray markdown Cell {idx}")
        continue

    # Skip duplicate Cell 8: 'try:\n    from google.colab import drive ... Could not locate a real dataset. Generating dummy mock videos'
    if 'Generating dummy mock videos for pipeline verification' in src:
        print(f"Removing duplicate mock-data Cell {idx}")
        continue

    # Skip redundant Cell 15: 'print(\'Paths of videos in the `inv` dataframe:\')'
    if "print('Paths of videos in the `inv` dataframe:')" in src:
        print(f"Removing debug Cell {idx}: Paths of videos")
        continue

    # Skip redundant Cell 40: "best_bl_model_name = conv.loc[conv['Best val accuracy (%)'].idxmax()]['Model']"
    if "best_bl_model_name = conv.loc[conv['Best val accuracy (%)'].idxmax()]['Model']" in src:
        print(f"Removing debug Cell {idx}: best_bl_model_name snippet")
        continue

    # Fix Cell 45: accidently markdown with code "CV = {}"
    if ctype == 'markdown' and 'CV = {}' in src and 'if RUN_CROSS_VALIDATION:' in src:
        print(f"Fixing Cell {idx}: restoring Section 18 markdown header")
        cell['source'] = [
            "## 18. Repeated cross-validation — **Reviewer A comment 9**\n",
            "\n",
            "The reviewer's point is that a single train/val/test split may favour one model by chance.\n",
            "This section runs repeated stratified $k$-fold cross-validation on the original clips\n",
            "(augmenting each fold's training set independently) for the proposed model, the strongest\n",
            "baseline and the unablated reference.\n"
        ]
        new_cells.append(cell)
        continue

    # Skip duplicate Cell 49: "print('Executing the ablation study cell to populate ABL_PERCLASS and ABL.')"
    if "print('Executing the ablation study cell to populate ABL_PERCLASS and ABL.')" in src:
        print(f"Removing duplicate ablation Cell {idx}")
        continue

    # Fix Cell 3: Drive mount
    if 'from google.colab import drive' in src and 'drive.mount(' in src and 'IN_COLAB' not in src:
        print(f"Patching Cell {idx}: Google Drive mount safe check")
        cell['source'] = [
            "try:\n",
            "    from google.colab import drive\n",
            "    drive.mount('/content/drive')\n",
            "    IN_COLAB = True\n",
            "    print('Google Drive mounted successfully.')\n",
            "except Exception as e:\n",
            "    print(f'Running locally / outside Google Colab ({type(e).__name__}); skipping Drive mount.')\n",
            "    IN_COLAB = False\n"
        ]
        new_cells.append(cell)
        continue

    # Fix Cell 5: Configuration paths
    if "PRESET = 'standard'" in src and "DRIVE_ROOT" in src:
        print(f"Patching Cell {idx}: Configuration paths and environment detection")
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
        src = re.sub(old_paths_pat, new_paths, src)
        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Fix Section 4: remove redundant fallback preamble in Cell 14
    if "# --- Robust configurations fallbacks if Section 2 was skipped ---" in src:
        print(f"Patching Cell {idx}: Section 4 inventory fallback preamble")
        src = src.replace("OUT_DIR = globals().get('OUT_DIR', '/content/outputs')",
                          "BASE_DIR = Path('/Volumes/MacX/Sw').resolve() if os.path.exists('/Volumes/MacX/Sw') else Path.cwd()\nOUT_DIR = globals().get('OUT_DIR', str(BASE_DIR / 'outputs'))")
        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Fix Section 5 (Landmark Extraction): Enable native MediaPipe holistic direct execution
    if "MP_ENV_DIR   =" in src and "_LegacyHolistic" in src:
        print(f"Patching Cell {idx}: Landmark extraction native MediaPipe support")
        # Add native check right before _mp_env_healthy
        native_mp_code = """
_USE_NATIVE_MP = False
try:
    import mediapipe as _mp_test
    if hasattr(_mp_test, 'solutions') and hasattr(_mp_test.solutions, 'holistic'):
        _USE_NATIVE_MP = True
        print(f'Using native MediaPipe {_mp_test.__version__} with solutions.holistic')
except Exception:
    _USE_NATIVE_MP = False

if not _USE_NATIVE_MP:
    if not _mp_env_healthy():
        _mp_build_env()
    with open(MP_SCRIPT, 'w') as _f:          # always refresh the worker script
        _f.write(_MP_WORKER_SRC)
    _MP_CONST = json.load(open(MP_CONSTS))
"""
        src = re.sub(r'if not _mp_env_healthy\(\):[\s\S]*?_MP_CONST = json\.load\(open\(MP_CONSTS\)\)',
                     native_mp_code.strip(), src)

        # In mp_holistic assignment:
        ns_code = """
if _USE_NATIVE_MP:
    mp_holistic = mp.solutions.holistic
    mp_drawing  = mp.solutions.drawing_utils
else:
    mp_holistic = types.SimpleNamespace(
        Holistic=_LegacyHolistic,
        POSE_CONNECTIONS=frozenset(tuple(c) for c in _MP_CONST['pose']),
        HAND_CONNECTIONS=frozenset(tuple(c) for c in _MP_CONST['hand']))
    mp_drawing = types.SimpleNamespace(DrawingSpec=DrawingSpec, draw_landmarks=draw_landmarks)
"""
        src = re.sub(r'mp_holistic = types\.SimpleNamespace\([\s\S]*?mp_drawing = types\.SimpleNamespace\(DrawingSpec=DrawingSpec, draw_landmarks=draw_landmarks\)',
                     ns_code.strip(), src)

        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Fix Section 11 (Model Zoo): Add SafeGlobalAveragePooling1D and SafeGlobalMaxPooling1D
    if "class TemporalAttention(layers.Layer):" in src and "def build_proposed" in src:
        print(f"Patching Cell {idx}: SafeGlobalAveragePooling1D and SafeGlobalMaxPooling1D")
        safe_pool_classes = """
@_reg(package='swsl')
class SafeGlobalAveragePooling1D(layers.Layer):
    \"\"\"Mask-aware GlobalAveragePooling1D preventing 0/0 division when all frames are masked.\"\"\"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.supports_masking = True

    def call(self, inputs, mask=None):
        if mask is not None:
            mask_cast = tf.cast(mask, inputs.dtype)
            mask_exp = tf.expand_dims(mask_cast, -1)
            sum_val = tf.reduce_sum(inputs * mask_exp, axis=1)
            count = tf.reduce_sum(mask_exp, axis=1)
            safe_count = tf.maximum(count, 1.0)
            return sum_val / safe_count
        return tf.reduce_mean(inputs, axis=1)

    def compute_mask(self, inputs, mask=None):
        return None

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])

@_reg(package='swsl')
class SafeGlobalMaxPooling1D(layers.Layer):
    \"\"\"Mask-aware GlobalMaxPooling1D safely handling masked frames.\"\"\"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.supports_masking = True

    def call(self, inputs, mask=None):
        if mask is not None:
            mask_exp = tf.expand_dims(mask, -1)
            inputs_masked = tf.where(mask_exp, inputs, -1e9)
            res = tf.reduce_max(inputs_masked, axis=1)
            return tf.where(tf.equal(res, -1e9), 0.0, res)
        return tf.reduce_max(inputs, axis=1)

    def compute_mask(self, inputs, mask=None):
        return None

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])
"""
        # Insert safe pooling classes before build_proposed
        idx_bp = src.find("def build_proposed")
        src = src[:idx_bp] + safe_pool_classes + "\n" + src[idx_bp:]

        # In build_proposed, use SafeGlobalAveragePooling1D and SafeGlobalMaxPooling1D
        src = src.replace("layers.GlobalAveragePooling1D(name='mean_pool')(x)",
                          "SafeGlobalAveragePooling1D(name='mean_pool')(x)")
        src = src.replace("layers.GlobalMaxPooling1D(name='max_pool')(x)",
                          "SafeGlobalMaxPooling1D(name='max_pool')(x)")

        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Fix Section 12 (Training Harness): Evaluate predictions proba sanitization
    if "def evaluate_predictions(y_true, proba):" in src:
        print(f"Patching Cell {idx}: evaluate_predictions sanitization")
        src = src.replace("proba = np.nan_to_num(proba, nan=1e-10, posinf=1e-10, neginf=1e-10)\n    # Ensure probabilities sum to 1 along the last axis after nan_to_num\n    proba = proba / proba.sum(axis=-1, keepdims=True)",
                          """proba = np.nan_to_num(proba, nan=1.0/N_CLASSES, posinf=1.0/N_CLASSES, neginf=1.0/N_CLASSES)
    row_sums = proba.sum(axis=-1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    proba = proba / row_sums""")
        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Fix Section 22 (Signer-Independent LOSO): Resilient retrieval of ref_recall
    if "LOSO = {}" in src and "ABL_PERCLASS['Full model (reference)']" in src:
        print(f"Patching Cell {idx}: Section 22 LOSO ref_recall resilience")
        old_ref = "pc['Recall, signer-dependent (%)'] = (\n            ABL_PERCLASS['Full model (reference)'] * 100).round(2)"
        new_ref = """if 'Full model (reference)' in ABL_PERCLASS:
            _ref_rec = ABL_PERCLASS['Full model (reference)']
        elif PROPOSED in RESULTS:
            _, _rec_ref, _, _ = precision_recall_fscore_support(
                d['yte'] if 'd' in globals() else yte,
                RESULTS[PROPOSED]['best']['pred'],
                labels=np.arange(N_CLASSES), zero_division=0)
            _ref_rec = _rec_ref
        else:
            _ref_rec = np.zeros(N_CLASSES)
        pc['Recall, signer-dependent (%)'] = (_ref_rec * 100).round(2)"""
        src = src.replace(old_ref, new_ref)
        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Fix Section 29 (Export): Ensure pandas and numpy are imported
    if "# ------------------------------------------------ reviewer evidence map" in src:
        print(f"Patching Cell {idx}: Section 29 Export imports")
        if "import pandas as pd" not in src:
            src = "import pandas as pd, numpy as np, os, json\n" + src
        cell['source'] = [line + '\n' for line in src.splitlines()]
        new_cells.append(cell)
        continue

    # Otherwise keep cell
    new_cells.append(cell)

print(f"New cell count: {len(new_cells)}")
nb['cells'] = new_cells

with open('SwSL_Reviewer_Response_Pipeline_FIXED_(1).ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Saved updated notebook successfully.")
