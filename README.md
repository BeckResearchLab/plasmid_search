# plasmid_search (reposotory name)

* `wget -m ftp://ftp.ncbi.nlm.nih.gov/refseq/release/plasmid` (downloading the government database of plasmids)
* `mv ftp.ncbi.nlm.nih.gov/refseq/release/plasmid .` (renaming subdirectory to root of reposotory)
* hmmer-3.1b2-macosx-intel (folder name/location with all commands for hmmer, downloadable content)

* `gzcat plasmid/plasmid.*.protein.faa.gz > plasmid/protein.faa`
* `gzip plasmid/protein.faa`
* `Created enviornment called 'biopython' and imported 'Bio'`

Run hmmer with:
* `hmmscan -o Resfams.log --tblout Resfams.tbl --domtblout Resfams.dom --pfamtblout Resfams.pfam --notextw hmm_databases/Resfams.hmm plasmid/protein.faa.gz`
OR
* `hmmscan -o Resfams.log --cut_ga --tblout Resfams.tbl --domtblout Resfams.dom --pfamtblout Resfams.pfam --notextw hmm_databases/Resfams.hmm plasmid/protein.faa.gz`

* 'then use 'df_min_evalue = df.loc[df.groupby("query")["full_evalue"].idxmin()] df_min_evalue.shape' to find the shape of data'

* 'to find the smalles evalue use 'df_min_evalue.loc[df_min_evalue["query"] == 'NP_774964.1']' (this ID is an example).'

