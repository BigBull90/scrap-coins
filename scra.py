import urllib3
import requests
from influxdb import InfluxDBClient

urllib3.disable_warnings()

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'crypto')
client.create_database('crypto')

def coindelta():
    r = requests.get('https://coindelta.com/api/v1/public/getticker/')
    if r.status_code != requests.codes.ok:
        return
    packet = ''

    for item in r.json():
        currency = str(item['MarketName']).split('-')[0].upper()
	point = "{},market={},exchange={} value={}".format(currency, str(item['MarketName']), 'coindelta', item['Last'])
	packet = '\n'.join([packet,point])
    if packet:
        print client.write_points(packet,protocol='line')
    
def koinex():
    r = requests.get('https://koinex.in/api/ticker')
    if r.status_code != requests.codes.ok:
        return
    packet = ''
    exchange = 'koinex'
    data = r.json()
    for key,value in data['prices'].iteritems():
        currency = str(key)
        market = currency.lower() + '-' + 'inr'
	point = "{},market={},exchange={} value={}".format(currency, market, exchange, value)
	packet = '\n'.join([packet,point])
    if packet:
        print client.write_points(packet,protocol='line')

if __name__ == "__main__":
    coindelta()
    koinex()
