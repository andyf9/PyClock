import sys
import datapoint
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

class Weather(QWidget):

    def __init__(self):
        super(Weather, self).__init__()
        self.setWindowTitle("Weather")
        
        self.conn = datapoint.Manager(api_key="put key here")
        self.site = self.conn.get_nearest_site(-0.0005, 51.4769)
        
        self.forecast = self.conn.get_forecast_for_site(self.site.id, "3hourly")
        cf = self.forecast.now()
        print cf.name
        print cf.date
        print cf.weather.value, cf.weather.text
        print cf.temperature.value, cf.temperature.units
        print cf.feels_like_temperature.value, cf.feels_like_temperature.units
        print cf.wind_speed.value, cf.wind_speed.text, cf.wind_speed.units
        print cf.wind_direction.value, cf.wind_direction.text, cf.wind_direction.units
        print cf.wind_gust.value, cf.wind_gust.text, cf.wind_gust.units
        print cf.visibility.value, cf.visibility.text, cf.visibility.units
        print cf.uv.value, cf.uv.text, cf.uv.units
        print cf.precipitation.value, cf.precipitation.text, cf.precipitation.units
        print cf.humidity.value, cf.humidity.text, cf.humidity.units


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        renderer =  QSvgRenderer('images/' + self.forecast.now().weather.value + '.svg', self)
        if (self.width() < self.height()):
            size = self.width()
            offset = 0
        else:
            size = self.height()
            offset = (self.width() - self.height())/2
        renderer.render(qp, QRectF(offset,0,size,size))
        font = QFont()
        font.setPointSize(36)
        font.setFamily('Piboto')
        qp.setFont(font)
        qp.setPen(QColor('white'))
        qp.drawText(QPointF(self.width() / 2, self.height() - 100), str(self.forecast.now().temperature.value))
        qp.end()

def main():
    app = QApplication(sys.argv)
    weather = Weather()
    weather.show()
    weather.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

