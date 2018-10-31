#!/usr/bin/env python
# coding=utf-8

import rospy
import evdev
import datetime
from evdev import InputDevice, categorize, ecodes
from std_msgs.msg import Header

'''
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

'''

keys = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

class BarCodeScanner:

  def __init__(self, args):
    self.topic = args['topic']
    self.port = args['port']
    self.dev = InputDevice(self.port)
    self.seq = 0
    self.init_time = datetime.datetime.now()
    rospy.loginfo(self.dev)

    # Create publisher
    self.pub = rospy.Publisher(self.topic, Header, queue_size=10)

  def scanBarcode(self):
    barcode = ''
    while True:
        event = self.dev.read_one()
        if event is None and barcode == '':
          #There are blank events in between characters, 
          #so we don't want to break if we've started
          #reading them
          if rospy.is_shutdown():
					  exit()
          break #nothing of importance, start a new read. 
        try:
          if event is not None:
            if event.type == ecodes.EV_KEY:
              data = categorize(event)
              if data.keystate == 0 and data.scancode != 42: # Catch only keyup, and not Enter
                if data.scancode == 28: #looking return key to be pressed
                  #rospy.loginfo(barcode)
                  msg = Header()
                  msg.seq = self.seq
                  self.seq = self.seq + 1
                  time_diff = datetime.datetime.now() - self.init_time
                  msg.stamp.secs = time_diff.seconds
                  msg.stamp.nsecs = time_diff.microseconds * 1000
                  msg.frame_id = barcode
                  self.pub.publish(msg)
                  barcode = ''
                else:
                    barcode += keys[data.scancode] # add the new char to the barcode
        except AttributeError:
            rospy.logerr("error parsing stream")
            return 'SOMETHING WENT WRONG'


if __name__ == "__main__":
  
  rospy.init_node("barcode_scanner")

  _name = rospy.get_name().replace('/','')

  arg_defaults = {
    'topic': 'barcode_scanner',
    'port': '/dev/input/barcode_scanner'
  }
  
  args = {}
  
  for name in arg_defaults:
    try:
      if rospy.search_param(name): 
        args[name] = rospy.get_param('~%s'%(name)) # Adding the name of the node, because the param has the namespace of the node
      else:
        args[name] = arg_defaults[name]
    except rospy.ROSException, e:
      rospy.logerr('%s: %s'%(e, _name))
  

  rc_node = BarCodeScanner(args)

  while(True):
    rc_node.scanBarcode()
