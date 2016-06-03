# coding:utf-8
import time
import datetime
from database import *



# ----------------------------------------------------------------------------------------------------
# 信用评级算法部分
# ----------------------------------------------------------------------------------------------------



# 交易数据对信用的更改(频次很高,每次查询信用都会调用)
def changeCreditUseDeal():
	print "service - changeCreditUseDeal:每次获取信用时,都会先调用这个方法来调整信用"
	# 访问其他数据,进行处理
	# 传出 username , 去访问第3方提供的网络接口, 获取该用户的信用权值
	# 使用权值更改信用


# detial填写完后,初始化信用的算法
def countCredit(username):
	print "service - countCredit:依据detial计算信用模块----------------------------------------------------"
	partDetail = getPartDetail(username)
	print "service - countCredit:    用户的基本详情为:",partDetail
	lastDetail = getLastDetail(username)
	print "service - countCredit:    用户的其他详情为:",lastDetail
	levelUp = 0
	# 开始处理详情中获得的数据了
	spare_money = partDetail['spare_money']
	levelUp += getLevelUpByUsemoney(spare_money)
	print "service - countCredit:    依据用户可用余额修改信用等级:",spare_money,levelUp
	salary = partDetail['salary']
	levelUp += getLevelUpBySalary(salary)
	print "service - countCredit:    依据用户每月工资修改信用等级:",salary,levelUp
	work = partDetail['work_status_id']
	levelUp += getLevelUpByWork(work)
	print "service - countCredit:    依据用户就业状态修改信用等级:",work,levelUp
	# 计算完毕重置信用
	print "service - countCredit:    得到的信用奖励为:",levelUp
	changeUserLevelByLevelDiff(username,levelUp)

# detial填写完后,使用认证初始化信用的接口
def countCreditWithCheck(username,oldValues,newValues):
	print "service - countCreditWithCheck:得到新旧认证信息,计算该信用"
	# 若旧认证为none(也就是第一次注册时),设定旧认证数据包全为否
	if (oldValues == None):
		oldValues = {}
		oldValues['IDCheck'] = 0
		oldValues['videoCheck'] = 0
		oldValues['eduCheck'] = 0
		oldValues['phoneCheck'] = 0
		oldValues['studyCheck'] = 0
		oldValues['cardCheck'] = 0
	# 计算新旧认证信息以及他们的差值
	oldLevelUp = getLevelUpByCheckResult(oldValues)
	newLevelUp = getLevelUpByCheckResult(newValues)
	levelDiff = newLevelUp - oldLevelUp
	print "service - countCreditWithCheck:    依据check获得的信用加分差为:",levelDiff
	changeUserLevelByLevelDiff(username,levelDiff)

# 每次有还款插入时,调用这个方法进行调整信用
def changeCreditWhenReturn(username,ahead_days,money_differ,duemoney,actual_return):
	 print "处理上述传入的还款信息,给出新信用"
	 levelUp = getLevelUpByRecord(ahead_days,money_differ,duemoney,actual_return)
	 changeUserLevelByLevelDiff(username, levelUp)

# 每次用户投资时,调用这个方法进行信用调整
def changeCreditWhenLend(username):
	levelUp = 2
	changeUserLevelByLevelDiff(username, levelUp)

# 每次用户投资回款时,调用这个方法进行信用调整
def changeCreditWhenRecive(username):
	levelUp = 2
	changeUserLevelByLevelDiff(username, levelUp)


# 依据level值返回等级，小于等于0为0级
def getLevelIndexByLevel(credit_level):
	if (1 and  credit_level <=0):
		return 0
	elif (credit_level >=1 and credit_level <=35):
		return 1
	elif (credit_level >=36 and credit_level <=60):
		return 2
	elif (credit_level >=61 and credit_level <=85):
		return 3
	elif (credit_level >=86 and credit_level <=110):
		return 4
	elif (credit_level >=111 and credit_level <=135):
		return 5
	elif (credit_level >=136 and 1):
		return 6

# 依据level返回高等级的钱数
def getLevelMoneyByLevel(credit_level):
	if (1 and credit_level <= 0):
		return 0
	elif (credit_level >= 1 and credit_level <= 35):
		return 2000.0
	elif (credit_level >= 36 and credit_level <= 60):
		return 3000.0
	elif (credit_level >= 61 and credit_level <= 85):
		return 5000.0
	elif (credit_level >= 86 and credit_level <= 110):
		return 10000.0
	elif (credit_level >= 111 and credit_level <= 135):
		return 15000.0
	elif (credit_level >= 136 and 1):
		return 50000.0


# 依据username和level增值（可以为负）来完成level增加修改和资金增加修改
def changeUserLevelByLevelDiff(username,levelDiff):
	print "service - changeUserLevelByLevelDiff:根据给定levelDiff修改用户信用"
	# 获取新旧Level
	oldLevel = getLevel(username)
	newLevel = oldLevel + levelDiff
	print "service - changeUserLevelByLevelDiff:    新旧level为:",oldLevel,newLevel
	# 获取修旧Level之间的钱差值
	oldMoney = getLevelMoneyByLevel(oldLevel)
	newMoney =  getLevelMoneyByLevel(newLevel)
	moneyDiff = newMoney - oldMoney
	print "service - changeUserLevelByLevelDiff:    新旧level钱差值为:",moneyDiff
	# 修改用户的level和资金
	changeLevel(newLevel,username)
	newCredit_limit = getCredit(username) + moneyDiff
	changeCredit(newCredit_limit,username)



# ----------------------------------------------------------------------------------------------------
# 信用评级算法的算法支持部分
# ----------------------------------------------------------------------------------------------------



# 依据可用余额返回对应等级level
def getLevelUpByUsemoney(useMoney):
	if (1 and useMoney <= 0):
		return 0
	elif (useMoney >= 1 and useMoney <= 500):
		return 0
	elif (useMoney >= 501 and useMoney <= 1000):
		return 3
	elif (useMoney >= 1001 and useMoney <= 3000):
		return 5
	elif (useMoney >= 3001 and useMoney <= 8000):
		return 8
	elif (useMoney >= 8001 and 1):
		return 10

# 依据每月工资返回对应等级的level
def getLevelUpBySalary(salary):
	if (1 and salary <= 0):
		return 0
	elif (salary >= 1 and salary <= 2000):
		return 0
	elif (salary >= 2001 and salary <= 5000):
		return 1
	elif (salary >= 5001 and salary <= 10000):
		return 2
	elif (salary >= 10001 and salary <= 20000):
		return 3
	elif (salary >= 20001 and 1):
		return 5

# 依据工作状态返回对应等级的level
def getLevelUpByWork(work):
	if (work == 1):
		return 3
	elif (work == 2):
		return 2
	elif (work == 3):
		return 0

# 依据认证信息返回level差值
def getLevelUpByCheckResult(valuePackage):
	levelUp = 0
	if ( valuePackage['IDCheck'] == 1):
		levelUp += 10
	if (valuePackage['videoCheck'] == 1):
		levelUp += 10
	if (valuePackage['phoneCheck'] == 1):
		levelUp += 10
	if (valuePackage['studyCheck'] == 1):
		levelUp += 10
	if (valuePackage['cardCheck'] == 1):
		levelUp += 5
	if (valuePackage['eduCheck'] > 0):
		levelUp += valuePackage['eduCheck']
	return levelUp

# 依据还款记录来计算levelUp
def getLevelUpByRecord(ahead_days,money_differ,duemoney,actual_return):
	levelUp = 0
	if (actual_return >= duemoney):
		levelUp += 1
	if ( ahead_days < -15 ):
		levelUp += -2
	return levelUp

# 封装getLend方法,加入回款检测机制
def getLendForShow(username):
	print "service - getLendForShow:遍历用户的所有lend,检查是否需要回款"
	# 获取该用户的所有还款
	results = getLend(username)
	# 获取当前时间
	nowTimeStr = time.strftime("%Y-%m-%d", time.localtime())
	for item in results:
		ahead_days = countDayDiff(item['return_date'],nowTimeStr)		# 获取当前时间, < 0 即当前时间在约定之间之后
		if ( ahead_days <= 0 and item['isReturn'] == 0 ):
			print "service - getLendForShow:    发生回款"
			# 修改封装好的isReturn , 和数据库中的isReturn
			item['isReturn'] = 1
			changeIsReturn(username,item['lend_id'],1)
			# 修改用户的money(增加回款)
			oldMoney = getMoney(username)
			newMoney = oldMoney + item['back_money']
			changeMoney(newMoney,username)
			# 修改用户的信用等级
			changeCreditWhenRecive(username)
	return results



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




# 根据time字符串计算天数差( 结果>0 说明后者比前者早)
def countDayDiff(dueDate,returnDate):
	dueDate_origin =  time.mktime(time.strptime(dueDate,"%Y-%m-%d"))
	returnDate_origin = time.mktime(time.strptime(returnDate,"%Y-%m-%d"))
	dayDiff = (dueDate_origin - returnDate_origin)/(60*60*24)
	return int(dayDiff)

# 还款分发器,根据传入的还款与对应recent_duetime比对,分发还款操作
def return_dispatch(username,borrow_id,return_time,return_money):
	print "return_dispatch:处理还款请求,判断来进行请求分发"

	if (return_money > getMoney(username)):		#还款不能大于现有资金
		print "return_dispatch:    资金不足"
		return False

	borrowItem = getOneBorrow(username, borrow_id)	# 还款也不能大于未还金额
	has_not_return = borrowItem['return_money'] - borrowItem['has_return']
	if (return_money > has_not_return):
		print "return_dispatch:    还款大于未还"
		return False

	print "->数据库查询单个借款条目"
	borrowItem = getOneBorrow(username, borrow_id)  # 还款发生时，从数据库提取该borrow所有数据
	ahead_days = countDayDiff(borrowItem['recent_duetime'],return_time)	# 获取本次还款提前了多少天（提前了为正数

	if( ahead_days >= 0):							#duetime前还款，回调响应函数
		print "return_dispatch:    截止日期前还款"
		if (return_money == 0):						# duetime前还0块是没有任何意义的
			print "return_dispatch:    截止日期前还款 0 元是没有意义的, 跳出->server"
			return
		print "return_dispatch:    将 '截止日前还款' 进行分发,跳转->addRecordBefore"
		addRecordBefore(username, borrow_id, return_time, return_money)

	else:						#duetime后还款，又分为普通duetime后还款,和deadline还款
		if(borrowItem['duration'] > borrowItem['duetime_phase']):
			print "return_dispatch:    将 '截止日后还款+普通逾期' 进行分发,跳转->addRecordAfter"
			addRecordAfter(username, borrow_id, return_time, return_money)
		else:
			print "return_dispatch:    将 '截止日后还款+Deadline逾期' 进行分发,跳转->addRecordAfterDead"
			addRecordAfterDead(username, borrow_id, return_time, return_money)

	return


# 处理 duetime前的还款情况
def addRecordBefore(username, borrow_id, return_time, return_money):
	print "addRecordBefore:'截止日前还款'-------------------------------------------------------"
	print "->数据库查询单个borrow"
	borrowItem = getOneBorrow(username, borrow_id)  						# 还款发生时，从数据库提取该borrow所有数据
	# 计算参数
	print "addRecordBefore:    疯狂的计算 还款条目 的数据"
	ahead_days = countDayDiff(borrowItem['recent_duetime'], return_time)  	# 获取本次还款提前了多少天（提前了为正数）
	duemoney = borrowItem['recent_duemoney']  								# 获取本月应还金额
	actual_return = max(0, min(return_money, duemoney))  					# 本月实际还款金额
	rest_money = return_money - actual_return  								# 还了本月金额后，还剩的可用金额（ >= 0 ）
	money_differ = actual_return - duemoney  								# 还款差值（还少了为负）
	# 打印语句
	print "addRecordBefore:    用户开始还款  username:%s , borrow_id:%s" % (username, borrow_id)
	print "                         还款时，提前天数为:", ahead_days
	print "                         还款时，还款金额:%s  ,  本月应还:%s:" %(return_money, duemoney)
	print "                         还款时，实际还款:%s  ,  还款盈余:%s:" %(actual_return, rest_money)
	# 更新现有资金
	print "addRecordBefore:    计算用户的新余额"
	newMoney = getMoney(username) - actual_return
	print "->数据库插入用户新余额"
	changeMoney(newMoney, username)
	# 更新信用
	print "->server调用插入 还款记录 时的算法"
	changeCreditWhenReturn(username, ahead_days, money_differ, duemoney, actual_return)
	# 插入到数据库中
	print "->数据库插入 还款记录"
	addRecord(username,borrow_id,ahead_days,money_differ,duemoney,actual_return)
	# 回调还款后，对借款条目的更改
	print "addRecordBefore:    插入 还款记录完成 , 回调对借款条目的更改 , 跳转->changeBorrowWhenReturnBefore"
	changeBorrowWhenReturnBefore(username, borrow_id, return_time, duemoney, actual_return, rest_money)

# 处理 duetime前的还款情况
def changeBorrowWhenReturnBefore(username, borrow_id, return_time, duemoney, actual_return, rest_money):
	print "changeBorrowWhenReturnBefore:'截止日前还款'"
	print "->数据库查询单个borrow"
	borrowItem = getOneBorrow(username, borrow_id)  # 还款发生时，从数据库提取该borrow所有数据
	# 需要更新的参数，实际更新值在下面处理
	print "changeBorrowWhenReturnBefore:    疯狂的计算 新借款条目 的数据"
	recent_duetime = ""  							# 新截止日期
	duetime_phase = 0  								# 新还款阶段
	recent_duemoney = 0  							# 新本月应还
	has_return = 0  								# 该借款的全部已还金额
	bad_times = 0  									# 是否有违约
	avg_money = float(borrowItem['return_money']) / float(borrowItem['duration'])
	# 实际处理
	if (actual_return < duemoney):  # 若实际还款 < 应还金额时，截止日期不变，更新应还金额
		print "changeBorrowWhenReturnBefore:    实际还款<应还金额,截止日期不变，更新应还金额 "
		recent_duetime = borrowItem['recent_duetime']
		duetime_phase = borrowItem['duetime_phase']
		recent_duemoney = duemoney - actual_return
	else:  # 还清本月应还时，截止日期往后推30天，更新应还金额
		print "changeBorrowWhenReturnBefore:    实际还款>=应还金额,还清本月应还时,截止日期往后推30天,更新应还金额"
		recent_duetime = datetime.datetime.strptime(borrowItem['recent_duetime'], "%Y-%m-%d").date() \
						 + datetime.timedelta(days=30)
		duetime_phase = borrowItem['duetime_phase'] + 1
		recent_duemoney = avg_money
	has_return = borrowItem['has_return'] + actual_return
	bad_times = borrowItem['bad_times']
	# 打印语句
	print "changeBorrowWhenReturnBefore:    还款后更改借款记录"
	print "    本次还款后，还款时间为：%s" %(return_time)
	print "    本次还款后，本月应还：%s  ,  实际还款：%s" %(duemoney, actual_return)
	print "    本次还款后，新截止为：%s  ,  新应还金额为：%s" %(recent_duetime,recent_duemoney)
	# 插入到数据库中
	print "->数据库将新借款条目更新到数据库中"
	changeBorrow(username, borrow_id, duetime_phase, recent_duetime, recent_duemoney, has_return, bad_times)
	# 若是有剩余还款，则继续开始新一轮还款记录
	if (rest_money > 0):
		print "changeBorrowWhenReturnBefore:    本次还款后，还款还有盈余：%s  ，  将系统性的再次触发还款" % (rest_money)
		addRecordBefore(username, borrow_id, return_time, rest_money)

# 处理 duetime后的还款情况
def addRecordAfter(username, borrow_id, return_time, return_money):
	print "addRecordAfter:'截止日后还款+普通逾期'-------------------------------------------------------"
	print "->数据库查询单个borrow"
	borrowItem = getOneBorrow(username, borrow_id)  						# 还款发生时，从数据库提取该borrow所有数据
	# 计算参数
	print "addRecordAfter:    疯狂的计算 逾期还款 的数据"
	ahead_days = countDayDiff(borrowItem['recent_duetime'], return_time)  	# 获取本次还款提前了多少天（延后了为负数）
	actual_ahead = max(-30, ahead_days)  									# 对一次截止的延后，不能超过30天，所以处理一下ahead_days
	duemoney = borrowItem['recent_duemoney']  								# 获取截止日期月应还金额
	actual_return = 0  														# 由于违约，强制还款为 0 元
	money_differ = actual_return - duemoney  								# 还款差值
	# 打印语句
	print "addRecordAfter:    用户的一次违约  username:%s , borrow_id:%s" % (username, borrow_id)
	print "                       还款时，截止日期为：%s  ,  还款日期为：%s  " % (borrowItem['recent_duetime'], return_time)
	print "                       还款时，违约天数为:%s  ,  实际违约天数为:%s" % (ahead_days,actual_ahead)
	print "                       还款时，截止日前应还:%s" % (duemoney)
	# 更新信用
	print "->server调用插入 还款记录 时的算法"
	changeCreditWhenReturn(username, ahead_days, money_differ, duemoney, actual_return)
	# 插入到数据库中
	print "->数据库插入 还款记录"
	addRecord(username, borrow_id, actual_ahead, money_differ, duemoney, actual_return)
	# 回调还款后，对借款条目的更改
	print "addRecordAfter:    插入 还款记录 完成 , 回调对借款条目的更改 , 跳转->changeBorrowWhenReturnAfter"
	changeBorrowWhenReturnAfter(username, borrow_id, return_time, return_money)

# 处理 duetime后的还款情况
def changeBorrowWhenReturnAfter(username, borrow_id, return_time, return_money):
	print "changeBorrowWhenReturnAfter:'截止日后还款+普通逾期'"
	print "->数据库查询单个borrow"
	borrowItem = getOneBorrow(username, borrow_id)  # 还款发生时，从数据库提取该borrow所有数据
	# 需要更新的参数，实际更新值在下面处理
	print "changeBorrowWhenReturnAfter:    疯狂的计算 逾期还款新borrow 的数据"
	recent_duetime = ""  			# 新截止日期
	duetime_phase = 0  				# 新还款阶段
	recent_duemoney = 0  			# 新本月应还
	has_return = 0  				# 该借款的全部已还金额
	bad_times = 0  					# 是否有违约
	avg_money = float(borrowItem['return_money']) / float(borrowItem['duration'])
	# 实际处理
	recent_duetime = datetime.datetime.strptime(borrowItem['recent_duetime'], "%Y-%m-%d").date() \
					 + datetime.timedelta(days=30)
	duetime_phase = borrowItem['duetime_phase'] + 1
	recent_duemoney = avg_money + borrowItem['recent_duemoney']
	has_return = borrowItem['has_return']
	bad_times = borrowItem['bad_times'] + 1
	# 打印语句
	print "changeBorrowWhenReturnAfter:    还款后更改借款记录"
	print "                                    本次还款后，还款时间为：%s" % (return_time)
	print "                                    本次还款后，旧截止时间为：%s  ,  新截止日期为：%s" % (borrowItem['recent_duetime'], recent_duetime)
	print "                                    本次还款后，新本月应还：%s" % (recent_duemoney)
	# 插入到数据库中
	print "->数据库将新借款条目更新到数据库中"
	changeBorrow(username, borrow_id, duetime_phase, recent_duetime, recent_duemoney, has_return, bad_times)
	# 将还款数据发送到 还款分发器，让他判定回调哪个函数
	print "changeBorrowWhenReturnAfter:    处理完一次违约后,由于更新了新的 截止 ,所以通过分发来分发是否还是逾期"
	print "changeBorrowWhenReturnAfter:    跳转->return_dispatch"
	return_dispatch(username, borrow_id, return_time, return_money)

# 处理 duetime后的还款情况
def addRecordAfterDead(username, borrow_id, return_time, return_money):
	print "addRecordAfterDead:'截止日后还款+deadline逾期'-------------------------------------------------------"
	if(return_money <= 0):
		print "addRecordAfterDead:    逾期deadline而还款为0的操作没有意义,跳出->server"
		return False
	print "->数据库查询单个borrow"
	borrowItem = getOneBorrow(username, borrow_id)  # 还款发生时，从数据库提取该borrow所有数据
	# 计算参数
	print "addRecordAfterDead:    疯狂的计算 逾期还款 的数据"
	ahead_days = countDayDiff(borrowItem['recent_duetime'], return_time)  	# 获取本次还款提前了多少天（延后了为负数）
	actual_ahead = ahead_days  												# 没有30天的限制了,逾期多少就记录多少
	duemoney = borrowItem['recent_duemoney']  								# 获取截止日期月应还金额
	actual_return = return_money  											# 还款也没有上限了,就是还了的金额
	money_differ = actual_return - duemoney  								# 还款差值
	# 打印语句
	print "addRecordAfterDead:    用户的一次deadline违约  username:%s , borrow_id:%s" % (username, borrow_id)
	print "                           还款时，截止日期为：%s  ,  还款日期为：%s  " % (borrowItem['recent_duetime'], return_time)
	print "                           还款时，违约天数为:%s" % (ahead_days)
	print "                           还款时，截止日前应还:%s" % (duemoney)
	# 更新现有资金
	print "addRecordBefore:    计算用户的新余额"
	newMoney = getMoney(username) - actual_return
	print "->数据库插入用户新余额"
	changeMoney(newMoney, username)
	# 更新信用
	print "->server调用插入 还款记录 时的算法"
	changeCreditWhenReturn(username, ahead_days, money_differ, duemoney, actual_return)
	# 插入到数据库中
	print "->数据库插入 还款记录"
	addRecord(username, borrow_id, actual_ahead, money_differ, duemoney, actual_return)
	# 回调还款后，对借款条目的更改
	print "addRecordAfterDead:    插入 还款记录完成 , 回调对借款条目的更改 , 跳转->changeBorrowWhenReturnAfterDead"
	changeBorrowWhenReturnAfterDead(username, borrow_id, return_time, return_money)

# 处理 duetime后的还款情况
def changeBorrowWhenReturnAfterDead(username, borrow_id, return_time, return_money):
	print "changeBorrowWhenReturnAfterDead:'截止日后还款+deadline逾期'"
	print "->数据库查询单个borrow"
	borrowItem = getOneBorrow(username, borrow_id)  # 还款发生时，从数据库提取该borrow所有数据
	# 需要更新的参数，实际更新值在下面处理
	print "changeBorrowWhenReturnAfterDead:    疯狂的计算 deadline逾期 新borrow 的数据"
	recent_duetime = ""  			# 新截止日期
	duetime_phase = 0  				# 新还款阶段
	recent_duemoney = 0  			# 新本月应还
	has_return = 0  				# 该借款的全部已还金额
	bad_times = 0  					# 是否有违约
	# 实际处理
	recent_duetime = borrowItem['recent_duetime']						# 因为是deadline,不推进duetime了
	duetime_phase = borrowItem['duetime_phase']							# 不推进
	recent_duemoney = borrowItem['recent_duemoney'] - return_money		# 还款多少,就减去duemoney多少
	has_return = borrowItem['has_return'] + return_money				# 还款多少,就添加多少的已经还款
	bad_times = borrowItem['bad_times'] + 1								# 因为是逾期还款,依旧增加违约次数
	# 打印语句
	print "changeBorrowWhenReturnAfterDead    deadline还款后更改借款记录"
	print "                                         本次还款后，还款时间为：%s" % (return_time)
	print "                                         本次还款后，旧截止时间为：%s  ,  新截止日期为：%s" % (borrowItem['recent_duetime'], recent_duetime)
	print "                                         本次还款后，新本月应还：%s" % (recent_duemoney)
	# 插入到数据库中
	print "->数据库将新借款条目更新到数据库中"
	changeBorrow(username, borrow_id, duetime_phase, recent_duetime, recent_duemoney, has_return, bad_times)



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------



# 执行用户的所有borrow检查(查看当前有哪一条是未还款的)
def checkAllBorrow(username):
	print "开始检查用户 %s 的所有借款项目" %(username)
	values = getBorrow(username)
	nowTimeStr =  time.strftime("%Y-%m-%d", time.localtime()  )
	for item in values:
		ahead_days = countDayDiff(item['recent_duetime'], nowTimeStr)	# 将item的duedate和现在比较
		print "borrow_id为:%s的借款,  duedate:%s  在  当前:%s  " % (item['borrow_id'], item['recent_duetime'], nowTimeStr)
		if(ahead_days >= 0):
			print "    未逾期"
			continue
		print "    已逾期,需要特殊处理"
		# 处理逾期未还款的borrow条目(添加一条还款记录为:在当前时间,还了0元s)
		return_dispatch(username,item['borrow_id'],nowTimeStr,0)

# 获取用户的所有borrow条目(用于前端展示)
def getBorrowForShow(username):
	checkAllBorrow(username)			#在获取展示数据前,先查看用户是否有逾期未还的款项
	results = getBorrow(username)
	return results