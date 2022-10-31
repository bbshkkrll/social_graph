import itertools


def get_partition(lst, size=25):
    for i in range(0, len(lst), size):
        yield list(itertools.islice(lst, i, i + size))


class PartitionList:
    pass
    """Список, в котором будут храниться списки ограниченной длины"""
