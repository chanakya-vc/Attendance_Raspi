'''
*Written by Vaibhav Choudhary. For more information please 
*visit: www.vaibhavchoudhary.com
*
*Copyright(C) 2016 Vaibhav Choudhary, CEDT, NSIT
*
*Portable Attendance Taker on the Raspberry PI
*
*This code may be copied and/or modified freely according to GNU General Public  
*License version 2 as published by the Free Software Foundation, provided   
*the following conditions are also met:
*1) Redistributions/adaptions of source code must retain this copyright
*   notice on the top, giving credit to the original author, along with 
*   this list of conditions.
*
*2) Redistributions in binary form, compiled from this source code and/or 
*   modified/adapted versions of this source code, must include this copyright 
*   notice giving credit to the original author, along with this list of conditions 
*   in the documentation and other materials provided with the
*   distribution.
*
*3) The original author shall not held for any loss arising from using this code.
*   There is no implied warranty associated with this code.
'''
import MySQLdb
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_Nokia_LCD as LCD
from time import sleep
import Image
import ImageDraw
import ImageFont
from Sensors import PCF8563
class Attendance:
	def __init__(self):
		self.LCD_DC = 5
		self.LCD_BL = 6
		self.LCD_RST = 22 
		self.time = '00:00:00'
		self.rtcSensor = PCF8563(1,0x51) 

	
	def database_setup(self):
		self.db=MySQLdb.connect("localhost","vc", "vc","attendance")
		self.cursor= self.db.cursor()
		return self.cursor

	def displayTime(self):
		self.font = ImageFont.truetype('PTS75F.ttf', 16)
		self.font8 = ImageFont.truetype('Lady Radical.ttf',8)
		self.draw.text((25,0),'Time',font=self.font)
		self.time = '{:2d}'.format(self.rtcSensor._read_year()) +":"+ '{:2d}'.format(self.rtcSensor._read_month())+":"+ '{:2d}'.format(self.rtcSensor._read_date())
		#self.time = '{:2d}'.format(self.rtcSensor._read_hours()) +":"+ '{:2d}'.format(self.rtcSensor._read_minutes())+":"+ '{:2d}'.format(self.rtcSensor._read_seconds())
		print self.time
		self.draw.text((20,20),self.time,font=self.font)
		self.Display.image(self.image)
		self.Display.display()

	def beginLCD(self):		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.LCD_BL,GPIO.OUT)
		GPIO.output(self.LCD_BL,GPIO.HIGH)
		self.Display = LCD.PCD8544(self.LCD_DC,self.LCD_RST, spi=SPI.SpiDev(0,0,max_speed_hz=4000000))
		self.Display.begin(contrast=60)
		self.Display.clear()
		self.Display.display()
	
	def clearImage(self):
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255,fill=255)
		self.Display.image(self.image)
		self.Display.display()		

	def welcomeMessage(self):
		self.Display.clear()
		self.image =  Image.new('1',(LCD.LCDWIDTH,LCD.LCDHEIGHT))
		self.draw = ImageDraw.Draw(self.image)
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255, fill = 255)
		self.font = ImageFont.truetype('PTS75F.ttf', 16)
		self.font8 = ImageFont.truetype('Lady Radical.ttf',8)
		self.draw.text((6,2),'Namaste!',font=self.font)
		self.Display.image(self.image)
		self.Display.display()
		sleep(2)
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255, fill = 255)
		self.draw.text((6,2),'Welcome to',font=self.font)
		self.Display.image(self.image)
		self.Display.display()
		sleep(2)
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255, fill = 255)
		self.draw.text((6,2),'Attendance',font=self.font)
		self.draw.text((6,27),'Tracker',font=self.font)
		self.Display.image(self.image)
		self.Display.display() 
		sleep(2)

	def display_name(self,name):
		self.Display.clear()
		self.image =  Image.new('1',(LCD.LCDWIDTH,LCD.LCDHEIGHT))
		self.draw = ImageDraw.Draw(self.image)
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255, fill = 255)
		self.font = ImageFont.truetype('PTS75F.ttf', 16)
		self.font8 = ImageFont.truetype('Lady Radical.ttf',8)
		self.draw.text((6,2),name,font=self.font)
		self.Display.image(self.image)
		self.Display.display()
		
if __name__ =='__main__':
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4, GPIO.OUT)
	GPIO.output(4,GPIO.LOW)

	present=17
	absent=26
	GPIO.setup(present, GPIO.IN)
	GPIO.setup(absent, GPIO.IN)
	device=Attendance()
	cursor=device.database_setup()
	device.beginLCD()
	#device.clearImage()
	device.welcomeMessage()
	sleep(2)
	device.displayTime()
	device.clearImage()
	sleep(1)
	date="""Feb1 """ #here call the rtc function
	#sql1=""" Alter table EC3 add """ + date + """ varchar(10);"""
	#cursor.execute(sql1)
	sql2=""" select* from EC3 ; """
	cursor.execute(sql2)
	data=cursor.fetchall()
	for row in data:
		name = row[0]
		disp_name=name
		name= """'""" + name + """'"""
		print name
		device.display_name(disp_name)
		while(GPIO.input(present)^GPIO.input(absent)==0):
			sleep(0.001)
		
		if(GPIO.input(present)==False):
			sleep(0.01)
			if(GPIO.input(present)==False):
				sql3 = """Update EC3 set """ + date + """='P'""" + """where name="""+name+""";"""
				cursor.execute(sql3)
				device.db.commit()
		if(GPIO.input(absent)==False):
			sleep(0.01)
			if(GPIO.input(absent)==False):
				sql3 = """Update EC3 set """ + date + """='A'""" + """where name="""+name+""";"""
				print sql3
				cursor.execute(sql3)
				device.db.commit()
		sleep(0.3)



	device.clearImage()
	device.db.close()









