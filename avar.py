import numpy as np
import matplotlib.pyplot as plt

class CharacteristicScale:
    def __init__(self, taus=None, horizon=None):
        if horizon is None:
            horizon = 200
        if taus is None:
            taus = range(1,int(horizon/2))
        self.memory = []
        self.taus = taus
        self.horizon = horizon
        

    def allanvar(self, y, taus=None):
        if taus is None:
            taus = list(range(1, int(len(y)/4)))
        av = []
        for m in taus:
            x = [0]
            for k in range(len(y)):
                x.append(x[-1] + y[k])
            n = len(x)
            cumsum = 0
            cnt = 0
            for k in range(n - 2 * m):
                cumsum += (x[k + 2 * m] - 2 * x[k + m] + x[k]) ** 2
                cnt += 1
            av.append(cumsum / (2 * (m ** 2) * (n - 2 * m)))
            
        return av

    def dynallanvar(self):
        if len(self.memory) >= self.horizon:
            davar = self.allanvar(self.memory[-self.horizon:], self.taus)
        else:
            davar = self.allanvar(self.memory, self.taus)
        return davar

    def find_charecteristic_scale(self, avar):
        if len(avar) < 2:
            return 1
        indx = list(avar).index(min(avar))
#         for i in range(len(avar)):
#             if i+1 == len(avar):
#                 return self.taus[i]
#             if avar[i+1] > avar[i]:
#                 return self.taus[i]
#         return self.taus[-1]
        return self.taus[indx], avar[indx]



if __name__ == '__main__':
    char_scale = CharacteristicScale()
    num_samples = 5000
    sigma_noise_initial = 2
    sigma_noise_final = 10
    sigma_random_walk = 1
    x = 0
    X = []
    Y = []
    M_c = []
    for t in range(num_samples):

        if t < num_samples / 2:
            sigma_noise = sigma_noise_initial
        else:
            sigma_noise = sigma_noise_final
        x = x + np.random.normal(0, sigma_random_walk)  # RANDOM WALK PROCESS
        y = x + np.random.normal(0, sigma_noise)  # ADD WHITE NOISE
        X.append(x)
        Y.append(y)
        char_scale.memory.append(y)
        if t > 100:
            avar = char_scale.dynallanvar()
            m_c = char_scale.find_charecteristic_scale(avar)
        else:
            m_c = 1
        M_c.append(m_c)


    fig, axs = plt.subplots(2)
    axs[0].scatter(range(len(Y)), Y, alpha=0.5, marker='.',s=5)
    axs[0].plot(X, color='red')
    axs[0].set_xlabel('time step')
    axs[0].set_ylabel('signal')
    axs[0].legend(['true signal', 'measurement'])
    axs[1].plot(M_c)
    axs[1].set_xlabel('time step')
    axs[1].set_ylabel('Window length')
    axs[1].grid()
    axs[0].grid()
    plt.show()