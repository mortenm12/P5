from ContentBased import calculate_n_recommendations


def regular_mode():
    s = ''
    while not str.isdigit(s):
        print("What user do you want recommendations for?")
        s = input()
        if not str.isdigit(s):
            print("That is not an integer dumbass!")
    u_id = int(s)
    recommendations = calculate_n_recommendations("Test1", u_id, 10)
    for recommendation in recommendations:
        print("Movie " + "{:4d}".format(recommendation[0]) + " with weight " + "{:1.2f}".format(recommendation[1]))


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
