from typing import List, Any


def emphasize(lst: List[str]) -> None:
    return lst * 2


if __name__ == '__main__':
    sentence = ['winter', 'is', 'coming']
    a = emphasize('winter')
    print(a)
