#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================
# Title:  A simple annotation tool for NLP
# Author: Frost Ming
# Email:  mianghong@gmail.com
# Date:   2016/3/13
# ====================================
import wx
import wx.richtext
import wx.grid
import wx.lib.buttons as buttons


class Frame(wx.Frame):
    def __init__(self, title):
        super(Frame, self).__init__(None, -1, title, size=(800, 600))
        self.SetMinSize((800, 600))
        self.keymap = {'a': 'ACTION', 'c': 'CONT', 'd': 'DATA', 'e': 'EDU', 'g': 'GEND',
                       'l': 'LOC', 'm': 'MISC', 'n': 'NAME', 'o': 'ORG', 'p': 'PRO',
                       'r': 'RACE', 't': 'TITLE', 'u': 'UNIV'}
        self.initUI()
        self.Center()
        self.Show()

    def initUI(self):
        self.SetBackgroundColour(wx.WHITE)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbox = wx.BoxSizer(wx.VERTICAL)
        rbox = wx.BoxSizer(wx.VERTICAL)
        fbox = wx.BoxSizer(wx.HORIZONTAL)
        self.filename = wx.StaticText(self, -1, 'File: ')
        fbox.Add(self.filename, 1, wx.ALL | wx.ALIGN_CENTRE, border=3)
        open_btn = wx.Button(self, wx.ID_OPEN)
        fbox.Add(open_btn, 0, wx.ALL, border=3)
        lbox.Add(fbox, 0, wx.EXPAND, 3)
        self.editor = wx.richtext.RichTextCtrl(self)
        self.editor.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.editor.SetEditable(False)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        lbox.Add(self.editor, 1, flag=wx.EXPAND | wx.ALL, border=3)
        self.Bind(wx.EVT_BUTTON, self.onOpen, open_btn)
        hbox.Add(lbox, 1, flag=wx.EXPAND | wx.ALL, border=3)
        rbox.Add(wx.StaticText(self, -1, 'Labels Shortcuts Map'), 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.grid = Grid(self, self.keymap)
        rbox.Add(self.grid, 1, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=3)
        bbox = wx.BoxSizer(wx.HORIZONTAL)
        for label in ['add', 'delete', 'apply', 'saveas']:
            bmp = wx.Bitmap('icons/%s.ico' % label)
            btn = buttons.GenBitmapButton(self, bitmap=bmp)
            btn.SetToolTipString(label.capitalize())
            self.Bind(wx.EVT_BUTTON, getattr(self, 'on'+label.capitalize()), btn)
            bbox.Add(btn, 0, wx.ALIGN_CENTER | wx.RIGHT, 3)
        rbox.Insert(1, bbox, 0, wx.EXPAND | wx.ALL, 3)
        hbox.Add(rbox, 0, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(hbox)

    def onOpen(self, evt):
        filedlg = wx.FileDialog(self, wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*")
        if filedlg.ShowModal() == wx.ID_OK:
            self.filepath = filedlg.GetPath()
            self.filename.SetLabel('File: ' + self.filepath)
            content = open(self.filepath).read()
            self.editor.SetValue(content)
            self.editor.SetFocus()

    def onAdd(self, evt):
        self.grid.AppendRows(updateLabels=False)

    def onDelete(self, evt):
        while len(self.grid.GetSelectionBlockTopLeft()) > 0:
            uprow = self.grid.GetSelectionBlockTopLeft()[0][0]
            self.grid.DeleteRows(uprow)
        self.grid.ClearSelection()

    def onApply(self, evt):
        key_dict = dict()
        for row in range(self.grid.GetNumberRows()):
            key = self.grid.GetCellValue(row, 0)
            label = self.grid.GetCellValue(row, 1)
            if len(key) > 0 and len(label) > 0:
                key_dict[key] = label
            elif any([len(key) > 0, len(label)>0]):
                wx.MessageBox("Some rows are incomplete, please set them!", "Warning", wx.OK|wx.ICON_ERROR)
                return

        self.keymap = key_dict

    def onSaveas(self, evt):
        pass

    def onKeyDown(self, evt):
        key_char = chr(evt.GetUniChar())
        print key_char
        if key_char.lower() in self.keymap:
            start, end = self.editor.GetSelection()
            if start == end:
                return
            self.editor.SetCaretPosition(start)
            evt.Skip()


class Grid(wx.grid.Grid):
    def __init__(self, parent, data):
        super(Grid, self).__init__(parent)
        self.SetRowLabelSize(0)
        self.SetDefaultRowSize(30)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetDefaultCellFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.CreateGrid(0, 2, self.wxGridSelectRows)
        self.EnableDragRowSize(False)
        self.SetColLabelValue(0, 'Key')
        self.SetColSize(0, 50)
        self.SetColLabelValue(1, 'Label')
        self.SetColSize(1, 120)
        row = 0
        for k, v in data.items():
            self.AppendRows()
            self.SetCellValue(row, 0, k)
            self.SetCellValue(row, 1, v)
            row += 1


if __name__ == '__main__':
    app = wx.App(False)
    Frame('Test')
    app.MainLoop()
