import asyncio
import random

# Colores ANSI
c = (
    "\033[0m",   # Fin del color
    "\033[36m",  # Color Cyan
    "\033[91m",  # Color Rojo
    "\033[35m",  # Color Magenta
)


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Iniciando makerandom({idx}), umbral seleccionado: {threshold}.")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i}, muy bajo: reintentando...")
        # await asyncio.sleep(idx + 1)
        await asyncio.sleep(random.randint(1,3))
        i = random.randint(0, 10)
    print(c[idx + 1] + f"---> Terminado: makerandom({idx}) == {i}" + c[0])

    return i


async def main():
    res = await asyncio.gather(*(makerandom(i, random.randint(6, 9)) for i in range(3)))
    return res


if __name__ == '__main__':
    # random.seed(1337)
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}: r2: {r2}, r3: {r3}")
