from pyrogram import Client, User, TermsOfService
from pyrogram.errors import exceptions
from pyrogram.errors import RPCError
from pyrogram.errors import FloodWait
from faker import Faker
import shutil, os, time

fake = Faker('it_IT')

api_id = 1332451
api_hash = "4a66a49e54166c9cff173f129de091b0"

def gen_person():
    person = fake.name().replace("-", " ")
    if person[-1] == " ":
        person = person[:-1]
    person = person.split(" ")
    surname, name = person[-1], " ".join(person[:-1])
    return name, surname

class TelegramLogin:
    def __init__(self, phone, session_dir):
        self.phone = phone
        self.session_dir = session_dir
        os.mkdir(self.session_dir)
        self.app = Client("app", api_id, api_hash, workdir=self.session_dir)
        self.app.connect()
    
    def request_code(self):    
        try:
            sent_code = self.app.send_code(self.phone)
            print(sent_code)

            if sent_code.type != "sms":
                self.bye()
                return False

        except exceptions.bad_request_400.PhoneNumberBanned:
            self.bye()
            return False

        self.sent_code = sent_code
        
        return True

    def create_session(self, code) -> User:
        signed_up = None
        signed_in = self.app.sign_in(self.phone, self.sent_code.phone_code_hash, code)

        if isinstance(signed_in, User):
            self.bye()
            return False

        first_name, last_name = gen_person()
        while not signed_up:
            try:
                signed_up = self.app.sign_up(self.phone, self.sent_code.phone_code_hash, first_name=first_name, last_name=last_name)

                if isinstance(signed_in, TermsOfService):
                    self.app.accept_terms_of_service(signed_in.id)

                self.app.disconnect()
                return signed_up
            
            except FloodWait as e:
                print("Sleeping ", e.x)
                time.sleep(e.x)


    def bye(self):
        self.app.disconnect()
        shutil.rmtree(self.session_dir)

# a = TelegramLogin("+639979731566", "5")
# res = a.request_code()
# if not res:
#     print("diocane eh")
# code = input("code: ")
# res = a.create_session(code)
# print(res)

# a.app.start()
# app = Client("app", api_id, api_hash, workdir="5")
# app.connect()
# app.disconnect()
# app.start()
# app.send_message("@abusefsbot","/start")
# app.send_message("@abusefsbot", "finally")
# app.stop()
