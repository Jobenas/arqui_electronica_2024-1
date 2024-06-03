import time

def count():
    print("Uno")
    time.sleep(1)
    print("Dos")


def main():
    for _ in range(3):
        count()


if __name__ == '__main__':
    inicio = time.perf_counter()
    main()
    fin = time.perf_counter()

    t_ejecucion = fin - inicio
    print(f"Tiempo de ejecucion: {t_ejecucion:0.5f} segundos")
