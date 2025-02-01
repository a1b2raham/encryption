import curses
from curses import wrapper
import time
from cryptography.fernet import Fernet
import random, string
import pygame



pygame.mixer.init()
rerun=True

master=""

def start(stdscr):
    global master
    master=""
    stdscr.clear()
    master += inp(stdscr,"  Enter the master password: ",False)


def generate_key():
    key = Fernet.generate_key()
    return key

def get_key():
    with open("key.key","rb") as key_file:
        key = key_file.read()
    return key

fer=Fernet(get_key())

def add(stdscr):
    site = inp(stdscr,"Enter the site: ",False)
    username = inp(stdscr,"Enter the username: ",False)
    password = inp(stdscr,"Enter the password: ",False,show=False)
    passw = master + '+' + password
    with open("passwords.txt","a") as f:
        f.write(f"{site}|{username}|"+fer.encrypt(passw.encode()).decode()+"\n")
        f.close()
      

def view(stdscr):
    with open("passwords.txt","r") as f:
        for line in f.readlines():
            data = line.rstrip()
            if not data:
                continue
            site,username,password = data.split("|")
            password = fer.decrypt(password.encode()).decode()
            mas,passw = password.split("+")
            
            if mas == master:
                inp(stdscr,"Site: " + site + " |Username: " + username + " |Password: " +passw,False,True)
            else:
                f= Fernet(generate_key())
                temp=""
                for i in range(len(passw)):
                    temp+= random.choice(string.ascii_letters)
                inp(stdscr,"Site: " + site + " |Username: " + username + " |Password: " +temp,False,True)    


def main(stdscr):
    global rerun
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    start(stdscr)
    sound = pygame.mixer.Sound('playf.mp3')

    stdscr.clear()
    stdscr.addstr(1,20,"Welcome to Password Manager",curses.color_pair(1))
    stdscr.addstr(2,20,"(press q to skip animations)",curses.color_pair(1))
    stdscr.refresh()
    time.sleep(0.2)
    str= "  OPTIONS  1)add  2)view  :"

    inpu=inp(stdscr,str)
    if inpu == '1':
        add(stdscr)
    elif inpu == '2':
        view(stdscr)
    
    stdscr.addch(" ")
    stdscr.refresh()
    y,x = stdscr.getyx()
    
    x = 20
    stdscr.addstr(y+2,x,"Please Press enter key to execute again and press any other key to exit the program",curses.color_pair(1))
    stdscr.refresh()
    repeat=stdscr.getkey()
    if repeat == '\n':
        return
    else:
        stdscr.addstr(y+4,x,"Thanks for using the program",curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1.25)
        stdscr.clear()
        stdscr.refresh()
        rerun=False
        return
    
    
    

def inp(stdscr,sen,down=True,display=False,show=True):
    
    chk= False
    
    sound = pygame.mixer.Sound('playf.mp3')
    stdscr.addch(" ")
    stdscr.refresh()
    y,x = stdscr.getyx()
    
    x = 20
    
    y += 1# start from next line
    for i in sen:
        
        if i == ' ':
            if down:
                y += 1
                x=20
            else:
                x += 1
            continue
        stdscr.addch(y,x,i,curses.color_pair(1))
        stdscr.refresh()
        stdscr.nodelay(True)
        try:
            d= stdscr.getkey()
        except:
            d=None    
        
        if d == 'q':
            x += 1
            chk=True
            continue  
            
            
        if chk==False:
            sound.play()
            time.sleep(0.15)
        x += 1

    stdscr.nodelay(False)
    a= stdscr.getkey()
    if display:
        return
    
    b=[]
    while a != '\n':
        if a=='\b':
            if len(b) > 0:
                b.pop()
                x -= 1
                stdscr.addch(y,x," ",curses.color_pair(1))
                stdscr.move(y,x)
                stdscr.refresh()
                a = stdscr.getkey()
                continue
            else:
                a= stdscr.getkey()
                continue
        if show:
                stdscr.addch(y,x,a,curses.color_pair(1))
        else:
            stdscr.addch(y,x,"*",curses.color_pair(1))
        x += 1
        b.append(a)
        a= stdscr.getkey()
    if len(b) == 1:
        return b[0]
    b = "".join(b)
    return b

while rerun:
    wrapper(main)

        
    



