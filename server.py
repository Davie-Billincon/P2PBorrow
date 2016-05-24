#coding:utf-8

from flask import session
from flask import escape
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from wtforms import Form , StringField ,PasswordField , validators

from service import  *


app=Flask(__name__)




# 写死的用户名(系统加载之初,就自动添加管理员账户)
admin = "admin"
if ( not registerCheck(admin) ):
	addUser(admin,admin)
	addDetail(getUerID(admin),admin,admin,350301,186,2,3,3,3424,3000,7000,200,300)
	countCredit(admin)

class LoginForm(Form):
	username = StringField("username",[validators.Required()])
	password = PasswordField("password",[validators.Required()])
form = LoginForm()

# 访问起始点,根目录（根据session判断是否登录过，来重定向请求）
@app.route("/",methods=['GET','POST'])
def home():
	print "/"
	if 'username' in session:                             # 若是session中存在username，说明登陆过，直接跳转到首页
		username = escape(session['username'])
		print "/:    当前用户为:",username
		if (not detailCheck(username)):					  # 若是用户没有填写详情,让他填写详情
			print "/:    用户没有填写详情,重定向->/detail"
			return redirect("/detail")
		print "/:    session存在用户名,重定向—>shouye.html"
		return render_template('shouye.html',username = username)
	else:                                                 # 没登录过就跳转到登录页面
		print "/:    sessiong 没有用户名,重定向->/login"
		return redirect(url_for('login'))

# 登录页面展示 + 登录表单处理
@app.route("/login",methods=['GET','POST'])
def login():
	print "/login:request请求的form内容为:{}".format(request.form)
	myForm = LoginForm(request.form)					  # 使用request的form表单实例化LoginForm对象
	if request.method=='POST':							  # 如果是表单提交，则处理表单
		print "/login:    处理登录表单"
		print "->查询数据库"
		if loginCheck(myForm.username.data,myForm.password.data):	# 向数据库申请验证
			print "/login:        通过验证,重定向->/"
			session['username'] = myForm.username.data				# 向session插入该用户
			return redirect("/")									# 重定向到首页
		else:
			print "/login:        没通过验证,重定向->login.html"
			message=u"输入有误，请重新输入"								# 否则提示输入有误（不输入，密码错误，用户名不存在）
			return render_template('login.html',message=message,form=myForm)
	else:											      # 若是普通访问（GET请求是普通访问），则返回login网页
		print "/login:    展示登录页面,重定向->login.html"
		return render_template('login.html',form=myForm)

# 退出登录
@app.route('/logout')
def logout():
	username = str(escape(session['username']))
	print "/logout:退出登录:%s" %username
	session.pop('username', None)
	print "/logout:    重定向->/"
	return redirect("/")

# 注册处理模块
@app.route("/register",methods=['GET','POST'])
def register():
	print "/register:注册"
	myForm = LoginForm(request.form)
	if request.method =='POST':							  # 请求为POST说明有表单传送，将表单内容插入到数据库中
		print "/register:    处理注册表单"
		print "->数据库检查"
		if myForm.validate() and ( not registerCheck(myForm.username.data) ):
			print "/register:        通过检查,成功注册,重定向->/detail"
			addUser(myForm.username.data,myForm.password.data)
			session['username'] = myForm.username.data
			return redirect("/detail")
		else:
			isExist = registerCheck(myForm.username.data)
			print "/register:        用户名存在情况:%s , 重定向->regiter.html" %isExist
			message = u"用户存在请重新输入"
			return render_template('register.html', message=message, form=myForm)
	else:
		print "/register:    展示登录页面,重定向->register.html"
		return render_template('register.html',form=myForm)

@app.route("/detail",methods=['GET','POST'])
def detail():
	print "/detail:详情填写"
	if request.method=='POST':
		print "/detail:    处理详情表单"
		realname = request.form['realname']
		IDnumber = request.form['IDnumber']
		phone = request.form['phone']
		MarriageStatusId = request.form['MarriageStatusId']
		EducationId = request.form['EducationId']
		UserType = request.form['UserType']
		creditnumber = request.form['creditnumber']
		salary = request.form['salary']
		loan = request.form['loan']
		AverageSalarys = request.form['AverageSalarys']
		AverageSalary = request.form['AverageSalary']
		# 字段转译
		username = escape(session['username'])
		user_id = getUerID(username)
		realname = realname
		identity_id = IDnumber
		phone = phone
		marry_status_id = MarriageStatusId
		edu_status_id = EducationId
		work_status_id = UserType
		credit_card = creditnumber
		salary = salary
		house_loan = loan
		spare_money = AverageSalarys
		loan_repay = AverageSalary
		print "->数据库添加详情"
		addDetail(user_id, username, realname, identity_id,
				phone, marry_status_id, edu_status_id, work_status_id,
				credit_card, salary, house_loan, spare_money, loan_repay)
		# 计算初始信用
		print "->serveice重置用户信用"
		countCredit(username)
		print "/detail:    处理完详情,重定向->/"
		return redirect("/")
	print "/detail:    展示注册页面,重定向->detail.html"
	return render_template('detail.html')

# 展示个人信息 & 修改个人信息
@app.route("/showDetail",methods=['GET','POST'])
def showDetail():
	print "/showDetail:详情展示"
	username = str(escape(session['username']))
	print "/showDetail:    当前用户为: %s" % (username)
	if request.method=='GET':
		result = getAllDetail(username)
		return render_template('showDetail.html', result = result)
	else:
		print "/showDetail:    处理详情修改表单"
		realname = request.form['realname']
		IDnumber = request.form['IDnumber']
		phone = request.form['phone']
		MarriageStatusId = request.form['MarriageStatusId']
		EducationId = request.form['EducationId']
		UserType = request.form['UserType']
		creditnumber = request.form['creditnumber']
		salary = request.form['salary']
		loan = request.form['loan']
		AverageSalarys = request.form['AverageSalarys']
		AverageSalary = request.form['AverageSalary']
		# 字段转译
		username = escape(session['username'])
		user_id = getUerID(username)
		realname = realname
		identity_id = IDnumber
		phone = phone
		marry_status_id = MarriageStatusId
		edu_status_id = EducationId
		work_status_id = UserType
		credit_card = creditnumber
		salary = salary
		house_loan = loan
		spare_money = AverageSalarys
		loan_repay = AverageSalary
		print "->数据库添加详情"
		changeDetail(user_id, username, realname, identity_id,
				  phone, marry_status_id, edu_status_id, work_status_id,
				  credit_card, salary, house_loan, spare_money, loan_repay)
		return redirect("/showDetail")

# 借款模块
@app.route("/borrow",methods=['GET','POST'])
def borrow():
	print "/borrow:我要借款"
	username = str(escape(session['username']))
	print "/borrow:    当前用户为: %s" %(username)
	if request.method=='POST':
		print "/borrow:    处理借款表单"
		user_id = str(getUerID(username))
		borrow_money = float(request.form['borrow_money'])
		return_rate = str(request.form['return_rate'])
		duration = str(request.form['duration'])
		print "/borrow:    借款数据为   %s   %s   %s   %s" %(user_id,borrow_money,return_rate,duration)
		print "->数据库插入借款条目"
		if ( not addBorrow(user_id,username,borrow_money,return_rate,duration) ): # 若返回false,则是额度不够了
			print "/borrow:        额度不够,插入失败,重定向->borrow.html"
			credit = getCredit(username)
			message = u"您的额度不够了"
			return render_template('borrow.html',credit=credit,message = message,username = username)
		print "/borrow:    插入成功,重定向->/"
		return redirect("/")
	else:
		print "/borrow:    展示借款页面,重定向->borrow.html"
		credit = getCredit(username)
		return render_template('borrow.html',credit = credit,username = username)

# 获取自己的所有信息
@app.route("/myinfo",methods=['GET','POST'])
def myinfo():
	print "/myinfo:查看我自己的所有记录"
	username = str(escape(session['username']))
	print "/myinfo:    当前用户为: %s" %(username)
	if request.method=='GET':
		print "/myinfo:    展示自己相关信息的页面"
		print "->数据库查询一堆数据"
		borrowItems = getBorrow(username)
		badTimes = str(getTotalBadTimes(username))
		credit = str(getCredit(username))
		return_records = getRecord(username)
		lendRecord = getLend(username)
		money = str(getMoney(username))
		print "/myinfo:    myinfo查询完毕,重定向->myinfo.html"
		return render_template('myinfo.html',
							   	borrowItems = borrowItems,
							   	badTimes = badTimes,
							   	credit = credit,
							   	return_records = return_records,
							   	lendRecord = lendRecord,
							   	money = money,
								username=username
						   		)
	else:
		pass

# 获取还款展示信息
@app.route("/returnMoney",methods=['GET','POST'])
def returnMoney():
	username = str(escape(session['username']))
	print "/returnMoney:还款,当前用户为: %s" %(username)
	if request.method=='GET':
		print "/returnMoney:    展示还款页面"
		print "->数据库查询一堆"
		borrowItems = getBorrow(username)
		badTimes = str(getTotalBadTimes(username))
		credit = str(getCredit(username))
		return_records = getRecord(username)
		money = str(getMoney(username))
		print "/returnMoney:    还款信息查询完毕,重定向->return.html"
		return render_template('return.html',
						   borrowItems = borrowItems,
						   badTimes = badTimes,
						   credit = credit,
						   return_records = return_records,
						   money = money,
						   username=username
						   )
	else:
		print "/returnMoney:    处理还款提交"
		borrow_id = str(request.form['borrow_id'])
		return_time = str(request.form['return_time'])
		return_money = float(str(request.form['return_money']))
		print "/returnMoney:    borrow_id:%s  ,  return_time:%s  ,  return_money:%s" %(borrow_id,return_time,return_money)
		print "->service提交插入还款的请求"
		if(not return_dispatch(username,borrow_id,return_time,return_money)):
			print "/returnMoney:        还款失败,一般是 余额不足 / 还款额度大于欠款 / 其他违规还款 ,重定向->/returnMoney"
			return redirect("/returnMoney")
		print "/returnMoney:    成功插入还款条目,重定向->/returnMoney"
		return redirect("/returnMoney")

# 展示投资的大分类界面 & 分发子投资展示页面
@app.route("/showlendall", methods=['GET', 'POST'])
def showlend():
	print "/showlendall:进入投资浏览,浏览全部"
	username = str(escape(session['username']))
	print "/showlendall:    当前用户为: %s" % (username)
	if request.method == 'GET':
		print "/showlendall:    全部投资页面展示"
		print "->数据库查询可投资数据"
		order_duration = getActualBorrowOrderByDuration()
		order_rate = getActualBorrowOrderByRate()
		print "/showlendall:    可投资查询完毕,重定向->lend.html"
		return render_template('lend.html',
							   order_duration = order_duration,
							   order_rate = order_rate,
							   username = username
							   )
	else:
		print "/showlendall:    查看详细投资列表请求到来"
		searchType = str(request.form['searchType'])
		searchValue = int(str(request.form['searchValue']))
		if (searchType == "duration"):
			print "/showlendall:        按照duration查询"
			print "->数据库按照 duration 查询数据"
			searchResult = getActualBorrowUseDuration(searchValue)
		else :
			print "/showlendall:        按照return_rate查询"
			print "->数据库按照 rate 查询数据"
			searchResult = getActualBorrowUseRate(searchValue)
		print "/showlendall:    可投资细节数据查询完毕,重定向->lendpart.html"
		return render_template('lendpart.html', searchResult = searchResult , username = username)

@app.route("/lend",methods=['GET','POST'])
def lend():
	print "/lend:开始投资"
	username = str(escape(session['username']))
	print "/lend:    当前用户为: %s" %(username)
	if request.method=='GET':
		pass
	else:
		print "/lend:    处理投资请求"
		duration = int(request.form['duration'])
		lend_rate = int(request.form['lend_rate'])
		lend_money = float(request.form['lend_money'])
		print "/lend:    请求内容为:   duration:%s  ,  lend_rate:%s  ,  lend_money:%s" %(duration , lend_rate , lend_money)
		print "->数据库查询uerid"
		user_id = getUerID(username)
		print "->数据库插入投资条目( 会因为余额不足而投资失败 )"
		addLend(user_id,username,lend_money,lend_rate,duration)
		print "/lend:    无论投资失败与否,都重定向->/showlendall"
		return redirect("/showlendall")


# 后台管理
@app.route("/back",methods=['GET','POST'])
def back():
	print "/back:进入后台管理"
	username = str(escape(session['username']))
	print "/back:    当前用户为: %s" %(username)
	if request.method=='GET':
		print "/back:    后台页面展示"
		if (username != admin):
			print "/back:    用户不是admin用户,重定向->backerror.html"
			return render_template('backerror.html',username = username)
		print "->数据库查询一系列数据"
		print "/back:    后台数据查询完毕,重定向->back.html"
		return render_template('back.html')
	else:
		print "/back:    处理后台修改提交"
		user_change = str(request.form['user_change'])
		money = str(request.form['money'])
		print "->数据库插入修改内容"
		changeMoney(money,user_change)
		print "/back:    插入完毕,重定向->/myinfo"
		return redirect("/myinfo")








app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'#秘钥 自己设置 或者干脆随机生成。
if __name__=="__main__":
	app.run(port=8080)