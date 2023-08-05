import os
from datetime import datetime
from time import time

from Phone_central import format_phone_number, is_int
from Call import Call
from msort import sort


def simulate_call(pc):
    num1 = input("Input caller number: ")
    num1 = format_phone_number(num1)
    if num1 is None:
        print("Invalid format of phone number")
        return None
    user1 = pc.trie_phone_numbers.find(num1)
    if user1 is None:
        print("Non existing user")
        print("Did you mean?")

        user1 = give_suggestion(pc, num1)
        if user1 is None:
            return None

    if user1.number in pc.blocked:
        print("The caller is blocked, which means you can't make this call")
        return None

    num2 = input("Input number of person to be called: ")
    num2 = format_phone_number(num2)
    if num2 is None:
        print("Invalid format of phone number")
        return None
    user2 = pc.trie_phone_numbers.find(num2)
    if user2 is None:
        print("Non existing user")
        print("Did you mean?")

        user2 = give_suggestion(pc, num2)
        if user2 is None:
            return None

    if user2.number in pc.blocked:
        print("The called person is blocked, which means you can't make this call")
        return None

    if user1.number == user2.number:
        print("The user can't call himself")
        return None

    input("Press enter to start a call: ")
    start = datetime.now()
    input("Press enter to stop call: ")
    end = datetime.now()
    call = Call(user1.number, user2.number, start, end-start)
    pc.graph_calls.insert_edge(user1.vertex, user2.vertex, call)
    print(call)


def give_suggestion(pc, num):
    # start = time()
    top_suggestions = pc.suggestion_list(num)
    # end = time()
    # print("{0:2f}".format(end - start) + " sec")
    for i, suggestion in enumerate(top_suggestions):
        print(str(i + 1) + ". " + suggestion)
    option = input("Type serial number: ")
    if not is_int(option):
        print("Invalid option")
        return None
    option = int(option)
    if option > len(top_suggestions):
        print("Invalid option")
        return None
    return pc.trie_phone_numbers.find(top_suggestions[option - 1])


def load_calls(pc):
    # x = input("Input the name of the file in data folder(without extension and only .txt files allowed): ")
    # path = os.path.join(os.getcwd(), "data", x + ".txt")
    # if not os.path.isfile(path):
    #     print("File doesn't exist")
    # pc.load_calls_data(os.path.join(path))

    pc.load_calls_data(os.path.join(os.path.join(os.getcwd(), "data", "calls1.txt")))


def history_of_calls_2_numbers(pc):
    num1 = input("Input first number(place * at the end for autocomplete): ")
    num1, autocomplete = format_phone_number_search(num1)

    if num1 is None:
        print("Invalid format of phone number")
        return None

    if autocomplete:
        num1 = offer_autocomplete(num1, pc)
        if num1 is None:
            return None

    user1 = pc.trie_phone_numbers.find(num1)
    if user1 is None:
        print("No such user")
        return None

    num2 = input("Input second number(place * at the end for autocomplete): ")
    num2, autocomplete = format_phone_number_search(num2)
    if num2 is None:
        print("Invalid format of phone number")
        return None

    if autocomplete:
        num2 = offer_autocomplete(num2, pc)
        if num2 is None:
            return None

    user2 = pc.trie_phone_numbers.find(num2)
    if user2 is None:
        print("No such user")
        return None

    if user1.number == user2.number:
        print("The user can't call himself")
        return None

    edge_in = pc.graph_calls.get_edge(user1.vertex, user2.vertex)
    edge_out = pc.graph_calls.get_edge(user2.vertex, user1.vertex)
    if edge_in is None and edge_out is None:
        print("No calls were made")
        return None

    calls = []
    if edge_in is not None:
        calls.extend(edge_in.elements())
    if edge_out is not None:
        calls.extend(edge_out.elements())
    calls = sort(calls)
    for call in calls:
        print(call)


def history_of_calls_1_number(pc):
    num = input("Input number(place * at the end for autocomplete): ")
    num, autocomplete = format_phone_number_search(num)
    if num is None:
        print("Invalid format of phone number")
        return None

    if autocomplete:
        num = offer_autocomplete(num, pc)
        if num is None:
            return None

    user = pc.trie_phone_numbers.find(num)
    if user is None:
        print("No such user")
        return None
    calls = pc.graph_calls.find_all_elements_surrounding_edges(user.vertex)
    calls = sort_calls_by_popularity(calls, pc)
    for call in calls:
        print(str(call)+" and the called person popularity is "
              + str(pc.calculate_popularity(pc.trie_phone_numbers.find(call.num2))))


def offer_autocomplete(num, pc):
    users = pc.trie_phone_numbers.prefix_words(num)
    users = sort_by_popularity(users, pc)
    print_users(users, pc)
    option = input("Type serial number: ")
    if not is_int(option):
        print("Invalid option")
        return None
    option = int(option)
    if option > len(users):
        print("Invalid option")
        return None
    return users[option - 1].number


def search(pc):
    while True:
        print("1.Search by name")
        print("2.Search by surname")
        print("3.Search by phone number")
        print("B Back")
        x = input("Input option: ")

        if x == "1":
            name = name_surname_input("Input prefix of user's name: ")
            users = pc.trie_names.prefix_words(name)
            print_users(users, pc)

        elif x == "2":
            surname = name_surname_input("Input prefix of user's name: ")
            users = pc.trie_surnames.prefix_words(surname)
            print_users(users, pc)

        elif x == "3":
            phone = name_surname_input("Input prefix of user's name: ")
            phone = format_phone_number(phone)
            print(phone)
            if phone is None:
                print("Invalid phone input.")
                continue
            users = pc.trie_phone_numbers.prefix_words(phone)
            print_users(users, pc)

        elif x.lower() == "b":
            return None

        else:
            print("Invalid option")
            continue


def print_users(users, pc):
    if len(users) == 0:
        print("There are no users with this criteria")
        return None
    users = sort_by_popularity(users, pc)
    for index, user in enumerate(users):
        print(str(index+1) + ". " + str(user) + " with popularity " + str(pc.calculate_popularity(user)))
    return users


def sort_by_popularity(users, pc):
    return sorted(users, key=pc.calculate_popularity, reverse=True)


def sort_calls_by_popularity(calls, pc):
    return sorted(calls, key=lambda call: pc.calculate_popularity(pc.trie_phone_numbers.find(call.num2)), reverse=True)


def name_surname_input(message):
    x = input(message)
    return x.lower()


def format_phone_number_search(phone_str):
    phone = ""
    if phone_str == "":
        return None, False

    autocomplete = False
    if phone_str[-1] == "*":
        autocomplete = True
        phone_str = phone_str[:-1]

    allowed_chars = ["-", " ", "\n"]
    for char in phone_str:
        if char in allowed_chars:
            continue

        # ako je broj to je u redu i treba se dodati
        if is_int(char):
            phone += char
        # ako nije broj vraca se None
        else:
            return None, False
    return phone, autocomplete
