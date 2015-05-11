#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
author:jaffer tsao
time:2014-6-5
function:readme
'''
import httplib2
import urllib2
import urllib
import socket
from urllib import urlopen
from string import replace,find,lower
from httplib import HTTPException
import time
import threading



#huo qu lengthgth 115.182.70.49
class IPisOK(object):
	def __init__(self,ip,list,port):
		self.ip = ip
		self.list = list
		self.port = ['80','8080','8081','81','9080','3128']
	
	def getIndex(self):
		for i in range(len(self.port)):
			try:
				h = httplib2.Http(timeout=0.15)
				res,con = h.request('http://'+self.ip+':'+self.port[i],'GET')
			except:
				return 
			a1 = con.find('Not Found')
			a2 = con.find('Bad Request')
			a3 = con.find('Forbidden')
			a4 = con.find('Service Unavailable')
			a5 = con.find('403')
			a6 = con.find('Apache 2 Test Page')
			a7 = con.find('It works!')
			a8 = con.find('IIS')
			a9 = con.find('Directory Listing Denied')
			a10 = con.find('Internal Server Error')
			a11 = con.find('Welcome to nginx!')
			a12 = con.find('502 Bad Gateway')
			a13 = con.find('<title>Apache Tomcat')
			if a1 != -1 or a2 != -1 or a3 != -1 or a4 != -1 or a5 != -1 or a6 != -1 or a1 != -1 or a8 != -1 or a9 != -1 or a10 != -1 or a11 != -1 or a12 != -1 or a13 != -1:
				return
			if len(con) == 0:
				return
			
			j = con.find('Index of /')
			if j != -1:
				list_ok.append(self.ip+':'+self.port[i])
				self.list.append(self.ip+':'+self.port[i])
			list_ok.append(self.ip+':'+self.port[i])
		

class IP(object):
	def __init__(self,ip_s,ip_e):
		self.ip_s = ip_s
		self.ip_e = ip_e
		
	def getlength(self):
		list_s = self.ip_s.split('.')
		list_e = self.ip_e.split('.')
		length = (int(list_e[0])-int(list_s[0]))*255*255*255 + (int(list_e[1])-int(list_s[1]))*255*255 + (int(list_e[2])-int(list_s[2]))*255 + int(list_e[3])-int(list_s[3])
		print length
		return length
	
	def ipadd1(self,ip):
		list = ip.split('.')
		if int(list[0])>254 or int(list[1])>255 or int(list[2])>255 or int(list[3])>255:
			return -1
		if int(list[3]) == 255:
			list[3] = '0'
			if int(list[2]) == 255:
				list[2] = '0'
				if int(list[1]) == 255:
					list[1] = '0'
					t0 = int(list[0]) + 1
					list[0] = str(t0)
				t1 = int(list[1]) + 1
				list[1] = str(t1)
			t2 = int(list[2]) + 1
			list[2] = str(t2)
		t3 = int(list[3]) + 1
		list[3] = str(t3)
		return '.'.join(list)
	
	def ipaddnum(self,ip,num):
		list = ip.split('.')
		if int(list[0])>254 or int(list[1])>255 or int(list[2])>255 or int(list[3])>255:
			return -1
		temp3 = int(list[3]) + num
		if temp3 > 255:
			temp3_left = temp3%256
			temp2 = temp3/256
			temp2 = int(list[2])+temp2
			if temp2 > 255:
				temp2_left = temp2%256
				temp1 = temp2/256
				temp1 = int(list[1])+temp1
				if temp1 > 255:
					temp1_left = temp1%256
					temp0 = temp1/256
					temp0 = int(list[0])+temp0
					list[0] = str(temp0)
					list[1] = str(temp1_left)
				else:
					list[1] = str(temp1)
				list[2] = str(temp2_left)
			else:
				list[2] = str(temp2)
			list[3] = str(temp3_left)
		else:
			list[3] = str(temp3)
			
			
		return '.'.join(list)
			
		
 
 
 
	   
'''
def main(ip_start,ip_end,port):
	#ip = ip_start
	IPs = IP(ip_start,ip_end)
	length = IPs.getlength()
	print length
	if length <=0:
		return  
	ip = ip_start
	for i in range(length):
		print "IP:"+ip
		isIP=IPisOK(ip,list,port)
		isIP.getIndex()
		ip = IPs.ipadd1(ip)
		print list
	print 'dictory list leak:'
	print list
'''  
class MyThread(threading.Thread):  
	def __init__(self,ip_start,ip_end,port):  
		threading.Thread.__init__(self)
		self.ip_start = ip_start
		self.ip_end = ip_end
		self.port = port
		  
	def run(self):  
		IPs = IP(self.ip_start,self.ip_end)
		length = IPs.getlength()
		print length
		print self.ip_start
		print self.ip_end
		if length <=0:
			return  
		ip = self.ip_start
		for i in range(length):
			isIP=IPisOK(ip,list,self.port)
			isIP.getIndex()
			ip = IPs.ipadd1(ip)
			#print list
		#print 'dictory list leak:'
		#print list 

'''def main(ip_start,ip_end,port):   
	mthread = MyThread(ip_start,ip_end,port)
 '''   
   
if __name__ == '__main__': 
	ip_start=raw_input('input start IP:')
	ip_end=raw_input('input a end IP:')
	port = raw_input('input a port(common is 80):(now you can input anything,it is not use this port)')
	thread_num = raw_input('input number of thread:')
	global list
	global list_ok
	list_ok = []
	list = []
	threads = []
	IPa = IP(ip_start,ip_end)
	length = IPa.getlength()
	eachthread = int(length)/int(thread_num)
	left = int(length)%int(thread_num)
	ip = ip_start					  
	print IPa.ipaddnum(ip, 1*int(eachthread))
	for i in range(0,int(thread_num)):
		t=MyThread(IPa.ipaddnum(ip, i*int(eachthread)),IPa.ipaddnum(ip, (i+1)*int(eachthread)),port)
		threads.append(t)
	if left > 0:
		t=MyThread(IPa.ipaddnum(ip, i*int(eachthread)),IPa.ipaddnum(ip, (i+1)*int(eachthread)),port)
		threads.append(t)
		for i in range(0,int(thread_num)+1):
			threads[i].start()
		for i in range(0,int(thread_num)+1):
			threads[i].join()
	else:
		for i in range(0,int(thread_num)):
			threads[i].start()
		for i in range(0,int(thread_num)):
			threads[i].join()
	print 'website you can visit:'
	print list_ok
	print len(list_ok)
	print 'dictory list leak:'
	print list
	raw_input('OK\n')
	
