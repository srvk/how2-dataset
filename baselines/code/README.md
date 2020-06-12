![nmtpytorch](docs/logo.png?raw=true "nmtpytorch")

This is a custom version of [nmtpytorch](https://github.com/lium-lst/nmtpytorch.git) that was used to train the baselines
in the How2 paper.

Training and testing models
---------------------------

- You can train models by providing a config file i.e. `nmtpy train -C <conf file>`
- Once you have trained the models, `nmtpy translate` can be used to transcribe speech
  or translate text regardless of the underlying model.
- `--help` flag for both command provides further details on how to manipulate these commands

