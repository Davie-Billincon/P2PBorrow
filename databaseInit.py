#coding:utf-8

import os
import os.path

def delFile(filename):
	targetDir = ""
	file = "database/%s.db" %(filename)
	targetFile = os.path.join(targetDir, file)
	if os.path.isfile(targetFile):
		os.remove(targetFile)

delFile('all')
delFile('1231')
delFile('1232')
delFile('1233')
delFile('1234')
delFile('admin')

from service import  *

# 模拟用户注册
addUser(1231,1231)
addUser(1232,1232)
addUser(1233,1233)
addUser(1234,1234)

# 模拟用户注册后的添加详情,以获得初始化的 信用等级 和 信用额度
valuesPackage = {}
valuesPackage['IDCheck'] = 1
valuesPackage['videoCheck'] = 1
valuesPackage['eduCheck'] = 0
valuesPackage['phoneCheck'] = 0
valuesPackage['studyCheck'] = 0

addDetail(1,1231,"davie",350301,186,2,3,3,3424,3000,7000,4000,300)
countCredit(1231)
countCreditWithCheck(1231,None,valuesPackage)
addDetail(2,1232,"davie",350301,186,2,3,3,3424,3000,7000,4000,300)
countCredit(1232)
countCreditWithCheck(1232,None,valuesPackage)
addDetail(3,1233,"davie",350301,186,2,3,3,3424,3000,7000,4000,300)
countCredit(1233)
countCreditWithCheck(1233,None,valuesPackage)
addDetail(4,1234,"davie",350301,186,2,3,3,3424,3000,7000,4000,300)
countCredit(1234)
countCreditWithCheck(1234,None,valuesPackage)

# 给用户充值
changeMoney(10000,1231)
changeMoney(10000,1232)
changeMoney(10000,1233)
changeMoney(10000,1234)

# changeCredit(3000.34,1231)
# changeCredit(3000.23,1232)
# changeCredit(3000.56,1233)
# changeCredit(3000.80,1234)

addBorrow(1,1231,112,7,3,'投资')
addBorrow(1,1231,300,3,8,'旅游')
addBorrow(1,1231,243,2,12,'学业')
addBorrow(1,1231,345,1,7,'学业')
addBorrow(1,1231,167,4,5,'学业')
addBorrow(1,1231,467,2,16,'购物')
addBorrow(1,1231,342,6,3,'购物')
addBorrow(2,1232,456,7,8,'购物')
addBorrow(2,1232,278,3,12,'购物')
addBorrow(2,1232,387,7,7,'其他')
addBorrow(2,1232,374,3,5,'旅行')
addBorrow(2,1232,467,4,16,'其他')
addBorrow(2,1232,786,7,3,'旅行')
addBorrow(3,1233,967,5,8,'投资')
addBorrow(3,1233,407,5,12,'购物')
addBorrow(3,1233,589,2,7,'购物')
addBorrow(3,1233,768,4,5,'学业')
addBorrow(3,1233,389,5,16,'购物')
addBorrow(3,1233,987,7,3,'学业')
addBorrow(4,1234,947,4,8,'旅行')
addBorrow(4,1234,654,4,12,'购物')
addBorrow(4,1234,286,4,7,'购物')
addBorrow(4,1234,197,3,5,'其他')
addBorrow(4,1234,378,3,16,'其他')
addBorrow(4,1234,245,6,3,'购物')
addBorrow(4,1234,264,7,3,'购物')
addBorrow(4,1234,365,7,3,'其他')


# addLend(1,1231,40,3,8)
# addLend(1,1231,70,2,12)
# addLend(1,1231,100,7,3)
# addLend(1,1231,232,4,7)




