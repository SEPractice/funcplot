
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

def __init__(self):

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