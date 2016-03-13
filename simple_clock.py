#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================
# A simple clock implemented by wxPython
# @Author: Frost Ming
# @Email: mianghong@gmail.com
# @Date: 2016/3/12
# =============================================
import wx
import time
import wx.animate
from math import sin, cos, pi


class Frame(wx.Frame):
    def __init__(self, title):
        super(Frame, self).__init__(None, -1, title,
                                    style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.buffer = None
        self.hour, self.min, self.sec = 0, 0, 0
        self.timer = wx.Timer(self)
        self.initBuffer()
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetClientSize((480, 480))
        self.initTime()
        self.timer.Start(1000)
        self.drawAll()
        self.Center()
        self.Show()

    @staticmethod
    def get_circle_coord(radius, angle):
        return 240 + int(radius * sin(angle * pi / 180)), 240 - int(radius * cos(angle * pi / 180))

    def onPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def onClose(self, evt):
        self.timer.Stop()
        self.Destroy()

    def initBuffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)

    def onSize(self, evt):
        self.initBuffer()
        self.drawAll()

    def initTime(self):
        cur_time = time.localtime()
        self.hour = cur_time.tm_hour
        self.min = cur_time.tm_min
        self.sec = cur_time.tm_sec

    def drawAll(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBackground(wx.Brush((255, 255, 255)))
        dc.Clear()
        self.drawPlate(dc)
        self.drawPointer(dc)

    def drawPlate(self, dc):
        def get_num_coord(num):
            w, h = dc.GetTextExtent(str(num))
            radius = 160
            startx, starty = Frame.get_circle_coord(radius, 30 * num)
            startx -= w / 2
            starty -= h / 2
            return (startx, starty)

        dc.SetBrush(wx.Brush((53, 53, 53)))
        dc.SetPen(wx.Pen((53, 53, 53), 5))
        dc.DrawCircle(240, 240, 200)
        dc.SetBrush(wx.Brush((252, 242, 227)))
        dc.DrawCircle(240, 240, 190)
        dc.SetBrush(wx.Brush(wx.BLACK))
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawCircle(240, 240, 12)
        dc.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, face=u"Arial"))
        dc.SetTextForeground((61, 61, 61))
        dc.SetPen(wx.Pen((53, 53, 53), 5))
        for num in range(1, 13):
            dc.DrawLine(240 + int(180 * sin(pi * num / 6)), 240 - int(180 * cos(pi * num / 6)),
                        240 + int(190 * sin(pi * num / 6)), 240 - int(190 * cos(pi * num / 6)))
            dc.DrawText(str(num), *get_num_coord(num))

    def drawPointer(self, dc):
        dc.SetPen(wx.Pen(wx.BLACK, 12))
        # Hour pointer
        dc.DrawLine(240, 240,
                    240 + int(90 * sin(pi * self.hour / 6 + pi * self.min / 360)),
                    240 - int(90 * cos(pi * self.hour / 6 + pi * self.min / 360)))
        # Minute pointer
        dc.DrawLine(240, 240,
                    240 + int(140 * sin(pi * self.min / 30)), 240 - int(140 * cos(pi * self.min / 30)))
        # Second pointer
        dc.SetPen(wx.Pen((186, 0, 0), 6))
        dc.SetBrush(wx.Brush((186, 0, 0)))
        dc.DrawCircle(240, 240, 5)
        dc.DrawLine(240, 240,
                    240 + int(150 * sin(pi * self.sec / 30)), 240 - int(150 * cos(pi * self.sec / 30)))

    def onTimer(self, evt):
        self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
        if self.min == 60:
            self.min = 0
            self.hour += 1
        self.drawAll()
        if self.min == 0:
            self.alarm()

    def alarm(self):
        dlg = ImgDialog(self, 'bird.gif', 'bugu.wav')
        dlg.SetFocus()
        dlg.Show()
        dlg.activate()


class ImgDialog(wx.Dialog):
    def __init__(self, parent, image, sound=None):
        img = wx.Image(image, wx.BITMAP_TYPE_GIF)
        w, h = img.GetSize()
        super(ImgDialog, self).__init__(parent, -1, '', size=(w,h), style=wx.BORDER_NONE)
        self.SetBackgroundColour(wx.Colour(255, 255, 255, 0))
        gif = wx.animate.GIFAnimationCtrl(self, -1, image)
        gif.GetPlayer().UseBackgroundColour(True)

        gif.Bind(wx.EVT_LEFT_UP, self.onClick)
        self.gif = gif
        self.sound = wx.Sound(sound)

    def activate(self):
        self.gif.Play()
        self.sound.Play(wx.SOUND_LOOP | wx.SOUND_ASYNC)

    def onClick(self, evt):
        self.gif.Stop()
        self.sound.Stop()
        self.Close()


if __name__ == '__main__':
    app = wx.App(False)
    Frame(u'Simple Clock v0.1 by Frost Ming')
    app.MainLoop()
