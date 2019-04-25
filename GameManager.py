import pyautogui
import random
import turtle
import pygame
import os
import math
from random import randint, uniform
import time
import sys
import win32gui, win32con, win32api


class GameManager(object):
    def __init__(self, rect, hwnd):
        self.gameRect = rect
        self.hwnd = hwnd
        self.hdc = win32gui.GetDC(0)
        self.state = None
        self.overlay = None
        self.ms = 0
        self.failed_to_work = 0
        # self.initialise_overlay()

    def check_for_image(self, image):
        screenshot = pyautogui.screenshot('RuneLiteSS.png', self.gameRect)
        return pyautogui.locate(image, screenshot)

    def check_state(self):
        location = self.check_for_image('img_templates/compass.png')

        if location is not None:
            return 'ingame'

        return 'login'

    def handle_login(self, password):
        stage_one = self.check_for_image('img_templates/existing-user-button.png')

        if stage_one is not None:
            self.move_cursor_somewhere_inside_box(stage_one)

        stage_two = self.check_for_image('img_templates/login.png')

        if stage_two is not None:
            pyautogui.typewrite(password, 0.2)
            self.move_cursor_somewhere_inside_box(stage_two)
            self.move_cursor_to(0, 0)
            time.sleep(3)

        stage_three = self.check_for_image('img_templates/click-here-to-play.png')

        if stage_three is not None:
            self.move_cursor_somewhere_inside_box(stage_three)
            time.sleep(2)

    def handle(self):
        if self.failed_to_work > 4:
            print('Failed to find alch spot more than 4 times, presuming were out of alchs and stopping')
            sys.exit()

        chance = random.randint(1, 10)

        if chance == 1:
            movement = random.randint(1, 4)
            if movement == 1:
                self.move_cursor_to(self.gameRect[0], self.gameRect[1]-600)
            if movement == 2:
                self.move_cursor_to(self.gameRect[0]+400, self.gameRect[1]-200)
            if movement == 3:
                self.move_cursor_to(self.gameRect[0]-self.gameRect[2], self.gameRect[1] + self.gameRect[3])
            if movement == 4:
                self.move_cursor_to(self.gameRect[0], self.gameRect[1] + self.gameRect[3])
            time.sleep(random.randint(1, 2))

        if chance == 2:
            time.sleep(random.randint(2, 10))

        alch = self.check_for_image('img_templates/alch.png')

        if alch is not None:
            if random.randint(0, 4) == 1:
                self.move_cursor_somewhere_inside_box(alch)
                time.sleep(0.250)
                self.move_cursor_somewhere_inside_box((alch[0], alch[1], 10, 10))
            else:
                self.move_cursor_to(alch[0], alch[1])
                time.sleep(0.250)
                self.move_cursor_to(alch[0], alch[1])
            return None
        time.sleep(1.250)

        spellbook = self.check_for_image('img_templates/spellbook.png')

        if spellbook is not None:
            self.move_cursor_somewhere_inside_box(spellbook)
            return None

        canAlch = self.check_for_image('img_templates/low-alch.png')

        if canAlch is None:
            self.failed_to_work += 1

    def initialise_overlay(self):
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.gameRect[0], self.gameRect[1])
        # pygame.init()
        # size = width, height = self.gameRect[2], self.gameRect[3]
        # self.overlay = pygame.display.set_mode(size)
        # self.overlay.fill('white')
        # ReleaseDC(hdc,0)
        self.draw_box(0, 0, 100, 100)

    def set_rect(self, rect):
        self.gameRect = rect
        pass

    def find_and_click(self, image):
        screenshot = pyautogui.screenshot('RuneLiteSS.png', self.gameRect)
        box = pyautogui.locate(image, screenshot)

        if box is None:
            return None

        self.move_cursor_somewhere_inside_box(box)

    def mouse_travel_time(self, x2, y2):
        """Calculates cursor travel time in seconds per 240-270 pixels, based on a variable rate of movement"""
        rate = uniform(0.09, 0.15)
        x1, y1 = pyautogui.position()
        distance = math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2))

        return max(uniform(.08, .12), rate * (distance/randint(250, 270)))

    def move_cursor_somewhere_inside_box(self, box):
        x = box[0] + random.randint(0, box[2])
        y = box[1] + random.randint(0, box[3])
        self.move_cursor_to(x, y)

    def move_cursor_to(self, x, y):
        xx = self.gameRect[0] + x
        yy = self.gameRect[1] + y
        pyautogui.moveTo(xx, yy, self.mouse_travel_time(xx, yy), tween=pyautogui.easeInOutQuint)
        pyautogui.click(None, None, 1)

    # def draw_box(self, x, y, w, h):
# win32gui.SelectObject(self.hdc, win32gui.GetStockObject('DC_BRUSH'))
# win32gui.Color
# win32gui.CreatePen(1, 2, win32api.RGB(255, 0, 0))
# win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
# win32gui.Rectangle(self.hdc, 100, 100, 300, 300)
# ps = win32gui.BeginPaint(self.hdc)
#
# # Draw red circle
# br = win32gui.CreateSolidBrush(win32api.RGB(0, 255, 0))
# win32gui.SelectObject(self.hdc, br)
# win32gui.Rectangle(self.hdc, 150, 20, 300, 120)
# win32gui.EndPaint(self.hwnd, ps)
# win32gui.LineTo()
# x1 = int(x)
# y1 = int(y)
# x2 = int(w)
# y2 = int(h)
# x1c, y1c = win32gui.ScreenToClient(self.hwnd, (x1, y1))
# x2c, y2c = win32gui.ScreenToClient(self.hwnd, (x2, y2))
# win32gui.MoveToEx(hdc, x1c, y1c)
# win32gui.LineTo(hdc, x2c, y2c)
# win32gui.ReleaseDC(self.hwnd, hdc)
