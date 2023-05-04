# HoneyEVSE: a low-interaction honeypot for EVSE emulation
This repository contains all the code realted to the implementation for HoneyEVSE.

The project was develped for the course Advance Topics in Computer Networking Security of the Master Degree Computer Science at Univeristy of Padova.

The complete paper to our project is available at the file `Report.pdf`.

![image](https://user-images.githubusercontent.com/50354884/219980176-44dd4891-3a9e-47e6-b105-8884642a3ba4.png)

## Requirements

- Operating system: tested on **ubuntu 18.04** and **20.04**.  
  Currently, the Honeypot was tested on a non-server version since the HMI requires a browser to be visualized.  
  Furthermore, some scripts in the physical process span new terminals tabs with the command gnome-terminal.
  
- Python 3 for the HMI web app (installation included in the preconfigured script).

- TimeMe.js library (https://github.com/jasonzissman/TimeMe.js/)

## Installation

In order to install the noeyport, clone this repo using the command:

`git clone https://github.com/massimilianobaldo/HoneyEVSE`

Once done that, there is a helper script `install.sh` that will install all the packages needed.

## Usage
To run the honeypot you have to:

1. Get an API-KEY from the site of __[Caltech](https://ev.caltech.edu/register)__

2. Copy that API-KEY inside the Makefile at line 6  
   `API-KEY = "YOUR API KEY"`
   
3. Use `make evse` to generate the dotenv file, the charges and start the HMI

4. From inside the repository, run:  
  `sudo honeyd -d -p nmap-os-db -i INTERFACE -l honeyd.log -f honeyd.conf IP --disable-webserver`  
  where IP is the same IP address of Honeyd configuration file and INTERFACE is the interface of the listening port.

6. The host computer has to intercept the network traffic addressed to the Honeypot, to allow honeyd to reply correctly.  
    A useful tool that you can use to achieve this result is farpd:  
    `sudo farpd -d -i INTERFACE <IP>`

## Test functionality
To check the correct functioning of HoneyEVSE, you can scan the IP from outside the Host machine with Nmap.

To do this, first install Nmap: `sudo apt install nmap`.

You can use the file with `scanners.sh`. You can launch it all together or just manually pick and run them.
