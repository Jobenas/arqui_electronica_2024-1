from concurrent.futures import ThreadPoolExecutor
import time
from threading import Lock


class FakeDatabse:
    def __init__(self):
        self.value = 0
        self._lock = Lock()

    def update(self, nombre):
        print(f"Thread {nombre}: Iniciando la actualización")
        print(f"Thread {nombre}: A punto de adquirir el lock")
        with self._lock:
            print(f"Thread {nombre}: Ha adquirido el lock")
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            print(f"Thread {nombre}: A punto de liberar el lock")
        print(f"Thread {nombre}: Ha liberado el lock")
        print(f"Thread {nombre}: Finalizando la actualización")


if __name__ == '__main__':
    workers = 5
    tasks = workers

    db = FakeDatabse()
    print(f"Valor inicial de la base de datos: {db.value}")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for index in range(tasks):
            executor.submit(db.update, index)

    print(f"Valor final de la base de datos: {db.value}")
