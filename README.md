## November 16th Update

## NEW: How2 has been used for end to end speech summarization- we are releasing 43 dim fbank+pitch features to support this. See our [ESPNet Recipe](https://github.com/espnet/espnet/tree/master/egs2/how2_2000h/sum1) and [paper](https://ieeexplore.ieee.org/document/9747320). Please fill the form to request this data. 






## NEW: How2 will be part of the [IWSLT 2019 speech to text evaluation](https://sites.google.com/view/iwslt-evaluation-2019/speech-translation).
## NEW: Unsupervised Object Recognition Grounding labels for development and test set! [check here](https://docs.google.com/forms/d/e/1FAIpQLSfW2i8UnjuoH2KKSU0BvcKRbhnk_vL3HcNlM0QLsJGb_UEDVQ/viewform?usp=pp_url).
## NEW: Please check out the [How2 Challenge Workshop at ICML 2019](https://srvk.github.io/how2-challenge/).

# How2 Dataset
This repository contains code and meta-data to (re-)create the *How2 dataset* as described in the following paper:

Ramon Sanabria, Ozan Caglayan, Shruti Palaskar, Desmond Elliott, Loic Barrault, Lucia Specia, and Florian Metze. How2: A large-scale dataset for multimodal language understanding. In Proceedings [Visually Grounded Interaction and Language (ViGIL)](https://nips2018vigil.github.io), Montreal; Canada, December 2018. Neural Information Processing Society (NeurIPS). https://arxiv.org/abs/1811.00347.

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

We also acknowledge earlier work (including first-time data collection) on the same data (and encourage you to do the same):

 - Shoou-I Yu, Lu Jiang, and Alexander Hauptmann. Instructional Videos for Unsupervised Harvesting and Learning of Action Examples. In Proc. 22nd ACM International Conference on Multimedia; Orlando, FL; U.S.A.; 2014. ACM. http://doi.acm.org/10.1145/2647868.2654997.

More papers can be found in the [bibliography](Bibliography.md).

To subscribe to the How2 mailing list [click here](https://lists.andrew.cmu.edu/mailman/listinfo/how-to).

## How2 Download
The corpus consists of around 80,000 instructional videos (about 2,000 hours) with associated English sub-titles and summaries. About 300 hours have also been translated into Portuguese using crowd-sourcing, and used during the [JSALT 2018 Workshop](https://www.clsp.jhu.edu/workshops/18-workshop/grounded-sequence-sequence-transduction). We are working on releasing a larger version - please let us know if you are interested.

You can obtain the corpus in one of two ways:

### (Option 1): Download a pre-packaged version

You can download a pre-packaged version of all the necessary files by filling in a [form](https://docs.google.com/forms/d/e/1FAIpQLSfW2i8UnjuoH2KKSU0BvcKRbhnk_vL3HcNlM0QLsJGb_UEDVQ/viewform?usp=pp_url).

To receive the Portuguese translations, please fill in this form and request the "translation package".

The aforementioned form will ask for the following informations:

- confirm that you understand that the download is a short-cut to getting the features only
- ask if you want the video features, audio features, text features, or the Portuguese translations (select one or many)
- then it will give you instructions on how to obtain the desired data

### (Option 2): Reproducible pipeline

Proceed from [here](/reproduce/300h/README.md)

## How2 Run
 - The results in the dataset paper can be reproduced using a custom version of [nmtpytorch](https://github.com/lium-lst/nmtpytorch) that is provided under `baselines/code`.
 - Configuration files for speech recognition, speech translation, and machine translation; along with their visual adaptation
   counterparts are provided under `baselines/configs`.

## How2 Evaluate
Here are instructions on how to score and submit our three challenge tasks. Report scores on the `test` set for each task.

### ASR

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



## How2 Get Help
Please use the `issues` ticket system (https://github.com/srvk/how2-dataset/issues) to ask questions and get clarification. You can also [send email](mailto:how2challenge@gmail.com).

## How2 License
License information for every video can be found in the `.info.json` file that is being downloaded for every video.
At the time of release, all videos included in this dataset were being made available by the original content providers under the standard [YouTube License](https://www.youtube.com/static?template=terms).

Unless noted otherwise, we are providing the contents of this repository under the [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (Attribution-Share-Alike) License (for data-like content) and/ or [BSD-2-Clause License](https://opensource.org/licenses/BSD-2-Clause) (for software-type content).

