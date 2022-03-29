from cgi import test
from datetime import datetime, timedelta
from datetime import time

import unittest

import pytz

from connect_to_db import connect_to_db

class TestDB(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)
        print('Connecting to db.....')
        self.db = connect_to_db()
        self.create_lady_data()
    
    def test_checkin_false(self):
        discord_id = "GHOST"
        guild_id = "TEST"
        check = self.db.check_in(discord_id, guild_id)
        self.assertFalse(check)
    
    def test_checkactive_false(self):
        discord_id = "GHOST"
        guild_id = "TEST"
        check = self.db.check_active(discord_id, guild_id)
        self.assertFalse(check)
    
    def test_checkcomplete_false(self):
        discord_id = "GHOST"
        guild_id = "TEST"
        check = self.db.check_complete(discord_id, guild_id)
        self.assertFalse(check)
    

    def test_add_delete_user(self):
        discord_id = "BOY"
        first = 'G'
        last = 'BOY'
        guild_id = "TEST"
        timezone = 'UTC'
        false_check = self.db.check_active(discord_id, guild_id)
        self.assertFalse(false_check)
        self.db.add_user(discord_id,first,last,timezone,guild_id,"00000")
        true_check = self.db.check_active(discord_id, guild_id)
        self.assertTrue(true_check)
        self.db.delete_user(discord_id, guild_id)
        false_check = self.db.check_active(discord_id, guild_id)
        self.assertFalse(false_check)

    def test_collision_true(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,2,22,9,0,0,0)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertTrue(check)

    def test_collision_before_false(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,2,22,7,0,0,0)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertFalse(check)

    def test_collision_after_false(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,2,22,19,0,0,0)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertFalse(check)

    def test_collision_true_tz(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,2,22,9,0,0,0)
        tz = pytz.timezone("UTC")
        test_time = tz.localize(test_time)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertTrue(check)

    def test_collision_false_tz(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,2,22,7,0,0,0)
        tz = pytz.timezone("UTC")
        test_time = tz.localize(test_time)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertFalse(check)

    def test_collision_afterin_true(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,2,23,9,0,0,0)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertTrue(check)

    def test_collision_afterin_true_long(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        test_time = datetime(2022,3,9,9,0,0,0)
        check = self.db.check_timestamp_collision(test_time,discord_id,guild_id)
        self.assertTrue(check)
    
    def test_check_manager_promote_demote(self):
        discord_id = 'LADY'
        guild_id = 'TEST'
        check = self.db.check_manager(discord_id,guild_id)
        self.assertTrue(check)

        self.db.demote_manager(discord_id, guild_id)
        check = self.db.check_manager(discord_id,guild_id)
        self.assertFalse(check)

        self.db.promote_manager(discord_id, guild_id)
        check = self.db.check_manager(discord_id,guild_id)
        self.assertTrue(check)

    def test_clock_in_wont_work_cases(self):
        # already clocked in
        discord_id = 'LADY'
        guild_id = 'TEST'
        check = self.db.check_in(discord_id, guild_id)
        self.assertTrue(check)
        self.assertFalse(self.db.clock_user_in(discord_id, guild_id))
        
        # not registered
        discord_id = 'GHOST'
        check = self.db.check_in(discord_id, guild_id)
        self.assertFalse(check)
        self.assertFalse(self.db.clock_user_in(discord_id, guild_id))

    def test_clock_in_out(self):
        discord_id = 'MAN'
        guild_id = 'TEST'
        check = self.db.check_in(discord_id, guild_id)
        self.assertFalse(check)
        self.assertTrue(self.db.clock_user_in(discord_id, guild_id))
        check = self.db.check_in(discord_id, guild_id)
        self.assertTrue(check)

        self.assertTrue(self.db.clock_user_out(discord_id, guild_id))
        check = self.db.check_in(discord_id, guild_id)
        self.assertFalse(check)
        check = self.db.check_complete(discord_id, guild_id)
        self.assertTrue(check)


    def test_checkin_true(self):
        discord_id = "LADY"
        guild_id = "TEST"
        check = self.db.check_in(discord_id, guild_id)
        self.assertTrue(check)
    
    def test_checkactive_true(self):
        discord_id = "LADY"
        guild_id = "TEST"
        check = self.db.check_active(discord_id, guild_id)
        self.assertTrue(check)
    
    def test_checkcomplete_true(self):
        discord_id = "LADY"
        guild_id = "TEST"
        check = self.db.check_complete(discord_id, guild_id)
        self.assertTrue(check)

    def create_lady_data(self):
        discord_id = 'MAN'
        guild_id = 'TEST'
        first = 'TESTING'
        last = 'MAN'
        timezone = 'UTC'

        records = self.db.get_employee_records(guild_id)

        new_employee = {
                'discord_id' : discord_id,
                'name_first' : first,
                'name_last' : last,
                'timezone' : timezone,
                'manager' : False
            }

        if len(list(records.find({'discord_id' : discord_id}))) == 0:
            records.insert_one(new_employee)

        discord_id = 'LADY'
        guild_id = 'TEST'
        first = 'TESTING'
        last = 'LADY'
        timezone = 'UTC'
        new_employee = {
                'discord_id' : discord_id,
                'name_first' : first,
                'name_last' : last,
                'timezone' : timezone,
                'manager' : True
            }

        if len(list(records.find({'discord_id' : discord_id}))) == 0:
            records.insert_one(new_employee)

        
        out_time_first_shift = datetime(2022, 2, 22, 16, 00, 00, 0)
        in_time_first_shift = datetime(2022, 2, 22, 8, 00, 00, 0)
        in_time_second_shift = datetime(2022, 2, 23, 8, 00, 00, 0)
        
        if not self.db.check_in(discord_id, guild_id):   
           new_in_time = {
                'discord_id' : discord_id,
                'in_time' : in_time_second_shift}
           ins = self.db.get_active_shifts(guild_id)
           ins.insert_one(new_in_time)
        
        if not self.db.check_complete(discord_id, guild_id):
            time_clock = {
                'discord_id' : discord_id,
                'in_time' : in_time_first_shift,
                'out_time' : out_time_first_shift,
                'seconds_worked' : (out_time_first_shift - in_time_first_shift).total_seconds(),
                'comments' : '',
                'paid' : False
            }
            complete = self.db.get_complete_shifts(guild_id)
            complete.insert_one(time_clock)
            
           


if __name__ == '__main__':
    unittest.main()
