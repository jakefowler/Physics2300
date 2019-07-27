# Weather


![Ogden Temperatures](/images/ogdenTemp.png)

![Min Max Temperatures](/images/minMaxTemp.png)
## This program is used for parsing weather data
1. It gets the name of the data file from the user on the command line
2. Opens the data file
3. Reads the first line of data and throws it away (it is the header info the computer doesn't need)
    * from all the remaining lines:
        * read in the date (index 2) and temperature (index 3)
        * parse the date string into year, month, day
        * convert year, month, day into decimal years for plotting
4. Makes two lists for the time series - the decimal year list and the temperature list
5. Sorts the data by month so we can average it and take the standard deviation later
6. Plots the results
