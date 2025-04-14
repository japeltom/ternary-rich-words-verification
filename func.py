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

def f_hat(w, a):
    images = ["01", "022", "02", "0222", "0121", "01221", "012", "021"]
    return images[int(a)]

