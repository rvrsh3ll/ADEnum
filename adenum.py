#!/usr/bin/env python
# -*- coding: utf-8 -*-
#title           :adenum.py
#description     :This program allows the user to enumerate active directory via LDAP queries.
#author          : @424f424f
#date            : 1/30/2016
#version         :0.1
#usage           :python adenum.py
#notes           :
#python_version  :2.7.6  
#=======================================================================
 
# Import the modules needed to run the script.
import sys, os, subprocess, re

# Main definition - constants
menu_actions  = {}  
hostname = ''
binddn = ''

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():
    os.system('clear')
    
    header = """\
         / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
        ( L | D | A | P ) ( E | n | u | m | e | r | a | t | o | r )
         \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/
    """
    print header
    print "Please enter your settings and begin your enumeration:"
    print "1. Enter DC/ldap address or hostname: %s" % hostname
    print "2. Enter the bind DN: %s" % binddn
    print "3. Begin LDAP Search"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    search_menu(choice)
 
    return
 
# Search menu
def search_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return
 
# LDAP Menu
def menu1():
    print "Enter DC/ldap address or hostname (penlab-dc)\n"
    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    while choice not in [9, 0]:
        global hostname
        hostname = choice
        main_menu()
    search_menu(choice)
    return
 
 
# Bind Menu
def menu2():
    print "Enter bind DN (user@domain.com)\n"
    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    while choice not in [10, 0]:
        global binddn
        binddn = choice
        regex = re.compile('.+@([^.]+)\..+')
        global tld
        match = re.match(regex, binddn)
        tld = match.group(1)
        global ext
        ext = choice.split('.')[1]
        main_menu()
    search_menu(choice)
    return

# Bind Menu
def menu3():
    print "Search Menu\n"
    print "1. Return all users"
    print "2. Return all info on a user"
    print "3. List all groups"
    print "4. List users of a specific group"
    print "5. List all groups a user is a member of"
    print "6. List OU's"
    print "7. List Domain Controllers"
    print "8. List all computers"
    print "9. List all File Servers"
    print "10. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    if choice == "1":
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(&(samAccountType=805306368))" -W""".format(hostname, tld, ext, binddn)
        print ""
        print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        menu3()
    if choice == "2":
        username = raw_input(" Enter Username >> ")
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(samAccountName="{}")" -W""".format(hostname, tld, ext, binddn, username)
        print ""
        print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        menu3()
    if choice == "3":
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(objectcategory=group)" -W""".format(hostname, tld, ext, binddn)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep", "name:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
        output.stdout.close()
        out,err = output2.communicate()
        print ""
        print out
        menu3()
    if choice == "4":
        groupname = raw_input(" Enter group >> ")
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "cn={}" -W""".format(hostname, tld, ext, binddn, groupname)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep", "member:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
        output.stdout.close()
        out,err = output2.communicate()
        print ""
        print out
        menu3()
    if choice == "5":
        username = raw_input(" Enter Username >> ")
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(samAccountName="{}")" -W""".format(hostname, tld, ext, binddn, username)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep", "memberOf:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
        output.stdout.close()
        out,err = output2.communicate()
        print ""
        print out
        menu3()
    if choice == "6":
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(OU=*)" -W""".format(hostname, tld, ext, binddn)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep", "ou:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
        output.stdout.close()
        out,err = output2.communicate()
        print ""
        print out
        menu3()
    if choice == "7":
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(&(objectcategory=Computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))" -W""".format(hostname, tld, ext, binddn)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep", "name:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
        output.stdout.close()
        out,err = output2.communicate()
        print ""
        print out
        menu3()
    if choice == "8":
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(objectcategory=Computer)" -W""".format(hostname, tld, ext, binddn)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep", "name:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
        output.stdout.close()
        out,err = output2.communicate()
        print ""
        print out
        menu3()
    if choice == "9":
        cmd = """ldapsearch -x -h {} -b "dc={},dc={}" -D {} "(&(samAccountType=805306368))" -W""".format(hostname, tld, ext, binddn)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
        with output.stdout:
            print ""
            for line in iter(output.stdout.readline, b''):
                if ("homeDirectory" or "scriptPath" or "profilePath") in line:
                    print "Results:"
                    print ""
                    m = re.search(r'\\\\([^\\]*)\\', line)
                    if m:
                        print m.group(1)
        output.wait()
        print ""
        menu3()
    search_menu(choice)
    return
 
# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    sys.exit()
 
# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '10': back,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
