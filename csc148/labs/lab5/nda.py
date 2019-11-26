def remove_duplicates(lst: list) -> list:
    """Remove duplicates in O(n) time.
    """
    l = []
    l.append(lst[0])
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1]:
            l.append(lst[i])
    return l


if __name__ == '__main__' :
    pass
