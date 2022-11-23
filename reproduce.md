

## How2 Baseline Setup and Experiment Reproduction for 300h ASR,MT,Summ

Proceed from [here](/reproduce/300h/README.md)

# How2 Run
 - The results in the dataset paper can be reproduced using a custom version of [nmtpytorch](https://github.com/lium-lst/nmtpytorch) that is provided under `baselines/code`.
 - Configuration files for speech recognition, speech translation, and machine translation; along with their visual adaptation
   counterparts are provided under `baselines/configs`.

# How2 Evaluation
Here are instructions on how to score and submit our three challenge tasks. Report scores on the `test` set for each task.

# ASR

Dependencies:
- [sclite](http://www1.icsi.berkeley.edu/Speech/docs/sctk-1.2/sclite.htm)

You can find a hypothesis example corresponding to the system with `18.4 WER` of Table 2 of [2019 Caglayan et al.](https://arxiv.org/pdf/1811.03865.pdf) in `./test/hyp.filtered.word.wer.r5f045.max150.dev5.beam10.sclite`.  

To score this hypothesis, you should execute the following command

```
sclite  -r ./eval/asr/dev5.filtered.en -h ./eval/asr/hyp.filtered.word.wer.r5f045.max150.dev5.beam10.sclite -i spu_id -f 0 -o sum stdout dtl pra | grep Sum/Avg | awk '{print $11}'
```

It should return


```
18.4
```

### Machine Translation and Summarization
We use the nmtpy-coco-metrics package for this evaluation. Report the BLEU scores for MT and Rouge-L scores for summarization.

Installation steps:
- pip install nmtpytorch

This will install all packages needed for this evaluation. You can find a demo hypothesis file from the summarization models described in Table 2 of [Libovicky et al. 2018](https://nips2018vigil.github.io/static/papers/accepted/8.pdf) in `./eval/summarization/demo.test.hypothesis`.

To score this hypothesis, you should execute the following command

```
nmtpy-coco-metrics ./eval/summarization/demo.test.hypothesis -r ./eval/summarization/demo.test.reference
```

It should return (Rouge-L)


```
31.2
```



