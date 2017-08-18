#!/usr/bin/env python

from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql://dacb@mysql/plasmid_search')
conn = engine.connect()

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

# For each match, find the minimum value using a groupby
print("finding the minimum evalue for each query sequence")
df_min_evalue = df.loc[df.groupby("query")["full_evalue"].idxmin()]
print(df_min_evalue.shape)
print("saving to sql")
df_min_evalue.to_sql('hmmscan_min_evalue', conn)

# Read in the catalog, note this is a huge file
print("reading the refseq catalog")
organism_table = pd.read_csv('RefSeq-release83.catalog.gz', sep='\t',
                            names=["taxid", "organism", "id", "gi", "db", 
                                "status", "length"],
                            dtype={ "taxid" : np.int64,
                                "organism" : object,
                                "id" : object,
                                "gi" : np.int64,
                                "db" : object,
                                "status" : object,
                                "length" : np.int64 })
print("discarding any non plasmid entities from the catalog")
organism_table = organism_table.loc[organism_table["db"].str.contains("plasmid")]
organism_table['id'] = organism_table['id'].map(lambda x: "ref|{}|".format(x))
#organism_table.to_csv('organism_table.tsv', sep='\t')
print("saving to sql")
organism_table.to_sql('organism_table', conn)

# Read in the lineages table with the taxonomy for each species
print("reading the taxonomy lineage data from NCBI")
lineages_table = pd.read_csv('lineages-2017-08-07.csv.gz', low_memory=False)
lineages_table.to_sql('lineages_table', conn)

# Join the catalog to the hmmscan data
print("joining the catalog to the hmmscan data")
#df_min_organism = df_min_evalue.merge(organism_table, how='left', left_on = 'query', right_on = 'id')
#print(df_min_organism.shape)
#df_min_organism.to_csv('hmmscan_organism.tsv', sep='\t')

# Join to the lineage file
print("joining the hmmscan data with organism annotations to the lineage table")
#df_min_organism_lineages = df_min_organism.merge(lineages_table, how = 'left', left_on = 'organism', right_on = 'species')
#print(df_min_organism_lineages.shape)
#df_min_organism_lineages.to_csv('hmmscan_organism_lineage.tsv', sep='\t')

# Process out some of the duplicates
print("cleaning the table from duplicates")
final_df = df_min_organism_lineages[
                df_min_organism_lineages['subspecies'].isnull() & 
                df_min_organism_lineages['no rank2'].isnull() & 
                df_min_organism_lineages['no rank1'].isnull()
            ]
print(final_df.shape)

# save figures
with PdfPages('figures.pdf') as pdf:
    final_df.groupby('family').query.count().plot(kind = "bar")
    pdf.savefig()
    plt.close()

    final_df.groupby('genus').query.count().plot(kind = "bar")
    pdf.savefig()
    plt.close()


# Save out the file
print("saving the result")
final_df.to_csv(path_or_buf='final_table.tsv', sep='\t')

conn.close()
