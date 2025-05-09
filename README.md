# Arducam UVC Python Demo
## Install Dependencies
```shell
python -m pip install -r requirements.txt
```
## RUN 
If you are using a windows system, it is recommended to set the -v parameter to 1

Type "a" on the keyboard to save a 200MP RAW image
```shell
python arducam_demo.py -W 1280 -H 720 --Focus 346 -i 0 --wait-frames 2 --read-eeprom
```

## Convert 200MP Image (Only for Windows11/10)

```shell
python arducam_200mp_convert.py -f <raw image path>
```