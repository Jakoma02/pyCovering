def string_constraint(model, group):
    """
    No four positions shall be adjecent to each other
    """

    # TODO: Fix

    # The constraint was fulfilled before adding the last position,
    # it is sufficent to check the number of neighbors for the last
    # position

    last_pos = group[-1]

    neighbors = model._neighbors(last_pos)
    in_group = [x for x in group if x in neighbors]

    # print(group)

    return len(in_group) <= 2


def path_constraint(model, group):
    """
    The positions make up a path
    """
    if len(group) == 1:
        return True

    last_pos = group[-1]

    neighbors = set(model._neighbors(last_pos))
    in_group = [x for x in group if x in neighbors]

    # The last position extends the path
    if (len(in_group) == 1) and (in_group[0] in (group[-2], group[0])):
        return True

    return False
