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

from service import  *

# addUser(1231,1231)
# addUser(1232,1232)
# addUser(1233,1233)
# addUser(1234,1234)
#
# addDetail(1,1231,"davie",350301,186,2,3,3,3424,3000,7000,200,300)
# countCredit(1231)
# addDetail(2,1232,"davie",350301,186,2,3,3,3424,3000,7000,200,300)
# countCredit(1232)
# addDetail(3,1233,"davie",350301,186,2,3,3,3424,3000,7000,200,300)
# countCredit(1233)
# addDetail(4,1234,"davie",350301,186,2,3,3,3424,3000,7000,200,300)
# countCredit(1234)

# changeCredit(3000.34,1231)
# changeCredit(3000.23,1232)
# changeCredit(3000.56,1233)
# changeCredit(3000.80,1234)

# changeMoney(10000,1231)
# changeMoney(10000,1232)
# changeMoney(10000,1233)
# changeMoney(10000,1234)

# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)
# addBorrow(2,1232,300,3,7)

# addBorrow(1,1231,300,3,8)
# addBorrow(1,1231,243,2,12)
# addBorrow(1,1231,345,1,7)
# addBorrow(1,1231,167,4,5)
# addBorrow(1,1231,467,2,16)
# addBorrow(1,1231,342,6,3)
# addBorrow(2,1232,456,7,8)
# addBorrow(2,1232,278,3,12)
# addBorrow(2,1232,387,7,7)
# addBorrow(2,1232,374,3,5)
# addBorrow(2,1232,467,4,16)
# addBorrow(2,1232,786,7,3)
# addBorrow(3,1233,967,5,8)
# addBorrow(3,1233,407,5,12)
# addBorrow(3,1233,589,2,7)
# addBorrow(3,1233,768,4,5)
# addBorrow(3,1233,389,5,16)
# addBorrow(3,1233,987,7,3)
# addBorrow(4,1234,947,4,8)
# addBorrow(4,1234,654,4,12)
# addBorrow(4,1234,286,4,7)
# addBorrow(4,1234,197,3,5)
# addBorrow(4,1234,378,3,16)
# addBorrow(4,1234,245,6,3)


# addLend(1,1231,40,3,8)
# addLend(1,1231,70,2,12)
# addLend(1,1231,100,7,3)
# addLend(1,1231,232,4,7)




