DROP TABLE IF EXISTS hmmscan_min_evalue;
CREATE TABLE `hmmscan_min_evalue` (
		  `target` VARCHAR(256),
		  `target_accession` VARCHAR(256),
		  `query` VARCHAR(256),
		  `query_accesion` VARCHAR(256),
		  `full_evalue` double DEFAULT NULL,
		  `full_score` double DEFAULT NULL,
		  `full_bias` double DEFAULT NULL,
		  `best_evalue` double DEFAULT NULL,
		  `best_score` double DEFAULT NULL,
		  `best_bias` double DEFAULT NULL,
		  `exp` double DEFAULT NULL,
		  `reg` double DEFAULT NULL,
		  `clu` bigint(20) DEFAULT NULL,
		  `ov` bigint(20) DEFAULT NULL,
		  `env` bigint(20) DEFAULT NULL,
		  `dom` bigint(20) DEFAULT NULL,
		  `rep` bigint(20) DEFAULT NULL,
		  `inc` bigint(20) DEFAULT NULL,
		  `description` VARCHAR(256),
		  INDEX `query_I` (`query`)
);

LOAD DATA LOCAL INFILE 'hmmscan_min_evalue.tsv' INTO TABLE hmmscan_min_evalue
	FIELDS TERMINATED BY '\t'
	LINES TERMINATED BY '\n'
	IGNORE 1 LINES;

SELECT CONCAT("hmmscan_min_evalue table has ", COUNT(*), " rows") FROM hmmscan_min_evalue;

SELECT * FROM hmmscan_min_evalue LIMIT 5;

DROP TABLE IF EXISTS release_catalog;
CREATE TABLE `release_catalog` (
		  `taxid` bigint(20),
		  `organism` VARCHAR(256),
		  `id` VARCHAR(256),
		  `gi` bigint(20) PRIMARY KEY NOT NULL,
		  `db` VARCHAR(256),
		  `status` VARCHAR(256),
		  `length` bigint(20) DEFAULT NULL,
		  INDEX `organism_I` (`organism`),
		  INDEX `id_I` (`id`),
		  INDEX `taxid_I` (`taxid`)
);

LOAD DATA LOCAL INFILE '/work/data/NCBI_plasmids/plasmids.catalog' INTO TABLE release_catalog
	FIELDS TERMINATED BY '\t'
	LINES TERMINATED BY '\n';

SELECT CONCAT("release_catalog table has ", COUNT(*), " rows") FROM release_catalog;

SELECT * FROM release_catalog LIMIT 5;

DROP TABLE IF EXISTS hmmscan_min_evalue_release_catalog;
CREATE TABLE hmmscan_min_evalue_release_catalog AS
	SELECT * FROM hmmscan_min_evalue AS h
		INNER JOIN release_catalog AS o ON h.query = o.id
		INNER JOIN lineages AS l ON o.taxid = l.tax_id
;

SELECT CONCAT("hmmscan_min_evalue_release_catalog table has ", COUNT(*), " rows") FROM hmmscan_min_evalue_release_catalog;

SELECT * FROM hmmscan_min_evalue_release_catalog LIMIT 5;

DROP TABLE IF EXISTS lineages;
CREATE TABLE `lineages` (
		  `tax_id` bigint(20) PRIMARY KEY NOT NULL,
		  `superkingdom` VARCHAR(256),
		  `phylum` VARCHAR(256),
		  `class` VARCHAR(256),
		  `order` VARCHAR(256),
		  `family` VARCHAR(256),
		  `genus` VARCHAR(256),
		  `species` VARCHAR(256),
		  `cohort` VARCHAR(256),
		  `forma` VARCHAR(256),
		  `infraclass` VARCHAR(256),
		  `infraorder` VARCHAR(256),
		  `kingdom` VARCHAR(256),
		  `no rank` VARCHAR(256),
		  `no rank1` VARCHAR(256),
		  `no rank10` VARCHAR(256),
		  `no rank11` VARCHAR(256),
		  `no rank12` VARCHAR(256),
		  `no rank13` VARCHAR(256),
		  `no rank14` VARCHAR(256),
		  `no rank15` VARCHAR(256),
		  `no rank16` VARCHAR(256),
		  `no rank17` VARCHAR(256),
		  `no rank18` VARCHAR(256),
		  `no rank19` VARCHAR(256),
		  `no rank2` VARCHAR(256),
		  `no rank20` VARCHAR(256),
		  `no rank21` VARCHAR(256),
		  `no rank22` VARCHAR(256),
		  `no rank3` VARCHAR(256),
		  `no rank4` VARCHAR(256),
		  `no rank5` VARCHAR(256),
		  `no rank6` VARCHAR(256),
		  `no rank7` VARCHAR(256),
		  `no rank8` VARCHAR(256),
		  `no rank9` VARCHAR(256),
		  `parvorder` VARCHAR(256),
		  `species group` VARCHAR(256),
		  `species subgroup` VARCHAR(256),
		  `subclass` VARCHAR(256),
		  `subfamily` VARCHAR(256),
		  `subgenus` VARCHAR(256),
		  `subkingdom` VARCHAR(256),
		  `suborder` VARCHAR(256),
		  `subphylum` VARCHAR(256),
		  `subspecies` VARCHAR(256),
		  `subtribe` VARCHAR(256),
		  `superclass` VARCHAR(256),
		  `superfamily` VARCHAR(256),
		  `superorder` VARCHAR(256),
		  `superphylum` VARCHAR(256),
		  `tribe` VARCHAR(256),
		  `varietas` VARCHAR(256),
		  INDEX `species_I` (`species`)
);

LOAD DATA LOCAL INFILE 'lineages-2017-08-07.csv' INTO TABLE lineages
	FIELDS TERMINATED BY ','
	LINES TERMINATED BY '\n'
	IGNORE 1 LINES;

SELECT CONCAT("lineages table has ", COUNT(*), " rows") FROM lineages;

SELECT * FROM lineages LIMIT 5;

DROP TABLE IF EXISTS master;
CREATE TABLE master AS
	SELECT * FROM hmmscan_min_evalue AS h
		INNER JOIN release_catalog AS o ON h.query = o.id
		INNER JOIN lineages AS l ON o.taxid = l.tax_id
;

SELECT CONCAT("master table has ", COUNT(*), " rows") FROM master;

SELECT * FROM master LIMIT 5;
