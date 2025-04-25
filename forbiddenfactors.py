from func import *
from conditions import poor_suffix

def power(period, top, bottom):
    """Raises the given word to power top/bottom."""

    p=len(period)
    rep=""
    while (len(rep)+1)*bottom <= p*top:
        rep+=period[len(rep)%p]
    return rep

def parikh(w):
    """Returns the Parikh vector of a word w over Sigma_3."""

    return [w.count(str(i)) for i in range(3)]

def parikh_check(period, top, bottom):
    """Returns True if and only if every entry of the Parikh vector of
    period^{top/bottom} is at least 2/7 of the corresponding entry of the
    Parikh vector of period"""

    excess = power(period, top, bottom)
    return all(7*parikh(excess)[i] >= 2*parikh(period)[i] for i in range(3))

def critical_exponent(w):
    """Returns the critical exponent of w and the factor having this exponent."""

    top = 1
    bottom = 1
    word = ""
    u = ""
    for n in range(len(w)):
        u += w[n]
        p = 1
        while n*bottom >= p*top:
            i = 0
            while u[-1-i] == u[-1-i-p]:
                i += 1
                if i + p >= n + 1:
                    break

            if i >= 1 and (i+p)*bottom > p*top:
                bottom = p
                top = i+p
                word = u[-p*top//bottom:]

            p += 1
        
    return [top, bottom, word]

def forbidden_factor_check(w, n, BadPeriod, BadTop, BadBottom, Prefixes=[""], Suffixes=[""], quiet=False):
    """Checks that f^n(awb) contains BadPeriod^{BadTop/BadBottom} for all letters a in
    prefixes and all letters b in suffixes."""
    
    BadRep = power(BadPeriod, BadTop, BadBottom)

    for a in Prefixes:
        for b in Suffixes:
            word = a + w + b
            for i in range(n):
                # First we check that tau(g(f^i(awb))) has a factor of exponent
                # at least 16/7. We do this only if quiet = False.
                u = apply(g, word)
                v = apply(transducer, u)
                ce_top, ce_bottom, ce_factor = critical_exponent(v)
                if ce_top*7 < ce_bottom*16:
                    return False, i, a, b
                # Uncomment to see the factor of exponent at least 16/7.
                #print(ce_top, ce_bottom, ce_factor)

                word = apply(f_hat, word)

            # Now we check that tau(g(f^n(awb))) has the claimed factor.
            if not BadRep in word:
                return False, i, a, b

    return True, None, None, None

