import sys
import UI
import pickle
from time import time

from Phone_central import PhoneCentral


def close():
    print("App is closing, please wait")
    pickle.dump(pc, open("phone_central.p", "wb"))
    sys.exit(1)


if __name__ == '__main__':
    # pc = PhoneCentral()
    # start = time()
    # pc.initialization()
    # pickle.dump(pc, open("phone_central.p", "wb"))
    # end = time()
    # print("{0:2f}".format(end - start))

    start = time()
    pc = pickle.load(open("phone_central.p", "rb"))
    end = time()
    print("{0:2f}".format(end - start))

    menu = {"1": UI.simulate_call, "2": UI.load_calls, "3": UI.history_of_calls_2_numbers,
            "4": UI.history_of_calls_1_number, "5": UI.search, "x": close}
    while True:
        print("1.Simulate call")
        print("2.Load more calls")
        print("3.History of calls for 2 numbers")
        print("4.History of calls for 1 number")
        print("5.Search")
        print("X Exit")
        x = input("Input option: ")
        if x.lower() == "x":
            break
        if x not in menu:
            print("Invalid option")
            continue
        x = x.lower()
        if x in menu:
            menu[x](pc)
    close()

