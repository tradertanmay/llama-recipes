# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from tqdm import tqdm
from itertools import chain

from torch.utils.data import Dataset

import torch.nn.functional
from torch.utils.data import Dataset
import torch

class ConcatDataset(Dataset):
    def __init__(self, dataset, chunk_size=4096):
        self.dataset = dataset
        self.chunk_size = chunk_size
        self.samples = []

        buffer = {
            "input_ids": [],
            "attention_mask": [],
            "labels": [],
        }

        for sample in tqdm(self.dataset, desc="Preprocessing dataset", dynamic_ncols=True):
            for key in buffer.keys():
                if isinstance(sample[key], list):
                    buffer[key].extend(sample[key])
                else:
                    buffer[key].append(sample[key])

            while len(buffer["input_ids"]) > self.chunk_size:
                chunk = {
                    "input_ids": buffer["input_ids"][:self.chunk_size],
                    "attention_mask": buffer["attention_mask"][:self.chunk_size],
                    "labels": torch.tensor(buffer["labels"][:self.chunk_size]),  # Integer labels directly
                }

                self.samples.append(chunk)

                buffer["input_ids"] = buffer["input_ids"][self.chunk_size:]
                buffer["attention_mask"] = buffer["attention_mask"][self.chunk_size:]
                buffer["labels"] = buffer["labels"][self.chunk_size:]
                print("Buffer Shapes - Input IDs:", buffer["input_ids"])
                print("Buffer Shapes - Attention Mask:", buffer["attention_mask"])
                print("Buffer Shapes - Labels:", buffer["labels"])


    def __getitem__(self, idx):
        print("Buffer Shapes - Input IDs:", buffer["input_ids"])
        print("Buffer Shapes - Attention Mask:", buffer["attention_mask"])
        print("Buffer Shapes - Labels:", buffer["labels"])

        return self.samples[idx]

    def __len__(self):
        return len(self.samples)
