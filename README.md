# robotnik_barcode_scanner

See where is the device "BarCode WPM ..."
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
