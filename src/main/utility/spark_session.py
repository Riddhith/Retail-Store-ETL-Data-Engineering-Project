import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from src.main.utility.logging_config import *

def spark_session():
    spark = SparkSession.builder.master("local[*]") \
        .appName("riddhith_spark2")\
        .config("spark.driver.extraClassPath", "/home/riddhith/mysql-connector-java-8.0.17.jar") \
        .getOrCreate()
    logger.info("spark session %s",spark)
    return spark