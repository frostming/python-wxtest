#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =========================================
# Snake game
# @Author: Frost Ming
# @Email: mianghong@gmail.com
# @Date: 2016/3/13
# ==========================================
import wx
import os
import random


class GameFrame(wx.Frame):
    def __init__(self, title, size):
        super(GameFrame, self).__init__(None, -1, title,
                                        style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.width = size[0]
        self.height = size[1]
        self.snake = []
        self.cookie = None
        self.direction = wx.WXK_RIGHT
        self.timer = wx.Timer(self)
        w = self.width * 25 + 65
        h = self.height * 25 + 125
        self.initBuffer()
        panel = wx.Panel(self)
        panel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        panel.SetFocus()
        self.initGame()
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.SetClientSize((w, h))
        self.SetIcon(wx.Icon("snake.ico", wx.BITMAP_TYPE_ICO))
        self.Center()
        self.Show()

    def initBuffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)

    def onPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def onSize(self, evt):
        self.initBuffer()
        self.drawAll()

    def onClose(self, evt):
        with open('bestscore.ini', 'w') as fp:
            fp.write(str(self.bestscore))
        self.timer.Stop()
        self.Destroy()

    def initGame(self):
        self.score = 0
        if os.path.exists('bestscore.ini'):
            self.bestscore = int(open('bestscore.ini').read().strip())
        else:
            self.bestscore = 0
        self.snake = [(i, 0) for i in range(5)]
        self.newCookie()
        self.direction = wx.WXK_RIGHT
        self.timer.Start(300)

    def newCookie(self):
        x, y = random.choice(
                [(i, j) for i in range(self.width) for j in range(self.height) if (i, j) not in self.snake])
        self.cookie = (x, y)

    def drawAll(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.drawBg(dc)
        self.drawLabel(dc)
        self.drawField(dc)

    def drawBg(self, dc):
        w, h = self.GetClientSize()
        dc.SetBackground(wx.Brush(wx.WHITE))
        dc.Clear()
        dc.SetBrush(wx.Brush((154, 154, 154)))
        dc.SetPen(wx.Pen((154, 154, 154)))
        dc.DrawRoundedRectangle(15, 45, w - 30, h - 90, 5)
        dc.SetBrush(wx.Brush(wx.WHITE))
        dc.SetPen(wx.Pen(wx.WHITE))
        dc.DrawRoundedRectangle(30, 60, w - 60, h - 120, 3)

    def drawField(self, dc):
        for i in range(len(self.snake) - 1):
            x, y = self.snake[i]
            x1, y1 = self.snake[i + 1]
            dc.SetBrush(wx.Brush(wx.BLACK))
            dc.SetPen(wx.Pen(wx.BLACK))
            dc.DrawRectangle(35 + x * 25, 65 + y * 25, 20, 20)
            dc.SetBrush(wx.Brush(wx.RED))
            if y == y1:
                dc.DrawRectangle(55 + min(x, x1) * 25, 65 + y * 25, 5, 20)
            if x == x1:
                dc.DrawRectangle(35 + x * 25, 85 + min(y, y1) * 25, 20, 5)
        dc.SetBrush(wx.Brush(wx.BLACK))
        dc.DrawRectangle(35 + self.snake[-1][0] * 25, 65 + self.snake[-1][1] * 25, 20, 20)
        dc.SetBrush(wx.Brush((255, 157, 0)))
        dc.DrawCircle(45 + self.cookie[0] * 25, 75 + self.cookie[1] * 25, 15)

    def drawLabel(self, dc):
        dc.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL, face=u'Arial'))
        dc.SetTextForeground((154, 154, 154))
        dc.DrawText(u'Score: %d' % self.score, 20, 15)
        text_width = dc.GetTextExtent(u'Best Score: %d' % self.bestscore)[0]
        w, h = self.GetClientSize()
        dc.DrawText(u'Best Score: %d' % self.bestscore, w - 15 - text_width, 15)
        text_width = dc.GetTextExtent(u'Press SPACE to pause the game.')[0]
        dc.DrawText(u'Press SPACE to pause the game.', w / 2 - text_width / 2, h - 40)

    def doMove(self):
        headx, heady = self.snake[-1]
        new_block = None
        if self.direction == wx.WXK_RIGHT:
            new_block = (headx + 1, heady)
        elif self.direction == wx.WXK_LEFT:
            new_block = (headx - 1, heady)
        elif self.direction == wx.WXK_UP:
            new_block = (headx, heady - 1)
        elif self.direction == wx.WXK_DOWN:
            new_block = (headx, heady + 1)
        self.snake.append(new_block)
        if self.cookie == new_block:
            self.score += 10
            self.newCookie()
        else:
            self.snake.pop(0)
        if self.isGameOver():
            self.timer.Stop()
            if self.score > self.bestscore:
                self.bestscore = self.score
            if wx.MessageBox(u"GAME OVER, restart?", u"Oops!",
                             wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                best = self.bestscore
                self.initGame()
                self.bestscore = best
        if self.isWin():
            self.timer.Stop()
            if self.score > self.bestscore:
                self.bestscore = self.score
            if wx.MessageBox(u"YOU WIN!, restart?", u"Congratulations!",
                             wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                best = self.bestscore
                self.initGame()
                self.bestscore = best
        self.drawAll()

    def isGameOver(self):
        return any(item == self.snake[-1] for item in self.snake[:-5]) or self.snake[-1][0] not in range(self.width) or \
               self.snake[-1][1] not in range(self.height)

    def isWin(self):
        return len(self.snake) == self.width * self.height and all(
                (i, j) in self.snake for i in range(self.width) for j in range(self.height))

    def onKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == self.direction or keycode == self.direction +2 or keycode == self.direction - 2:
            return
        if keycode == wx.WXK_SPACE:
            if self.timer.IsRunning():
                self.timer.Stop()
            else:
                self.timer.Start(300)
            return
        self.direction = keycode
        self.timer.Stop()
        self.doMove()
        self.timer.Start(300)

    def onTimer(self, evt):
        self.doMove()

if __name__ == "__main__":
    app = wx.App(False)
    GameFrame(u"Snake v0.1 by Frost Ming", (10, 15))
    app.MainLoop()
