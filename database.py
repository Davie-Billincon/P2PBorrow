# coding:utf-8
import sqlite3
import csv

import time
import datetime

import random

import service

# str 转精度
def strToFloat(str):
	return float('%0.2f'%float(str))



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




conn_all = sqlite3.connect("database/all.db")
cur_all = conn_all.cursor()

cur_all.execute("""
    CREATE TABLE IF NOT EXISTS users(
			user_id 			integer PRIMARY KEY AUTOINCREMENT NOT NULL,
			username 			varchar UNIQUE,
			password			varchar,
			credit_limit        varchar,
			money				varchar,
			credit_level		integer
			)
""")

cur_all.execute("""
    CREATE TABLE IF NOT EXISTS users_detail(
    			user_id 			integer REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    			username 			varchar REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    			realname 			varchar,
    			identity_id 		varchar,
    			phone 				varchar,
    			marry_status_id 	varchar,
    			edu_status_id 		varchar,
    			work_status_id 		varchar,
    			credit_card 		varchar,
    			salary 				varchar,
    			house_loan 			varchar,
    			spare_money 		varchar,
    			loan_repay   		varchar
    			)
""")
cur_all.execute("""
    CREATE TABLE IF NOT EXISTS all_borrow(
    		    borrow_id 			integer,
    			user_id 			integer REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    			username 			varchar REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    			borrow_money 		varchar,
    			return_rate         integer,
    			return_money        varchar,
    			borrow_date 		varchar,
    			duration 			integer,
    			duetime_phase       varchar,
    			recent_duetime      varchar,
    			recent_duemoney     varchar,
    			has_return			varchar,
    			bad_times   		varchar,
    			aim					varchar
    			)
""")
cur_all.execute("""
    CREATE TABLE IF NOT EXISTS all_lend(
    		    lend_id 			integer,
    			user_id 			integer REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    			username 			varchar REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    			lend_money 			varchar,
    			lend_rate         	integer,
    			back_money       	varchar,
    			lend_date 			varchar,
    			duration 			integer,
    			return_date			varchar,
    			isReturn			varchar
    			)
""")
cur_all.execute("""
    CREATE TABLE IF NOT EXISTS lend_borrow(
    		    lend_id 			integer REFERENCES all_lend(lend_id),
    		    username		integer REFERENCES users(username),
    		    borrow_id 			integer REFERENCES all_borrow(borrow_id)
    			)
""")

# 在数据库中添加用户(总数据库添加用户的同时,为该用户开辟其自己的数据库)
def addUser(username,password):
	# 检测该用户是否存在
	if ( registerCheck(username)  ):
		return
	# 在总数据库添加用户
	sql = """
		insert into users
			  (username,password,credit_limit,money,credit_level)
		values('%s','%s',0,0,0)
		""" %(username,password)
	cur_all.execute(sql)
	conn_all.commit()
	# 为该用户开辟从数据库（存放贷款还款信息等）
	conn_user = sqlite3.connect("database/%s.db"%username)
	cur_user = conn_user.cursor()
	sql="""
        CREATE TABLE IF NOT EXISTS borrow(
    		    borrow_id 			integer PRIMARY KEY AUTOINCREMENT,
    			borrow_money 		varchar,
    			return_rate         integer,
    			return_money        varchar,
    			borrow_date 		varchar,
    			duration 			integer,
    			duetime_phase       varchar,
    			recent_duetime      varchar,
    			recent_duemoney     varchar,
    			has_return			varchar,
    			bad_times   		varchar,
    			aim					varchar
    			)
    """
	cur_user.execute(sql)
	sql = """
		CREATE TABLE IF NOT EXISTS return_record(
			borrow_id 	  integer REFERENCES borrow(borrow_id) ON DELETE CASCADE ON UPDATE CASCADE ,
		    ahead_days 	  varchar,
			money_differ  varchar,
	  		duemoney	  varchar,
	  		actual_return varchar
			)
	"""
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close
	sql = """
			CREATE TABLE IF NOT EXISTS lend(
    		    lend_id 			integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    			lend_money 			varchar,
    			lend_rate         	integer,
    			back_money       	varchar,
    			lend_date 			varchar,
    			duration 			integer,
    			return_date			varchar,
    			isReturn			varchar
    			)
		"""
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




# 用户名验证
def loginCheck(username,password):
    sql = """
        select * from users WHERE username="%s"and password="%s"
    """ % (username, password)
    cur_all.execute(sql)
    values = cur_all.fetchall()		# fetchall 能够抓取查询结果的所有条目,返回一个 列表(行)的列表
    if (len(values)==0):
	    return False
    else:
	    return True

# 注册验证：查询注册的用户是否存在
def registerCheck(username):
    sql = """
        select * from users WHERE username="%s"
    """%(username)
    cur_all.execute(sql)
    values = cur_all.fetchall()
    if (len(values)==0):
		return False
    else:
		return True

# 获取用户的ID主键
def getUerID(username):
	sql = """
		SELECT user_id FROM users
		WHERE username == '%s';
	""" % (username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	return values[0]

# 添加详情
def addDetail(user_id , username , realname , identity_id ,
			  phone , marry_status_id , edu_status_id , work_status_id ,
			  credit_card , salary , house_loan , spare_money , loan_repay):
	# 检测是否已经有用户详情了
	sql = """
	        select * from users_detail WHERE username="%s"
	    """ % (username)
	cur_all.execute(sql)
	values = cur_all.fetchall()
	if (len(values) != 0):
		return
	# 没有的话就执行插入
	sql = """
		insert into users_detail
			  (user_id , username , realname , identity_id ,
			  phone , marry_status_id , edu_status_id , work_status_id ,
			  credit_card , salary , house_loan , spare_money , loan_repay)
		values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
	""" %(user_id , username , realname , identity_id ,
			  phone , marry_status_id , edu_status_id , work_status_id ,
			  credit_card , salary , house_loan , spare_money , loan_repay)
	cur_all.execute(sql)
	conn_all.commit()
	return

#获取用户所有详情
def getAllDetail(username):
	sql = """
			SELECT * FROM users_detail
			WHERE username = '%s'
		""" % (username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	result = {}
	result['realname'] = str(values[2])
	result['identity_id'] = str(values[3])
	result['phone'] = str(values[4])
	result['marry_status_id'] = int(values[5])
	result['edu_status_id'] = int(values[6])
	result['work_status_id'] = int(values[7])
	result['credit_card'] = str(values[8])
	result['salary'] = str(values[9])
	result['house_loan'] = str(values[10])
	result['spare_money'] = str(values[11])
	result['loan_repay'] = str(values[12])
	return result

# 改变详情
def changeDetail(user_id , username , realname , identity_id ,
			  phone , marry_status_id , edu_status_id , work_status_id ,
			  credit_card , salary , house_loan , spare_money , loan_repay):
	sql = """
		UPDATE users_detail
		SET	user_id = '%s', realname = '%s' , identity_id = '%s' ,
			  phone = '%s' , marry_status_id = '%s' , edu_status_id = '%s', work_status_id = '%s' ,
			  credit_card = '%s' , salary = '%s' , house_loan = '%s' , spare_money = '%s' , loan_repay = '%s'
		WHERE username = '%s'
	""" %(user_id , realname , identity_id ,
			phone , marry_status_id , edu_status_id , work_status_id ,
			credit_card , salary , house_loan , spare_money , loan_repay , username)
	cur_all.execute(sql)
	conn_all.commit()

# 获取用户是否已经有详情了
def detailCheck(username):
	sql = """
            select * from users_detail WHERE username="%s"
        """ % (username)
	cur_all.execute(sql)
	values = cur_all.fetchall()
	if (len(values) == 0):
		return False
	else:
		return True
# 获取部分详情(返回对象为字典)
def getPartDetail(username):
	sql = """
		SELECT * FROM users_detail
		WHERE username = '%s'
	""" %(username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	result = {}
	result['marry_status_id'] = int(values[5])
	result['edu_status_id'] = int(values[6])
	result['work_status_id'] = int(values[7])
	result['salary'] = int(values[9])
	result['house_loan'] = int(values[10])
	result['spare_money'] = int(values[11])
	result['loan_repay'] = int(values[12])
	return result
# 获取详情的剩余部分
def getLastDetail(username):
	result = {}
	result['is_realname'] = random.choice(range(2))
	result['credit_money'] = random.choice(range(10000))
	return result




# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




# 更新用户信用额度
def changeCredit(credit_limit,username):
	sql = """
    		UPDATE users
			SET credit_limit = '%s'
			WHERE username == '%s';
    	""" % (credit_limit, username)
	cur_all.execute(sql)
	conn_all.commit()
	return
# 获取用户信用额度
def getCredit(username):
	# service.changeCreditUseDeal()
	sql = """
		SELECT credit_limit FROM users
		WHERE username == '%s';
    """ % (username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	return float(values[0])


# 更新用户的存款
def changeMoney(money,username):
	if(float(money) < 0):
		return False
	sql = """
    		UPDATE users
			SET money = '%s'
			WHERE username == '%s';
    	""" % (money, username)
	cur_all.execute(sql)
	conn_all.commit()
	return True
# 获取用户存款
def getMoney(username):
	sql = """
		SELECT money FROM users
		WHERE username == '%s';
    """ % (username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	return float(values[0])


# 更新用户密码
def changePassword(password,username):
	sql = """
    		UPDATE users
			SET password = '%s'
			WHERE username == '%s';
    	""" % (password, username)
	cur_all.execute(sql)
	conn_all.commit()
	return True
# 获取用户密码
def getPassword(username):
	sql = """
		SELECT password FROM users
		WHERE username == '%s';
    """ % (username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	return str(values[0])


# 更新用户信用等级
def changeLevel(credit_level,username):
	sql = """
    		UPDATE users
			SET credit_level = %d
			WHERE username == '%s';
    	""" % (credit_level, username)
	cur_all.execute(sql)
	conn_all.commit()
	return True
# 获取用户信用等级
def getLevel(username):
	sql = """
		SELECT credit_level FROM users
		WHERE username == '%s';
    """ % (username)
	cur_all.execute(sql)
	values = cur_all.fetchone()
	return int(values[0])


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




# 添加借款记录
def addBorrow(user_id,username,borrow_money,return_rate,duration,aim):
	print "向数据库添加借款"
	# 先获取借款记录的初始信息
	return_money = float(borrow_money) * (1 + float(return_rate)/100)
	print "    添加借款记录:return_money = ",return_money
	timeStrMe = time.strftime("%Y-%m-%d", time.localtime())			# 获取当前时间字符串
	borrow_date = timeStrMe
	print "    添加借款记录:borrow_date = ",borrow_date
	duetime_phase = 1												# 还款阶段(处于第几个月了)
	recent_duetime = datetime.date.today() + datetime.timedelta(days=30)	#下一次还款截止日期
	print "    添加借款记录:recent_duetime = ", recent_duetime
	recent_duemoney = return_money / float(duration)				# 每个月还多少
	print "    添加借款记录:recent_duemoney = ", recent_duemoney
	has_return = 0													# 已经还款
	bad_times = 0													# 不良记录
	# 更新用户信用额度 以及 用户的总资金
	cur_credit = getCredit(username)
	if ( borrow_money > cur_credit):
		print "这次借款的额度不够"
		return False
	else:
		changeCredit(cur_credit - borrow_money,username)
		newMoney = borrow_money + getMoney(username)
		print "    新资金为:",newMoney
		changeMoney(newMoney,username)
	# 在用户的个人数据库中插入数据
	sql = """insert into borrow
					  (borrow_money,return_rate,return_money,borrow_date,duration,
						duetime_phase,recent_duetime,recent_duemoney,has_return,bad_times,aim)
				values('%s',%d,'%s','%s',%d,'%s','%s','%s','%s','%s','%s')
			""" % (borrow_money, int(return_rate), return_money, borrow_date, int(duration),
				   duetime_phase, recent_duetime, recent_duemoney, has_return, bad_times, aim)
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close
	# 获得从数据库刚插入数据的主键
	sql = """
			SELECT MAX(borrow_id) FROM borrow
	    """
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchone()
	conn_user.close
	borrow_id = int(values[0])
	print "刚刚插入数据库的borrow条目主键为:",borrow_id
	# 在总数据库中插入借款记录
	sql = """insert into all_borrow
			  (borrow_id,user_id,username,borrow_money,return_rate,return_money,borrow_date,duration,
				duetime_phase,recent_duetime,recent_duemoney,has_return,bad_times,aim)
		values('%s','%s','%s','%s',%d,'%s','%s',%d,'%s','%s','%s','%s','%s','%s')
	""" %(borrow_id,user_id,username,borrow_money,int(return_rate),return_money,borrow_date,int(duration),
				duetime_phase,recent_duetime,recent_duemoney,has_return,bad_times,aim)
	cur_all.execute(sql)
	conn_all.commit()
	return True


# 删除所有借款记录
def delBorrow(username):
	# 删除主数据库列表
	sql = """
		DELETE FROM all_borrow
		WHERE  username = '%s'
    """ % (username)
	cur_all.execute(sql)
	conn_all.commit()
	# 删除从数据库列表
	sql = """
		DELETE FROM borrow
		"""
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close

# 更改用户的借款记录
def changeBorrow(username,borrow_id,duetime_phase,recent_duetime,recent_duemoney,has_return,bad_times):
	# 更新从数据库列表
	sql = """
		    		UPDATE borrow
		    		SET duetime_phase = '%s',recent_duetime = '%s',
		    			recent_duemoney = '%s',has_return = '%s',bad_times = '%s'
		    		WHERE  borrow_id == '%s'
		        """ % (duetime_phase, recent_duetime, recent_duemoney, has_return, bad_times, borrow_id)
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close
	# 更新主数据库列表
	sql = """
    		UPDATE all_borrow
    		SET duetime_phase = '%s',recent_duetime = '%s',
    			recent_duemoney = '%s',has_return = '%s',bad_times = '%s'
    		WHERE  borrow_id == '%s' AND username == '%s'
        """ % (duetime_phase,recent_duetime,recent_duemoney,has_return,bad_times,borrow_id,username)
	cur_all.execute(sql)
	conn_all.commit()

# 获取用户所有借款记录
def getBorrow(username):
	sql = """
		SELECT * FROM borrow
	"""
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchall()
	conn_user.close
	# 封装数据为字典列表
	results = []
	for item in values:
		result = {}
		result['borrow_id'] = item[0]
		result['return_money'] = strToFloat(item[3])
		result['borrow_date'] = str(item[4])
		result['duration'] = int(item[5])
		result['duetime_phase'] = int(item[6])
		result['recent_duetime'] = str(item[7])
		result['recent_duemoney'] = strToFloat(item[8])
		result['has_return'] = strToFloat(item[9])
		result['bad_times'] = int(item[10])
		result['aim'] = item[11]
		results.append(result)
	if (len(results) == 0):
		results.append({})
	return results

# 获取用户单个借款记录(用于计算)
def getOneBorrow(username,borrow_id):
	sql = """
		SELECT * FROM borrow
		WHERE borrow_id = '%s'
	""" %(borrow_id)
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	item = cur_user.fetchone()
	conn_user.close
	# 封装数据为字典列表
	result = {}
	result['borrow_id'] = item[0]
	result['return_money'] = float(item[3])
	result['borrow_date'] = str(item[4])
	result['duration'] = int(item[5])
	result['duetime_phase'] = int(item[6])
	result['recent_duetime'] = str(item[7])
	result['recent_duemoney'] = float(item[8])
	result['has_return'] = float(item[9])
	result['bad_times'] = int(item[10])
	result['aim'] = item[11]
	return result

# 获取所有用户的所有借款记录(并且减去已经被投资金额)
def getAllBorrowForShow():
	sql = """
		SELECT borrow_id,tmp.username as username,aim,borrow_money,duration,return_rate,all_lend,borrow_last,credit_level
		FROM
		(
			SELECT borrow_id,username,aim,borrow_money,duration,return_rate,SUM(lend_money) as all_lend,(borrow_money - SUM(lend_money)) as borrow_last
			FROM
				(
					SELECT borrow_id,borrow_lend.username as username,aim,borrow_money,borrow_lend.duration as duration,return_rate,lend_id,lend_money
					FROM
						(
							SELECT borrow_id,username,aim,borrow_money,duration,return_rate,lend_id
							FROM all_borrow LEFT OUTER JOIN lend_borrow USING (username,borrow_id)
						) as borrow_lend
						LEFT OUTER JOIN
						all_lend USING (lend_id)
				)
			GROUP BY borrow_id,username
		) as tmp
		LEFT OUTER JOIN
		users USING (username)
		WHERE borrow_last > 0 OR borrow_last IS NULL
	"""
	cur_all.execute(sql)
	values = cur_all.fetchall()
	# 封装数据为字典列表
	results = []
	for item in values:
		result = {}
		if (item[7] == None):
			result['borrow_last'] = float(item[3])
		else:
			result['borrow_last'] = float(item[7])
		result['borrow_id'] = int(item[0])
		result['username'] = str(item[1])
		result['aim'] = item[2]
		result['duration'] = int(item[4])
		result['return_rate'] = int(item[5])
		result['level'] = int(item[8])
		results.append(result)
	if (len(results) == 0):
		results.append({})
	return results



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




# 添加还款记录
def addRecord(username,borrow_id,ahead_days,money_differ,duemoney,actual_return):
	sql = """
    		insert into return_record
    			  (borrow_id,ahead_days,money_differ,duemoney,actual_return)
    		values('%s','%s','%s','%s','%s')
    		""" % (borrow_id,ahead_days,money_differ,duemoney,actual_return)
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close

# 查询用户所有的还款记录
def getRecord(username):
	sql = """
        	SELECT * FROM return_record
        """
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchall()
	conn_user.close
	# 封装为数据
	results = []
	for item in values:
		result = {}
		result['borrow_id'] = item[0]
		result['ahead_days'] = item[1]
		result['money_differ'] = strToFloat(item[2])
		result['duemoney'] = strToFloat(item[3])
		result['actual_return'] = strToFloat(item[4])
		results.append(result)
	return results


# 获取用户的违约总次数
def getTotalBadTimes(username):
	sql = """
    		SELECT SUM(bad_times) FROM borrow
    	"""
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchone()
	conn_user.close
	if(values == (None,)):
		print values
		return '0'
	else:
		return int(values[0])



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------


# 添加投资
def addLend(user_id,username,lend_money,lend_rate,duration):
	# 更新用户存款(更新失败说明余额不足)
	money = getMoney(username) - float(lend_money)
	if ( not changeMoney(str(money),username) ):
		print "余额不足"
		return False
	# 计算各种值
	back_money = float(lend_money) * (1 + float(lend_rate)/100)
	lend_date = time.strftime("%Y-%m-%d", time.localtime())
	return_date = datetime.date.today() + datetime.timedelta(days=30*duration)
	isReturn = 0
	# 从数据库的插入
	sql = """
				insert into lend
					  (lend_money,lend_rate,back_money,lend_date,duration,return_date,isReturn)
				values('%s',%d,'%s','%s',%d,'%s',%d)
				""" % (lend_money, lend_rate, back_money, lend_date, duration, return_date, isReturn)
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close
	# 获得从数据库刚插入数据的主键
	sql = """
				SELECT MAX(lend_id) FROM lend
		    """
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchone()
	conn_user.close
	lend_id = int(values[0])
	print "刚刚插入数据库的lend条目主键为:", lend_id
	# 主数据库的插入
	sql = """
			insert into all_lend
				  (lend_id,user_id,username,lend_money,lend_rate,back_money,lend_date,duration,return_date,isReturn)
			values(%d,%d,'%s','%s',%d,'%s','%s',%d,'%s',%d)
			""" % (lend_id,user_id,username,lend_money,lend_rate,back_money,lend_date,duration,return_date,isReturn)
	cur_all.execute(sql)
	conn_all.commit()
	return True

# 为某个borrow添加投资
def addLendToBorrow(user_id,username,lend_money,lend_rate,duration,borrow_id,userBeLended):
	# 将lend信息插入lend数据表中
	if ( not addLend(user_id, username, lend_money, lend_rate, duration) ):
		return False
	# 获取刚插入的lend的主键ID
	sql = """
    				SELECT MAX(lend_id) FROM lend
    	  """
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchone()
	conn_user.close
	lend_id = int(values[0])
	# 为借款与投资的关联表插入数据
	sql = """
			insert into lend_borrow
				  (lend_id,username,borrow_id)
			values(%d,%s,%d)
			""" % (lend_id,userBeLended,borrow_id)
	cur_all.execute(sql)
	conn_all.commit()
	return True

# 获取用户的所有lend
def getLend(username):
	sql = """
		SELECT * FROM lend
	"""
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	values = cur_user.fetchall()
	conn_user.close
	# 封装数据为字典列表
	results = []
	for item in values:
		result = {}
		result['lend_id'] = item[0]
		result['lend_money'] = float(item[1])
		result['lend_rate'] = int(item[2])
		result['back_money'] = float(item[3])
		result['lend_date'] = str(item[4])
		result['duration'] = int(item[5])
		result['return_date'] = str(item[6])
		result['isReturn'] = int(item[7])
		results.append(result)
	return results

# 修改对应用户,对应lend的还款情况
def changeIsReturn(username,lend_id,isReturn):
	sql = """
    		UPDATE lend
			SET isReturn = %d
			WHERE lend_id == %d;
    	""" % (isReturn, lend_id)
	conn_user = sqlite3.connect("database/%s.db" % (username))
	cur_user = conn_user.cursor()
	cur_user.execute(sql)
	conn_user.commit()
	conn_user.close
	return True


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------



# 按照duration,获取整理后的所有用户所有lend条目(减去已经投资的金额)
def getActualBorrowOrderByDuration():
	sql = """
        SELECT (total_money - total_lend) as total_need,duration,min_rate,max_rate,total_money,total_lend
		FROM
      		(
      		SELECT sum(borrow_money) as total_money,duration,min(return_rate) as min_rate,max(return_rate) as max_rate
			FROM
				(
				SELECT * FROM all_borrow
				WHERE has_return < return_money
				)
			GROUP BY duration
			ORDER BY duration DESC
			)
			LEFT OUTER JOIN
			(
			SELECT sum(lend_money) as total_lend,duration
			FROM
				(
				SELECT * FROM all_lend
				WHERE isReturn == 0
				)
			GROUP BY duration
			ORDER BY duration DESC
			)
			USING (duration)
    """
	cur_all.execute(sql)
	values = cur_all.fetchall()
	results = []
	for item in values:
		result = {}
		if( item[0] == None):
			result['total_need'] = float(item[4])
		else:
			result['total_need'] = float(item[0])
		result['duration'] = int(item[1])
		result['min_rate'] = int(item[2])
		result['max_rate'] = int(item[3])
		result['total_money'] = float(item[4])
		result['total_lend'] = item[5]
		results.append(result)
	return  results

# 按照duration,获取整理后的所有用户所有lend条目(减去已经投资的金额)
def getActualBorrowOrderByRate():
	sql = """
        SELECT (total_money - total_lend) as total_need,return_rate,min_duration,max_duration,total_money,total_lend
		FROM
      		(
      		SELECT sum(borrow_money) as total_money,return_rate,min(duration) as min_duration,max(duration) as max_duration
			FROM
				(
				SELECT * FROM all_borrow
				WHERE has_return < return_money
				)
			GROUP BY return_rate
			ORDER BY return_rate DESC
			)
			LEFT OUTER JOIN
			(
			SELECT sum(lend_money) as total_lend,lend_rate as return_rate
			FROM
				(
				SELECT * FROM all_lend
				WHERE isReturn == 0
				)
			GROUP BY lend_rate
			ORDER BY lend_rate DESC
			)
			USING (return_rate)
    """
	cur_all.execute(sql)
	values = cur_all.fetchall()
	results = []
	for item in values:
		result = {}
		if( item[0] == None):
			result['total_need'] = float(item[4])
		else:
			result['total_need'] = float(item[0])
		result['return_rate'] = int(item[1])
		result['min_duration'] = int(item[2])
		result['max_duration'] = int(item[3])
		result['total_money'] = float(item[4])
		result['total_lend'] = item[5]
		results.append(result)
	return  results

# 获取指定duration的借款列表
def getActualBorrowUseDuration(duration):
	sql = """
		SELECT (total_money - total_lend) as total_need,duration,return_rate,total_money,total_lend
		FROM
      		(
      		SELECT sum(borrow_money) as total_money,return_rate,duration
			FROM
				(
				SELECT * FROM all_borrow
				WHERE duration = %d AND has_return < return_money
				)
			GROUP BY return_rate
			ORDER BY return_rate DESC
			)
			LEFT OUTER JOIN
			(
			SELECT sum(lend_money) as total_lend,lend_rate as return_rate
			FROM
				(
				SELECT * FROM all_lend
				WHERE  duration = %d AND isReturn == 0
				)
			GROUP BY lend_rate
			ORDER BY lend_rate DESC
			)
			USING (return_rate)
	""" %(duration,duration)
	cur_all.execute(sql)
	values = cur_all.fetchall()
	results = []
	for item in values:
		result = {}
		if (item[0] == None):
			result['total_need'] = float(item[3])
		else:
			result['total_need'] = float(item[0])
		result['duration'] = int(item[1])
		result['return_rate'] = int(item[2])
		result['total_money'] = float(item[3])
		result['total_lend'] = item[4]
		results.append(result)
	return results

# 获取指定rate的借款列表
def getActualBorrowUseRate(rate):
	sql = """
		SELECT (total_money - total_lend) as total_need,return_rate,duration,total_money,total_lend
		FROM
      		(
      		SELECT sum(borrow_money) as total_money,return_rate,duration
			FROM
				(
				SELECT * FROM all_borrow
				WHERE return_rate = %d AND has_return < return_money
				)
			GROUP BY duration
			ORDER BY duration DESC
			)
			LEFT OUTER JOIN
			(
			SELECT sum(lend_money) as total_lend,duration
			FROM
				(
				SELECT * FROM all_lend
				WHERE  lend_rate = %d AND isReturn == 0
				)
			GROUP BY duration
			ORDER BY duration DESC
			)
			USING (duration)
	""" %(rate,rate)
	cur_all.execute(sql)
	values = cur_all.fetchall()
	results = []
	for item in values:
		result = {}
		if (item[0] == None):
			result['total_need'] = float(item[3])
		else:
			result['total_need'] = float(item[0])
		result['return_rate'] = int(item[1])
		result['duration'] = int(item[2])
		result['total_money'] = float(item[3])
		result['total_lend'] = item[4]
		results.append(result)
	return results


