#!/usr/bin/env python

import pandas as pd

lineages_table = pd.read_csv('lineages-2017-08-07.csv.gz')
print(lineages_table.head())

organism_table = pd.read_csv('organism_table.tsv', sep='\t')
print(organism_table.head())
