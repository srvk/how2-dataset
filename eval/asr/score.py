#!/usr/bin/env python
import bz2
import os
import argparse
import subprocess
from collections import defaultdict, OrderedDict
from pathlib import Path

import numpy as np
from tabulate import tabulate


SCLITE_HEADERS = ["Name", "# Snt", "# Wrd", "Corr", "Sub", "Del", "Ins", "Err", "S.Err"]
FORMAT = [None, 'g', 'g', '2.1f', '2.1f', '2.1f', '2.1f', '2.1f', '2.1f']


# Example:
# To score dev5 files and have mean/stdev table
# ./score.py -s dev5 -p hyp.filtered.word -r dev5.filtered.en
# To score val (cv05)
# ./score.py -s val -r val.en


def run_sclite(ref, hyp):
    cmd = ['sclite', '-r', str(ref), '-h', str(hyp),
           '-i', 'spu_id', '-f', '0', '-o', 'sum', 'stdout', 'dtl', 'pra']
    out = subprocess.check_output(cmd, universal_newlines=True)
    with open('{}.results'.format(hyp), 'w') as f:
        f.write(out)
    return Path('{}.results'.format(hyp))


def parse_sclite_results(fname):
    # bzgrep works with both .bz2 files and plain files
    out = subprocess.check_output(
        ['bzgrep', '-i', 'sum/avg', str(fname)], universal_newlines=True)
    scores = [float(field) for field in out.strip().split() if field[0].isdigit()]
    return scores


def get_systems(root, test_set, ref_file, metric, prefix='hyp.word', beam=20):
    scores = []
    compressed = False

    pattern = '{}.{}*.max150.{}.beam{}.sclite'.format(
        prefix, metric, test_set, beam)

    # First check for .bz2 versions, if any uncompress them
    hyps = list(Path(root).glob('*/{}.bz2'.format(pattern)))
    for hyp in hyps:
        compressed = True
        os.system('bunzip2 -k {}'.format(str(hyp)))

    # Now get plain text ones
    hyps = list(Path(root).glob('*/{}'.format(pattern)))

    for hyp in hyps:
        score = [hyp.parent]
        if compressed:
            res_file = hyp.with_suffix('.sclite.results.bz2')
        else:
            res_file = hyp.with_suffix('.sclite.results')
        if res_file.exists():
            score.extend(parse_sclite_results(res_file))
        else:
            score.extend(parse_sclite_results(run_sclite(ref_file, hyp)))
        scores.append(score)
    return scores

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='sclite')
    parser.add_argument('-b', '--beam', default=10, type=int,
                        help='Beam size')
    parser.add_argument('-m', '--metric', default='wer',
                        help='Gives the metric for which the best ckpts were created and decoded.')
    parser.add_argument('-s', '--split', default=None, type=str,
                        help='Which test split to evaluate (default: all)')
    parser.add_argument('-r', '--reffile', type=str, required=True,
                        help='Which file to use as reference for sclite')
    parser.add_argument('-p', '--prefix', type=str, default='hyp.word',
                        help='Prefix for hyp files.')
    parser.add_argument('-a', '--sort-alpha', action='store_true',
                        help='Sort alphabetically.')
    parser.add_argument('-M', '--reduce-mode', type=str, default='mean',
                        help='mean or min for multi-seed runs.')
    args = parser.parse_args()

    scores = get_systems('.', args.split, args.reffile,
                         args.metric, args.prefix, beam=args.beam)

    if any(scores):
        if args.reduce_mode:
            # break it down in case there are multiple runs
            sys_ids = [str(s[0]) for s in scores]
            new_scores = []
            for sys_id in set(sys_ids):
                # Iterate over unique system names
                stats = None
                sys_scores = np.array(
                    [s[1:] for s in scores if str(s[0]) == sys_id])
                if args.reduce_mode == 'mean':
                    # fetch WER specifically
                    wers = sys_scores[:, -2]
                    stats = '{:.2f}/{:.2f}/{:.2f} ({} runs)'.format(
                        wers.min(), wers.max(), wers.std(), sys_scores.shape[0])
                    # Compute means for all columns
                    sys_scores = sys_scores.mean(0)
                elif args.reduce_mode == 'min':
                    sys_scores = sys_scores.min(0)
                if stats is not None:
                    new_scores.append([sys_id, stats] + sys_scores.tolist())
                else:
                    new_scores.append([sys_id] + sys_scores.tolist())
            scores = new_scores

        if args.sort_alpha:
            scores = sorted(scores, key=lambda x: str(x[0]))
        else:
            scores = sorted(scores, key=lambda x: -x[-2])

        if stats is not None:
            SCLITE_HEADERS.insert(1, 'min/max/stdev WER%')
            FORMAT.insert(0, None)

        print(tabulate(scores, headers=SCLITE_HEADERS, floatfmt=FORMAT, tablefmt='pipe'))
