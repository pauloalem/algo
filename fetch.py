#!/usr/bin/python
# -*- coding: utf-8
import argparse
import os
from os.path import join

import requests
from lxml.html import fromstring


parser = argparse.ArgumentParser(description="Downloads files from coursera servers for offline viewing")
parser.add_argument("course", metavar="c", type=str, help="The chosen course", choices=['algo','nlp','gametheory','pgm','crypto'])
parser.add_argument("email", metavar="e", type=str, help="Email registered on coursera")
parser.add_argument("password", metavar="p", type=str, help="Password registered on coursera")

args = parser.parse_args()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
COURSE = args.course
AUTH_URL = "https://www.coursera.org/%s/auth/auth_redirector?type=login&subtype=normal&email=&minimal=true" % COURSE

def get_authenticated_session(email, password):
    session = requests.session()
    payload = session.get(AUTH_URL, allow_redirects=True)
    credentials = {'email': email, 'password': password, "login": "login"}
    response = session.post(payload.url, data=credentials, allow_redirects=True)
    if response.ok == False:
        print "deu merda"
        raise Exception("Could not authenticate")
    return session


class Section(object):
    def __init__(self, section):
        self.section = section

    def get_section_dir(self):
        return join(BASE_DIR, self.section)

    def create_section_dir(self):
        return os.mkdir(join(BASE_DIR, self.section))

    def save(self, name, data):
        if os.path.exists(self.get_section_dir()) == False:
            self.create_section_dir()
        f = open(join(self.get_section_dir(), name), "wb")
        return f.write(data)




session = get_authenticated_session(email=args.email,
                                    password=args.password)
materials_page = session.get("https://www.coursera.org/algo/lecture/index")
page = fromstring(materials_page.text)
content = zip(page.cssselect(".list_header"),
              page.cssselect("ul.item_section_list"))
for header, item_section_list in content:
    section = Section(header.text)
    for li in item_section_list.findall("li"):
        title = li.find('a').text
        for a in li.findall('div/a'):
            href = a.get('href')
            if '.ppt' in href:
                ext = ".ppt"
            elif '.pdf' in href:
                ext = ".pdf"
            elif 'subtitles' in href:
                ext = ".txt"
            elif '.mp4' in href:
                ext = ".mp4"
            else:
                ext = ".chucknorris"
            print "downloading %s(%s)..." % (title + ext, href)
            data = session.get(href).content
            section.save(title + ext, data)
