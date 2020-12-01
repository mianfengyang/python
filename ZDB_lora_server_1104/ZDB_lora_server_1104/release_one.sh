pyinstaller -F main.py
cp -a own_devices.ini server.ini  ./dist
mv ./dist/main ./dist/ZDB_LoRa_server_V12_`date '+%Y%m%d'`