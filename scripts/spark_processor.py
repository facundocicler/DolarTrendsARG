from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

KAFKA_TOPIC = "cotizaciones"
KAFKA_SERVER = "kafka:9092"
S3_BUCKET = "s3a://dolar-data-arg"

# Esquema de los datos
schema = StructType() \
    .add("nombre", StringType()) \
    .add("compra", DoubleType()) \
    .add("venta", DoubleType()) \
    .add("fechaActualizacion", TimestampType())

# Sesión de Spark
spark = SparkSession.builder \
    .appName("DolarProcessor") \
    .getOrCreate()

# Leer desde Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Procesar datos
cotizaciones = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
cotizaciones = cotizaciones.withColumn("spread", col("venta") - col("compra"))

# Guardar en S3
query = cotizaciones.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("path", S3_BUCKET) \
    .start()

query.awaitTermination()
