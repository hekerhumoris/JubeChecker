import ssl
import socket
import argparse
import os
import sys
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
import datetime
import datetime
today = datetime.datetime.now()
today = today.strftime("%Y-%m-%d %H:%M:%S")
from time import sleep
from rich.console import Console
from prettytable import PrettyTable
import subprocess
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
import csv

COLORS = {\
"black":"\u001b[30;1m",
"red": "\u001b[31;1m",
"green":"\u001b[32m",
"yellow":"\u001b[33;1m",
"blue":"\u001b[34;1m",
"magenta":"\u001b[35m",
"cyan": "\u001b[36m",
"white":"\u001b[37m",
"yellow-background":"\u001b[43m",
"black-background":"\u001b[40m",
"cyan-background":"\u001b[46;1m",
"BOLD":"\033[1m"
}

table = PrettyTable()
table.field_names = ["Kategori", "Parameter", "Result", "POC"]
table.align["Kategori"] = "l"
table.align["Parameter"] = "l"
# table.add_row(["Penggunaan HTTPS", "Matikan HTTP", 25, "Jakarta"])

def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text

class Loader:
    def __init__(self, desc=colorText(f"[[white]][[[cyan]]{today}[[white]]] [[[yellow]]info[[white]]] Proses Pengujian..."), timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        # self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        # print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


def show_logo():
    f  = open("resources/logo.txt","r")
    ascii = "".join(f.readlines())
    print(colorText(ascii))


def add_protocol(frontend_url):
    if not frontend_url.startswith("http"):
        frontend_url = f"http://{frontend_url}"
    return frontend_url


def clear():
    cols = get_terminal_size((80, 20)).columns
    print("\r" + " " * cols, end="", flush=True)


def title(title):
    print(colorText(f"\n[[white]][[[green]]+[[white]]][[white]] {title} [[white]]"))


def show_result_table():
    print(colorText(f"\n[[white]][[[blue]]*[[white]]][[white]] Summary Pengujian [[white]]"))
    print(colorText(f"[[white]]{table}"))


def sub_title(frontend_url, title, true):
    time.sleep(1)
    clear()
    if true == True:
        print(colorText(f"\r[[green]] | [[white]][[[green]]✓[[white]]] {title}"))
        # print(colorText(f"\r[[green]] | [[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[green]]✓[[white]]] {title}"))
    else:
        print(colorText(f"\r[[green]] | [[white]][[[red]]X[[white]]] {title}"))
        # print(colorText(f"\r[[green]] | [[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[red]]X[[white]]] {title}"))


def mitigate(frontend_url, title):
    time.sleep(1)
    clear()
    print(colorText(f"\r[[green]] | [[white]][[[cyan]]![[white]]] Cara mitigasi:"))
    print(colorText(f"\r[[green]] | [[white]]\t- {title}"))
    # print(colorText(f"\r[[green]] | [[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[cyan]]✓[[white]]] Cara mitigasi -> [[cyan]]{title}"))
        

def run_server(port):
    os.system('python3 -m http.server ' + str(port) + ' >/dev/null 2>&1 &')
    

def create_clickjacking_file(domain):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', domain)
    file_name = 'clickjacking-result/' + text.replace(' ', '').lower() + '.html'
    file_content = '<html><body>\n'
    file_content += '<iframe sandbox="allow-modals allow-popups allow-forms allow-same-origin allow-scripts" src="' + domain + '" style="display:block; position:fixed; width:100%; height:100%; z-index:1000; top:0; left:0; opacity:0.5;"></iframe>\n'
    file_content += '</body></html>'
    with open(file_name, 'w') as f:
        f.write(file_content)
    return file_name


def get_params():
    frontend_url = input(colorText("[[blue]][Frontend URL][[white]] Please input Frontend URL : "))
    api_url = input(colorText("[[cyan]][API URL][[white]] Please input API URL : "))
    token = input(colorText("[[yellow]][Token][[white]] Please input Token : "))
    checking = input(colorText("[[green]][Checking Type][[white]] Please input Checking type [c]/[s]/[a] : "))
    return frontend_url, api_url, token, checking


def pwnxss(domain, frontend_url):
    print(colorText(f"\r[[green]] | [[white]][[[cyan]]*[[white]]] Harap tunggu. Sedang menyiapkan tool PwnXSS... (https://github.com/pwn0sec/PwnXSS)"))
    # print(colorText(f"\r[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[cyan]]*[[white]]] Harap tunggu. Sedang menyiapkan tool PwnXSS... (https://github.com/pwn0sec/PwnXSS)"))
    time.sleep(5)
    clear()
    dirb_options = ["python3", "third-party/PwnXSS/pwnxss.py", "-u", domain]
    subprocess.call(dirb_options)
    print(colorText(f"\n[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[green]]✓[[white]]] Scanning selesai. Melanjutkan pengujian..\n"))


def checking_https(frontend_url_protocol, frontend_url):
    title('Pengujian HTTPS')
    with Loader():
        try:
            time.sleep(2)
            response = requests.get(frontend_url_protocol)
            if response.history:
                sub_title(frontend_url, "Sudah mematikan HTTP", True)
                sub_title(frontend_url, "Sudah menggunakan SSL", True)
                table.add_row(["Penggunaan HTTPS", "Matikan HTTP", "✓", "-"])
                table.add_row(["Penggunaan HTTPS", "Implementasikan SSL", "✓", "-"])
            else:
                sub_title(frontend_url, f"Belum mematikan HTTP -> [[red]][POC] {frontend_url_protocol}", False)
                sub_title(frontend_url, f"Belum menggunakan SSL", False)
                table.add_row(["Penggunaan HTTPS", "Matikan HTTP", "X", "-"])
                table.add_row(["Penggunaan HTTPS", "Implementasikan SSL", "X", "-"])
        except:
            sub_title(frontend_url, f"Domain gagal diakses", False)
            

def checking_csp(frontend_url_protocol,frontend_url):
    title('Pengujian Content Security Policy')
    with Loader():
        try:
            time.sleep(2)
            response = requests.get(frontend_url_protocol)
            if 'Content-Security-Policy' in response.headers:
                if "script-src 'none'" in response.headers['Content-Security-Policy'] or "'self'" in response.headers['Content-Security-Policy']:
                    csp = response.headers['Content-Security-Policy']
                    sub_title(frontend_url, f"Content-Security-Policy : {csp}", True)
                    sub_title(frontend_url, f"XSS Tidak Berpotensi tereksekusi", True)
                    table.add_row(["Konfigurasi Headers", "Implementasikan CSP", "✓", "-"])
                    return True
                else:
                    sub_title(frontend_url, f"XSS Berpotensi tereksekusi", False)
                    mitigate(frontend_url, 'https://portswigger.net/web-security/cross-site-scripting/content-security-policy')
                    table.add_row(["Konfigurasi Headers", "Implementasikan CSP", "X", "-"])
                    return False
            else:
                sub_title(frontend_url, f"Content-Security-Policy tidak ditemukan", False)
                sub_title(frontend_url, f"XSS Berpotensi tereksekusi", False)
                mitigate(frontend_url, 'https://portswigger.net/web-security/cross-site-scripting/content-security-policy')
                table.add_row(["Konfigurasi Headers", "Implementasikan CSP", "X", "-"])
                return False
        except:
            sub_title(frontend_url, f"Domain gagal diakses", False)
            return True


def checking_x_frame_options(frontend_url_protocol,frontend_url):
    title('Pengujian X-Frame-Options')
    with Loader():
        try:
            time.sleep(2)
            response = requests.get(frontend_url_protocol)
            x_frame_options = response.headers.get('X-Frame-Options')
            if x_frame_options == 'DENY' or x_frame_options == 'SAMEORIGIN':
                sub_title(frontend_url, f"Content-Security-Policy : {x_frame_options}", True)
                sub_title(frontend_url, f"Clickjacking Tidak Berpotensi tereksekusi", True)
                table.add_row(["Konfigurasi Headers", "Implementasikan opsi Secure X-Frame", "✓", "-"])
            else:
                sub_title(frontend_url, f"Content-Security-Policy : {x_frame_options}", False)
                run_server(8000)
                file = create_clickjacking_file(frontend_url_protocol)
                sub_title(frontend_url, f"Clickjacking Berpotensi tereksekusi -> [[red]][POC] http://localhost:8000/{file}", False)
                mitigate(frontend_url, 'https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html')
                table.add_row(["Konfigurasi Headers", "Implementasikan opsi Secure X-Frame", "X", "-"])
        except:
            sub_title(frontend_url, f"Domain gagal diakses", False)


def checking_directory_listing(domain, frontend_url):
    title('Pengujian Directory Listing')
    nextExploit = input(colorText(f"\r[[green]] | [[white]][[[yellow]]?[[white]]] Lakukan scanning directory? y/n (Proses ini akan memerlukan waktu beberapa menit) : "))
    # nextExploit = input(colorText(f"\r[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[cyan]]?[[white]]] Lakukan scanning directory? y/n (Proses ini akan memerlukan waktu beberapa menit) : "))
    if nextExploit == 'y':
        nextExploit = input(colorText(f"\r[[green]] | [[white]][[[yellow]]?[[white]]] Pilih tools [1]gobuster | [2]dirb : "))
        if nextExploit == '1':
            print(colorText(f"\r[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[cyan]]*[[white]]] Harap tunggu. Sedang menyiapkan tool gobuster"))
            time.sleep(5)
            clear()
            try:
                cmd = ['gobuster', 'dir', '-u', domain, '-w', 'wordlists/directory_only_one.small.txt', '-s', '200', '-b', '', '-t', '10']
                subprocess.call(cmd)
                print(colorText(f"\n[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[green]]✓[[white]]] Scanning selesai. Melanjutkan pengujian..\n"))
            except:
                print(colorText(f"\n[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[red]]![[white]]] Scanning gagal dijalankan. Melanjutkan pengujian..\n"))
            table.add_row(["Konfigurasi Web Server", "Nonaktifkan Directory Listing", "Manual", "-"])
        else:
            print(colorText(f"\r[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[cyan]]*[[white]]] Harap tunggu. Sedang menyiapkan tool dirb"))
            time.sleep(5)
            clear()
            try:
                cmd = ['dirb', domain, 'wordlists/directory_only_one.small.txt', '-f', '-r']
                subprocess.call(cmd)
                print(colorText(f"\n[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[green]]✓[[white]]] Scanning selesai. Melanjutkan pengujian..\n"))
            except:
                print(colorText(f"\n[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[red]]![[white]]] Scanning gagal dijalankan. Melanjutkan pengujian..\n"))
            table.add_row(["Konfigurasi Web Server", "Nonaktifkan Directory Listing", "Manual", "-"])


def compliance_checker(frontend_url_protocol, frontend_url):
    checking_https(frontend_url_protocol, frontend_url)
    result = checking_csp(frontend_url_protocol,frontend_url)
    if result == False:
        time.sleep(1)
        clear()
        nextExploit = input(colorText(f"\r[[green]] | [[white]][[[yellow]]?[[white]]] Exploitasi XSS lebih lanjut? y/n (Proses ini akan memerlukan waktu beberapa menit) : "))
        # nextExploit = input(colorText(f"\r[[white]][[[cyan]]{today}[[white]]] [[[yellow]]{frontend_url}[[white]]] [[[cyan]]?[[white]]] Exploitasi XSS lebih lanjut? y/n (Proses ini akan memerlukan waktu beberapa menit) : "))
        if nextExploit == 'y':
            pwnxss(frontend_url_protocol, frontend_url)
    checking_x_frame_options(frontend_url_protocol,frontend_url)
    checking_directory_listing(frontend_url_protocol,frontend_url)
    

show_logo()
# frontend_url, api_url, token, checking = get_params()
frontend_url = 'msklg.com'
api_url = 'a'
token = 'a'
checking = 'c'

if checking == 'c':
    print(colorText(f"[[green]][*][[white]] Frontend URL: {frontend_url}"))
    print(colorText(f"[[green]][*][[white]] Started: {today}"))
    compliance_checker(add_protocol(frontend_url), frontend_url)
    show_result_table()
elif checking == 's':
    print(f"[*] Start Security Checking -> {today}\n")
    # security_checker(add_https(frontend_url), add_https(api_url), token)
elif checking == 'a':
    print(f"[*] Start All Checking -> {today}\n")
    # all_checker(add_https(frontend_url), add_https(api_url), token)
else :
    print("Checking Type Invalid!")
    exit()