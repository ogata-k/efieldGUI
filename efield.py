# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 16:30:06 2017

@author: Owner
"""

import wx
import math
import matplotlib.pyplot as plt
import seaborn
import os


class NumValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Clone(self):
        return NumValidator()

    def Validate(self, win):
        txt = self.GetWindow()
        val = txt.GetValue()

        try:
            val = float(val)
        except:
            val = None
        #print(val, type(val))

        if not isinstance(val, float):
            txt.SetBackgroundColour("YELLOW")
            txt.SetFocus()
            txt.Refresh()
            #print(False)
            return False
        else:
            txt.SetBackgroundColour(wx.WHITE)
            txt.Refresh()
            return True


class ThreeItems(wx.Panel):
    def __init__(self, parent, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id=ID)
        layout = wx.BoxSizer(wx.HORIZONTAL)
        self.ID_TARGET_TEXT = ID

        gap = 10
        # X
        layout.Add(wx.StaticText(self, wx.ID_ANY, label="X"),
                   flag=wx.ALL | wx.ALIGN_CENTER, border=gap, proportion=1)
        self.X = wx.TextCtrl(self, self.ID_TARGET_TEXT,
                             validator=NumValidator(), style=wx.TE_RIGHT)
        self.X.SetMaxLength(6)
        layout.Add(self.X, flag=wx.RIGHT | wx.TOP | wx.BOTTOM, border=gap,
                   proportion=2)

        # Y
        layout.Add(wx.StaticText(self, wx.ID_ANY, label="Y"),
                   flag=wx.ALL | wx.ALIGN_CENTER, border=gap, proportion=1)
        self.Y = wx.TextCtrl(self, self.ID_TARGET_TEXT,
                             validator=NumValidator(), style=wx.TE_RIGHT)
        self.Y.SetMaxLength(6)
        layout.Add(self.Y, flag=wx.RIGHT | wx.TOP | wx.BOTTOM, border=gap,
                   proportion=2)

        # Q
        layout.Add(wx.StaticText(self, wx.ID_ANY, label="Q"),
                   flag=wx.ALL | wx.ALIGN_CENTER, border=gap, proportion=1)
        self.Q = wx.TextCtrl(self, self.ID_TARGET_TEXT,
                             validator=NumValidator(), style=wx.TE_RIGHT)
        self.Q.SetMaxLength(6)
        layout.Add(self.Q, flag=wx.RIGHT | wx.TOP | wx.BOTTOM, border=gap,
                   proportion=2)

        self.SetSizer(layout)

    def GetItems(self):
        if self.IsValidate():
            items = [self.X.GetValue(), self.Y.GetValue(), self.Q.GetValue()]
            return items
        else:
            return None

    def IsValidate(self):
        self.QVali = self.Q.Validator.Validate(self.Q)
        self.YVali = self.Y.Validator.Validate(self.Y)
        self.XVali = self.X.Validator.Validate(self.X)
        #print(self.XVali, self.YVali, self.QVali)
        return self.XVali and self.YVali and self.QVali

    def Clear(self):
        items = [self.X, self.Y, self.Q]
        for item in items:
            item.SetBackgroundColour(wx.WHITE)
            item.Clear()


class TopFrame(wx.Frame):
    def __init__(self, app):
        wx.Frame.__init__(self, None, size=(500, 500),
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |
                          wx.CLIP_CHILDREN)
        self.CreateStatusBar()
        self.SetTitle(u"固定電荷による電子の軌道")
        self.Center()
        app.SetTopWindow(self)

        panel = wx.Panel(self)
        baseLayout = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(baseLayout)

        elecTitle = wx.StaticBox(panel, label=u"電子の開始条件")
        elecLayout = wx.StaticBoxSizer(elecTitle, wx.VERTICAL)
        elecLayout.Add(wx.StaticText(panel, label=u"位置と電荷"))
        self.ID_ELEC = wx.NewId()
        TI1 = ThreeItems(panel, self.ID_ELEC)
        TI1.Q.SetValue("-1")
        TI1.Q.Disable()
        elecLayout.Add(TI1, flag=wx.EXPAND)
        elecLayout.Add(wx.StaticText(panel, label=u"速度"))
        self.ID_VEC = wx.NewId()
        TIVEC = ThreeItems(panel, self.ID_VEC)
        TIVEC.Q.SetValue("0")
        TIVEC.Q.Disable()
        elecLayout.Add(TIVEC, flag=wx.EXPAND)


        baseLayout.Add(elecLayout, flag=wx.EXPAND | wx.ALL, border=5)

        fixedTitle = wx.StaticBox(panel, label=u"固定電荷の条件")
        fixedLayout = wx.StaticBoxSizer(fixedTitle, wx.VERTICAL)
        self.ID_FIXED = wx.NewId()
        TI2 = ThreeItems(panel, self.ID_FIXED)
        fixedLayout.Add(TI2)
        btnLayout = wx.BoxSizer(wx.HORIZONTAL)
        fixedLayout.Add(btnLayout)

        addBtn = wx.Button(panel, label=u"追加")
        addBtn.Bind(wx.EVT_BUTTON, self.AddAction)
        btnLayout.Add(addBtn, flag=wx.LEFT | wx.RIGHT, border=5)

        delBtn = wx.Button(panel, label=u"削除")
        delBtn.Bind(wx.EVT_BUTTON, self.DelAction)
        btnLayout.Add(delBtn, flag=wx.LEFT | wx.RIGHT, border=5)

        self.ID_LB = wx.NewId()
        textBox = wx.ListBox(panel, self.ID_LB,
                               style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        fixedLayout.Add(textBox, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)

        baseLayout.Add(fixedLayout, flag=wx.EXPAND | wx.ALL, border=5, proportion=1)

        bottomLayout = wx.BoxSizer(wx.HORIZONTAL)
        baseLayout.Add(bottomLayout)
        simBtn = wx.Button(panel, label=u"シミュレート")
        simBtn.Bind(wx.EVT_BUTTON, self.SimulateAction)
        bottomLayout.Add(simBtn, flag=wx.LEFT | wx.RIGHT, border=5)

        resetBtn = wx.Button(panel, label=u"リセット")
        resetBtn.Bind(wx.EVT_BUTTON, self.ResetAction)
        bottomLayout.Add(resetBtn, flag=wx.LEFT | wx.RIGHT, border=5)

        self.Show()

    def GetAllItems(self):
        initItems = [self.ID_ELEC, self.ID_VEC, self.ID_LB]
        target = wx.FindWindowById(initItems[0])
        start_loc = target.GetItems()[0:2]
        start_loc = [float(i) for i in start_loc]
        target = wx.FindWindowById(initItems[1])
        start_vec = target.GetItems()[0:2]
        start_vec = [float(i) for i in start_vec]

        target = wx.FindWindowById(initItems[2])
        fixed_xs = []
        fixed_ys = []
        fixed_qs = []
        for item in target.GetItems():
            #print(item)
            item = item.split(" ")
            #print(item)
            x, y, q = item[0], item[1], item[2]
            x, y, q = float(x), float(y), float(q)
            fixed_xs.append(x)
            fixed_ys.append(y)
            fixed_qs.append(q)
        items = [start_loc, start_vec, fixed_xs, fixed_ys, fixed_qs]
        print(items)
        return items

    def AddAction(self, event):
        TI = wx.FindWindowById(self.ID_FIXED)
        if TI.GetItems():
            item = str(TI.GetItems()[0])+" "+str(TI.GetItems()[1])+" "+str(TI.GetItems()[2])

            LB = wx.FindWindowById(self.ID_LB)
            if TI.IsValidate():
                LB.Append(item)
                self.SetStatusText("")
        else: self.SetStatusText(u"数字を入力してください。")

    def DelAction(self, event):
        LB = wx.FindWindowById(self.ID_LB)
        if LB.GetSelection()>=0:
            LB.Delete(LB.GetSelection())
            self.SetStatusText("")
        else: self.SetStatusText(u"削除する対象を選択してください。")

    def SimulateAction(self, event):
        IDS = [self.ID_ELEC, self.ID_VEC]
        for ID in IDS:
            if not wx.FindWindowById(ID).IsValidate():
                self.SetStatusText(u"電子の開始条件を入力してください")
                return None
            else:
                self.SetStatusText("")
        items = self.GetAllItems()
        PlotFrame(self, items)


    def ResetAction(self, event):
        ID_LIST = [self.ID_ELEC, self.ID_VEC, self.ID_FIXED, self.ID_LB]
        for ID in ID_LIST:
            target = wx.FindWindowById(ID)
            target.Clear()
            if ID == self.ID_ELEC:
                target.Q.SetValue("-1")
            if ID == self.ID_VEC:
                target.Q.SetValue("0")


class PlotFrame(wx.Frame):
    def __init__(self, parent, items):
        wx.Frame.__init__(self, parent, size=(800, 700))

        self.parent = parent
        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(layout)
        self.imgBmp = self.main(items)

        layout.Add(wx.StaticBitmap(panel, label=self.imgBmp), proportion=1,
                   flag=wx.ALL, border=5)
        saveBtn = wx.Button(panel, label=u"保存")
        saveBtn.Bind(wx.EVT_BUTTON, self.save)
        layout.Add(saveBtn, flag=wx.ALIGN_CENTER | wx.ALL, border=20)

        self.Show()

    def main(self, items):
        init_elec_x, init_elec_y = items[0]
        init_elec_vx, init_elec_vy = items[1]
        init_xs = items[2]
        init_ys = items[3]
        init_qs = items[4]

        DT = 0.0005
        R = 0.001


        class coordinate:
            def __init__(self, x, y):
                self.x = x
                self.y = y


        class charge:
            def __init__(self, x, y, q):
                self.qxy = coordinate(x, y)
                self.q = q


        def inputq(xs, ys, qs):
            for x, y, q in zip(xs, ys, qs):
                yield x, y, q


        # 計算対象の初期化
        x = []
        y = []

        v_tmp = coordinate(init_elec_vx, init_elec_vy)
        loc_tmp = coordinate(init_elec_x, init_elec_y)

        # 配置電荷の初期化
        xs = init_xs #[0, 5, -3]
        ys = init_ys#[0, -5, 2]
        qs = init_qs#[10, 5, -3]

        qi = [charge(*val) for val in inputq(xs, ys, qs)]

        # シミュレーション用の初期化
        t = 0
        h = DT

        # print("%f\t%f\t%f\t%f\t%f" % (t, v_tmp.x, v_tmp.y, loc_tmp.x, loc_tmp.y))
        x.append(loc_tmp.x)
        y.append(loc_tmp.y)


        while 1:
            t += h
            rmin = 1  # DBL_MAX
            for Q in qi:
                rx = Q.qxy.x-loc_tmp.x
                ry = Q.qxy.y-loc_tmp.y
                r = math.sqrt(rx**2+ry**2)
                if r < rmin:
                    rmin = r
                try:
                    v_tmp.x += (rx/(r**3)*Q.q)*h
                    v_tmp.y += (ry/(r**3)*Q.q)*h
                except:
                    self.parent.SetStatusText(u"0割りが発生したので描画をしません。")
                    self.Destroy()
            loc_tmp.x += v_tmp.x*h
            loc_tmp.y += v_tmp.y*h
            # print("%f\t%f\t%f\t%f\t%f" % (t, v_tmp.x, v_tmp.y, loc_tmp.x, loc_tmp.y))
            x.append(loc_tmp.x)
            y.append(loc_tmp.y)

            if rmin < R:
                break
            if abs(loc_tmp.x) > 100 and abs(loc_tmp.y) > 100:
                break
            if t>1000:
                break


        # print(x)
        # print(y)

        plt.cla()
        plt.plot(x, y)
        plt.scatter(xs, ys)
        for numx, numy, q in zip(xs, ys, qs):
            q = str(q)
            plt.text(numx, numy, q)
        plt.scatter(x[0], y[0], s=100, marker="*")
        plt.title("electric field")

        #plt.show()
        plt.savefig("tmp.jpg")
        self.img = wx.Image("tmp.jpg")
        return wx.Bitmap(self.img)

    def save(self, event):
        fileDlg = wx.FileDialog(self, u"保存先を選択してください","", "", "*.png", wx.FD_SAVE)
        s = fileDlg.ShowModal()
        print(s)
        if s == 5100:
            filename = fileDlg.GetFilename()
            dirname = fileDlg.GetDirectory()
            print(os.path.join(dirname, filename))
            self.imgBmp.SaveFile(os.path.join(dirname, filename), type=wx.BITMAP_TYPE_PNG)
        fileDlg.Destroy()


# 以下は適当


app = wx.App(True, "./log.txt")
frame = TopFrame(app)

app.MainLoop()