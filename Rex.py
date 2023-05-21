import copy


class ReX:
    """collects common for all regular expressions properties and methods"""

    def __str__(self):
        if isinstance(self, EmptyReX):
            return "empty"
        if isinstance(self, NilReX):
            return "nil"
        if isinstance(self, SingleReX):
            return self._data[0]
        if isinstance(self, StarReX):
            return f"{str(self._data[0])}*"
        if isinstance(self, CatReX):
            return f"({str(self._data[0])} . {str(self._data[1])})"
        # self is an instance of type AltReX
        return f"({str(self._data[0])} | {str(self._data[1])})"

    @property
    def is_nil_aMember(self) -> bool:
        """realises function E: ReX -> bool that determines whether 'self'
        is in the language specified by the function argument"""
        if isinstance(self, EmptyReX) or isinstance(self, SingleReX):
            return False
        elif isinstance(self, NilReX) or isinstance(self, StarReX):
            return True
        elif isinstance(self, CatReX):
            return (self._data[0].is_nil_aMember and
                    self._data[1].is_nil_aMember)
        # self is an instance of AltReX
        return (self._data[0].is_nil_aMember or
                self._data[1].is_nil_aMember)

    def compare(self, other: 'ReX') -> bool:
        """
        Compares two ReX's
        :param other: other ReX
        :return: True if ReX's are equal, False otherwise
        """
        if type(self) != type(other):
            return False

        if isinstance(self, EmptyReX) and isinstance(other, EmptyReX):
            return True
        elif isinstance(self, NilReX) and isinstance(other, NilReX):
            return True
        elif isinstance(self, SingleReX):
            return self._data[0] == other._data[0]
        elif isinstance(self, StarReX):
            return self._data[0].compare(other._data[0])
        elif isinstance(self, (CatReX, AltReX)):
            return (self._data[0].compare(other._data[0]) and
                    self._data[1].compare(other._data[1]))

    def Brzozowski(self, letter: str):
        """'letter' is a string of length one"""
        if not isLetter(letter):
            raise Exception("invalid letter")
        # now compute Brzozowski derivative of the expression
        if (isinstance(self, EmptyReX) or
                isinstance(self, NilReX)):
            return EmptyReX()
        if isinstance(self, SingleReX):
            return NilReX() if self._data[0] == letter else EmptyReX()
        if isinstance(self, StarReX):
            return CatReX(self._data[0].Brzozowski(letter), self)
        if isinstance(self, CatReX):
            mandatory = CatReX(self._data[0].Brzozowski(letter), self._data[1])
            return (AltReX(mandatory, self._data[1].Brzozowski(letter)) if
                    self._data[0].is_nil_aMember else
                    mandatory)
        else:  # 'self' is an instance of class AltReX
            return AltReX(self._data[0].Brzozowski(letter),
                          self._data[1].Brzozowski(letter))

    def simplify(self) -> 'ReX':
        """Simplifies ReX to the very bottom.
        For example (empty . a) = empty
        (empty | empty) = empty
        So, method deletes all redundant empty ReX's
        """
        if isinstance(self, (EmptyReX, NilReX, SingleReX)):
            return self
        elif isinstance(self, StarReX):
            return StarReX(self._data[0].simplify())
        elif isinstance(self, CatReX):
            left = self._data[0].simplify()
            right = self._data[1].simplify()
            if isinstance(left, EmptyReX) or isinstance(right, EmptyReX):
                return EmptyReX()
            return CatReX(left, right)
        else:  # self is an instance of AltReX
            left = self._data[0].simplify()
            right = self._data[1].simplify()
            if isinstance(left, EmptyReX) and isinstance(right, EmptyReX):
                return EmptyReX()
            elif isinstance(left, EmptyReX):
                return right
            elif isinstance(right, EmptyReX):
                return left
            return AltReX(left, right)


def naive_recognition(rex, word):
    """returns 'True' if the list 'word' of letters represents the word
    belonging to the language specified by the regular expression 'rex'
    """
    if not isinstance(rex, ReX):
        raise Exception("invalid regular expression")
    if not (isinstance(word, list) and
            all(map(isinstance, word, len(word) * [str])) and
            all(map(lambda x: len(x) == 1, word))):
        raise Exception("invalid word")
    # Now, let us recognise
    rex_curr = copy.deepcopy(rex)
    for a in word:
        rex_curr = rex_curr.Brzozowski(a)
    return rex_curr.is_nil_aMember


class EmptyReX(ReX):  # синтаксичне правило (1)
    def __init__(self):
        self._data = None


class NilReX(ReX):  # синтаксичне правило (2)
    def __init__(self):
        self._data = ()


class SingleReX(ReX):  # синтаксичне правило (3)
    def __init__(self, letter):
        """'letter' is a string of length one"""
        if not isLetter(letter):
            raise Exception("invalid letter")
        self._data = (letter,)


class StarReX(ReX):  # синтаксичне правило (4)
    def __init__(self, rex: ReX):
        if not isinstance(rex, ReX):
            raise Exception("invalid regular expression")
        self._data = (rex,)


class CatReX(ReX):  # синтаксичне правило (5)
    def __init__(self, rex1: ReX, rex2: ReX):
        if not (all(map(isinstance, (rex1, rex2), (ReX, ReX)))):
            raise Exception("invalid regular expression")
        self._data = (rex1, rex2)


class AltReX(ReX):  # синтаксичне правило (6)
    def __init__(self, rex1: ReX, rex2: ReX):
        if not (all(map(isinstance, (rex1, rex2), (ReX, ReX)))):
            raise Exception("invalid regular expression")
        self._data = (rex1, rex2)


def isLetter(x):
    return isinstance(x, str) and len(x) == 1


class Acceptor:

    def __init__(self, spec):
        self._data = spec

    def run(self, state, u):
        if u:
            a, u_new = u[0], u[1:]
            return self.run(self._data[state][a], u_new)
        return state

    def isAcceptable(self, u):
        return self._data[self.run(0, u)]['acceptant']
