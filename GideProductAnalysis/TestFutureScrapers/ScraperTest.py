from lxml.html import fromstring
from itertools import cycle
from torrequest import TorRequest
#import traceback
import requests 
import random
import stem
#import cookielib

import socks
import socket
from stem.util import term

SOCKS_PORT = 9050

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
socket.socket = socks.socksocket
'''
def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print (term.format(line, term))

tor_process = stem.process.launch_tor_with_config(
    tor_cmd = '/Applications/TorBrowser.app/Contents/MacOS/Tor/tor.real',
    config = {'SocksPort': str(SOCKS_PORT),
               'ExitNodes': '{ru}',},
    #init_msg_handler = print_bootstrap_lines,
)
'''
'''
tr=TorRequest(password='HelloGide')
response= tr.get('http://ipecho.net/plain')
print("New Ip Address",response.text)
#print requests.get("http://icanhazip.com").text
'''

text_file = open("instaurl.txt", "r")
lines = text_file.read().split('\n')
text_file.close()

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

#Lets make 5 requests and see what user agents are used 
count = 0
for i in lines:
    count += 1
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    url = 'https://instagram.com/'+i
    response = requests.get(url,headers=headers)
    html = response.content
    print("Done " + str(count) )

# Choose a proxy port, a control port, and a password. 
# Defaults are 9050, 9051, and None respectively. 
# If there is already a Tor process listening the specified 
# ports, TorRequest will use that one. 
# Otherwise, it will create a new Tor process, 
# and terminate it at the end.
    
# Specify HTTP verb and url.
#resp = tr.get('http://google.com')
#print(resp.text)

# Send data. Use basic authentication.
#response= tr.get('https://www.amazon.ca')
#print ("New Ip Address",response.text)

# Change your Tor circuit,
# and likely your observed IP address.##
#tr.reset_identity()

# TorRequest object also exposes the underlying Stem controller 
# and Requests session objects for more flexibility.
'''
print(type(tr.ctrl))            # a stem.control.Controller object
tr.ctrl.signal('CLEARDNSCACHE') # see Stem docs for the full API

socket.socket = socks.socksocket

socket.socket = socks.socksocket

print(type(tr.session))         # a requests.Session object
c = cookielib.CookieJar()
tr.session.cookies.update(c)    # see Requests docs for the full API
'''
