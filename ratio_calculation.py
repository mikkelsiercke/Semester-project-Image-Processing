class RatioCalculation:
    def y(self,  centers0, centers1):
        pos = (centers0 + centers1) / 2
        a = 0.00053
        # x1 = 640 - pos
        if centers0 < 320 < centers1:
            y = 1
            return y
        elif pos > 320:
            b = 0.83
            y = a * pos + b
            return y
        elif pos < 321:
            b = 1
            y = -a * pos + b
            return y

    def distance(self, y):
        return int(145 * y)