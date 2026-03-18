import requests, pgeocode

class nws:
    baseUrl = "https://api.weather.gov/"

    def findCoord(self, zipCode):
        """Takes the zip code and returns the latitude and longitude derived from it using pgeocode
        Args:
            zipCode (int): The zip code that the user inputted
        Returns:
            tuple: The latitude and longitude derived from the zip code"""
        geocoder = pgeocode.Nominatim('us')
        info = geocoder.query_postal_code(zipCode)

        lat = info.latitude
        long = info.longitude
        return lat, long

    def callAPI(self, url):
        """General purpose function for retrieving data from a url
        Args:
            url (string): url???
        Raises:
            RuntimeError: Raises a runtime error when the status code isn't 200
        Returns:
            json: the data retrieved from the website"""
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise RuntimeError(f"Request failed: {response.status_code}")


    def forecastValues(self, data, date):
        tempValues = []
        windValues = []
        windChills = []

        forecastData = data["properties"]["periods"]
        count = 0
        for i in range(len(forecastData)):
            date2 = forecastData[i]["startTime"][0:10]
            if date2 == date.strftime("%Y-%m-%d"):
                if count > 4 and count < 10: 
                    tempValues.append(forecastData[i]["temperature"])

                    #checks for the more accurate windGust and if it's not present uses windSpeed as a fallback
                    tempwind = forecastData[i].get("windGust") or forecastData[i]["windSpeed"]
                    #sorry this is very chopped but basically to cut out the "mph" in the wind values it uses slicing to only include the
                    #index of the " " between the number and "mph" to cut it out. then it converts it to int
                    windValues.append(int(tempwind[:tempwind.index(" ")]))
                count += 1
        count = 0

        for i in range(len(tempValues)):
            windChills.append(round(35.74 + 0.6215 * tempValues[i] - 35.75 * (windValues[i] ** 0.16) + 0.4275 * tempValues[i] * (windValues[i] ** 0.16), 0))

        self.tempValues = tempValues
        self.windValues = windValues
        self.windChills = windChills

        return tempValues, windValues, windChills
    
    def precipValues(self, data, date):
        snowValues = []
        iceValues = []

        snowData = data["properties"]["snowfallAmount"]["values"]

        count = 0
        for i in range(len(snowData)):
            # date2 = snowData[i]["validTime"][0:10]
            # if date2 == date.strftime("%Y-%m-%d"):
            #     #if count > 4 and count < 10:
            #     snowValues.append(round(snowData[i]["value"] / 25.4, 2))
            #     count += 1
            snowValues.append(snowData[i])
        count = 0

        iceData = data["properties"]["iceAccumulation"]["values"]



        self.snowValues = snowValues
        self.iceValues = iceValues

        return snowValues, iceValues


        
    def __str__(self):
        return (
f"""
Base Temperatures (f): {self.tempValues}
Wind Speed/Gust (mph): {self.windValues}
Windchills (f): {self.windChills} 
Snowfall by each period during transportation (in): {self.snowValues} 
Ice accumulation by each period during transportation (in): {self.iceValues} 
"""
        )

    def __init__(self, zipCode, date):
        self.zipCode = zipCode
        self.date = date
        
        
