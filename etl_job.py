import os
import requests
import geohash2 as geohash
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, trim
from pyspark.sql.types import StringType

# ✅ OpenCage API Key
OPENCAGE_API_KEY = "e863c7e8f91c491f838190dcfb02e0ec"

# 🔧 Configure Spark on Windows
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# 📍 UDF: Get formatted address using OpenCage
def reverse_geocode(lat, lon):
    if not lat or not lon:
        return None
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if result["results"]:
                return result["results"][0]["formatted"]
    except Exception as e:
        print(f"[API ERROR] Reverse geocode failed for lat={lat}, lon={lon}: {str(e)}")
    return None

# 🧭 UDF: Create 4-character geohash
def generate_geohash(lat, lon):
    try:
        return geohash.encode(float(lat), float(lon), precision=4)
    except:
        return None

# 🧠 Register UDFs
reverse_geocode_udf = udf(reverse_geocode, StringType())
geohash_udf = udf(generate_geohash, StringType())

if __name__ == "__main__":
    # 🚀 Start Spark
    spark = SparkSession.builder.appName("ETL_Join_Hotels_Weather").getOrCreate()

    # 📁 Paths
    base_path = "file:///C:/Users/HP/Documents/spark-etl-homework/data/m06sparkbasics"
    weather_path = os.path.join(base_path, "weather")
    hotels_path = os.path.join(base_path, "hotels")
    enriched_output_path = os.path.join(base_path, "output", "hotels_enriched.parquet")
    final_output_path = os.path.join(base_path, "output", "hotels_weather_joined.parquet")

    # 📥 Read input datasets
    weather_df = spark.read.option("basePath", weather_path).parquet(weather_path)
    hotels_df = spark.read.option("header", True).csv(hotels_path)

    # 🧹 Clean hotels: Remove null/empty lat/lon
    cleaned_hotels_df = hotels_df \
        .withColumn("Latitude", trim(col("Latitude"))) \
        .withColumn("Longitude", trim(col("Longitude"))) \
        .filter(
            (col("Latitude").isNotNull()) &
            (col("Longitude").isNotNull()) &
            (trim(col("Latitude")) != "") &
            (trim(col("Longitude")) != "")
        ) \
        .limit(100)  # Optional for local testing

    # 🌍 Enrich with Geohash and Formatted Address
    enriched_hotels_df = cleaned_hotels_df \
        .withColumn("Geohash", geohash_udf("Latitude", "Longitude")) \
        .withColumn("FormattedAddress", reverse_geocode_udf("Latitude", "Longitude"))

    # 💾 Save enriched hotels
    enriched_hotels_df.write.mode("overwrite").parquet(enriched_output_path)

    # 🧩 Add Geohash column to weather data (from lat/lng)
    weather_df_short = weather_df.withColumn("Geohash", geohash_udf("lat", "lng"))

    # 🔗 LEFT JOIN: Hotels ← Weather on Geohash
    joined_df = enriched_hotels_df.join(weather_df_short, on="Geohash", how="left")

    # 💾 Save final output
    joined_df.write.mode("overwrite").parquet(final_output_path)

    # ✅ Done
    print(f"[✔] Enriched hotels saved to: {enriched_output_path}")
    print(f"[✔] Joined hotels + weather saved to: {final_output_path}")

    spark.stop()




