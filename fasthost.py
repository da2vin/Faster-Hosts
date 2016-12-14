#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
import re
import os
import shutil

hosts_location = os.environ['SYSTEMROOT'] + '\\System32\\drivers\\etc\\hosts'
backup_hosts_location = 'C:\\hosts_backup\\hosts'


def abstract_str(content, start_str, end_str):
    if not content:
        return ''
    res = ''
    if start_str:
        if start_str not in content:
            return res
        else:
            content = content[content.index(start_str) + len(start_str):]
    if end_str:
        if end_str not in content:
            return res
        else:
            res = content[:content.index(end_str)]
    else:
        res = content
    return res


def get_fast_dns(domain):
    try:
        session = requests.session()
        headers = dict()
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        headers["Referer"] = "http://ipaddress.com/"
        headers["Accept-Encoding"] = "gzip, deflate, sdch"
        headers["Accept-Language"] = "zh-CN,zh;q=0.8"
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        session.headers = headers
        response = session.post("http://ipaddress.com/search/", data='host=' + domain)
        return abstract_str(response.content, '<tr><th>IP Address:</th><td>', '</td></tr>')
    except:
        return ''


def backup_hosts():
    try:
        if not os.path.exists('C:\\hosts_backup'):
            os.mkdir('C:\\hosts_backup')
        shutil.copyfile(hosts_location, backup_hosts_location)
        return True
    except:
        return False


def revert_hosts():
    try:
        if not os.path.exists('C:\\hosts_backup\hosts'):
            print 'backup file not exsit!'
        shutil.copyfile(backup_hosts_location, hosts_location)
        os.system('ipconfig /flushdns')
        os.system('ipconfig /displaydns')
        print 'revert hosts success!'
    except:
        print 'revert hosts failed!'


def update_hosts(dns, domain):
    try:
        with open(hosts_location, 'a') as fs:
            fs.write('\n%s     %s' % (dns, domain))
        return True
    except:
        return False


def read_hosts():
    with open(hosts_location, 'r') as fs:
        print fs.read()


def main(domain):
    print 'start to update your hosts...'
    fast_dns = get_fast_dns(domain)
    if not re.match(r'\d+\.\d+\.\d+\.\d+', fast_dns):
        print 'get fast dns failed'
        return False
    print 'get fast dns success:' + fast_dns + ',backup hosts...'
    if not backup_hosts():
        print 'backup host failed'
        return False
    print 'backup host success'
    if not update_hosts(fast_dns, domain):
        print 'update hosts failed'
        return False
    os.system('ipconfig /flushdns')
    os.system('ipconfig /displaydns')
    print 'update host success,now you can fly!'


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'input --google.com or other domain'
        print 'input -read to review your hosts'
        print 'input -revert to revert your hosts'
    elif '--' in sys.argv[1] and '.' in sys.argv[1]:
        main(sys.argv[1][2:])
    elif sys.argv[1] == '-revert':
        revert_hosts()
    elif sys.argv[1] == '-read':
        read_hosts()
    else:
        print 'input --google.com or other domain'
        print 'input -read to review your hosts'
        print 'input -revert to revert your hosts'
