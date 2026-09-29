# AutoReck: Detecting Red Packet Reward Inconsistencies in Android Applications

## About
This repository stores the dataset and the code for AutoReck, a prototype system for the paper "AutoReck: Detecting Red Packet Reward Inconsistencies in Android Applications".
AutoReck is the approach we proposed in this paper for automatically detecting red packet reward inconsistencies in Android apps.

## Datasets
In the evaluation experiment, we use 334 Android apps with red packets from Google Play Store and three major Chinese app markets (Tencent, Huawei and Xiaomi).
We provide these datasets in the "dataset" folder.

## Prerequisite

1. `Python 3`
2. `Android SDK`
3. `Android device` equipped with `Magisk` and `LSPosed` frameworks


## How to use

1. Connect an Android device to your host machine via `adb`.

2. Install the hooking module (`runtime_hooking/ApkHook.apk`) on the Android device.

3. Configure the parameters of the hooking module, such as the host's IP address and the relevant parameters of the target app to be hooked.

4. Execute `loader.py` file to dynamically explore the app and execute red packet tasks.