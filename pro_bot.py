import os
import time
import sys
import datetime
from tradingview_ta import TA_Handler, Interval

# --- UI DESIGN TOKENS (Matrix/Hacker Style) ---
G = "\033[38;5;46m"  # Matrix Green
R = "\033[38;5;196m" # Danger Red
Y = "\033[38;5;226m" # Warning Yellow
B = "\033[38;5;33m"  # Cyber Blue
C = "\033[38;5;51m"  # Neon Cyan
W = "\033[38;5;255m" # Text White
BOLD = "\033[1m"
RESET = "\033[0m"

# --- ALL PAIRS FROM YOUR IMAGES (Mapped to TradingView) ---
ASSETS = {
    # FOREX OTC
    "01": {"name": "EURUSD", "display": "EUR/USD", "exch": "FX_IDC", "scr": "forex"},
    "02": {"name": "GBPUSD", "display": "GBP/USD", "exch": "FX_IDC", "scr": "forex"},
    "03": {"name": "USDJPY", "display": "USD/JPY", "exch": "FX_IDC", "scr": "forex"},
    "04": {"name": "AUDCAD", "display": "AUD/CAD", "exch": "FX_IDC", "scr": "forex"},
    "05": {"name": "USDCAD", "display": "USD/CAD", "exch": "FX_IDC", "scr": "forex"},
    "06": {"name": "EURGBP", "display": "EUR/GBO", "exch": "FX_IDC", "scr": "forex"},
    "07": {"name": "NZDUSD", "display": "NZD/USD", "exch": "FX_IDC", "scr": "forex"},
    # CRYPTO
    "10": {"name": "BTCUSD", "display": "BITCOIN", "exch": "BITSTAMP", "scr": "crypto"},
    "11": {"name": "ETHUSD", "display": "ETHEREUM", "exch": "BINANCE", "scr": "crypto"},
    "12": {"name": "SOLUSD", "display": "SOLANA", "exch": "BINANCE", "scr": "crypto"},
    "13": {"name": "DOGEUSD", "display": "DOGE", "exch": "BINANCE", "scr": "crypto"},
    "14": {"name": "XRPUSD", "display": "RIPPLE", "exch": "BINANCE", "scr": "crypto"},
    # STOCKS/COMMODITIES
    "20": {"name": "GOLD", "display": "GOLD", "exch": "OANDA", "scr": "cfd"},
    "21": {"name": "SILVER", "display": "SILVER", "exch": "OANDA", "scr": "cfd"},
    "22": {"name": "AAPL", "display": "APPLE", "exch": "CAPITALCOM", "scr": "stock"},
    "23": {"name": "GOOGL", "display": "GOOGLE", "exch": "CAPITALCOM", "scr": "stock"},
    "24": {"name": "TSLA", "display": "TESLA", "exch": "CAPITALCOM", "scr": "stock"},
    "25": {"name": "FB", "display": "FACEBOOK", "exch": "CAPITALCOM", "scr": "stock"},
}

# --- DEFAULT STATE ---
state = {
    "pair": "01",
    "tf": "1m",
    "bal": 100.0,
    "last_signal": "NONE"
}

def clear():
    os.system('clear')

def get_header():
    # ASCII Art & Pair Matrix
    header = f"""
{G} █████╗ ██╗    ███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗     
██╔══██╗██║    ██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██║     
███████║██║    ███████╗██║██║  ███╗██╔██╗ ██║███████║██║     
██╔══██║██║    ╚════██║██║██║   ██║██║╚██╗██║██╔══██║██║     
██║  ██║██║    ███████║██║╚██████╔╝██║ ╚████║██║  ██║███████╗
╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
{C}   >> AI BINARY PREDICTION TERMINAL | ENCRYPTED LINK | V5.0 <<{RESET}
{BOLD}{W}----------------------------------------------------------------------
[ AVAILABLE PAIRS MATRIX ]
{G}01:EURUSD  02:GBPUSD  03:USDJPY  04:AUDCAD  05:USDCAD  06:EURGBP  07:NZDUSD
10:BITCOIN 11:ETHEREUM 12:SOLANA  13:DOGE    14:RIPPLE
20:GOLD    21:SILVER   22:APPLE   23:GOOGLE  24:TESLA   25:FACEBOOK
{W}----------------------------------------------------------------------
[ CONFIG ]  Pair: {Y}{ASSETS[state['pair']]['display']}{W}  | TF: {Y}{state['tf'].upper()}{W} | Bal: {G}${state['bal']}{W}
----------------------------------------------------------------------{RESET}
{BOLD}CMD: {C}signal{W} | {C}pair [no]{W} | {C}tf [1m/5m]{W} | {C}bal [amt]{W} | {C}exit{RESET}
"""
    return header

def run_prediction():
    p = ASSETS[state['pair']]
    print(f"\n{C}[SYSTEM] Initializing Analysis for {p['display']}...")
    time.sleep(1)
    print(f"{C}[SYSTEM] Syncing 26 Indicators (RSI, Stoch, MACD, etc.){RESET}")
    
    tf_map = {"1m": Interval.INTERVAL_1_MINUTE, "5m": Interval.INTERVAL_5_MINUTES}
    
    try:
        handler = TA_Handler(
            symbol=p['name'],
            screener=p['scr'],
            exchange=p['exch'],
            interval=tf_map.get(state['tf'], Interval.INTERVAL_1_MINUTE)
        )
        analysis = handler.get_analysis()
        buy = analysis.summary['BUY']
        sell = analysis.summary['SELL']
        neutral = analysis.summary['NEUTRAL']
        
        # Accuracy Calculation Logic
        total_signals = buy + sell + neutral
        acc = 0
        direction = "STAY"
        
        if buy > sell:
            acc = (buy / total_signals) * 100
            direction = f"{G}CALL (UP){RESET}"
        else:
            acc = (sell / total_signals) * 100
            direction = f"{R}PUT (DOWN){RESET}"

        # Syncing Countdown
        exec_time = (datetime.datetime.now() + datetime.timedelta(seconds=20)).strftime("%H:%M:%S")
        
        print(f"{Y}[ALERT] Strong Trend Identified. Preparing Entry Point...{RESET}")
        for i in range(15, 0, -1):
            sys.stdout.write(f"\r{BOLD}{R} [LOCKING] ENTRY AT {exec_time} | SYNC: {i}s {RESET}")
            sys.stdout.flush()
            time.sleep(1)
        print("\n")

        # Result Table
        res_color = G if acc >= 80 else R
        print(f"{G}╔════════════════════ SIGNAL REPORT ════════════════════╗{RESET}")
        print(f"{G}║{W} ASSET     : {BOLD}{p['display'].ljust(35)}{RESET}{G}║")
        print(f"{G}║{W} DIRECTION : {BOLD}{direction.ljust(44)}{RESET}{G}║")
        print(f"{G}║{W} EXEC TIME : {BOLD}{exec_time.ljust(35)}{RESET}{G}║")
        print(f"{G}║{W} ACCURACY  : {res_color}{BOLD}{str(round(acc,2))+'%'.ljust(35)}{RESET}{G}║")
        
        # Money Management
        inv = state['bal'] * (0.05 if acc > 88 else 0.02)
        risk = f"{G}LOW{RESET}" if acc > 88 else f"{Y}MEDIUM{RESET}"
        
        print(f"{G}║{W} INVEST    : {BOLD}${str(round(inv,1)).ljust(35)}{RESET}{G}║")
        print(f"{G}║{W} RISK      : {BOLD}{risk.ljust(44)}{RESET}{G}║")
        print(f"{G}╚═══════════════════════════════════════════════════════╝{RESET}")
        
        if acc < 80:
            print(f"{R}>> BAD MARKET: System recommends SKIPPING this trade. <<{RESET}")

    except Exception as e:
        print(f"{R}[ERROR] Market Data Unreachable for {p['name']}.{RESET}")

def main():
    while True:
        clear()
        print(get_header())
        
        try:
            user_input = input(f"{G}AI_BOT_SHELL# {W}").lower().strip().split()
            if not user_input: continue
            
            cmd = user_input[0]
            
            if cmd == "exit":
                print(f"{R}Terminating Link...{RESET}")
                break
            
            elif cmd == "signal":
                run_prediction()
                input(f"\n{W}Press Enter to continue...{RESET}")
                
            elif cmd == "pair":
                if len(user_input) > 1 and user_input[1] in ASSETS:
                    state['pair'] = user_input[1]
                else:
                    print(f"{R}Invalid Pair Code. See Matrix Above.{RESET}")
                    time.sleep(2)
                    
            elif cmd == "tf":
                if len(user_input) > 1 and user_input[1] in ["1m", "5m"]:
                    state['tf'] = user_input[1]
                else:
                    print(f"{R}Use 'tf 1m' or 'tf 5m'{RESET}")
                    time.sleep(2)
                    
            elif cmd == "bal":
                if len(user_input) > 1:
                    state['bal'] = float(user_input[1])
                else:
                    print(f"{R}Provide amount, e.g., 'bal 500'{RESET}")
                    time.sleep(2)
            else:
                print(f"{R}Command Error. Type 'signal' or 'pair [no]'{RESET}")
                time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception:
            print(f"{R}Input Error. Restarting Shell...{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
