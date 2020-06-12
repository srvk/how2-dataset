from .metric import Metric
from .multibleu import BLEUScorer
from .sacrebleu import SACREBLEUScorer
from .wer import WERScorer
from .cer import CERScorer
from .rouge import ROUGEScorer

beam_metrics = ["BLEU", "SACREBLEU", "WER", "CER", "ROUGE"]

metric_info = {
    'BLEU': 'max',
    'SACREBLEU': 'max',
    'ROUGE': 'max',
    'LOSS': 'min',
    'WER': 'min',
    'CER': 'min',
}
