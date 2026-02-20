import sqlite3
import time

class CleanerDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
      
    def minus_complaint(self):
      with self.connection:
        self.cursor.execute("UPDATE `users` SET `complaintsCount` = `complaintsCount` - 1 WHERE `complaintsCount` <> 0")
        
class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
  
    def add_queue(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (user_id) VALUES (?)", (user_id,))

    def delete_queue(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE user_id = ?", (user_id,))

    def get_queue(self):
        with self.connection:
            queue = self.cursor.execute("SELECT * FROM `queue`").fetchmany(1)

            if bool(len(queue)):
                for row in queue:
                    return row[1]
            else:
                return False

    def create_chat(self, user_id, partner_id):
        if partner_id != 0:
            with self.connection:
                self.cursor.execute("INSERT INTO `chats` (user, partner) VALUES (?, ?)", (user_id, partner_id))
                return True

        return False

    def get_chat(self, user_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE user = ? OR partner = ?", (user_id, user_id))

            for i in chat:
                return [i[0], i[1] if i[1] != user_id else i[2]]

            return False
    
  
    def delete_chat(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE user = ? OR partner = ?", (user_id, user_id))

    def clear_chats_table(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats`")
  
    def user_exist(self, user_id):
      with self.connection:
        result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
        return bool(len(result))

    def add_user(self, user_id, username, connectTime, firstname, lastname, referral_id):
      with self.connection:
        self.cursor.execute("INSERT INTO `history` (user) VALUES (?)", (user_id,))
        self.cursor.execute("INSERT INTO `users` (`user_id`, `username`, `connectTime`, `firstname`, `lastname`, `referralID`) VALUES (?, ?, ?, ?, ?, ?)", (user_id, username, connectTime, firstname, lastname, referral_id,)) 

    def update_user(self, user_id, username, firstname, lastname):
      with self.connection:
        self.cursor.execute("UPDATE `users` SET `username` = ?, `firstname` = ?, `lastname` = ? WHERE user_id = ?", (username, firstname, lastname, user_id))

    def add_referral(self, user_id):
      with self.connection:
        self.cursor.execute(f"UPDATE `users` SET `referralCount` = `referralCount` + 1 WHERE user_id = {user_id}")

    def minus_referral(self, user_id):
      with self.connection:
        self.cursor.execute(f"UPDATE `users` SET `referralCount` = `referralCount` - 1 WHERE user_id = {user_id}")
  
    def get_referral(self, user_id):
      with self.connection:
        return self.cursor.execute(f"SELECT `referralCount` FROM `users` WHERE `user_id` = {user_id}").fetchone()
    
    def get_referral_list(self):
      with self.connection:
        referral_list_ = self.cursor.execute("SELECT `referralCount` FROM `users` ORDER BY `referralCount` DESC").fetchall()
        referral_list = []
        for i in referral_list_:
          referral_list.append(i[0])
          
        return referral_list
        
    def set_active(self, user_id, active):
      with self.connection:
        return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))

    def add_complaint(self, user_id):
      with self.connection:
        self.cursor.execute(f"UPDATE `users` SET `complaintsCount` = `complaintsCount` + 1 WHERE user_id = {user_id}")
  
    def set_complaint(self, user_id, count):
      with self.connection:
        self.cursor.execute(f"UPDATE `users` SET `complaintsCount` = {count} WHERE user_id = {user_id}")

    def get_complaint(self, user_id):
      with self.connection:
        return self.cursor.execute(f"SELECT `complaintsCount` FROM `users` WHERE `user_id` = {user_id}").fetchone()
    
    def get_users(self):
      with self.connection:
        return self.cursor.execute("SELECT * FROM `users`").fetchall()

    def user_history(self, user_id):
      with self.connection:
        return self.cursor.execute(f"SELECT `partner` FROM `history` WHERE `user_id` = {user_id}").fetchone()

  
    def get_queue_users(self):
      with self.connection:
        return self.cursor.execute("SELECT * FROM `queue`").fetchall()
  
    def get_user_history(self, user_id):
      with self.connection:
        return self.cursor.execute(f"SELECT * FROM `history` WHERE `user` = {user_id}").fetchone()

    def set_user_history(self, user_id, partner_id):
      with self.connection:
        self.cursor.execute("UPDATE `history` SET `partner` = ? WHERE `user` = ?", (partner_id, user_id))
        
    def set_user_opinion(self, user_id, opinion_id):
      with self.connection:
        self.cursor.execute("UPDATE `history` SET `opinionID` = ? WHERE `user` = ?", (opinion_id, user_id))   

    def add_rating(self, user_id):
      with self.connection:
        self.cursor.execute(f"UPDATE `users` SET `rating` = `rating` + 1 WHERE user_id = {user_id}")

    def minus_rating(self, user_id, quantity):
      with self.connection:
        now_rating = self.cursor.execute(f"SELECT `rating` FROM `users` WHERE `user_id` = {user_id}").fetchone()[0]
        if now_rating >= quantity:
          self.cursor.execute(f"UPDATE `users` SET `rating` = `rating` - {quantity} WHERE user_id = {user_id}")
        else:
          self.cursor.execute(f"UPDATE `users` SET `rating` = 0 WHERE user_id = {user_id}")

    def get_rating(self, user_id):
      with self.connection:
        return self.cursor.execute(f"SELECT `rating` FROM `users` WHERE `user_id` = {user_id}").fetchone()

    def get_rating_list(self):
      with self.connection:
        rating_list_ = self.cursor.execute("SELECT `rating` FROM `users` ORDER BY `rating` DESC").fetchall()
        rating_list = []
        for i in rating_list_:
          rating_list.append(i[0])
        return rating_list

    def get_mut_time(self, user_id):
      with self.connection:
        mut_time =  self.cursor.execute(f"SELECT `mutTime` FROM `users` WHERE `user_id` = {user_id}").fetchone()
        return mut_time[0]
        
    def get_status(self, user_id):
      with self.connection:
        mutTime = self.cursor.execute(f"SELECT `mutTime` FROM `users` WHERE `user_id` = {user_id}").fetchone()
        if int(mutTime[0]) <= int(time.time()):
          status = "FREE"
          self.cursor.execute(f"UPDATE `users` SET `status` = 'FREE' WHERE user_id = {user_id}")
          self.cursor.execute(f"UPDATE `users` SET `mutTime` = 0 WHERE user_id = {user_id}")
        else:
          status = "MUT"
        return status       
    def give_free_status(self, user_id):
      with self.connection:
        self.cursor.execute(f"UPDATE `users` SET `status` = 'FREE' WHERE user_id = {user_id}")
        self.cursor.execute(f"UPDATE `users` SET `mutTime` = 0 WHERE user_id = {user_id}")
  
    def give_mut_status(self, user_id, mutTime):
      with self.connection:
        mutTime = int(time.time()) + (int(mutTime) * 60 * 60)
        self.cursor.execute(f"UPDATE `users` SET `status` = 'MUT' WHERE user_id = {user_id}")
        self.cursor.execute("UPDATE `users` SET `mutTime` = ? WHERE user_id = ?", (mutTime, user_id,))
