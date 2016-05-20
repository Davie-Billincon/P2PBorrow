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