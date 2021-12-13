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
Scriptit olettavat koneella olevan Statsd data agregaattorin. Asennus näin:

```bash
sudo apt update && sudo apt -y upgrade
sudo apt-cache search graphite | grep "graphite-"
sudo apt-get install graphite-carbon graphite-web
cat /etc/carbon/carbon.conf |egrep -v '#' |sed '/^$/d'
sudo systemctl start carbon-cache
sudo systemctl status carbon-cache
sudo systemctl enable carbon-cache
Uuidgen
sudo nano /etc/graphite/local_settings.py
```
Muutettavat tiedot ovat:
○ Time_zone = "Europe/Helsinki"
○ Secret_key ='ssssss'
salaiseen avaimeen voit syöttää uuidgen antaman arvon ja tietokanta osaan vaihdetaan seuraavat tiedot:
DATABASES = {
    'default': {
        'NAME': 'graphite',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'graphite',
        'PASSWORD': 'StrongP@Ssword',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}


```bash
sudo apt install python3-dev libmysqlclient-dev default-libmysqlclient-dev python3-pip
sudo pip3 install mysqlclient
sudo sed -i 's/from cgi import parse_qs/from urllib.parse import parse_qs/' /usr/lib/python3/dist-packages/graphite/render/views.py
sudo sed -i -E "s/('django.contrib.contenttypes')/\1,\n  'django.contrib.messages'/" /usr/lib/python3/dist-packages/graphite/app_settings.py
sudo /usr/lib/python3/dist-packages/django/bin/django-admin.py migrate --settings=graphite.settings
```


