#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://mf.91yunma.cn")

element = driver.find_element_by_id("username")
print type(element)
element.send_keys("13175064086")


element = driver.find_element_by_name("password")
print type(element)
element.send_keys("123456mf")

if driver.find_element_by_id("captcha").is_displayed():
    print(driver.find_element_by_id("captcha").is_displayed())
    while True:
       val = raw_input("input CreateCheckCode:") 
       if val and len(val)>0:
           print val
           driver.find_element_by_id("vcode").send_keys(val)
           break

driver.find_element_by_id("btnLogin").click()

print 'Login done.'


# get cookie
list_cookies=driver.get_cookies()  # 获取selenium cookie
cookie={}
# 转换dict，准备在requests中调用
for item in list_cookies:
    cookie[item['name']]=item['value']
print cookie


from selenium.webdriver.common.by import By

nButton = 0
import time
while nButton == 0:
	driver.get("http://mf.91yunma.cn/admin/qpay/mytasks")
	try:
		element = driver.find_element_by_partial_link_text('获取500面值订单')
		print element.text,'-- 检测到'

		if len(element.text):
			element.click()
			print element.text,'-- click'
			driver.implicitly_wait(.4) # seconds

			# 获取SEQ
			element = driver.find_element_by_name('SEQ')
			print 'find seq element'
			seq = element.get_attribute('value')
			print 'get SEQ.', seq
			
			driver.implicitly_wait(1) # seconds
			btn = driver.find_element_by_id('submit')
			print 'Btn get'
			time.sleep(.5)
			driver.implicitly_wait(5) # seconds
			btn.click()
			print "Final btn click"
			break

	except Exception, e:
		print Exception
		print e.msg
	finally:
		#nButton = 1
		driver.implicitly_wait(1) # seconds


def get_order(cookie, param):
	url='http://mf.91yunma.cn/admin/qpay/mytasks'
	header={
	    'Connection':'keep-alive',
	    'Cache-Control':'max-age=0',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Upgrade-Insecure-Requests':'1',
	    'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1;Trident/5.0)',
	    'Accept-Encoding':'gzip, deflate',
	    'Accept-Language':'zh-CN,zh;q=0.8',}
	response=requests.get(url,headers=header,cookies=cookie)
