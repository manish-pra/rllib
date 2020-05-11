"""Model-Based MPPO Agent."""
from typing import Union

from torch.distributions import Distribution
from torch.optim.optimizer import Optimizer

from .model_based_agent import ModelBasedAgent
from rllib.algorithms.mppo import MBMPPO


class MBMPPOAgent(ModelBasedAgent):
    mppo: MBMPPO
    mppo_optimizer: Optimizer
    mppo_gradient_steps: int
    def __init__(self, env_name: str, mppo: MBMPPO,
                 model_optimizer: Union[Optimizer, None], mppo_optimizer: Optimizer,
                 initial_distribution: Distribution = None,
                 action_scale: float=1.,
                 plan_horizon: int = 1, plan_samples: int = 8, plan_elite: int = 1,
                 max_memory: int = 10000,
                 model_learn_batch_size: int = 64,
                 model_learn_num_iter: int = 30,
                 mppo_num_iter: int = 100,
                 mppo_gradient_steps: int = 50,
                 mppo_batch_size: int = None,
                 sim_num_steps: int = 200,
                 sim_num_subsample: int = 1,
                 sim_initial_states_num_trajectories: int = 8,
                 sim_initial_dist_num_trajectories: int = 0,
                 sim_memory_num_trajectories: int = 0,
                 thompson_sampling: bool = False,
                 gamma: float = 1.0, exploration_steps: int = 0,
                 exploration_episodes: int = 0,
                 comment: str = '') -> None: ...

    def _optimize_policy(self) -> None: ...
