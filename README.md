# arducam uvc python demo
## introduce
arducam uvc camera opencv python demo
## install dependencies
```shell
python -m pip install -r requirements.txt
```
## RUN 
If you are using a windows system, it is recommended to set the -v parameter to 1

Type "a" on the keyboard to save a 200MP RAW image
```shell
python arducam_demo.py -W 1280 -H 720 -F -i 0 --wait-frames 2
```

## Convert 200MP single image

```shell
python arducam_200mp_convert.py -f <raw image path> -c 1
```

## Batch convert 200MP images

```shell
python arducam_200mp_convert.py -f <Raw image folder path> -b -c 1
```