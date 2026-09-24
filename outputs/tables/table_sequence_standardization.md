### table_sequence_standardization

What the 60-frame window actually does to this corpus. If most of the window is padding, two things follow for the manuscript: the input Masking layer and the attention mask are doing real work rather than being a formality, and the choice of T = 60 deserves a sentence of justification. The ablation section measures uniform temporal resampling as the alternative.

