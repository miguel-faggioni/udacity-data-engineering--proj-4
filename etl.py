import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, IntegerType, DateType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']

def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data files
    song_data_in = os.path.join(input_data,'song_data')#TODO revisar
    song_data_out = os.path.join(output_data,'song_data')#TODO revisar

    # enforce the field types using a schema to read the data
    song_data_schema = StructType([
        StructField('artist_id',StringType()),
        StructField('artist_latitude',DoubleType()),
        StructField('artist_location',StringType()),
        StructField('artist_longitude',DoubleType()),
        StructField('artist_name',StringType()),
        StructField('duration',DoubleType()),
        StructField('num_songs',IntegerType()),
        StructField('song_id',StringType()),
        StructField('title',StringType()),
        StructField('year',IntegerType()),
    ])

    # read song data files
    df = spark.read \
              .option('recursiveFileLookup','true') \
              .json(song_data, schema=song_data_schema)

    # extract columns to create songs table
    songs_table = df.select(['song_id','title','artist_id','year','duration'])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write \
               .mode('overwrite') \
               .partitionBy('year','artist_id') \
               .format('parquet') \
               .option('path',os.path.join(song_data_out,'songs')) \
               .save()

    # extract columns to create artists table
    artists_table = df.select(['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']) \
                      .withColumnRenamed('artist_name','name') \
                      .withColumnRenamed('artist_location','location') \
                      .withColumnRenamed('artist_latitude','latitude') \
                      .withColumnRenamed('artist_longitude','longitude')

    # write artists table to parquet files
    artists_table.write \
                 .mode('overwrite') \
                 .partitionBy('artist_id') \
                 .format('parquet') \
                 .option('path',os.path.join(song_data_out,'artists')) \
                 .save()


def process_log_data(spark, input_data, output_data):
    # get filepath to log data files
    log_data_in = os.path.join(input_data,'log_data')#TODO revisar
    log_data_out = os.path.join(output_data,'log_data')#TODO revisar

    # enforce the field types using a schema to read the data
    log_data_schema = StructType([
        StructField('artist',StringType()),
        StructField('auth',StringType()),
        StructField('firstName',StringType()),
        StructField('gender',StringType()),
        StructField('itemInSession',IntegerType()),
        StructField('lastName',StringType()),
        StructField('length',DoubleType()),
        StructField('level',StringType()),
        StructField('location',StringType()),
        StructField('method',StringType()),
        StructField('page',StringType()),
        StructField('registration',StringType()),
        StructField('sessionId',IntegerType()),
        StructField('song',StringType()),
        StructField('status',IntegerType()),
        StructField('ts',StringType()),
        StructField('userAgent',StringType()),
        StructField('userId',StringType()),
    ])
    
    # read log data file
    df = spark.read \
              .option('recursiveFileLookup','true') \
              .json(log_data,schema=log_data_schema)
    
    # filter by actions for song plays
    df = df.where(df.page == 'NextSong')

    # extract columns for users table
    users_table = df.select(['userId','firstName','lastName','gender','level']) \
                    .withColumnRenamed('userId','user_id') \
                    .withColumnRenamed('firstName','first_name') \
                    .withColumnRenamed('lastName','last_name')

    # handle duplicates
    #TODO
    
    # write users table to parquet files
    users_table.write \
               .mode('overwrite') \
               .format('parquet') \
               .option('path',os.path.join(song_data_out,'users')) \
               .save()

    # create timestamp column from original timestamp column
    @udf(TimestampType())
    def get_timestamp(line):
        if line == None:
            return None
        line = int(line)
        return datetime.fromtimestamp(line/1000)
    df = df.withColumn('timestamp', get_timestamp('ts'))
    
    # create datetime column from original timestamp column
    @udf(DateType())
    def get_datetime(line):
        if line == None:
            return None
        line = int(line)
        return datetime.fromtimestamp(line/1000)
    df = df.withColumn('datetime', get_datetime('ts'))
    
    # extract columns to create time table
    #TODO
    time_table = 
    
    # write time table to parquet files partitioned by year and month
    #TODO
    time_table

    # read in song data to use for songplays table
    #TODO
    song_df = 

    # extract columns from joined song and log datasets to create songplays table
    #TODO
    songplays_table = 

    # write songplays table to parquet files partitioned by year and month
    #TODO
    songplays_table


def main():
    spark = create_spark_session()
    input_data = '/home/miguel/udacity/project_4/data' #TODO mudar pra S3
    #input_data = "s3a://udacity-dend/"
    output_data = '/home/miguel/udacity/project_4/data/output_data'
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
