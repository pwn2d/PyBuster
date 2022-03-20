import requests
import sys
from colorama import Fore
import colorama
import os
import time
import threading
import ctypes

colorama.init()

subdomains = []
unkowns = []


global words
words = []

def open_list(wordlist):
    counter = 0
    f=open(wordlist, "r", encoding="utf-8")
    for letter in f:
        word = letter.strip("\n")
        words.append(word)
        counter += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Appending To File : {counter}")
        if counter == 5000000:
            break

def send_requests(word):
    global r
    try:
        r = requests.get(f"{args}/{word}")
        if r.status_code == 200:
            subdomains.append(f"{word} {Fore.WHITE}({Fore.MAGENTA}{r.status_code}{Fore.WHITE})")

        elif r.status_code == 204:
            subdomains.append(f"{word} {Fore.WHITE}({Fore.MAGENTA}{r.status_code}{Fore.WHITE})")

        elif r.status_code == 301:
            subdomains.append(f"{word} {Fore.WHITE}({Fore.MAGENTA}{r.status_code}{Fore.WHITE})")

        elif str(r.status_code).startswith("30"):
            subdomains.append(f"{word} {Fore.WHITE}({Fore.MAGENTA}{r.status_code}{Fore.WHITE})")

        elif r.status_code == 404:
            pass

        elif r.status_code == 401:
            print(f"{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}*{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Unauthorized - {word} ({Fore.RED + str(r.status_code) + Fore.RESET})")

        else:
            print(f"Returned Unknown ({Fore.YELLOW + str(r.status_code + Fore.WHITE)}) Word {Fore.LIGHTBLACK_EX}: {Fore.WHITE}({Fore.YELLOW}{word}{Fore.WHITE}){Fore.RESET}")
            unkowns.append(word)
    except:
        pass


def find(domain, speed=0):
    counter = 0
    for word in words:
        thread = threading.Thread(target=send_requests, args=(word,))
        thread.start()
        counter += 1
        time.sleep(float(speed))
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(f"Sending Requests : {counter}/{len(words)} ({r.status_code})")
        except:
            pass

        

    print("\n")
    for subdomain in subdomains:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Found {Fore.LIGHTBLACK_EX}- {Fore.WHITE}{subdomain} ")

    print(f"\n{domain} Subdomain Scan\n")
    print(f"Found {len(subdomains)}/{len(words)} Subdomains")    

def bust(website, wordlist=None):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    }
    print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}*{Fore.LIGHTBLACK_EX}]{Fore.YELLOW} Pinging{Fore.WHITE} {website}{Fore.RESET}")
    r = requests.get(f"{website}", headers=headers)
    if r.status_code == 200:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Website Is Up! ({Fore.MAGENTA + str(r.status_code) + Fore.RESET})")
    elif r.status_code == 204:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Website Is Up! ({Fore.MAGENTA + str(r.status_code) + Fore.RESET})")
    elif r.status_code == 301:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Website Is Up! ({Fore.MAGENTA + str(r.status_code) + Fore.RESET})")
    elif r.status_code == 404:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}-{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Website Returned 404 Not Found, It's Up Though ({Fore.RED + str(r.status_code) + Fore.RESET})")
    elif r.status_code == 401:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}-{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Website Returned 401 Unauthorized, It's Up Though ({Fore.RED + str(r.status_code) + Fore.RESET})")
    else:
        print(f"Returned Unknown ({Fore.YELLOW + str(r.status_code) + Fore.RESET})")
        

    try:
        domain = str(website).split(":")
        domain = str(domain[1]).removeprefix("//")
    except Exception as e:
        print(f"Error, {e}")
    
    if wordlist is None:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Looking For Directories In ({Fore.MAGENTA + domain}{Fore.RESET})")
        paths = []
        wordlists = []
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}*{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Looking For Wordlists 1/3")

        for thing in os.listdir():
            thing = str(thing)
            paths.append(thing)

        
        for object in paths:
            temp = str(object)
            if temp.endswith(".txt"):
                wordlists.append(temp)
        
        for list in wordlists:
            print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Using Wordlist {Fore.MAGENTA}{list}{Fore.RESET} 2/3")
            time.sleep(0.3)
            print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Appending Words To List 3/3")
            open_list(list)

        print(f"{Fore.MAGENTA}Wordlist/s Have {len(words)} Word/s!{Fore.RESET}")
        time.sleep(0.3)
    else:
        open_list(wordlist)

    print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}*{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Sending Requests To {domain}")
    try:
        find(domain, speed)
    except Exception as e:
        print(f"{Fore.RED}Did not input speed value!")

def pybuster():
    global speed
    try:
        website = sys.argv[1]
        wordlist = sys.argv[2]
        speed = sys.argv[3]
        try:
            bust(website, wordlist)
        except:
            bust(website)
    except:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Usage{Fore.LIGHTBLACK_EX}] : {Fore.YELLOW}pybuster {Fore.LIGHTBLACK_EX}[{Fore.YELLOW}website{Fore.LIGHTBLACK_EX}] [{Fore.YELLOW}wordlist{Fore.LIGHTBLACK_EX}] {Fore.LIGHTBLACK_EX}[{Fore.YELLOW}speed{Fore.LIGHTBLACK_EX}]{Fore.RESET}")


pybuster()
