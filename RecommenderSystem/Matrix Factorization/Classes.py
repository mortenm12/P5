class Movie:
    def __init__(self, m_id):
        self.id = m_id
        self.rating = 0
        self.bias = 0

    def set_average_rating(self, number):
        self.rating = number

    def set_bias(self, number):
        self.bias = number


class User:
    def __init__(self, u_id):
        self.id = u_id
        self.bias = 0

    def set_bias(self, number):
        self.bias = number
