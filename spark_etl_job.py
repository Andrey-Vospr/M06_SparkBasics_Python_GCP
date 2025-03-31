from pyspark.sql import SparkSession
import pygeohash as pgh
import requests

# Create Spark session
spark = SparkSession.builder.appName("ETL_Spark_Basics").getOrCreate()

# Load weather data
weather = spark.read.parquet("gs://storage-bucket-polished-owl/data/m06sparkbasics/weather/")

# Load all hotel CSVs
hotels = spark.read.option("header", True).csv("gs://storage-bucket-polished-owl/data/m06sparkbasics/hotels/*.csv")

# Convert columns to correct types if needed
hotels = hotels.withColumn("Latitude", hotels["Latitude"].cast("double"))
hotels = hotels.withColumn("Longitude", hotels["Longitude"].cast("double"))

# TODO: Add OpenCage REST API logic here for missing lat/lon
# TODO: Generate geohash using pgh.encode(lat, lon, precision=4)

# Save result 
hotels.write.mode("overwrite").parquet("gs://storage-bucket-polished-owl/data/output/hotels_cleaned")

spark.stop()
