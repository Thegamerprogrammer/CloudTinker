#!/usr/bin/env python3
# CloudTinker v9.6 – Full Loop + Interrupt Safety + OG Input UI + WebSocket TurboWarp

import os, sys, time, platform, subprocess, asyncio, json
from tqdm import tqdm
import pwinput
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Auto-install missing dependencies
for pkg in [
    "scratchattach>=2.1.13",
    "colorama",
    "pyfiglet",
    "pwinput",
    "requests",
    "tqdm",
    "websockets"
]:
    module = pkg.split(">=")[0]
    try:
        __import__(module)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import scratchattach as sa
import requests
import websockets

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def beep(n=1):
    if platform.system() == "Windows":
        import winsound
        for _ in range(n):
            winsound.Beep(800, 200)
    else:
        print("\a" * n, end="", flush=True)

def splash(msg=None):
    clear()
    print(Fore.CYAN + Figlet(font="slant").renderText("CloudTinker"))
    print(Fore.GREEN + "CloudTinker v9.6\n")
    print(Fore.CYAN + "-By Thegamerprogrammer\n")
    print(Fore.CYAN + "ScratchAttach by TimMcCool\n")
    print(Fore.BLUE + "A pentest tool for changing cloud variables on Scratch & TurboWarp.\n")
    print(Style.DIM + "-" * 120 + Style.RESET_ALL)
    print(Fore.RED + "[!] YOU are responsible for any damage caused!\n")
    print(Fore.YELLOW + "[!] Changing others' projects cloud variables may violate TOU.\n")
    if msg:
        print(Fore.MAGENTA + f"[INFO] {msg}\n")
    print(Style.DIM + "-" * 120 + Style.RESET_ALL)

def wait(prompt):
    return input(Fore.CYAN + prompt + Style.RESET_ALL)

def getpass():
    return pwinput.pwinput(Fore.GREEN + "Password: ", mask="*")

def animate(msg):
    sys.stdout.write(Fore.CYAN + msg)
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(0.3)
        sys.stdout.write(".")
        sys.stdout.flush()
    print()

def get_int(prompt, minimum=1):
    while True:
        try:
            v = int(wait(prompt))
            if v < minimum:
                print(Fore.RED + f"Value must be ≥ {minimum}.")
                continue
            return v
        except ValueError:
            print(Fore.RED + "Please enter a valid integer.")

def get_float(prompt, minimum=0.0):
    while True:
        try:
            v = float(wait(prompt))
            if v < minimum:
                print(Fore.RED + f"Value must be ≥ {minimum}.")
                continue
            return v
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

# ── Scratch login & loop ─────────────────────────────────────────────────────

def login_scratch():
    while True:
        splash("Scratch Login")
        print(Fore.CYAN + "Scratch/Multi/Monitor Mode\n" + Style.DIM + "-" * 120 + Style.RESET_ALL)
        try:
            user = wait("Scratch Username: ")
            pwd  = getpass()
            animate("Connecting to Scratch")
            return sa.login(user, pwd)
        except Exception as e:
            splash(f"[FATAL] {e}")
            beep(2); time.sleep(2)

def scratch_loop():
    sess = login_scratch()
    pid  = get_int("Project ID: ")
    try:
        cloud = sess.connect_cloud(pid)
    except Exception as e:
        splash(f"[FATAL] Could not connect to project {pid}: {e}")
        time.sleep(2)
        return

    splash(f"[SUCCESS] Connected to Scratch {pid}")
    print(Fore.CYAN + "Scratch Mode\n" + Style.DIM + "-" * 120 + Style.RESET_ALL)
    beep()
    n     = get_int("Number of variables?: ")
    vars_ = [(wait(f"Variable {i+1} name: "), wait("Value to be set: ")) for i in range(n)]
    delay = get_float("Delay between cycles (sec): ")
    wait("Press Enter to continue...")
    cycle = 0
    try:
        while True:
            splash(f"Scratch Loop #{cycle}")
            print(Fore.CYAN + "Scratch Mode\n" + Fore.RED + "Press CTRL+C to exit!\n" + Style.DIM + "-" * 120 + Style.RESET_ALL)
            for name, val in vars_:
                try:
                    cloud.set_var(name, val)
                    print(Fore.GREEN + f"[SUCCESS] {name} → {val}")
                except Exception as e:
                    print(Fore.RED + f"[FATAL] {name}: {e}")
                    beep(2)
            for _ in tqdm(range(int(delay)), desc="Next in", ncols=60):
                time.sleep(1)
            cycle += 1
    except KeyboardInterrupt:
        return

# ── TurboWarp via WebSocket ───────────────────────────────────────────────────

class TurboWarpCloudClient:
    def __init__(self, username, project_id):
        self.username   = username
        self.project_id = str(project_id)
        self.ws         = None

    async def connect(self):
        uri = "wss://clouddata.turbowarp.org"
        self.ws = await websockets.connect(uri)
        await self.ws.send(json.dumps({
            "method":     "handshake",
            "user":       self.username,
            "project_id": self.project_id
        }))

    async def set_var(self, name, value):
        if not self.ws:
            raise Exception("WebSocket not connected.")
        await self.ws.send(json.dumps({
            "method": "set",
            "name":   name,
            "value":  str(value)
        }))

    async def close(self):
        if self.ws:
            await self.ws.close()
            

def turbowarp_loop():
    # Gather credentials *outside* the async function so Ctrl+C here also returns
    splash("TurboWarp Login")
    print(Fore.CYAN + "TurboWarp Mode\n" + Style.DIM + "-" * 120 + Style.RESET_ALL)
    user = wait("Scratch Username: ")
    pwd  = getpass()
    animate("Connecting to TurboWarp")
    pid  = get_int("Project ID: ")

    client = TurboWarpCloudClient(user, pid)

    async def run_loop():
        # Handshake
        try:
            await client.connect()
        except Exception as e:
            splash(f"[FATAL] Handshake failed: {e}")
            time.sleep(2)
            return

        splash(f"[SUCCESS] Connected to TurboWarp {pid}")
        beep()
        n     = get_int("Number of variables?: ")
        vars_ = [(wait(f"Variable {i+1} name: "), wait("Value to be set: ")) for i in range(n)]
        delay = get_float("Delay between cycles (sec): ")
        wait("Press Enter to continue...")
        cycle = 0

        while True:
            splash(f"TurboWarp Loop #{cycle}")
            print(Fore.CYAN + "TurboWarp Mode\n"
                  + Fore.RED + "Press CTRL+C to return to menu!\n"
                  + Style.DIM + "-" * 120 + Style.RESET_ALL)
            for name, val in vars_:
                try:
                    await client.set_var(name, val)
                    print(Fore.GREEN + f"[SUCCESS] {name} → {val}")
                except Exception as e:
                    print(Fore.RED + f"[FATAL] {name}: {e}")
                    beep(2)
            for _ in tqdm(range(int(delay)), desc="Next in", ncols=60):
                time.sleep(1)
            cycle += 1

    # Run on its own event loop to catch KeyboardInterrupt
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_loop())
    except KeyboardInterrupt:
        # Gracefully close the websocket if connected
        try:
            loop.run_until_complete(client.close())
        except:
            pass
        # Return to main menu without traceback
        return
    finally:
        loop.close()

# ── Multi-Project Mode ────────────────────────────────────────────────────────

def multi_loop():
    sess   = login_scratch()
    total  = get_int("Number of Projects?: ")
    projects=[]
    for i in range(total):
        pid = get_int(f"Project {i+1} ID: ")
        try:
            cloud = sess.connect_cloud(pid)
        except Exception as e:
            splash(f"[FATAL] Could not connect to {pid}: {e}")
            time.sleep(2); return
        n     = get_int(f"Vars for {pid}?: ")
        vars_ = [(wait(f"[{pid}] Var{j+1} name: "), wait("Value to set: ")) for j in range(n)]
        projects.append((pid, cloud, vars_))
    delay = get_float("Delay between cycles (sec): ")
    wait("Press Enter to continue...")
    cycle = 0
    try:
        while True:
            splash(f"Multi-Project Loop #{cycle}")
            for pid, cloud, vars_ in projects:
                print(Fore.YELLOW + f"[{pid}]\n")
                for name, val in vars_:
                    try:
                        cloud.set_var(name, val)
                        print(Fore.GREEN + f"  {name} → {val}")
                    except Exception as e:
                        print(Fore.RED + f"  [FATAL] {name}: {e}")
                        beep(2)
            for _ in tqdm(range(int(delay)), desc="Next in", ncols=60):
                time.sleep(1)
            cycle += 1
    except KeyboardInterrupt:
        return

# ── Cloud Monitor ───────────────────────────────────────────────────────────

def monitor_loop():
    sess = login_scratch()
    pid  = get_int("Project ID to monitor: ")
    try:
        cloud = sess.connect_cloud(pid)
    except Exception as e:
        splash(f"[FATAL] Could not connect to {pid}: {e}")
        time.sleep(2); return
    vars     = [v.strip() for v in wait("Vars (comma sep): ").split(",") if v.strip()]
    interval = get_float("Interval (sec): ")
    old      = {v: None for v in vars}
    wait("Press Enter to continue...")
    try:
        while True:
            splash(f"Cloud Monitor {pid}")
            for v in vars:
                try:
                    val = cloud.get_var(v)
                    if old[v] != val:
                        print(Fore.GREEN + f"[UPDATED] {v}: {val}")
                        beep()
                    else:
                        print(Fore.YELLOW + f"[UNCHANGED] {v}: {val}")
                    old[v] = val
                except Exception as e:
                    print(Fore.RED + f"[FATAL] {v}: {e}")
                    beep(2)
            for _ in tqdm(range(int(interval)), desc="Next in", ncols=60):
                time.sleep(1)
    except KeyboardInterrupt:
        return

# ── Stats ────────────────────────────────────────────────────────────────────

def stats():
    splash("Scratch API Status")
    try:
        r = requests.get("https://api.scratch.mit.edu/")
        t = requests.get("https://clouddata.turbowarp.org/")
        if r.ok:
            print(Fore.GREEN + "[SUCCESS] Scratch API is online.")
            time.sleep(2)
        else:
            print(Fore.RED + "[FATAL] Scratch API is down.")
            time.sleep(2)
        if t.ok:
            print(Fore.GREEN + "[SUCCESS] TurboWarp API is online.")
            time.sleep(2)
        else:
            print(Fore.RED + "[FATAL] TurboWarp API is down.")
            time.sleep(2)
    except:
        print(Fore.RED + "[FATAL] Could not reach Scratch API.")
        print(Fore.RED + "[FATAL] Could not reach TurboWarp API.")
    time.sleep(2)

# ── Help Menu ─────────────────────────────────────────────────────────────────

def info_menu():
    splash("Help Menu")
    print(Fore.CYAN + "1) Scratch loop(Changes Scratch project cloud variables)")
    print(Fore.CYAN + "2) TurboWarp loop(Changes TurboWarp project cloud variables)")
    print(Fore.BLUE + "3) Multi-project loop(Change the cloud variables of multiple projects scratch only!)")
    print(Fore.BLUE + "4) Cloud monitor(Monitors cloud variable activity of projects scratch only!)")
    print(Fore.BLUE + "5) Status of Scratch api")
    print(Fore.BLUE + "6) Help menu")
    print(Fore.BLUE + "7) Exit")
    wait("\nPress Enter to return...")

# ── Main Menu ─────────────────────────────────────────────────────────────────
def main():
    while True:
        splash()  # redraw the ASCII header, credits, warnings, etc.

        # Row 1: Scratch & TurboWarp
        print(Fore.CYAN + "[1] Scratch        [2] TurboWarp")
        print(Fore.BLUE + "[3] Multi-Project  [4] Monitor")
        print(Fore.BLUE + "[5] Stats          [6] Help")
        print(Fore.BLUE + "[7] Exit \n")

        try:
            choice = wait("Choice (1–7): ").strip()
            if choice == "1":
                scratch_loop()
            elif choice == "2":
                turbowarp_loop()
            elif choice == "3":
                multi_loop()
            elif choice == "4":
                monitor_loop()
            elif choice == "5":
                stats()
            elif choice == "6":
                info_menu()
            elif choice == "7":
                splash("Exiting...")
                time.sleep(1)
                sys.exit(0)
            else:
                beep(2)
        except KeyboardInterrupt:
            # Return gracefully to the menu on Ctrl+C
            continue

if __name__ == "__main__":
    main()
