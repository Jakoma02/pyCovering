def string_constraint(model, group):
    """
    No four positions shall be adjecent to each other
    """

    # The constraint was fulfilled before adding the last position,
    # it is sufficent to check the number of neighbors for the last
    # position

    last_pos = group[-1]

    neighbors = model._neighbors(last_pos)
    in_group = [x for x in group if x in neighbors]

    return len(in_group) <= 2
