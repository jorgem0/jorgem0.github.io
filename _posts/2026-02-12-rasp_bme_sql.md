---
title: Raspberry Pi BME280 MySQL Data Collection
description: Collect data using a Raspberry Pi and BME280 sensor and upload it to a MySQL database.
layout: post
toc: true
---

![jorgem0/raspberry\u005fpi\u005fbme280\u005fmysql](/assets/images/github.svg){: width="100" height="100" }
_<a href="https://github.com/jorgem0/raspberry_pi_bme280_mysql" target="_blank" rel="noopener noreferrer">jorgem0/raspberry_pi_bme280_mysql</a>_

## Introduction

This tutorial will use a Raspberry Pi Zero W, a BME280 sensor, and MariaDB in order to collect temperature, pressure, and humidity data and store it in a DBMS.

## Setting Up the Raspberry Pi

The first step for this project is to install the Raspbian Stretch OS for the Raspberry Pi. Download the Raspbian Stretch OS image from the [Raspberry Pi website](https://www.raspberrypi.org/downloads/raspbian/){:target="_blank" rel="noopener noreferrer"} and flash it to your MicroSD card using [Etcher](https://etcher.io){:target="_blank" rel="noopener noreferrer"} as seen in the [Raspberry Pi tutorial](https://www.raspberrypi.org/documentation/installation/installing-images/README.md){:target="_blank" rel="noopener noreferrer"}. Once the process has been completed, insert the MicroSD card into your Raspberry Pi and install the OS (it should install automatically). You will now be greeted with the Raspbian Stretch OS desktop. Go to **Raspberry Pi Configuration** by selecting the menu in the top left corner of the screen. Select the **Interfaces** tab and enable **SSH** and **I2C**. Also set up your Wi-Fi in the top right corner.

![Settings](/assets/images/rasp_bme_sql/settings.png)
_Settings_

![Interfaces and Wi-Fi](/assets/images/rasp_bme_sql/interfaces.png)
_Interfaces and Wi-Fi_

