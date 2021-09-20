from m5stack import *
from m5stack_ui import *
from uiflow import *
from IoTcloud.AWS import AWS
import time
import json

import imu

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x5a3b5d)


Capacity = None

imu0 = imu.IMU()
Sign_In_Visitor = M5Btn(text='Sign In', x=10, y=56, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
Sign_Out_Visitor = M5Btn(text='Sign Out', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
label0 = M5Label('Home', x=27, y=8, color=0xffffff, font=FONT_MONT_20, parent=None)
Staff_Button_Home = M5Btn(text='Staff', x=10, y=56, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
Visitor_Button_Home = M5Btn(text='Vistor', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
Error_Registration = M5Label('Error- Contact Front Desk', x=68, y=213, color=0xffffff, font=FONT_MONT_14, parent=None)
Temperature = M5Label('Temperature: ', x=22, y=76, color=0x000, font=FONT_MONT_24, parent=None)
Close_Sign = M5Btn(text='Close Sign', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)

from numbers import Number


# Describe this function...
def CloseHome():
  global Capacity
  Staff_Button_Home.set_hidden(True)
  Visitor_Button_Home.set_hidden(True)

# Describe this function...
def OpenHome():
  global Capacity
  Staff_Button_Home.set_hidden(False)
  Visitor_Button_Home.set_hidden(False)

# Describe this function...
def OpenVisitorSign():
  global Capacity
  Sign_In_Visitor.set_hidden(False)
  Sign_Out_Visitor.set_hidden(False)

# Describe this function...
def CloseVisitorSign():
  global Capacity
  Sign_In_Visitor.set_hidden(True)
  Sign_Out_Visitor.set_hidden(True)


def Sign_In_Visitor_pressed():
  global Capacity
  Capacity = (Capacity if isinstance(Capacity, Number) else 0) + 1
  aws.publish(str('capacity'),str((json.dumps(({'capacity':Capacity})))))
  wait(1.5)
  rgb.setColorAll(0x33ff33)
  speaker.playWAV("res/success.wav")
  Sign_In_Visitor.set_hidden(True)
  Sign_Out_Visitor.set_hidden(True)
  CloseVisitorSign()
  OpenHome()
  pass
Sign_In_Visitor.pressed(Sign_In_Visitor_pressed)

def Sign_Out_Visitor_pressed():
  global Capacity
  if Capacity > 0:
    Capacity = (Capacity if isinstance(Capacity, Number) else 0) + -1
    aws.publish(str('capacity'),str((json.dumps(({'capacity':Capacity})))))
    wait(1.5)
    rgb.setColorAll(0x33ffff)
    speaker.playWAV("res/success.wav")
    CloseVisitorSign()
    OpenHome()
  else:
    Error_Registration.set_hidden(False)
    wait(3)
    Error_Registration.set_hidden(True)
  pass
Sign_Out_Visitor.pressed(Sign_Out_Visitor_pressed)

def Visitor_Button_Home_pressed():
  global Capacity
  CloseHome()
  wait(2)
  OpenVisitorSign()
  pass
Visitor_Button_Home.pressed(Visitor_Button_Home_pressed)


Capacity = 0
Error_Registration.set_hidden(True)
Temperature.set_hidden(True)
Staff_Button_Home.set_hidden(True)
Visitor_Button_Home.set_hidden(True)
Sign_In_Visitor.set_hidden(True)
Sign_Out_Visitor.set_hidden(True)
Close_Sign.set_hidden(True)
rgb.setColorAll(0xffffff)
aws = AWS(things_name='volatus', host='affaxcdeac20e-ats.iot.us-east-1.amazonaws.com', port=8883, keepalive=60, cert_file_path="/flash/res/certificate.pem.crt", private_key_path="/flash/res/private.pem.key")
aws.start()
if (imu0.ypr[1]) > 5:
  Error_Registration.set_hidden(True)
  Staff_Button_Home.set_hidden(False)
  Visitor_Button_Home.set_hidden(False)
else:
  if (imu0.ypr[1]) < -5:
    Close_Sign.set_hidden(False)
    Temperature.set_hidden(False)
    Temperature.set_text(str((str('Temperature:') + str((power.getTempInAXP192())))))
