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


# foreach sample
#  crop_list = [region1.jpg, region2.jpg ..]


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
    parser.add_argument('--attns', nargs='+',
                        help='Names of attentions that might me in the model.')

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
        img_att = [[] for _ in range(batch.size)]

        # Textual attention
        txt_att = [[] for _ in range(batch.size)]

        if 'attns' in args:
            other_atts = [
                {name: [] for name in args.attns} for _ in range(batch.size)]
        else:
            other_atts = [None for _ in range(batch.size)]

        batch_hyps = [[] for _ in range(batch.size)]

        batch_src = batch[model.sl].data.cpu().t().tolist()
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
            if hasattr(model.dec, 'txt_alpha_t'):
                tatt = model.dec.txt_alpha_t.cpu().data.clone().numpy()
            else:
                tatt = None

            # If decoder has .img_alpha_t
            if hasattr(model.dec, 'img_alpha_t'):
                iatt = model.dec.img_alpha_t.cpu().data.clone().numpy()
            else:
                iatt = None

            if hasattr(model.dec, 'att_history') and 'attns' in args:
                other_atts_t = {
                    name: att.cpu().data.clone().numpy()
                    for name, att in model.dec.att_history.items()}
            else:
                other_atts_t = None

            if hasattr(model, 'coattention') and hasattr(model.coattention, 'affinity_matrix'):
                affinity = model.coattention.affinity_matrix.cpu().data.clone().numpy()
            else:
                affinity = [None for _ in range(batch.size)]

            top_scores, y_t = logp.data.topk(1, largest=True)
            hyp = y_t.cpu().numpy().tolist()
            for idx, w in enumerate(hyp):
                if 2 not in batch_hyps[idx]:
                    batch_hyps[idx].append(w[0])
                    if tatt is None:
                        txt_att[idx].append(None)
                    else:
                        txt_att[idx].append(tatt[:, idx])
                    if iatt is None:
                        img_att[idx].append(None)
                    else:
                        img_att[idx].append(iatt[:, idx])

                    if other_atts_t is None:
                        pass
                    else:
                        for att_name, att in other_atts_t.items():
                            other_atts[idx][att_name].append(att[:, idx])

            # Did we finish? (2 == <eos>)
            fini = fini | y_t.eq(2).squeeze().long()
            if fini.sum() == batch.size:
                break

        data.extend(zip(batch_src, batch_hyps, txt_att, img_att,
                        other_atts, affinity))

    # Put into correct order
    data = [data[i] for i, j in sorted(
        enumerate(loader.batch_sampler.orig_idxs), key=lambda k: k[1])]
    # Sort by increasing length
    data = sorted(data, key=lambda x: len(x[0]))

    with open('{}.greedy.pkl'.format(args.output), 'wb') as f:
        pkl.dump(data, f)
