"""
Written 2018.
Edited for clarity and shared for fun 05-31-2023.
Tested in windows since that's the only OS we have (so it may or may not work in others).

Note: this is a python recreation inspired by https://www.deviantart.com/childish-n/art/DDLC-Shimeji-Pack-718209813
Unfortunately it does not have the physics and some other functions (cloning, climbing) implemented and might be sliiightly less polished in comparison.

To use:
-For your own chibi, you need an equivalent set of chibi sprites made/edited to match the default ones provided (you can use like Gimp and simply replace each chibi frame with your own, or any other better ways to do this)
-The chibi has a menu which can run python scripts.
    -HOWEVER you need to make sure your python can actually run as program itself, otherwise it wont open
    -And for more customized scripts using different libraries, you need to make sure that the python opening chibi and scripts with these libraries are the same or else they wont run (in experience, issues were encountered before with this because we had many versions of python installed)
-Finally, you may need to pip install some missing libs, like "win32api" (and some others you will just be prompted to install if needed)
"""

import subprocess, os, json, random
import tkinter as tk
import PIL.Image, PIL.ImageTk, PIL.ImageFile

#This is for setting limits for where chibi can be on your screen, so it doesn't run away and disappear
from win32api import GetSystemMetrics
right_lim = GetSystemMetrics(0) - 64 #horizontal plane of your screen. This sets the chib limit to your entire horizontal plane minus 64 pixels from the right
left_lim = -5 #This sets the chib limit to your entire horizontal plane + 5 pixels from the left
down_lim = GetSystemMetrics(1) - 150 #vertical plane of your screen. This sets the chib limit to your entire vertical plane - 150 pixels from the bottom

#If you cannot install win32api for some reason, you can use the below but you will need to adjust your screen limits a little more manually
#right_lim = your screen's horizontal length - amount of pixels you desire
#left_lim = -amount of pixels you desire
#down_lim = your screen's vertical length - amount of pixels you desire

PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True

prepend = "/".join(os.path.abspath(__file__).split("\\")[:-1])
targfile = "sprites" #dir to your folder of sprites, edit it as needed

#N'SZLASCH
class Sprite(tk.Tk):
    """Initiates sprite"""
    def __init__(self, master = None):
        tk.Tk.__init__(self, master)

        #Window variables
        self.dirloc = os.path.join(prepend, targfile) + "/"
        self.geometry('+{x}+{y}'.format(x=random.randint(0, 1000),y=-998))
        self.overrideredirect(True)
        self.lift()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "grey")
        self.title('')
        #self.iconbitmap(default=self.dirloc + "transparent.ico") #Uncomment this if you have a custom icon for your chibi, shows up on toolbar
        self.toplevel = TestWin()

        #For movement and mouse
        self._offsetx, self._offsety = 0, 0
        self.draxi = []

        #Boolean values
        self.countered = False #Note: implemented to avoid random actions conflicting with each other, but never was able to fix it properly
        self.dragged = False
        self.executede = False
        self.fallin = True
        self.infamo = False
        self.left, self.right = True, False
        self.snugging = False
        self.statue = False
        self.walked = False
        self.execflow = True
        #self.debug = True #If set to True, debugger window opens at start if I recall correctly

        self.labelimage = None

        print("AH!") #Test

        #Sprites defined here- you have to map your own sprites to these names just make sure you have a valid one for each
        #Note: this code can likely be simplified...
        self.stande = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand.png"))]
        self.stander = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "standr.png"))]
        self.falle = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "aire.png"))]
        self.faller = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "airer.png"))]
        self.rightface = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "standr.png"))]
        self.leftface = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand.png"))]
        self.frames = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand_walk1.png")),
                       PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand_walk2.png")),
                       PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand_walk1.png")),
                       PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand.png"))]
        self.flipframes = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand_walk1r.png")),
                       PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand_walk2r.png")),
                       PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand_walk1r.png")),
                       PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "standr.png"))]
        self.hop = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_3.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "stand.png"))]
        self.hopflip = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_3r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "standr.png"))]
        self.vhop = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_3.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2.png")),
                    PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1.png"))]
        self.vhopflip = [PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_3r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_2r.png")),
                        PIL.ImageTk.PhotoImage(PIL.Image.open(self.dirloc + "jump_1r.png"))]

        #Starting sprite
        self.label = self.displaypic(self.dirloc + "chib3.png")

        #Mouse vars
        self.bind('<Button-1>', self.clickwin)
        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<ButtonRelease-1>', self.resetted)
        self.bind('<Button-2>', self.exito)
        self.bind('<Button-3>', self.meny)

        #Chibi menu
        self.popup = tk.Menu(self, tearoff = 0)
        self.popup2 = tk.Menu(self, tearoff = 0)
        self.popup3 = tk.Menu(self, tearoff = 0)

        self.popup.add_cascade(label = "Commands", menu = self.popup2)
        self.popup2.add_command(label = "MAIN", command = self.tempfunc) #Map to a function that you usually use often. This used to map to opening a compiled renpy project
        self.popup2.add_separator()
        self.popup2.add_command(label = "Priority", command = lambda: self.deploy(os.path.join(prepend, "scripts", "priority.py")))
        self.popup2.add_command(label = "Test tool", command = lambda: self.deploy(os.path.join(prepend, "scripts", "test_tool.py")))
        #custom scripts - these will map to some python scripts that you can launch via the chibi

        #these actions are for the chibi itself. Note: these may make the chibi go erratic if overused, never was able to fix it
        self.popup.add_separator()
        self.popup.add_cascade(label = "Actions", menu = self.popup3)
        self.popup3.add_command(label = "Chase Mouse", command = lambda: self.run_chib_func(self.chase_mouse(0, self.frames, self.flipframes)))
        self.popup3.add_command(label = "Crawl", command = lambda: self.run_chib_func(self.crawl(10, self.frames, self.flipframes)))
        self.popup3.add_command(label = "Face Mouse", command = lambda: self.run_chib_func(self.facemouse()))
        self.popup3.add_command(label = "Fast Walk", command = lambda: self.run_chib_func(self.fastwalkfunc()))
        self.popup3.add_command(label = "Hop", command = lambda: self.run_chib_func(self.hoppp()))
        self.popup3.add_command(label = "Run", command = lambda: self.run_chib_func(self.runfunc()))
        self.popup3.add_command(label = "Snug", command = lambda: self.run_chib_func(self.snug()))
        self.popup3.add_command(label = "Statue", command = lambda: self.run_chib_func(self.statua()))
        self.popup3.add_command(label = "Walk", command = lambda: self.run_chib_func(self.walkfunc()))
        self.popup3.add_command(label = "Watch Mouse", command = lambda: self.run_chib_func(self.facemouseintense()))
        #more may be added here

        self.popup.add_separator()
        self.popup.add_command(label = "Debugger", command = self.toplevel.winder)
        self.popup.add_command(label = "Dismiss", command = self.destroy)

        #Pack and start
        self.label.pack()
        self.initfall()


    #FUNCTIONS
    #Some random timers (excuse the lolrandom 2019 naming...)
    def lol(self): return random.randint(10000, 100000)

    def lowlol(self): return random.randint(100, 10000)

    def loworlol(self):
        chance = random.randint(1, 2)
        if chance == 1: return self.lol()
        else: return self.lowlol()

    #Temporary function, i.e. dummy functions that can be used for WIPs
    def tempfunc(self):
        """placeholder function"""
        self.toplevel.prnter("Function not implemented yet")

    #SPRITE FUNCTIONS
    def initfall(self):
        """generates random coordinates to fall from above, within boundaries of screen"""
        chance = random.randint(1, 2)
        if chance == 1: self.left, self.right = True, False
        else: self.left, self.right = False, True

        #Updating sprite location as it falls
        #self.after(2, self.geometry, '+{x}+{y}'.format(x=random.randint(0, 1000),y=-1000)) #fix top-left coordinate issue
        if self.left: self.update2(0, self.falle)
        elif self.right: self.update2(0, self.faller)
        self.draxi += [int(self.winfo_x())]

    def displaypic(self, path):
        """displays picture (works only in some instances)"""
        image = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
        label = tk.Label(self, image = image, bg = "grey")
        self.labelimage = label
        return label

    def displaypics(self, path):
        """displays picture (works only in some instances)"""
        image = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
        self.label.configure(image = image)
        self.labelimage = image

    def displaypica(self, frames):
        """displays picture or pictures from a list (working)"""
        frame = frames[0]
        self.label.configure(image=frame, bg = "grey")

    #RANDOM ACTION FUNCTIONS
    def randomact(self): #Note: may be somewhat buggy at times
        if self.statue:
            self.execflow = False
            self.walked = False
            self.toplevel.prnter("> standing...")
            if self.left: self.displaypics(self.dirloc + "chib3.png") #had a chance of randomly disappearing after snug
            elif self.right: self.displaypics(self.dirloc + "standr.png")
            self.executede = False
            self.after(self.lol(), self.randomact)
        else:
            if os.path.isfile("signal.txt"):
                 self.toplevel.prnter("> register0")
                 exit()
            #Code that's meant to prevent chibis from disappearing down the screen
            if self.winfo_y() > down_lim:
                self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=down_lim))

            if self.dragged: self.countered = True
            elif self.fallin or self.infamo: self.toplevel.prnter("randomact countered")
            elif not self.execflow:
                self.toplevel.prnter("not execflow")
                self.execflow = True
                self.toplevel.prnter("execflow set to true: initializing new loop")
                self.after(self.lol(), self.randomact)
            else:
                self.toplevel.prnter("executing randomact")
                self.executede = True
                chance = random.randint(1, 100)

                if chance < 10: #stand
                    self.walked = False
                    self.toplevel.prnter("> standing...")
                    if self.left: self.displaypics(self.dirloc + "chib3.png") #had a chance of randomly disappearing after snug
                    elif self.right: self.displaypics(self.dirloc + "standr.png")
                    self.executede = False
                    self.after(self.lol(), self.randomact)

                elif chance > 10 and chance < 35: #walk
                    if self.walked:
                        chance = self.lol()
                        if chance > 65000:
                            self.executede = False
                            self.walked = False
                            self.walkfunc()
                        else:
                            self.toplevel.prnter("it tried to walk...")
                            self.after(self.lol(), self.randomact) #self.after(0, self.updateflip, 0, self.flipframes) #pass
                    else:
                        self.executede = False
                        self.walkfunc()

                elif chance > 35 and chance < 45: #fast walk
                    self.executede = False
                    self.walked = False
                    self.fastwalkfunc()

                elif chance > 45 and chance < 50: #chase mouse
                    self.executede = False
                    self.walked = False
                    self.after(0, self.chase_mouse, 0, self.frames, self.flipframes)

                elif chance > 50 and chance < 55: #run
                    self.executede = False
                    self.walked = False
                    self.runfunc()

                elif chance > 55 and chance < 60: #hop
                    self.executede = False
                    self.walked = False
                    self.toplevel.prnter("> hopping...")
                    self.hoppp()

                elif chance > 60 and chance < 75: #face mouse
                    self.executede = False
                    self.walked = False
                    self.toplevel.prnter("> faced mouse...")
                    self.facemouse()

                elif chance > 75 and chance < 85: #watch mouse
                    self.executede = False
                    self.walked = False
                    self.toplevel.prnter("> watching mouse...")
                    self.facemouseintense()

                elif chance > 85 and chance < 90: #crawl
                    self.executede = False
                    self.walked = False
                    self.toplevel.prnter("> crawling...")
                    self.after(0, self.crawl, 10, self.frames, self.flipframes)

                else: #snug
                    self.executede = False
                    self.walked = False
                    self.toplevel.prnter("> hygge time!")
                    self.snug()

                self.toplevel.prnter("end of random session")

    #More actions
    def update(self, ind, piclist):
        """animates walking left"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("leftwalk countered")
            self.after(self.lol(), self.randomact)
        else:
            try: frame = piclist[ind]
            except:
                chance = self.lol()
                if chance < 12500:
                    self.walked = True
                    self.toplevel.prnter("ending leftwalk")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("leftwalking should be halted")
                    else:
                        self.toplevel.prnter("walking left")
                        self.after(0, self.update, 0, piclist)
            else:
                if self.executede: self.toplevel.prnter("leftwalking should be halted")
                else:
                    ind += 1
                    if self.winfo_x() < left_lim:
                        frame = piclist[3]
                        self.label.configure(image = frame)
                    else:
                        self.label.configure(image = frame)
                        self.toplevel.prnter(str(frame))
                        if str(frame) == "pyimage10":
                            self.toplevel.prnter("leftwalk pause")
                            self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=self.winfo_y()))
                        else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-3,y=self.winfo_y()))
                    if str(frame) == "pyimage10": self.after(310, self.update, ind, piclist)
                    else: self.after(40, self.update, ind, piclist)

    def updateflip(self, ind, piclist):
        """animates walking right"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("rightwalk countered")
            self.after(self.lol(), self.randomact)
        else:
            try: frame = piclist[ind]
            except:
                chance = self.lol()
                if chance < 12500:
                    self.walked = True
                    self.toplevel.prnter("ending rightwalk")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("rightwalking should be halted")
                    else:
                        self.toplevel.prnter("walking right")
                        self.after(0, self.updateflip, 0, piclist)
            else:
                if self.executede: self.toplevel.prnter("rightwalking should be halted")
                else:
                    ind += 1
                    if self.winfo_x() > right_lim:
                        frame = piclist[3]
                        self.label.configure(image = frame)
                    else:
                        self.label.configure(image = frame)
                        self.toplevel.prnter(str(frame))
                        if str(frame) == "pyimage14":
                            self.toplevel.prnter("rightwalk pause")
                            self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=self.winfo_y()))
                        else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+3,y=self.winfo_y()))
                    if str(frame) == "pyimage14": self.after(310, self.updateflip, ind, piclist)
                    else: self.after(40, self.updateflip, ind, piclist)

    def update2(self, ind, piclist): #FIX ANIMATION
        """animates initfall, where kani falls from above"""
        self.toplevel.prnter("falling")
        if self.dragged: self.countered = True
        else:
            if self.winfo_y() > down_lim:
                self.fallin = False
                self.toplevel.prnter("> landed at - x: " + str(self.winfo_x()) + ", y: " + str(self.winfo_y()))
                if self.left: self.displaypica(self.stande)
                elif self.right: self.displaypica(self.stander)
                self.execflow = True

                #uncomment for debugging
                self.after(self.loworlol(), self.randomact)

                #place debugging code here:
                #self.facemouseintense()
                #self.after(0, self.run_left, 0, self.frames)
                #self.after(0, self.run_right, 0, self.flipframes)
                #self.after(0, self.chase_mouse, 0, self.frames, self.flipframes)
                #self.after(0, self.crawl, 10, self.frames, self.flipframes)
                #self.after(0, self.snug)
                #self.after(0, self.update3, 0, self.hop)
                #self.after(0, self.update3, 0, self.hopflip)
            else:
                try: frame = piclist[ind]
                except: self.after(0, self.update2, 0, piclist)
                else:
                    ind += 1
                    self.label.configure(image = frame)
                    self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=self.winfo_y()+15))
                    self.after(10, self.update2, ind, piclist)

    def update3(self, ind, piclist):
        """animates hop"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("hopping countered")
            self.after(self.lol(), self.randomact)
        else:
            if self.infamo:
                self.toplevel.prnter("victory hops")
                try:
                    frame = piclist[ind]
                    ind += 1
                    self.label.configure(image = frame)
                    self.after(50, self.update3, ind, piclist)
                except:
                    self.toplevel.prnter("kanpai!")
                    chance = random.randint(1,2)
                    if chance == 1:
                        self.infamo = False
                        if self.left: self.displaypics(self.dirloc + "chib3.png")
                        elif self.right: self.displaypics(self.dirloc + "standr.png")
                        self.after(self.loworlol(), self.randomact)
                    else: self.after(50, self.update3, 0, piclist)
            else:
                try:
                    self.toplevel.prnter("> hopping")
                    frame = piclist[ind]
                    ind += 1
                    self.label.configure(image = frame)
                    self.after(50, self.update3, ind, piclist)
                except: self.after(self.loworlol(), self.randomact)

    def hoppp(self):
        """encapsulates hopping in a func"""
        if self.left: self.after(0, self.update3, 0, self.hop)
        else: self.after(0, self.update3, 0, self.hopflip)

    def walkfunc(self):
        """assists in executing walking function, depending on direction kani is facing"""
        self.toplevel.prnter("> walking...")
        chance = random.randint(1, 2)
        if chance == 1:
            if self.winfo_x() < left_lim:
                self.left, self.right = False, True
                self.after(0, self.updateflip, 0, self.flipframes)
            else:
                self.left, self.right = True, False
                self.after(0, self.update, 0, self.frames)
        elif chance == 2:
            if self.winfo_x() > right_lim:
                self.left, self.right = True, False
                self.after(0, self.update, 0, self.frames)
            else:
                self.left, self.right = False, True
                self.after(0, self.updateflip, 0, self.flipframes)


    def fastwalkfunc(self):
        """assists in executing fastwalking function, depending on direction kani is facing"""
        self.toplevel.prnter("> fastwalking...")
        chance = random.randint(1, 2)
        if chance == 1:
            if self.winfo_x() < left_lim:
                self.left, self.right = False, True
                self.after(0, self.fast_walk_right, 0, self.flipframes)
            else:
                self.left, self.right = True, False
                self.after(0, self.fast_walk_left, 0, self.frames)
        elif chance == 2:
            if self.winfo_x() > right_lim:
                self.left, self.right = True, False
                self.after(0, self.fast_walk_left, 0, self.frames)
            else:
                self.left, self.right = False, True
                self.after(0, self.fast_walk_right, 0, self.flipframes)

    def runfunc(self):
        """assists in executing running function, depending on direction kani is facing"""
        self.toplevel.prnter("> running!")
        chance = random.randint(1, 2)
        if chance == 1:
            if self.winfo_x() < left_lim:
                self.left, self.right = False, True
                self.after(0, self.run_right, 0, self.flipframes)
            else:
                self.left, self.right = True, False
                self.after(0, self.run_left, 0, self.frames)
        elif chance == 2:
            if self.winfo_x() > right_lim:
                self.left, self.right = True, False
                self.after(0, self.run_left, 0, self.frames)
            else:
                self.left, self.right = False, True
                self.after(0, self.run_right, 0, self.flipframes)

    def snug(self):
        """executes snug action"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("snug countered")
            self.after(self.lol(), self.randomact)
        else:
            self.snugging = True
            self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=self.winfo_y()+15))
            if self.right: self.displaypics(self.dirloc + "snugr.png")
            else: self.displaypics(self.dirloc + "snug.png")
            self.after(self.lol(), self.shortstan)

    def statua(self):
        """executes statue mode, where it freezes the chibi"""
        if self.statue:
            self.statue = False
            self.toplevel.prnter("statue off")
        else:
            self.statue = True
            self.toplevel.prnter("statue on")

    def shortstan(self):
        """post-snug assisting function that makes kani transition more smoothly to other acts"""
        if self.dragged:
            self.countered = True
            self.toplevel.prnter("shortstan drag-countered")
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("shortstan countered")
            self.after(self.lol(), self.randomact)
        else: #DEFINITELY TRACK HERE: IF POST SNUG EXECUTES AS A RANDOMACT DOES, THEN IT COULD CAUSE A CONFLICT
            if self.snugging:
                self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=self.winfo_y()-15))
                self.snugging = False
            if self.left: self.displaypics(self.dirloc + "chib3.png") #TRACK (had a chance of disappearing before)
            elif self.right: self.displaypics(self.dirloc + "standr.png")
            traque = random.randint(1, 10)
            self.toplevel.prnter("post-snug executed for " + str(traque) + " seconds")
            self.after(traque * 1000, self.randomact)

    def facemouse(self):
        """faces direction where mouse is at"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("facemouse countered")
            self.after(self.lol(), self.randomact)
        else:
            if self.winfo_pointerx() > self.winfo_x() + 64:
                self.displaypica(self.rightface)
                self.left, self.right = False, True
                self.toplevel.prnter("facing right")
            elif self.winfo_pointerx() < self.winfo_x() + 64:
                self.displaypica(self.leftface)
                self.left, self.right = True, False
                self.toplevel.prnter("facing left")
            else: self.toplevel.prnter("facing... middle???")

            self.after(random.randint(100, 10000), self.randomact)

    def facemouseintense(self):
        """tracks direction where mouse is at for a randomized duration"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("intense facemouse countered")
            self.after(self.lol(), self.randomact)
        else:
            self.infamo = True
            if self.infamo:
                if self.winfo_pointerx() > self.winfo_x() + 64:
                    self.displaypica(self.rightface)
                    self.left, self.right = False, True
                    self.toplevel.prnter("gazing right")
                elif self.winfo_pointerx() < self.winfo_x() + 64:
                    self.displaypica(self.leftface)
                    self.left, self.right = True, False
                    self.toplevel.prnter("gazing left")
                else: self.toplevel.prnter("facing middle!?")

                chance = self.lol()
                if chance < 15000:
                    self.infamo = False
                    self.after(random.randint(10, 10000), self.randomact)
                else: self.after(500, self.facemouseintense)

    def chase_mouse(self, ind, piclist, piclisttwo):
        """makes kani chase the mouse until coordinates meet"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("chase mouse left countered")
            self.after(self.lol(), self.randomact)
        else:
            self.infamo = True
            if self.infamo:

                #debug code below:
                #self.toplevel.prnter("coordinates: " + str(self.winfo_x()) + ", " + str(self.winfo_y()))

                if self.winfo_pointerx() > self.winfo_x() + 70:
                    self.displaypica(self.rightface)
                    self.left, self.right = False, True
                    try: frame = piclisttwo[ind]
                    except: self.after(0, self.chase_mouse, 0, piclist, piclisttwo)
                    else:
                        if self.executede: self.toplevel.prnter("chasing should be halted")
                        else:
                            ind += 1
                            self.label.configure(image = frame)
                            self.toplevel.prnter(str(frame))
                            if str(frame) == "pyimage14":
                                self.toplevel.prnter("rightchase pause")
                                self.geometry('+{x}+{y}'.format(x=self.winfo_x()+6,y=self.winfo_y()))
                            else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+9,y=self.winfo_y()))
                            if str(frame) == "pyimage14":
                                self.after(45, self.chase_mouse, ind, piclist, piclisttwo)
                            else:
                                self.after(30, self.chase_mouse, ind, piclist, piclisttwo)

                elif self.winfo_pointerx() < self.winfo_x() - 70:
                    self.left, self.right = True, False
                    try: frame = piclist[ind]
                    except: self.after(0, self.chase_mouse, 0, piclist, piclisttwo)
                    else:
                        if self.executede: self.toplevel.prnter("chasing should be halted")
                        else:
                            ind += 1
                            self.label.configure(image = frame)
                            self.toplevel.prnter(str(frame))
                            if str(frame) == "pyimage10":
                                self.toplevel.prnter("leftchase pause")
                                self.geometry('+{x}+{y}'.format(x=self.winfo_x()-6,y=self.winfo_y()))
                            else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-9,y=self.winfo_y()))
                            if str(frame) == "pyimage10":
                                self.after(45, self.chase_mouse, ind, piclist, piclisttwo)
                            else:
                                self.after(30, self.chase_mouse, ind, piclist, piclisttwo)

                else: #Chibi catches mouse too easily: see if you can make it a little more challenging?
                    self.toplevel.prnter("victory!")
                    if self.left: self.after(55, self.update3, 0, self.vhop)
                    else: self.after(55, self.update3, 0, self.vhopflip)

    def fast_walk_left(self, ind, piclist):
        """animates fastwalking left"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("fast leftwalk countered")
            self.after(self.lol(), self.randomact)
        else:
            try: frame = piclist[ind]
            except:
                chance = self.lol()
                if chance < 12500:
                    self.walked = True
                    self.toplevel.prnter("ending fast leftwalk")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("fast leftwalking should be halted")
                    else:
                        self.toplevel.prnter("fast walking left")
                        self.after(0, self.fast_walk_left, 0, piclist)
            else:
                if self.executede: self.toplevel.prnter("fast leftwalking should be halted")
                else:
                    ind += 1
                    if self.winfo_x() < left_lim:
                        frame = piclist[3]
                        self.label.configure(image = frame)
                    else:
                        self.label.configure(image = frame)
                        self.toplevel.prnter(str(frame))
                        if str(frame) == "pyimage10":
                            self.toplevel.prnter("fast leftwalk pause")
                            self.geometry('+{x}+{y}'.format(x=self.winfo_x()-3,y=self.winfo_y()))
                        else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-5,y=self.winfo_y()))
                    if str(frame) == "pyimage10": self.after(65, self.fast_walk_left, ind, piclist)
                    else: self.after(45, self.fast_walk_left, ind, piclist)

    def fast_walk_right(self, ind, piclist):
        """animates fastwalking right"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("fast rightwalk countered")
            self.after(self.lol(), self.randomact)
        else:
            try: frame = piclist[ind]
            except:
                chance = self.lol()
                if chance < 12500:
                    self.walked = True
                    self.toplevel.prnter("ending fast rightwalk")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("fast rightwalking should be halted")
                    else:
                        self.toplevel.prnter("fast walking right")
                        self.after(0, self.fast_walk_right, 0, piclist)
            else:
                if self.executede: self.toplevel.prnter("fast rightwalking should be halted")
                else:
                    ind += 1
                    if self.winfo_x() > right_lim:
                        frame = piclist[3]
                        self.label.configure(image = frame)
                    else:
                        self.label.configure(image = frame)
                        self.toplevel.prnter(str(frame))
                        if str(frame) == "pyimage14":
                            self.toplevel.prnter("fast rightwalk pause")
                            self.geometry('+{x}+{y}'.format(x=self.winfo_x()+3,y=self.winfo_y()))
                        else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+5,y=self.winfo_y()))
                    if str(frame) == "pyimage14": self.after(65, self.fast_walk_right, ind, piclist)
                    else: self.after(45, self.fast_walk_right, ind, piclist)

    def run_left(self, ind, piclist):
        """animates running left"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("left run countered")
            self.after(self.lol(), self.randomact)
        else:
            try: frame = piclist[ind]
            except:
                chance = self.lol()
                if chance < 12500:
                    self.walked = True
                    self.toplevel.prnter("ending left run")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("left running should be halted")
                    else:
                        self.toplevel.prnter("running left")
                        self.after(0, self.run_left, 0, piclist)
            else:
                if self.executede: self.toplevel.prnter("left running should be halted")
                else:
                    ind += 1
                    if self.winfo_x() < left_lim:
                        frame = piclist[3]
                        self.label.configure(image = frame)
                    else:
                        self.label.configure(image = frame)
                        self.toplevel.prnter(str(frame))
                        if str(frame) == "pyimage10":
                            self.toplevel.prnter("left run pause")
                            self.geometry('+{x}+{y}'.format(x=self.winfo_x()-6,y=self.winfo_y()))
                        else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-9,y=self.winfo_y()))
                    if str(frame) == "pyimage10": self.after(45, self.run_left, ind, piclist)
                    else: self.after(30, self.run_left, ind, piclist)

    def run_right(self, ind, piclist):
        """animates running right"""
        if self.dragged: self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("right run countered")
            self.after(self.lol(), self.randomact)
        else:
            try: frame = piclist[ind]
            except:
                chance = self.lol()
                if chance < 12500:
                    self.walked = True
                    self.toplevel.prnter("ending right run")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("right running should be halted")
                    else:
                        self.toplevel.prnter("running right")
                        self.after(0, self.run_right, 0, piclist)
            else:
                if self.executede: self.toplevel.prnter("right running should be halted")
                else:
                    ind += 1
                    if self.winfo_x() > right_lim:
                        frame = piclist[3]
                        self.label.configure(image = frame)
                    else:
                        self.label.configure(image = frame)
                        self.toplevel.prnter(str(frame))
                        if str(frame) == "pyimage14":
                            self.toplevel.prnter("right run pause")
                            self.geometry('+{x}+{y}'.format(x=self.winfo_x()+6,y=self.winfo_y()))
                        else: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+9,y=self.winfo_y()))
                    if str(frame) == "pyimage14": self.after(45, self.run_right, ind, piclist)
                    else: self.after(30, self.run_right, ind, piclist)

    def crawl(self, ind, piclist, piclisttwo):
        """animates crawling"""
        if self.dragged:
            self.countered = True
        elif self.executede:
            self.executede = True
            self.toplevel.prnter("crawl countered")
            self.after(self.lol(), self.randomact)
        else:
            ind -= 1
            if self.left: frame = piclist[3]
            elif self.right: frame = piclisttwo[3]
            self.label.configure(image = frame)
            if self.winfo_x() < left_lim or self.winfo_x() > right_lim:
                if self.lol() < 25000:
                    self.toplevel.prnter("ending crawl")
                    self.after(self.loworlol(), self.randomact)
                else:
                    if self.executede: self.toplevel.prnter("crawl should be halted")
                    else: self.toplevel.prnter("crawling")
                    self.after(1750, self.crawl, ind, piclist, piclisttwo)
            else:
                if ind == 9:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-0,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+0,y=self.winfo_y()))
                    self.after(79, self.crawl, ind, piclist, piclisttwo)
                elif ind == 8:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-1,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+1,y=self.winfo_y()))
                    self.after(75, self.crawl, ind, piclist, piclisttwo)
                elif ind == 7:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-2,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+2,y=self.winfo_y()))
                    self.after(71, self.crawl, ind, piclist, piclisttwo)
                elif ind == 6:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-3,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+3,y=self.winfo_y()))
                    self.after(69, self.crawl, ind, piclist, piclisttwo)
                elif ind == 5:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-4,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+4,y=self.winfo_y()))
                    self.after(67, self.crawl, ind, piclist, piclisttwo)
                elif ind == 4:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-5,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+5,y=self.winfo_y()))
                    self.after(65, self.crawl, ind, piclist, piclisttwo)
                elif ind == 3:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-3,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+3,y=self.winfo_y()))
                    self.after(69, self.crawl, ind, piclist, piclisttwo)
                elif ind == 2:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-2,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+2,y=self.winfo_y()))
                    self.after(73, self.crawl, ind, piclist, piclisttwo)
                elif ind == 1:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-1,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+1,y=self.winfo_y()))
                    self.after(79, self.crawl, ind, piclist, piclisttwo)
                else:
                    if self.left: self.geometry('+{x}+{y}'.format(x=self.winfo_x()-0,y=self.winfo_y()))
                    elif self.right: self.geometry('+{x}+{y}'.format(x=self.winfo_x()+0,y=self.winfo_y()))
                    ind = 10

                    if self.lol() < 20000:
                        self.toplevel.prnter("ending crawl")
                        self.after(self.loworlol(), self.randomact)
                    else:
                        if self.executede: self.toplevel.prnter("crawl should be halted")
                        else: self.toplevel.prnter("crawling")
                        self.after(1750, self.crawl, ind, piclist, piclisttwo)

    #Other functions
    def clickwin(self, event):
        """runs when kani is clicked"""
        self._offsetx = event.x
        self._offsety = event.y
        #if not self.movin:
            #self.displaypics(self.dirloc + "air.png")

    def dragwin(self, event):
        """runs when kani is dragged"""
        self.countered = True
        self.infamo = False
        self.fallin = False
        self.dragged = True
        x = self.winfo_pointerx() - 64 #- self._offsetx
        y = self.winfo_pointery() -15 #- self._offsety
        if self.snugging:
            self.geometry('+{x}+{y}'.format(x = x,y = y - 15))
            self.snugging = False
        else: self.geometry('+{x}+{y}'.format(x = x,y = y))

        self.draxi += [x]

        #if x is found to be increasing more than current x: display swing left
        if self.draxi[len(self.draxi) - 1] > self.draxi[len(self.draxi) - 2]:
            self.displaypics(self.dirloc + "air_swing_l.png")

        #if x is found to be decreasing more than current x: display swing right
        elif self.draxi[len(self.draxi) - 1] < self.draxi[len(self.draxi) - 2]:
            self.displaypics(self.dirloc + "air_swing_r.png")

        else: self.displaypics(self.dirloc + "air.png")

        #debug code below:
        #self.displaypics(self.dirloc + "air.png")
        #self.toplevel.prnter("x-y: " + str(self.winfo_pointerx()) + str(self.winfo_pointery()))

    def resetted(self, event):
        """runs after dragging event"""
        self.toplevel.prnter("resetted...")
        self.pickedup()

    def pickedup(self):
        """resets kani's behaviour after dragging event"""
        self.toplevel.prnter("> at pickedup")

        #below code can be improved, you think?
        if self.draxi[len(self.draxi) - 1] > self.draxi[len(self.draxi) - 2]:
            self.displaypics(self.dirloc + "standr.png")
            self.left, self.right = False, True

        elif self.draxi[len(self.draxi) - 1] < self.draxi[len(self.draxi) - 2]:
            self.displaypics(self.dirloc + "chib3.png")
            self.left, self.right = True, False
        else:
            self.displaypics(self.dirloc + "chib3.png")
            self.left, self.right = True, False

        #self.deiconify()

        if self.winfo_x() > right_lim:
            self.geometry('+{x}+{y}'.format(x=1304,y=self.winfo_y()))
        if self.winfo_x() < left_lim:
            self.geometry('+{x}+{y}'.format(x=-63,y=self.winfo_y()))
        if self.winfo_y() > down_lim:
            self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=down_lim))

        self.dragged = False
        self.execflow = True
        self.toplevel.prnter("> leaving pickedup")
        #TIMEMARK
        if self.countered:
            self.after(self.loworlol(), self.randomact) #TRACK: this bit of code was responsible for spawning redundant timers
            self.countered = False

    def meny(self, event):
        """menu that activates on right click"""
        try: self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally: self.popup.grab_release()

    def deploy(self, module):
        """deploys a module, specifically a python script"""
        #This code opens a cmd window
        # try: subprocess.Popen(["start", "cmd", "/c", "python36 " + module], shell=True)
        #This code opens a python window- it's here if you want to use this instead and edit as needed
        try: subprocess.call(["cmd.exe", "/c", "START", "python36", module])
        except Exception as e: self.toplevel.prnter("error: " + str(e))

    def run_chib_func(self, func):
        """executes func on command"""
        #Code that's meant to prevent chibis from disappearing down the screen
        if self.winfo_y() > down_lim:
            self.geometry('+{x}+{y}'.format(x=self.winfo_x(),y=down_lim))
        self.execflow = False
        func

    #Exit
    def exito(self, event): self.destroy()


#Logger and debugger window (WIP)
class TestWin(tk.Tk):
    def __init__(self, master = None):
        self.debug = False #True
        self.top = tk.Toplevel()
        self.top.title("Debugger")
        self.text = tk.Text(self.top, height=40, width=45)
        self.text.configure(background='black', fg='white')
        self.vscrollbar = tk.Scrollbar(self.top, orient="vertical", command=self.text.yview)
        #self.top.wm_geometry("500x500")
        self.vscrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        #top.overrideredirect(True)
        self.top.protocol("WM_DELETE_WINDOW", self.winder)
        self.top.withdraw()

    def winder(self):
        if self.debug:
            self.top.withdraw()
            self.debug = False
            #top.deiconify()
        else:
            self.top.deiconify()
            self.debug = True

    def prnter(self, txt):
        self.text.insert("end-1c", txt + "\n")
        self.text.see("end")


#MAIN
root = Sprite()
root.focus()
root.mainloop()
print("> SESSION ENDED")
exit()
