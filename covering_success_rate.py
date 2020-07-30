from covering import CoveringModel, ImpossibleToFinishException

WIDTH = 20
HEIGHT = 20
TILE_SIZE = 4

TEST_COUNT = 100


model = CoveringModel(WIDTH, HEIGHT, TILE_SIZE)


success_count = 0

for i in range(TEST_COUNT):
    print(f"Attempt #{i + 1}... ", end="")
    model.reset()

    try:
        model.try_cover()
        print("SUCCESS")
        success_count += 1
    except ImpossibleToFinishException:
        print("FAIL")

print(f"\nResults: successful {success_count}/{TEST_COUNT}")
