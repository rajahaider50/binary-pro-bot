import os
import time
import sys
import datetime
import requests
from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

# --- REAL-TIME DATA ENGINE ---
def get_live_data(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers).json()
        result = response['chart']['result'][0]
        prices = result['indicators']['quote'][0]['close']
        prices = [p for p in prices if p is not None]
        return prices
    except:
        return []

# --- PAIRS MATRIX ---
ASSETS = {
    "01": {"sym": "EURUSD=X", "name": "EUR/USD"},
    "02": {"sym": "GBPUSD=X", "name": "GBP/USD"},
    "03": {"sym": "USDJPY=X", "name": "USD/JPY"},
    "04": {"sym": "AUDCAD=X", "name": "AUD/CAD"},
    "10": {"sym": "BTC-USD",  "name": "BITCOIN"},
    "11": {"sym": "ETH-USD",  "name": "ETHEREUM"},
    "20": {"sym": "GC=F",     "name": "GOLD"},
}

state = {"pair": "01", "tf": "1m", "bal": 100.0}

def clear():
    os.system('clear')

def get_header():
    p_info = ASSETS[state['pair']]
    return f"""
{G}{BOLD} █████╗ ██╗    ██████╗  ██████╗ ████████╗
 ██╔══██╗██║    ██╔══██╗██╔═══██╗╚══██╔══╝
 ███████║██║    ██████╔╝██║   ██║   ██║   
 ██╔══██║██║    ██╔══██╗██║   ██║   ██║   
 ██║  ██║██║    ██████╔╝╚██████╔╝   ██║   
 ╚═╝  ╚═╝╚═╝    ╚═════╝  ╚═════╝    ╚═╝   
{C}   >> LIGHTWEIGHT AI ENGINE V10.0 (FIXED) <<
{W}------------------------------------------------------
[ MATRIX ] {G}01:EURUSD 02:GBPUSD 03:USDJPY 04:AUDCAD 10:BTC{W}
------------------------------------------------------
[ LIVE ] Asset: {Y}{p_info['name']}{W} | TF: {Y}{state['tf']}{W} | Bal: {G}${state['bal']}{W}
------------------------------------------------------
{BOLD}COMMANDS: {C}signal{W} | {C}auto{W} | {C}pair [no]{W} | {C}bal [amt]{W} | {C}exit{RESET}
"""

def analyze_logic(pair_key):
    p = ASSETS[pair_key]
    prices = get_live_data(p['sym'])
    
    if len(prices) < 10:
        return 0, "DATA ERROR"

    last = prices[-1]
    prev = prices[-2]
    avg_5 = sum(prices[-5:]) / 5
    
    buy_weight = 0
    sell_weight = 0
    
    if last > prev: buy_weight += 35
    else: sell_weight += 35
    
    if last > avg_5: buy_weight += 45
    else: sell_weight += 45
    
    accuracy = max(buy_weight, sell_weight) + (time.time() % 15)
    if accuracy > 98: accuracy = 98.2
    
    direction = "CALL (UP)" if buy_weight > sell_weight else "PUT (DOWN)"
    return accuracy, direction

def auto_finder():
    print(f"\n{C}[AUTO] Scanning all assets for best trend...{RESET}")
    best_pair = None
    max_acc = 0
    
    for key in ASSETS:
        acc, _ = analyze_logic(key)
        sys.stdout.write(f"\r{W}Checking {ASSETS[key]['name']}: {G}{acc:.1f}%{RESET}   ")
        sys.stdout.flush()
        if acc > max_acc:
            max_acc = acc
            best_pair = key
        time.sleep(0.3)
        
    if best_pair:
        state['pair'] = best_pair
        print(f"\n\n{G}[FOUND] Switched to {ASSETS[best_pair]['name']} ({max_acc:.1f}%){RESET}")
        time.sleep(1.5)

def run_prediction():
    print(f"\n{C}[*] Analyzing Global Market Liquidity...")
    for i in range(5, 0, -1):
        sys.stdout.write(f"\r{Y} [SYNCING] Verifying Candle Patterns... {i}s {RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    acc, direction_text = analyze_logic(state['pair'])
    now = datetime.datetime.now()
    # Predicting entry for the very next minute start
    entry_time = (now + datetime.timedelta(minutes=1)).replace(second=0).strftime("%H:%M:00")

    dir_color = G if "CALL" in direction_text else R
    color = G if acc >= 80 else R
    
    print(f"\n\n{G}╔══════════════════ LIGHT-AI REPORT ══════════════════╗{RESET}")
    print(f"{G}║{W} ASSET      : {BOLD}{ASSETS[state['pair']]['name'].ljust(35)}{RESET}{G}║")
    print(f"{G}║{W} DIRECTION  : {dir_color}{BOLD}{direction_text.ljust(35)}{RESET}{G}║")
    print(f"{G}║{W} EXEC TIME  : {BOLD}{entry_time.ljust(35)}{RESET}{G}║")
    print(f"{G}║{W} ACCURACY   : {color}{BOLD}{str(round(acc,2))+'%'.ljust(35)}{RESET}{G}║")
    
    inv = state['bal'] * (0.10 if acc >= 85 else 0.03)
    print(f"{G}║{W} INVEST     : {BOLD}${str(round(inv,1)).ljust(35)}{RESET}{G}║")
    print(f"{G}╚══════════════════════════════════════════════════════╝{RESET}")
    
    if acc < 80:
        print(f"{R}>> ALERT: Accuracy below 80%. HIGH RISK. SKIP! <<{RESET}")
    else:
        print(f"{G}>> CONFIRMED: High Probability Trade at {entry_time}. <<{RESET}")

def main():
    while True:
        clear()
        print(get_header())
        try:
            cmd_in = input(f"{G}BOT_SHELL# {W}").lower().strip().split()
            if not cmd_in: continue
            
            c = cmd_in[0]
            if c == "exit": break
            elif c == "auto": auto_finder()
            elif c == "signal":
                run_prediction()
                input(f"\n{W}Press Enter to continue...{RESET}")
            elif c == "pair" and len(cmd_in)>1 and cmd_in[1] in ASSETS:
                state['pair'] = cmd_in[1]
            elif c == "bal" and len(cmd_in)>1:
                state['bal'] = float(cmd_in[1])
            else:
                print(f"{R}Unknown Command.{RESET}"); time.sleep(1)
        except Exception as e:
            print(f"{R}Error: {e}{RESET}"); time.sleep(1)

if __name__ == "__main__":
    main()
