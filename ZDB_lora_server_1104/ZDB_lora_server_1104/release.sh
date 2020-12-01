python3 setup.py build_ext
cd meterreader
python3 setup.py build_ext
cd ..
release_dir=ZDB_lora_server_release_`date +%Y%m%d%H%M%S`
release_zip="$release_dir".zip
mkdir $release_dir
mkdir -p $release_dir/meterreader
cp -a main.py own_devices.ini server.ini  $release_dir
cp -a build/lib.linux-x86_64-3.6/zdb_server.cpython-36m-x86_64-linux-gnu.so $release_dir/zdb_server.so
cp -a meterreader/__init__.py $release_dir/meterreader
cp -a meterreader/build/lib.linux-x86_64-3.6/meterreader/Mreader.cpython-36m-x86_64-linux-gnu.so $release_dir/meterreader/Mreader.so
zip -r $release_zip $release_dir
echo "Done! Release file is $release_zip"