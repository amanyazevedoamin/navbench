import numpy as np
import navbench as nb
try:
    import pathos.multiprocessing as mp
except:
    print('WARNING: Could not find pathos.multiprocessing module')


class InfoMax:
    DEFAULT_LEARNING_RATE = 1e-4

    def __init__(self, num_inputs, num_hidden=None, learning_rate=DEFAULT_LEARNING_RATE, seed=None):
        self.learning_rate = learning_rate

        # seed may be None, in which case it'll be initialised by platform
        np.random.seed(seed)

        # Save seed in case we want it again
        self.seed = np.random.get_state()[1][0]
        print('Seed for InfoMax net: %i' % self.seed)

        if num_hidden is None:
            num_hidden = num_inputs

        weights = np.random.randn(num_inputs, num_hidden)

        # Normalise so that weights.mean() is approx 0 and weights.std() is approx 1
        weights -= weights.mean()
        weights /= weights.std()

        # Use 32-bit floats for performance
        self.weights = weights.astype('f')

    def train(self, image):
        u = self.weights * image.ravel()
        y = np.tanh(u)
        weight_update = (np.eye(self.weights.shape[0]) - (y + u)
                         * np.transpose(u) * self.weights)
        self.weights += (self.learning_rate / u.shape[0]) * weight_update
        assert not np.isnan(self.weights).any()

    def test(self, image):
        return np.sum(np.abs(self.weights * image.ravel()))

    def ridf(self, image, step=1):
        vals = []
        for rot in range(0, image.shape[1], step):
            rot_image = np.roll(image, rot, axis=1)
            vals.append(self.test(rot_image))
        return np.array(vals)


@nb.cache_result
def get_trained_network(training_images, seed, num_hidden=None,
                        learning_rate=InfoMax.DEFAULT_LEARNING_RATE):
    num_inputs = training_images[0].size
    infomax = InfoMax(num_inputs, num_hidden or num_inputs,
                      learning_rate, seed)
    for image in training_images:
        infomax.train(image)
    return infomax


@nb.cache_result
def get_infomax_headings(ann, images, step=1):
    def get_heading(image):
        return nb.ridf_to_radians(ann.ridf(image, step=step))

    headings = mp.Pool().map(get_heading, images)
    return np.array(headings)
