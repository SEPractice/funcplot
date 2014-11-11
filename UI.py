#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
#
# Author: Cao Yang
# mail: 1054490383@qq.com
# Created Time: Sat 25 Oct 2014 03:50:50 PM 

import os
import copy
import cairo
import gtk
import sys
import rpy2.robjects as ro
import rpy2.rinterface as ri
from rpy2.robjects.packages import importr

class App(gtk.Window):

	count = 0
	
	def __init__(self):
		super(App, self).__init__()
		
		App.count = App.count + 1 
		self.d3 = 0
		self.d2d = 0
		self.d2y = 0
		self.d3_L = []
		self.d2d_L = []
		self.d2y_L = []
		self.flag =0
		self.filen = str(os.path.abspath(__file__))[:len(str(os.path.abspath(__file__)))-6]
		#self.ff = [(781, 588)]
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_title("FuncPlot"+str(App.count))
		#self.modify_bg(gtk.gdk.Color(65535, 65535, 65535))
		#self.ww = 781
		#self.hh = 588
		self.resize(781, 588)
		#self.connect("size-allocate", self.on_size)
		
		#菜单栏
		mb = gtk.MenuBar()
		filemenu = gtk.Menu()
		filem = gtk.MenuItem("文件(_F)", use_underline = True)
		filem.set_submenu(filemenu)
		mb.append(filem)
		
		agr = gtk.AccelGroup()
		self.add_accel_group(agr)
		
		#新建
		newi = gtk.ImageMenuItem(gtk.STOCK_NEW, agr)
		key, mod = gtk.accelerator_parse("<Control>N")
		newi.add_accelerator("activate", agr, key,
				mod, gtk.ACCEL_VISIBLE)
		filemenu.append(newi)
		newi.connect("activate", self.on_new)
		
		##打开
		#openi = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
		#key, mod = gtk.accelerator_parse("<Control>O")
		#openi.add_accelerator("activate", agr, key, 
		#		mod, gtk.ACCEL_VISIBLE)
		#filemenu.append(openi)
		#openi.connect("activate", self.on_open)
		
		#保存
		savei = gtk.ImageMenuItem(gtk.STOCK_SAVE, agr)
		key, mod = gtk.accelerator_parse("<Control>S")
		savei.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)
		filemenu.append(savei)
		savei.connect("activate", self.on_save)
		#分隔符
		sep = gtk.SeparatorMenuItem()
		filemenu.append(sep)
		
		#退出
		exiti = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
		key, mod = gtk.accelerator_parse("<Control>E")
		exiti.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)
		exiti.connect("activate", self.windestroy1)
		filemenu.append(exiti)
		
		#fileexit = gtk.MenuItem("退出")
		#fileexit.connect("activate", gtk.main_quit)
		#filemenu.append(fileexit)

		#作图
		graphmenu = gtk.Menu()
		graphm = gtk.MenuItem("作图(_D)", use_underline = True)
		graphm.set_submenu(graphmenu)
		mb.append(graphm)
		
		d2menu = gtk.Menu()
		graph2d = gtk.MenuItem("2D作图")
		graph3d = gtk.MenuItem("3D作图")

		dx = gtk.MenuItem("显函数作图")
		key, mod = gtk.accelerator_parse("<Control>1")
		dx.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)
		dy = gtk.MenuItem("隐函数作图")
		key, mod = gtk.accelerator_parse("<Control>2")
		dy.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)
		key, mod = gtk.accelerator_parse("<Control>3")
		graph3d.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)

		graph2d.set_submenu(d2menu)
		d2menu.append(dx)
		d2menu.append(dy)

		dx.connect("activate", self.on_2d)
		dy.connect("activate", self.on_2y)
		graph3d.connect("activate", self.on_3d)
		graphmenu.append(graph2d)
		graphmenu.append(graph3d)
		
		#编辑栏
		editmenu = gtk.Menu()
		editm = gtk.MenuItem("编辑(_E)", use_underline = True)
		editm.set_submenu(editmenu)
		mb.append(editm)
		self.ecount = 2
		
		#undo
		self.undoi = gtk.ImageMenuItem(gtk.STOCK_UNDO, agr)
		key, mod = gtk.accelerator_parse("<Control>U")
		self.undoi.add_accelerator("activate", agr, key,
				mod, gtk.ACCEL_VISIBLE)
		editmenu.append(self.undoi)
		self.undoi.connect("activate", self.on_undo)

		#redo
		self.redoi = gtk.ImageMenuItem(gtk.STOCK_REDO, agr)
		key, mod = gtk.accelerator_parse("<Control>R")
		self.redoi.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)
		editmenu.append(self.redoi)
		self.redoi.connect("activate", self.on_redo)

		#选项栏
		setmenu = gtk.Menu()
		setm = gtk.MenuItem("选项(_O)", use_underline = True)
		setm.set_submenu(setmenu)
		mb.append(setm)

		#显示工具栏
		tool = gtk.CheckMenuItem("显示工具栏")
		tool.set_active(True)
		tool.connect("activate", self.on_tool)
		setmenu.append(tool)

		#显示状态栏
		stat = gtk.CheckMenuItem("显示状态栏")
		stat.set_active(True)
		stat.connect("activate", self.on_status)
		setmenu.append(stat)

		#帮助
		helpmenu = gtk.Menu()
		helpm = gtk.MenuItem("帮助(_H)", use_underline = True)
		helpm.set_submenu(helpmenu)
		mb.append(helpm)

		helpxm = gtk.MenuItem("显示帮助")
		key, mod = gtk.accelerator_parse("<Control>Q")
		helpxm.add_accelerator("activate", agr, key,
				mod , gtk.ACCEL_VISIBLE)
		helpmenu.append(helpxm)
		helpxm.connect("activate", self.expose)

		#关于
		abouti = gtk.ImageMenuItem(gtk.STOCK_ABOUT, agr)
		key, mod = gtk.accelerator_parse("<Control>T")
		abouti.add_accelerator("activate", agr, key, 
				mod, gtk.ACCEL_VISIBLE)
		helpmenu.append(abouti)
		abouti.connect("activate", self.on_about)
		#工具栏
		self.toolbar = gtk.Toolbar()
		self.toolbar.set_style(gtk.TOOLBAR_ICONS)

		newtb = gtk.ToolButton(gtk.STOCK_NEW)
		newtb.set_tooltip_text("新建")
		#opentb = gtk.ToolButton(gtk.STOCK_OPEN)
		#opentb.set_tooltip_text("打开")
		savetb = gtk.ToolButton(gtk.STOCK_SAVE)
		savetb.set_tooltip_text("保存图片")
		sep1 = gtk.SeparatorToolItem()
		img2d = gtk.Image()
		img2y = gtk.Image()
		img3d = gtk.Image()
		img2d.set_from_file(self.filen + "/icon/2d.svg")
		img2y.set_from_file(self.filen + "/icon/2dy.svg")
		img3d.set_from_file(self.filen + "/icon/3d.png")
		tb2d = gtk.ToolButton(icon_widget = img2d)
		tb2d.set_tooltip_text("2D显函数作图")
		tb2y = gtk.ToolButton(icon_widget = img2y)
		tb2y.set_tooltip_text("2D隐函数作图")
		tb3d = gtk.ToolButton(icon_widget = img3d)
		tb3d.set_tooltip_text("3D作图")
		sep3 = gtk.SeparatorToolItem()
		self.undotb = gtk.ToolButton(gtk.STOCK_UNDO)
		self.undotb.set_tooltip_text("撤销")
		self.redotb = gtk.ToolButton(gtk.STOCK_REDO)
		self.redotb.set_tooltip_text("重做")
		sep2 = gtk.SeparatorToolItem()
		quittb = gtk.ToolButton(gtk.STOCK_QUIT)
		quittb.set_tooltip_text("退出")

		self.toolbar.insert(newtb, 0)	
		#self.toolbar.insert(opentb, 0)
		self.toolbar.insert(savetb, 1)
		self.toolbar.insert(sep1, 2)
		self.toolbar.insert(tb2d, 3)
		self.toolbar.insert(tb2y, 4)
		self.toolbar.insert(tb3d, 5)
		self.toolbar.insert(sep3, 6)
		self.toolbar.insert(self.undotb, 7)
		self.toolbar.insert(self.redotb, 8)
		self.toolbar.insert(sep2, 9)
		self.toolbar.insert(quittb, 10)

		newtb.connect("clicked", self.on_new)
		#opentb.connect("clicked", self.on_open)
		savetb.connect("clicked", self.on_save)
		tb2d.connect("clicked", self.on_2d)
		tb2y.connect("clicked", self.on_2y)
		tb3d.connect("clicked", self.on_3d)
		self.undotb.connect("clicked", self.on_undo)
		self.redotb.connect("clicked", self.on_redo)
		quittb.connect("clicked", self.windestroy1)

		#状态栏
		self.statusbar = gtk.Statusbar()
		self.statusbar.push(1, "就绪")
		
		#中间部分

		#pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(os.getcwd() + "/buf/file.png", 700, 700)
		#self.image = gtk.Image()
		#self.image.set_from_pixbuf(pixbuf)
		self.image = gtk.Image()
		self.image.set_from_file(self.filen  + "/buf/file.png")
		
		#图形控制
		self.vbtu = gtk.VBox(False, 0)
		
		#箭头
		hbA = gtk.HBox(False, 5)

		self.btnAl = gtk.Button()
		self.btnAr = gtk.Button()
		al = gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_IN)
		ar = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_IN)
		self.btnAl.add(al)
		self.btnAr.add(ar)
		self.btnAl.set_sensitive(False)

		self.btnAl.connect("clicked", self.on_al)
		self.btnAr.connect("clicked", self.on_ar)

		hbA.pack_end(self.btnAr, False, False, 0)
		hbA.pack_end(self.btnAl, False, False, 0)
		#2D显式
		self.vb2u = gtk.VBox(False, 20)

		#函数定义
		vbDe = gtk.VBox(False, 10)

		amtDe = gtk.Alignment(0, 0, 0, 0)
		lalDe = gtk.Label("2D显函数: ")
		amtDe.add(lalDe)
		
		hbDe = gtk.HBox(False, 0)
		laly = gtk.Label("y = ")
		self.etyP = gtk.Entry()
		self.etyP.set_text("sin(x)")
		self.etyP.connect("activate", self.on_ok2d)

		hbDe.pack_start(laly, False, False, 10)
		hbDe.pack_start(self.etyP, False, False, 0)
		
		vbDe.pack_start(amtDe, False, False, 0)
		vbDe.pack_start(hbDe, False, False, 0)

		#函数范围
		vbRg = gtk.VBox(False, 10)

		amtRg = gtk.Alignment(0, 0, 0, 0)
		lalRg = gtk.Label("绘制范围(x): ")
		amtRg.add(lalRg)

		hbRg1 = gtk.HBox(False, 0)
		hbRg2 = gtk.HBox(False, 0)
		lalM = gtk.Label("最小值: ")
		lalX = gtk.Label("最大值: ")
		#self.etyM = gtk.Entry()
		#self.etyM.set_text("0")
		#self.etyX = gtk.Entry()
		#self.etyX.set_text("1")
		adj = gtk.Adjustment(-3.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyM = gtk.SpinButton(adj, 0, 0)
		self.etyM.set_size_request(160, 28)
		adj = gtk.Adjustment(3.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyX = gtk.SpinButton(adj, 0, 0)
		self.etyX.set_size_request(160, 28)
		hbRg1.pack_start(lalM, False, False, 10)
		hbRg1.pack_start(self.etyM, False, False, 0)
		hbRg2.pack_start(lalX, False, False, 10)
		hbRg2.pack_start(self.etyX, False, False, 0)
		
		self.etyM.connect("value-changed", self.on_changeC2d)
		self.etyX.connect("value-changed", self.on_changeC2d)

		vbRg.pack_start(amtRg, False, False, 0)
		vbRg.pack_start(hbRg1, False, False, 0)
		vbRg.pack_start(hbRg2, False, False, 0)

		#附加
		vbAh = gtk.VBox(False, 0)
		
		amtAh = gtk.Alignment(0, 0, 0, 0)
		lalAh = gtk.Label("附加: ")
		amtAh.add(lalAh)

		hbMN = gtk.HBox(False, 0)
		hbFN = gtk.HBox(False, 0)
		lalMN = gtk.Label("主标题: ")
		lalFN = gtk.Label("副标题: ")
		self.etyMN = gtk.Entry()
		self.etyMN.set_text("三角正弦函数")
		self.etyFN = gtk.Entry()
		self.etyFN.set_text("Fangyu He")
		hbMN.pack_start(lalMN, False, False, 10)
		hbMN.pack_start(self.etyMN, False, False, 0)
		hbFN.pack_start(lalFN, False, False, 10)
		hbFN.pack_start(self.etyFN, False, False, 0)

		vbAh.pack_start(amtAh, False, False, 0)
		vbAh.pack_start(hbMN, False, False, 5)
		vbAh.pack_start(hbFN, False, False, 5)
		
		#图像设置
		vbGO = gtk.VBox(False, 0)

		amtGO = gtk.Alignment(0, 0, 0, 0)
		lalGO = gtk.Label("图像设置: ")
		amtGO.add(lalGO)
		
		hbGO = gtk.HBox(False, 0)
		lalCr = gtk.Label("颜色:")
		self.btnCr = gtk.ColorButton(gtk.gdk.Color())
		self.btnCr.connect("color-set", self.on_changeC2d)
		
		hbGO.pack_start(lalCr, False, False, 10)
		hbGO.pack_start(self.btnCr, False, False, 0)
		
		vbGO.pack_start(amtGO, False, False, 0)
		vbGO.pack_start(hbGO, False, False, 5)

		#执行按钮
		amto2d = gtk.Alignment(1, 0, 0, 0)
		ok2d = gtk.Button("确认")
		ok2d.connect("clicked", self.on_ok2d)
		amto2d.add(ok2d)

		self.vb2u.pack_start(vbDe, False, False, 0)
		self.vb2u.pack_start(vbAh, False, False, 5)
		self.vb2u.pack_start(vbRg, False, False, 5)
		self.vb2u.pack_start(vbGO, False, False, 5)
		self.vb2u.pack_start(amto2d, False, False, 5)
		
		#2D隐式
		self.vb2y = gtk.VBox(False, 20)

		#函数定义
		vbDey = gtk.VBox(False, 10)

		amtDey = gtk.Alignment(0, 0, 0, 0)
		lalDey = gtk.Label("2D隐函数: ")
		amtDey.add(lalDey)
		
		hbDey = gtk.HBox(False, 0)
		lalyy = gtk.Label("0 = ")
		self.etyPy = gtk.Entry()
		self.etyPy.set_text("x^3+y^3-3*x*y")
		self.etyPy.connect("activate", self.on_ok2y)
		hbDey.pack_start(lalyy, False, False, 10)
		hbDey.pack_start(self.etyPy, False, False, 0)
		
		vbDey.pack_start(amtDey, False, False, 0)
		vbDey.pack_start(hbDey, False, False, 0)

		#函数范围
		vbRgy = gtk.VBox(False, 10)

		amtRgy = gtk.Alignment(0, 0, 0, 0)
		lalRgy = gtk.Label("绘制范围: ")
		amtRgy.add(lalRgy)

		hbRg1y = gtk.HBox(False, 0)
		hbRg2y = gtk.HBox(False, 0)
		hbRg1yy = gtk.HBox(False, 0)
		hbRg2yy = gtk.HBox(False, 0)
		lalMy = gtk.Label("x 范围: ")
		lalXy = gtk.Label(" ~ ")
		#self.etyMy = gtk.Entry()
		#self.etyMy.set_text("-2")
		
		adj = gtk.Adjustment(-2.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyMy = gtk.SpinButton(adj, 0, 0)
		self.etyMy.set_size_request(55,28)
		#self.etyXy = gtk.Entry()
		#self.etyXy.set_text("2")
		adj = gtk.Adjustment(2.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyXy = gtk.SpinButton(adj, 0, 0)
		self.etyXy.set_size_request(55, 28)
		lalMyy = gtk.Label("y 范围: ")
		lalXyy = gtk.Label(" ~ ")
		#self.etyMyy = gtk.Entry()
		#self.etyMyy.set_text("-2")
		adj = gtk.Adjustment(-2.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyMyy = gtk.SpinButton(adj, 0, 0)
		self.etyMyy.set_size_request(55, 28)
		#self.etyXyy = gtk.Entry()
		#self.etyXyy.set_text("2")
		adj = gtk.Adjustment(2.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyXyy = gtk.SpinButton(adj, 0, 0)
		self.etyXyy.set_size_request(55, 28)

		self.etyMy.connect("value-changed", self.on_changeC2y)
		self.etyXy.connect("value-changed", self.on_changeC2y)
		self.etyMyy.connect("value-changed", self.on_changeC2y)
		self.etyXyy.connect("value-changed", self.on_changeC2y)

		hbRg1y.pack_start(lalMy, False, False, 10)
		hbRg1y.pack_start(self.etyMy, False, False, 0)
		hbRg1y.pack_start(lalXy, False, False, 10)
		hbRg1y.pack_start(self.etyXy, False, False, 0)
		hbRg2y.pack_start(lalMyy, False, False, 10)
		hbRg2y.pack_start(self.etyMyy, False, False, 0)
		hbRg2y.pack_start(lalXyy, False, False, 10)
		hbRg2y.pack_start(self.etyXyy, False, False, 0)
		
		
		vbRgy.pack_start(amtRgy, False, False, 0)
		vbRgy.pack_start(hbRg1y, False, False, 0)
		vbRgy.pack_start(hbRg2y, False, False, 0)
		#vbRgy.pack_start(hbRg1yy, False, False, 0)
		#vbRgy.pack_start(hbRg2yy, False, False, 0)

		#附加
		vbAhy = gtk.VBox(False, 0)
		
		amtAhy = gtk.Alignment(0, 0, 0, 0)
		lalAhy = gtk.Label("附加: ")
		amtAhy.add(lalAhy)

		hbMNy = gtk.HBox(False, 0)
		hbFNy = gtk.HBox(False, 0)
		lalMNy = gtk.Label("主标题: ")
		lalFNy = gtk.Label("副标题: ")
		self.etyMNy = gtk.Entry()
		self.etyMNy.set_text("笛卡尔叶形线")
		self.etyFNy = gtk.Entry()
		self.etyFNy.set_text("Fangyu He")
		hbMNy.pack_start(lalMNy, False, False, 10)
		hbMNy.pack_start(self.etyMNy, False, False, 0)
		hbFNy.pack_start(lalFNy, False, False, 10)
		hbFNy.pack_start(self.etyFNy, False, False, 0)

		vbAhy.pack_start(amtAhy, False, False, 0)
		vbAhy.pack_start(hbMNy, False, False, 5)
		vbAhy.pack_start(hbFNy, False, False, 5)
		
		#图像设置
		vbGOy = gtk.VBox(False, 0)

		amtGOy = gtk.Alignment(0, 0, 0, 0)
		lalGOy = gtk.Label("图像设置: ")
		amtGOy.add(lalGOy)
		
		hbGOy = gtk.HBox(False, 0)
		lalCry = gtk.Label("颜色:")
		self.btnCry = gtk.ColorButton(gtk.gdk.Color())
		self.btnCry.connect("color-set", self.on_changeC2y)
		
		hbGOy.pack_start(lalCry, False, False, 10)
		hbGOy.pack_start(self.btnCry, False, False, 0)
		
		vbGOy.pack_start(amtGOy, False, False, 0)
		vbGOy.pack_start(hbGOy, False, False, 5)

		#执行按钮
		amto2dy = gtk.Alignment(1, 0, 0, 0)
		ok2y = gtk.Button("确认")
		ok2y.connect("clicked", self.on_ok2y)
		amto2dy.add(ok2y)
		
		self.vb2y.pack_start(vbDey, False, False, 0)
		self.vb2y.pack_start(vbAhy, False, False, 5)
		self.vb2y.pack_start(vbRgy, False, False, 5)
		self.vb2y.pack_start(vbGOy, False, False, 5)
		self.vb2y.pack_start(amto2dy,False, False, 0 )
		#3D
		self.vb23 = gtk.VBox(False, 20)

		#函数定义
		vbDe3 = gtk.VBox(False, 10)

		amtDe3 = gtk.Alignment(0, 0, 0, 0)
		lalDe3 = gtk.Label("3D函数: ")
		amtDe3.add(lalDe3)
		
		hbDe3 = gtk.HBox(False, 0)
		laly3 = gtk.Label("z = ")
		self.etyP3 = gtk.Entry()
		
		self.etyP3.set_text("x*cos(2*pi*x)+sin(2*pi*y/3)")
		self.etyP3.connect("activate", self.on_ok23)
		#self.etyP3.connect("preedit-changed", self.change_fun3)
		hbDe3.pack_start(laly3, False, False, 10)
		hbDe3.pack_start(self.etyP3, False, False, 0)
		
		vbDe3.pack_start(amtDe3, False, False, 0)
		vbDe3.pack_start(hbDe3, False, False, 0)

		#函数范围
		vbRg3 = gtk.VBox(False, 10)

		amtRg3 = gtk.Alignment(0, 0, 0, 0)
		lalRg3 = gtk.Label("绘制范围: ")
		amtRg3.add(lalRg3)

		hbRg13 = gtk.HBox(False, 0)
		hbRg23 = gtk.HBox(False, 0)
		hbRg1y3 = gtk.HBox(False, 0)
		hbRg2y3 = gtk.HBox(False, 0)

		lalM3 = gtk.Label("x 范围: ")
		lalX3 = gtk.Label(" ~ ")
		#self.etyM3 = gtk.Entry()
		adj = gtk.Adjustment(0.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyM3 = gtk.SpinButton(adj, 0, 0)
		#self.etyM3.set_text("0")
		self.etyM3.set_size_request(55,28)
		#self.etyX3 = gtk.Entry()
		#self.etyX3.set_text("1")
		adj = gtk.Adjustment(1.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyX3 = gtk.SpinButton(adj, 0, 0)
		self.etyX3.set_size_request(55, 28)
		lalMy3 = gtk.Label("y 范围: ")
		lalXy3 = gtk.Label(" ~ ")
		adj = gtk.Adjustment(0.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyMy3 = gtk.SpinButton(adj, 0, 0)
		#self.etyMy3 = gtk.Entry()
		#self.etyMy3.set_text("0")
		self.etyMy3.set_size_request(55, 28)
		adj = gtk.Adjustment(1.0, -9999.0, 9999.0, 1.0, 5.0, 0.0)
		self.etyXy3 = gtk.SpinButton(adj, 0, 0)
		#self.etyXy3 = gtk.Entry()
		#self.etyXy3.set_text("1")
		self.etyXy3.set_size_request(55, 28)

		self.etyM3.connect("value-changed", self.on_changeC3)
		self.etyX3.connect("value-changed", self.on_changeC3)
		self.etyMy3.connect("value-changed", self.on_changeC3)
		self.etyXy3.connect("value-changed", self.on_changeC3)

		hbRg13.pack_start(lalM3, False, False, 10)
		hbRg13.pack_start(self.etyM3, False, False, 0)
		hbRg13.pack_start(lalX3, False, False, 10)
		hbRg13.pack_start(self.etyX3, False, False, 0)
		hbRg23.pack_start(lalMy3, False, False, 10)
		hbRg23.pack_start(self.etyMy3, False, False, 0)
		hbRg23.pack_start(lalXy3, False, False, 10)
		hbRg23.pack_start(self.etyXy3, False, False, 0)
		
		
		vbRg3.pack_start(amtRg3, False, False, 0)
		vbRg3.pack_start(hbRg13, False, False, 0)
		vbRg3.pack_start(hbRg23, False, False, 0)
		#vbRgy.pack_start(hbRg1yy, False, False, 0)
		#vbRgy.pack_start(hbRg2yy, False, False, 0)

		#附加
		vbAh3 = gtk.VBox(False, 0)
		
		amtAh3 = gtk.Alignment(0, 0, 0, 0)
		lalAh3 = gtk.Label("附加: ")
		amtAh3.add(lalAh3)

		hbMN3 = gtk.HBox(False, 0)
		hbFN3 = gtk.HBox(False, 0)
		lalMN3 = gtk.Label("主标题: ")
		lalFN3 = gtk.Label("副标题: ")
		self.etyMN3 = gtk.Entry()
		self.etyMN3.set_text("3D Demo")
		self.etyFN3 = gtk.Entry()
		self.etyFN3.set_text("Fangyu He")
		hbMN3.pack_start(lalMN3, False, False, 10)
		hbMN3.pack_start(self.etyMN3, False, False, 0)
		hbFN3.pack_start(lalFN3, False, False, 10)
		hbFN3.pack_start(self.etyFN3, False, False, 0)

		vbAh3.pack_start(amtAh3, False, False, 0)
		vbAh3.pack_start(hbMN3, False, False, 5)
		vbAh3.pack_start(hbFN3, False, False, 5)
		
		#图像设置
		vbGO3 = gtk.VBox(False, 0)

		amtGO3 = gtk.Alignment(0, 0, 0, 0)
		lalGO3 = gtk.Label("图像设置: ")
		amtGO3.add(lalGO3)
		
		hbGO3 = gtk.HBox(False, 0)
		lalCr3 = gtk.Label("颜色:")
		self.btnCr3 = gtk.ColorButton(gtk.gdk.Color(54648, 56558,15111))
		self.btnCr3.connect("color-set", self.on_changeC3)

		self.cobb = gtk.combo_box_new_text()
		self.cobb.append_text('默认图形')
		self.cobb.append_text('3D图形2')
		self.cobb.append_text('等高线图')
		self.cobb.set_active(0)
		self.cobb.connect('changed', self.change_cb)	

		hbGO3.pack_start(lalCr3, False, False, 10)
		hbGO3.pack_start(self.btnCr3, False, False, 0)
		hbGO3.pack_end(self.cobb, False, False, 0)
		
		vbGO3.pack_start(amtGO3, False, False, 0)
		vbGO3.pack_start(hbGO3, False, False, 5)

		#执行按钮
		amto2d3 = gtk.Alignment(1, 0, 0, 0)
		ok23 = gtk.Button("确认")
		ok23.connect("clicked", self.on_ok23)
		amto2d3.add(ok23)

		frame3d = gtk.Frame()
		frame3d.set_label("选项")
		frame3d.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		
		#vbRG = gtk.VBox(False, 20)
		#vbRG.set_border_width(5)
		#vbRG.pack_start(vbRg3, False, False, 5)
		#vbRG.pack_start(vbGO3, False, False, 5)

		#frame3d.add(vbRG)

		self.vb23.pack_start(vbDe3, False, False, 0)
		self.vb23.pack_start(vbAh3, False, False, 5)
		self.vb23.pack_start(vbRg3, False, False, 5)
		self.vb23.pack_start(vbGO3, False, False, 5)
		#self.vb23.pack_start(frame3d,False, False, 5 )
		self.vb23.pack_start(amto2d3,False, False, 0 )
		

		#图像设定容器
		self.vbtu.pack_start(hbA, False, False, 5)
		self.vbtu.pack_start(self.vb2u, False, False, 0)	

		#容器
		self.vb = gtk.VBox(False, 0)
		self.hb = gtk.HBox(False, 0)
		self.hb.pack_start(self.vbtu, False, False, 10)
		self.hb.pack_end(self.image, False, False, 8)
		self.vb.pack_start(mb, False, False, 0)
		self.vb.pack_start(self.toolbar, False, False, 0)
		self.vb.pack_start(self.hb, True, True, 0)
		self.vb.pack_start(self.statusbar, False, False, 0)

		#print self.vbtu.get_allocation()
		
		self.add(self.vb)

		self.connect("delete-event", self.windestroy)
		self.show_all()

		gtk.main()

	def on_new(self, widget):

		App()

	def on_open(self, widget):

		dialog = gtk.FileChooserDialog("",
									   None,
									   gtk.FILE_CHOOSER_ACTION_OPEN,
									   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
										gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("Images")
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/jpeg")
		filter.add_mime_type("image/gif")
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		filter.add_pattern("*.gif")
		filter.add_pattern("*.tif")
		filter.add_pattern("*.xpm")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			print dialog.get_filename(), 'selected'
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		dialog.destroy()
	
	def on_save(self, widget):

		dialog = gtk.FileChooserDialog("",
									   None,
									   gtk.FILE_CHOOSER_ACTION_SAVE,
									   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
										gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_current_name("funcplot" + str(App.count))

		#filter = gtk.FileFilter()
		#filter.set_name("All files")
		#filter.add_pattern("*")
		#dialog.add_filter(filter)

		#filter = gtk.FileFilter()
		#filter.set_name("Images")
		#filter.add_mime_type("image/png")
		#filter.add_mime_type("image/jpeg")
		#filter.add_mime_type("image/gif")
		#filter.add_pattern("*.png")
		#filter.add_pattern("*.jpg")
		#filter.add_pattern("*.gif")
		#filter.add_pattern("*.tif")
		#filter.add_pattern("*.xpm")
		#dialog.add_filter(filter)
		
		for bb in self.vbtu.get_children():
			if bb == self.vb2u and self.d2d == 1:
				file = open(self.filen + "/buf/bu2d.png", "r")
			if bb == self.vb2y and self.d2y == 1:
				file = open(self.filen + "/buf/2ybu.png", "r")
			if bb == self.vb23 and self.d3 == 1:
				file = open(self.filen + "/buf/bu3d.png", "r")
			else:
				file = open(self.filen + "/buf/file.png", "r")

		savef = file.readlines()
		file.close()


		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			savefile = open(dialog.get_filename() + ".png", "w")
			savefile.writelines(savef)
			if self.flag == 1:
				gtk.main_quit()
		elif response == gtk.RESPONSE_CANCEL and self.flag == 1:
			gtk.main_quit()
			
		dialog.destroy()

