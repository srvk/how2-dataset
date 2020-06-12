# Baseline Experiments

The model configuration files provided under `configs/` are used to construct
the baselines provided in the paper. These models were trained with a
special version (1.5.0) of `nmtpytorch` that is provided under `code/`.
This codebase relies on pytorch `0.3.1` and the newer versions of `nmtpytorch`
does not support these models out-of-the-box.

The config files require setting paths to provided feature files, do not forget
to adjust them according to your needs. The visual adaptation models would also
require pretrained checkpoints in order to apply the finetuning. These checkpoints
are determined with the `pretrained_file` option in the configuration files.

We provide the training logs of each model with 3 random runs under the `logs/` folder
for further reference.

Finally, these configurations are provided as reference and results may change
depending on random seeds, pytorch version, data pre-processing and so on.
