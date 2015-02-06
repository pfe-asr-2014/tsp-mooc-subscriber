# tsp-mooc-subscriber
Container fetching events from the server's broker and sending them to moodle

## Configure

Configure the application in `app/agent.yml` :

```yaml
# the MQTT server you collect events from
server: "tsp-mooc-server"
# the URL of your moodle's token.php
tokenurl: "http://IP:PORT/login/token.php"
# the URL of your moodle's server.php
posturl: "http://IP:PORT/webservice/rest/server.php"
```

## License

This software is distributed under the terms of the MIT license. See [LICENSE](./LICENSE) for details.
