import os
import socket
import ssl
import requests
import whois
import dns.resolver
import threading
import concurrent.futures
from urllib.parse import urlparse
from colorama import init, Fore, Style

init(autoreset=True)

# ================= COLORS =================
COLORS = {
    "RED": Fore.RED,
    "GREEN": Fore.GREEN,
    "BLUE": Fore.BLUE,
    "YELLOW": Fore.YELLOW,
    "MAGENTA": Fore.MAGENTA,
    "CYAN": Fore.CYAN,
    "WHITE": Fore.WHITE,
    "LIGHTRED": Fore.LIGHTRED_EX,
    "LIGHTGREEN": Fore.LIGHTGREEN_EX,
    "LIGHTBLUE": Fore.LIGHTBLUE_EX,
    "LIGHTYELLOW": Fore.LIGHTYELLOW_EX,
    "LIGHTMAGENTA": Fore.LIGHTMAGENTA_EX,
    "LIGHTCYAN": Fore.LIGHTCYAN_EX
}

current_color = Fore.CYAN

def c(t):
    return current_color + t + Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(c("\n[ENTER] Retour"))

def req(url, allow_redirects=False):
    try:
        return requests.get(url, timeout=6, allow_redirects=allow_redirects)
    except:
        return None

def banner():
    print(c(r"""
       ▒█████    ██████  ██▓ ███▄    █ ▄▄▄█████▓   ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
      ▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
      ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
      ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░    ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
      ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░      ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
      ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░        ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
        ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░           ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
      ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░           ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
          ░ ░        ░   ░           ░                          ░ ░      ░ ░      ░  ░      ░  
                                    N = Next Page | P = Previous Page
"""))                                                                                 

# ================= PAGE 1 FUNCTIONS =================
def ip_lookup():
    ip = input(c("IP > "))
    d = req(f"http://ip-api.com/json/{ip}")
    if d:
        j = d.json()
        print(j)
        if j.get("lat"):
            print("MAP:", f"https://www.google.com/maps?q={j['lat']},{j['lon']}")
    pause()

def my_ip():
    print(req("https://api.ipify.org").text)
    pause()

def domain_ip():
    print(socket.gethostbyname(input(c("Domain > "))))
    pause()

def dns_lookup():
    try:
        print(socket.gethostbyname_ex(input(c("Domain > ")))[2])
    except:
        print("ERROR")
    pause()

def whois_lookup():
    try:
        print(whois.whois(input(c("Domain > "))).registrar)
    except:
        print("ERROR")
    pause()

def headers():
    r = req(input(c("URL > ")))
    if r:
        print(r.headers)
    pause()

def status():
    r = req(input(c("URL > ")))
    print(r.status_code if r else "ERROR")
    pause()

def ssl_info():
    host = input(c("Host > "))
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.connect((host, 443))
            cert = s.getpeercert()
            print("Subject  :", cert.get("subject"))
            print("Issuer   :", cert.get("issuer"))
            print("Expires  :", cert.get("notAfter"))
    except Exception as e:
        print("SSL ERROR:", e)
    pause()

def geoip():
    ip = input(c("IP > "))
    print(req(f"http://ip-api.com/json/{ip}").json())
    pause()

def dorks():
    t = input(c("Target > "))
    dork_list = [
        f"site:{t}",
        f"site:{t} filetype:pdf",
        f"site:{t} inurl:admin",
        f"site:{t} inurl:login",
        f"site:{t} intitle:index.of",
        f"\"{t}\" email OR contact",
        f"site:{t} filetype:sql",
        f"site:{t} filetype:env",
    ]
    print(c("\n[GOOGLE DORKS]"))
    for d in dork_list:
        print(f"  https://www.google.com/search?q={requests.utils.quote(d)}")
    pause()

def robots():
    print(req("http://" + input(c("Domain > ")) + "/robots.txt").text[:500])
    pause()

def sitemap():
    print(req("http://" + input(c("Domain > ")) + "/sitemap.xml").text[:500])
    pause()

def title_page():
    r = req(input(c("URL > ")))
    if r:
        try:
            print(r.text.split("<title>")[1].split("</title>")[0])
        except:
            print("NO TITLE")
    pause()

def links():
    r = req(input(c("URL > ")))
    if r:
        for i in r.text.split('"'):
            if i.startswith("http"):
                print(i)
    pause()

def full_ip():
    ip = req("https://api.ipify.org").text
    print(req(f"http://ip-api.com/json/{ip}").json())
    pause()

def domain_parser():
    print(urlparse(input(c("URL > "))).netloc)
    pause()

def port_check():
    host = input(c("Host > "))
    port = int(input(c("Port > ")))
    s = socket.socket()
    s.settimeout(1)
    print("OPEN" if s.connect_ex((host, port)) == 0 else "CLOSED")
    pause()

def reverse_dns():
    try:
        print(socket.gethostbyaddr(input(c("IP > ")))[0])
    except:
        print("ERROR")
    pause()

def ua():
    print(req("https://httpbin.org/user-agent").text)
    pause()

def email_check():
    print("VALID" if "@" in input(c("Email > ")) else "INVALID")
    pause()

def hash_info():
    h = input(c("Hash > "))
    types = {32: "MD5", 40: "SHA1", 56: "SHA224", 64: "SHA256", 96: "SHA384", 128: "SHA512"}
    print(f"Length: {len(h)} → Probably: {types.get(len(h), 'UNKNOWN')}")
    pause()

def isp():
    print(req("http://ip-api.com/json/").json().get("isp"))
    pause()

def os_info():
    print(os.name)
    pause()

def ping():
    os.system("ping -c 1 " + input(c("Host > ")))
    pause()

def subdomain():
    d = input(c("Domain > "))
    for s in ["www", "mail", "ftp", "dev", "api", "test"]:
        print(s + "." + d)
    pause()

def methods():
    url = input(c("URL > "))
    for m in ["GET", "POST", "HEAD"]:
        print(m)
    pause()

def geo_full():
    ip = input(c("IP > "))
    d = req(f"http://ip-api.com/json/{ip}").json()
    print(d)
    if d.get("lat"):
        print("MAP:", f"https://www.google.com/maps?q={d['lat']},{d['lon']}")
    pause()

def extract_domain():
    print(urlparse(input(c("URL > "))).netloc)
    pause()

def settings():
    global current_color
    keys = list(COLORS.keys())
    for i, k in enumerate(keys, 1):
        print(c(f"[{i}] {k}"))
    try:
        current_color = COLORS[keys[int(input("> ")) - 1]]
    except:
        pass
    pause()

def tech_fp(): print(req(input(c("URL > "))).headers.get("Server")); pause()
def ip_rep(): print(req("http://ip-api.com/json/" + input(c("IP > "))).json()); pause()

def dns_adv():
    d = input(c("Domain > "))
    for t in ["A", "MX", "TXT", "NS"]:
        try:
            print(t, dns.resolver.resolve(d, t))
        except:
            print(t, "NONE")
    pause()

def mx_check():
    d = input(c("Domain > "))
    try:
        dns.resolver.resolve(d, "MX")
        print("MX OK")
    except:
        print("NO MX")
    pause()

def sec_headers(): print(req(input(c("URL > "))).headers); pause()
def redirect(): print(req(input(c("URL > ")), allow_redirects=True).url); pause()
def expand(): print(req(input(c("URL > "))).url); pause()
def pass_strength(): print("STRONG" if len(input(c("Pass > "))) > 10 else "WEAK"); pause()

def user_check():
    u = input(c("User > "))
    for s in ["github.com", "twitter.com", "reddit.com"]:
        print(s + "/" + u)
    pause()

def net_sum(): print(os.name, req("https://api.ipify.org").text); pause()

def geo_map():
    ip = input(c("IP > "))
    d = req("http://ip-api.com/json/" + ip).json()
    print(f"https://www.google.com/maps?q={d.get('lat')},{d.get('lon')}")
    pause()

def http_full():
    url = input(c("URL > "))
    for m in ["GET", "POST"]:
        try:
            print(m, req(url).status_code)
        except:
            print(m, "ERR")
    pause()

def sub_enum():
    d = input(c("Domain > "))
    for s in ["www", "mail", "api", "dev", "test"]:
        print(s + "." + d)
    pause()

def asn(): print(req("http://ip-api.com/json/" + input(c("IP > "))).json().get("as")); pause()
def zone(): print("ZONE CHECK"); pause()
def tech_stack(): print(req(input(c("URL > "))).headers); pause()

def email_mx():
    d = input(c("Domain > "))
    try:
        dns.resolver.resolve(d, "MX")
        print("MX OK")
    except:
        print("NO MX")
    pause()

def blacklist(): print(req("http://ip-api.com/json/" + input(c("IP > "))).json()); pause()
def geo_full2(): print(req("http://ip-api.com/json/" + input(c("IP > "))).json()); pause()
def meta(): r = req(input(c("URL > "))); print(len(r.text) if r else "ERR"); pause()

def rev_ip():
    try:
        print(socket.gethostbyaddr(input(c("IP > ")))[0])
    except:
        print("ERROR")
    pause()


# ================= PAGE 2 FUNCTIONS =================

# ---- USERNAME TRACKER ULTRA ----
USERNAME_SITES = [
    ("GitHub",           "https://github.com/{}"),
    ("GitLab",           "https://gitlab.com/{}"),
    ("Twitter/X",        "https://twitter.com/{}"),
    ("Instagram",        "https://www.instagram.com/{}"),
    ("TikTok",           "https://www.tiktok.com/@{}"),
    ("Reddit",           "https://www.reddit.com/user/{}"),
    ("YouTube",          "https://www.youtube.com/@{}"),
    ("Pinterest",        "https://www.pinterest.com/{}"),
    ("Twitch",           "https://www.twitch.tv/{}"),
    ("Steam",            "https://steamcommunity.com/id/{}"),
    ("Pastebin",         "https://pastebin.com/u/{}"),
    ("Keybase",          "https://keybase.io/{}"),
    ("Spotify",          "https://open.spotify.com/user/{}"),
    ("SoundCloud",       "https://soundcloud.com/{}"),
    ("Vimeo",            "https://vimeo.com/{}"),
    ("Flickr",           "https://www.flickr.com/people/{}"),
    ("DeviantArt",       "https://www.deviantart.com/{}"),
    ("Medium",           "https://medium.com/@{}"),
    ("HackerNews",       "https://news.ycombinator.com/user?id={}"),
    ("ProductHunt",      "https://www.producthunt.com/@{}"),
    ("Behance",          "https://www.behance.net/{}"),
    ("Dribbble",         "https://dribbble.com/{}"),
    ("Replit",           "https://replit.com/@{}"),
    ("Codepen",          "https://codepen.io/{}"),
    ("HackTheBox",       "https://app.hackthebox.com/users/{}"),
    ("TryHackMe",        "https://tryhackme.com/p/{}"),
    ("DockerHub",        "https://hub.docker.com/u/{}"),
    ("NPM",              "https://www.npmjs.com/~{}"),
    ("PyPI",             "https://pypi.org/user/{}"),
    ("Leetcode",         "https://leetcode.com/{}"),
    ("Codeforces",       "https://codeforces.com/profile/{}"),
    ("AtCoder",          "https://atcoder.jp/users/{}"),
    ("Gravatar",         "https://en.gravatar.com/{}"),
    ("About.me",         "https://about.me/{}"),
    ("Linktree",         "https://linktr.ee/{}"),
    ("Gumroad",          "https://gumroad.com/{}"),
    ("Substack",         "https://substack.com/@{}"),
    ("Mastodon",         "https://mastodon.social/@{}"),
    ("Bluesky",          "https://bsky.app/profile/{}"),
    ("Telegram",         "https://t.me/{}"),
    ("Snapchat",         "https://www.snapchat.com/add/{}"),
    ("Discord",          "https://discord.com/users/{}"),
    ("Fiverr",           "https://www.fiverr.com/{}"),
    ("Freelancer",       "https://www.freelancer.com/u/{}"),
    ("Upwork",           "https://www.upwork.com/freelancers/~{}"),
    ("Ebay",             "https://www.ebay.com/usr/{}"),
    ("Etsy",             "https://www.etsy.com/shop/{}"),
    ("Roblox",           "https://www.roblox.com/user.aspx?username={}"),
    ("Chess.com",        "https://www.chess.com/member/{}"),
    ("Lichess",          "https://lichess.org/@/{}"),
]

def _check_user(site, url_template, username, results):
    url = url_template.format(username)
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        if r.status_code == 200 and username.lower() in r.url.lower():
            results.append((Fore.GREEN + "[FOUND]   " + Style.RESET_ALL, site, url))
        elif r.status_code == 404:
            results.append((Fore.RED + "[NOT FOUND]" + Style.RESET_ALL, site, url))
        else:
            results.append((Fore.YELLOW + f"[{r.status_code}]     " + Style.RESET_ALL, site, url))
    except:
        results.append((Fore.RED + "[ERROR]   " + Style.RESET_ALL, site, url))

def username_tracker():
    username = input(c("Username > ")).strip()
    print(c(f"\n[*] Recherche de '{username}' sur {len(USERNAME_SITES)} plateformes...\n"))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(_check_user, site, url, username, results) for site, url in USERNAME_SITES]
        concurrent.futures.wait(futures)
    found = [r for r in results if "FOUND" in r[0] and "NOT" not in r[0]]
    notfound = [r for r in results if "NOT FOUND" in r[0]]
    other = [r for r in results if r not in found and r not in notfound]
    print(c(f"=== TROUVÉ ({len(found)}) ==="))
    for status, site, url in sorted(found, key=lambda x: x[1]):
        print(f"  {status} {site:<20} {url}")
    print(c(f"\n=== NON TROUVÉ ({len(notfound)}) ==="))
    for status, site, url in sorted(notfound, key=lambda x: x[1]):
        print(f"  {status} {site:<20} {url}")
    if other:
        print(c(f"\n=== INCERTAIN ({len(other)}) ==="))
        for status, site, url in sorted(other, key=lambda x: x[1]):
            print(f"  {status} {site:<20} {url}")
    pause()

# ---- PHONE OSINT ----
def phone_osint():
    phone = input(c("Numéro (ex: +33612345678) > ")).strip()
    print(c("\n[PHONE OSINT]"))
    print(f"  Numverify  : https://numverify.com/v2/validate?number={phone}")
    print(f"  Google     : https://www.google.com/search?q={requests.utils.quote(phone)}")
    print(f"  Truecaller : https://www.truecaller.com/search/fr/{phone.replace('+','')}")
    print(f"  Sync.me    : https://sync.me/search/?number={phone.replace('+','')}")
    pause()

# ---- PORT SCANNER MULTI ----
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 6379, 8080, 8443, 27017]

def _scan_port(host, port, open_ports):
    s = socket.socket()
    s.settimeout(0.5)
    if s.connect_ex((host, port)) == 0:
        open_ports.append(port)
    s.close()

def port_scanner():
    host = input(c("Host > ")).strip()
    print(c(f"\n[*] Scan des ports courants sur {host}...\n"))
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(_scan_port, host, p, open_ports) for p in COMMON_PORTS]
        concurrent.futures.wait(futures)
    if open_ports:
        for p in sorted(open_ports):
            print(Fore.GREEN + f"  [OPEN]  {p}" + Style.RESET_ALL)
    else:
        print("  Aucun port ouvert détecté.")
    pause()

# ---- FULL PORT SCAN (1-1024) ----
def full_port_scan():
    host = input(c("Host > ")).strip()
    try:
        start = int(input(c("Port début (ex: 1) > ")))
        end = int(input(c("Port fin (ex: 1024) > ")))
    except:
        start, end = 1, 1024
    print(c(f"\n[*] Scan {host} ports {start}-{end}...\n"))
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(_scan_port, host, p, open_ports) for p in range(start, end + 1)]
        concurrent.futures.wait(futures)
    for p in sorted(open_ports):
        print(Fore.GREEN + f"  [OPEN]  {p}" + Style.RESET_ALL)
    if not open_ports:
        print("  Aucun port ouvert.")
    pause()

# ---- SUBDOMAIN BRUTEFORCE ----
SUBDOMAIN_LIST = [
    "www","mail","ftp","dev","api","test","admin","portal","vpn","remote",
    "ns1","ns2","mx","smtp","pop","imap","webmail","cpanel","blog","shop",
    "forum","cdn","static","assets","media","img","images","video","app",
    "mobile","m","secure","login","auth","oauth","sso","status","monitor",
    "git","gitlab","jenkins","ci","staging","preprod","prod","demo","beta"
]

def _check_sub(base, sub, found):
    full = f"{sub}.{base}"
    try:
        ip = socket.gethostbyname(full)
        found.append((full, ip))
    except:
        pass

def subdomain_bruteforce():
    domain = input(c("Domain > ")).strip()
    print(c(f"\n[*] Bruteforce subdomains sur {domain}...\n"))
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(_check_sub, domain, s, found) for s in SUBDOMAIN_LIST]
        concurrent.futures.wait(futures)
    for sub, ip in sorted(found):
        print(Fore.GREEN + f"  [FOUND]  {sub:<40} → {ip}" + Style.RESET_ALL)
    if not found:
        print("  Aucun subdomain trouvé.")
    pause()

# ---- SOCIAL MEDIA LINKS ----
def social_links():
    name = input(c("Nom/pseudo > ")).strip()
    platforms = {
        "Facebook":  f"https://www.facebook.com/{name}",
        "Instagram": f"https://www.instagram.com/{name}",
        "Twitter":   f"https://twitter.com/{name}",
        "TikTok":    f"https://www.tiktok.com/@{name}",
        "YouTube":   f"https://www.youtube.com/@{name}",
        "LinkedIn":  f"https://www.linkedin.com/in/{name}",
        "Reddit":    f"https://www.reddit.com/user/{name}",
        "Telegram":  f"https://t.me/{name}",
        "Twitch":    f"https://www.twitch.tv/{name}",
        "GitHub":    f"https://github.com/{name}",
    }
    for p, url in platforms.items():
        print(f"  {p:<12} → {url}")
    pause()

# ---- IP FULL DETAILS ----
def ip_full_details():
    ip = input(c("IP > ")).strip()
    r = req(f"http://ip-api.com/json/{ip}?fields=66846719")
    if r:
        j = r.json()
        for k, v in j.items():
            print(f"  {k:<20}: {v}")
        if j.get("lat"):
            print(f"\n  MAP: https://www.google.com/maps?q={j['lat']},{j['lon']}")
    pause()

# ---- WHOIS FULL ----
def whois_full():
    domain = input(c("Domain > ")).strip()
    try:
        w = whois.whois(domain)
        print(w)
    except Exception as e:
        print("ERROR:", e)
    pause()

# ---- EXIF / META URL ----
def exif_url():
    url = input(c("URL image > ")).strip()
    r = req(url)
    if r:
        print(f"  Content-Type : {r.headers.get('Content-Type')}")
        print(f"  Taille       : {len(r.content)} bytes")
        print(f"  Last-Modified: {r.headers.get('Last-Modified', 'N/A')}")
    pause()

# ---- EMAIL HEADER ANALYZER ----
def email_header_analyzer():
    print(c("Colle tes headers email (ligne vide pour terminer):"))
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    headers_raw = "\n".join(lines)
    import re
    ips = re.findall(r'\d{1,3}(?:\.\d{1,3}){3}', headers_raw)
    print(c("\n[IPs trouvées dans les headers]"))
    for ip in set(ips):
        print(f"  {ip}")
    pause()

# ---- GOOGLE DORKS AVANCÉ ----
def dorks_advanced():
    t = input(c("Target (domaine ou nom) > ")).strip()
    dorks_list = [
        (f"site:{t}", "Index du site"),
        (f"site:{t} filetype:pdf", "PDFs publics"),
        (f"site:{t} filetype:xls OR filetype:xlsx", "Fichiers Excel"),
        (f"site:{t} filetype:sql", "Bases SQL exposées"),
        (f"site:{t} filetype:env OR filetype:log", "Fichiers sensibles"),
        (f"site:{t} inurl:admin OR inurl:panel OR inurl:login", "Pages admin"),
        (f"site:{t} inurl:api OR inurl:v1 OR inurl:v2", "Endpoints API"),
        (f"site:{t} intitle:\"index of\"", "Directory listing"),
        (f"\"{t}\" email OR contact OR @{t}", "Emails associés"),
        (f"site:linkedin.com \"{t}\"", "LinkedIn"),
        (f"site:pastebin.com \"{t}\"", "Pastebin leaks"),
        (f"site:github.com \"{t}\"", "GitHub mentions"),
    ]
    print(c("\n[GOOGLE DORKS AVANCÉ]"))
    for dork, desc in dorks_list:
        url = f"https://www.google.com/search?q={requests.utils.quote(dork)}"
        print(f"  [{desc}]\n  {url}\n")
    pause()

# ---- DNS RECORDS COMPLET ----
def dns_records_full():
    d = input(c("Domain > ")).strip()
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME", "PTR", "SRV"]
    print(c(f"\n[DNS Records complets pour {d}]"))
    for rt in record_types:
        try:
            answers = dns.resolver.resolve(d, rt)
            for ans in answers:
                print(Fore.GREEN + f"  {rt:<8}" + Style.RESET_ALL + f" {ans}")
        except:
            print(Fore.RED + f"  {rt:<8}" + Style.RESET_ALL + " NONE")
    pause()

# ---- REVERSE IP (tous domaines sur même IP) ----
def reverse_ip_domains():
    ip = input(c("IP > ")).strip()
    print(c(f"\n[Reverse IP → domaines sur {ip}]"))
    print(f"  HackerTarget : https://api.hackertarget.com/reverseiplookup/?q={ip}")
    r = req(f"https://api.hackertarget.com/reverseiplookup/?q={ip}")
    if r:
        domains = r.text.strip().split("\n")
        for d in domains[:30]:
            print(f"  → {d}")
    pause()

# ---- HEADER SECURITY SCORE ----
def header_security_score():
    url = input(c("URL > ")).strip()
    r = req(url)
    if not r:
        print("ERROR")
        pause()
        return
    security_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
        "X-XSS-Protection",
    ]
    score = 0
    for h in security_headers:
        if h in r.headers:
            print(Fore.GREEN + f"  [OK]  {h}" + Style.RESET_ALL)
            score += 1
        else:
            print(Fore.RED + f"  [--]  {h}" + Style.RESET_ALL)
    print(c(f"\n  Score: {score}/{len(security_headers)}"))
    pause()

# ---- TECHNOLOGY FINGERPRINT ----
def tech_fingerprint():
    url = input(c("URL > ")).strip()
    r = req(url)
    if not r:
        print("ERROR")
        pause()
        return
    h = r.headers
    body = r.text.lower()
    print(c("\n[TECH FINGERPRINT]"))
    print(f"  Server     : {h.get('Server', 'N/A')}")
    print(f"  X-Powered  : {h.get('X-Powered-By', 'N/A')}")
    print(f"  Via        : {h.get('Via', 'N/A')}")
    cms_signs = {
        "WordPress": "wp-content",
        "Joomla":    "joomla",
        "Drupal":    "drupal",
        "Shopify":   "shopify",
        "Wix":       "wixsite",
        "React":     "react",
        "Vue":       "vue",
        "Angular":   "ng-version",
        "Laravel":   "laravel",
        "Django":    "csrftoken",
    }
    detected = [name for name, sig in cms_signs.items() if sig in body]
    if detected:
        print(f"  CMS/Frameworks : {', '.join(detected)}")
    else:
        print("  CMS/Frameworks : Non détecté")
    pause()

# ---- LEAK CHECK EMAIL ----
def leak_check():
    email = input(c("Email > ")).strip()
    print(c("\n[LEAK CHECK]"))
    print(f"  HaveIBeenPwned : https://haveibeenpwned.com/account/{requests.utils.quote(email)}")
    print(f"  DeHashed       : https://www.dehashed.com/search?query={requests.utils.quote(email)}")
    print(f"  LeakCheck      : https://leakcheck.io/search?query={requests.utils.quote(email)}")
    print(f"  Snusbase       : https://snusbase.com/ (rechercher: {email})")
    pause()

# ---- IP RANGE / CIDR INFO ----
def cidr_info():
    import ipaddress
    cidr = input(c("CIDR (ex: 192.168.1.0/24) > ")).strip()
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        print(f"  Réseau      : {net.network_address}")
        print(f"  Broadcast   : {net.broadcast_address}")
        print(f"  Masque      : {net.netmask}")
        print(f"  Nb d'IPs    : {net.num_addresses}")
        print(f"  Hosts dispo : {net.num_addresses - 2}")
        print(f"  Première IP : {list(net.hosts())[0] if net.num_addresses > 2 else 'N/A'}")
        print(f"  Dernière IP : {list(net.hosts())[-1] if net.num_addresses > 2 else 'N/A'}")
    except Exception as e:
        print("ERROR:", e)
    pause()

# ---- MAC VENDOR LOOKUP ----
def mac_vendor():
    mac = input(c("MAC (ex: AA:BB:CC:DD:EE:FF) > ")).strip().replace(":", "").replace("-", "")[:6]
    r = req(f"https://api.macvendors.com/{mac}")
    print(f"  Vendor: {r.text if r else 'NOT FOUND'}")
    pause()

# ---- URL SHORTENER EXPAND ----
def url_expand():
    url = input(c("Short URL > ")).strip()
    r = requests.get(url, timeout=6, allow_redirects=True)
    print(f"  URL finale : {r.url}")
    print(f"  Status     : {r.status_code}")
    pause()

# ---- PASTEBIN SEARCH ----
def pastebin_search():
    q = input(c("Recherche > ")).strip()
    print(c("\n[PASTEBIN / PASTE SEARCH]"))
    print(f"  Google  : https://www.google.com/search?q=site:pastebin.com+{requests.utils.quote(q)}")
    print(f"  Google  : https://www.google.com/search?q=site:paste.ee+{requests.utils.quote(q)}")
    print(f"  Google  : https://www.google.com/search?q=site:ghostbin.com+{requests.utils.quote(q)}")
    print(f"  Grep.app: https://grep.app/search?q={requests.utils.quote(q)}")
    pause()

# ---- GITHUB SEARCH ----
def github_search():
    q = input(c("Recherche GitHub > ")).strip()
    print(c("\n[GITHUB OSINT]"))
    print(f"  Code    : https://github.com/search?q={requests.utils.quote(q)}&type=code")
    print(f"  Repos   : https://github.com/search?q={requests.utils.quote(q)}&type=repositories")
    print(f"  Users   : https://github.com/search?q={requests.utils.quote(q)}&type=users")
    print(f"  Commits : https://github.com/search?q={requests.utils.quote(q)}&type=commits")
    print(f"  Issues  : https://github.com/search?q={requests.utils.quote(q)}&type=issues")
    pause()

# ---- LINKEDIN SEARCH ----
def linkedin_search():
    name = input(c("Nom complet > ")).strip()
    company = input(c("Entreprise (optionnel) > ")).strip()
    q = f'site:linkedin.com "{name}"' + (f' "{company}"' if company else '')
    print(c("\n[LINKEDIN OSINT]"))
    print(f"  Google  : https://www.google.com/search?q={requests.utils.quote(q)}")
    print(f"  Direct  : https://www.linkedin.com/search/results/people/?keywords={requests.utils.quote(name)}")
    pause()

# ---- GOOGLE MAPS PERSON ----
def gmaps_person():
    name = input(c("Nom/lieu > ")).strip()
    print(f"  https://www.google.com/maps/search/{requests.utils.quote(name)}")
    pause()

# ---- WAYBACK MACHINE ----
def wayback():
    url = input(c("URL > ")).strip()
    domain = urlparse(url).netloc or url
    print(c("\n[WAYBACK MACHINE]"))
    print(f"  Archive  : https://web.archive.org/web/*/{domain}")
    r = req(f"https://archive.org/wayback/available?url={domain}")
    if r:
        j = r.json()
        snap = j.get("archived_snapshots", {}).get("closest", {})
        if snap:
            print(f"  Dernière : {snap.get('timestamp')} → {snap.get('url')}")
        else:
            print("  Aucune archive trouvée.")
    pause()

# ---- SHODAN LINKS ----
def shodan_search():
    q = input(c("IP ou domaine > ")).strip()
    print(c("\n[SHODAN]"))
    print(f"  Host    : https://www.shodan.io/host/{q}")
    print(f"  Search  : https://www.shodan.io/search?query={requests.utils.quote(q)}")
    pause()

# ---- CERT TRANSPARENCY ----
def cert_transparency():
    domain = input(c("Domain > ")).strip()
    print(c("\n[CERTIFICATE TRANSPARENCY]"))
    print(f"  crt.sh  : https://crt.sh/?q={domain}")
    r = req(f"https://crt.sh/?q={domain}&output=json")
    if r:
        try:
            data = r.json()
            names = set()
            for entry in data[:20]:
                names.add(entry.get("name_value", ""))
            for n in sorted(names):
                for line in n.split("\n"):
                    print(f"  → {line.strip()}")
        except:
            print("  Erreur parsing JSON")
    pause()

# ---- CRYPTO WALLET OSINT ----
def crypto_wallet():
    addr = input(c("Adresse wallet > ")).strip()
    print(c("\n[CRYPTO OSINT]"))
    print(f"  BTC Explorer : https://www.blockchain.com/btc/address/{addr}")
    print(f"  ETH Explorer : https://etherscan.io/address/{addr}")
    print(f"  BTC Blockchr : https://blockchair.com/bitcoin/address/{addr}")
    print(f"  ETH Blockchr : https://blockchair.com/ethereum/address/{addr}")
    print(f"  Google       : https://www.google.com/search?q={requests.utils.quote(addr)}")
    pause()

# ---- TOR / ONION CHECK ----
def tor_check():
    ip = input(c("IP à vérifier (Tor exit node?) > ")).strip()
    r = req(f"https://check.torproject.org/torbulkexitlist")
    if r and ip in r.text:
        print(Fore.GREEN + f"  [!] {ip} est un noeud Tor exit !" + Style.RESET_ALL)
    else:
        print(f"  {ip} n'est pas dans la liste Tor exit.")
    pause()

# ---- NETWORK TRACEROUTE ----
def traceroute():
    host = input(c("Host > ")).strip()
    cmd = f"tracert {host}" if os.name == "nt" else f"traceroute -m 15 {host}"
    os.system(cmd)
    pause()

# ---- HTTP RESPONSE FULL ----
def http_response_full():
    url = input(c("URL > ")).strip()
    r = req(url)
    if r:
        print(c("[STATUS]"))
        print(f"  {r.status_code} {r.reason}")
        print(c("\n[HEADERS]"))
        for k, v in r.headers.items():
            print(f"  {k}: {v}")
        print(c(f"\n[BODY] (500 premiers chars)"))
        print(r.text[:500])
    pause()

# ---- ROBOTS & SITEMAP COMBO ----
def robots_sitemap():
    domain = input(c("Domain > ")).strip()
    for path in ["/robots.txt", "/sitemap.xml", "/sitemap_index.xml", "/.well-known/security.txt"]:
        url = f"http://{domain}{path}"
        r = req(url)
        if r and r.status_code == 200:
            print(Fore.GREEN + f"\n[FOUND] {url}" + Style.RESET_ALL)
            print(r.text[:300])
        else:
            print(Fore.RED + f"[NOT FOUND] {url}" + Style.RESET_ALL)
    pause()

# ---- OPEN REDIRECT TEST ----
def open_redirect():
    url = input(c("URL (avec param) > ")).strip()
    payloads = [
        "https://evil.com",
        "//evil.com",
        "/\\evil.com",
        "https:evil.com",
    ]
    print(c("\n[OPEN REDIRECT TEST]"))
    for p in payloads:
        test = f"{url}{requests.utils.quote(p)}"
        print(f"  {test}")
    pause()

# ---- IP BATCH LOOKUP ----
def ip_batch():
    print(c("Entre les IPs (une par ligne, ligne vide pour finir):"))
    ips = []
    while True:
        line = input().strip()
        if not line:
            break
        ips.append(line)
    for ip in ips:
        r = req(f"http://ip-api.com/json/{ip}")
        if r:
            j = r.json()
            print(f"  {ip:<18} | {j.get('country','?'):<15} | {j.get('city','?'):<15} | {j.get('isp','?')}")
    pause()

# ---- OSINT PERSON ----
def osint_person():
    name = input(c("Nom complet > ")).strip()
    print(c(f"\n[OSINT PERSON: {name}]"))
    links = [
        ("Google",       f"https://www.google.com/search?q={requests.utils.quote(name)}"),
        ("LinkedIn",     f"https://www.linkedin.com/search/results/people/?keywords={requests.utils.quote(name)}"),
        ("Twitter",      f"https://twitter.com/search?q={requests.utils.quote(name)}"),
        ("Facebook",     f"https://www.facebook.com/search/top?q={requests.utils.quote(name)}"),
        ("Instagram",    f"https://www.instagram.com/{name.replace(' ','').lower()}"),
        ("Pastebin",     f"https://www.google.com/search?q=site:pastebin.com+\"{requests.utils.quote(name)}\""),
        ("GitHub",       f"https://github.com/search?q={requests.utils.quote(name)}&type=users"),
        ("Pipl",         f"https://pipl.com/search/?q={requests.utils.quote(name)}"),
        ("Spokeo",       f"https://www.spokeo.com/{requests.utils.quote(name)}"),
        ("TruePeopleSearch", f"https://www.truepeoplesearch.com/results?name={requests.utils.quote(name)}"),
    ]
    for site, url in links:
        print(f"  {site:<20} → {url}")
    pause()

# ---- VULNERABILITIES SEARCH ----
def vuln_search():
    target = input(c("Logiciel / CVE > ")).strip()
    print(c("\n[VULNERABILITY SEARCH]"))
    print(f"  NVD    : https://nvd.nist.gov/vuln/search/results?query={requests.utils.quote(target)}")
    print(f"  CVE    : https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={requests.utils.quote(target)}")
    print(f"  Exploit: https://www.exploit-db.com/search?q={requests.utils.quote(target)}")
    print(f"  CVSS   : https://www.cvedetails.com/google-search-results.php?q={requests.utils.quote(target)}")
    pause()

# ---- IOT SEARCH (SHODAN/CENSYS) ----
def iot_search():
    q = input(c("Requête (ex: webcam, router...) > ")).strip()
    print(c("\n[IOT / DEVICE SEARCH]"))
    print(f"  Shodan  : https://www.shodan.io/search?query={requests.utils.quote(q)}")
    print(f"  Censys  : https://search.censys.io/search?resource=hosts&q={requests.utils.quote(q)}")
    print(f"  Fofa    : https://fofa.info/result?qbase64={requests.utils.quote(q)}")
    pause()

# ---- DARKWEB SEARCH ----
def darkweb_links():
    q = input(c("Recherche dark web > ")).strip()
    print(c("\n[DARK WEB SEARCH (via moteurs clearnet)]"))
    print(f"  Ahmia   : https://ahmia.fi/search/?q={requests.utils.quote(q)}")
    print(f"  Torch   : http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/4a1f6b&s={requests.utils.quote(q)}")
    print(f"  Note: Ces liens nécessitent Tor pour les .onion")
    pause()

# ---- MENU PAGE 2 =================
def menu_page2():
    while True:
        clear()
        banner()
        print(c("""

[51]  Username Tracker ULTRA     [61] Header Security Score    [71] Pastebin Search       [81] Osint Personne
[52]  Phone OSINT                [62] Tech Fingerprint Adv     [72] Github Search         [82] Vuln Search (CVE)
[53]  Port Scanner Multi         [63] Leak Check Email         [73] LinkedIn Search       [83] IoT/Device Search
[54]  Full Port Scan (range)     [64] CIDR / IP Range Info     [74] Google Maps Person    [84] Darkweb Search
[55]  Subdomain Bruteforce       [65] MAC Vendor Lookup        [75] Wayback Machine       [85] IP Batch Lookup
[56]  Social Media Links         [66] URL Expand Full          [76] Shodan Links           [86] HTTP Response Full
[57]  IP Full Details            [67] DNS Records Complet      [77] Cert Transparency     [87] Robots+Sitemap Combo
[58]  WHOIS Full                 [68] Reverse IP Domains       [78] Crypto Wallet OSINT   [88] Open Redirect Test
[59]  Exif / Meta URL            [69] Dorks Google Avancé      [79] Tor Exit Node Check   [89] Traceroute
[60]  Email Header Analyzer      [70] Email MX + SPF           [80] Username + Socials    [90] Exit

"""))

        ch = input(c("> "))

        if ch.upper() == "P":
            return

        actions2 = {
            "51": username_tracker,
            "52": phone_osint,
            "53": port_scanner,
            "54": full_port_scan,
            "55": subdomain_bruteforce,
            "56": social_links,
            "57": ip_full_details,
            "58": whois_full,
            "59": exif_url,
            "60": email_header_analyzer,
            "61": header_security_score,
            "62": tech_fingerprint,
            "63": leak_check,
            "64": cidr_info,
            "65": mac_vendor,
            "66": url_expand,
            "67": dns_records_full,
            "68": reverse_ip_domains,
            "69": dorks_advanced,
            "70": email_mx,
            "71": pastebin_search,
            "72": github_search,
            "73": linkedin_search,
            "74": gmaps_person,
            "75": wayback,
            "76": shodan_search,
            "77": cert_transparency,
            "78": crypto_wallet,
            "79": tor_check,
            "80": username_tracker,
            "81": osint_person,
            "82": vuln_search,
            "83": iot_search,
            "84": darkweb_links,
            "85": ip_batch,
            "86": http_response_full,
            "87": robots_sitemap,
            "88": open_redirect,
            "89": traceroute,
            "90": exit,
        }

        if ch in actions2:
            try:
                actions2[ch]()
            except Exception as e:
                print("ERROR:", e)
                pause()


# ================= MENU PAGE 1 =================
def menu():
    while True:
        clear()
        banner()

        print(c("""


[1]  IP Lookup + Maps       [11] Robots                 [21] Hash Info           [31] Tech Fingerprint
[2]  My IP                  [12] Sitemap                [22] ISP                 [32] IP Reputation 
[3]  Domain → IP            [13] Title                  [23] OS Info             [33] DNS Advanced  
[4]  DNS                    [14] Links                  [24] Ping                [34] MX Check 
[5]  WHOIS                  [15] Full IP Info           [25] Subdomains          [35] Security Headers 
[6]  Headers                [16] Domain Parser          [26] HTTP Methods        [36] Redirect Chain
[7]  Status                 [17] Port Check             [27] Geo Full + Maps     [37] URL Expand
[8]  SSL                    [18] Reverse DNS            [28] Extract Domain      [38] Password Strength
[9]  GeoIP                  [19] User-Agent             [29] Settings            [39] Username Check 
[10] Dorks                  [20] Email Check            [30] Exit                [40] Network Summary
[41] Geo Maps Link          [44] IP → ASN               [46] Website Tech Stack  [48] Reverse IP Lookup
[43] Subdomain Enum         [45] DNS Zone Guess         [47] Email MX Validator

"""))

        ch = input(c("> "))

        actions = {
            "1": ip_lookup, "2": my_ip, "3": domain_ip, "4": dns_lookup, "5": whois_lookup,
            "6": headers, "7": status, "8": ssl_info, "9": geoip, "10": dorks,
            "11": robots, "12": sitemap, "13": title_page, "14": links, "15": full_ip,
            "16": domain_parser, "17": port_check, "18": reverse_dns, "19": ua, "20": email_check,
            "21": hash_info, "22": isp, "23": os_info, "24": ping, "25": subdomain, "26": methods,
            "27": geo_full, "28": extract_domain, "29": settings, "30": exit,
            "31": tech_fp, "32": ip_rep, "33": dns_adv, "34": mx_check, "35": sec_headers,
            "36": redirect, "37": expand, "38": pass_strength, "39": user_check, "40": net_sum,
            "41": geo_map, "42": http_full, "43": sub_enum, "44": asn, "45": zone,
            "46": tech_stack, "47": email_mx, "48": rev_ip
        }

        if ch.upper() == "N":
            menu_page2()
            continue
        elif ch.upper() == "A":
            email_check()
            continue
        elif ch.upper() == "B":
            user_check()
            continue
        elif ch.upper() == "C":
            whois_lookup()
            continue
        elif ch.upper() == "D":
            ip_rep()
            continue

        if ch in actions:
            try:
                actions[ch]()
            except Exception as e:
                print("ERROR:", e)
                pause()


if __name__ == "__main__":
    menu()
