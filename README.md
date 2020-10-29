- [Data Lake - Udacity](#orgf9e01f3)
  - [Introduction](#org5c6ed31)
  - [Project description](#orgad1a72f)
- [Folder structure](#org9fc7204)
- [Usage](#org0ea6d02)


<a id="orgf9e01f3"></a>

# Data Lake - Udacity

This repository is intended for the the fourth project of the Udacity Data Engineering Nanodegree Programa: Data Lake.

The Introduction and project description were taken from the Udacity curriculum, since they summarize the activity better than I could.


<a id="org5c6ed31"></a>

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.


<a id="orgad1a72f"></a>

## Project description

In this project, you'll apply what you've learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. To complete the project, you will need to load data from S3, process the data into analytics tables using Spark, and load them back into S3. You'll deploy this Spark process on a cluster using AWS.


<a id="org9fc7204"></a>

# Folder structure

```
/
├── data
│   ├── log-data.zip - zip file containing a subset of the log data from the S3 archive
│   ├── song-data.zip - zip file containing a subset of the song data from the S3 archive
|   ├── log_data - contains the unzipped content of data/log-data.zip
|   │   └── <year>-<month>-<day>-events.csv
│   └── song_data - contains the unzipped content of data/song-data.zip
│       └── <first letter of song track ID>
│           └── <second letter of song track ID>
│               └── <third letter of song track ID>
│                   ├── (...)
│                   └── TR<track ID>.json
├── dl.cfg - config file with access key and secret to AWS
├── etl.py - code to read data from the S3 song and log archives to parquet files in another S3 bucket, for later analytics
├── README.md - this file in markdown
└── README.org - this file in orgmode
```


<a id="org0ea6d02"></a>

# Usage

To run the pipeline, run the following snippet on the terminal:

```bash
python etl.py
```

This code depends on the AWS credentials stored in the `dl.cfg` file according to the following structure:

```
[AWS]
key=<AWS key>
secret=<AWS secret>

[S3]
input=<S3 bucket to load the data from>
output=<S3 bucket to store the processed data in>
```

The pipeline creates a spark session, processes the `song_data` folder on the input S3 bucket, then the `log_data` folder on the input S3 bucket. The schema needed to read the files is defined, so as to avoid any unforeseen data mixing up the expected column types.

When saving the data into the output S3 bucket, each table is stored on their own folder in the S3 output bucket. And each folder is partitioned by the following columns:

-   the *songs* table is partitioned by `year`, then `artist_id`;
-   the *artists* table is partitioned by `artist_id`;
-   the *users* table is not partitioned;
-   the *time* table is partitioned by `year`, then `month`;
-   and the *songplays* table is partitioned by `year`, then `month`