"""SARSA Algorithm."""
import torch
import torch.nn as nn
import copy
from .q_learning import QLearningLoss


class SARSA(nn.Module):
    r"""Implementation of SARSA algorithm.

    SARSA is an on-policy model-free control algorithm.

    The SARSA algorithm attempts to find the fixed point of:
    .. math:: Q(s, a) = r(s, a) + \gamma Q(s', a')
    where a' is sampled from a greedy policy w.r.t the current Q-Value estimate.

    Usually the loss is computed as:
    .. math:: Q_{target} = r(s, a) + \gamma Q(s', a')
    .. math:: \mathcal{L}(Q(s, a), Q_{target})

    Parameters
    ----------
    q_function: AbstractQFunction
        q_function to optimize.
    criterion: _Loss
        Criterion to optimize.
    gamma: float
        discount factor.

    References
    ----------
    TODO: Find.
    """

    def __init__(self, q_function, criterion, gamma):
        super().__init__()
        self.q_function = q_function
        self.q_target = copy.deepcopy(q_function)
        self.criterion = criterion
        self.gamma = gamma

    def forward(self, state, action, reward, next_state, done, next_action):
        """Compute the loss and the td-error."""
        pred_q = self.q_function(state, action)

        with torch.no_grad():
            next_v = self.q_target(next_state, next_action)
            target_q = reward + self.gamma * next_v * (1 - done)

        return self._build_return(pred_q, target_q)

    def _build_return(self, pred_q, target_q):
        return QLearningLoss(loss=self.criterion(pred_q, target_q),
                             td_error=(pred_q - target_q).detach())

    def update(self):
        """Update the target network."""
        self.q_target.update_parameters(self.q_function.parameters())


class GradientSARSA(SARSA):
    r"""Implementation of Gradient SARSA.

    The gradient SARSA algorithm takes the gradient of the target value too.

    .. math:: Q_{target} = (r(s, a) + \gamma Q(s', a')).detach()

    References
    ----------
    TODO: find
    """

    def forward(self, state, action, reward, next_state, done, next_action):
        """Compute the loss and the td-error."""
        pred_q = self.q_function(state, action)

        next_v = self.q_function(next_state, next_action)
        target_q = reward + self.gamma * next_v * (1 - done)

        return self._build_return(pred_q, target_q)
