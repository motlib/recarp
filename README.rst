# recarp

====================================================
Remote Control of Air Conditioning by a Raspberry PI
====================================================

This project implements a distributed climate sensor (tempaerature,
humidity, air pressure) and actor (air conditioning and heating
control) system. It is based on a central web server and client nodes
(Raspberry PI) which connect to the server by use of MQTT to send
sensor data and to receive remote commands to control the air
conditioning / heating system by infrared commands.

