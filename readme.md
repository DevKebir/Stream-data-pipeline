# Weather Data Streaming and Storage

## Overview

This project retrieves weather data for a list of cities, transforms the data, streams it to a Kinesis Firehose and visualize it in opensearch. Additionally, it stores the weather data  to S3 and locally in CSV format.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3 installed
- Dependencies installed: `boto3`, `pandas`, `requests`, `dotenv`
- AWS credentials configured with permissions to access Kinesis Firehose

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DevKebir/Stream-weather-data-pipeline.git
   cd weather-data-streaming


## Install dependencies
- pip install -r requirements.txt

## Create a .env file in the project root and set the following variables
- AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
- STREAM_NAME=your_kinesis_firehose_stream_name
- API_KEY=your_openweathermap_api_key
- REGION_NAME=your_aws_region




## Ressources 
- [Kinesis firehose AWS Documentation] 
 <https://docs.aws.amazon.com/managed-flink/latest/java/get-started-exercise-fh.html#get-started-exercise-fh-2

- [Openserach AWS Documentation] 
<https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html
<https://docs.aws.amazon.com/opensearch/latest/dashboards/

- [AWS CLI documentation]
<https://awscli.amazonaws.com/v2/documentation/api/latest

- [OpenWeatherMap API Docs] 
<https://openweathermap.org/api>

## Additional Notes

The script is configured to run every 5 seconds for each city in the provided list.
Adjust the list of cities in main.py based on your requirements.
The CSV file is stored in the output directory.