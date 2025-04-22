from conditions import Condition, FunctionCondition

def backtrack(n, k, preconditions, postconditions=None, func=None, prefix="", quiet=False):
    """A backtracking algorithm that builds words u satisfying given
    precondition that maps to words v that satisfy postconditions.

    Args:
    n: Max length of u, guarantees termination.
    k: Alphabet size of u.
    preconditions: Conditions that u must satisfy..
    postconditions: Conditions that v must satisfy.
    func: A function f that maps u to v defined recursively by f(ua) = f(u)f(u, a).
    prefix: An initial prefix for u to start with.
    quiet: Display progress or not.

    Returns:
    u: A word u of length n satisfying the conditions if exists. None otherwise.
    len(u): Length of the longest u satisfying the conditions that was found.
    """

    def config_conditions(conditions):
        if conditions is None:
            conditions = []
        if not isinstance(conditions, list):
            conditions = [conditions]
        # If a condition is a plain function, we assume that we can use
        # FunctionCondition.
        for i in range(len(conditions)):
            if not isinstance(conditions[i], Condition):
                conditions[i] = FunctionCondition(conditions[i])
        return conditions

    preconditions = config_conditions(preconditions)
    postconditions = config_conditions(postconditions)

    pop_lengths = [] # Pop lengths for the image.

    def pop(conditions, pop_lengths=None, limit=-1):
        """Calls the pop method of every condition. If limit != -1, then only
        the first limit pop methods are called. Returns the pop length."""

        if len(conditions) == 0:
            return 1

        pop_length = pop_lengths.pop() if pop_lengths is not None else 1

        for n, c in enumerate(conditions):
            if limit != -1 and n >= limit:
                break
            for _ in range(pop_length):
                c.pop()

        return pop_length

    def check_conditions(w, x, conditions, pop_lengths=None):
        """Checks that all conditions are satisfied for w + x. Returns the
        number of calls to add that were successful and the first nonsuccessful
        condition (None if it does not exist)."""

        failed = False
        n = -1
        for n, c in enumerate(conditions):
            z = ""
            for a in x:
                if c.add(w + z, a) is not None:
                    failed = True
                z += a
            if failed: break

        if pop_lengths is not None:
            pop_lengths.append(len(x))

        n_failed = n + 1 if not failed else n
        return n_failed, None if not failed else c

    # Check that the provided prefix satisfies the given conditions.
    u = "" # preimage
    v = "" # image
    for a in prefix:
        x = a if func is None else func(u, a)
        _, c = check_conditions(u, a, preconditions)
        if c is not None:
            raise ValueError(f"The entered prefix does not satisfy the precondition {str(c)}.")
        _, c = check_conditions(v, x, postconditions, pop_lengths=pop_lengths)
        if c is not None:
            raise ValueError(f"The entered prefix does not satisfy postcondition {str(c)}.")
        u += a
        v += x

    longest = prefix

    extensions = "0"
    while len(extensions) > 0:
        a = extensions[-1]
        x = a if func is None else func(u, a)

        l_pre, _ = check_conditions(u, a, preconditions)
        l_post, _ = check_conditions(v, x, postconditions, pop_lengths=pop_lengths)
        if l_pre == len(preconditions) and l_post == len(postconditions):
            # u + a and v + x are good
            u = u + a
            v = v + x
            if len(u) > len(longest):
                # Save and print the new longest word.
                longest = u
                if not quiet:
                    print(len(u), u)

            if len(u) == n:
                # Terminate if we reach the given length.
                if not quiet:
                    print(f"Found a word of length {n}.")
                return u, len(u)
            else:
                # Set the next extension letter to be 0.
                extensions += "0"
        else:
            # u + a or v + x is not good, backtrack
            # First, we pop only on those conditions for which add was called and it succeeded.
            pop(preconditions, limit=l_pre+1)
            pop(postconditions, pop_lengths=pop_lengths, limit=l_post+1)
            a = extensions[-1]
            extensions = extensions[:-1]

            # Continue backtracking until we can increment a letter or we reach
            # th beginning.
            while len(extensions) > 0 and int(a) == k - 1:
                l_pre = pop(preconditions)
                l_post = pop(postconditions, pop_lengths=pop_lengths)
                a = extensions[-1]
                extensions = extensions[:-1]
                u = u[:-l_pre]
                v = v[:-l_post]

            if int(a) != k - 1:
                extensions += str(int(a) + 1)

    if not quiet:
        print(f"There are only finitely many words satisfying the given conditions. The longest such word has length {len(longest)}.")

    return None, len(longest)

