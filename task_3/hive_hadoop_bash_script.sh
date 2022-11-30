## Put file 'downloaded_files.csv' to hdfs:
## Put file 'downloaded_files.csv' to hdfs:

## from local
docker exec -it namenode /bin/bash

## from Hadoop namenode
cd home && mkdir testSber
hadoop fs -mkdir /test
exit

## from local
docker cp /path/to/downloaded_files.csv namenode:/home/testSber/
docker exec -it namenode /bin/bash

## from Hadoop namenode:
cd home/testSber
hadoop fs -put downloaded_files.csv /test/
## screen_01_hdfs_browse


## Put file 'downloaded_files.csv' to hive:

## from local
docker exec -it docker-hive-hive-server-1 /bin/bash

## from Hive docker-hive-hive-server-1:
cd home && mkdir testDb
hadoop fs -mkdir /testSberHive
exit

## from local:
docker cp /path/to/downloaded_files.csv docker-hive-hive-server-1:/home/testDb/
docker exec -it docker-hive-hive-server-1: /bin/bash

## from Hive docker-hive-hive-server-1:
cd home/testDb/
hdfs dfs -put downloaded_files.csv /testSberHive/
hive

## goto hive db interface:
create database test_sber;
use test_sber;
create table downloaded_files (id int, zip_file_name string) row format delimited fields terminated by ',' ;
## need preprocessing of csv file to drop headers:
LOAD DATA INPATH '/testSberHive/downloaded_files.csv' INTO TABLE downloaded_files;
SELECT * FROM downloaded_files LIMIT 10;
## screen_02_hive_table_select
