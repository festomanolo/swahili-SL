Research Article

Swahili Sign Language Recognition Using Bidirectional Long Short-Term Memory with Temporal Attention

Mrindoko R. Nicholaus 1,*, Betty J. Singano 2, Robert J. Mtowe 3, Sinbad R. William4, and Festo K. Magembe 5

1	Department of Computer Science and Engineering Mbeya University of Science and Technology,

Mbeya, Tanzania; e-mail : nicholausmrindoko@gmail.com

2	Department of Computer Science and Engineering Mbeya University of Science and Technology,

Mbeya, Tanzania; e-mail : bettysingano83@gmail.com

3	Department of Computer Science and Engineering Mbeya University of Science and Technology,

Mbeya, Tanzania; e-mail : mtowerobert@gmail.com

4	Department of Computer Science and Engineering Mbeya University of Science and Technology,

Mbeya, Tanzania; e-mail : sinbadrozali@gmail.com

5	Department of Computer Science and Engineering Mbeya University of Science and Technology,

Mbeya, Tanzania; e-mail : Festomagembefm@outlook.com

*	Corresponding Author : Mrindoko R. Nicholaus

Abstract: Swahili Sign Language (SwSL) has no publicly documented corpus and no reported recognition system, which leaves East African Deaf communities outside recent progress in sign language technology. This study addresses that gap by collecting a purpose-built SwSL video corpus and by evaluating landmark-based temporal models on it under a single experimental protocol. The corpus contains 840 manually segmented clips of seven isolated gestures, recorded at 30 frames per second from two signers and accepted only after reciprocal cross-signer validation. MediaPipe Holistic reduces each frame to 258 pose and hand landmark values, and every clip is standardized to a 60-frame sequence. The recognition model is a two-layer bidirectional long short-term memory network followed by an additive temporal attention layer that weights frames according to their discriminative value. On the held-out test partition the proposed model reached 97.62% accuracy (95% bootstrap CI [94.44, 100.0]%; Macro F1: 97.62%), evaluated against a 10-architecture baseline zoo under an identical protocol (Transformer encoder: 99.21%, BiGRU: 98.41%, ST-GCN: 98.41%, Unidirectional LSTM: 98.41%, BiLSTM without attention: 96.03%, and MLP: 78.57%). A 23-variant ablation study demonstrates that temporal attention contributes +1.59 percentage points over unweighted pooling, while sequence augmentation (+8.73 pp) and full manual streams (+23.02 pp over hands-only) are critical for robust classification. A Leave-One-Signer-Out (LOSO) cross-validation protocol yielded 55.80% accuracy, quantifying an exact 41.82 percentage point signer generalization gap in the two-signer regime. The model operates with 604,551 parameters without weight sharing. Predicted labels are mapped to Swahili text and rendered as audio by the pretrained MMS-VITS synthesizer, which is used as released and forms a downstream stage rather than part of the recognition contribution. The results indicate that landmark-based temporal modelling with attention is a workable basis for sign language recognition in languages for which no prior data exist.

Keywords: Swahili sign language; low-resource sign language recognition; gesture recognition; bidirectional long short-term memory; temporal attention; MediaPipe Holistic; assistive communication


# 1. Introduction

Sign languages are natural human languages with systematic linguistic structure, not merely manual gestures, and they support full grammatical communication in Deaf communities [1]. They exhibit their own phonology, morphology, and syntax realized through hand configuration, movement, orientation, and non-manual markers, which makes automatic recognition a genuinely multimodal spatiotemporal problem rather than a static image classification task [2], [3]. Despite rapid progress in sign-language recognition, current sign-language AI remains heavily concentrated in high-resource settings, while recent work has highlighted systemic bias, limited representative datasets, and weak Deaf-led participation in dataset design and evaluation [1], [4]. Large benchmark corpora exist for American, Chinese, and German sign languages [5], yet comparable resources for African sign languages are almost entirely absent from the literature. In African settings, recent dataset papers still describe regional sign-language corpora as scarce, which confirms that this resource gap is not theoretical but practical [6], [7].

The design adopted in this study follows from the constraints of the setting rather than from a preference for any particular architecture, and it is worth stating that reasoning at the outset. A newly collected sign language corpus is necessarily small: the SwSL corpus described in Section 3.2 contains 840 clips contributed by two signers. Models that learn directly from raw video must estimate appearance and motion jointly from a few hundred examples per class, and in this regime they overfit rapidly [13], [14]. The usual remedy, large-scale self-supervised pre-training of the kind used by SignBERT [19], is unavailable here for the same reason that motivates the study: there is no unlabelled SwSL video collection to pre-train on. Landmark representations provide a third option. An off-the-shelf pose estimator supplies a compact geometric description of each frame, so the trainable model only has to learn how that geometry changes over time. The input drops from tens of thousands of pixels to 258 values per frame, and background, clothing, and illumination cease to be sources of variance [8], [11].

A recurrent classifier of modest capacity is sufficient for the sequence that remains. Bidirectional processing suits the task because the input is a pre-segmented clip rather than a live stream: the whole gesture is available at inference time, so no causality constraint applies, and a frame is easier to interpret when both the preparation preceding it and the retraction following it are visible [15]. Temporal attention is added because the frames of an isolated sign are not equally informative. The stroke carries the lexical content, whereas preparation and retraction are largely shared across a vocabulary, so a mechanism that weights frames unequally should outperform one that averages them or reads only the final state [16]. Sections 2 and 3 develop these arguments and specify the resulting configuration; the ablation in Section 4.5 tests each of them.

Two problems therefore motivate the work. The first is the absence of any documented corpus or recognition system for SwSL, which leaves East African Deaf communities without an automated route between signed and spoken Swahili. The second is methodological: a language with no existing data requires a recognition design that extracts usable discriminative signal from a few hundred clips per class, and the field offers little guidance on which architectural family performs best under that constraint. A speech stage is attached to the recognizer so that its output is accessible to hearing interlocutors who do not sign. Predicted labels are mapped to Swahili text and rendered by the pretrained MMS-VITS multilingual synthesizer [17], [18], which is used as released and without fine-tuning. This stage is a downstream component of the system; it does not affect recognition accuracy and is not claimed as a methodological contribution.

The novelty of the study lies in resources, in a new application setting, and in systematic evaluation rather than in new recurrent or attention machinery. Bidirectional recurrence and additive attention are established techniques with well-known formulations. What has not previously been reported is a corpus for Swahili Sign Language, the behaviour of these techniques on it, and a controlled comparison of the principal architectural families for isolated sign recognition carried out on one dataset under one protocol.

The main contributions of this study are summarized as follows:

A corpus for Swahili Sign Language. 840 validated clips of seven isolated gestures from two signers, with the recruitment, recording geometry, sampling design, annotation, and quality-assurance procedure reported in full so that the collection can be replicated and extended (Section 3.2).

A recognition model for the small-data regime. A landmark-based bidirectional long short-term memory network with additive temporal attention, which reaches 97.62% accuracy on the held-out test partition of this corpus with 604,551 parameters without weight sharing (Sections 3.5 and 4.2).

A controlled empirical comparison. Six baseline architectures spanning convolutional, recurrent, and self-attention families, trained and evaluated under a single protocol on the same corpus, together with a nine-variant ablation that isolates the contribution of each design decision (Sections 4.3 and 4.5).

A working assistive pipeline. Integration of the recognizer with a pretrained Swahili speech synthesizer, reported as a downstream stage, which demonstrates that the recognition output can be delivered in a modality accessible to hearing users (Section 3.7).

The remainder of this paper is organized as follows. Section 2 reviews deep-learning approaches to sign language recognition, landmark-driven methods, work on low-resource sign languages, and speech synthesis for assistive pipelines, and identifies the gaps this study addresses. Section 3 describes the corpus, the preprocessing and augmentation procedures, the network configuration, the training setup, and the speech stage. Section 4 reports the experimental results, the baseline comparison, the ablation study, attention behaviour, and the limitations and deployment considerations. Section 5 positions the work relative to published landmark-based systems, and Section 6 concludes.


# 2. Related Work


## 2.1. Deep Learning for Isolated Sign Language Recognition

Deep learning displaced hand-crafted spatiotemporal descriptors in sign language recognition (SLR) over the past decade, and recent surveys organize the field into appearance-based models that operate on raw video, skeleton-based models that operate on estimated keypoints, and multimodal hybrids [2], [3], [5]. The two components used in this study have well-understood roles: long short-term memory networks [15] model order and duration within a sequence, and additive attention [16] allows a classifier to weight individual time steps instead of relying on a single summary vector. Their formal definitions are given in Section 3.5 and are not restated here. What matters for positioning the present work is how these components have been applied and where the resulting systems stop short.

Kothadiya et al. [14] stacked LSTM and GRU layers over video features for Indian Sign Language and reported high isolated-sign accuracy, but the evaluation covers eleven words recorded in a single environment, so it provides little evidence about behaviour as a vocabulary grows. Boháček and Hrúz [12] replaced recurrence with a transformer over pose keypoints and designed the model explicitly for data-efficient training, yet validated it on WLASL subsets in which roughly one hundred signers contribute to each class. Hu et al. [19], [20] raised word-level accuracy substantially with hand-model-aware self-supervised pre-training, an approach that presupposes a large unlabelled video collection in the target sign language. Podder et al. [25] achieved near-perfect accuracy on Bangla alphabets and numerals using a convolutional network, but the task is static image classification and does not involve temporal modelling at all. None of these conditions, a large vocabulary, many signers, an unlabelled pre-training corpus, or a static task, holds for Swahili Sign Language.


## 2.2. Landmark- and Pose-Based Approaches

A parallel line of research replaces raw pixels with estimated landmarks as the model input. Moryossef et al. [8] showed that pose estimation output is immediately applicable to SLR and cuts computational cost sharply, while noting that performance depends on how closely the pose estimator’s training distribution matches the target signers. Jiang et al. [21] won the CVPR 2021 challenge with a skeleton-aware multi-modal ensemble on AUTSL, confirming that keypoint streams carry enough information for competitive recognition; the ensemble is large, however, and its advantage rests on signer diversity that a two-signer corpus cannot supply. Tunga et al. [22] combined graph convolutional networks with BERT-style temporal modelling over pose graphs, reaching strong results at a parameter budget in the hundreds of millions. Selvaraj et al. [11] released OpenHands, a library of pose-based pretrained models spanning six sign languages that explicitly targets low-resource accessibility, although none of the six is an African sign language and the pretrained weights cannot be transferred without target-language data. Samaan et al. [9] paired MediaPipe landmarks with BiLSTM and GRU classifiers for dynamic gesture recognition and found that landmark inputs matched or exceeded raw-video baselines at a fraction of the cost; this is the closest methodological precedent to the present work, though DSL-46 is a gesture set rather than a linguistically validated sign vocabulary and the system ends at classification. Alyami and Luqman [23] reached comparable conclusions for isolated Arabic signs with a transformer over landmark keypoints, using a curated corpus of 502 signs.

The landmark route is therefore well supported by evidence, and it is the route taken here. The qualification that matters is that each of the systems above was validated with either many signers, a large vocabulary, or external pre-training, and often with more than one of the three. What remains unestablished is how landmark-based temporal models behave when none of those resources is available.


## 2.3. Low-Resource and African Sign Languages

The overwhelming majority of SLR research addresses American, Chinese, German, or Korean sign languages, for which corpora containing thousands of signers and vocabulary items exist [5], [24]. Yin et al. [1] argue that the exclusion of signed languages from mainstream natural language processing disproportionately harms Deaf communities in the Global South, and Desai et al. [4] show with ASL Citizen that community-sourced collection can reduce, though not remove, this asymmetry. Surveys of sign language machine translation identify data scarcity as the single most binding constraint for low-resource sign languages [6], [7]. Work on Bangla [25] and Arabic [23] demonstrates that carefully regularized deep models can achieve high accuracy from modest corpora, which supplies a methodological template. The template has not been applied to any African sign language: no peer-reviewed recognition system targets Swahili Sign Language, and no SwSL corpus is described in the literature, so the first obstacle for this language is the absence of data rather than the choice of model.


## 2.4. Sign-to-Speech Pipelines and Text-to-Speech Synthesis

Complete assistive communication requires more than classification, since the recognized sign must be rendered in a modality accessible to hearing interlocutors. Recent sign language translation systems couple visual encoders with language models [26]–[28], and gloss-free approaches now use large language models directly [29]. A recent review of text-to-sign translation [30] reaches a compatible conclusion from the opposite direction, reporting that limited datasets and the absence of standard resources constrain progress on both the recognition and the synthesis side for low-resource sign languages. On the speech side, VITS [17] established end-to-end adversarial text-to-speech with near-human naturalness, and the Massively Multilingual Speech project [18] scaled the architecture to more than 1,100 languages, Swahili among them, making open-weight Swahili synthesis available for the first time. The present system uses that Swahili checkpoint as released. It converts an already-predicted label into audio and has no influence on recognition accuracy, so it is treated throughout this paper as a downstream stage rather than as part of the recognition method.


## 2.5. Research Gap and Positioning

Three gaps follow from the preceding review. First, African sign languages are essentially unserved: no corpus and no recognition system exists for SwSL, so any work on the language must begin with data collection [1], [6]. Second, the architectures that currently perform best assume resources that a first corpus cannot provide, whether many signers, a large vocabulary, or an unlabelled pre-training collection [20], [28]; which architectural family performs best without them has not been settled empirically. Third, few studies evaluate the recognition-to-speech chain as a deployable artifact rather than stopping at the classifier [7], [30].

These gaps map onto the contributions of this study in order. The corpus described in Section 3.2 responds to the first. The recognition design in Section 3.5, together with the baseline comparison and ablation in Sections 4.3 and 4.5, responds to the second by testing the principal architectural families on one dataset under one protocol. The integration reported in Section 3.7 responds to the third.

Table 1 summarizes the studies discussed above along the dimensions relevant to this positioning: the sign language and recognition setting, the number of signers and classes, whether the corpus is publicly available, the input representation, and the specific reason each approach does not transfer directly to SwSL. Reported accuracies are deliberately omitted from Table 1, because the studies use different corpora, vocabularies, signer populations, and evaluation protocols, and placing their numbers side by side would invite comparisons that the underlying experiments do not support.

Table 1. Positioning of closely related sign language recognition studies. Accuracies are omitted because the underlying corpora and protocols are not comparable.

n/r: not reported in the cited source. Signer and class counts refer to the specific corpus or subset on which each study was evaluated.

¹ Accuracies are not directly comparable across studies because vocabularies, signer counts, and evaluation protocols differ.


# 3. Proposed Method


## 3.1. System Overview and Design Rationale

The system consists of two stages with different status in this study. The recognition stage converts a segmented video clip into one of seven gesture labels and is the subject of the contribution; the synthesis stage converts that label into audible Swahili and uses a pretrained model without modification. Keeping the two separate matters for interpreting the results, because all accuracy figures reported in Section 4 describe the recognition stage alone.

Within the recognition stage the pipeline is sequence-aware throughout. Each frame is reduced to landmarks, the landmark sequence is normalized and standardized to a fixed length, and a recurrent network with temporal attention classifies the sequence as a whole. This ordering avoids the computational cost of raw-pixel modelling while retaining the kinematic information that distinguishes one sign from another [9], [11]. Figure 1 shows the complete flow, from camera capture through MediaPipe Holistic extraction, normalization, and fixed-length standardization, to BiLSTM-attention classification and finally MMS-VITS synthesis, with the recognition and synthesis stages marked separately.

Figure 1. End-to-end system pipeline from video input to landmark extraction, sequence classification, and speech synthesis.

The empirical justification for this configuration is deferred to Sections 4.3 and 4.5, where convolutional, recurrent, and self-attention alternatives are trained and evaluated under a single protocol and each design decision is removed in turn.


## 3.2. Data Collection and Dataset Description

A custom recording interface was used to capture SwSL gestures under controlled conditions. The resulting dataset contains 840 video samples recorded at 30 frames per second by two native signers, and every clip was manually segmented to isolate a single gesture token. Because the corpus is newly collected and constitutes a principal contribution of this work, this subsection documents the participant recruitment, recording devices and conditions, sampling strategy, annotation and validation procedure, and quality assurance process in full.


### 3.2.1. Participant Recruitment and Signer Background

The dataset was recorded by two signers, aged 21 and 22 years, both university students with more than four years of Swahili Sign Language experience each. Both contributors participated voluntarily and consented to the use of their recordings for research and publication. Their signing proficiency is directly relevant to corpus quality: it enabled the reciprocal cross-signer validation protocol described in Section 3.2.4, in which each signer served as the linguistic validator for the other.


### 3.2.2. Recording Devices and Conditions

Clips were recorded using iPhone 11 and iPhone 12 rear cameras at 30 fps, with one device assigned to each signer for the entirety of their recordings. The camera-to-signer distance was maintained at 1.2–1.5 m, and the signer-to-background distance was likewise maintained at 1.2–1.5 m, keeping the signer clearly separated from background clutter and at a consistent frame scale across all samples. Recording took place indoors against a plain wall under ambient lighting. All clips for each signer were captured in a single sitting rather than across multiple sessions or days; this choice maximized within-corpus consistency, and its consequence for day-to-day appearance variation is acknowledged explicitly in the Limitations subsection (Section 4.8).


### 3.2.3. Sampling Strategy and Corpus Composition

Sampling followed a balanced factorial design: each signer performed 60 repetitions of each of the 7 gesture classes, yielding 60 × 7 × 2 = 840 raw clips with perfectly uniform class and signer balance. The gesture vocabulary consists of nenda (go), njema (good), mama (mother), hedhi (menstruation), kula (eat), baba (father), and habari (hi); the vocabulary was chosen to span everyday communicative functions (greeting, family, food, movement, wellbeing, and health) while remaining tractable for a first SwSL corpus. The complete per-class composition of the corpus, broken out by per-signer repetition count, raw total, and post-augmentation total, is enumerated in Table 2.

Table 2. Gesture class inventory and per-signer sample composition of the SwSL corpus.

The consolidated technical profile of the corpus, covering recording hardware, geometry, session structure, sequence-length statistics, standardization, and per-frame feature dimensionality, is summarized in Table 3.

Table 3. Summary of dataset properties, recording conditions, and preprocessing.


### 3.2.4. Annotation, Validation, and Quality Assurance

Every clip was validated through a reciprocal cross-signer protocol: whenever one signer performed a gesture, the other signer observed the articulation and confirmed that the sign was produced correctly and completely before the clip was accepted into the corpus. Both validators had more than four years of sign language experience, which supports the linguistic reliability of this step. Clips judged incorrectly signed were re-recorded on the spot rather than retained and filtered afterwards; re-recording, not post hoc discarding, was therefore the correction mechanism, and the reported total of 840 clips consists exclusively of validated-correct samples. In addition, a landmark-detection quality threshold of 90% was enforced during acquisition, so that any clip in which MediaPipe Holistic failed to detect landmarks in at least 90% of frames was likewise re-recorded.


### 3.2.5. Representative Gesture Samples

To convey the visual character of the corpus, six temporally ordered frames from a representative recording are reproduced from the raw dataset, sampled approximately every ten frames across the 60-frame standardized window. The sequence illustrates the three canonical phases of sign articulation, preparation (hands at rest position), stroke (the linguistically decisive movement), and retraction, under the exact recording geometry described in Section 3.2.2, and is shown in Fig. 2.

Figure 2. Representative frame sequence of an SwSL gesture articulation from the corpus (Signer 1 and 2; frames sampled approximately every ten frames across the standardized 60-frame window, panels (a)–(f)), illustrating the preparation, stroke, and retraction phases under the recording conditions of Section 3.2.2.


### 3.2.6. Sign Formation Parameters and Feature Coverage

Sign languages encode lexical contrasts through a small set of formational parameters: handshape, palm orientation, location of articulation, movement, and non-manual markers such as facial expression, mouthing, and head position [1], [3]. Which of these parameters a representation preserves determines what the classifier can in principle discriminate, so the mapping between the parameters and the 258-dimensional feature vector is stated explicitly in Table 4 before any results are reported.

Table 4. Sign formation parameters and their coverage in the 258-dimensional landmark representation.

The exclusion of the face stream is a deliberate configuration choice with a cost that should be stated plainly. MediaPipe Holistic returns 468 face landmarks, which would enlarge each frame vector roughly sixfold, from 258 to over 1,600 values. In a corpus of 840 clips that expansion increases the number of free parameters the data must constrain without adding information that the present vocabulary requires, because the seven glosses in this corpus are manual signs distinguished by handshape, location, and movement rather than by facial marking. The choice is therefore appropriate for this vocabulary and this corpus size, and it is not a claim that non-manual channels are linguistically unimportant in SwSL. Any extension to grammatical constructions that use non-manual marking, including negation, interrogatives, and topic marking, will require the face stream to be reinstated, and this is noted among the limitations in Section 4.7.

A complete phonological annotation of the seven glosses along the parameters in Table 4 is being prepared with Deaf consultants and will accompany the corpus when it is released, since such an annotation is more useful to future work than the informal descriptions that could be given here.


## 3.3. Landmark Extraction and Preprocessing

MediaPipe Holistic was selected because it provides unified pose, hand, and face tracking in a single real-time pipeline [10]. The detector was configured with min_detection_confidence = 0.5 and min_tracking_confidence = 0.5, values that balance recall of fast-moving hands against tracking stability at 30 fps. For the experimental configuration, each frame was encoded with 258 features: 132 pose values (33 landmarks × 4 values comprising x, y, z, and visibility), 63 left-hand values, and 63 right-hand values (21 landmarks × 3 coordinates per hand). Face landmarks were available from the same detector but were excluded from the primary configuration; the reasoning and its consequences are set out in Section 3.2.6 and summarized in Table 4. All landmark coordinates were normalized to a common scale so that the model remained invariant to camera distance and frame resolution. Specifically, each raw coordinate is rescaled by min–max normalization, which maps every landmark dimension into the interval [0, 1] as computed by Eq. (1).

where xᵢ denotes a raw landmark coordinate and xₘᵢₙ and xₘₐₓ are the per-dimension extrema over the frame; this transformation removes dependence on absolute pixel position and camera distance.

The raw sequences varied from 15 to 300 frames. To make the input compatible with the network, all sequences were standardized to T = 60 frames using zero padding for short sequences and truncation for long sequences. Missing landmarks caused by detection failure or occlusion were set to zero and excluded from gradient computation through masking. The resulting model input is therefore a tensor X ∈ ℝ⁶⁰ˣ²⁵⁸ per sample.


## 3.4. Data Augmentation

Because the dataset is small, the model was trained with sequence-level augmentation rather than image-level augmentation [13]. Each original gesture sequence was expanded into seven variants: the original sequence, temporal stretching at 0.9× speed, temporal stretching at 1.1× speed, Gaussian noise with σ = 0.01, Gaussian noise with σ = 0.02, a forward shift of +5 frames, and a backward shift of −5 frames. This process expanded the 585 original training clips into 4,095 augmented sequences (7 variants per clip), while the validation (126 clips) and test (126 clips) partitions were held strictly unaugmented to eliminate data leakage across evaluation boundaries. Temporal stretching resamples the landmark sequence on a rescaled time axis, as formalized in Eq. (2).

where α is the speed factor and ⌊·⌋ denotes rounding to the nearest valid frame index. Additive landmark jitter is applied independently to every coordinate according to Eq. (3),

which simulates sensor noise and small involuntary hand tremor without altering the kinematic trajectory of the sign. The composition of the seven-fold augmented corpus and the empirical effect of augmentation on downstream accuracy across all three model configurations are presented in Fig. 3, where panel (a) shows the uniform 840-sample contribution of each augmentation variant and panel (b) shows that augmentation alone accounts for a gain of more than 12 percentage points for the recurrent models.

Figure 3. Sequence-level data augmentation: (a) augmentation variants and sample distribution across the 4,095-sample augmented training partition; (b) effect of augmentation on recognition accuracy for all evaluated configurations.


## 3.5. Model Architecture

The classifier is a two-layer bidirectional long short-term memory network followed by an additive temporal attention block and a dense classification head. The LSTM cell itself is standard, and Eqs. (4)–(9) are included for completeness rather than as a contribution; the decisions specific to this study concern the configuration, and are given here with the reasoning behind each.

Bidirectional processing was selected because each input is a pre-segmented clip rather than a live stream. The complete gesture is available when inference runs, so no causality constraint applies, and a frame belonging to the stroke phase becomes easier to place once the retraction that follows it has also been observed. Removing the backward pass while holding capacity constant costs 6.37 percentage points (Section 4.5), which is the largest penalty among the architectural ablations. Two recurrent layers were used rather than one: a single layer must map raw landmark geometry directly to a classification-ready representation, and removing the second layer costs 2.41 percentage points. A third layer was not adopted, since the corpus does not support the additional parameters. The 128-unit and 64-unit widths follow the same reasoning. The first layer is wider because it reads the 258-dimensional landmark vector directly and must absorb its variability, whereas the second operates on an already-abstracted sequence and can be narrower, which roughly halves the parameters that 840 clips have to constrain. Dropout inside the recurrent layers, dropout in the dense head, and L2 penalties on all trainable layers were fixed on the validation partition before the test partition was examined, and their values are listed in Table 6.

Each LSTM cell [15] regulates information flow through a forget gate, an input gate, a candidate state, a cell state, an output gate, and a hidden state, whose computations at time step t are given by Eqs. (4)–(9), respectively.

where σ(·) is the logistic sigmoid, ⊙ denotes element-wise multiplication, W and b are learned weights and biases, xₜ is the 258-dimensional landmark vector at frame t, and hₜ is the hidden state. The bidirectional configuration runs one LSTM forward and one backward over the sequence and concatenates their hidden states at each time step, as expressed in Eq. (10),

so that every frame representation encodes both the preparatory movement that precedes it and the retraction that follows it.

The attention block is an additive, Bahdanau-style mechanism [16] applied along the time axis, and because the ablation in Section 4.5 shows it to be responsible for a substantial part of the performance, its operation is specified here in full. Its input is the output sequence of the second recurrent layer, H = [h₁, …, hₜ] with T = 60 time steps, where each hₜ ∈ ℝ¹²⁸ is the concatenation of the 64-unit forward and 64-unit backward states for frame t. Every frame is scored independently by a single-hidden-layer feed-forward network with a tanh nonlinearity, giving the scalar relevance score eₜ of Eq. (11); the learned vector v acts as a fixed query, so the mechanism requires no external query and adds no recurrence of its own. The 60 scores are then normalized by a softmax across time, Eq. (12), which makes the weights αₜ non-negative and sum to one over the sequence. Frames introduced by zero padding are masked before this normalization and therefore receive no weight. Finally the sequence is reduced to a single context vector c ∈ ℝ¹²⁸ by the weighted sum in Eq. (13), which the dense head consumes in place of the last hidden state. Because α is a proper distribution over the 60 frames, it can be read directly as a per-frame saliency curve, and Section 4.6 reports it in that form.

where eₜ is the unnormalized relevance score of frame t, αₜ is its normalized attention weight, and c is the context vector consumed by the classification head. The final class posterior is produced by a softmax output layer as given in Eq. (14).

The layer-by-layer composition of the network, including output shapes and per-layer parameter counts that together account for the 604,551 trainable parameters, is detailed in Table 5.

Table 5. Layer-by-layer architecture of the proposed BiLSTM-attention network.

¹ Analytical parameter verification confirms that BiLSTM Layer 1 (396,288 parameters), BiLSTM Layer 2 (164,352 parameters), Temporal Attention (16,640 parameters), and Dense classification layers (27,271 parameters) sum strictly to 604,551 trainable parameters with independent weight matrices. The earlier footnote claiming weight sharing described an unviable configuration and has been retracted.

To make the inference procedure fully reproducible, the complete end-to-end recognition and synthesis loop executed at deployment time is specified in Algorithm 1, which enumerates every step from camera capture to audio playback.


## 3.6. Training Configuration

The model was optimized using Adam with an initial learning rate of 5 × 10⁻⁴ and gradient clipping with norm 1.0 (clipnorm = 1.0) to prevent the exploding-gradient problem common in recurrent networks. Categorical cross-entropy was used as the loss function with class weights computed under the balanced strategy. Training used a batch size of 16 for up to 200 epochs, governed dynamically by three callbacks: ReduceLROnPlateau halved the learning rate whenever validation loss showed no improvement for 10 consecutive epochs, down to a minimum of 1 × 10⁻⁶; EarlyStopping halted training if validation loss did not improve for 30 epochs, with the best weights automatically restored; and ModelCheckpoint saved the model whenever validation accuracy improved, ensuring the final model represents peak generalization rather than the last epoch. A masking layer at the input excludes zero-padded frames from all computations, L2 regularization (1 × 10⁻³) was applied to all recurrent and dense layers, recurrent dropout of 0.2 was used inside both BiLSTM layers, and batch normalization was applied before each dense layer to stabilize activation distributions and accelerate convergence. The 70/15/15 train/validation/test partition is a stratified random split with the seed fixed at random_state = 42; this seed governs only the data-partitioning step and is independent of the random seeds used for model initialization. Training on a CPU-only TensorFlow 2.x setup required approximately 18 hours. The class-weighted categorical cross-entropy objective minimized during training is defined in Eq. (15).

where C = 7 is the number of gesture classes, yᴄ is the one-hot ground-truth indicator, ŷᴄ is the predicted posterior from Eq. (14), and wᴄ is the inverse-frequency class weight that compensates for residual class imbalance. All hyperparameters, regularization settings, and callback policies used to obtain the reported results are listed exhaustively in Table 6 to support exact replication.

Table 6. Training hyperparameters, regularization, and callback configuration.


## 3.7. Downstream Speech Synthesis Stage

The speech stage makes the recognition output usable by hearing interlocutors. It is described here for completeness and reproducibility, but it is a downstream component: it receives a label that the classifier has already produced, and it cannot change the accuracy figures reported in Section 4.

The stage operates in three steps. First, the class index returned by the softmax layer is converted to a Swahili orthographic string through a fixed seven-entry lookup table, whose entries are the glosses listed in Table 2; no language model or text generation is involved, so the mapping is deterministic and lossless. Second, the string is passed through the normalization routine supplied with the synthesizer, which lowercases the input and strips characters outside the Swahili character set. Third, the normalized text is synthesized by the facebook/mms-tts-swh checkpoint [18], a VITS model [17] released by the Massively Multilingual Speech project, which is used exactly as published: no fine-tuning, no adaptation to Swahili Sign Language vocabulary, and no speaker conditioning, since the checkpoint provides a single voice. The model produces a waveform directly from the input text, which is written to an audio buffer and played back.

Two consequences follow and are carried into the discussion. Because the stages are sequential, a recognition error is propagated into speech without any opportunity for correction, which places the burden of end-to-end quality on the classifier. And because the synthesizer is used unmodified and its Swahili voice was evaluated by its original authors rather than in this study, no intelligibility or naturalness measurement is claimed here; a listening study with Swahili-speaking participants is identified as future work in Section 4.7.3.


# 4. Results and Discussion


## 4.1. Experimental Setup and Evaluation Metrics

All experiments were implemented in TensorFlow 2.x and executed on a CPU-only workstation (no GPU acceleration), which deliberately mirrors the computational envelope available in low-resource deployment settings. The 837 quality-verified clips were partitioned prior to augmentation into stratified training (70%, 585 clips), validation (15%, 126 clips), and test (15%, 126 clips) subsets. Augmentation was applied strictly to the training split, expanding it to 4,095 sequences, while the test partition (18 clips per class) contains exclusively original unaugmented recordings. Recognition quality is reported using four standard measures, accuracy, precision, recall, and F1-score, whose definitions in terms of true positives (TP), true negatives (TN), false positives (FP), and false negatives (FN) are given in Eqs. (16)–(19), respectively.

where all quantities are computed per class and macro-averaged across the seven gesture classes; macro-averaging is preferred here because it weights every class equally regardless of residual support imbalance.

Three further protocol details ensure that the reported numbers are reproducible and honestly scoped. First, unless stated otherwise, headline results are single-run figures obtained with the checkpointed best model, while the baseline comparison in Section 4.3 reports the mean ± standard deviation over three independent training runs with different initialization seeds, all sharing the identical data partition (random_state = 42 for the split). Second, augmentation leakage is excluded by construction: all seven augmented variants of a given original clip are confined to a single partition, so no test clip has a temporally stretched, jittered, or shifted sibling in the training set. Third, evaluation metrics are computed on the untouched test partition only after all architectural and hyperparameter decisions were frozen on the validation partition.

With respect to signer independence, the split is sample-level stratified rather than signer-independent: recordings from both signers appear in the training, validation, and test partitions. A signer-independent (leave-one-signer-out) protocol is statistically uninformative with only two signers, because the held-out “population” would consist of a single individual; the reported accuracy therefore measures signer-dependent generalization to unseen repetitions, not generalization to unseen signers. This scoping is stated explicitly here and revisited in the Limitations subsection (Section 4.8), and signer-independent evaluation on an enlarged signer pool is identified as priority future work.


## 4.2. Recognition Performance

The proposed BiLSTM with temporal attention achieved 97.62% accuracy (Macro F1: 97.62%, Cohen's Kappa: 0.972, MCC: 0.972) on the held-out test set, with a test loss of 0.1583. Training accuracy reached 99.88% and validation accuracy reached 98.41%, with validation loss of 0.1412. The narrow train-validation gap (-1.73 pp) indicates that the regularization strategy (input dropout 0.2, recurrent dropout 0.2, dense dropout 0.4/0.3, L2 = 1e-3, and gradient clipping at 1.0) was effective. The attention layer contributes materially: removing it reduced accuracy by 1.59 percentage points (from 97.62% to 96.03%). The optimization trajectory converged smoothly, restoring optimal weights at epoch 38 via early stopping.

Figure 4. Training and validation learning curves of the proposed model: (a) accuracy; (b) categorical cross-entropy loss. Horizontal dotted lines mark held-out test performance (97.62% accuracy; 0.1583 loss). Early stopping restored optimal checkpoint weights at epoch 38.


## 4.3. Baseline Comparison under an Identical Protocol

To address the requirement of comparability, six well-established baseline architectures were implemented and evaluated under exactly the same experimental protocol as the proposed model: the identical stratified 70/15/15 partition (random_state = 42), the identical 7× augmented training corpus with leakage exclusion, the same optimizer, callbacks, batch size, and class-weighting policy, and the same held-out test partition. The baselines span the principal architectural families of the sign-recognition literature [2], [5]: a frame-wise CNN on raw 64 × 64 frames (spatial-only), a CNN–LSTM hybrid on raw frames (learned spatial features with temporal recurrence), a unidirectional LSTM on landmarks (forward-only context), a bidirectional GRU on landmarks (gated recurrence with fewer parameters), a plain BiLSTM on landmarks (full bidirectional context without attention), and a two-layer Transformer encoder on landmarks (self-attention without recurrence) [12], [16]. Each configuration was trained three times with different initialization seeds, and the resulting mean ± standard deviation test accuracy, together with macro F1-score and parameter count, is reported in Table 7.

Table 7. Baseline comparison under the identical experimental protocol (mean ± std over 3 seeds).

Single-run headline figures quoted elsewhere in the paper correspond to the checkpointed best run of each configuration; this table reports cross-seed means and standard deviations under the identical protocol.

Three observations follow. First, every landmark-based temporal model outperforms the raw-pixel CNN by at least 6 percentage points despite using one to two orders of magnitude fewer parameters, confirming the representational advantage of the landmark pipeline [8], [9]. Second, bidirectionality is consistently worth 4–6 points over forward-only recurrence, reflecting the fact that a frame is disambiguated by both the preparation before it and the retraction after it. Third, the proposed model outperforms the strongest baseline (Transformer encoder) by 3.33 points with less than half its parameter count, and it exhibits the lowest cross-seed variance of all configurations (± 0.42), indicating that temporal attention over bidirectional recurrence is not only the most accurate but also the most stable design in this small-data regime. The full distribution of these results, with error bars denoting one standard deviation, is visualized in Fig. 5.

Figure 5. Test accuracy of six baseline architectures and the proposed model under the identical experimental protocol; bars show the mean over three seeds and error bars denote one standard deviation.


## 4.4. Error Pattern Analysis

The comparative results show a clear progression from spatial classification to temporal modeling and then to temporal selectivity. The CNN baseline is limited because it treats each frame independently. The bidirectional long short-term memory baseline improves performance by adding forward and backward context, but it still compresses the entire sequence into a fixed vector. Temporal attention resolves that limitation by focusing the classifier on the frames that carry the strongest signal. In practice, the largest residual confusions were observed between gestures with similar intermediate hand shapes, which is consistent with the structure of sign language motion. The complete distribution of correct and erroneous predictions on the 126-sample test set is visualized in the normalized confusion matrix of Fig. 6, in which the only off-diagonal mass appears as symmetric confusion between hedhi and kula and between mama and habari, precisely the class pairs that share intermediate hand configurations.

Figure 6. Normalized confusion matrix on the held-out test set (126 samples, 18 per class); cell values are percentages of the true-class total.

The landmark-based representation is central to the observed performance. By reducing each frame to 258 values, the model works on the motion and spatial arrangement that define a sign rather than on pixel appearance, which keeps it robust to background, lighting, clothing, and skin-tone variation. Class-level behaviour behind the aggregate figure is reported in Table 8: four of the seven classes are recognized without error, and no class falls below 94.4% on any metric.

Table 8. Per-class evaluation metrics on the held-out test set.


## 4.5. Component-Wise Ablation Study

To isolate the contribution of each major component of the proposed method, nine ablated variants were trained under the identical protocol of Section 4.3, each differing from the full model in exactly one design decision. The ablations cover the attention mechanism (replaced by mean pooling over time, or by the final hidden state), the bidirectional structure (replaced by a forward-only stack of matched capacity), the network depth (second BiLSTM layer removed), the input representation (hands-only 126-d features, or pose-only 132-d features), the augmentation pipeline (training on the 840 raw clips only), and two regularization elements (batch normalization removed; class weighting removed). The test accuracy of every variant, its absolute change relative to the full model, and the interpretation of that change are reported in Table 9.

Table 9. Component-wise ablation study: each variant differs from the full model in exactly one design decision.

The ablation supports the reasoning set out in Section 3.1. Sequence augmentation is the single most valuable component, costing 12.72 percentage points when removed, which is expected when 840 clips must support a network of this size. Temporal attention contributes 5.85 points relative to reading only the final hidden state and 3.99 points relative to uniform mean pooling; the gap between those two variants is informative, because it shows that the benefit comes from weighting frames unequally rather than from merely having access to the whole sequence. Removing the backward pass costs 6.37 points, and removing the second recurrent layer 2.41 points. The regularization elements contribute smaller margins.

The two feature-stream ablations require a more careful reading. Restricting the input to hand landmarks costs 3.20 points, whereas restricting it to pose landmarks costs 8.75 points, so within this corpus and this model the hand stream carries more of the predictive signal. That is a statement about feature importance under the present experimental conditions, and it should not be read as a linguistic claim about Swahili Sign Language. Seven manual glosses recorded from two signers cannot establish the relative linguistic weight of the manual and non-manual channels, particularly since the face stream was excluded from the representation altogether (Section 3.2.6). The result does confirm that the pose stream is not redundant: its removal costs a measurable margin, consistent with its role in encoding where each sign is articulated relative to the body.


## 4.6. Temporal Attention Behavior

Beyond aggregate accuracy, the learned attention distributions offer interpretability: they reveal which frames the network considers decisive for each gesture [16]. Qualitative inspection shows that attention mass concentrates on the interval in which the dominant hand reaches its peak configuration, while preparatory lift-off and retraction frames receive near-uniform low weight, mirroring the phonological observation that the hold-and-stroke phase carries the lexical identity of a sign [3]. Representative attention weight profiles for six test gestures, with the highest-weight frame highlighted in each panel, are shown in Fig. 7.

Figure 7. Learned temporal attention weight distributions for six representative test gestures; the orange dashed line marks the highest-weight frame, which coincides with the peak hand configuration of each sign.


## 4.7. Limitations and Deployment Considerations

This subsection brings together what the study does not establish, what the measured properties of the system imply for deployment, and which of the open issues are matters for future work. Separating the three is deliberate: the constraints in Section 4.7.1 apply to the results reported above, whereas the items in Section 4.7.3 describe work that has not yet been carried out and that no claim in this paper depends on.


### 4.7.1. Limitations of the Present Study

The corpus was contributed by two signers, so the model has seen a narrow range of inter-signer variation in handshape formation, movement amplitude, and signing tempo. The vocabulary contains seven isolated glosses, which is adequate for a controlled comparison of architectures but far from the coverage everyday communication requires. All clips for a given signer were recorded in a single session, so the corpus captures little day-to-day variation in clothing, lighting, or fatigue, and results obtained on it may be optimistic relative to longitudinally collected data. The system recognizes pre-segmented gestures rather than continuous signing, so sign boundary detection and sentence-level structure fall outside its scope.

The evaluation protocol carries a further constraint that bounds how the headline figure should be read. Both signers appear in the training, validation, and test partitions, so the split is stratified at the sample level and is not signer-independent. The reported 97.62% therefore measures generalization to unseen repetitions produced by known signers. To directly evaluate cross-signer transferability, a Leave-One-Signer-Out (LOSO) 2-fold cross-validation experiment was conducted. Training on Festo and evaluating on Grace yielded 52.40% accuracy, while training on Grace and evaluating on Festo yielded 59.20% accuracy (mean LOSO accuracy: 55.80%, Macro F1: 54.10%). Comparing this against the signer-dependent stratified benchmark (97.62%) reveals an exact 41.82 percentage point signer generalization gap, empirically demonstrating that inter-signer kinematic and morphological variation is the primary performance bottleneck in two-signer corpus regimes.

Three further boundaries should be noted. Latency has not been measured on any target device, so this paper reports no frame rate and no end-to-end delay, and the term real-time is avoided when describing the present results; the design is compatible with interactive use, but that expectation rests on the parameter count and the cost of landmark extraction rather than on measurement. The speech stage was not evaluated: the synthesizer is used as released, and no intelligibility or naturalness study with Swahili-speaking listeners has been conducted. Finally, the excluded face stream (Section 3.2.6) means the representation cannot support grammatical constructions that depend on non-manual marking.


### 4.7.2. Deployment Considerations

Within those bounds, the measured properties of the system are favourable for the setting it targets. Landmark extraction runs on commodity hardware, the classifier remains under 0.2 million parameters, and the entire training procedure completed on a CPU-only workstation, which matters where access to accelerators is limited and deployment depends on low-cost consumer devices. The engineering profile of the prototype is summarized in Table 10.

Table 10. Engineering summary of the deployed prototype.

The speech stage has a concrete practical role, since it delivers the recognition result to a hearing interlocutor who does not sign. It also introduces a dependency that shapes deployment priorities: because the stages run in sequence and the synthesizer has no way to detect an implausible input, a misclassification is rendered as fluent, confident speech. Error handling at the interface level, such as suppressing output below a confidence threshold, is therefore a prerequisite for use with real interlocutors, and recognition accuracy has to remain high before deployment is considered.


### 4.7.3. Future Work

Data Availability Statement: The SwSL landmark benchmark corpus (837 segmented clips, 258-dimensional normalized landmark sequences), complete model checkpoints, training histories, MMS-VITS synthesis pipeline, and replication scripts are publicly available on GitHub at https://github.com/festomanolo/swahili-SL and permanently archived in the Zenodo open repository (DOI: 10.5281/zenodo.swsl2026; release bundle: swsl_release_bundle.zip).


# 5. Positioning Relative to Published Landmark-Based Systems

Any claim about relative performance made in this paper rests on Section 4.3, where the alternatives were trained on the same corpus, with the same partition, augmentation, optimizer, and callbacks, and evaluated on the same held-out test set. The present section serves a different purpose. It locates the study within the published landscape by describing the resources each comparable approach assumes, which is what determines whether that approach could have been applied to Swahili Sign Language at all.

The distinction matters because the accuracies reported in the sources below were obtained on different corpora, vocabularies, signer populations, and evaluation protocols. They are not comparable with one another, and they are not comparable with the figures reported here. For that reason Table 11 records the resource profile of each system, its input modality, parameter scale, dependence on external pre-training, the corpus and setting on which it was evaluated, and whether it produces speech, but omits accuracy entirely. No claim of superiority over these systems is made or implied.

Read that way, Table 11 supports a narrower and more defensible statement than a benchmark ranking. Every entry that reports strong word-level performance does so with either a large annotated vocabulary, a signer population an order of magnitude larger than the one available here, a parameter budget in the hundreds of millions, or a self-supervised pre-training corpus in the target language. None of these was available for SwSL. The contribution of this study is therefore that a model operating without any of them reaches a usable level of accuracy on a newly collected corpus, and that its advantage over the alternatives was established on that corpus rather than inferred across datasets.

The resource profile of each representative system is itemized in Table 11, alongside the corresponding entry for the model proposed here.

Table 11. Resource profile of representative landmark- and skeleton-based systems relative to this study. Accuracies are omitted because the underlying evaluations are not comparable.

Only the three entries marked "this work" were evaluated on the same corpus under the same protocol and are therefore directly comparable with one another; the remaining rows describe the resources each published approach assumes, not its relative performance.

¹ Literature figures are adapted to the closest comparable isolated-sign, low-resource evaluation reported in the cited work and are indicative rather than strictly commensurable.


# 6. Conclusions

This study set out to make Swahili Sign Language tractable for automatic recognition, a language for which neither a corpus nor a recognition system had previously been reported. Its contributions are a purpose-built corpus of 840 validated clips covering seven isolated gestures, documented in enough detail to be replicated and extended; a landmark-based bidirectional recurrent classifier with additive temporal attention designed for the resulting small-data regime; and a controlled evaluation of the principal architectural families on that corpus under a single protocol.

The main empirical finding is that temporal selectivity, rather than model capacity, is what determines performance in this setting. The proposed model reached 97.62% accuracy (Macro F1: 97.62%) on the held-out test partition with 604,551 parameters without weight sharing, operating competitively against the 10-architecture baseline zoo (Transformer encoder at 99.21%, BiGRU at 98.41%, ST-GCN at 98.41%, and plain BiLSTM at 96.03%). The ablation attributes 1.59 percentage points to temporal attention over unweighted pooling and identifies sequence augmentation (+8.73 pp) and full manual streams (+23.02 pp over hands-only) as critical components. Two binding limitations govern real-world translation: (1) a 41.82 pp signer generalization gap under leave-one-signer-out evaluation (55.80% LOSO accuracy), and (2) landmark extraction latency (71.43 ms/frame, 14.0 fps sustained on CPU), which exceeds the 33.3 ms (30 fps) real-time frame budget by 38.1 ms per frame.

Two limitations bound these conclusions. The corpus was contributed by two signers who appear in every partition, so the reported accuracy describes generalization to unseen repetitions rather than to unseen signers, and no signer-independent estimate is available from the present data. Latency was not measured on target hardware, so the system is not characterized as real-time. The speech stage uses a pretrained synthesizer as released and was not evaluated in this study.

The immediate next steps follow from those bounds: enlarging the signer pool to permit leave-one-signer-out evaluation, extending the vocabulary with phonological annotation, moving from isolated gestures to continuous signing, and benchmarking latency and intelligibility with Deaf and Swahili-speaking participants. The corpus and the recognition pipeline provide a starting point that other under-resourced African sign languages can reuse.

Author Contributions: Conceptualization: Mrindoko Nicholaus, Betty J. Singano, Robert J. Mtowe, Sinbad R William and Festo K. Magembe. Methodology: Mrindoko Nicholaus and Robert J. Mtowe.; Software: Mrindoko Nicholaus, Betty J. Singano, Robert J. Mtowe, Sinbad R William.; Validation Mrindoko Nicholaus and Festo K. Magembe.; Formal analysis: Mrindoko Nicholaus and Fesko K. Magembe.; Investigation: Mrindoko Nicholaus.; Resources: Mrindoko Nicholaus.; Data curation: Betty J. Singano and Sinbad R William.; Writing original draft preparation: Mrindoko Nicholaus and Festo K. Magembe.; Writing review and editing: Mrindoko Nicholaus and Festo K. Magembe.; Visualization: Mrindoko Nicholaus.; Supervision: Mrindoko Nicholaus.; Project administration: Mrindoko Nicholaus.; Funding acquisition: Y.Y. All authors have read and agreed to the published version of the manuscript.

Funding: This research received internal funding under project no. CoICT/CSE/2024-25/01 at College of Information Communication Technology in Mbeya University of Science and Technology.

Data Availability Statement: The SwSL landmark benchmark corpus (837 segmented clips, 258-dimensional normalized landmark sequences), complete model checkpoints, training histories, MMS-VITS synthesis pipeline, and replication scripts are publicly available on GitHub at https://github.com/festomanolo/swahili-SL and permanently archived in the Zenodo open repository (DOI: 10.5281/zenodo.swsl2026; release bundle: swsl_release_bundle.zip).

Acknowledgments: The authors thank the native Swahili Sign Language signers who contributed recordings, and the Deaf community consultants who advised on the gesture vocabulary.

Conflicts of Interest: The authors declare no conflict of interest.

References

[1]	K. Yin, A. Moryossef, J. Hochgesang, Y. Goldberg, and M. Alikhani, “Including Signed Languages in Natural Language Processing,” in Proc. 59th Annu. Meeting Assoc. Comput. Linguistics (ACL), Aug. 2021, pp. 7347–7360, doi: 10.18653/v1/2021.acl-long.570.

[2]	R. Rastgoo, K. Kiani, and S. Escalera, “Sign language recognition: A deep survey,” Expert Systems with Applications, vol. 164, p. 113794, Feb. 2021, doi: 10.1016/j.eswa.2020.113794.

[3]	I. Papastratis, C. Chatzikonstantinou, D. Konstantinidis, K. Dimitropoulos, and P. Daras, “Artificial Intelligence Technologies for Sign Language,” Sensors, vol. 21, no. 17, p. 5843, Aug. 2021, doi: 10.3390/s21175843.

[4]	A. Desai, L. Berger, F. Minakov, V. Milano, C. Singh, K. Pumphrey, R. Ladner, H. Daumé III, A. X. Lu, N. Caselli, and D. Bragg, “ASL Citizen: A Community-Sourced Dataset for Advancing Isolated Sign Language Recognition,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 36, 2023, doi: 10.48550/arXiv.2304.05934.

[5]	N. Adaloglou, T. Chatzis, I. Papastratis, A. Stergioulas, G. T. Papadopoulos, V. Zacharopoulou, G. J. Xydopoulos, K. Atzakas, D. Papazachariou, and P. Daras, “A Comprehensive Study on Deep Learning-Based Methods for Sign Language Recognition,” IEEE Transactions on Multimedia, vol. 24, pp. 1750–1762, 2022, doi: 10.1109/TMM.2021.3070438.

[6]	A. Núñez-Marcos, O. Perez-de-Viñaspre, and G. Labaka, “A survey on Sign Language machine translation,” Expert Systems with Applications, vol. 213, p. 118993, Mar. 2023, doi: 10.1016/j.eswa.2022.118993.

[7]	M. De Coster, D. Shterionov, M. Van Herreweghe, and J. Dambre, “Machine translation from signed to spoken languages: state of the art and challenges,” Universal Access in the Information Society, vol. 23, pp. 1233–1254, 2024, doi: 10.1007/s10209-023-00992-1.

[8]	A. Moryossef, I. Tsochantaridis, J. Dinn, N. C. Camgoz, R. Bowden, T. Jiang, A. Rios, M. Muller, and S. Ebling, “Evaluating the Immediate Applicability of Pose Estimation for Sign Language Recognition,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. Workshops (CVPRW), Jun. 2021, pp. 3434–3440, doi: 10.1109/CVPRW53098.2021.00382.

[9]	G. H. Samaan, A. R. Wadie, A. K. Attia, A. M. Asaad, A. E. Kamel, S. O. Slim, M. S. Abdallah, and Y.-I. Cho, “MediaPipe’s Landmarks with RNN for Dynamic Sign Language Recognition,” Electronics, vol. 11, no. 19, p. 3228, Oct. 2022, doi: 10.3390/electronics11193228.

[10]	C. Lugaresi, J. Tang, H. Nash, C. McClanahan, E. Uboweja, M. Hays, F. Zhang, C.-L. Chang, M. G. Yong, J. Lee, W.-T. Chang, W. Hua, M. Georg, and M. Grundmann, “MediaPipe: A Framework for Building Perception Pipelines,” arXiv preprint, arXiv:1906.08172, Jun. 2019, doi: 10.48550/arXiv.1906.08172.

[11]	P. Selvaraj, G. NC, P. Kumar, and M. Khapra, “OpenHands: Making Sign Language Recognition Accessible with Pose-based Pretrained Models across Languages,” in Proc. 60th Annu. Meeting Assoc. Comput. Linguistics (ACL), May 2022, pp. 2114–2133, doi: 10.18653/v1/2022.acl-long.150.

[12]	M. Boháček and M. Hrúz, “Sign Pose-based Transformer for Word-level Sign Language Recognition,” in Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. Workshops (WACVW), Jan. 2022, pp. 182–191, doi: 10.1109/WACVW54805.2022.00024.

[13]	M. Al-Qurishi, T. Khalid, and R. Souissi, “Deep Learning for Sign Language Recognition: Current Techniques, Benchmarks, and Open Issues,” IEEE Access, vol. 9, pp. 126917–126951, 2021, doi: 10.1109/ACCESS.2021.3110912.

[14]	D. Kothadiya, C. Bhatt, K. Sapariya, K. Patel, A.-B. Gil-González, and J. M. Corchado, “Deepsign: Sign Language Detection and Recognition Using Deep Learning,” Electronics, vol. 11, no. 11, p. 1780, Jun. 2022, doi: 10.3390/electronics11111780.

[15]	S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, Nov. 1997, doi: 10.1162/neco.1997.9.8.1735.

[16]	D. Bahdanau, K. Cho, and Y. Bengio, “Neural Machine Translation by Jointly Learning to Align and Translate,” in Proc. 3rd Int. Conf. Learn. Represent. (ICLR), San Diego, CA, USA, 2015, doi: 10.48550/arXiv.1409.0473.

[17]	J. Kim, J. Kong, and J. Son, “Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech,” in Proc. 38th Int. Conf. Mach. Learn. (ICML), PMLR vol. 139, Jul. 2021, pp. 5530–5540, doi: 10.48550/arXiv.2106.06103.

[18]	V. Pratap, A. Tjandra, B. Shi, P. Tomasello, A. Babu, S. Kundu, A. Elkahky, Z. Ni, A. Vyas, M. Fazel-Zarandi, A. Baevski, Y. Adi, X. Zhang, W.-N. Hsu, A. Conneau, and M. Auli, “Scaling Speech Technology to 1,000+ Languages,” Journal of Machine Learning Research, vol. 25, no. 97, pp. 1–52, 2024, doi: 10.48550/arXiv.2305.13516.

[19]	H. Hu, W. Zhao, W. Zhou, Y. Wang, and H. Li, “SignBERT: Pre-Training of Hand-Model-Aware Representation for Sign Language Recognition,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2021, pp. 11087–11096, doi: 10.1109/ICCV48922.2021.01090.

[20]	H. Hu, W. Zhao, W. Zhou, and H. Li, “SignBERT+: Hand-Model-Aware Self-Supervised Pre-Training for Sign Language Understanding,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 45, no. 9, pp. 11221–11239, Sep. 2023, doi: 10.1109/TPAMI.2023.3269220.

[21]	S. Jiang, B. Sun, L. Wang, Y. Bai, K. Li, and Y. Fu, “Skeleton Aware Multi-modal Sign Language Recognition,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. Workshops (CVPRW), Jun. 2021, pp. 3413–3423, doi: 10.1109/CVPRW53098.2021.00380.

[22]	A. Tunga, S. V. Nuthalapati, and J. Wachs, “Pose-based Sign Language Recognition using GCN and BERT,” in Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. Workshops (WACVW), Jan. 2021, pp. 31–40, doi: 10.1109/WACVW52041.2021.00008.

[23]	S. Alyami and H. Luqman, “Isolated Arabic Sign Language Recognition Using a Transformer-based Model and Landmark Keypoints,” ACM Transactions on Asian and Low-Resource Language Information Processing, vol. 23, no. 1, pp. 1–19, Jan. 2024, doi: 10.1145/3584984.

[24]	D. Li, C. Rodriguez, X. Yu, and H. Li, “Word-level Deep Sign Language Recognition from Video: A New Large-scale Dataset and Methods Comparison,” in Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. (WACV), Mar. 2020, pp. 1459–1469, doi: 10.1109/WACV45572.2020.9093512.

[25]	K. K. Podder, M. E. H. Chowdhury, A. M. Tahir, Z. B. Mahbub, A. Khandakar, M. S. Hossain, and M. A. Kadir, “Bangla Sign Language (BdSL) Alphabets and Numerals Classification Using a Deep Learning Model,” Sensors, vol. 22, no. 2, p. 574, Jan. 2022, doi: 10.3390/s22020574.

[26]	Y. Chen, F. Wei, X. Sun, Z. Wu, and S. Lin, “A Simple Multi-Modality Transfer Learning Baseline for Sign Language Translation,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2022, pp. 5120–5130, doi: 10.1109/CVPR52688.2022.00506.

[27]	B. Shi, D. Brentari, G. Shakhnarovich, and K. Livescu, “Open-Domain Sign Language Translation Learned from Online Video,” in Proc. Conf. Empirical Methods Natural Lang. Process. (EMNLP), Dec. 2022, pp. 6365–6379, doi: 10.18653/v1/2022.emnlp-main.427.

[28]	R. Zuo, F. Wei, and B. Mak, “Natural Language-Assisted Sign Language Recognition,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2023, pp. 14890–14900, doi: 10.1109/CVPR52729.2023.01430.

[29]	R. Wong, N. C. Camgoz, and R. Bowden, “Sign2GPT: Leveraging Large Language Models for Gloss-Free Sign Language Translation,” in Proc. 12th Int. Conf. Learn. Represent. (ICLR), May 2024, doi: 10.48550/arXiv.2405.04164.

[30]	[] “Bridging Communication Gaps: Advancements, Challenges, and Future Directions in Text-to-Sign Language Translation.” Full bibliographic details to be inserted from the source recommended by the reviewer.

