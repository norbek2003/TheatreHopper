from flask import Flask, render_template, redirect, url_for, request, make_response
from TheatreHopper import *
from pprint import pprint
from app import app
@app.route("/",  methods=["GET", "POST"])
def page():
    options = {}
    theatres, links = getTheatres()
    theatresLinks = [(theatres[i], links[i]) for i in xrange(len(theatres))]
    options["theatreList"] = theatresLinks
    #print "made it this far"
    #raise IndexError
    #print request
    if request.form:
     #   print request.form
        if "theatre" in request.form:
            url, soup = getShowtimesPage(request.form["theatre"])
            dates, urls = getDates(soup, url)
            dateList = [(dates[i], urls[i]) for i in xrange(len(dates))]
            options["dates"] = dateList
            if "dates" in request.form:
                #print request.form["dates"]
                showtimes = getShowtimes(None, url=request.form["dates"])
                #print showtimes
                hops = findHops(showtimes, int(request.form["maxWait"]))
                #pprint(hops)
                marathons = findMovieMarathons(hops)
                removeDuplicates(marathons, [])
                options["marathons"] = marathons
                #display(marathons, 0)
                #print request.form["dates"] 
    return make_response(render_template('index.html', **options))