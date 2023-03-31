# Exploratory Data Analysis of Radio Signal Receiver Performance Evaluation


This repository contains the solution to a data analysis task that evaluates the skills of the applicant. The task involves evaluating the performance of a test receiver installed to receive signals of certain radio waves. A vehicle equipped with an emitter of a specific radio signal is driven around the receiver, and every time the receiver detects the radio signal, a record is created with a time stamp and signal strength of the received signal. The vehicle logs its position via GPS every 100 ms and logs the longitude and latitude, which are stored in a comma-separated-value file.

## Task Description

The following tasks were given as part of the challenge:

1. Read the file receiver.json and vehicle.csv in Python.
2. Combine both datasets and keep only files where the receiver detected the vehicle. Use the time stamps of both files for combination (maximum allowed time difference for a match t = 100 ms).
3. Determine the distance between the receiver and the vehicle in km for each match.
4. Create a scatter plot showing the signal strength vs. distance to the receiver.

## Dataset Description

The receiver.json and vehicle.csv files contain data related to the test receiver and the vehicle's GPS logs, respectively. The GPS logs have a time offset of 1 hour, which should be corrected before combining the datasets. The data from the vehicle's GPS logs should be filtered to use only logs that meet the condition Status_POS_Heading_deg = 1.

## Solution Overview

The Python programming language was used to complete the data analysis task. The solution includes the following steps:

1. Load the receiver.json and vehicle.csv files using appropriate Python libraries. 
2. Preprocess the data to correct the time offset in the GPS logs and filter out the logs that do not meet the required condition.
3. Combine the two datasets based on the timestamps with a maximum allowed time difference of 100 ms to keep only the records where the receiver detected the vehicle.
4. Calculate the distance between the receiver and the vehicle in km for each match using the latitude and longitude data.
5. Create a scatter plot of the signal strength vs. distance to the receiver.
The implementation details can be found in the Jupyter notebook radio_signal_receiver_performance_evaluation.ipynb.

## Usage
To run the solution code, the following Python libraries are required:

* pandas
* numpy
* matplotlib
* datetime
* pytz
* geopy

## Logic

![image](https://user-images.githubusercontent.com/61086577/229110487-1a767d00-aa84-4b4f-b0eb-ac572bd30493.png)


Clone the repository to your local machine and run the Jupyter notebook radio_signal_receiver_performance_evaluation.ipynb.

## Conclusion
The solution to the data analysis task evaluates the applicant's skills in processing and combining datasets, filtering data, and creating visualizations. The task provides a realistic example of a common data analysis problem that the applicant might encounter in the position.



