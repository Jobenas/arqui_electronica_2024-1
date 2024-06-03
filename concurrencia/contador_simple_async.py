import asyncio
import time

async def count(idx: int):
    print(f"[{idx}] Uno")
    await asyncio.sleep(1)
    print(f"[{idx}] Dos")


# async def main():
#     await asyncio.gather(count(1), count(2), count(3))

async def main():
    await asyncio.gather(*(count(i + 1) for i in range(2)))


if __name__ == '__main__':
    inicio = time.perf_counter()
    asyncio.run(main())
    fin = time.perf_counter()

    t_ejecucion = fin - inicio
    print(f"Tiempo de ejecucion: {t_ejecucion:0.5f} segundos")
