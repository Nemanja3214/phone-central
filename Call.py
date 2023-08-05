class Call(object):
    __slots__ = "_num1", "_num2", "_time_of_begining", "_time_lasted"

    def __init__(self, num1, num2, time_of_begining=None, time_lasted=None):
        self._num1 = num1
        self._num2 = num2
        self._time_of_begining = time_of_begining
        self._time_lasted = time_lasted

    @property
    def num1(self):
        return self._num1

    @num1.setter
    def num1(self, value):
        self._num1 = value

    @property
    def num2(self):
        return self._num2

    @num2.setter
    def num2(self, value):
        self._num2 = value

    @property
    def time_of_begining(self):
        return self._time_of_begining

    @time_of_begining.setter
    def time_of_begining(self, value):
        self._time_of_begining = value

    @property
    def time_lasted(self):
        return self._time_lasted

    @time_lasted.setter
    def time_lasted(self, value):
        self._time_lasted = value

    def __str__(self):
        return "Caller is " + self._num1 + ", called number is " + self._num2 + ", call started " +\
               str(self._time_of_begining) + " and it lasted for "\
               + str(self._time_lasted)

    def __lt__(self, other):
        return self.time_of_begining < other.time_of_begining

    def __gt__(self, other):
        return self.time_of_begining > other.time_of_begining
