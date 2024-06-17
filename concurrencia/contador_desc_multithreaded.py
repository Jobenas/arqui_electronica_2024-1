import time
from threading import Thread


N = 70_000_000


def cuenta(n):
    while n > 0:
        n -= 1


if __name__ == '__main__':
    N_2 = N // 2
    t1 = Thread(target=cuenta, args=(N_2, ))
    t2 = Thread(target=cuenta, args=(N_2, ))

    inicio = time.perf_counter()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    fin = time.perf_counter()

    print(f"Tiempo total de ejecucion: {(fin - inicio):0.5f} segundos")
