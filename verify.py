from conditions import *
from backtrack import backtrack
from func import *
from forbiddenfactors import *

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
postconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 16, 7)
]
w, l = backtrack(1000, 3, preconditions=[], postconditions=postconditions, func=transducer, prefix="2212", quiet=quiet)
assert w is None and l == 105, "Section 3.2, Table 2, 2212: claim of maximum length 105 fails."

# Proposition 3.6
# -----------------------------------------------------------------------------
postconditions = [
    RichnessCondition(),
    lambda w, a: power_suffix(w + a, 7, 3)
]
w, l = backtrack(1000, 2, [], postconditions, func=transducer, quiet=quiet)
assert w is None and l == 18, "Section 3.2, Proposition 3.6: claim of maximum length 18 fails."

# Lemma 3.10
# -----------------------------------------------------------------------------

# Factors in F_1

for w in F1.keys():
    assert forbidden_factor_check(w,*F1[w],quiet=quiet),f"Section 3.3, Lemma 3.10: claim that the word w={w} in F_1 is forbidden fails."

# Factors in F_2

for w in F2.keys():
    assert forbidden_factor_check(w,*F2[w],quiet=quiet),f"Section 3.3, Lemma 3.10: claim that the word w={w} in F_2 is forbidden fails."

# Factors in F_3

for w in F3.keys():
    assert forbidden_factor_check(w,*F3[w],quiet=quiet),f"Section 3.3, Lemma 3.10: claim that the word w={w} in F_3 is forbidden fails."

# Factors in F_4

for w in F4.keys():
    assert forbidden_factor_check(w,*F4[w],quiet=quiet),f"Section 3.3, Lemma 3.10: claim that the word w={w} in F_4 is forbidden fails."

# Claim 3.17
# -----------------------------------------------------------------------------

assert directed_edges_in_H()==[[1, 2, 3, 7], [0, 2, 7], [0, 1, 2], [0, 3], [4, 5], [4, 5, 6], [0, 1, 7], [5, 6]],f"Section 3.4, the claim that x' corresponds to an infinite walk on the digraph H fails."

# Claim 3.18
# -----------------------------------------------------------------------------

for u in ["1","01","10","010","101"]:
    assert short_factor_check(u,"3.18.1",quiet), f"Section 3.4, Claim 3.18: claim that the image of the word 6u7 under f_hat has a factor from F_2 fails when u={u}."

F_phi=["00", "11", "22", "33", "01", "20", "31"]

for w in F_phi:
    assert short_factor_check(w,"3.18.2",quiet), f"Section 3.4, Claim 3.18: claim that the image of the word w0 under f_hat compose phi has a factor from F_2 fails when w={w}."

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

for w in ["54445","454454"]:
    assert short_factor_check(w,"3.19",False), f"Section 3.4, Claim 3.19: claim that the image of the word w under f_hat has a factor from F_3 fails when w={w}."

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

for w in ["33330"]:
    assert short_factor_check(w,"3.20.1",quiet), f"Section 3.4, Claim 3.20: claim that the image of the word w under f_hat has a factor from F_4 fails when w={w}."

for w in ["3","21","11","000","010010"]:
    assert short_factor_check(w,"3.20.2",quiet), f"Section 3.4, Claim 3.20: claim that the (slightly extended) image of the word w under f_hat compose psi has a factor from F_4 fails when w={w}."

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



print("All claims verified successfully.")
