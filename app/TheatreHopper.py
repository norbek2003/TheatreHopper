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
def getShowtimesPage(link):
    """ Returns the soup of the page containing the showtimes. """
    now = datetime.datetime.now()
    url = "https://www.amctheatres.com" + link + "/showtimes/all/" + str(now.year) + "-" + ("0" + str(now.month))[-2:] + "-" + ("0" + str(now.day))[-2:] + "/" + link.split("/")[-1] + "/all"
    request = requests.get(url)
    soup = BeautifulSoup(request.content, features="html5lib")
    return url, soup
def getShowtimes(link, url=None):
    """ Gets the showtimes in the local theater. """
    if not url:
        url, soup = getShowtimesPage(link)
        request = requests.get(askForDates(soup, url))
        soup = BeautifulSoup(request.content, features="html5lib")  
    else:
        request = requests.get(url)
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
def getDates(soup, url):
    """ Returns the dates and resulting links """
    dates = soup.findAll("select", {"class" : "Showtimes-Action-Dropdown"})[1].findAll("option")[0 : 7]
    options = [date.text for date in dates]
    urls = [re.sub(r"/all/(.*)/amc", "/all/" + date.get("value") + "/amc", url) for date in dates]
    return options, urls
def askForDates(soup, url):
    """  Asks the user which date and returns the corresponding url. """
    dates, urls = getDates(soup, url)
    for x in xrange(len(dates)):
        print "[ " + str(x) + " ] -> " + dates[x]
    opt = input("\nWhich date? -> ")
    return urls[opt]
def findHops(showtimes, acceptableWaitTime=0):
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
       # print movie, " ",time, " ", endTime, " ", showtimes[movie]["length"], " ", acceptableWaitTime
        for startTime in times:
            timeDiff = getTimeDifference(endTime, startTime)
            if -15 < timeDiff and timeDiff < acceptableWaitTime:
                #print "adding ---->", startTime, timeDiff, (-15 < timeDiff and timeDiff < acceptableWaitTime)
                hops[showing] += [(movie, startTime) for movie in times[startTime]]
    return hops
def findMovieMarathons(allHops):
    """ Finds all possible chains of movies. """
    hops = {movie:allHops[movie][:] for movie in allHops}
    chain(allHops, hops)
    return hops
def chain(allHops, hops):
    """ Recursively chains together movies. """
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
    endMinute += int(length.split(":")[1]) + 15 #Preview time
    if(endMinute >= 60):
        endMinute %= 60
        endHour += 1
    endHour += int(length.split(":")[0])
    if(endHour > 12): # Do not reduce by 12! This will cause so many error. 13:25 PM is legit.
        AMPM = "pm"
    return str(endHour) + ":" + ("0" + str(endMinute))[-2:] + AMPM
def getTimeDifference(startTime, endTime):
    """ Gets the time difference in minutes between two times. """
    if "pm" in endTime:
        endTime = str(12 + int(endTime.split(":")[0])) + ":" + endTime.split(":")[1]
    if "pm" in startTime:
        startTime = str(12 + int(startTime.split(":")[0])) + ":" + startTime.split(":")[1]
    return int(endTime.split(":")[0]) * 60 +  int(endTime.split(":")[1][:-2]) - int(startTime.split(":")[0]) * 60 - int(startTime.split(":")[1][:-2])
def display(marathons,  depth):
    """ Displays possible movie marathons. """
    #print sorted(list(marathons), key=lambda k : toMinutes(k[1]))
    for movie in sorted(list(marathons), key=lambda k : toMinutes(k[1])):
        print (depth - 1) * "      " + "|-----" + str(movie) + "--->"
        display(marathons[movie], depth + 1)
def removeDuplicates(marathons, movieList):
    """ Removes duplicate movies in marathons """
    for movie in list(marathons):
        if movie[0] in movieList:
            del marathons[movie]
        else:
            newMovieList = [m for m in movieList] + [movie[0]]
            removeDuplicates(marathons[movie], newMovieList)
def toMinutes(time):
    if "pm" in time:
        time = str(12 + int(time.split(":")[0])) + ":" + time.split(":")[1]

    return int(time.split(":")[0]) * 60 + int(time.split(":")[1][:-2])

def main():
    theatres, links = getTheatres()
    for x in xrange(len(theatres)):
        print "[ " + str(x) + " ] -> " + theatres[x]
    num = input("\nWhich theatre? -> ")
    showtimes = getShowtimes(links[x])
    waitTime = input("\nIn minutes, how long are you willing to wait for a movie to start? -> ")
    hops = findHops(showtimes, waitTime)
    marathons = findMovieMarathons(hops)
    removeDuplicates(marathons, [])
    display(marathons, 0)
if __name__ == "__main__":
    main()
    
