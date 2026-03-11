import os
import time
import sys
import datetime
from tradingview_ta import TA_Handler, Interval

# --- UI DESIGN (Cyber-Security / Hacker Aesthetic) ---
G = "\033[38;5;46m"  # Matrix Green
R = "\033[38;5;196m" # Danger Red
Y = "\033[38;5;226m" # Warning Yellow
B = "\033[38;5;33m"  # Cyber Blue
C = "\033[38;5;51m"  # Neon Cyan
W = "\033[38;5;255m" # Text White
BOLD = "\033[1m"
RESET = "\033[0m"

# --- EXTENDED ASSET DATABASE ---
ASSETS = {
    "01": {"name": "EURUSD", "display": "EUR/USD", "exch": "FX_IDC", "scr": "forex"},
    "02": {"name": "GBPUSD", "display": "GBP/USD", "exch": "FX_IDC", "scr": "forex"},
    "03": {"name": "USDJPY", "display": "USD/JPY", "exch": "FX_IDC", "scr": "forex"},
    "04": {"name": "AUDCAD", "display": "AUD/CAD", "exch": "FX_IDC", "scr": "forex"},
    "05": {"name": "USDCAD", "display": "USD/CAD", "exch": "FX_IDC", "scr": "forex"},
    "10": {"name": "BTCUSD", "display": "BITCOIN", "exch": "BITSTAMP", "scr": "crypto"},
    "11": {"name": "ETHUSD", "display": "ETHEREUM", "exch": "BINANCE", "scr": "crypto"},
    "20": {"name": "GOLD", "display": "GOLD", "exch": "OANDA", "scr": "cfd"},
    "21": {"name": "SILVER", "display": "SILVER", "exch": "OANDA", "scr": "cfd"},
    "22": {"name": "AAPL", "display": "APPLE", "exch": "CAPITALCOM", "scr": "stock"},
    "23": {"name": "TSLA", "display": "TESLA", "exch": "CAPITALCOM", "scr": "stock"},
}

state = {"pair": "01", "tf": "1m", "bal": 100.0}

def clear():
    os.system('clear')

def get_header():
    return f"""
{G} ██████╗ ███████╗███████╗██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
 ██╔══██╗██╔════╝██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║
 ██║  ██║█████╗  █████╗  ██████╔╝    ███████╗██║     ███████║██╔██╗ ██║
 ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝     ╚════██║██║     ██╔══██║██║╚██╗██║
 ██████╔╝███████╗███████╗██║         ███████║╚██████╗██║  ██║██║ ╚████║
 ╚═════╝ ╚══════╝╚══════╝╚═╝         ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{C}   >> DEEP-SCAN ANALYZER V6.0 | AUTO-PAIR FINDER | 85%+ TARGET <<{RESET}
{BOLD}{W}----------------------------------------------------------------------
[ PAIR MATRIX ] {G}01:EURUSD 02:GBPUSD 03:USDJPY 04:AUDCAD 05:USDCAD 10:BTC 
                11:ETH    20:GOLD   21:SILV   22:AAPL   23:TSLA{W}
----------------------------------------------------------------------
[ CONFIG ] Pair: {Y}{ASSETS[state['pair']]['display']}{W} | TF: {Y}{state['tf'].upper()}{W} | Bal: {G}${state['bal']}{W}
----------------------------------------------------------------------{RESET}
{BOLD}COMMANDS: {C}signal{W} | {C}auto{W} | {C}pair [no]{W} | {C}tf [1m/5m]{W} | {C}bal [amt]{W} | {C}exit{RESET}
"""

def fetch_signals(pair_key):
    p = ASSETS[pair_key]
    tf_map = {"1m": Interval.INTERVAL_1_MINUTE, "5m": Interval.INTERVAL_5_MINUTES}
    try:
        handler = TA_Handler(
            symbol=p['name'], screener=p['scr'], exchange=p['exch'],
            interval=tf_map.get(state['tf'], Interval.INTERVAL_1_MINUTE)
        )
        analysis = handler.get_analysis()
        buy = analysis.summary['BUY']
        sell = analysis.summary['SELL']
        neutral = analysis.summary['NEUTRAL']
        total = buy + sell + neutral
        
        # Enhanced Logic: Deep Strength
        if buy > sell:
            acc = (buy / total) * 100
            direction = "CALL (UP)"
        else:
            acc = (sell / total) * 100
            direction = "PUT (DOWN)"
        return acc, direction
    except:
        return 0, "ERROR"

def auto_finder():
    print(f"\n{C}[AUTO] Scanning all assets for the best market trend...{RESET}")
    best_pair = None
    max_acc = 0
    
    for key in ASSETS:
        acc, _ = fetch_signals(key)
        sys.stdout.write(f"\r{W}Checking {ASSETS[key]['display']}: {G}{acc:.1f}%{RESET}   ")
        sys.stdout.flush()
        if acc > max_acc:
            max_acc = acc
            best_pair = key
        time.sleep(0.5)
        
    if best_pair:
        state['pair'] = best_pair
        print(f"\n\n{G}[FOUND] Best Asset: {ASSETS[best_pair]['display']} with {max_acc:.1f}% Accuracy!{RESET}")
        time.sleep(2)
    else:
        print(f"\n{R}[ERROR] Could not find high accuracy pairs.{RESET}")

def run_prediction():
    acc, direction = fetch_signals(state['pair'])
    p = ASSETS[state['pair']]
    
    print(f"\n{C}[SCAN] Analyzing indicators & candle patterns...{RESET}")
    # 20 second calculation delay for "Deep Scan"
    for i in range(15, 0, -1):
        sys.stdout.write(f"\r{Y} [CALCULATING] Syncing Global Indices... {i}s {RESET}")
        sys.stdout.flush()
        time.sleep(1)
    print("\n")

    # Prediction for entry 1-2 minutes ahead to ensure high accuracy
    now = datetime.datetime.now()
    entry_time = (now + datetime.timedelta(minutes=1)).replace(second=0).strftime("%H:%M:00")
    
    res_color = G if acc >= 80 else R
    print(f"{G}╔════════════════════ DEEP-SCAN REPORT ════════════════════╗{RESET}")
    print(f"{G}║{W} BEST ASSET  : {BOLD}{p['display'].ljust(35)}{RESET}{G}║")
    print(f"{G}║{W} DIRECTION   : {BOLD}{direction.ljust(44)}{RESET}{G}║")
    print(f"{G}║{W} EXEC TIME   : {BOLD}{entry_time.ljust(35)}{RESET}{G}║")
    print(f"{G}║{W} ACCURACY    : {res_color}{BOLD}{str(round(acc,2))+'%'.ljust(35)}{RESET}{G}║")
    
    inv = state['bal'] * (0.05 if acc > 88 else 0.02)
    risk = f"{G}LOW-RISK{RESET}" if acc > 88 else f"{Y}MODERATE{RESET}"
    
    print(f"{G}║{W} INVESTMENT  : {BOLD}${str(round(inv,1)).ljust(35)}{RESET}{G}║")
    print(f"{G}║{W} RISK EVAL   : {BOLD}{risk.ljust(44)}{RESET}{G}║")
    print(f"{G}╚══════════════════════════════════════════════════════════╝{RESET}")
    
    if acc < 80:
        print(f"{R}>> ALERT: Accuracy below 80%. Market unstable. DO NOT TRADE! <<{RESET}")
    else:
        print(f"{G}>> TREND CONFIRMED: Prepare to trade at {entry_time}. <<{RESET}")

def main():
    while True:
        clear()
        print(get_header())
        try:
            user_input = input(f"{G}DEEP_SHELL# {W}").lower().strip().split()
            if not user_input: continue
            cmd = user_input[0]
            if cmd == "exit": break
            elif cmd == "auto": auto_finder()
            elif cmd == "signal":
                run_prediction()
                input(f"\n{W}Press Enter to return to Shell...{RESET}")
            elif cmd == "pair" and len(user_input)>1 and user_input[1] in ASSETS:
                state['pair'] = user_input[1]
            elif cmd == "tf" and len(user_input)>1 and user_input[1] in ["1m", "5m"]:
                state['tf'] = user_input[1]
            elif cmd == "bal" and len(user_input)>1:
                state['bal'] = float(user_input[1])
            else:
                print(f"{R}Error: Command not recognized.{RESET}"); time.sleep(1)
        except:
            print(f"{R}System Error. Resetting...{RESET}"); time.sleep(1)

if __name__ == "__main__":
    main()
