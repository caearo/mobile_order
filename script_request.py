#coding:utf-8

# 使用request的方式尝试

import json, time
import requests


def load_cofiguration():
	### Load configuration from local file.
	with open("configure.json", "r") as of:
		conf = json.load(of)

	return conf



def login():
	### Login and get cookie
	### Return: `0,[session, coolie]` if login successes, otherwise `-1, []`

	conf = load_cofiguration()

	# Login param
	data_login = {
		"username":conf["username"],
		"password":conf["password"],
		"vcode":""
	}

	sessLogin = requests.session()

	# Get captcha image and store into file
	headers = {'content-type': 'application/json',
				"Connection": "keep-alive",
				"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
				"Accept-Encoding": "gzip, deflate",
				"Accept-Language": "zh-CN,zh;q=0.9",
}
	captcha = sessLogin.get(conf['url_captcha'], headers = headers)

	with open ('captcha.png', 'wb') as wf:
		wf.write(captcha.content)

	# Read captha
	capCode = raw_input("captcha:")

	# Update param and login
	data_login["vcode"] = str(capCode)

	# Login
	resp = sessLogin.post(
			conf["url_login"],
			cookies = requests.utils.dict_from_cookiejar(captcha.cookies),
			data = data_login)
	

	b_login = False
	try:
		if -1 != resp.headers["refresh"].split(";")[1].find(conf["keyword_login"]):
			b_login = True
	except Exception, e:
		#raise e
		pass

	if b_login:
		# Get order page.
		resp_order = sessLogin.get( conf["url_order"] )

		if 200 == resp.status_code:
			if -1 != resp_order.text[:500].find(conf["keyword_order"]):
				print "Loged in."
				return 0, sessLogin, captcha.cookies

				resp_task = sessLogin.get( conf["url_getseq"] )
				print len(resp_task.text)
	else:
		print "Login failed."
		return -1, 0, 0



def get_seq(session, url_getseq, cookies):
	resp = session.get(url_getseq)#, cookies = requests.utils.dict_from_cookiejar(cookies))
	#print '* Getting SEQ res:', resp.status_code
	string = resp.text
	if -1 != string.encode("utf-8").find("请先完成进行中的任务"):
		return -2
	pos = string.find("SEQ")
	if -1 != pos:
		pos = string.find("value", pos)
		if -1 != pos:
			seq = string[pos+len("value=\"\""):pos+18]
			return seq

	with open("test.html", 'w') as wf:
		wf.write(string)
	return


def get_task(session, url_gettask, cookies, SEQ):
	param = {"id":"5", "count":"1", "SEQ":SEQ} # id:1,2,5,4,11,12,13,15
	assert loginRes == 0
	resp = session.post(url_gettask,
			data = param)
			#allow_redirects = False)
	#print '* Getting task res:', resp.status_code
	pos = resp.text.encode('utf-8').find("tip_message('")
	print resp.text.encode('utf-8')[pos:pos+60]
	if -1 != resp.text.encode('utf-8').find("最近24小时"):
		return -2
	if -1 != resp.text.encode('utf-8').find("慢点来"):
		print "请求太快，少许等待..."
		time.sleep(2)
		return -1
	if -1 != resp.text.encode('utf-8').find("成功获取订单"):
		return 0
	else:
		return -1


def test():
	string = '''
	{"data":"<div class=\"modal-dialog\">\n    <form class=\"form-horizontal validator\" method=\"post\" action=\"get_tasks\">\n        <div class=\"modal-content\">\n            <div class=\"modal-header\">\n                <button type=\"button\" class=\"close\" data-dismiss=\"modal\"><span aria-hidden=\"true\">&times;<\/span><span\n                            class=\"sr-only\">Close<\/span><\/button>\n                <h4 class=\"modal-title\">\u83b7\u53d6\u4ee3\u5145\u8ba2\u5355<\/h4>\n            <\/div>\n            <div class=\"modal-body\">\n                <div class=\"form-group\">\n                    <label class=\"col-sm-2 control-label\" for=\"count\">\u4ee3\u5145\u7c7b\u578b<\/label>\n                    <div class=\"col-sm-10\">\n                        <select id=\"id\" name=\"id\" class=\"form-control input-large input-inline\">\n                            <option value='1' >100\u5143<\/option><option value='2' selected>200\u5143<\/option><option value='5' >300\u5143<\/option><option value='6' >500\u5143<\/option><option value='3' >\u5fae\u4fe1500\u4ee5\u5185\u8ba2\u5355<\/option><option value='4' >\u5fae\u4fe1500\u4ee5\u4e0a\u8ba2\u5355<\/option>\n                        <\/select>\n                    <\/div>\n                <\/div>\n                <div class=\"form-group\">\n                    <label class=\"col-sm-2 control-label\" for=\"count\">\u6570\u91cf<\/label>\n                    <div class=\"col-sm-10\">\n                        <select id=\"count\" name=\"count\" class=\"form-control input-large input-inline\">\n                            <option value='1' >1<\/option>\n                        <\/select>\n                    <\/div>\n                <\/div>\n\n                <div class=\"form-group\">\n                    <label class=\"col-sm-2 control-label\" for=\"count\">\u81ea\u52a8\u5f39\u7a97<\/label>\n                    <div class=\"col-sm-10\">\n                        <label class=\"form-control-static\">\n                            <input type=\"checkbox\" name=\"auto\" value=\"1\"  \/>\n                            \u63a5\u5355\u6210\u529f\u540e\uff0c\u81ea\u52a8\u5f39\u51fa\u626b\u7801\u7a97\u53e3\n                        <\/label>\n                    <\/div>\n                <\/div>\n\n            <\/div>\n            <input type=\"hidden\" name=\"SEQ\" value=\"1523358175\" \/>\n            <div class=\"modal-footer\">\n                <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\u53d6\u6d88<\/button>\n                <button type=\"submit\" class=\"btn btn-info\" id=\"submit\">\u7acb\u523b\u83b7\u53d6<\/button>\n            <\/div>\n        <\/div>\n    <\/form>\n<\/div>","type":"dialog"}
	'''
	print type(string.decode('utf-8'))
	string = string.decode('utf-8')
	pos = string.find("SEQ")
	print pos
	if -1 != pos:
		pos = string.find("value", pos)
		print pos
		if -1 != pos:
			print pos
			print string[ pos+len("value=\"") : string.find("\"", pos+len("value=\"")) ]

if __name__ == '__main__':
	import os
	INTERVAL = 2.1
	conf = load_cofiguration()
	loginRes, session, cookies = login()
	assert loginRes == 0
	for i in range(200):
		print "进行第%d次尝试..." % i
		seq = get_seq(session, conf["url_getseq"], cookies)
		time.sleep( INTERVAL )
		res = get_task(session, conf["url_gettask"], cookies, seq)
		if 0 == res:
			print "成功，请前往订单完成操作"
			break
		elif -2 == res:
			print "请先完成进行中的任务"
			break

		time.sleep( INTERVAL )
		os.system("afplay /System/Library/Sounds/Tink.aiff")
	
	os.system("say 'Quit, please check your order.'")

	#test()
