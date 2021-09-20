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
    from m5stack import *
    from m5stack_ui import *
    from uiflow import *
    from IoTcloud.AWS import AWS
    import json


    screen = M5Screen()
    screen.clean_screen()
    screen.set_screen_bg_color(0x5a3b5d)


    maskboxes = None
    employee = None


    mask_button = M5Btn(text='Masks', x=10, y=56, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    medicine_button = M5Btn(text='Medicine', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    Stock_Label = M5Label('Stock', x=27, y=7, color=0xffffff, font=FONT_MONT_20, parent=None)
    add_mask = M5Btn(text='+', x=46, y=143, w=75, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    remove_mask = M5Btn(text='-', x=186, y=145, w=75, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    medicine_amount = M5Label('Amount: 0', x=43, y=64, color=0xffffff, font=FONT_MONT_40, parent=None)

    from numbers import Number



    def mask_button_pressed():
      global maskboxes, employee
      medicine_amount.set_hidden(False)
      mask_button.set_hidden(True)
      medicine_button.set_hidden(True)
      medicine_remove.set_hidden(False)
      add_medicine.set_hidden(False)
      pass
    mask_button.pressed(mask_button_pressed)

    def add_mask_pressed():
      global maskboxes, employee
      maskboxes = (maskboxes if isinstance(maskboxes, Number) else 0) + 1
      aws.publish(str('masks'),str((json.dumps(({'Employee':employee,'Amount':maskboxes})))))
      medicine_amount.set_text(str((str('Amount:') + str(maskboxes))))
      pass
    add_mask.pressed(add_mask_pressed)

    def remove_mask_pressed():
      global maskboxes, employee
      maskboxes = (maskboxes if isinstance(maskboxes, Number) else 0) + -1
      aws.publish(str('masks'),str((json.dumps(({'Employee':employee,'Amount':maskboxes})))))
      medicine_amount.set_text(str((str('Amount:') + str(maskboxes))))
      pass
    remove_mask.pressed(remove_mask_pressed)


    employee = 'Ashwin'
    medicine_amount.set_hidden(True)
    add_medicine.set_hidden(True)
    medicine_remove.set_hidden(True)
    mask_button.set_hidden(False)
    medicine_button.set_hidden(False)
    maskboxes = 0
    aws = AWS(things_name='volatus', host='affaxcdeac20e-ats.iot.us-east-1.amazonaws.com', port=8883, keepalive=60, cert_file_path="/flash/res/certificate.pem.crt", private_key_path="/flash/res/private.pem.key")
    aws.start()
