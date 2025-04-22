def transducer(w, a):
    state = (len(w) - 1) % 2 == 0
    if state == 0:
        images = ["001", "00101101", "00101101"*2]
    else:
        images = ["002", "00202202", "00202202"*2]
    return images[int(a)]

def phi(w, a):
    images = ["76", "760", "756", "7560"]
    return images[int(a)]

def psi(w,a):
    images = ["03","033","0333","01"]
    return images[int(a)]

def f_hat(w, a):
    images = ["01", "022", "02", "0222", "0121", "01221", "012", "021"]
    return images[int(a)]

def g(w,a):
    images = ["20", "21", "2"]
    return images[int(a)]

def apply(func, w):
    """Returns the image of w under func."""

    if len(w) == 0:
        return ""
    return apply(func, w[:-1]) + func(w[:-1], w[-1])

