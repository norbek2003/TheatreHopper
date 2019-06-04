# TheatreHopper

## Description

* A python command line and web tool for organizing theater hopping at local AMC cinemas.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prequisites

* python
* virtualenv
* pip
* git

### Installing

A step by step series of examples that tell you how to get a development environment running on the command line.

Clone the repo.

```
git clone https://github.com/norbek2003/TheatreHopper
```

Create virtual environment.

```
virtualenv env
```

Activate virtual environent.

* Windows : `\env\Scripts\activate`

* Unix : `source env/bin/activate`

Install program requirements.
```
pip install -r requirements.txt
```

### Usage

#### Command Line

1) Type `cd app` and then `python TheatreHopper.py` into the command line.
1) You will be given a list of local theatres. Choose one.
2) You will then be given a list of days, starting from the current date. Choose one.
3) You will then be presented with all movies and chains of movies.

#### Webpage

1) Type `python run.py` into the command line.
2) Navigate to `127.0.0.1:5000` in your web browser.
2) You will be asked to choose a local theatre from a dropdown menu. Choose one.
3) You will then be given a dropdown menu of days. Choose one.
4) The webpage will then display the possible movies in the form of recursive dropdown lists.

## Author
Ian Williams

## Why This Is Neither Unethical Nor Illegal

### Why This IS Legal
* Web scraping is not illegal by itself.
* *I* didn't tell you to theatre-hop. That was your choice.

### Why This IS NOT Unethical
* The program only scrapes two pages each time the program is run, not enough to bog down the company's servers and the equivalent of a human's request time. The program merely automates it and presents the data.
* Theater-Hopping inspires more people to go to the movie theatres. The markups are enormous for movie ticket prices anyways, so they aren't really losing money. Most money they make is from concessions, and people staying for multiple movies get hungry, so they actually might make more money.


