##########################
# inconstant v1.0       
# Author: Urim Berisha
# Youtube.com/urimberisha
# Date: November 25th 2020
##########################

from datetime import datetime
import ctypes, os, time
import comtypes

yourSunrise = "0800"
yourSunset = "1600"

sunrise = int(yourSunrise[0:2])*60 + int(yourSunrise[2:4]);
sunset = int(yourSunset[0:2])*60 + int(yourSunset[2:4]);
total = 1440
totalPics = 200
riseToSet = sunset - sunrise
setToRise = sunrise+total-sunset
sunrisePic = 40
sunsetPic = 170

now = (datetime.now()).strftime("%H%M")
currentTime = int(now[0:2])*60 + int(now[2:4])

def changeBg(par):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, '..\\inconstant\\images\\' + str(int(par)) + ".png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

if sunrise < currentTime < sunset:
    x = riseToSet / (sunsetPic-sunrisePic)
    currentPic = 40 + (currentTime - sunrise) / x
    
elif sunset < currentTime :
    x = setToRise / (200-sunsetPic+sunrisePic)
    currentPic = (170 + ((currentTime-sunset)/x))%200

else:
    x = setToRise / (200-sunsetPic+sunrisePic)
    currentPic = 8 + currentTime/x

i = int(currentPic)
while i<= totalPics:
    changeBg(i)
    time.sleep(60*int(x))
    i += 1
    if (i >= 200):
        i = 1