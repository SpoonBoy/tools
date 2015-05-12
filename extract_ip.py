from urllib2 import urlopen
from pprint  import pprint

import argparse
import re
import socket
import threading


def ping_task(url):
    try:
        print(url + " : " + socket.gethostbyname(url))
    except socket.error:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="URL from which you want to extract ip")

    try:
        args = parser.parse_args()
    except IOError as e:
        parser.error(e)
        return false

    if args.url:
        if args.url.startswith("http://"):
            url = args.url
        else:
            url = "http://" + args.url
        html = urlopen(url).read()
        pattern = r'([a-z\-_]+\.){1,3}[a-z]+'
        regex = re.compile(pattern, re.IGNORECASE)
        matches = []
        for match in regex.finditer(html):
            if not ( match.group().endswith("html")      or
                     match.group().endswith("jpg")       or
                     match.group().endswith("gif")       or
                     match.group().endswith("xml")       or
                     match.group().endswith("css")       or
                     match.group().endswith("js")        or
                     match.group().endswith("do")        or
                     match.group().endswith("get")       or
                     match.group().endswith("json")      or
                     match.group().endswith("paper")     or
                     match.group().endswith("container") or
                     match.group().endswith("x")         or
                     match.group().endswith("jspa")      or
                     match.group().endswith("asp")       or
                     match.group().endswith("init")      or
                     match.group().endswith("BCL")       or
                     match.group().endswith("Width")     ):
                matches.append(match.group())

        matches = set(matches)
        matches = list(matches)

        threads = []
        for i in matches:
            thr = threading.Thread(target=ping_task, args=(i,))
            threads.append(thr)
            thr.start()

    else:
        print("there is no url given")
        print("""Usage :
        extract_ip www.cisco.com""")


if __name__ == "__main__":
    main()
