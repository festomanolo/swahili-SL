# Numbers for the revised manuscript

Generated 2026-09-24 14:27 · preset `quick` · 1 seeds · CPU only

Every value below was produced by this run. Where a value replaces one in the
current manuscript, the note says where.

| Quantity | Value | Where it belongs |
|---|---|---|
| `n_clips_raw` | 837 | Section 3.2.3 and Table 3: raw clip count |
| `n_classes` | 7 | everywhere the class count appears |
| `n_signers` | 2 | Section 3.2.1 |
| `fps` | 30.0 | Section 3.2.2 |
| `frames_min` | 15 | Section 3.3 sequence-length range |
| `frames_max` | 176 | Section 3.3 sequence-length range |
| `n_clips_retained` | 837 | Section 3.2.4: clips passing the 90% landmark-quality threshold |
| `pct_clips_padded` | 99.6 | Section 3.3: share of clips shorter than the 60-frame window |
| `mean_live_frames` | 25.7 | Section 3.3: mean number of real (non-padded) frames per standardized sequence |
| `n_train_original` | 585 | Section 4.1: training clips before augmentation |
| `n_val` | 126 | Section 4.1: validation clips |
| `n_test` | 126 | Section 4.1, Table 8, Figure 6: test clips |
| `test_per_class` | 18 | Figure 6 caption: test samples per class |
| `train_imbalance_ratio` | 1.012 | Section 3.6 / Eq. (15): whether class weighting is justified |
| `proposed_accuracy_mean` | 97.62 | Abstract, Section 4.2, Table 7, Conclusions: headline accuracy (mean over seeds) |
| `proposed_accuracy_std` | 0.0 | Table 7: cross-seed standard deviation of the proposed model |
| `proposed_macro_f1_mean` | 97.62 | Table 7 and Table 8 macro-average row |
| `proposed_best_accuracy` | 97.62 | Section 4.2: single-run checkpointed best model, if a single figure is quoted |
| `strongest_baseline` | Transformer encoder (2 layers) | Section 4.3: the model the proposed one is compared to |
| `strongest_baseline_accuracy` | 99.21 | Section 4.3 and Conclusions |
| `margin_over_best_baseline_pp` | -1.59 | Section 4.3: margin in percentage points over the strongest same-corpus baseline |
| `proposed_best_epoch` | 38 | Figure 4 caption: the epoch at which early stopping restored the best weights |
| `proposed_train_val_gap_pp` | -1.73 | Section 4.2: the train-validation gap behind the regularization claim |
| `expected_calibration_error` | 0.0164 | Section 4.7.2: whether the confidence threshold in Algorithm 1 is trustworthy |
| `n_baselines_significantly_beaten` | 1 | Section 4.3: how many baselines the proposed model separates from at p<0.05 |
| `proposed_accuracy_ci` | [94.44, 100.0] | Abstract and Section 4.2: the 95% bootstrap interval to quote alongside the point accuracy |
| `delta_full_face_pp` | -3.17 | Section 3.2.6 (A10): measured effect of adding the full 468-landmark face stream |
| `delta_compact_face_pp` | -0.79 | Section 3.2.6 (A10): measured effect of adding the compact 40-landmark face stream |
| `delta_hands_only_pp` | -23.02 | Section 4.5 (B16): measured feature importance, NOT a linguistic claim |
| `delta_pose_only_pp` | 0.0 | Section 4.5 (B16): measured feature importance, NOT a linguistic claim |
| `attention_entropy_ratio` | 0.4956 | Section 4.6: how much more selective than uniform the learned attention is |
| `attention_top10_mass` | 0.96 | Section 4.6: share of attention mass on the ten most salient frames |
| `signer_dependent_accuracy` | 97.62 | Abstract and Section 4.2: the headline figure, scoped to unseen repetitions by known signers |
| `signer_independent_accuracy` | 55.8 | Section 4.1 and 4.7.1 (B15): leave-one-signer-out accuracy, to be reported alongside the headline figure |
| `signer_generalization_gap_pp` | 41.82 | Section 4.7.1 (B15): how much of the headline figure depends on having seen the signer during training |
| `proposed_parameters` | 604551 | Abstract, Table 5, Table 10, Table 11, Section 4.7.2: the true parameter count |
| `proposed_macs_per_clip_M` | 34.65 | Section 4.7.2: computational cost per clip, if a complexity figure is quoted |
| `proposed_model_size_mb` | 7.35 | Table 10: deployed model size |
| `extraction_ms_per_frame` | 71.43 | Section 4.7.2 (B14): the cost that determines whether the pipeline is interactive |
| `extraction_fps` | 14.0 | Section 4.7.2 (B14): sustained landmark-extraction frame rate |
| `inference_ms_cpu` | 1301.74 | Section 4.7.2 (B14): classifier latency per clip on CPU |
| `end_to_end_ms_cpu` | 5587.6 | Section 4.7.2 (B14): end-to-end delay for one clip on CPU |
| `real_time_verdict` | EXCEEDED by 38.1 ms per frame | Section 4.7.1 (B14): whether the term "real-time" is defensible at all |
| `tts_parameters` | 36284784 | Section 3.7: size of the pretrained synthesizer, for contrast with the recognition model. Makes the point that the large component is the one this study did not train. |
| `tts_mean_latency_ms` | 930.0 | Section 4.7.2: synthesis latency, if end-to-end interaction cost is quoted |
| `release_dataset_mb` | 12.3 | Data Availability Statement: size of the releasable landmark corpus |

## The five corrections this run forces

1. **Parameter count.** The model has **604,551** parameters, not 177,607. Correct the abstract, Table 5, Table 10, Table 11 and Section 4.7.2, and delete the weight-sharing footnote.
2. **The augmented corpus size.** The training partition holds 4,095 augmented sequences, from 585 original clips. 5,880 describes augmenting every partition, which is not the procedure. Replace the augmented column of Table 2 with the per-partition table.
3. **Class weighting.** The training imbalance ratio is 1.012. Weighting was unnecessary; Table 6 and Eq. (15) should say so.
4. **Signer independence.** Leave-one-signer-out gives 55.8% against 97.62% signer-dependent. The claim that the experiment could not be run must go; the precision caveat stays.
5. **Real-time.** EXCEEDED by 38.1 ms per frame at 71.43 ms per frame (14.0 fps) on i386. Name the device wherever a rate is quoted.

## What the conclusion should contain (B17)

1. Contributions: the corpus, the landmark-based recurrent classifier with temporal attention, and the single-protocol evaluation of the architectural families on that corpus.
2. Main finding: temporal selectivity rather than capacity determines performance in this regime — with the ablation margins and the significance test result.
3. The two binding limitations: signer dependence (now quantified) and latency unmeasured on target hardware (now measured on this one).
4. Next validation steps: enlarged signer pool, phonological annotation, continuous signing, device benchmarking, listening and usability studies.

## Do not claim

- Superiority over published systems evaluated on other corpora. Only the same-protocol table supports a comparative claim.
- Signer-independent recognition from the headline figure.
- Real-time operation on a target device that was not benchmarked.
- A linguistic conclusion about the manual versus non-manual channel from the feature ablation.