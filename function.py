
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
		self.etyFN.set_text("Baodi&Caoyang")
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
		self.etyFNy.set_text("Baodi&Caoyang")
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
