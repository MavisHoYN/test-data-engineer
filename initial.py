# Connect to the MySQL database using appropriate libraries or connectors available in Databricks.
username = dbutils.secrets.get(scope = "jdbc", key = "username")  # use the saved username in secret
password = dbutils.secrets.get(scope = "jdbc", key = "password")  # use the saved pw in secret

# Set variables
database_host = "<database-host-url>"
database_port = "<port>"
database_name = "<database-name>"
table_name = "Members"

# Use spark.read to read mySQL table
df = spark.read \
    .format("mysql") \
    .option("dbtable", table_name) \
    .option("host", database_host) \
    .option("port", database_port) \
    .option("database", database_name) \
    .option("user", username) \
    .option("password", password) \
    .load()

# Create temp view for the table
df.createOrReplaceTempView("tmp_members")

# Transform schemas (or just in case it read the registration_date as string)
df_members = spark.sql("SELECT CAST(member_id AS STRING) AS member_id, \
    CAST(first_name AS STRING) AS first_name, \
    CAST(last_name AS STRING) AS last_name, \
    CAST(email AS STRING) AS email, \
    CAST(phone_number AS STRING) AS phone_number, \
    CAST(address AS STRING) AS STRING, \
    CAST(city AS STRING) AS city, \
    CAST(country AS STRING) AS country, \
    CAST(registration_date AS DATE) AS registration_date \
    FROM Members")


storage = "<storage_name>"
access_key = "<accesskey>"
container = "<container_name>"
subfolder = "<subfolder_name>"

# Configure the blob storage account access key globally
spark.conf.set("fs.azure.account.key.{}.blob.core.windows.net".format(storage), access_key)

# For Azure blob storage
output_path = "wasbs://{}/{}.blob.core.windows.net/{}".format(container, storage, subfolder)

# Write the transformed data to Parquet files using Databricks, ensuring to partition the data appropriately.
# Store the Parquet files in blob storage (e.g., Azure Blob Storage, AWS S3) for data persistence and scalability.
partition_columns = ["city", "country"]  # Can partition with date column for delta load also
df_members.write.parquet(path=output_path, mode="overwrite", partitionBy=partition_columns)


# Create a workflow to automate the data extraction, transformation, and loading process, ensuring it runs at specified intervals or triggers.
# I would create a job to run the notebook as a workflow.
# 1. Create a job in workflow, configure to the notebook with the saved code above.
# 2. Using the new job cluster option.
# 3. Add a scheduled trigger for schedule it runs at specified intervals.
# 4. Or add a File arrival trigger when there is new files arrive.


# For the second workflow, read the Parquet files from blob storage into Databricks.












