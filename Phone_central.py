from difflib import SequenceMatcher

from Call import Call
from Trie import Trie
import os
from graph import Graph
from time import time
from datetime import datetime, timedelta

from User import User


class PhoneCentral(object):
    __slots__ = "_trie_phone_numbers", "_trie_names", "_trie_surnames", "_graph_calls", "_blocked", "_non_blocked"

    def __init__(self):
        self._trie_phone_numbers = Trie()
        self._trie_names = Trie()
        self._trie_surnames = Trie()
        self._graph_calls = Graph(True)
        self._blocked = set()
        self._non_blocked = set()

    def initialization(self):
        self.load_users_data()
        self.load_calls_data()
        self.load_blocked_data()

    def load_users_data(self):
        with open(os.path.join(os.getcwd(), "data", "phones.txt"), "r") as file:
            line = file.readline()
            while line != "":
                # print(line)
                full_name, phone_str = line.split(",")
                full_name = full_name.strip()
                name, surname = full_name.split(" ")
                phone = format_phone_number(phone_str)
                # ako je phone None preskace se red
                if phone is None:
                    line = file.readline()
                    continue
                # dodaje se telefon u trie a vrednost lista je korisnik
                user = User(name, surname, phone)
                self._non_blocked.add(phone)

                # trie_node = self._trie_phone_numbers.insert(phone, user)
                self._trie_phone_numbers.insert(phone, user)
                self._trie_names.insert(name, user)
                self._trie_surnames.insert(surname, user)
                # dodaje se vertex sa vrednoscu objekta i cuva se vertex referenca u objektu, dvosmerno
                vertex = self._graph_calls.insert_vertex(user)
                user.vertex = vertex

                # dvosmerno nije potrebno sa trie
                # user.trie_node = trie_node
                # print(user)
                line = file.readline()

    @property
    def trie_phone_numbers(self):
        return self._trie_phone_numbers

    @trie_phone_numbers.setter
    def trie_phone_numbers(self, value):
        self._trie_phone_numbers = value

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, value):
        self._blocked = value

    @property
    def trie_names(self):
        return self._trie_names

    @trie_names.setter
    def trie_names(self, value):
        self._trie_names = value

    @property
    def trie_surnames(self):
        return self._trie_surnames

    @trie_surnames.setter
    def trie_surnames(self, value):
        self._trie_surnames = value

    @property
    def graph_calls(self):
        return self._graph_calls

    def load_calls_data(self, path=None):
        # i = 0
        if path is None:
            path = os.path.join(os.getcwd(), "data", "calls.txt")
        with open(path, "r") as file:
            line = file.readline()
            while line != "":
                # print(line)
                caller, called, time_began, lasted_temp = line.split(",")

                caller = format_phone_number(caller)
                # ako je phone None preskace se red
                if caller is None:
                    line = file.readline()
                    continue

                called = format_phone_number(called)
                # ako je phone None preskace se red
                if called is None:
                    line = file.readline()
                    continue

                # 23.02.2020 17:52:43,
                time_began = datetime.strptime(time_began.strip(), "%d.%m.%Y %H:%M:%S")
                lasted_temp = datetime.strptime(lasted_temp.strip(), "%H:%M:%S")
                lasted = timedelta(hours=lasted_temp.hour, minutes=lasted_temp.minute, seconds=lasted_temp.second)
                call = Call(caller, called, time_began, lasted)
                print(call)
                # objekti klase user
                caller = self._trie_phone_numbers.find(caller)
                called = self._trie_phone_numbers.find(called)

                self._graph_calls.insert_edge(caller.vertex, called.vertex, call)
                line = file.readline()
                # i+=1

    def calculate_popularity(self, user):
        graph_node = user.vertex

        # duzina primljenih poziva
        timedelta_of_calls = 0
        incoming_calls = self._graph_calls.find_all_elements_incoming_edges(graph_node)
        for call in incoming_calls:
            timedelta_of_calls += call.time_lasted.total_seconds()

        # broj primljenih poziva
        num_of_incoming = len(incoming_calls)

        # broj pozivalaca svih pozivalaca ovog korisnika
        num_off_incoming_to_caller = 0
        # za svakog suseda koji je pozvao
        for edge in self._graph_calls.incident_edges(graph_node, False):
            # dodaj koliko je poziva upuceno ka njemu
            num_off_incoming_to_caller += self._graph_calls.degree(edge.origin, False)

        return num_of_incoming * 2 + timedelta_of_calls * 3 + num_off_incoming_to_caller * 4

    def load_blocked_data(self):
        with open(os.path.join(os.getcwd(), "data", "blocked.txt"), "r") as file:
            line = file.readline()
            while line != "":
                num = format_phone_number(line.strip())
                if num is None:
                    continue
                self._blocked.add(num)
                self._non_blocked.remove(num)
                line = file.readline()

    def suggestion_list(self, input_number):
        return find_best(self._non_blocked.union(self._blocked), input_number, 5)


def find_best(collection, input_number, best_number=5):
    result_list = [None] * best_number
    similarities = {}

    for element in collection:
        for result_index, result in enumerate(result_list):
            if result is None:
                result_list[result_index] = element
                break

            if similarities.get(element) is None:
                similarities[element] = similar(input_number, element)

            if similarities.get(result) is None:
                similarities[result] = similar(input_number, result)

            if similarities.get(element) > similarities.get(result):
                insert_in_position(result_list, result_index, element)
                break

    return result_list


def insert_in_position(collection, position, element):
    n = len(collection)
    current_position = n - 1

    while current_position > position:
        collection[current_position] = collection[current_position - 1]
        current_position -= 1

    collection[position] = element


def format_phone_number(phone_str):
    phone = ""
    if phone_str == "":
        return None
    allowed_chars = ["-", " ", "\n"]
    for char in phone_str:
        # crta i space su dozvoljeni
        if char in allowed_chars:
            continue

        # ako je broj to je u redu i treba se dodati
        if is_int(char):
            phone += char
        # ako nije broj vraca se None
        else:
            return None
    return phone


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
