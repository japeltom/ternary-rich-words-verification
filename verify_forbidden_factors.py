from forbiddenfactors import *

quiet = True

# Lemma 3.10
# -----------------------------------------------------------------------------
# The idea is that for each forbidden factor w (key of the below dictionary),
# there is a factor v^{p/q} such that it occurs in f^n(awb) for all letters a
# in the given prefixes and all letters b in the given suffixes. Once this is
# known, we can prove that tau(g(f^k(awb))) has at least a 16/7-power for all
# k >= n. Set quiet to False to see the arguments.
#
# The format of the dictionary is w: (n, v, p, q, prefixes, suffixes)
F1 = {
    "00": (1, "01", 5, 2, [""], ["0","1","2"]),
    "11": (1, "022", 7, 3, [""], ["0","1","2"]),
    "212": (3, "2010201022010", 31, 13, [""], ["0","1","2"]),
    "2222": (2, power("0102",2,1), 5, 2, [""], ["0","1","2"]),
    "1222": (4, power("02010220102010220102", 2, 1), 19, 8, [""], ["0","1"]),
    "2221": (4, power("20102010220102020102", 2, 1), 19, 8, ["0","1"], ["0","1","2"]),
    "1010": (1, "02201", 12, 5, [""], ["1","2"]),
    "0101": (1, "20102", 12, 5, ["2"], ["2"]),
    "022022": (2, "2010220102010", 31, 13, ["0","1","2"], ["0","1","2"]),
    "220220": (2, "2010201020102", 31, 13, ["0","1","2"], ["0","1","2"])
}
F2 = {
    "202202": (2, "2010201022010", 31, 13, ["0","1","2"], ["0","1","2"]),
    "1022021": (3, "20102010220102020102201020102", 67, 29, [""], [""]),
    "1202201": (3, "20102010220102010220102020102", 67, 29, [""], [""]),
    "120102201021": (3, "20102010220102010220102020102201020102010220102020102", 124, 53, [""], [""]),
    power("021012", 13, 6): (2, "020102201020102020102201020201", 71, 30, ["1","2"], ["1","2"]),
    power("012021", 13, 6): (2, "020102201020201020102201020102", 71, 30, ["1","2"], ["1","2"]),
    power("21012010", 21, 8): (0, "21012010", 21, 8, [""], [""]),
    power("21012210120", 27, 11): (0, "21012210120", 27, 11, [""], [""]),
    power("2101221012010", 31, 13): (0, "2101221012010", 31, 13, [""], [""])
}
F3 = {
    "2" + power("2101", 17, 4) + "2": (3, "20102010220102010220102010201022010202010220102010201022010201022010201020102201020201022010", 211, 92, ["0","1"], ["0","1"]),
    power("2101210122101", 31, 13): (0, "2101210122101", 31, 13, [""], [""])
}
F4 = {
    power("0222", 17, 4) + "1": (1, "2010202020102020", 37, 16, ["1","2"], [""]),
    power("22010", 12, 5): (1, "02020102201", 27, 11, [""], ["0","1","2"]),
    power("022201", 29, 6): (0, "022201022201", 29, 12, [""], [""]),
    power("0222010222", 12, 5): (0, "0222010222", 12, 5, [""], [""]),
    power("0222022201", 12, 5): (0, "0222022201", 12, 5, [""], [""]),
    power("0222010222010222022201", 5, 2): (0, "0222010222010222022201", 5, 2, [""], [""])
}

F = F1 | F2 | F3 | F4
for w in F:
    exists, i, a, b = forbidden_factor_check(w, *F[w], quiet=quiet)
    if not exists:
        print(f"The word f^n(awb), where w = {w}, a = {a}, b = {b}, and n = {i}, has no factor ({F[w][1]})^{F[w][2]}/{F[w][3]} as claimed.")
    if not quiet:
        print(f"The word f^n(awb), where w = {w}, a in {F[w][4]}, and b in {F[w][5]}, has factor ({F[w][1]})^{F[w][2]}/{F[w][3]} for all n >= {F[w][0]}.")

# Print out the arguments.
if not quiet:
    F = F1 | F2 | F3 | F4
    for w in F:
        print()
        print(f"Argument for w = {w}:")
        print("-"*(len(w) + 18))
        if w in ["00", "11", "1010", "0101"]:
            k = F1[w][0]
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(awb))) has a factor of exponent at least 7/3 for all n >= {k}.")
        elif w == power("0222", 17, 4) + "1":
            print(f"We can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3 p_4)^2 p_1, where p_1 = 20102, p_2 = 02020, p_3 = 10202, and p_4 = 20. ", end="")
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(awb))) has a factor of exponent at least 16/7 for all n>={n}.")
        elif w == power("22010", 12, 5):
            print(f"We can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1 = 02020, p_2 = 102, and p_3 = 201. ", end="")
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(awb))) has a factor of exponent at least 7/3 for all n>={n}.")
        elif w == power("2101221012010", 31, 13):
            print(f"We can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1 = p_2 = 21012, and p_3 = 010. ", end="")
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.")
        elif w == power("022201", 29, 6):
            print(f"We can write p^{BadTop}/{BadBottom} = (q 1 q 1)^2 q, where q = 02220. ", end="")
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.")
        elif w == power("0222010222", 12, 5):
            print(f"Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1 = p_3 = 0222 and p_2 = 01. ", end="")
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.")
        elif w == power("0222022201", 12, 5):
            print(f"Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1 = p_2 = 0222 and p_3 = 01.")
            print(f"It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.")
        else:
            n = F[w][0]
            BadPeriod = F[w][1]
            BadTop = F[w][2]
            BadBottom = F[w][3]
            if parikh_check(BadPeriod, BadTop - 2*BadBottom, BadBottom):
                if not quiet:
                    print(f"We can write p^{BadTop}/{BadBottom} = p^2 q, where p = {BadPeriod} and q = {power(BadPeriod,BadTop-2*BadBottom,BadBottom)}. ", end="")
                    print(f"We check that each entry in the Parikh vector of q is at least 2/7 of the corresponding entry in the Parikh vector of p. ", end="")
                    print(f"Thus, we conclude that tau(g(f^n(awb))) has a factor of exponent at least 16/7 for all n >= {n}.")
            else:
                print(f"The Parikh check failed for {w}.")
                raise SystemExit

print()
print("Claims of Lemma 3.10 verified successfully.")

