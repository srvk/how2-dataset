#!/usr/bin/env python
import argparse

from pathlib import Path

from nmtpytorch.translator import Translator
from nmtpytorch.utils.data import make_dataloader

import numpy as np
import torch
import pickle as pkl

from torch.autograd import Variable

import tqdm



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='nmtpy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="generate attention info",
        argument_default=argparse.SUPPRESS)

    parser.add_argument('-m', '--model', type=str, required=True,
                        help=".ckpt model file")
    parser.add_argument('-s', '--split', type=str,
                       help='test_set name given as in configuration file')
    parser.add_argument('-o', '--output', type=str,
                       help='output file name.')

    args = parser.parse_args()
    translator = Translator(models=[args.model], splits=args.split,
                            source=None, disable_filters=False, att_temp=1.0)

    model = translator.instances[0]

    dataset = model.load_data(args.split, 96, mode='beam')
    loader = make_dataloader(dataset)
    data = []

    # Greedy search
    for batch in tqdm.tqdm(loader, unit='batch'):
        batch.to_gpu(volatile=True)

        # Visual attention (may not be available)
        img_att = [[] for i in range(batch.size)]

        # Textual attention
        spc_att = [[] for i in range(batch.size)]

        # Hierarchical attention
        hie_att = [[] for i in range(batch.size)]

        hyps = [[] for i in range(batch.size)]

        fini = torch.zeros(batch.size).long().cuda()
        ctx_dict = model.encode(batch)

        # Get initial hidden state
        h_t = model.dec.f_init(ctx_dict)

        y_t = model.get_bos(batch.size).cuda()

        # Iterate for 100 timesteps
        for t in range(100):
            y_t = Variable(y_t, volatile=True).cuda()
            logp, h_t = model.dec.f_next(ctx_dict, model.dec.emb(y_t), h_t)

            # text attention
            tatt = model.dec.txt_alpha_t.cpu().data.clone().numpy()

            # If decoder has .img_alpha_t
            if hasattr(model.dec, 'img_alpha_t'):
                iatt = model.dec.img_alpha_t.cpu().data.clone().numpy()
            else:
                iatt = None

            if 'hier' in model.dec.att_history:
                hatt = model.dec.att_history['hier'].cpu().data.clone().numpy()
            else:
                hatt = None

            top_scores, y_t = logp.data.topk(1, largest=True)
            hyp = y_t.cpu().numpy().tolist()
            for idx, w in enumerate(hyp):
                if 2 not in hyps[idx]:
                    hyps[idx].append(w[0])
                    spc_att[idx].append(tatt[:, idx])
                    if iatt is None:
                        img_att[idx].append(None)
                    else:
                        img_att[idx].append(iatt[:, idx])

                    if hatt is None:
                        hie_att[idx].append(None)
                    else:
                        hie_att[idx].append(hatt[:, idx])


            # Did we finish? (2 == <eos>)
            fini = fini | y_t.eq(2).squeeze().long()
            if fini.sum() == batch.size:
                break

        for h, sa, ia, ha in zip(hyps, spc_att, img_att, hie_att):
            data.append((model.trg_vocab.idxs_to_sent(h), sa, ia, ha))

    # Put into correct order
    data = [data[i] for i, j in sorted(
        enumerate(loader.batch_sampler.orig_idxs), key=lambda k: k[1])]

    with open('{}.greedy.pkl'.format(args.output), 'wb') as f:
        pkl.dump(data, f)
