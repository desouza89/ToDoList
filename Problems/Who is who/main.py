class Plant:
    def __init__(self, spec):
        self.spec = spec


class Cactus(Plant):
    pass

basil = Plant("Ocimum basilicum")

opuntia = Cactus("Opuntia vulgaris")


print(isinstance(opuntia, object))
print(type(basil) == object)
print(isinstance(opuntia, Plant))
print(type(basil) == Cactus)
print(type(opuntia) == Cactus)
print(isinstance(basil, Plant))
