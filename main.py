from Rex import ReX, EmptyReX, NilReX, CatReX, AltReX, StarReX, SingleReX
from Rex import Acceptor
from Reducer import reduce_acceptor

def create_acceptor(rex):
    stringReX = str(rex)
    stringReX = stringReX.replace('nil', '')
    stringReX = stringReX.replace('empty', '')
    listReX = []
    for c in stringReX:
        if c != '|' and c != '.' and c != '*' and c != '(' and c != ')' and c != ' ':
            listReX.append(c)

    A = set(listReX)            # Alphabet set

    Q = set()                   # States set
    Q.add(rex)
    doDict = {}                 # Transition dictionary
    acceptantsSet = set()       # Acceptant states set

    Q_new = set()
    Q_new.add(rex)
    Q_new_prime = set()

    while Q_new:
        for e_prime in Q_new:
            doDict.update({e_prime: {a: None for a in A}})
            for letter in A:
                next_rex = e_prime.Brzozowski(letter).simplify()
                doDict[e_prime][letter] = next_rex
                if not any(next_rex.compare(q) for q in Q_new | Q_new_prime):
                    Q_new_prime.add(next_rex)
            if e_prime.is_nil_aMember:
                acceptantsSet.add(e_prime)
        Q = Q.union(Q_new_prime)
        Q_new = Q_new_prime
        Q_new_prime = set()

    Q_list = list(Q)
    acceptor_spec = {i: {letter: find_rex_index(doDict[rex][letter], Q_list) for letter in A} for i, rex in enumerate(Q_list)}

    for state_id, rex in enumerate(Q_list):             # For that defines acceptant states
        if any(rex.compare(acceptant_rex) for acceptant_rex in acceptantsSet):
            acceptor_spec[state_id]['acceptant'] = True

    for state_id, state_data in acceptor_spec.items():  # For to print all states
        print(f"State {Q_list[state_id]}:")
        for letter, next_state in state_data.items():
            if letter != 'acceptant':
                print(f"  On input '{letter}': go to state {Q_list[next_state]}")
        if state_data.get('acceptant'):
            print(f"  This is an acceptant state")
        print()

    return Acceptor(acceptor_spec)

def find_rex_index(rex, rex_list):
    """
    Find index of rex in rex_list.
    :param rex: Our ReX
    :param rex_list: list of ReX's
    :return: index of rex in rex_list or -1 if it doesn't exist.
    """
    for i, rex_item in enumerate(rex_list):
        if rex.compare(rex_item):
            return i
    return -1

def main():
    rex = AltReX(
        AltReX(
            NilReX(),
            CatReX(
                CatReX(
                    CatReX(
                        SingleReX('a'),
                        StarReX(SingleReX('b'))
                    ),
                    SingleReX('a')
                ),
                SingleReX('b')
            )
        ),
        CatReX(
            CatReX(
                CatReX(
                    SingleReX('b'),
                    StarReX(SingleReX('a'))
                ),
                SingleReX('b')
            ),
            SingleReX('a')
        )
    )
    create_acceptor(rex)
    specA = {
        0: {
            'a': 1,
            'b': 2,
            'acceptant': False
        },
        1: {
            'a': 3,
            'b': 4,
            'acceptant': False
        },
        2: {
            'a': 4,
            'b': 5,
            'acceptant': False
        },
        3: {
            'a': 1,
            'b': 2,
            'acceptant': True
        },
        4: {
            'a': 3,
            'b': 4,
            'acceptant': False
        },
        5: {
            'a': 4,
            'b': 5,
            'acceptant': True
        }
    }

    specB = {
        0: {
            'a': 1,
            'b': 0,
            'acceptant': True
        },
        1: {
            'a': 0,
            'b': 2,
            'acceptant': False
        },
        2: {
            'a': 0,
            'b': 1,
            'acceptant': False
        }
    }

    specC = {
        0: {
            'a': 1,
            'b': 5,
            'acceptant': False
        },
        1: {
            'a': 6,
            'b': 2,
            'acceptant': False
        },
        2: {
            'a': 0,
            'b': 2,
            'acceptant': True
        },
        3: {
            'a': 2,
            'b': 6,
            'acceptant': False
        },
        4: {
            'a': 7,
            'b': 5,
            'acceptant': False
        },
        5: {
            'a': 2,
            'b': 6,
            'acceptant': False
        },
        6: {
            'a': 6,
            'b': 4,
            'acceptant': False
        },
        7: {
            'a': 6,
            'b': 2,
            'acceptant': False
        }
    }
    reduce_acceptor(Acceptor(specA))
    reduce_acceptor(Acceptor(specB))
    reduce_acceptor(Acceptor(specC))


if __name__ == "__main__":
    main()