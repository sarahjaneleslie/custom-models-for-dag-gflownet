import numpy as np
import math

from scipy.special import gammaln

from dag_gflownet.scores.base import BasePrior, AdjacencyPrior


class UniformPrior(BasePrior):
    @property
    def log_prior(self):
        if self._log_prior is None:
            self._log_prior = np.zeros((self.num_variables,))
        return self._log_prior


class ErdosRenyiPrior(BasePrior):
    def __init__(self, num_variables=None, num_edges_per_node=1.):
        super().__init__(num_variables)
        self.num_edges_per_node = num_edges_per_node

    @property
    def log_prior(self):
        if self._log_prior is None:
            num_edges = self.num_variables * self.num_edges_per_node  # Default value
            p = num_edges / ((self.num_variables * (self.num_variables - 1)) // 2)
            all_parents = np.arange(self.num_variables)
            self._log_prior = (all_parents * math.log(p)
                + (self.num_variables - all_parents - 1) * math.log1p(-p))
        return self._log_prior


class EdgePrior(BasePrior):
    def __init__(self, num_variables=None, beta=1.):
        super().__init__(num_variables)
        self.beta = beta

    @property
    def log_prior(self):
        if self._log_prior is None:
            self._log_prior = np.arange(self.num_variables) * math.log(self.beta)
        return self._log_prior


class FairPrior(BasePrior):
    @property
    def log_prior(self):
        if self._log_prior is None:
            all_parents = np.arange(self.num_variables)
            self._log_prior = (
                - gammaln(self.num_variables + 1)
                + gammaln(self.num_variables - all_parents + 1)
                + gammaln(all_parents + 1)
            )
        return self._log_prior
    

class SprinklerPrior(AdjacencyPrior):
    def __init__(self, num_variables=3):
        super().__init__(num_variables)
        self.logits_array = np.array([[0,0,0],[-1e2,0,0],[-1e2,-1e2,0]])

    def log_prior(self, key):
        target, indices = key
        return np.sum(self.logits_array[indices, target])

class CustomAdjPrior(AdjacencyPrior):
    def __init__(self, logits_array):
        super().__init__(logits_array.shape[0])
        self.logits_array = logits_array

    def log_prior(self, key):
        target, indices = key
        return np.sum(self.logits_array[indices, target])