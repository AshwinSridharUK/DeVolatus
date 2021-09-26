from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
from IoTcloud.AWS import AWS
import json

import imu

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x5a3b5d)


Capacity = None #Creates variable called "Capacity" without any value

imu0 = imu.IMU()
Sign_In_Visitor = M5Btn(text='Sign In', x=10, y=56, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
Sign_Out_Visitor = M5Btn(text='Sign Out', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
label0 = M5Label('Home', x=27, y=8, color=0xffffff, font=FONT_MONT_20, parent=None)
Staff_Button_Home = M5Btn(text='Staff', x=10, y=56, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
Visitor_Button_Home = M5Btn(text='Visitor', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
Error_Registration = M5Label('Error- Contact Front Desk', x=68, y=213, color=0xffffff, font=FONT_MONT_14, parent=None)
#creates all the UI elements
from numbers import Number


# Shows staff (non-functional) and visitor button on UI
def OpenHome():
  global Capacity
  Staff_Button_Home.set_hidden(False)
  Visitor_Button_Home.set_hidden(False)

# Hides staff (non-functional) and visitor button on UI.
def CloseHome():
  global Capacity
  Staff_Button_Home.set_hidden(True)
  Visitor_Button_Home.set_hidden(True)

# Shows the visitor sign in and out buttons
def OpenVisitorSign():
  global Capacity
  Sign_In_Visitor.set_hidden(False)
  Sign_Out_Visitor.set_hidden(False)

# Hides the visitor sign in and out buttons
def CloseVisitorSign():
  global Capacity
  Sign_In_Visitor.set_hidden(True)
  Sign_Out_Visitor.set_hidden(True)

# Changes from initial to visitor sign in screen when visitor button pressed
def Visitor_Button_Home_pressed():
  global Capacity
  CloseHome()
  wait(2)
  OpenVisitorSign()
  pass
Visitor_Button_Home.pressed(Visitor_Button_Home_pressed)
# Increases Capacity variable by + 1 and sends MQTT request to AWS IoT. Plays speaker notification and WAV file to validate sucess on the user end.
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
# Decreases Capacity variable by 1 and sends MQTT request to AWS IoT. Plays speaker notification and WAV file to validate sucess on the user end. If capacity is already equal to 0 an error is thrown.
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


Capacity = 0
Error_Registration.set_hidden(True)
Staff_Button_Home.set_hidden(True)
Visitor_Button_Home.set_hidden(True)
Sign_In_Visitor.set_hidden(True)
Sign_Out_Visitor.set_hidden(True)
rgb.setColorAll(0xffffff)
aws = AWS(things_name='enterthingname', host='enterhostname', port=8883, keepalive=60, cert_file_path="/flash/res/certificate.pem.crt", private_key_path="/flash/res/private.pem.key")
#setups AWS IoT connection- replace with your own credentials
aws.start()
#Checks Orientation of device, once the orientation is set it will either replace with the user or staff mode. Can only be changes by switching the device off and turning back around
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

    import time

    screen = M5Screen()
    screen.clean_screen()
    screen.set_screen_bg_color(0x5a3b5d)


    maskboxes = None
    employee = None
    medicine = None
    CodeData = None
    #Creates necessary variables

    mask_button = M5Btn(text='Masks', x=10, y=56, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    mask_amount = M5Label('Amount: 0', x=42, y=48, color=0xffffff, font=FONT_MONT_40, parent=None)
    medicine_button = M5Btn(text='Medicine', x=10, y=140, w=300, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    Stock_Label = M5Label('Stock', x=27, y=7, color=0xffffff, font=FONT_MONT_20, parent=None)
    add_mask = M5Btn(text='+', x=56, y=101, w=75, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    remove_mask = M5Btn(text='-', x=186, y=103, w=75, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_40, parent=None)
    Code_Display = M5Btn(text='Enter Staff Code ', x=10, y=16, w=300, h=65, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_26, parent=None)
    A_Button = M5Btn(text='A', x=7, y=90, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    B_Button = M5Btn(text='B', x=89, y=90, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    C_Button = M5Btn(text='C', x=171, y=90, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    One_Button = M5Btn(text='1', x=7, y=164, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    Two_Button = M5Btn(text='2', x=89, y=164, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    Del_Button = M5Btn(text='<', x=253, y=90, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    Three_Button = M5Btn(text='3', x=170, y=164, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    Ent_Button = M5Btn(text='=', x=253, y=164, w=60, h=60, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    Back_Masks = M5Btn(text='<', x=6, y=175, w=56, h=56, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_46, parent=None)
    add_medicine = M5Btn(text='+', x=56, y=101, w=75, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    remove_medicine = M5Btn(text='-', x=186, y=103, w=75, h=70, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    back_medicine = M5Btn(text='<', x=6, y=175, w=56, h=56, bg_c=0xfedc2a, text_c=0x5a3b5d, font=FONT_MONT_42, parent=None)
    medicine_amount = M5Label('Amount:', x=42, y=48, color=0xffffff, font=FONT_MONT_42, parent=None)
    #Creates UI elements (buttons, labels etc.)
    from numbers import Number


    #Automatically hides UI elements and switches to mask inventory mode
    def mask_button_pressed():
      global maskboxes, employee, medicine, CodeData
      mask_amount.set_hidden(False)
      Back_Masks.set_hidden(False)
      mask_button.set_hidden(True)
      medicine_button.set_hidden(True)
      add_mask.set_hidden(False)
      remove_mask.set_hidden(False)
      pass
    mask_button.pressed(mask_button_pressed)
  #Adds mask to the variable "maskboxes" and publishhes new value as MQTT using JSON format, with employee name and maskboxes amount
    def add_mask_pressed():
      global maskboxes, employee, medicine, CodeData
      maskboxes = (maskboxes if isinstance(maskboxes, Number) else 0) + 1
      aws.publish(str('masks'),str((json.dumps(({'Employee':employee,'Amount':maskboxes})))))
      mask_amount.set_text(str((str('Amount:') + str(maskboxes))))
      pass
    add_mask.pressed(add_mask_pressed)
#Removes mask to the variable "maskboxes" and publishhes new value as MQTT using JSON format, with employee name and maskboxes amount. Only works when masks amount is >0 or else throws error to the user
    def remove_mask_pressed():
      global maskboxes, employee, medicine, CodeData
      if maskboxes > 0:
        maskboxes = (maskboxes if isinstance(maskboxes, Number) else 0) + -1
        aws.publish(str('masks'),str((json.dumps(({'Employee':employee,'Amount':maskboxes})))))
        mask_amount.set_text(str((str('Amount:') + str(maskboxes))))
      else:
        rgb.setColorAll(0xff0000)
        speaker.playWAV("res/error.wav")
        wait(1)
        rgb.setColorAll(0xffffff)
      pass
    remove_mask.pressed(remove_mask_pressed)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Buttons for the employee code setup
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def A_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      employee = (str(employee) + str('A'))
      Code_Display.set_btn_text(employee)
      pass
    A_Button.pressed(A_Button_pressed)

    def B_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      employee = (str(employee) + str('B'))
      Code_Display.set_btn_text(employee)
      pass
    B_Button.pressed(B_Button_pressed)

    def C_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      employee = (str(employee) + str('C'))
      Code_Display.set_btn_text(employee)
      pass
    C_Button.pressed(C_Button_pressed)

    def One_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      employee = (str(employee) + str('1'))
      Code_Display.set_btn_text(employee)
      pass
    One_Button.pressed(One_Button_pressed)

    def Two_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      employee = (str(employee) + str('2'))
      Code_Display.set_btn_text(employee)
      pass
    Two_Button.pressed(Two_Button_pressed)

    def Del_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      Code_Display.set_btn_text('Enter Staff Code')
      employee = ''
      pass
    Del_Button.pressed(Del_Button_pressed)

    def Three_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      employee = (str(employee) + str('3'))
      Code_Display.set_btn_text(employee)
      pass
    Three_Button.pressed(Three_Button_pressed)
#Enter button which checks to see if the employee codes is stored inside the map. If true, extracts the key value and publishes a MQTT message with employee code and name
    def Ent_Button_pressed():
      global maskboxes, employee, medicine, CodeData
      if (employee in CodeData.keys()) == True:
        aws.publish(str('Code'),str((json.dumps(({'EmpCode':employee,'Name':(CodeData[employee])})))))
        Code_Display.set_btn_text('Enter Staff Code')
        rgb.setColorAll(0x33ff33)
        speaker.playWAV("res/success.wav")
        wait(1)
        rgb.setColorAll(0xffffff)
        mask_button.set_hidden(False)
        medicine_button.set_hidden(False)
        A_Button.set_hidden(True)
        B_Button.set_hidden(True)
        C_Button.set_hidden(True)
        One_Button.set_hidden(True)
        Two_Button.set_hidden(True)
        Three_Button.set_hidden(True)
        Ent_Button.set_hidden(True)
        Del_Button.set_hidden(True)
        Code_Display.set_hidden(True)
      else:
        Code_Display.set_btn_text('Enter Staff Code')
        employee = ''
        rgb.setColorAll(0xff0000)
        speaker.playWAV("res/error.wav")
        wait(1)
        rgb.setColorAll(0xffffff)
      pass
    Ent_Button.pressed(Ent_Button_pressed)

    def Back_Masks_pressed():
      global maskboxes, employee, medicine, CodeData
      add_mask.set_hidden(True)
      remove_mask.set_hidden(True)
      Back_Masks.set_hidden(True)
      mask_amount.set_hidden(True)
      medicine_button.set_hidden(False)
      mask_button.set_hidden(False)
      pass
    Back_Masks.pressed(Back_Masks_pressed)

    def medicine_button_pressed():
      global maskboxes, employee, medicine, CodeData
      medicine_amount.set_hidden(False)
      back_medicine.set_hidden(False)
      mask_button.set_hidden(True)
      medicine_button.set_hidden(True)
      add_medicine.set_hidden(False)
      remove_medicine.set_hidden(False)
      pass
    medicine_button.pressed(medicine_button_pressed)

    def add_medicine_pressed():
      global maskboxes, employee, medicine, CodeData
      medicine = (medicine if isinstance(medicine, Number) else 0) + 1
      aws.publish(str('medicine'),str((json.dumps(({'Employee':employee,'Amount':medicine})))))
      medicine_amount.set_text(str((str('Amount:') + str(medicine))))
      pass
    add_medicine.pressed(add_medicine_pressed)

    def remove_medicine_pressed():
      global maskboxes, employee, medicine, CodeData
      if medicine > 0:
        medicine = (medicine if isinstance(medicine, Number) else 0) + -1
        aws.publish(str('medicine'),str((json.dumps(({'Employee':employee,'Amount':medicine})))))
        medicine_amount.set_text(str((str('Amount:') + str(medicine))))
      else:
        rgb.setColorAll(0xff0000)
        speaker.playWAV("res/error.wav")
        wait(1)
        rgb.setColorAll(0xffffff)
      pass
    remove_medicine.pressed(remove_medicine_pressed)

    def back_medicine_pressed():
      global maskboxes, employee, medicine, CodeData
      add_medicine.set_hidden(True)
      remove_medicine.set_hidden(True)
      back_medicine.set_hidden(True)
      medicine_amount.set_hidden(True)
      medicine_button.set_hidden(False)
      mask_button.set_hidden(False)
      pass
    back_medicine.pressed(back_medicine_pressed)


    employee = ''
    Stock_Label.set_hidden(True)
    medicine_amount.set_hidden(True)
    mask_amount.set_hidden(True)
    mask_button.set_hidden(True)
    medicine_button.set_hidden(True)
    add_mask.set_hidden(True)
    remove_mask.set_hidden(True)
    add_medicine.set_hidden(True)
    remove_medicine.set_hidden(True)
    A_Button.set_hidden(False)
    B_Button.set_hidden(False)
    C_Button.set_hidden(False)
    One_Button.set_hidden(False)
    Two_Button.set_hidden(False)
    Del_Button.set_hidden(False)
    Code_Display.set_hidden(False)
    Back_Masks.set_hidden(True)
    back_medicine.set_hidden(True)
    maskboxes = 0
    CodeData = {'AB321':'Ashwin','CB123':'James'} #Example map ("CodeData") with user names and keycodes.
    aws = AWS(things_name='enterthingname', host='enterhostname', port=8883, keepalive=60, cert_file_path="/flash/res/certificate.pem.crt", private_key_path="/flash/res/private.pem.key")
    aws.start()
