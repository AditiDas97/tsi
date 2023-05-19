# tsi
## tsi : UCD-500 API package
We should import this package to make use of the UCD-500 hardware functionalities via APIs in any automated way of testing. It is a collection of packages and modules that can be used to access all the operations that are supported by the UCD-User-Interface Application (GUI)

## tsi_lib.py and tsi_devices
This folder package has been provided by Unigraf, containing the entire API library package (collection of related modules) to access the functionalities it has to offer. 

## Unigraf.py
Unigraf.py is a class that acts as a wrapper on top of the parent tsi_lib package.It contains exposed methods which one can call, to configure and test the device accordingly and fetch all kinds of protocol level information that is possible from the UCD user-interface application.

## default_EDID 
default_EDID folder contains the different resolution/timing files that can be loaded and written, so that the UCD-500 can act like that particular resoltution monitor to which is has been configured to.
It also contains the APIs to record event (AUX etc) logs, read DPCD register values or store the entire DPCD Dump into a file.

# NOTE:
setup.py is not part of the package, it is only required to make a wheel file from tsi package.
To make a wheel file, follow the below steps:
1. Clone the tsi repo, entire contents will be cloned inside a "tsi" named folder.
2. Move the setup.py one level out of the folder and keep in the same directory where "tsi" folder was cloned.
3. Open cmd and paste the following commands:
  i) pip install wheel
  ii) python setup.py bdist_wheel
4. This will create "build" and "dist" folders.
   Inside the "dist" folder, we will be having the corresponding wheel file.
   
   


