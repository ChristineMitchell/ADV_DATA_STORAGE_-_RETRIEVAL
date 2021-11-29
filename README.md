# ADV_DATA_STORAGE_AND_RETRIEVAL

## Overview
While enjoying my pineapple flavored ice cream cone, I fondly recalled my vacation to Oahu where I discovered my passion for the waves. How sweet would it be to surf every day? So, I thought to myself, why not make this a reality? What if I could enjoy both of my indulgences by opening up an ice cream shop in Hawaii? So, I reached out to a fellow surfing enthusiast who could be a potential investor. While he appreciated my excitement, but warned me of how he had a similar idea to open up a surf shop to sustain is surfing lifestyle, but had to close down to the weather cycle. So, he suggested that I do a little research to see just how viable it is to have an ice cream shop year round to sell him on the idea of investing with me. 

So, I put my newfound data analytic skills to work. I was able to utilize *SQLalchemy* via Pandas to access a *SQLite database* that stored weather data from nine different weather stations in Hawaii. The SQLite database is basically a flat file stored on my local server. I worked through the module retrieving a year of precipitation data from the most active weather station, then for this challenge I extracted the temperature data for the months of June and December at all of the Hawaii stations.

I discovered a new tool called a *flask app* to showcase the results on my local server to potential investors without bogging them down with the code. This was done with a python file, app.py, via Visual Studio Code. After connecting to the database file with an engine, I created multiple routes, the first being the welcome page, then I was able to provide separate pages showcasing individual result lists such as the precipitation, stations, tobs (temperature observations), and temperature stats (min, ave, and max) for a particular date range.

## Results

