import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin # Fondamentale per gestire i link relativi

URL = "http://web-15.challs.olicyber.it/"

def solve_web15():
    print(f"[*] Analisi delle risorse esterne su {URL}...")
    session = requests.Session() # Usiamo una sessione per efficienza
    
    try:
        response = session.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Troviamo tutti i link (CSS) e gli script (JS)
        links = [urljoin(URL, l.get('href')) for l in soup.find_all('link') if l.get('href')]
        scripts = [urljoin(URL, s.get('src')) for s in soup.find_all('script') if s.get('src')]
        
        # Uniamo le liste delle risorse da controllare
        resources = list(set(links + scripts)) # set() rimuove eventuali duplicati
        print(f"[*] Trovate {len(resources)} risorse esterne da ispezionare.")
        
        for res_url in resources:
            print(f"[?] Controllo: {res_url}")
            res_content = session.get(res_url).text
            
            if "flag{" in res_content:
                # Usiamo una regex per estrarre la flag pulita
                import re
                flag = re.search(r"flag\{.*?\}", res_content)
                if flag:
                    print("\n" + "!"*50)
                    print(f"[!] FLAG TROVATA in {res_url}:")
                    print(f"    {flag.group(0)}")
                    print("!"*50 + "\n")
                    return

    except Exception as e:
        print(f"[-] Errore: {e}")

if __name__ == "__main__":
    solve_web15()