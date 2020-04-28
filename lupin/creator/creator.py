from .voipapi import VoipAPI

class SessionCreator(VoipAPI):
    def __init__(self, token, timeout=None, sessions_dir=None):
        """
        Arguments:
            VoipAPI {class} -- Api 
            token {str} -- sms-activate.ru token
            count {int} -- Number of accounts to generate
            timeout {int} -- Timeout in seconds to wait for code
            callback {fucnction} -- Function to call after code retrieved. ex. func(code): pass
        """
        super().__init__(token, timeout=timeout, sessions_dir=sessions_dir)
    
    def ready(self):
        if self.count > 0:
            return True
        return False

    def start(self, count):
        # Check credit available > tot
        # Check count > 0
        # Start
        self.count = count
        while self.ready():
            print("Get activation")
            activation = self.get_activation()

            print("Get tgapi")
            tgapi = self.get_telegram_api(activation)
            print(tgapi)

            print("Asking code")
            if not self.ask_code(activation, tgapi):
                print("Skip")
                continue

            #activation.cancel()
            success = self.wait_code(activation, tgapi)
            
            if not success: 
                print("Skip")
                continue # Skip already used

            print("Success!")
            
            self.count-=1

            print(f"Remaining: {self.count}")
            

        else:
            print("Finito")
            return False

