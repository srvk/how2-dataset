# -*- coding: utf-8 -*-
import torch.nn as nn
from torch.nn import functional as F


class BiRNNPv1(nn.Module):
    """A recurrent encoder for speech features without embeddings. A batch should
    only contain samples that have the same sequence length.

    Arguments:
        input_size (int): Embedding dimensionality.
        hidden_size (int): RNN hidden state dimensionality.
        rnn_type (str): RNN Type, i.e. GRU or LSTM.
        num_base_layers (int, optional): Number of base stacked RNNs (Default: 1).
        subsample (tuple(int), optional): A tuple of state-skip values.
            The size of the tuple determines the number of RNNs to be applied
            to reduce the input size exponentially. ``None`` means no subsampling
            RNNs will be used.
        num_sub_layers(int, optional): Determines the number of stacked RNNs
            for each subsampling RNN. Default: 1.
        dropout(float, optional): Dropout rate for encoder (Default: 0.)

    Input:
        x (Variable): A variable of shape (n_timesteps, n_samples, n_feats)
            that includes acoustic features of dimension ``n_feats`` per
            each timestep (in the first dimension).

    Output:
        hs (Variable): A variable of shape (n_timesteps, n_samples, hidden)
            that contains encoder hidden states for all timesteps. If
            bidirectional, `hs` is doubled in size in the last dimension
            to contain both directional states.
        mask (Variable): A binary mask of shape (n_timesteps, n_samples)
            that may further be used in attention and/or decoder. `None`
            is returned for now as homogeneous batches are expected.
    """
    def __init__(self, input_size, hidden_size, rnn_type,
                 num_base_layers=1, subsample=(), num_sub_layers=1,
                 dropout=0):
        super().__init__()

        self.rnn_type = rnn_type.upper()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_base_layers = num_base_layers
        self.subsample = subsample
        self.num_sub_layers = num_sub_layers
        self.dropout = dropout

        # Fill 0-vector as <eos> to the end of the frames
        self.pad_tuple = (0, 0, 0, 0, 0, 1)

        # Doubles its size because of concatenation
        self.ctx_size = self.hidden_size * 2

        # Create base RNN
        # Output size -> hidden_size
        RNN = getattr(nn, self.rnn_type)
        self.base_rnn = RNN(
            self.input_size, self.hidden_size,
            self.num_base_layers, bias=True, batch_first=False,
            bidirectional=True)

        if len(self.subsample) > 0:
            self.sub_rnns = nn.ModuleList()
            for i in range(len(self.subsample)):
                self.sub_rnns.append(
                    RNN(self.ctx_size, self.hidden_size,
                        num_layers=self.num_sub_layers,
                        bias=True, batch_first=False, bidirectional=True))

        if self.dropout > 0:
            self.do = nn.Dropout(self.dropout)

    def forward(self, x):
        x = F.pad(x, self.pad_tuple)

        # Apply base RNN
        hs, _ = self.base_rnn(x)

        # Apply subsampling layers
        for i, sub_factor in enumerate(self.subsample):
            hs, _ = self.sub_rnns[i](hs[::sub_factor])

        if self.dropout > 0:
            hs = self.do(hs)

        # No mask is returned as batch contains elements of all same lengths
        return hs, None
