from lupin.creator import SessionCreator
from lupin.adder import Adder
import yaml, sys, time, os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

lupin_logo = r"""
  o                                     o              
 <|>                                  _<|>_            
 / \                                                   
 \o/           o       o   \o_ __o      o    \o__ __o  
  |           <|>     <|>   |    v\    <|>    |     |> 
 / \          < >     < >  / \    <\   / \   / \   / \ 
 \o/           |       |   \o/     /   \o/   \o/   \o/ 
  |            o       o    |     o     |     |     |  
 / \ _\o__/_   <\__ __/>   / \ __/>    / \   / \   / \ 
                           \o/                         
                            |                          
                           / \                    
"""

testo = """
1. Generare accounts
2. Addare accounts
"""

with open("config.yaml") as f:
    CONF = yaml.load(f, Loader=yaml.FullLoader)

def check_conf():
    if CONF["SESSIONS_DIR"][-1] != "/":
        sys.exit("SESSIONS_DIR must end with /")


def realize_choice(choice):
    cls() # Clear
    print(bcolors.WARNING + lupin_logo + bcolors.ENDC)
    if choice is "1":
        creator = SessionCreator(CONF["SMSACTIVATE_API_KEY"], sessions_dir=CONF["SESSIONS_DIR"])
        creator.get_balance()
        creator.get_telegram_slots()
        print("")
        if input("Vuoi procedere ? [y/n] > ").lower() != 'y':
            return
        num = input("Inserisci numero account da generare: ")
        if num.isdigit():   
            creator.start(count=int(num))


    elif choice is "2":
        print("still nothing")

        adder = Adder(CONF["SESSIONS_DIR"], CONF["API_ID"], CONF["API_HASH"])
        #print(adder.apps[0].workdir)
        #adder.start_all()
        #adder.send_message("@soermejo", "ciao")
        #adder.get_members("pyrogramchat")
        #adder.add_member("@DsquaredTv", "@lascamorza")
        #res = adder.get_diff_members("@pyrogramchat", "@DsquaredTv")
        #print(res[0], len(res))
        adder.run("@cazzatemanontroppeSOLOPERVIP", "@DsquaredTv", 1000)
        adder.stop_all()
        print("fatto")
    else:
        print("Scegli una valida opzione!")

cls() # Clear
check_conf()

#print(bcolors.WARNING + lupin_logo + bcolors.ENDC)

while True:
    try:
        print(bcolors.WARNING + lupin_logo + bcolors.ENDC)
        print(testo)
        choice = input("Cosa vuoi fare? > ")
        
        realize_choice(choice)
    except KeyboardInterrupt:
        print("OK")
        break

