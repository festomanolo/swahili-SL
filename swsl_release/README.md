# SwSL isolated-gesture landmark corpus and recognizer

Companion release for *A Swahili Sign Language Recognition Using Bidirectional Long
Short-Term Memory with Temporal Attention*.

## Contents

| File | What it is |
|---|---|
| `swsl_landmarks_v1.npz` | 837 landmark sequences, 60 x 258, with labels, signer ids and the exact paper partition (12.3 MB) |
| `normalization_constants.npz` | The fitted min/max per feature dimension. Fitted on the training partition only |
| `swsl_bilstm_attention.keras` | The trained recognition model (604,551 parameters) |
| `config.json` | Every setting behind the reported numbers |
| `attention_specification.json` | Full specification of the temporal attention block |
| `label_to_text.json` | Class index to Swahili text, for the speech stage |
| `data_dictionary.csv` | Field-by-field description of the dataset arrays |

## Corpus

- **7 isolated gestures**: nenda (go), njema (good), mama (mother), hedhi (menstruation), kula (eat), baba (father), habari (hi)
- **2 signers**: Britney, Grace
- **837 validated clips**, 30 fps, recorded indoors against a plain wall
- Landmarks from MediaPipe Holistic (model complexity 1,
  min detection / tracking confidence 0.5 / 0.5)
- Face landmarks were extracted but are excluded from the released 258-d vector; see the
  ablation results in the article

## Reproducing the results

```python
import numpy as np, keras
d = np.load('swsl_landmarks_v1.npz', allow_pickle=True)
n = np.load('normalization_constants.npz')
X = (d['X'] - n['min']) / n['range']
model = keras.models.load_model('swsl_bilstm_attention.keras')
te = d['test_idx']
print((model.predict(X[te]).argmax(1) == d['y'][te]).mean())
```

Augmentation is applied to `train_idx` only: seven variants per clip (original, temporal
stretch at 0.9x and 1.1x, Gaussian jitter at sigma
0.01 and 0.02, temporal shift of +5 and
-5 frames). Do not augment validation or test.

## Evaluation protocols

`train_idx` / `val_idx` / `test_idx` is a sample-level stratified split: **both signers
appear in all three partitions**, so it measures generalization to unseen repetitions by
known signers. Use the `signers` array for a leave-one-signer-out protocol, which is the
signer-independent measurement.

## Licence

Landmark data CC BY 4.0; code MIT. Raw video is not released — see `LICENSE`.
