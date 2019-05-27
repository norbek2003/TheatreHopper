from bs4 import BeautifulSoup
import urllib2
import re
import requests
import datetime
from pprint import pprint
from os import system, name
from googlesearch import search
import json
def clear(): 
    """ Clears the terminal. """
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 
def getTheatres():
    """ Returns local theatres. """
    query = [i for i in search("AMC theatres near me", tld="co.in", num=1, stop=1, pause=2)][0]
    page = urllib2.urlopen(query)
    soup = BeautifulSoup(page, features="html5lib")
    theatres = []
    links = []
    for row in soup.findAll("div", {"class": "PanelList-item-center TheatreFinder-centerPanel"}):
        texts = row.findAll("span", {"class": "Link-text Headline--h3"})
        for t in texts:
            links.append(row.find("a").get("href"))
            theatres.append(t.text)
    return theatres, links

def getShowtimes(link):
    """ Gets the showtimes in the local theater. """
    now = datetime.datetime.now()
    url = "https://www.amctheatres.com" + link + "/showtimes/all/" + str(now.year) + "-" + ("0" + str(now.month))[-2:] + "-" + ("0" + str(now.day))[-2:] + "/" + link.split("/")[-1] + "/all"
    request = requests.get(url)
    soup = BeautifulSoup(request.content, features="html5lib")
    request = requests.get(getDate(soup, url))
    soup = BeautifulSoup(request.content, features="html5lib")  
    showtimes = {}
    for row in soup.findAll("div", {"class" : "ShowtimesByTheatre-film"}):
        showtimes[row.find("h2").text] = {
            "length" : row.find("div", {"class" : "txt--tiny MovieTitleHeader-list txt--medium txt--gray--light u-uppercase"}).find("span").findAll("span")[1].text.replace(" hr ", ":").replace(" min", ""),
            "showtimes":[]
        }
        for showing in row.findAll("div", {"class" : "Showtime"}):
            if "Showtime-disabled" not in showing.attrs["class"]:
                showtimes[row.find("h2").text]["showtimes"].append(showing.get("aria-label"))
    return showtimes
def getDate(soup, url):
    """ Asks the user the date and returns the corresponding page. """
    dates = soup.findAll("select", {"class" : "Showtimes-Action-Dropdown"})[1].findAll("option")[0 : 7]
    options = [date.get("value") for date in dates]
    for x in xrange(len(dates)):
        print "[ " + str(x) + " ] -> " + dates[x].text 
    opt = input("\nWhich date? -> ")
    return re.sub(r"/all/(.*)/amc", "/all/" + dates[opt].get("value") + "/amc", url)

def findHops(showtimes):
    """ Finds possible single hops. """
    times = {}
    hops = {}
    for movie in showtimes:
        for time in showtimes[movie]["showtimes"]:
            if time not in times:
                times[time] = []
            times[time].append(movie)
    for time in times:
        for movie in times[time]:
            hops[(movie, time)] = []
    for showing in hops:
        movie, time = showing
        endTime = getEndTime(time, showtimes[movie]["length"])
        for startTime in times:
            if abs(getTimeDifference(startTime, endTime)) < 15:
                hops[showing] += [(movie, startTime) for movie in times[startTime]]
    return hops
def findMovieMarathons(allHops):
    """ Finds all possible chains of movies. """
    hops = {movie:allHops[movie][:] for movie in allHops}
    chain(allHops, hops)
    return hops
def chain(allHops, hops):
    """ Recursviely chains together movies. """
    for movie in hops:
        if hops[movie]:
            h = hops[movie]
            hops[movie] = {movie:allHops[movie] for movie in h}
            chain(allHops, hops[movie])
def getEndTime(startTime, length):
    """ Returns the end time of a movie. """
    endHour = int(startTime.split(":")[0])
    endMinute = int(startTime.split(":")[1][:2])
    AMPM = startTime.split(":")[1][2:]
    endMinute += int(length.split(":")[1])
    if(endMinute >= 60):
        endMinute %= 60
        endHour += 1
    endHour += int(length.split(":")[0])
    if(endHour > 12):
        AMPM = "pm"
    return str(endHour) + ":" + ("0" + str(endMinute))[-2:] + AMPM
def getTimeDifference(startTime, endTime):
    """ Gets the time difference in minutes between two showings. """
    if "pm" in endTime:
        endTime = str(12 + int(endTime.split(":")[0])) + ":" + endTime.split(":")[1]
    return int(endTime.split(":")[0]) * 60 +  int(endTime.split(":")[1][:-2]) - int(startTime.split(":")[0]) * 60 - int(startTime.split(":")[1][:-2])
def main():
    theatres, links = getTheatres()
    for x in xrange(len(theatres)):
        print "[ " + str(x) + " ] -> " + theatres[x]
    num = input("\nWhich theatre? -> ")
    showtimes = getShowtimes(links[x])
    hops = findHops(showtimes)
    marathons = findMovieMarathons(hops)
    #print json.dumps(marathons, indent=4)
    pprint(marathons, indent = 4, depth=20)
if __name__ == "__main__":
    main()