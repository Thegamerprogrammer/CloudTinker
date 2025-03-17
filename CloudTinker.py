import os
import warnings
import argparse
import random
import winsound
import ssl
import requests
import getpass
import sys
import importlib.util
import subprocess
import urllib.request
import time
import websocket
#Windows?
def check_operating_system():
    print("Checking OS")
    if os.name != 'nt':  # Windows-specific check
        print(Fore.RED + "This program is intended to run on Windows.")
        sys.exit(1)
#call function
check_operating_system()
def check_python_version():
    print("Checking Python Version")
    required_python_version = (3, 10)  # Checks Python Version Minimum 3.10
    if sys.version_info < required_python_version:
        print(f"Error: Python {required_python_version[0]}.{required_python_version[1]} or later is required.")
        sys.exit(1)
check_python_version()
#checking if internet is available/good
def check_internet_quality():
    try:
        os.system('cls')
        urllib.request.urlopen('https://www.google.com')
        print("Internet Connection Is Good!.")
        time.sleep(4)
        os.system('cls')
    except urllib.error.URLError:
        print("Check Your Internet Connection! exiting...")
        time.sleep(5)
        exit()
#install libraries automatically
def install_missing_libraries():
    print("Checking Libraries!")
    required_libraries = ['scratchconnect', 'art', 'colorama', 'pyfiglet']
    missing_libraries = []
    for library in required_libraries:
        spec = importlib.util.find_spec(library)
        if spec is None:
            missing_libraries.append(library)
    if len(missing_libraries) > 0:
        print("Installing missing libraries...")
        for library in missing_libraries:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
                print(f"Installed {library}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {library}")
        print("All missing libraries installed.")
        time.sleep(2)
        os.system('cls')
#calling functions
check_internet_quality()
install_missing_libraries()
import scratchconnect
from colorama import Fore, Back, Style
from pyfiglet import figlet_format
from art import *
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--suppress_warnings", action="store_true", help="Suppress warnings")
parser.add_argument("--turbowarp", action="store_true", help="Enable TurboWarp mode.")
parser.add_argument("--stats", action="store_true", help="Technical Stats For Nerds.")
parser.add_argument("--info", action="store_true", help="How To Use The Program?")
parser.add_argument("--cloud_monitor", action="store_true", help="CloudMonitor For a Project.")
args = parser.parse_args()

if args.cloud_monitor:
    print(Fore.MAGENTA + figlet_format("CloudTinker", font="standard"))
    print()
    print("===CloudMonitor_Mode===")
    print(randart())
    username = input(Fore.GREEN + 'Username?: ')
    print(Fore.YELLOW + "Password will not be visible due to security reasons!")
    password = getpass.getpass(Fore.GREEN + 'Password?: ')
    print('Connecting....')
    time.sleep(1)
    time.sleep(1)
    user = scratchconnect.ScratchConnect(username, password)
    project_id = input('Project id?: ')
    project1 = user.connect_project(project_id=project_id)
    cloud = project1.connect_cloud_variables()  # Connect the project's cloud
    event = cloud.create_cloud_event()  # Create a cloud event
    @event.on("connect")
    def connect():
        print(Fore.GREEN + "Connected Cloud!")

    @event.on("set")
    def set(data):
        print(Fore.GREEN + "SET: ", data)

    event.start()

if args.info:
    print(Fore.MAGENTA + figlet_format("CloudTinker", font="standard"))
    print()
    print("Welcome To CloudTinker! A Tool For Changing Cloud Variables Of Any Project")
    input("Press Any Key To Continue")
    print()
    print("Note: This Program Is A Pentest Tool And Is Stricly Forbidden To Change Other Project's Cloud Variables Which You Don't Have Permission To Change!")
    input("Press Any Key To Continue")
    print()
    print("This Program Is Safe To Use On Your Own Projects Or Which Ones You Have Permission To Change If You Use It For Malicous Purposes You Are Violating Scratch's Terms Of Use And May Result In A Ban!")
    input("Press Any Key To Continue")
    print()
    print("It Is Recommended To Run This Program In Powershell Or CMD")
    input("Press Any Key To Continue")
    print()
    print("You Have 4 Different aliases in the shell Which Are:-")
    print("--suppress_warnings, --turbowarp, --stats, --cloudmonitor")
    input("Press Any Key To Continue")
    print()
    print("--suppres_warnings Directs All Console Errors and Warning to A Log File In The Same Directory As The Program")
    input("Press Any Key To Continue")
    print()
    print("--turbowarp Is A Mode That Allow You To Change Cloud Variables On TurboWarp")
    input("Press Any Key To Continue")
    print()
    print("--Stats Shows The Health And Availabilty Of Scratch And TurboWarp")
    input("Press Any Key To Continue")
    print()
    print("Well That's All Enjoy :)")
    print()
    input("Press Any Key To Exit")
#stats
if args.stats:
    while True:
        print(randart())
        username = input(Fore.GREEN + 'Username?: ')
        print(Fore.YELLOW + "Password will not be visible due to security reasons!")
        password = getpass.getpass(Fore.GREEN + 'Password?: ')
        print('Connecting....')
        time.sleep(1)
        try:
            time.sleep(1)
            user = scratchconnect.ScratchConnect(username, password)
            break  # valid login, break out of the loop
        except scratchconnect.Exceptions.InvalidInfo as e:
            os.system('cls')
            time.sleep(1)
            print(randart())
            print(Fore.RED + str(e))
    os.system('cls')
    print(Style.RESET_ALL)
    print(randart())
    print(Fore.GREEN + 'Initializing...')
    time.sleep(1)
    os.system('cls')
    print(user.site_health())
    os.system('cls')
    os.system('cls')
    winsound.Beep(500, 1000)
    os.system('title CloudTinker Scratch Stats Tool')
    print("CloudTinker 5.0")
    print()
    print(Fore.GREEN + "Scratch Health")
    print()
    print(user.site_health())
    input("Press Any Key To Continue")
    os.system('cls')
    print(Fore.YELLOW + "Requesting Scratch...")
    r = requests.get('https://api.scratch.mit.edu/')
    print(Fore.YELLOW + "Requesting Turbowarp...")
    t = requests.get('https://turbowarp.org/')
    if r.status_code == 200:
        print(Fore.GREEN + 'Scratch API Is Online!')
        print(r)
        input(Fore.YELLOW + "Press Any Key To Continue")
    else:
        print(Fore.RED + 'Scratch API Is Down!')
        print(r)
        input(Fore.YELLOW + "Press Any Key To Continue")
        exit()
    if t.status_code == 200:
        print(Fore.GREEN + 'Turbowarp is Online!')
        print(t)
        input(Fore.YELLOW + "Press Any Key To Continue")
        exit()
    else:
        print(Fore.RED + 'Turbowarp is Down!')
        print(t)
        input(Fore.YELLOW + "Press Any Key To Continue")
        exit()

#suppresses console errors to a log file
if args.suppress_warnings:
    time.sleep(4)
    os.system('cls')
    time.sleep(1)
    error_log_file = "error_log.txt"
    requests.packages.urllib3.disable_warnings()
    warnings.filterwarnings("ignore")
    sys.stderr = open(error_log_file, "w")
#turbowarp
if args.turbowarp:
    time.sleep(4)
    os.system('cls')
    time.sleep(1)
    print(Fore.YELLOW + "Requesting Scratch...")
    r = requests.get('https://api.scratch.mit.edu/')
    print(Fore.YELLOW + "Requesting Turbowarp...")
    t = requests.get('https://turbowarp.org/')
    if r.status_code == 200:
        print(Fore.GREEN + 'Scratch API Is Online!')
        print(r)
    else:
        print(Fore.RED + 'Scratch API Is Down!')
        print(r)
        time.sleep(4)
        exit()
    if t.status_code == 200:
        print(Fore.GREEN + 'Turbowarp is Online!')
        print(t)
    else:
        print(Fore.RED + 'Turbowarp is Down!')
        print(t)
        time.sleep(4)
        exit()
    time.sleep(5)
    os.system('cls')
    print(Fore.MAGENTA + "By Thegamerprogrammer")
    print(Fore.YELLOW + "Scratchconnect library by Sid72020123")
    print(Fore.MAGENTA + figlet_format("CloudTinker", font="standard"))
    if args.suppress_warnings:
        print(Fore.YELLOW + "Warning! suppress_warnings enabled! check error_log.txt for warnings and errors")
    winsound.PlaySound("SystemStart", winsound.SND_ALIAS)
    print(Fore.YELLOW + "=== TurboWarp Mode ===")
    print()
    print(randart())
    #Login Script
    while True:
        Tw_Username = input(Fore.GREEN + "Scratch Username: ")
        print(Fore.YELLOW + "Password will not be visible due to security reasons!")
        Tw_Password = getpass.getpass(Fore.GREEN + "Scratch Password: ")
        print("Connecting")
        try:
            user = scratchconnect.ScratchConnect(Tw_Username, Tw_Password)
            break
        except scratchconnect.Exceptions.InvalidInfo as e:
            os.system('cls')
            time.sleep(1)
            print(randart())
            print(Fore.RED + str(e))
    os.system('cls')
    print(user.site_health())
    time.sleep(2)
    os.system('cls')
    print(randart())
    print()
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    Tw_Project = int(input(Fore.YELLOW + "Project ID: "))
    Tw_Custom_Username = input(Fore.YELLOW + "Custom Username This Feature May Not Work As Intended! Use Your Normal Username To Skip This.: ")
    project = user.connect_project(project_id=Tw_Project)
    tw_cloud = project.connect_turbowarp_cloud(username=Tw_Custom_Username)
    os.system('cls')
    print(randart())
    print()
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    Spam_Delay = input(Fore.YELLOW + "Spam Delay: ")
    if '.' in Spam_Delay:
        sleep_duration = float(Spam_Delay)
    else:
        sleep_duration = int(Spam_Delay)
    variable_count = int(input(Fore.YELLOW + "Number of variables to change: "))
    os.system('cls')
    variables = []
    values = []
    print()
    print(randart())
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    print(Fore.MAGENTA + "Enter variable names and values:")
    for i in range(variable_count):
        print(randart())
        variable_name = input(Fore.YELLOW + f"Variable {i+1}: ")
        while True:
            try:
                value = int(input(Fore.YELLOW + f"Value for Variable {i+1}: "))
                break
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter an integer value.")
        variables.append(variable_name)
        values.append(value)
    print()
    print(Fore.MAGENTA + "Running TurboWarp mode...")
    print()
    os.system('cls')
    while True:
        for variable, value in zip(variables, values):
            os.system('cls')
            print(randart())
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            set = tw_cloud.set_cloud_variable(variable_name=variable, value=value)
            if set:
                print(Fore.GREEN + "Cloud Updated")
                print(Fore.MAGENTA + f'Changed Cloud Var: {variable}')
            time.sleep(sleep_duration)
else:
    os.system('cls')
    time.sleep(1)
    print(Fore.YELLOW + 'Requesting Scratch API')
    r = requests.get('https://api.scratch.mit.edu/')
    if r.status_code == 200:
        print(Fore.GREEN + 'Scratch API Is Online!')
        print(r)
    else:
        print(Fore.RED + 'Scratch Is Down!')
        print(r)
        time.sleep(4)
        exit()
    time.sleep(4)
#login script
    def login():
        print(Fore.MAGENTA + "By Thegamerprogrammer")
        print(Fore.YELLOW + "Scratchconnect library by Sid72020123")
        print(Fore.MAGENTA + 'Running Latest Version 5.0')
        print(figlet_format("CloudTinker", font="standard"))
        print(Fore.YELLOW + 'Changes Cloud Variables Of Any Project In Scratch (You Dont need a scratcher account!)')
        print(Fore.RED + 'I Am Not Responsible For Any Damage Caused By The Program! (Use This At Your Own Risk!!)')
        if args.suppress_warnings:
            print(Fore.YELLOW + "Warning! suppress_warnings enabled! check error_log.txt for warnings and errors")
        print(randart())
        time.sleep(5)
        # Login Mode?
        print(Fore.GREEN + 'Initializing...')
        login_mode = input(Fore.YELLOW + 'Use Cookie Login Or Normal Login? Enter 1 for Cookie login and 2 for Normal Login: ')
        os.system('cls')
        # Cookie Login
        if login_mode == "1":
            while True:
                print(randart())
                username = input(Fore.GREEN + 'Username?: ')
                print(Fore.YELLOW + "Session ID will not be visible due to security reasons!")
                session_id = str(getpass.getpass(Fore.GREEN + 'Scratch Session Id?: '))
                scratch_cookie = {
                    "Username": username,
                    "SessionID": session_id,
                }  # set the cookie dictionary
                # Connect to Scratch
                try:
                    time.sleep(1)
                    user = scratchconnect.ScratchConnect(cookie=scratch_cookie)
                    break  # valid login, break out of the loop
                except scratchconnect.Exceptions.InvalidInfo as e:
                    os.system('cls')
                    time.sleep(1)
                    print(randart())
                    print(Fore.RED + str(e))
            os.system('cls')
            print(Style.RESET_ALL)
            print(randart())
            print(Fore.GREEN + 'Initializing...')
            time.sleep(1)
            os.system('cls')
            print(user.site_health())
            os.system('cls')
        # Normal Login
        else:
            while True:
                print(randart())
                username = input(Fore.GREEN + 'Username?: ')
                print(Fore.YELLOW + "Password will not be visible due to security reasons!")
                password = getpass.getpass(Fore.GREEN + 'Password?: ')
                print('Connecting....')
                time.sleep(1)
                try:
                    time.sleep(1)
                    user = scratchconnect.ScratchConnect(username, password)
                    break  # valid login, break out of the loop
                except scratchconnect.Exceptions.InvalidInfo as e:
                    os.system('cls')
                    time.sleep(1)
                    print(randart())
                    print(Fore.RED + str(e))
            os.system('cls')
            print(Style.RESET_ALL)
            print(randart())
            print(Fore.GREEN + 'Initializing...')
            print(user.site_health())
            os.system('cls')
            time.sleep(1)
        return user
    os.system('cls')
    # title
    winsound.Beep(500, 1000)
    os.system('title CloudTinker version 5.0')
    while True:
        user = login()
        # Connect To The Project
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        print(randart())
        project_id = input('Project id?: ')
        project1 = user.connect_project(project_id=project_id)
        os.system('cls')
        # Just Colors
        print(randart())
        print(Fore.MAGENTA + 'Project Connected Successfully Attempting To Connect To The Cloud Variables')
        print(Style.RESET_ALL)
        time.sleep(1)
        # Connect To Cloud Variables
        variables1 = project1.connect_cloud_variables()
        os.system('cls')
        # Setting up with inputs
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        print(randart())
        print(Fore.GREEN + 'All The Cloud Variables Connected Successfully!')
        time.sleep(1)
        os.system('cls')
        print(Style.RESET_ALL)
        os.system('cls')
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        print(randart())
        spam_delay = input(Fore.YELLOW + "Set The Spam Delay!: ")
        if '.' in spam_delay:
            sleep_duration = float(spam_delay)
        else:
            sleep_duration = int(spam_delay)
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        variable_count = int(input(Fore.YELLOW + "Number of variables to change?: "))
        variables = []
        values = []
        for i in range(variable_count):
            os.system('cls')
            print(Fore.GREEN + randart())
            variable_name = input(Fore.YELLOW + f'Variable {i+1}?: ')
            while True:
                try:
                    value = int(input(Fore.YELLOW + f'Value for Variable {i+1}?: '))
                    break
                except ValueError:
                    print(randart())
                    print(Fore.RED + "Invalid input. Please enter an integer value.")
            variables.append(variable_name)
            values.append(value)
        time.sleep(1)
        print(Style.RESET_ALL)
        os.system('cls')
        # Executing Main Script
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        time.sleep(1)
        print(Style.RESET_ALL)
        os.system('cls')
        print(randart())
        print(Fore.GREEN + 'Initiating...')
        winsound.PlaySound("SystemStart", winsound.SND_ALIAS)
        os.system('cls')
        time.sleep(1)
        os.system('cls')
        # Main Script
        try:
            while True:
                variables1 = project1.connect_cloud_variables()
                time.sleep(0.1)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                print(Fore.GREEN + 'Cloud Updated!')
                for variable, value in zip(variables, values):
                    try:
                        set = variables1.set_cloud_variable(variable_name=variable, value=value)
                        if set:
                            print(Fore.MAGENTA + f'Changed Cloud Var: {variable}')
                    except websocket.WebSocketBadStatusException as e:
                        print("WebSocketBadStatusException Occured!")
                        print("Status:", e.status)
                        print("Status message:", e.message)
                    except ssl.SSLEOFError:
                        print(Fore.RED + 'SSL EOF Error occurred. Retrying...')
                    except Exception as e:
                        print(Fore.RED + f'Error occurred: {e}')
                print(Fore.RED + 'PRESS CTRL+C TO QUIT!')
                time.sleep(sleep_duration)
                print(Style.RESET_ALL)
                os.system('cls')
        except KeyboardInterrupt:
            print(randart())
            print(Fore.GREEN + 'Stopping...')
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            time.sleep(1)
            os.system('cls')
            break
