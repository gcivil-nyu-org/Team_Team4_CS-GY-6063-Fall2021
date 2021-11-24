#!/usr/bin/env python
# coding=utf-8
import sys
import os
import django

def populate_test_accounts():
    cur_path = os.getcwd()
    sys.path.append(cur_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'StudyCity.settings'
    
    django.setup()
    from accounts.models import Profile
    from django.contrib.auth.models import User

    usernames = ["prof_test","ta_test","test1","test2","test3","test4","test5"]
    business = [True, False, True, True, False, False, False]
    password = "studycity"
    for idu, user_name in enumerate(usernames):
        user = User.objects.filter(username = user_name)
        if not user:
            user = User.objects.create(username = user_name,
                password = password, email = user_name+"@gmail.com")
            user.set_password(password)
            user.save()
            print("Create an account for " + user_name + ".")
        else:
            print(user_name+" has been created before.")
            user = user[0]
        Profile.objects.filter(user=user).update(business_account=business[idu]) 

def main():
    populate_test_accounts()

if __name__ == '__main__':
    main()
