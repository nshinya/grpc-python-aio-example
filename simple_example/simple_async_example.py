import asyncio

async def func(n):
    print(f"func{n} start")
    await asyncio.sleep(1)
    print(f"func{n} done")
    return n

async def main():
    print("start")
    f1 = await func(1)
    print(f1)
    f2 = await func(2)
    print(f2)
    f3 = await func(3)
    print(f3)

async def main2():
    print("start")
    f1 = func(1)
    f2 = func(2)
    f3 = func(3)
    print(await f1)
    print(await f2)
    print(await f3)

async def main3():
    f1 = asyncio.ensure_future(func(1))
    f2 = asyncio.ensure_future(func(2))
    f3 = asyncio.ensure_future(func(3))
    print(await f1)
    print(await f2)
    print(await f3)

if __name__ == "__main__":
    print("=== blocking ===")
    asyncio.run(main())
    print("=== blocking done ===")

    print("=== blocking ===")
    asyncio.run(main2())
    print("=== blocking done ===")

    print("=== non-blocking ===")
    asyncio.run(main3())
    print("=== non-blocking done ===")
