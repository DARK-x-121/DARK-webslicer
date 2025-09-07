import aiohttp
import asyncio
import requests
import os
import time
import json
from colorama import Fore, init
from tqdm import tqdm
from prettytable import PrettyTable

init(autoreset=True)


BANNER = f"""{Fore.MAGENTA}
██████╗  █████╗ ██████╗ ██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██████╔╝███████║██████╔╝█████╔╝ 
██╔═══╝ ██╔══██║██╔═══╝ ██╔═██╗ 
██║     ██║  ██║██║     ██║  ██╗
╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝
{Fore.CYAN}Dark WebSlicer v2.0 - By Amit @ DARK
{Fore.YELLOW}DARK Community: Educating Hackers Since 2025
"""


DEFAULT_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "' OR '1'='1 --",
    "' UNION SELECT null,null,null --",
    "javascript:alert('OpenRedirect')",
    "http://evil.com"
]


async def fetch(session, url, payload=None, param="q"):
    try:
        if payload:
            target_url = f"{url}?{param}={payload}"
        else:
            target_url = url
        async with session.get(target_url, timeout=5) as response:
            return target_url, await response.text(), response.status, str(response.headers)
    except:
        return target_url, "", 0, ""


async def check_xss(session, url, payload, results):
    full_url, text, status, _ = await fetch(session, url, payload)
    if payload in text:
        results.append({
            "type": "XSS",
            "payload": payload,
            "url": full_url,
            "severity": "High"
        })


async def check_sqli(session, url, payload, results):
    full_url, text, status, _ = await fetch(session, url, payload)
    errors = ["mysql", "sql syntax", "you have an error in your sql"]
    if any(err in text.lower() for err in errors):
        results.append({
            "type": "SQL Injection",
            "payload": payload,
            "url": full_url,
            "severity": "Critical"
        })


async def check_redirect(session, url, payload, results):
    full_url, text, status, headers = await fetch(session, url, payload)
    if status in [301, 302] and payload in headers:
        results.append({
            "type": "Open Redirect",
            "payload": payload,
            "url": full_url,
            "severity": "Medium"
        })


async def check_csrf(session, url, results):
    full_url, text, status, headers = await fetch(session, url)
    if "csrf" not in text.lower():
        results.append({
            "type": "CSRF Protection Missing",
            "url": full_url,
            "severity": "Medium"
        })


async def dir_bruteforce(session, url, results):
    dirs = ["admin", "backup", "login", "test", "db", "config"]
    for d in dirs:
        full_url = f"{url}/{d}"
        target_url, text, status, _ = await fetch(session, full_url)
        if status == 200:
            results.append({
                "type": "Directory Found",
                "url": full_url,
                "severity": "Info"
            })


async def run_scanner(url, param="q"):
    print(BANNER)
    print(Fore.CYAN + "[*] Starting DARK WebSlicer Scan...\n")
    
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        
        for payload in DEFAULT_PAYLOADS:
            tasks.append(check_xss(session, url, payload, results))
            tasks.append(check_sqli(session, url, payload, results))
            tasks.append(check_redirect(session, url, payload, results))
        
        
        tasks.append(check_csrf(session, url, results))

        
        tasks.append(dir_bruteforce(session, url, results))
        
        await asyncio.gather(*tasks)
    
    display_results(results)
    save_results(url, results)
    return results


def display_results(results):
    table = PrettyTable()
    table.field_names = ["Vulnerability", "Severity", "Payload/Dir", "URL"]
    for r in results:
        table.add_row([r['type'], r['severity'], r.get('payload', 'N/A'), r['url']])
    
    print(Fore.YELLOW + "\nScan Results:\n")
    print(table)


def save_results(url, results):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename_json = f"webslicer_results_{timestamp}.json"
    
    data = {
        "target_url": url,
        "scan_time": timestamp,
        "results": results,
        "author": "Amit @ DARK",
        "powered_by": "GlitchWareX"
    }
    
    with open(filename_json, "w") as f:
        json.dump(data, f, indent=4)
    
    print(Fore.GREEN + f"\n[+] Results saved as {filename_json}")


def main():
    os.system("clear")
    print(BANNER)
    print(Fore.CYAN + "[1] Start Website Scan")
    print(Fore.CYAN + "[2] Exit\n")
    choice = input(Fore.WHITE + "Choose an option: ")
    
    if choice == "1":
        url = input(Fore.WHITE + "Enter Target URL (e.g., http://testphp.vulnweb.com): ")
        asyncio.run(run_scanner(url))
    else:
        print(Fore.RED + "Exiting... Stay in the shadows 🌑")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Scan interrupted by user.")