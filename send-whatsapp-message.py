import pywhatkit
import pyautogui
from tkinter import *



win = Tk()
screenwidth = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()



# Send a WhatsApp Message to a Contact at 12:24 PM
# pywhatkit.sendwhatmsg("+263775588770", "Hi, mama!", 17,15,32)
pywhatkit.sendwhatmsg("+26", "Hi, mama!", 17,15,32)
pyautogui.moveTo(screenwidth*0.694,screen_height*0.964)
pyautogui.click()
pyautogui.press('enter')

