#!/usr/bin/env python

import gzip

from Bio import SeqIO
import pandas as pd

print("reading protein fastas in")

with gzip.open("plasmid/plasmid.1.protein.faa.gz", "rt") as handle:
    record_dict1 = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))

with gzip.open("plasmid/plasmid.3.protein.faa.gz", "rt") as handle:
    record_dict3 = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))

with gzip.open("plasmid/plasmid.nonredundant_protein.1.protein.faa.gz", "rt") as handle:
    record_dictnr = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))

plasmid_sequences = record_dict1.copy()
plasmid_sequences.update(record_dict3)
plasmid_sequences.update(record_dictnr)

print("creating pandas data frame from fasta data")
rows_list = []
for key in plasmid_sequences.keys():
    s = plasmid_sequences[key].description
    organism = " ".join(s[s.find("[")+1:s.find("]")].split()[:2])
    tmp_dict = {}
    tmp_dict['id'] = key
    tmp_dict['description'] = s
    tmp_dict['organism'] = organism
    rows_list.append(tmp_dict)
    
ps_df = pd.DataFrame(rows_list, columns=['id', 'description', 'organism'])

print(ps_df.head())

print("saving data frame to tsv")
ps_df.to_csv(path_or_buf='organism_table.tsv', sep='\t')
