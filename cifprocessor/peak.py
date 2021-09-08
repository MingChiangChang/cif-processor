import numpy as np


class Gauss():
    '''
    Array-based Gauss. Not normalized. 
    All unit are in unit of array index.
    '''

    def __init__(self, *args):
        assert (len(args) == 1) or (len(args)==3), 'Wrong number of parameters'
        if len(args) == 1:
            res = args[0]
            self.intensity = res.x[0]
            self.miu = res.x[1]
            self.sigma = res.x[2]
        if len(args) == 3:
            self.intensity = args[0]
            self.miu = args[1]
            self.sigma = args[2]
        
        self.miu_Q = 0
        self.sigma_Q = 0
        
        self.is_in_Q = False

    def make_it_Q(self, Q_range, pxls):
        if self.is_in_Q == False:
            self.miu_Q = self.interpolate(Q_range, pxls)
            self.sigma_Q = self.sigma/(np.max(Q_range)-np.min(Q_range))
            self.is_in_Q = True

    def interpolate(self, Q_range, pxls):
        stepsize = (np.max(Q_range)-np.min(Q_range))/pxls
        return np.min(Q_range) + miu*stepsize

    def __str__(self):
        return ('Intensity: {:.2f}, miu: {:.2f}, sigma: {:.2f}, miu_Q: {:.2f}'
                ', sigma_Q: {:.2f}').format(self.intensity,
                self.miu, self.sigma, self.miu_Q, self.sigma_Q)

    def __repr__(self):
        return ('Intensity: {:.2f}, miu: {:.2f}, sigma: {:.2f}, miu_Q: {:.2f}'
                ', sigma_Q: {:.2f}').format(self.intensity,
                self.miu, self.sigma, self.miu_Q, self.sigma_Q)

    def distribution(self, arr_size):
        '''
        Construct distribution with the correct array shape
        '''
        gauss = [np.exp(-(x-self.miu)**2/(2*self.sigma**2))
                for x in range(arr_size)] 
        return self.intensity/(self.sigma*np.sqrt(2*np.pi))*np.array(gauss)
    
class Lorentz():

    def __init__(self, x0, gamma):
        self.gamma = gamma
        self.x0 = x0

    def distribution(self, arr_size):
        lorentz = [1/((x-x0)**2 + gamma**2) for x in range(arr_size)]
