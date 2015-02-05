import signal
import sys
import yaml
import paho.mqtt.client as mqtt
import urllib
import urllib2
import json

"""Get the authentication token"""
def get_token(url, username, password):
    query = {'username': username, 'password': password, 'service': 'mem'}
    encoded = urllib.urlencode(query)
    token = urllib2.urlopen(url + '?' + encoded).read()
    return json.loads(token)['token']

"""Post the log content"""
def post(url, message):
    data = urllib.urlencode(message)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    print "sent log line"
    print response.read()

"""Called when the client is reconnected"""
def on_connect(client, userdata, flags, rc):
    client.subscribe("mooc/")

"""Called when a message is received"""
def on_message(client, obj, msg):
    data = json.loads(msg.payload)
    token = get_token(cfg['tokenurl'], data['username'], data['password'])
    data['wsfunction'] = 'local_mem_post_event'
    data['wstoken'] = token
    del data['username']
    del data['password']
    # Limit precision for PHP compatibility
    data['datetime'] = data['datetime'][:23] + 'Z'
    post(cfg['posturl'], data)

def signal_term_handler(signal, frame):
    print 'terminating...'
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

mqtt = mqtt.Client(protocol=mqtt.MQTTv31)
with open("agent.yml", 'r') as ymlfile:
  cfg = yaml.load(ymlfile)

mqtt.connect(cfg['server'])
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.subscribe("mooc/")
mqtt.loop_forever()
