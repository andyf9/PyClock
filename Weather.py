import sys
import datapoint
from math import radians,sin,cos,atan2,sqrt,acos
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
import os.path
import requests

# override with better implementation of distance calculation
def _new_distance_between_coords(self, lon1, lat1, lon2, lat2):
    # https://www.movable-type.co.uk/scripts/latlong.html

    # haversine
    #R = 6371000
    #delta_lat = radians(lat2-lat1)
    #delta_lon = radians(lon2-lon1)
    #a = sin(delta_lat/2) * sin(delta_lat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(delta_lon/2) * sin(delta_lon/2)
    #c = 2 * atan2(sqrt(a), sqrt(1-a))
    #distance = R * c

    # spherical law of cosines
    distance = acos(sin(radians(lat1))*sin(radians(lat2))+cos(radians(lat1))*cos(radians(lat2))*cos(radians(lon2)-radians(lon1))) * 6371000
    return distance

datapoint.Manager._distance_between_coords = _new_distance_between_coords

class Weather(QWidget):

    def __init__(self):
        super(Weather, self).__init__()
        self.setWindowTitle("Weather")
        
        self.ctimer = QTimer()
        self.ctimer.timeout.connect(self.refresh)
        self.ctimer.start(360000) # every hour
        self.refresh()

    def refresh(self):
        conn = datapoint.Manager(api_key="put key here")
        site = conn.get_nearest_site(-0.0005, 51.4769)
#        print site.name, site.id
        
        forecast = conn.get_forecast_for_site(site.id, "3hourly")
        self.current = forecast.now()
#        print self.current
#        print self.current.name
#        print self.current.date
#        print self.current.weather.value, self.current.weather.text
#        print self.current.temperature.value, self.current.temperature.units
#        print self.current.feels_like_temperature.value, self.current.feels_like_temperature.units
#        print self.current.wind_speed.value, self.current.wind_speed.text, self.current.wind_speed.units
#        print self.current.wind_direction.value, self.current.wind_direction.text, self.current.wind_direction.units
#        print self.current.wind_gust.value, self.current.wind_gust.text, self.current.wind_gust.units
#        print self.current.visibility.value, self.current.visibility.text, self.current.visibility.units
#        print self.current.uv.value, self.current.uv.text, self.current.uv.units
#        print self.current.precipitation.value, self.current.precipitation.text, self.current.precipitation.units
#        print self.current.humidity.value, self.current.humidity.text, self.current.humidity.units

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        image_dir = 'images'
        image_name = self.current.weather.value + '.svg'
        image_path = image_dir + '/' + image_name
        if not os.path.exists(image_path):
            if not os.path.isdir(image_dir):
                os.mkdir(image_dir)
            r = requests.get('https://www.metoffice.gov.uk/webfiles/1534500346087/images/icons/wx/' + image_name)
            open(image_path, 'wb').write(r.content)
        renderer =  QSvgRenderer(image_path, self)
        if (self.width() < self.height()):
            size = self.width()
            offset = 0
        else:
            size = self.height()
            offset = (self.width() - self.height())/2
        renderer.render(qp, QRectF(offset,0,size,size))
        
        qp.setPen(QColor('white'))
        font = QFont()
        font.setPixelSize(self.height() / 6)
        font.setFamily('Sans')
        qp.setFont(font)
        metrics = QFontMetrics(font)
        
        textHeight = self.height() / 2 + metrics.height()
        text = str(self.current.temperature.value) + u"\u00b0" + self.current.temperature.units
        qp.drawText((self.width() - metrics.boundingRect(text).width()) / 2, textHeight, text)
        
        font.setPixelSize(self.height() / 20)
        qp.setFont(font)
        metrics = QFontMetrics(font)
        textHeight = textHeight + metrics.height()
        text = 'feels like ' + str(self.current.feels_like_temperature.value) + u"\u00b0" + self.current.feels_like_temperature.units
        qp.drawText((self.width() - metrics.boundingRect(text).width()) / 2, textHeight, text)
        
        qp.drawText(0, self.height()-metrics.height()*2, str(self.current.wind_speed.value) + ' ' + self.current.wind_speed.units)
        qp.drawText(0, self.height()-metrics.height(), str(self.current.wind_gust.value) + ' ' + self.current.wind_gust.units)
        qp.drawText(0, self.height(), self.current.wind_direction.value)
        
        text = str(self.current.precipitation.value) + self.current.precipitation.units
        qp.drawText(self.width() - metrics.boundingRect(text).width(), self.height(), text)
        
        qp.end()

def main():
    app = QApplication(sys.argv)
    weather = Weather()
    weather.show()
    weather.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

