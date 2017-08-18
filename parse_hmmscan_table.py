#!/usr/bin/env python

import numpy as np
import pandas as pd

# Clean up the Resfams.tbl file by making it tab delimited and 
# stripping off the header, footer, and small woodland creatures 
# that inhabit it. Save to Resfams.tsv.
print("reprocessing the hmmscan table to a tab separated value file that is clean")
with open('Resfams.tbl', 'rt') as input, open('Resfams.tsv', 'wt') as output:
    line_no = 1;
    for line in input:
        fields = line.split()
        if fields:
            if fields[0][0] != '#':
                if len(fields) < 19:
                    raise Exception("Incorrect number of fields", "Line %d has fewer than 19 fields after initial split" % line_no)
                else:
                    for field in fields[:18]:
                        output.write("%s\t" % field.replace('"', ''))
                    for field in fields[18:len(fields)-1]:
                        output.write("%s " % field.replace('"', ''))
                    output.write("%s\n" % fields[len(fields)-1].replace('"', ''))
            else:
                pass
        line_no += 1

# Read the modified table using the fixed width reader. 
# Note we manually specify the dtypes and column names 
# and skip the header and footer. Bummer.
print("read the reprocessed tsv file")
df = pd.read_csv('Resfams.tsv', sep='\t',
                    header=None, error_bad_lines=False, 
                    warn_bad_lines=True, 
                    names=[ "target", "target_accession", "query",
                        "query_accesion", "full_evalue", "full_score",
                        "full_bias", "best_evalue", "best_score", "best_bias",
                        "exp", "reg", "clu", "ov", "env",
                        "dom", "rep", "inc", "description"],
                    dtype={ "target" : object, "target_accession" : object,
                        "query" : object, "query_accesion" : object, 
                        "full_evalue" : np.float64, "full_score" : np.float64,
                        "full_bias" : np.float64, "best_evalue" : np.float64,
                        "best_score" : np.float64, "best_bias" : np.float64, 
                        "exp" : np.float64, "reg" : np.float64, 
                        "clu" : np.int64, "ov" : np.int64, "env" : np.int64,
                        "dom" : np.int64, "rep" : np.int64, "inc" : np.int64,
                        "description" : object, })

# Clean up the query field
def extract_query(s):
    return s.split("|")[1]
df["query"] = df["query"].apply(extract_query)

# For each match, find the minimum value using a groupby
print("finding the minimum evalue for each query sequence")
df_min_evalue = df.loc[df.groupby("query")["full_evalue"].idxmin()]
print(df_min_evalue.shape)
print("saving to tsv")
df_min_evalue.to_csv('hmmscan_min_evalue.tsv', sep='\t', index=False)
