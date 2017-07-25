#!/usr/bin/env python

import gzip

from Bio import SeqIO

with gzip.open("plasmid/plasmid.1.protein.faa.gz", "rt") as handle:
    record_dict = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
    print(record_dict["NP_775035.1"])
