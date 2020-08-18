class GeneralView:
    def show(self, model):
        raise NotImplementedError


class TwoDPrintView(GeneralView):
    def show(self, model):
        data = model.state.raw_data()

        vals = [x for row in data for x in row]
        longest = max(vals)
        max_len = len(str(longest))
        width = max_len + 1

        for row in data:
            p_row = " ".join([str(x).ljust(width) for x in row])
            print(p_row)


class PyramidPrintView(GeneralView):
    def show(self, model):
        pass
