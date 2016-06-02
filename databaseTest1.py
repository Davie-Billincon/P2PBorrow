#coding:utf-8
from service import  *

# print registerCheck(1234)
#
# print getBorrow(1234)

# print getActualBorrowUseDuration(7)


# duetime前,还款<应还
# return_dispatch('1234','1','2016-05-30','100')
# return_dispatch(1234,1,'2016-05-30',100)

# # duetime前,还款<应还
# return_dispatch(1235,2,'2016-6-18',24)
#
# # duetime前,还款>应还
# return_dispatch(1235,3,'2016-06-10',58)
#
# # duetime前,还款 远远> 应还
# return_dispatch(1235,4,'2016-06-10',111)
#
# # duetime后30天内, 还款 = 0
# return_dispatch(1235,5,'2016-08-10',0)

# # duetime后30天内外, 还款>应还
# return_dispatch(1235,6,'2016-09-10',155)
#
# # duetime后30天外, 还款 = 0
# return_dispatch(1232,6,'2016-08-10',0)
#
# # duetime后30天外, 还款>应还
# return_dispatch(1232,7,'2016-08-10',100)
#
# # duetime后30天外, 还款>应还
# return_dispatch(1232,8,'2016-08-10',200)

# print getOneBorrow('1231',1)
# retult =  getOneBorrow('1231',1)
# print retult['aim']
# # print getOneBorrow('admin',1)
# print getOneBorrow('1231',3)

# u = u'中文' #显示指定unicode类型对象u
# str = u.encode('gb2312') #以gb2312编码对unicode对像进行编码
# print str
# # str1 = u.encode('gbk') #以gbk编码对unicode对像进行编码
# str2 = u.encode('utf-8') #以utf-8编码对unicode对像进行编码
# print str2
# # u1 = str.decode('gb2312')#以gb2312编码对字符串str进行解码，以获取unicode
# u2 = str[4:].decode('utf-8')#如果以utf-8的编码对str进行解码得到的结果，将无法还原原来的unicode类型

# print getAllBorrowForShow()

# print getLevelIndexByLevel(22)
# print getLevelMoneyByLevel(67)

changeUserLevelByLevelDiff(1231,22)