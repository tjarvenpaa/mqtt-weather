# mqtt-weather
mqtt python scripts to transfer weather information from raspberry pi envirophat to graphite tsdb

# Scriptien ajamiseen tarvittavat python ajurit

Sriptit tarvitsevat toimiakseen muutaman ajurin. Conn ja Datareader scriptit tarvitsevat ainakin paho-mqtt -clientin sekä statsd clientin. Näiden asentaminen tapahtuu seuraavasti:

```bash
sudo apt update && apt -y upgrade
sudo apt install python3-pip python3
sudo -H python3 -m pip install paho-mqtt statsd
```

Fmikarhi scripti käy noutamassa ilmatieteenlaitoksen opendata ympäristöstä paikan nimeen sidottuna lämpötilan ja ilmanpaineen. Tämä scripti käyttää taustarakenteenaan pypi kannasta poimittua fmi-weather-client palikkaa. Ajuri on python3 pohjainen, joten suoritusympäristön täytyy olla python3. Asennus seuraavasti:

```bash
sudo -H python3 -m pip install fmi-weather-client
```

# Scriptien ajaminen

MQTT brokerilta tietoa hakevat scriptit on kirjoitettu looppina, eli ohjelmia ajetaan jatkuvasti. FMiKarhi scripti on kerta suoritteinen, eli se voidaan ajastaa toimimaan kerran 5 minuuttiin. 
Ajastus käy yksinkertaisimmin käyttäen student käyttäjän crontab ympäristöä. Seuraavasti:

```bash
crontab -e
```

avautuvaan editoriin annetaan ajettavaksi scriptiksi seuraavalla tavalla:

```cron
*/5 * * * * python3 /polku/jossa/fmikarhi.py
```

Jatkuvasti ajettavat scriptit voidaan yksinkertaisesti ajaa SCREEN ympäristössä. https://www.tecmint.com/screen-command-examples-to-manage-linux-terminals/ 

```bash
sudo apt install screen
screen python3 /polku/jossa/conn.py
```

samassa polussa täytyy olla myös datareader.py, jota conn.py kutsuu käsitelläkseen hakemaansa dataa. 
Jotta scripti toimii oikein, täytyy datareader.py scriptin lopussa olevat topic muuttuja vaihtaa vastaamaan lähetettäviä tietoja.
