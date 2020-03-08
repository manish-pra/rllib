"""Policy Gradient Algorithm."""
import torch
import torch.nn as nn
import copy
from collections import namedtuple
from rllib.util.utilities import integrate

PGLoss = namedtuple('PolicyGradientLoss',
                    ['actor_loss', 'critic_loss'])


class CriticPolicyGradient(nn.Module):
    r"""Implementation of Policy Gradient algorithm.

    Policy-Gradient is an on-policy model-free control algorithm.
    Policy-Gradient computes the policy gradient using a critic to estimate the returns
    (sum of discounted rewards).

    The Policy-Gradient algorithm is a policy gradient algorithm that estimates the
    gradient:
    .. math:: \grad J = \int_{\tau} \grad \log \pi(s_t) Q(s_t, a_t),
    where the previous integral is computed through samples (s_t, a_t) samples.


    Parameters
    ----------
    policy: AbstractPolicy
        policy to optimize.
    critic: AbstractValueFunction
        critic that evaluates the current policy.
    criterion: _Loss
        Criterion to optimize the baseline.
    gamma: float
        discount factor.

    References
    ----------
    Williams, Ronald J. "Simple statistical gradient-following algorithms for
    connectionist reinforcement learning." Machine learning 8.3-4 (1992): 229-256.

    Sutton, Richard S., et al. "Policy gradient methods for reinforcement learning with
    function approximation." Advances in neural information processing systems. 2000.

    """

    eps = 1e-12

    def __init__(self, policy, critic, criterion, gamma):
        super().__init__()
        # Actor
        self.policy = policy
        self.policy_target = copy.deepcopy(policy)

        # Critic
        self.critic = critic
        self.critic_target = copy.deepcopy(critic)

        self.criterion = criterion
        self.gamma = gamma

    def forward(self, trajectories):
        """Compute the losses."""
        actor_loss = torch.tensor(0.)
        critic_loss = torch.tensor(0.)

        for trajectory in trajectories:
            state, action, reward, next_state, done, *r = trajectory

            # ACTOR LOSS
            pi = self.policy(state)
            pred_q = self.critic(state, action)
            with torch.no_grad():
                returns = pred_q - integrate(lambda a: self.critic(state, a),
                                             self.policy(state))
            if self.policy.discrete_action:
                action = action.long()
            actor_loss += (-pi.log_prob(action) * returns).sum()

            # CRITIC LOSS
            with torch.no_grad():
                next_v = integrate(lambda a: self.critic_target(next_state, a),
                                   self.policy(next_state))
                target_q = reward + self.gamma * next_v * (1 - done)

            critic_loss += self.criterion(pred_q, target_q)

        return PGLoss(actor_loss, critic_loss)

    def update(self):
        """Update the baseline network."""
        self.policy_target.update_parameters(self.policy.parameters())
        self.critic_target.update_parameters(self.critic.parameters())
