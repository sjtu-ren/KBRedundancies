def __getRecordFormatString(arity: int) -> str:
    return '<' + 'i' * arity


def getMeta():
    a = set()
    a.add(1)
    a.add(2)
    print(2 in a)


if __name__ == '__main__':
    getMeta()
