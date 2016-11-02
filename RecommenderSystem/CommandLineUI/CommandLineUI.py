def regular_mode():
    s = ''
    while not str.isdigit(s):
        print("What user do you want recommendations for?")
        s = input()
        if not str.isdigit(s):
            print("That is not an integer dumbass!")
    u_id = int(s)



def debug_mode():
    print("debug")

s = ''
debug = False
while s not in ['Y', 'N']:
    print("Debug mode? (Y/N)")
    s = input()
    if s not in ['Y', 'N']:
        print("Invalid input, please try again.")
if s == 'Y':
    debug = True
elif s == 'N':
    debug = False

if debug:
    debug_mode()
else:
    regular_mode()
