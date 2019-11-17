#Import image comparison modules
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import cv2

import time

#Keyboard + mouse capture modules
from pynput import mouse
import keyboard

import mss
import mss.tools

import gamesense

import threading

#Create game instance
gs = gamesense.GameSense("OVERWATCH", "Overwatch")

#Register game on SSE3
gs.register_game(icon_color_id=gamesense.GS_ICON_BLUE)

#Register events on SSE3
gs.register_event("SHIFT_READY")
gs.register_event("E_READY")
gs.register_event("SPACE_READY")
gs.register_event("RIGHT_CLICK_READY")

#Screenshot avatar in bottom left
def screenshot():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 924, "left": 148, "width": 70, "height": 47}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

#Calculate MSE of given image and screenshot
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def checkImage(hero):
    def compare_images(imageA, imageB, title):
    	# compute the mean squared error and structural similarity
    	# index for the images
        m = mse(imageA, imageB)
        s = measure.compare_ssim(imageA, imageB)

        return m

    # load the images -- the original, the original + contrast,
    # and the original + photoshop
    original = cv2.imread("images/{}.png".format(hero))
    contrast = cv2.imread("sct-924x148_70x47.png")
    shopped = cv2.imread("images/wreckingball.png")

    # convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)

    # initialize the figure
    fig = plt.figure("Images")
    images = ("Original", original), ("Contrast", contrast), ("Photoshopped", shopped)

    # loop over the images
    for (i, (name, image)) in enumerate(images):
    	# show the image
    	ax = fig.add_subplot(1, 3, i + 1)
    	ax.set_title(name)
    	plt.imshow(image, cmap = plt.cm.gray)
    	plt.axis("off")

    # compare the images
    return compare_images(original, contrast, "Original vs. Contrast")

class overwatchHero:
    def __init__(self,name,shiftCooldown,eCooldown,spaceCooldown,rightClickCooldown):
        self.name = name
        self.shiftCooldown = shiftCooldown
        self.eCooldown = eCooldown
        self.spaceCooldown = spaceCooldown
        self.rightClickCooldown = rightClickCooldown



anaHero = overwatchHero('ana',13.0,11.0,0.0,0.0)
asheHero = overwatchHero('ashe',11.0,11.0,0.0,0.0)
bastionHero = overwatchHero('bastion',0.0,0.0,0.0,0.0)
brigitteHero = overwatchHero('brigitte',5.0,6.0,0.0,7.0)


global currentHero
global heros

heros = {'ana': anaHero,'ashe':asheHero,'bastion':bastionHero}
""",'brigitte':brigitteHero,'doomfist':doomfistHero,'dva':dvaHero,'genji':genjiHero,'hanzo':hanzoHero,'junkrat':junkratHero,'lucio':lucioHero,'mccree':mccreeHero,'mei':meiHero,'mercy':mercyHero,'moira':moiraHero,'orisa':orisaHero,'pharah':pharahHero,'reaper':reaperHero,'reinhardt':reinhardtHero,'roadhog':roadhogHero,'sigma':sigmaHero,'soldier76':soldier76Hero,'sombra':sombraHero,'symmetra':symmetraHero,'torbjorn':torbjornHero,'tracer':tracerHero,'widowmaker':widowmakerHero,'winston':winstonHero,'wreckingBall':wreckingBallHero,'zarya':zaryaHero,'zenyatta':zenyattaHero}"""

"""
global leftClickActive
global rightClickActive

def on_click(x, y, button, pressed):
    global rightClickActive
    global leftClickActive

    if pressed:
        if button == mouse.Button.left:
            leftClickActive = True

        elif button == mouse.Button.right:
            rightClickActive = True

    if not pressed:
        if button == mouse.Button.left:
            leftClickActive = False

        elif button == mouse.Button.right:
            rightClickActive = False

    time.sleep(0.01)

"""

def heroCheckLoop():
    global currentHero
    global heros
    while True:
        screenshot()
        for i in heros:
            if checkImage(i) < 1000:
                currentHero = i

        time.sleep(1)

def shiftCooldown():
    global currentHero
    global heros

    while True:
        try:
            if keyboard.is_pressed('shift'):
                print('Shift')
                currentHeroObject = heros[currentHero]
                print(currentHeroObject.shiftCooldown)
                time.sleep(currentHeroObject.shiftCooldown)
                print('Cooldown over')
                gs.send_event('SHIFT_READY',{'value':22})
            else:
                pass

        except:
            pass

def eCooldown():
    global currentHero
    global heros

    while True:
        try:
            if keyboard.is_pressed('e'):
                currentHeroObject = heros[currentHero]
                if currentHeroObject.eCooldown != 0:
                    time.sleep(currentHeroObject.eCooldown)
                    print('Cooldown over')
                    gs.send_event('E_READY',{'value':22})
            else:
                pass

        except:

            pass

"""def brigitteBashCheck():
    global currentHero
    global heros
    global rightClickActive
    global leftClickActive

    while True:
        try:
            if currentHero == 'brigitte':
                if rightClickActive:
                    if leftClickActive:
                        print('Stun')
                        time.sleep(7)
                        gs.send_event('RIGHT_CLICK_READY',{'value':22})

        except Exception as e:
            pass"""

heroCheckThread = threading.Thread(target=heroCheckLoop)
heroCheckThread.start()

shiftCooldownThread = threading.Thread(target=shiftCooldown)
shiftCooldownThread.start()

eCooldownThread = threading.Thread(target=eCooldown)
eCooldownThread.start()

"""def mouseCheck():
    #with mouse.Listener(on_click=on_click) as listener:
    #    listener.join()

    listener = mouse.Listener(on_click=on_click)

    listener.start()



mouseCheckLoop = threading.Thread(target=mouseCheck)
mouseCheckLoop.start()"""

#brigitteBashCheckLoop = threading.Thread(target=brigitteBashCheck)
#brigitteBashCheckLoop.start()
