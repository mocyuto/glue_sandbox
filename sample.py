import os
import boto3
import sys
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job
from botocore.client import Config

# glue Initialize
os.environ["TEST_S3_ENDPOINT_URL"] = "http://glue.dev.s3.local:4566"

sys.argv += ["--JOB_NAME", "glue_script"]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

spark = SparkSession.builder.config(
    "spark.serializer", "org.apache.spark.serializer.KryoSerializer"
).getOrCreate()
sc = spark.sparkContext
glueContext = GlueContext(sc)
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
sc.getConf().getAll()

# Set S3 with localstack parameters
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.environ["TEST_S3_ENDPOINT_URL"])
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.signing-algorithm", "S3SignerType")

# Create S3 bucket
session = boto3.session.Session(aws_access_key_id="xxx", aws_secret_access_key="xxx")
s3client = session.client(
    "s3",
    endpoint_url=os.environ["TEST_S3_ENDPOINT_URL"],
    use_ssl=False,
)
bucket = s3client.create_bucket(Bucket="test-bucket")

# S3 init
s3 = boto3.resource(
    "s3",
    endpoint_url=os.environ["TEST_S3_ENDPOINT_URL"],
    region_name="ap-northeast-1",
    use_ssl=False,
)
bucket_name = "test-bucket"
bucket = s3.Bucket(bucket_name)
bucket.upload_file("test_data/sample.json", "sample/sample.json")

# get dynamic frame and data frame convert
p = f"s3://{bucket_name}/sample/sample.json"
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [p]},
    format="json",
).toDF()
df.count()
df.show()

# spark sql exec
df.createOrReplaceTempView("sample")
spark.sql("show tables").show()
spark.sql("select count(*) from sample").show()
spark.sql("select * from sample").show()
