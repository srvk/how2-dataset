#!/usr/bin/env python

from collections import defaultdict
import sys
import torch
import argparse

from nmtpytorch import models
from nmtpytorch.config import Options
from nmtpytorch.utils.misc import load_pt_file, pbar
from nmtpytorch.utils.data import make_dataloader


def save_ckpt(param_dict, fname):
    if not fname.endswith('.pt'):
        fname += '.pt'
    torch.save({'opts': {}, 'history': {}, 'model': param_dict}, fname)


def get_representation(ctx, mask, repr_type):
    if mask is None:
        if repr_type == 'last':
            return ctx[-1]
        elif repr_type == 'meanpool':
            return ctx.mean(0)
        elif repr_type == 'maxpool':
            return ctx.max(0)
        else:
            return ctx


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='nmtpy-dump-features')
    parser.add_argument('-o', '--output-file', type=str, required=True,
                        help='Output file name.')

    parser.add_argument('-m', '--model', type=str, required=True,
                        help='Path to model checkpoint file')

    parser.add_argument('-p', '--params', type=str, default=None,
                        help='Comma separated list of parameters to dump.')

    parser.add_argument('-l', '--list', action='store_true',
                        help='List all parameters.')

    parser.add_argument('-e', '--encode', type=str, default=None,
                        help='Encode the given test_set and dump it.')

    parser.add_argument('-t', '--encode-type', type=str, default='last',
                        help='One of last, meanpool, maxpool or seq.')

    args = parser.parse_args()

    try:
        pt_file = sys.argv[1]
    except IndexError as ie:
        print('Usage: {} <.ckpt file>'.format(sys.argv[0]))
        sys.exit(1)

    # Load the checkpoint file
    weights, history, opts = load_pt_file(args.model)
    param_list = sorted(weights.keys())
    if args.list:
        for key in param_list:
            print('{}'.format(key))
        sys.exit(0)

    if args.params is not None:
        params = args.params.split(',')
        if any(set(params).difference(param_list)):
            print('Error: Unknown parameter name requested')
            sys.exit(1)

        state_dict = {k:weights[k] for k in params}
        save_ckpt(state_dict, args.output_file)
        sys.exit(0)

    if args.encode is not None:
        # Parse the options
        opts = Options.from_dict(opts)

        # Create model instance
        instance = getattr(models, opts.train['model_type'])(opts=opts)

        # Setup layers
        instance.setup(is_train=False)
        instance.load_state_dict(weights, strict=True)
        instance.cuda()
        instance.train(False)
        dataset = instance.load_data(args.encode, 64, mode='beam')
        loader = make_dataloader(dataset)

        result = defaultdict(list)
        for batch in pbar(loader, unit='batch'):
            batch.to_gpu(volatile=True)
            ctx_dict = instance.encode(batch)
            for key, (data, mask) in ctx_dict.items():
                result[key].append(
                    get_representation(data.data.cpu().numpy(), mask, args.encode_type))
