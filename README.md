## The How-2 Dataset 

How-2 is a multimodal dataset which consists of around 80,000 instructional videos (about 2,000 hours) with associated English sub-titles and summaries. About 300 hours have also been translated into Portuguese using crowd-sourcing, and used during the [JSALT 2018 Workshop](https://www.clsp.jhu.edu/workshops/18-workshop/grounded-sequence-sequence-transduction). The How-2 training data was split into 300h and 2000h, with only the former supporting Portuguese Machine Translation. The 2000h set can be used for other tasks such as speech recognition, speech summarization, text summarization, and their multimodal extensions. 

We currently have released the following packages pertaining to the How-2 data to be able to replicate our results and encourage further research:

- ASR (300h): This release contains (audio) fbank+pitch features in Kaldi scp/ark format for 300 hours
- E2E Summ + ASR (2000h): This release contains (audio_2000) fbank+pitch features in Kaldi scp/ark format, along with transcript and abstractive summaries for 2000 hours
- Visual features: This release contains (video) Action features in numpy arrays for MT and ASR
- English Transcript: This release contains (en) English text for How2
- Portuguese Machine Translations: This release contains (pt) Portuguese crowdsource text
- English Abstractive Summaries: This release contains (en_sum) Summarization text
- Visual features for Summarization: This release contains (video_sum) Summarization action features in numpy arrays
- Object Grounding Features: This release contains (ground) Object grounding test and development set

Please fill the [Data Request form](https://docs.google.com/forms/d/e/1FAIpQLSfW2i8UnjuoH2KKSU0BvcKRbhnk_vL3HcNlM0QLsJGb_UEDVQ/viewform?usp=pp_url)


Please cite the following paper in all academic work that uses this dataset:
```
@inproceedings{sanabria18how2,
  title = {{How2:} A Large-scale Dataset For Multimodal Language Understanding},
  author = {Sanabria, Ramon and Caglayan, Ozan and Palaskar, Shruti and Elliott, Desmond and Barrault, Lo\"ic and Specia, Lucia and Metze, Florian},
  booktitle = {Proceedings of the Workshop on Visually Grounded Interaction and Language (ViGIL)},
  year = {2018},
  organization={NeurIPS},
  url = {http://arxiv.org/abs/1811.00347}
}
```

More papers can be found in the [bibliography](Bibliography.md).

To subscribe to the How2 mailing list [click here](https://lists.andrew.cmu.edu/mailman/listinfo/how-to).



## Speech Summarization

How2 has been used for end to end speech summarization- we are releasing 43 dim fbank+pitch features to support this. See our [ESPNet Recipe](https://github.com/espnet/espnet/tree/master/egs2/how2_2000h/sum1) and [paper](https://ieeexplore.ieee.org/document/9747320). Please consider citing our paper on speech summarization if you utilize this data release.

```
@inproceedings{Sharma2022, 
author={Sharma, Roshan and Palaskar, Shruti and Black, Alan W and Metze, Florian},
booktitle={ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
title={End-to-End Speech Summarization Using Restricted Self-Attention},
year={2022}, 
volume={},
number={},
pages={8072-8076},
doi={10.1109/ICASSP43922.2022.9747320}
}
```


## How2 Get Help
Please use the `issues` ticket system (https://github.com/srvk/how2-dataset/issues) to ask questions and get clarifications. 

## How2 License
License information for every video can be found in the `.info.json` file that is being downloaded for every video.
At the time of release, all videos included in this dataset were being made available by the original content providers under the standard [YouTube License](https://www.youtube.com/static?template=terms).

Unless noted otherwise, we are providing the contents of this repository under the [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (Attribution-Share-Alike) License (for data-like content) and/ or [BSD-2-Clause License](https://opensource.org/licenses/BSD-2-Clause) (for software-type content).





## How2 Baseline Setup and Experiment Reproduction

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




