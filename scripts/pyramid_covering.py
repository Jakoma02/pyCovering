from covering.models import PyramidCoveringModel, CoveringTimeoutException, \
                            ImpossibleToFinishException

model = PyramidCoveringModel(30, 4)

ATTEMPTS = 1000

for i in range(ATTEMPTS):
    model.reset()
    try:
        model.try_cover()
    except ImpossibleToFinishException:
        print("Impossible to finish")
    except CoveringTimeoutException:
        print("Timeout")
    else:
        print("OK")
