from pyrogram import Client, Filters
import glob, datetime, time, shutil
from pyrogram.errors.exceptions import ChatWriteForbidden, FloodWait, PeerFlood, Forbidden, PeerIdInvalid, UserDeactivatedBan, UserNotMutualContact


class Adder:
    def __init__(self, workdir, api_id, api_hash):
        self.workdir = workdir
        self.api_id = api_id
        self.api_hash = api_hash
        self.proxy = []
        self.apps = self.load_apps()

    def start_deamon_proxy(self, apps_count):
        """Update list proxy every minute"""
        pass

    def load_apps(self):
        apps = []
        #apps = [Client("app", workdir=session_dir, api_id=self.api_id, api_hash=self.api_hash) for session_dir in glob.glob(self.workdir + "*")]
        for session_dir in glob.glob(self.workdir + "*"):
            try:
                app = Client("app", workdir=session_dir, api_id=self.api_id, api_hash=self.api_hash)
                app.start()
                apps.append(app)
                print("[OK] Loaded: ", session_dir)
            except UserDeactivatedBan:
                print("[RIP] Account bannato: ", session_dir)
                shutil.rmtree(session_dir)
            
        return apps


    def stop_all(self):
        for app in self.apps:
            app.stop()

    def send_message(self, user, text):
        for app in self.apps:
            try:
                app.send_message(user, text)
                print(app.get_me().phone_number)
            except Exception as e:
                print(e)
                pass

    def get_members(self, app, chat, limit=200, all_members=False):
        members = []
        hours_ago = int((datetime.datetime.utcnow() - datetime.timedelta(hours=3)).strftime("%s"))
        for member in app.iter_chat_members(chat):   
            if limit and len(members) > limit:
                break
            if not all_members and member.user and member.status is "member" and member.user.last_online_date:
                if member.user.last_online_date < hours_ago:
                    members.append(member.user.username)

            elif all_members and member.user:
                members.append(member.user.username)

        return members

    
    def get_diff_members(self, from_chat, to_chat, limit=200):
        for app in self.apps:
            try:
                from_chat_members = self.get_members(app, from_chat, limit=limit)
                to_chat_members = self.get_members(app, to_chat, limit=None, all_members=True)

                final_members = list(set(from_chat_members) - set(to_chat_members))

                print("Membri totali da aggiungere: ", len(final_members))
                return final_members
            except UserDeactivatedBan:
                self.apps.pop(self.apps.index(app))
                pass



    def add_member(self, app, chat, user):
        try:
            res = app.add_chat_members(chat, user)
            print("Risposta", res)
            if res: print("[OK] ", user)
            return True
        except ChatWriteForbidden:
            print("[!] Not joined yet, joining... > ", app.workdir)
            app.join_chat(chat)
            return self.add_member(app, chat, user)
        except PeerFlood:
            print("[!!] Account limitato > ", app.workdir)
            self.apps.pop(self.apps.index(app))
            return "limited"
        except UserDeactivatedBan:
            print("[RIP] Account bannato > ", app.workdir)
            self.apps.pop(self.apps.index(app))
            shutil.rmtree(app.workdir)
            return "ban"
        except FloodWait as e:
            print("Sleeping ", e.x, " > ", app.workdir)
            return self.add_member(app, chat, user)
        except Forbidden:
            print("[!] Forbidden: ", user)
            return False
        except PeerIdInvalid:
            print("[!] PeerIdInvalid: ", user)
            return False
        except UserNotMutualContact:
            print("[!] UserNotMutualContact: ", user)
            return False


    
    def run(self, from_chat, to_chat, limit=1000):

        count = 0
        MAX_PER_VOIP = 40
        members = self.get_diff_members(from_chat, to_chat, limit=limit)

        while count < len(members):
            if count >= MAX_PER_VOIP:
                #MAX_PER_VOIP = MAX_PER_VOIP
                print("Sleepping to prevent limitation")
                time.sleep(120)


            for app in self.apps:

                member = members[count]
                res = self.add_member(app, to_chat, member)
                if res is False:
                    members.pop(count)

                else:
                    time.sleep(2.5)
                    count+=1

                print("Total", count)
            

                





    
    
    
        


    
