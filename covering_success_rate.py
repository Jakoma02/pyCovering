from covering import CoveringModel, ImpossibleToFinishException, \
                     CoveringTimeoutException

WIDTH = 20
HEIGHT = 20
TILE_SIZE = 4

TIMEOUT = 30

model = CoveringModel(WIDTH, HEIGHT, TILE_SIZE)


def non_trivial_divisors(x):
    for i in range(2, x):
        if x % i == 0:
            yield i


def measure(w, h, ts, count):
    success_count = 0
    timeout_count = 0

    model.set_size(w, h)
    model.set_block_size(ts)

    for i in range(count):
        print(f"    {i+1}/{count}", end="\r")
        model.reset()

        try:
            model.try_cover(check_finishable=False, timeout=TIMEOUT)
            success_count += 1

        except ImpossibleToFinishException:
            pass
        except CoveringTimeoutException:
            timeout_count += 1

    return (success_count, timeout_count)


CSV_FILE = "experiment_results.csv"

MIN_SIZE = 3
MAX_SIZE = 30
TEST_COUNT = 1000

with open(CSV_FILE, "w") as out_file:
    out_file.write("w,h,ts,success,timeouts\n")

    for w in range(MIN_SIZE, MAX_SIZE + 1):
        for h in range(MIN_SIZE, MAX_SIZE + 1):
            size = w * h

            for ts in non_trivial_divisors(size):
                print(f"Measuring w={w}, h={h}, ts={ts}...")
                success, timeouts = measure(w, h, ts, TEST_COUNT)
                print(f"  OK: {success}/{TEST_COUNT}\t({timeouts} timeouts)")
                out_file.write(f"{w},{h},{ts},{success},{timeouts}\n")
