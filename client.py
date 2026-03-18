import nws, utility
from datetime import date

class client:
    def callNWS(self, zipCode, date):
        baseUrl = "https://api.weather.gov/"
        NWS = nws.nws(zipCode, date)

        lat, long = NWS.findCoord(zipCode)

        pointsUrl = f"{baseUrl}/points/{lat},{long}"
        pointsData = NWS.callAPI(pointsUrl)
        forecastUrl = pointsData["properties"]["forecastHourly"]
        forecastData = NWS.callAPI(forecastUrl)
        tt, tw, tc = NWS.forecastValues(forecastData, date)

        precipUrl = pointsData["properties"]["forecastGridData"]
        precipData = NWS.callAPI(precipUrl)
        sv, iv = NWS.precipValues(precipData, date)

        print(NWS)

        return tt, tw, tc, sv, iv, NWS
    
    def mockData(self):
        fn_t = -8
        fn_c = -18
        fn_w = 34
        fn_s = 2.1
        fn_i = .07
        str_NWS = """
Base Temperatures (f): [-7, -8, -8, -7, -6]
Wind Speed/Gust (mph): [27, 32, 29, 34, 31]
Windchills (f): [-15, -18, -17, -16, -14]
Snowfall by each period during transportation (in): [1.2, 0.9]
Ice accumulation by each period during transportation (in): [0.04, 0.03]
"""
        percent, label = self.calculate(fn_t, fn_c, fn_w, fn_s, fn_i)
        return str_NWS, percent, label

    def calculate(self, fn_t, fn_c, fn_w, fn_s, fn_i):
        if (fn_c <= -30) or (fn_t <= -15) or (fn_i >= .25) or (fn_s >= 8):
            percent = 100
            label = "Guaranteed"
            return percent, label
            
        snow_points = fn_s * 5
        ice_points = fn_i * 120
        temp_points = (0 - fn_t) * 1
        windchill_points = (0 - fn_c) * 1
        wind_points = max(0, (fn_w - 20)) * 1

        total_points = snow_points + ice_points + temp_points + windchill_points + wind_points
        percent = min(100, (total_points / 120) * 100)

        if percent == 100:
            label = "Guaranteed"
        elif percent >= 60:
            label = "Likely"
        elif percent >= 40:
            label = "Possible"
        elif percent >= 20:
            label = "Unlikely"
        else:
            label = "Not Happening"

        return percent, label



    def main(self, zipCode, targetDate):
        today = date.today()
        dateDiff = (targetDate - today).days

        #if dateDiff <= 7:
        tt, tw, tc, sv, iv, str_NWS = self.callNWS(zipCode, targetDate)

        #return None, None, None


        #------ AFTER CALLS ARE DONE --------------------
        # util = utility.utility()
        # fn_t = util.getMax(False, tt)
        # fn_c = util.getMax(False, tc)
        # fn_w = util.getMax(True, tw)
        # fn_s = util.getSum(sv)
        # fn_i = util.getSum(iv)

        # percent, chance = self.calculate(fn_t, fn_c, fn_w, fn_s, fn_i)

        #return str_NWS, percent, chance
        return tt, tw, tc, sv, iv, str_NWS

        


    