import numpy as np
class Car:
    def __init__(self, vx):
        L = 0.323
        lf = L/2
        lr = L/2
        Cf = 25
        Cr = 25
        m = 4
        Iz = 1
        self.car_params = {\
                    "vx": vx, \
                    "L": L, \
                    "Cf": Cf, \
                    "Cr": Cr, \
                    "m": m, \
                    "lf": lf, \
                    "lr": lr, \
                    "Iz": Iz, \
                    "A" : np.array([[0,1,0,0], [0,-2*(Cf+Cr)/(m*vx),0,-vx-2*(Cf*lf-Cr*lr)/(m*vx)], [0,0,0,1], [0,2*(Cr*lr-Cf*lf)/(Iz*vx),0,-2*(Cr*lr**2+Cf*lf**2)/(Iz*vx)]]), \
                    "B" : np.array([0,2*Cf/m,0,2*lf*Cf/Iz])}

    def getParams(self):
        return self.car_params
