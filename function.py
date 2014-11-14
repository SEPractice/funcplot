
#
# Author: Bao Di
# mail: 771385600@qq.com
# Created Time: Sat 1 Nov 2014 13:14:14 PM 

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

def on_ok2d(self, widget):

		
		self.d2d_L += [self.etyP.get_text()]

		ly = self.etyP.get_text()		
		lal = "fun <- function(x) " + ly 
		try:
			ro.r(lal)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		xm = "xm <- " + self.etyM.get_text()
		xx = "xx <- " + self.etyX.get_text()
		try:
			ro.r(xm)
			ro.r(xx)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的范围！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		ro.r("xl <- c(xm, xx)")

		#grdevices = importr('grDevices')
		#graphics = importr('graphics')
		#grdevices.png('2dbu.png', width = 512, height = 512)
		#expr = ri.parse(ly)
		#graphics.curve(expr,main=self.etyM.get_text())
		#grdevices.dev_off()

		if self.etyMN.get_text() == "":
			m = "m <- ' '"
		else:
			m = "m <- '" + self.etyMN.get_text() + "'"
		if self.etyFN.get_text() == "":
			nm = "nm <- ' '"
		else:
			nm = "nm <- '" + self.etyFN.get_text() + "'"
		try:
			ro.r(m)
			ro.r(nm)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0

		col2d = self.btnCr.get_color()
		colo = "c<-rgb(" + str(col2d.red) +", " + str(col2d.green) + "," + str(col2d.blue) + "," + "maxColorValue=65535)"
		ro.r(colo)

		ro.r("png("+"'" + self.filen+"/buf/bu2d.png'"+", width = 512, height = 512)")
		try:
			ro.r("curve(fun, xlim = xl, main = m, sub = nm, col = c)")
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		ro.r("dev.off()")
                self.d2d = 1

		self.image.set_from_file(self.filen + "/buf/bu2d.png")
		self.show_all()

	def on_ok2y(self, widget):

		
		self.d2y_L += [self.etyPy.get_text()]

		ly = self.etyPy.get_text()
		lal = "fun <- function(x,y) " + ly
		try:
			ro.r(lal)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0

		xm = "xm <- " + self.etyMy.get_text()
		xx = "xx <- " + self.etyXy.get_text()
		ym = "ym <- " + self.etyMyy.get_text()
		yx = "yx <- " + self.etyXyy.get_text()
		try:
			ro.r(xm)
			ro.r(xx)
			ro.r(ym)
			ro.r(yx)
                        ro.r("xl <- seq(xm, xx, length = 1000)")
                        ro.r("yl <- seq(ym, yx, length = 1000)")
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数范围！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0

		
		if self.etyMNy.get_text() == "":
			m = "m <- ' '"
		else:
			m = "m <- '" + self.etyMNy.get_text() + "'"
		if self.etyFNy.get_text() == "":
			nm = "nm <- ' '"
		else:
			nm = "nm <- '" + self.etyFNy.get_text() + "'"
		try:
			ro.r(m)
			ro.r(nm)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0

		#grdevices = importr('grDevices')
		#graphics = importr('graphics')
		#grdevices.png('2ybu.png', width = 512, height = 512)
		##laly = "funcp = lambda x, y: " + ly
		##print laly, lal
		#zz = ri.globalenv.get("fun")
		##exec(laly)
		##cost_f = ri.rternalize(funcp)
		#seq = ri.globalenv.get("seq")
		#contour = ri.globalenv.get("contour")
		#outer = ri.globalenv.get("outer")
		#a1 = [-2.0]
		#a2 = [2]
		#b1 = [-2.0]
		#b2 = [2]
		#a = seq(ri.IntSexpVector(a1),ri.IntSexpVector(a2),length=ri.IntSexpVector([50,]))
		#b = seq(ri.IntSexpVector(b1),ri.IntSexpVector(b2),length=ri.IntSexpVector([50,]))
			
		col2y = self.btnCry.get_color()
		colo = "c<-rgb(" + str(col2y.red) +", " + str(col2y.green) + "," + str(col2y.blue) + "," + "maxColorValue=65535)"
		ro.r(colo)

		ro.r("png("+"'" + self.filen+"/buf/2ybu.png'"+", width = 512, height = 512)")
		try:
			ro.r("z <- outer(xl, yl, fun)")
			ro.r("contour(xl, yl, z, col = c, main = m, sub = nm, levels = 0)")
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		ro.r("dev.off()")
		#z = outer(a,b,zz)
		#contour(a,b,z,levels=ri.IntSexpVector([0,]))
		##graphics.curve(expr)
		#grdevices.dev_off()
                self.d2y = 1

		self.image.set_from_file(self.filen + "/buf/2ybu.png")
		self.show_all()
	
	def on_ok23(self, widget):

		
		self.d3_L += [self.etyP3.get_text()]
		
		ly = self.etyP3.get_text()
		func3 = "fun <- function(x, y) " + ly
		try:
			ro.r(func3)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		
		xm = "xm <- " + self.etyM3.get_text()
		xx = "xx <- " + self.etyX3.get_text()
		ym = "ym <- " + self.etyMy3.get_text()
		yx = "yx <- " + self.etyXy3.get_text()
		try:
			ro.r(xm)
			ro.r(xx)
			ro.r(ym)
			ro.r(yx)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数范围！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		ro.r("xl <- c(xm, xx)")
		ro.r("yl <- c(ym, yx)")

		if self.etyMN3.get_text() == "":
			m = "m <- ' '"
		else:
			m = "m <- '" + self.etyMN3.get_text() + "'"
		if self.etyFN3.get_text() == "":
			nm = "nm <- ' '"
		else:
			nm = "nm <- '" + self.etyFN3.get_text() + "'"
		try:
			ro.r(m)
			ro.r(nm)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0

		if self.cobb.get_active_text() == "默认图形":
			s3d = "s3d <- 'wireframe'"
		elif self.cobb.get_active_text() == "3D图形2":
			s3d = "s3d <- 'persp'"
		elif self.cobb.get_active_text() == "等高线图":
			s3d = "s3d <- 'contour'"
		try:
			ro.r(s3d)
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的函数格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0

		col3d = self.btnCr3.get_color()
		colo = "c <- rgb(" + str(col3d.red) +"," + str(col3d.green) + "," + str(col3d.blue) + "," + "maxColorValue=65535)"
		ro.r(colo)
		#self.ww == 781
		#self.hh == 588
		#wid = "wid <- " + str(self.ww)
		#hei = "hei <- " + str(self.hh)
		#ro.r(wid)
		#ro.r(hei)
		
		ro.r("library(emdbook)")
		try:
			ro.r("png("+"'" + self.filen+"/buf/bu3d.png'"+", width = 512, height = 512)")
			ro.r("curve3d(fun, xlim = xl, ylim = yl, col = c, main = m, sub = nm, sys3d = s3d)")
		except:
			md = gtk.MessageDialog(None,
					0,gtk.MESSAGE_WARNING,
					gtk.BUTTONS_CLOSE,"请输入正确的格式！")
			n = md.add_button(gtk.STOCK_HELP,gtk.RESPONSE_HELP)
			n.connect("clicked",self.expose)
			n.show_all()
			md.run()
			md.destroy()
			return 0
		ro.r("dev.off()")
                self.d3 = 1

		self.image.set_from_file(self.filen + "/buf/bu3d.png")
		self.show_all()