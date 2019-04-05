# How2 Dataset
This repository contains code and meta-data to (re-)create the *How2 dataset* as described in the following paper:

Ramon Sanabria, Ozan Caglayan, Shruti Palaskar, Desmond Elliott, Loic Barrault, Lucia Specia, and Florian Metze. How2: A large-scale dataset for multimodal language understanding. In Proceedings [Visually Grounded Interaction and Language (ViGIL)](https://nips2018vigil.github.io), Montreal; Canada, December 2018. Neural Information Processing Society (NeurIPS). https://arxiv.org/abs/1811.00347.

Please cite the following paper in all academic work that uses this dataset:
```
@inproceedings{sanabria18how2,
  title = {{How2:} A Large-scale Dataset For Multimodal Language Understanding},
  author = {Sanabria, Ramon and Caglayan, Ozan  and Palaskar, Shruti and Elliott, Desmond and Barrault, Lo\"ic and Specia, Lucia and Metze, Florian},
  booktitle = {Proceedings of the Workshop on Visually Grounded Interaction and Language (ViGIL)},
  year = {2018},
  organization={NeurIPS},
  url = {http://arxiv.org/abs/1811.00347}
}
```

We also acknowledge earlier work on the same data:

 - Shoou-I Yu, Lu Jiang, and Alexander Hauptmann. Instructional Videos for Unsupervised Harvesting and Learning of Action Examples. In Proc. 22nd ACM International Conference on Multimedia; Orlando, FL; U.S.A.; 2014. ACM. http://doi.acm.org/10.1145/2647868.2654997.

## How2 Download
The corpus consists of around 80,000 instructional videos (about 2,000 hours) with associated English sub-titles and summaries. About 300 hours have also been translated into Portuguese using crowd-sourcing, and used during the [JSALT 2018 Workshop](https://www.clsp.jhu.edu/workshops/18-workshop/grounded-sequence-sequence-transduction). A larger version will be released soon.

You can obtain the corpus in one of two ways:

### (Option 1): Download a pre-packaged version

You can download a pre-packaged version of all the necessary files by filling in a [form](https://docs.google.com/forms/d/e/1FAIpQLSfW2i8UnjuoH2KKSU0BvcKRbhnk_vL3HcNlM0QLsJGb_UEDVQ/viewform?usp=pp_url).

To receive the Portuguese translations, please also fill in this form and request the "translation package".

The aforementioned form will ask for the following informations:

- confirm that you understand that the download is a short-cut to getting the features only
- ask if you want the video features, audio features, text features, or the Portuguese translations (select one or many)
- then it will give you instructions on how to obtain the desired data

### (Option 2): Reproducible Pipeline

Proceed from [here](/reproduce/300h/README.md)

## How2 run
The results in the dataset paper can be reproduced using the [nmtpytorch](https://github.com/lium-lst/nmtpytorch).
We will provide the necessary instructions and configuration files shortly.

## How2 help
Please use the `issues` ticket system (https://github.com/srvk/how2-dataset/issues) to ask questions and get clarification.

## How2 license
License information for every video can be found in the `.info.json` file that is being downloaded for every video.
At the time of release, all videos included in this dataset were being made available by the original content providers under the Standard YouTube License.

The contents of this repository are being made available under the Creative Commons License (data) and/ or BSD-2 (software).
