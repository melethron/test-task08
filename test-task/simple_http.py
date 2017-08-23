#!/usr/bin/env python
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from tinydb import TinyDB, Query
from validate_email import validate_email


DB = TinyDB('db.json')

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/hello':
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("<html><body><h1>Hello page</h1></body></html>".encode("utf-8"))
		else:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("<html><body><h1>hi!</h1></body></html>".encode("utf-8"))

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length).decode(encoding="utf-8", errors="strict") # <--- Gets the data itself
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		print (post_data)
		post_dict = dict(item.split('=') for item in post_data.split('&'))
		print (post_dict)
		#print(DB.all())
		for item in post_dict:
			#print(post_dict[item])
			if validate_date(post_dict[item]):
				date_post = post_dict[item]
			elif validated_number(post_dict[item]):
				phone_post = post_dict[item]
			elif validate_email(post_dict[item]):
				email_post = post_dict[item]
			else:
				text_post = post_dict[item]
		print(date_post)
		print(phone_post)
		print(email_post)
		#print(text_post)

def validated_number(phone_number):
	if len(phone_number) != 16:
		return False
	for i in range(1, 16):
		if i in [2, 6, 10, 13]:
			if phone_number[i] != ' ':
				return False
	if phone_number[0:2] != '+7':
		return False
	return True

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        try:
        	datetime.datetime.strptime(date_text, '%d-%m-%Y')
        	return True
       	except ValueError:
       		return False
        return False
    return True

def run(server_class=HTTPServer, handler_class=MyServer):
	server_address = ('', 8000)
	httpd = server_class(server_address, handler_class)
	print("Starting http server...")
	httpd.serve_forever()

run()