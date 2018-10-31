# robotnik_barcode_scanner

## Params
* port (string)
 * default: /dev/input/barcode_scanner
* topic (string)
  * default: barcode_scanner

## Topics
### Publishers

* ~heading (std_msgs/Header)
  * Publishes the time stamp and data of the barcode scanner

## Bringup

'''
roslaunch robotnik_barcode_scanner barcode_scanner.launch
'''

## Installation instructions
See where the device "BarCode WPM" is:
  $ lsusb
- Find BUS 00x Device 0xx: ID idVendor:idProduct Winbond Electronics Corp.
- Create an udev rule
  $ sudo nano /etc/udev/rules.d/40-scanner.rules
- And write (modifying idVendor and idProduct if is necessary):
  KERNEL=="event[0-9]*", SUBSYSTEM=="input", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="c141", SYMLINK="input/barcode_scanner",GROUP="dialout", MODE="0666"
- Execute:
  $ sudo service udev restart
  $ sudo udevadm trigger
- Check if the link has been created:
  $ ls -ln /dev/input | grep barcode
