''' Thie module uses Gaussian mixture to fit multimodal data '''
from sklearn.mixture import GaussianMixture

def gaussian_mix_fit(data, num_of_peak):
    data = data.reshape(-1,1)
    model = GaussianMixture(n_components=num_of_peak)
    model.fit(data)
    print('weights: ', model.weights_)
    print('means: ', model.means_)
    print('covariance: ', model.covariances_)
    return 1,2 

