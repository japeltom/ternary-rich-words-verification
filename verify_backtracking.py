from conditions import *
from backtrack import backtrack
from func import *

quiet = True

# Section 3.1, 1st paragraph
# -----------------------------------------------------------------------------
preconditions = [
    ForbiddenSuffixCondition(["001002", "112110", "220221"]), # No given forbidden factors.
    RichnessCondition(),                                      # No nonrich factors.
    lambda w, a: power_suffix(w + a, 7, 3)                    # No powers with exponent 7/3.
]
w, l = backtrack(1000, 3, preconditions, quiet=quiet)
assert w is None and l == 388, "Section 3.1, 1st paragraph claim of maximum length 388 fails."

# Section 3.1, Table 1
# -----------------------------------------------------------------------------
preconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 7, 3)
]
w, l = backtrack(1000, 3, preconditions, prefix="102", quiet=quiet)
assert w is None and l == 152, "Section 3.1, Table 1, 102: claim of maximum length 152 fails."
preconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 7, 3)
]
w, l = backtrack(1000, 3, preconditions, prefix="0011", quiet=quiet)
assert w is None and l == 498, "Section 3.1, Table 1, 0011: claim of maximum length 498 fails."
preconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 7, 3)
]
w, l = backtrack(1000, 3, preconditions, prefix="00100200", quiet=quiet)
assert w is None and l == 502, "Section 3.1, Table 1, 00100200: claim of maximum length 502 fails."

# Lemma 3.3
# -----------------------------------------------------------------------------
preconditions = [
    ForbiddenSuffixCondition(["00"]),
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 7, 3)
]
w, l = backtrack(1000, 3, preconditions, quiet=quiet)
assert w is None and l == 57, "Section 3.1, Lemma 3.3: claim of maximum length 57 fails."

# Table 2
# -----------------------------------------------------------------------------
postconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 16, 7)
]
w, l = backtrack(1000, 3, preconditions=[], postconditions=postconditions, func=transducer, prefix="201", quiet=quiet)
assert w is None and l == 141, "Section 3.2, Table 2, 201: claim of maximum length 141 fails."
postconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 16, 7)
]
w, l = backtrack(1000, 3, preconditions=[], postconditions=postconditions, func=transducer, prefix="210", quiet=quiet)
assert w is None and l == 144, "Section 3.2, Table 2, 210: claim of maximum length 144 fails."
postconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 16, 7)
]
w, l = backtrack(1000, 3, preconditions=[], postconditions=postconditions, func=transducer, prefix="211", quiet=quiet)
assert w is None and l == 101, "Section 3.2, Table 2, 211: claim of maximum length 101 fails."

# Proposition 3.6
# -----------------------------------------------------------------------------
postconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 7, 3)
]
w, l = backtrack(1000, 2, [], postconditions, func=transducer, quiet=quiet)
assert w is None and l == 18, "Section 3.2, Proposition 3.6: claim of maximum length 18 fails."

# Claim 3.18
# -----------------------------------------------------------------------------
preconditions = [
    ForbiddenSuffixCondition(F_phi),
    lambda w, a: power_suffix(w + a, 3, 1)
]
postconditions = [
    lambda w, a: poor_suffix(w + a)
]
func = lambda w, a: "".join(f_hat("", c) for c in phi(w, a))
w, l = backtrack(1000, 4, preconditions=preconditions, postconditions=postconditions, func=func, quiet=quiet)
assert w is None and l == 8, "Section 3.4, Claim 3.18: claim of maximum length 8 fails."

# Claim 3.19
# -----------------------------------------------------------------------------
preconditions = [
    ForbiddenSuffixCondition(["11", "000", "1001"]),
    lambda w, a: power_suffix(w + a, 5, 1)
]
postconditions = [
    lambda w, a: poor_suffix(w + a)
]
func = lambda w, a: f_hat(w,str(int(a)+4))
w, l = backtrack(1000, 2, preconditions=preconditions, postconditions=postconditions, func=func, quiet=quiet)
assert w is None and l == 11, "Section 3.4, Claim 3.19: claim of maximum length 11 fails."

# Claim 3.20
# -----------------------------------------------------------------------------
preconditions = [
    ForbiddenSuffixCondition(["11", "000", "1001"]),
    lambda w, a: power_suffix(w + a, 5, 1)
]
postconditions = [
    lambda w, a: poor_suffix(w + a)
]
func = lambda w, a: "".join(f_hat("", c) for c in psi(w, a))
w, l = backtrack(1000, 2, preconditions=preconditions, postconditions=postconditions, func=func, quiet=quiet)
assert w is None and l == 11, "Section 3.4, Claim 3.20: claim of maximum length 11 fails."

print("All backtracking claims verified successfully.")
