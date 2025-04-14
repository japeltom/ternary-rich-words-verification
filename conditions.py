from eertree import eerTree

class Condition:
    """A superclass for all conditions."""

    pass

class FunctionCondition(Condition):
    """A stateless condition."""

    def __init__(self, func):
        super().__init__()
        self.func = func

    def __str__(self):
        return f"FunctionCondition({str(self.func)})"

    def add(self, w, a):
        return self.func(w, a)

    def pop(self):
        pass

class RichnessCondition(Condition):

    def __init__(self):
        self.eertree = eerTree("")

    def add(self, w, a):
        self.eertree.add(a)
        return self.eertree._palSufStack[-1] if not self.eertree._newPal else None

    def pop(self):
        self.eertree.pop()

class ForbiddenSuffixCondition(Condition):

    def __init__(self, forbidden):
        for x in forbidden:
            assert len(x) > 0, "Forbidden factors must be nonempty."
        self.forbidden = forbidden

    def add(self, w, a):
        for p in [x[:-1] for x in self.forbidden if x[-1] == a]:
            if w.endswith(p):
                return p + a
        return None

    def pop(self):
        pass

def power_suffix(w, top, bottom):
    """Checks if the word w has as a suffix a repetition with exponent >=
    top/bottom."""

    n = len(w)
    p = 1
    while n*bottom >= p*top:
        i = 0
        while w[-1 - i] == w[-1 - i - p]:
            if (i + 1 + p)*bottom >= p*top:
                return w[-1 - i - p:]
            i += 1
            if i + p >= n:
                break
        p += 1

    return None

def non_prefix_occurrences(u, w):
    if len(u) == 0:
        return list(range(1, len(w) + 1))
    occurrences = []
    pos = 1
    while pos > 0 and pos < len(w):
        pos = w.find(u, pos)
        if pos != -1:
            occurrences.append(pos)
        pos += 1

    return occurrences

def is_poor(w):
    is_palindrome = lambda w: w == w[::-1]
    for l in range(len(w) + 1):
        pref = w[:l]
        if not is_palindrome(pref): continue
        if not pref.count("2") % 2 == 0: continue
        found = False
        for pos in non_prefix_occurrences(pref, w):
            x = w[:pos]
            if x.count("2") % 2 == 0:
                found = True
                break

        if not found:
            return False

    return True

def poor_suffix(w):
    """Checks if w has a poor suffix."""

    for l in range(1, len(w) + 1):
        suff = w[-l:]
        if is_poor(suff):
            return suff

    return None

