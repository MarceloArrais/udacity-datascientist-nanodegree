# Disaster Response Pipeline Project

## Motivation
Predicting human behavior is a trend followed by companies which have already understood the importance of being always a step forward of the competitors.
It is more than clear that social media are a huge source of information about us and can be very useful for forecasting our behaviors. For example: we can predict happiness base on sentiment analysis of twitter data or categorise real messages sent during disaster events. Thus, to get information from raw messages sent on social medias could be an strategic skill for a data scientist.
In light of that, I've done this project to improve my *Data Science* skills.


## Overview

In this project I've built a *etl/ml pipeline* to analyze a dataset that contains real messages sent during disaster events.

## Components

### ETL Pipeline

Loads data from csv files and cleans the data. See [process_data.py](https://github.com/MarceloArrais/udacity-datascientist-nanodegree/tree/master/disaster-response/data/process_data.py)
									
### ML Pipeline

Apply various NLP algorithms for feature engineering and builds a classifier that categorizes unseen messages. See [train_classifier.py](https://github.com/MarceloArrais/udacity-datascientist-nanodegree/tree/master/disaster-response/models/train_classifier.py)

### Web App

A Flask application where the user can put messages to be categorized and then display the results. See [app/](https://github.com/MarceloArrais/udacity-datascientist-nanodegree/tree/master/disaster-response/app)

### UI

![dataset](images/message-genre-distribution.png)

![classification](images/categories-distribution.png)


## Running
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

## Python Libraries

* sys
* nltk
* flask
* plotly
* Numpy
* Pandas
* pickle
* sklearn
* Matplotlib
* sqlalchemy

## Acknowledgment

Dataset was curated and given by [Flight Eight](https://appen.com/datasets/combined-disaster-response-data/)



  

  
	