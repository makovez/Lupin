import time, glob
from smsactivateru import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber, SetStatus, GetStatus
from lupin.creator.tgapi import TelegramLogin


class SmsTypesPlus(SmsTypes):
    def __init__(self):
        super()
    SmsTypes.Country.PA = '87'
    SmsTypes.Country.IT = '86'


class VoipAPI:

    def __init__(self, token, timeout=60, sessions_dir = "lupin/sessions/"):
        self.sessions_dir = sessions_dir
        self.timeout = timeout
        self.wrapper = Sms(token)

    def get_balance(self):
        balance = GetBalance().request(self.wrapper)
        print('Current balance: {} rub.'.format(balance))
        return balance

    def get_telegram_slots(self):
        #getting free slots (count available phone numbers for each services)
        available_phones = GetFreeSlots(
            country=SmsTypesPlus.Country.PA
        ).request(self.wrapper)

        print('Telegram: {} available'.format(available_phones.Telegram.count))

        return available_phones.Telegram.count

    def get_activation(self):
        # try get phone for youla.io
        activation = GetNumber(
            service=SmsService().Telegram,
            country=SmsTypesPlus.Country.PA,
            operator=SmsTypesPlus.Operator.any
        ).request(self.wrapper)
        # show activation id and phone for reception sms
        print('id: {} phone: {}'.format(str(activation.id), str(activation.phone_number)))
    
        return activation
    
    def get_status_activation(self, activation):
        # getting and show current activation status
        response = GetStatus(id=activation.id).request(self.wrapper)
        return response
    
    def cancel_activation(self, activation):
        set_as_cancel = SetStatus(
            id=activation.id,
            status=SmsTypesPlus.Status.Cancel
        ).request(self.wrapper)

        return set_as_cancel

    def ask_code(self, activation, tgapi):
        # send phone number to pyrogram
        res = tgapi.request_code()
        if not res: # Banned
            activation.mark_as_used()
            print("[!] Banned or already used")
        else:
            # set current activation status as SmsSent (code was sent to phone)
            activation.was_sent()

        return res

    def wait_code(self, activation, tgapi):
        success = False
        try:
            code = activation.wait_code(wrapper=self.wrapper, timeout=120) #TODO: impostare questo da classe
            #print(code)
            success = tgapi.create_session(code)
            #print(success)
            if not success:            
                #activation.mark_as_used()
                activation.cancel()
                print("[!] Creating session returned False")


        except TypeError: # Timeout error
            activation.cancel()
            tgapi.bye()
            print("[!] Timeout sms-activate expired")
            pass

        return success

    def get_count_sessions(self):

        count = len(glob.glob(self.sessions_dir + "*") )
        print(f"Total count: {count}")
        return count

    def get_telegram_api(self, activation):
        number = "+" + str(activation.phone_number)
        self.get_count_sessions()
        max_session = max([int(session_dir.split("/")[-1]) for session_dir in glob.glob("lupin/sessions/*")])
        session_folder = max_session + 1

        return TelegramLogin(number, self.sessions_dir+str(session_folder))

    
        

    


    


