# Spark Real time tweets sentiment analysis

## Description
The primary objectives of this project are to gather a substantial dataset of tweets related to the Israel-Palestine conflict and analyze public sentiment. This involves implementing an automated method to categorize tweets based on specific hashtags, distinguishing between different stances on the conflict. To ensure high-quality input for sentiment analysis, thorough data preprocessing is performed to standardize and clean the text. The project also aims to train and evaluate machine learning models to accurately classify the sentiment of the tweets, achieving high accuracy and robust performance metrics. Additionally, the project facilitates real-time processing and analysis of tweets, providing up-to-date insights into public sentiment on the Israel-Palestine conflict.

## Table of Contents
- [scrapping script](#)
- [Model](#Model)
- [Cluster](#Cluster)

## scrapping script
In the scrapping script directory you will find a .env_example, you need to modify the file with your own config, then you need to rename the file to .env, to run the scrapping script you can use the run the run_script.sh file.
For the script to work, the XPATHS defined in the script/xpath.py should be up to date, my script also assumes that this is the order of execution to scrap posts:

login (without problems) -> search -> click latest tab -> click post -> scrap text -> go back ->  scrap next post -> repeat until all posts are scrapped

so if the scrapping process is no longer possible then the script won't work.

Also make sure to install the requirements.txt file.

## Model
the Model directory is for training and saving the model to disk, you will find a notebook in the src directory, if you run it a model will be saved to the src/model directory, you will need this model later for running the spark application.

Also make sure to install the requirements.txt file. 

## Cluster
the Cluster directory has the docker-compose file for running spark, kafka, zookeeper, elasticSearch and kibana, the cluster directory also has the spark_apps folder which is linked to the spark_master container, in this folder you need to put the model.keras and a virtualenv packed using venv-pack the packages defined in the Cluster/spark_apps/requirements.txt file installed, preferably name it pyspark_venv.tar.gz, you also need to put the virtualenv by the name env, of course this isn't necessary if you modify the commands to your case.

To run the cluster, you can use the commands already defined in the make file, for example : make build.

You need to first run make build , then you can choose either to run the spark cluster with one worker, using make run, or 2 workers, using make run-scaled, if you want to run more than one worker you need to change the run-scaled command in the makefile by modifying the number of workers.

Once the cluster is running, make sure that the kafka topic has been created first and foremost, then connect to the spark master and go into the /opt/spark/apps directory, there you will need to run these commands : 

export PYSPARK_PYTHON=./env/bin/python

spark-submit --archives pyspark_venv.tar.gz#env --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.3,org.elasticsearch:elasticsearch-spark-30_2.12:8.0.0 --files preprocess.py app.py

hopefully everything is configured correctly and you will have a successfully running spark app.






