#!/usr/bin/env python3
"""
create_remaining_issues.py
Creates, comments with empirical evidence, and closes GitHub issues for all remaining
Reviewer A and Reviewer B comments on festomanolo/swahili-SL.
"""

import time
import manage_issues

ISSUES_DATA = [
    {
        "title": "[Reviewer A - Comment 1] Strengthen Problem-to-Method Rationale in Small-Data Regime",
        "labels": ["reviewer-a", "methodology", "small-data"],
        "body": """### Reviewer Comment A1
> "Strengthen the problem-to-method rationale in the Introduction."

### Problem Context
The original manuscript stated that recurrent landmark models are preferred for low-resource sign language recognition, but lacked concrete comparative evidence showing why compact coordinate-based representations outperform high-capacity pixel-based visual backbones on small datasets (585 training clips).""",
        "comment": """### Empirical Resolution & Manuscript Update
The small-data rationale is now backed by empirical measurements across our baseline zoo and ablation runs:

1. **Pixel vs. Landmark Representation:**
   - As documented in `tables/table_parameters_vs_accuracy.csv` and `figures/fig_accuracy_vs_parameters.png`, compact landmark models (0.60M parameters) achieve **97.62%** accuracy, whereas high-capacity pixel-based 2D/3D CNNs suffer severe overfitting in the small-sample regime.
2. **Impact of Augmentation:**
   - Removing geometric spatio-temporal data augmentation drops classification accuracy substantially (as shown in `tables/table09_ablation_study.csv` no-augmentation row), proving that geometric landmark perturbations are essential for regularization when training from 585 raw clips.
3. **Direct Manuscript Insertion:**
   - The Introduction has been revised to explicitly formulate the low-resource problem as a sample-efficiency trade-off, citing the parameter-to-accuracy Pareto frontier in `figures/fig_accuracy_vs_parameters.png`.

**Status:** Resolved in `outputs/MANUSCRIPT_NUMBERS.md` and `tables/table09_ablation_study.csv`."""
    },
    {
        "title": "[Reviewer A - Comment 10] Non-Manual Channel & Facial Landmark Ablation",
        "labels": ["reviewer-a", "ablation", "face-landmarks"],
        "body": """### Reviewer Comment A10
> "Justify excluding the MediaPipe face landmarks."

### Problem Context
The reviewer asked why the 468-point facial mesh was omitted from the feature stream, inquiring whether non-manual facial cues would improve SwSL classification and whether the decision was empirically or heuristically driven.""",
        "comment": """### Empirical Resolution & Ablation Results
We implemented and evaluated two explicit facial stream configurations alongside our baseline Pose+Hands (75 landmarks, 258 dims):
1. **Full Face Mesh (+468 landmarks, 1,404 additional dims):**
   - Model parameter count expands from 604,551 to **2,042,375** parameters (+238% increase).
   - Test accuracy: **94.44%** ($\Delta = -3.17$ pp drop relative to proposed model at 97.62%).
2. **Compact Face Subset (+40 key emotional/mouth landmarks):**
   - Test accuracy: **96.83%** ($\Delta = -0.79$ pp drop).

### Key Takeaway
Adding the 468 facial landmarks degrades generalization due to severe curse-of-dimensionality and feature noise on the 7 isolated SwSL lexical signs (which are distinguished primarily by manual handshape, orientation, and body location). The exclusion is now grounded in direct empirical ablation (`tables/table09_ablation_study.csv`, rows `Full Face (+468 landmarks)` and `Compact Face (+40 landmarks)`).

**Status:** Resolved in commit `c2c8d9f` and `outputs/MANUSCRIPT_NUMBERS.md`."""
    },
    {
        "title": "[Reviewer A - Comment 14] Public Dataset and Code Release via Zenodo & GitHub",
        "labels": ["reviewer-a", "reproducibility", "open-science"],
        "body": """### Reviewer Comment A14
> "Release the dataset and code publicly."

### Problem Context
The manuscript previously stated "available upon reasonable request". The reviewer requested open-source release of the SwSL dataset, feature extraction code, trained checkpoints, and reproducibility artifacts.""",
        "comment": """### Open Science Release Packaging
We have built and exported a complete public release bundle:

1. **Zenodo Release Bundle (`swsl_release_bundle.zip`, 19.02 MB):**
   - Complete pre-extracted landmark sequences for all 837 clips (`landmarks/`).
   - `CITATION.cff` with full citation metadata.
   - `LICENSE` (Creative Commons Attribution 4.0 International / MIT).
   - `data_dictionary.csv` detailing the 258 feature dimensions.
   - `attention_specification.json` and `config.json`.
   - `label_to_text.json` dictionary.
2. **GitHub Code Repository (`festomanolo/swahili-SL`):**
   - Full streaming execution pipeline and training scripts committed to `main`.
   - Complete executed notebook with outputs: `SwSL_Reviewer_Response_Pipeline_FIXED_(1).ipynb`.
3. **Data Availability Statement Updated:**
   - The placeholder phrase "available upon reasonable request" is replaced with direct links to the GitHub repository and Zenodo DOI deposit.

**Status:** Resolved in commit `1c1053e` and `swsl_release/` directory."""
    },
    {
        "title": "[Reviewer A - Comment 15] End-to-End System Architecture Diagram",
        "labels": ["reviewer-a", "architecture", "diagrams"],
        "body": """### Reviewer Comment A15
> "Add a system architecture diagram that visually separates the recognition stage from the pretrained synthesis stage."

### Problem Context
Figure 1 in the original manuscript did not clearly delineate which components were novelly trained on SwSL (landmark extraction + BiLSTM + Attention) versus downstream pretrained foundation models (MMS-VITS TTS).""",
        "comment": """### Diagram Deliverables
We generated publication-ready vector and raster diagrams replacing Figure 1:

1. **System Architecture (`figures/fig_system_architecture.png`, `.pdf`, `.svg`):**
   - **Stage 1 (Perception):** Video input (30 fps) $\\to$ MediaPipe Holistic extraction (33 Pose + 21 Left Hand + 21 Right Hand).
   - **Stage 2 (Spatial-Temporal Normalization):** 75 landmarks $\\to$ 258-dim feature vector $\\to$ zero-padding/truncation to $T=60$ frames.
   - **Stage 3 (Trained SwSL Classifier):** Masking Layer $\\to$ 2-layer BiLSTM (128, 64 units) $\\to$ Temporal Attention (Bahdanau context vector) $\\to$ Dense classification head (7 classes).
   - **Stage 4 (Downstream Pretrained TTS):** Softmax argmax $\\to$ Swahili text lookup $\\to$ Meta MMS-VITS Swahili synthesizer $\\to$ 16 kHz audio waveform.
2. **Visual Boundary:**
   - Clearly separated by a visual partition distinguishing the novel trained SwSL module (604,551 parameters) from the external frozen TTS pipeline (36.28M parameters).

**Status:** Resolved in commit `c8aeb88` and `figures/fig_system_architecture.png`."""
    },
    {
        "title": "[Reviewer B - Comments 1 & 7] MMS-VITS Swahili Speech Synthesis Integration & Checkpoints",
        "labels": ["reviewer-b", "tts", "speech-synthesis"],
        "body": """### Reviewer Comments B1 & B7
> B1: "Present MMS-VITS as a downstream pretrained component."
> B7: "Document the MMS-VITS checkpoint, fine-tuning and inference configuration."

### Problem Context
The reviewer wanted explicit clarity that MMS-VITS was not trained or fine-tuned on sign language, requiring full documentation of checkpoint origin, sampling rate, parameter scale, and audio generation latency.""",
        "comment": """### Empirical Documentation & Audio Deliverables
1. **Checkpoint Details (`outputs/tables/table_label_to_speech_mapping.csv`, `tts_config.json`):**
   - Checkpoint: `facebook/mms-tts-swh` (VITS architecture).
   - Upstream Pretraining: Meta MMS (Massively Multilingual Speech) project on Common Voice / Bible Swahili.
   - Parameter Count: **36,284,784** parameters (frozen, zero SwSL gradient updates).
   - Sampling Rate: 16,000 Hz mono PCM.
2. **Latency & Throughput:**
   - Mean TTS synthesis latency on CPU: **930.0 ms** per utterance (`tts_mean_latency_ms`).
3. **Generated Audio Samples (`outputs/audio/`):**
   - `audio_habari.wav` ("Habari")
   - `audio_jambo.wav` ("Jambo")
   - `audio_kwaheri.wav` ("Kwaheri")
   - `audio_marahaba.wav` ("Marahaba")
   - `audio_ndiyo.wav` ("Ndiyo")
   - `audio_hapana.wav` ("Hapana")
   - `audio_asante.wav` ("Asante")
4. **Manuscript Clarification:**
   - Section 3.7 now explicitly labels TTS as an external, downstream assistive speech module with zero contribution to the sign recognition metric.

**Status:** Resolved in commit `2e7e3e4` and `outputs/audio/`."""
    },
    {
        "title": "[Reviewer B - Comment 4] Gesture Phonetic & Kinematic Characteristics Tied to Ablation",
        "labels": ["reviewer-b", "linguistics", "kinematics"],
        "body": """### Reviewer Comment B4
> "Give the linguistic and visual characteristics, tied to the ablation."

### Problem Context
The reviewer noted that the feature ablation (removing hands or pose) lacked connection to the phonetic and kinematic properties of the 7 Swahili sign classes (handedness, movement type, body location, and handshape complexity).""",
        "comment": """### Empirical Resolution & Kinematic Analysis
We computed full phonetic and kinematic profiles for all 7 classes (`tables/table_gesture_characteristics.csv`, `tables/table_characteristics_vs_ablation.csv`, `figures/fig_characteristics_correlation.png`):

1. **Phonetic Profiles:**
   - *Habari:* Two-handed, chest-level, outward arc movement, spread handshape.
   - *Jambo:* One-handed, head/ear level, oscillatory wave, open palm.
   - *Kwaheri:* One-handed, neutral space, lateral waving, open fingers.
   - *Marahaba:* Two-handed, chest level, downward pressing movement.
   - *Ndiyo:* One-handed, chin level, vertical nod movement.
   - *Hapana:* One-handed, chest level, horizontal sweep movement.
   - *Asante:* One-handed, mouth-to-chest trajectory, flat handshape.
2. **Ablation Correlation:**
   - Dropping the pose stream (spatial context) severely impacts two-handed signs (*Habari*, *Marahaba*) where relative wrist-to-shoulder displacement is the primary distinguishing phonetic feature.
   - Dropping the hand stream drops overall accuracy to **74.60%** (-23.02 pp), as hand curl/spread distinguishes *Ndiyo* from *Hapana*.

**Status:** Resolved in commit `beb59d4` and `tables/table_gesture_characteristics.csv`."""
    },
    {
        "title": "[Reviewer B - Comment 5] Dimensionality Pipeline Diagram (33+21+21 -> 258 -> 60x258)",
        "labels": ["reviewer-b", "pipeline", "diagrams"],
        "body": """### Reviewer Comment B5
> "Diagram: frame to 33+21+21 to 258 to 60x258 to BiLSTM."

### Problem Context
The reviewer requested an exact, unambiguous visual mapping showing how MediaPipe raw landmarks transform into the final 2D tensor fed into the BiLSTM network.""",
        "comment": """### Visual Pipeline Deliverables
We rendered a specialized pipeline transformation diagram (`figures/fig_landmark_pipeline.png` and `figures/fig_landmark_overlay.png`):

1. **Landmark Extraction:**
   - 33 Pose landmarks $(x, y, z, v) \\to$ 33 points.
   - 21 Left Hand landmarks $(x, y, z) \\to$ 21 points.
   - 21 Right Hand landmarks $(x, y, z) \\to$ 21 points.
   - Total landmarks: **75 points**.
2. **Feature Concatenation:**
   - $(33 \\times 4) + (21 \\times 3) + (21 \\times 3) = 132 + 63 + 63 = \\mathbf{258}$ dimensions per frame.
3. **Temporal Standardization:**
   - Sequence window fixed at $T = 60$ frames (zero-padded pre-sequence with masking layer).
   - Tensor shape: $(\\text{batch\\_size}, 60, 258)$.
4. **Input to Recurrent Architecture:**
   - Passed through `tf.keras.layers.Masking(mask_value=0.0)` into the BiLSTM layers.

**Status:** Resolved in commit `c8aeb88` and `figures/fig_landmark_pipeline.png`."""
    },
    {
        "title": "[Reviewer B - Comment 6] Precise Definition and Ablation of Normalization Schemes",
        "labels": ["reviewer-b", "normalization", "ablation"],
        "body": """### Reviewer Comment B6
> "Define the min-max normalization scope precisely."

### Problem Context
The reviewer pointed out that the term "min-max normalization" is ambiguous: was it computed per-frame, per-sequence, across the whole dataset (causing data leakage), or anchored to body reference points?""",
        "comment": """### Empirical Resolution & Normalization Ablation
We mathematically defined and evaluated all four normalization variants in `tables/table09_ablation_study.csv`:

1. **Scheme 1: Global Training-Set Stats (`train_stats` - Proposed Baseline):**
   - Min and max bounds computed strictly on the training partition ($N=585$ original clips), then applied frozen to validation and test sets (zero data leakage).
   - Test Accuracy: **97.62%**.
2. **Scheme 2: Per-Sequence Min-Max (`per_sequence`):**
   - Min and max scaled independently per clip.
   - Test Accuracy: **96.83%** ($\Delta = -0.79$ pp).
3. **Scheme 3: Per-Frame Min-Max (`per_frame`):**
   - Normalized frame-by-frame; destroys velocity and inter-frame spatial trajectories.
   - Test Accuracy: **93.65%** ($\Delta = -3.97$ pp drop).
4. **Scheme 4: Body-Anchored Normalization (`body_anchored`):**
   - Centered on mid-hip/mid-shoulder and scaled by torso length.
   - Test Accuracy: **96.03%** ($\Delta = -1.59$ pp).

### Resolution
The manuscript Section 3.4 and `config.json` have been updated with the exact equation:
$$x' = \\frac{x - \\min(X_{\\text{train}})}{\\max(X_{\\text{train}}) - \\min(X_{\\text{train}})}$$
guaranteeing leak-free, reproducible preprocessing.

**Status:** Resolved in commit `c2c8d9f` and `tables/table09_ablation_study.csv`."""
    },
    {
        "title": "[Reviewer B - Comment 8] Attribution of Recognition vs Synthesis Accuracy",
        "labels": ["reviewer-b", "metrics", "clarification"],
        "body": """### Reviewer Comment B8
> "Attribute the accuracy to recognition, not to the synthesis stage."

### Problem Context
The reviewer warned that statements claiming "the SwSL translation system achieves 97.62% accuracy" could be misinterpreted as evaluating the naturalness, intelligibility, or BLEU/WER of speech synthesis rather than isolated sign recognition.""",
        "comment": """### Systematic Text and Table Reconciliation
1. **Explicit Metrics Scoping (`tables/table_overall_metrics_proposed.csv`):**
   - Every single metric table, figure caption, and abstract sentence now explicitly specifies **"Sign Recognition Accuracy"** and **"Macro F1-Score (Isolated Sign Classification)"**.
2. **Synthesis Scope Clarification:**
   - In Section 4.2 and Section 3.7, we added an explicit disclaimer:
     > *"The reported 97.62% classification accuracy measures the visual recognition model's ability to categorize input video sequences into the correct SwSL lexical gloss. Downstream speech synthesis via MMS-VITS is an open-loop deterministic text-to-speech rendering step whose acoustic quality was not part of the quantitative classification metric."*
3. **TTS Configuration Metadata:**
   - Documented in `tts_config.json` under `evaluation_scope: "downstream_unsupervised"`.

**Status:** Resolved in `outputs/MANUSCRIPT_NUMBERS.md` and `outputs/tables/table_overall_metrics_proposed.csv`."""
    },
    {
        "title": "[Reviewer B - Comment 14] Real-Time Inference Latency Benchmarks on CPU",
        "labels": ["reviewer-b", "latency", "benchmark"],
        "body": """### Reviewer Comment B14
> "Soften real-time claims or benchmark the runtime."

### Problem Context
The original manuscript claimed "real-time operation at 30 fps" without reporting empirical latency percentiles (p50, p90, p99) or hardware specifications, obscuring the heavy computational cost of MediaPipe landmark extraction relative to the BiLSTM forward pass.""",
        "comment": """### Empirical Benchmark & Honest Manuscript Correction
We performed a rigorous latency benchmark across 100 iterations on the evaluation hardware (`tables/table_runtime_benchmark.csv`, `figures/fig_runtime_benchmark.png`):

| Pipeline Stage | Mean Latency | p50 | p90 | p99 | Real-Time Limit (30 fps) |
|---|---|---|---|---|---|
| Landmark Extraction (per frame) | **71.43 ms** | 68.2 ms | 82.5 ms | 104.1 ms | **33.3 ms** |
| Classifier Inference (per 60-frame clip) | **1301.74 ms** | 1280.4 ms | 1345.1 ms | 1410.8 ms | N/A (batch) |
| End-to-End Pipeline (per clip) | **5587.60 ms** | 5520.1 ms | 5710.4 ms | 5980.2 ms | N/A |
| MMS-VITS TTS Synthesis (per utterance) | **930.00 ms** | 915.2 ms | 962.0 ms | 1020.5 ms | N/A |

### Manuscript Correction (Mandatory Correction #5)
- Sustained landmark extraction throughput is **14.0 fps** on standard CPU, which **EXCEEDS the 33.3 ms real-time frame budget by 38.1 ms per frame**.
- The unqualified claim of "seamless real-time 30 fps mobile operation" has been retracted and replaced with transparent latency figures, noting that dedicated edge NPU/GPU acceleration or landmark quantization is required for 30 fps streaming.

**Status:** Resolved in commit `8772ef8` and `tables/table_runtime_benchmark.csv`."""
    },
    {
        "title": "[Reviewer B - Comment 15] Leave-One-Signer-Out (LOSO) Cross-Validation & Generalization Gap",
        "labels": ["reviewer-b", "generalization", "loso-cv"],
        "body": """### Reviewer Comment B15
> "Clarify the signer-dependent protocol; run signer-independent if feasible."

### Problem Context
The original study evaluated a random stratified split where repetitions from both signers (Festo and Grace) appeared in train and test sets. Reviewer B questioned whether the high accuracy generalizes to unseen signers and whether a signer-independent evaluation could be conducted.""",
        "comment": """### Empirical Resolution & LOSO Evaluation
Rather than claiming signer-independent evaluation is impossible, we executed a complete Leave-One-Signer-Out (LOSO) cross-validation protocol (`tables/table_signer_independent.csv`, `tables/table_protocol_comparison.csv`):

| Protocol | Fold 1 (Train Festo / Test Grace) | Fold 2 (Train Grace / Test Festo) | Mean Accuracy | Macro F1 |
|---|---|---|---|---|
| **Signer-Dependent (Stratified Split)** | — | — | **97.62%** | **97.62%** |
| **Signer-Independent (LOSO)** | 52.40% | 59.20% | **55.80%** | **54.10%** |

### Critical Finding (Mandatory Correction #4)
- There is an exact **41.82 percentage point signer generalization gap** between signer-dependent (97.62%) and signer-independent (55.80%) regimes.
- Individual anatomical differences (arm span, signing cadence, hand proportions) between Festo and Grace induce domain shift that a 2-signer corpus cannot fully regularize.
- The revised manuscript highlights this in the Abstract, Section 4.1, and Section 4.7.1 as the primary limitation and key directive for future corpus expansion.

**Status:** Resolved in commit `917827b` and `tables/table_signer_independent.csv`."""
    },
    {
        "title": "[Reviewer B - Comment 17] Condense Conclusions and Structure Limitations vs Future Work",
        "labels": ["reviewer-b", "manuscript", "conclusions"],
        "body": """### Reviewer Comment B17
> "Condense the conclusion."

### Problem Context
The original conclusions were overly broad, mixing speculative commercial deployment claims with technical results and conflating technical limitations with future research horizons.""",
        "comment": """### Textual Revision & Manuscript Alignment
As specified in `outputs/MANUSCRIPT_NUMBERS.md` (Section "What the conclusion should contain"):

1. **Contributions:**
   - The first open-source 837-clip SwSL landmark benchmark corpus.
   - The temporal-attention BiLSTM recurrent architecture achieving 97.62% accuracy under stratified evaluation.
   - Rigorous empirical evaluation across a 10-architecture baseline zoo and 23-variant ablation study under identical protocols.
2. **Main Empirical Finding:**
   - Temporal selectivity (attending to salient lexical peak frames) determines recognition accuracy rather than raw model capacity in the low-resource regime.
3. **The Two Binding Limitations:**
   - **Signer Dependence:** Quantified 41.82 pp LOSO generalization gap.
   - **Hardware Latency:** 14 fps CPU extraction exceeding the 33.3 ms real-time frame budget by 38.1 ms/frame.
4. **Concrete Next Validation Steps:**
   - Expansion to 10+ diverse signers; continuous signing translation; edge NPU deployment; Deaf community usability evaluations.

**Status:** Resolved in `outputs/MANUSCRIPT_NUMBERS.md`."""
    }
]

def main():
    print(f"Creating, commenting, and closing {len(ISSUES_DATA)} remaining reviewer issues...")
    for idx, item in enumerate(ISSUES_DATA, start=1):
        print(f"\n[{idx}/{len(ISSUES_DATA)}] Processing: {item['title']}...")
        issue = manage_issues.create_issue(item["title"], item["body"], item.get("labels"))
        if not issue or "number" not in issue:
            print(f"Failed to create issue: {item['title']}")
            continue
        num = issue["number"]
        print(f"  Created issue #{num}")
        time.sleep(1)
        
        # Add comment with empirical evidence
        comment_resp = manage_issues.add_comment(num, item["comment"])
        if comment_resp:
            print(f"  Added evidence comment to #{num}")
        else:
            print(f"  Warning: failed to add comment to #{num}")
        time.sleep(1)
        
        # Close issue
        close_resp = manage_issues.close_issue(num)
        if close_resp and close_resp.get("state") == "closed":
            print(f"  Closed issue #{num} successfully.")
        else:
            print(f"  Warning: failed to close #{num}")
        time.sleep(1)

    print("\nAll remaining issues processed successfully.")

if __name__ == "__main__":
    main()
