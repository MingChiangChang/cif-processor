import numpy as np
from numpy.linalg import norm
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from peak import Gauss

# TODO: The previous summary csv can be test data if properly processed

# TODO: Check if normalizeable
# TODO: Convert sigma to unit in Q
# TODO: Align strongest peak then try to align others?

# TODO: Write test

def peak_fitting(arr, max_peak, min_improv, 
        bnds=((0, None), (10, None), (10, None)), plot=False):
    '''
    Do background subtraction before using this.
    '''
    peak_ls = []
    for i in range(max_peak):
        result = single_peak_fitting(arr, bnds)
        #print(result.x)
        peak = Gauss(result)
        r = cal_residual(arr, peak)
        #print('Res:{}'.format(norm(r)))
        if plot:
            plt.plot(arr)
            plt.plot(r)
            plt.plot(peak.distribution(arr.shape[0]))
            plt.show()
        if (norm(arr)-norm(r)) < min_improv:
            break
        else:
            arr = r
            arr[int(peak.miu-4*peak.sigma):int(peak.miu+4*peak.sigma)]=0
            peak_ls.append(peak)
        
    return peak_ls

def single_peak_fitting(arr, bnds):
    '''
    Note: The intensity is not normalized. 
    '''
    miu = find_max_point_res(arr)

    # Good bound on width can prevent combining peaks
    def f(x):
        g = Gauss(x[0], x[1], x[2])
        return norm(arr-g.distribution(arr.shape[0]))
    res = minimize(f, (1, miu,1), bounds=bnds)
    return res

def find_max_point_res(arr):
    '''
    Input: np array
    Output: Index of maximum residual point
    '''
    return np.argmax(abs(arr))

def cal_residual(arr, peak):
    return arr-peak.distribution(arr.shape[0])

def reconstruct(peak_ls, arr_size):
    arr = np.zeros(arr_size)
    for peak in peak_ls:
        arr += peak.distribution(arr_size)
    return arr

if __name__ == '__main__':
    data = np.load('../data/npy/BTO_substrate_subtracted_resampled_after_MCBL.npy')
    data = data.reshape(625, 40, 1024)
    #test = np.array([1,2,5,4,2,1,0,0,0,0,0,0])
    test = data[127][20]
    fit = np.zeros(test.shape)

    residual = [norm(test)]
    print('Res: {}'.format(norm(test)))
    peak_ls = peak_fitting(test, 10, 1, plot=True)

    plt.plot(reconstruct(peak_ls, test.shape[0]))
    plt.show()

    intense = np.array([peak.intensity for peak in peak_ls])

    print(intense/np.max(intense))

