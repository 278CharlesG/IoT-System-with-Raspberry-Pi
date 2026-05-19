from RPLCD.i2c import CharLCD
import time
lcd = CharLCD ('PCF8574',0x27)

p1= ( #0,6,9,8,5,LT
  0b00111,
  0B01111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111
 )
 
p2=(#8,9,6,3,MT
  0B11111,
  0B11111,
  0B11111,
  0B00000,
  0B00000,
  0B00000,
  0B11111,
  0B11111
)

p3= (#8,9,3,2,RT
  0b11100,
  0B11110,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111
 )
 
p4=(#8,9,6,5,2,3 MB
  0B11111,
  0B11111,
  0B00000,
  0B00000,
  0B00000,
  0B11111,
  0B11111,
  0B11111
)

p5= (#8,6,2,LB
  0b11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B01111,
  0B00111
 )
 
p6=(#8,9,6,5,3,RB
  0b11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11111,
  0B11110,
  0B11100
)
p7=(#0,7,MT
  0B11111,
  0B11111,
  0B11111,
  0B00000,
  0B00000,
  0B00000,
  0B00000,
  0B00000
)
p8=(#0,MB
  0B00000,
  0B00000,
  0B00000,
  0B00000,
  0B00000,
  0B11111,
  0B11111,
  0B11111
)



lcd.create_char(0,p1)
lcd.create_char(1,p2)
lcd.create_char(2,p3)
lcd.create_char(3,p4)
lcd.create_char(4,p5)
lcd.create_char(5,p6)
lcd.create_char(6,p7)
lcd.create_char(7,p8)


def time_convert(sec):
    mins=sec//60
    sec=sec%60
    hours=mins//60
    hours=(hours+8)%24
    mins=mins%60
    return ("{:02}{:02}{:02}".format(int(hours),int(mins),int(sec)))
    
def check_num(c,side):
    global lcd
    if c=='0' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x06')
        lcd.write_string('\x02')
    if c=='0' and side==1:
        lcd.write_string('\x04')
        lcd.write_string('\x07')
        lcd.write_string('\x05')
    if c=='1' and side==0:
        lcd.write_string(' ')
        lcd.write_string(' ')
        lcd.write_string('\x02')
    if c=='1' and side==1:
        lcd.write_string(' ')
        lcd.write_string(' ')
        lcd.write_string('\x05')
    if c=='2' and side==0:
        lcd.write_string('\x01')
        lcd.write_string('\x01')
        lcd.write_string('\x02')
    if c=='2' and side==1:
        lcd.write_string('\x04')
        lcd.write_string('\x03')
        lcd.write_string('\x03')
    if c=='3' and side==0:
        lcd.write_string('\x01')
        lcd.write_string('\x01')
        lcd.write_string('\x02')
    if c=='3' and side==1:
        lcd.write_string('\x03')
        lcd.write_string('\x03')
        lcd.write_string('\x05')
    if c=='4' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x07')
        lcd.write_string('\x02')
    if c=='4' and side==1:
        lcd.write_string(' ')
        lcd.write_string(' ')
        lcd.write_string('\x05')
    if c=='5' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x01')
        lcd.write_string('\x01')
    if c=='5' and side==1:
        lcd.write_string('\x03')
        lcd.write_string('\x03')
        lcd.write_string('\x05')
    if c=='6' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x01')
        lcd.write_string('\x01')
    if c=='6' and side==1:
        lcd.write_string('\x04')
        lcd.write_string('\x03')
        lcd.write_string('\x05')
    if c=='7' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x06')
        lcd.write_string('\x02')
    if c=='7' and side==1:
        lcd.write_string(' ')
        lcd.write_string(' ')
        lcd.write_string('\x05')
    if c=='8' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x01')
        lcd.write_string('\x02')
    if c=='8' and side==1:
        lcd.write_string('\x04')
        lcd.write_string('\x03')
        lcd.write_string('\x05')
    if c=='9' and side==0:
        lcd.write_string('\x00')
        lcd.write_string('\x01')
        lcd.write_string('\x02')
    if c=='9' and side==1:
        lcd.write_string('\x03')
        lcd.write_string('\x03')
flag=False

while True:
    flag= not flag
    t=time.time()
    t=time_convert(t)
    for i in range(2):
        lcd.cursor_pos=(0,i*3)
        check_num(t[i],0)
        lcd.cursor_pos=(1,i*3)
        check_num(t[i],1)
    
    for i in range(2,4):
        lcd.cursor_pos=(0,i*3+1)
        check_num(t[i],0)
        lcd.cursor_pos=(1,i*3+1)
        check_num(t[i],1)
        
    lcd.cursor_pos=(1,14)
    lcd.write_string('{}'.format(t[4]))
    lcd.cursor_pos=(1,15)
    lcd.write_string('{}'.format(t[5]))
    
    if flag:
        lcd.cursor_pos=(0,6)
        lcd.write_string('.')
        lcd.cursor_pos=(1,6)
        lcd.write_string('.')
        lcd.cursor_pos=(1,13)
        lcd.write_string(':')
        lcd.cursor_pos=(0,14)
        lcd.write_string('\x00')
        lcd.cursor_pos=(0,15)
        lcd.write_string('\x02')
        
    time.sleep(0.98)
    lcd.clear()

    
