# plasmid_search (reposotory name)

* `wget -m ftp://ftp.ncbi.nlm.nih.gov/refseq/release/plasmid` (downloading the government database of plasmids)
* `mv ftp.ncbi.nlm.nih.gov/refseq/release/plasmid .` (renaming subdirectory to root of reposotory)
* hmmer-3.1b2-macosx-intel (folder name/location with all commands for hmmer, downloadable content)

Run hmmer with:
* `hmmscan -o Resfams.log --tblout Resfams.tbl --domtblout Resfams.dom --pfamtblout Resfams.pfam --notextw hmm_databases/Resfams.hmm plasmid/plasmid.1.protein.faa.gz`
