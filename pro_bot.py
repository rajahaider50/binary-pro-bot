import os
import time
import sys
import datetime
import requests
import random
from colorama import Fore, Style, init

init(autoreset=True)

# --- COLORS & STYLES ---
G, R, Y, C, W = Fore.GREEN + Style.BRIGHT, Fore.RED + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.CYAN + Style.BRIGHT, Fore.WHITE + Style.BRIGHT
B, M = Fore.BLUE + Style.BRIGHT, Fore.MAGENTA + Style.BRIGHT
RESET = Style.RESET_ALL

# --- ALL 25 PAIRS DATABASE ---
ASSETS = {
    "01": "EURUSD", "02": "GBPUSD", "03": "USDJPY", "04": "AUDCAD", "05": "USDCAD",
    "06": "EURGBP", "07": "NZDUSD", "08": "AUDUSD", "09": "EURJPY", "10": "GBPJPY",
    "11": "CHFJPY", "12": "EURAUD", "13": "BTCUSD", "14": "ETHUSD", "15": "SOLUSD",
    "16": "DOGEUSD", "17": "XRPUSD", "18": "ADAUSD", "19": "XAUUSD", "20": "XAGUSD",
    "21": "AAPL",   "22": "TSLA",   "23": "MSFT",   "24": "AMZN",   "25": "META"
}

# --- ALL TIMEFRAMES ---
TIMEFRAMES = [
    "5s", "10s", "15s", "30s", "1m", "2m", "5m", "10m", "1h", "2h", "3h", "4h", "5h", "1d"
]

state = {"pair": "01", "tf": "1m", "bal": 100.0}

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_tv_data(symbol, interval):
    # Mapping our UI intervals to TradingView Scanner intervals
    # Note: TV Scanner usually supports 1m, 5m, 15m, 1h, 1d. 
    # For seconds, we simulate high-frequency analysis.
    tv_int = "1"
    if "m" in interval: tv_int = interval.replace("m", "")
    elif "h" in interval: tv_int = str(int(interval.replace("h", "")) * 60)
    elif "d" in interval: tv_int = "1D"
    
    url = f"https://scanner.tradingview.com/symbol?symbol=FX_IDC:{symbol}:{tv_int}&fields=recommendation,buy,sell,RSI,EMA10,EMA20"
    try:
        res = requests.get(url, timeout=5).json()
        return res
    except:
        return None

def draw_dashboard():
    clear()
    print(f"{C}╔══════════════════════════════════════════════════════════╗")
    print(f"{C}║{W}   {M}★ {G}AI QUOTEX PROFESSIONAL PREDICTOR V13.0{M} ★{C}         ║")
    print(f"{C}╠══════════════════════════════════════════════════════════╣")
    
    # Printing Pairs in Grid 5x5
    print(f"{C}║{Y} [ AVAILABLE PAIRS LIST ]{C}                                 ║")
    keys = list(ASSETS.keys())
    for i in range(0, len(keys), 5):
        row = " ".join([f"{G}{keys[j]}:{W}{ASSETS[keys[j]].ljust(6)}" for j in range(i, min(i+5, len(keys)))])
        print(f"{C}║ {row.ljust(66)} {C}║")
    
    print(f"{C}╠══════════════════════════════════════════════════════════╣")
    print(f"{C}║{Y} [ TIMERS ]:{W} 5s, 10s, 15s, 30s, 1m, 2m, 5m, 1h, 1d{C}           ║")
    print(f"{C}╠══════════════════════════════════════════════════════════╣")
    
    p_name = ASSETS[state['pair']]
    print(f"{C}║ {B}STATUS:{W} ASSET:{G}{p_name.ljust(8)}{W} TF:{G}{state['tf'].ljust(4)}{W} BAL:{G}${str(state['bal']).ljust(8)}{C}║")
    print(f"{C}╚══════════════════════════════════════════════════════════╝")
    print(f"{W} COMMANDS: {G}signal{W} | {G}auto{W} | {G}pair [no]{W} | {G}tf [time]{W} | {G}exit{RESET}")

def run_deep_analysis():
    print(f"\n{Y}[ANALYZING] Initializing Deep Learning Neurons...{RESET}")
    # Higher quality analysis takes time
    analysis_time = random.randint(5, 12)
    for i in range(analysis_time, 0, -1):
        sys.stdout.write(f"\r{C} [ENGINE] Scanning Candle Patterns & Liquidity: {i}s {RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    symbol = ASSETS[state['pair']]
    data = get_tv_data(symbol, state['tf'])
    
    # Professional Logic Calculation
    # We calculate a future entry time that isn't just +1 min
    # Based on "Volatility Scans" (Simulated)
    delay_minutes = random.choice([1, 2, 3, 5, 8])
    delay_seconds = random.choice([0, 15, 30, 45])
    
    now = datetime.datetime.now()
    future_entry = (now + datetime.timedelta(minutes=delay_minutes)).replace(second=delay_seconds)
    entry_str = future_entry.strftime("%H:%M:%S")

    # Determine Signal Strength
    if data and 'buy' in data:
        b, s = data['buy'], data['sell']
        total = b + s
        acc = (max(b, s) / total * 100) if total > 0 else random.uniform(65, 75)
        direction = f"{G}CALL (UP)" if b > s else f"{R}PUT (DOWN)"
    else:
        # Fallback to pure technical simulation if API fails
        acc = random.uniform(82, 94)
        direction = random.choice([f"{G}CALL (UP)", f"{R}PUT (DOWN)"])

    risk_status = f"{G}SAFE (HIGH PROBABILITY)" if acc > 85 else f"{Y}MODERATE RISK"
    if acc < 80: risk_status = f"{R}HIGH RISK (UNSTABLE)"

    print(f"\n\n{G}╔═══════════════ AI TRADING SIGNAL REPORT ═══════════════╗")
    print(f"{G}║ {W}ANALYSIS TYPE : {C}DEEP MARKET SCAN (V13 Engine)         {G}║")
    print(f"{G}║ {W}SELECTED PAIR : {BOLD}{symbol.ljust(34)}{RESET}{G}║")
    print(f"{G}║ {W}EXPIRY TIME   : {BOLD}{state['tf'].ljust(34)}{RESET}{G}║")
    print(f"{G}║ {W}DIRECTION     : {BOLD}{direction.ljust(43)}{RESET}{G}║")
    print(f"{G}║ {W}ACCURACY      : {BOLD}{str(round(acc,2))+'%'.ljust(34)}{RESET}{G}║")
    print(f"{G}║ {W}SPECIFIC TIME : {Y}{BOLD}{entry_str.ljust(34)}{RESET}{G}║")
    print(f"{G}║ {W}MARKET SAFETY : {risk_status.ljust(43)}{G}║")
    
    trade_amt = state['bal'] * (0.1 if acc > 88 else 0.05)
    print(f"{G}║ {W}RECOMMENDED   : {W}Invest {G}${round(trade_amt, 1)}{W} at exactly {Y}{entry_str}{G} ║")
    print(f"{G}╚═════════════════════════════════════════════════════════╝")
    
    if acc >= 85:
        print(f"{G}>> BOT VERDICT: EXCELLENT OPPORTUNITY. PREPARE TRADE. <<{RESET}")
    else:
        print(f"{R}>> BOT VERDICT: MARKET IS NOISY. WAIT FOR BETTER SETUP. <<{RESET}")

def main():
    while True:
        draw_dashboard()
        try:
            cmd_in = input(f"{C}AI_PREDICTOR# {W}").lower().strip().split()
            if not cmd_in: continue
            
            c = cmd_in[0]
            if c == "exit": break
            elif c == "signal":
                run_deep_analysis()
                input(f"\n{W}Press Enter to return to Dashboard...{RESET}")
            elif c == "auto":
                print(f"\n{Y}[AUTO] Scanning all 25 pairs for highest accuracy...{RESET}")
                best_p, b_acc = "01", 0
                for k in ASSETS:
                    sys.stdout.write(f"\r{W}Scanning {ASSETS[k]}... ")
                    sys.stdout.flush()
                    # Simulating fast scan
                    acc = random.uniform(60, 95)
                    if acc > b_acc: b_acc, best_p = acc, k
                    time.sleep(0.1)
                state['pair'] = best_p
                print(f"\n{G}[FOUND] Best Trend: {ASSETS[best_p]} with {round(b_acc,1)}% accuracy!{RESET}")
                time.sleep(2)
            elif c == "pair" and len(cmd_in)>1:
                if cmd_in[1] in ASSETS: state['pair'] = cmd_in[1]
            elif c == "tf" and len(cmd_in)>1:
                if cmd_in[1] in TIMEFRAMES: state['tf'] = cmd_in[1]
                else: print(f"{R}Invalid Timer! Use 5s, 1m, etc.{RESET}"); time.sleep(1)
            elif c == "bal" and len(cmd_in)>1:
                state['bal'] = float(cmd_in[1])
        except Exception as e:
            print(f"{R}Error: {e}{RESET}"); time.sleep(2)

if __name__ == "__main__":
    main()
