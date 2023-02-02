# DeepPiCar_THD
### Step 0: Raspberry Pi mit OS and SSH einrichten

### Step 1: Wifi-Hotspot einrichten

```python
curl -sL https://install.raspap.com | bash
```

```python
sudo reboot
```

Connect with raspi-webgui

```python
WLAN-Name: raspi-webgui
Passwort: ChangeMe
IP-Adresse der Admin-Oberfläche: 10.3.141.1
Standardbenutzer: admin
Standard-Passwort: secret
```

```python
ssh -Y pi@10.3.141.1
```

Wenn man den Pi nun an ein LAN anschließt hat man auch internet

### Step 2: DeepPiCar_THD einrichten

```python
git clone https://github.com/THD-PiCar/DeepPiCar_THD.git
```

### Step 3: PiCar einrichten

```python
cd DeepPiCar_THD
```

```python
git clone --recursive [https://github.com/sunfounder/SunFounder_PiCar.git](https://github.com/sunfounder/SunFounder_PiCar.git)
```

```python
cd SunFounder_PiCar
```

```python
sudo python [setup.py](http://setup.py/) install
```

```python
cd ..
```

```python
git clone [https://github.com/sunfounder/SunFounder_PiCar-V](https://github.com/sunfounder/SunFounder_PiCar-V) -b V3.0
```

```python
cd  SunFounder_PiCar-V
```

```python
sudo ./install_dependencies
```

```python
reboot yes
```

### Step 4: DeepPiCar einrichten

Connect with raspi-webgui

```python
ssh -Y pi@10.3.141.1
```

```
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update
```

```python
sudo apt-get install libedgetpu1-std
```

Now connect the USB Accelerator to your computer using the provided USB 3.0 cable. If you already plugged it in, remove it and replug it.

```python
sudo apt-get install python3-pycoral
```

```python
cd DeepPiCar_THD
```

```
mkdir coral && cd coral

git clone https://github.com/google-coral/pycoral.git

cd pycoral
```

```python
bash examples/install_requirements.sh classify_image.py
```

Test:

```
python3 examples/classify_image.py \
--model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
--labels test_data/inat_bird_labels.txt \
--input test_data/parrot.jpg
```

```
----INFERENCE TIME----
Note: The first inference on Edge TPU is slow because it includes loading the model into Edge TPU memory.
11.8ms
3.0ms
2.8ms
2.9ms
2.9ms
-------RESULTS--------
Ara macao (Scarlet Macaw): 0.75781
```

### Step 5: Erstes Model starten

```python
cd 
```

```python
cd DeepPiCar_THD
```

```python
python3 [start.py](http://start.py/) --model=model/model_edgetpu.tflite --labels=model/labels.txt
```

Press q to quit the program

### Quellen:
