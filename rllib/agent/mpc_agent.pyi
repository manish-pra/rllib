"""MPC Agent Implementation."""

from typing import Optional
from torch.optim.optimizer import Optimizer
from torch.distributions import Distribution

from .model_based_agent import ModelBasedAgent
from rllib.policy.mpc_policy import MPCPolicy
from rllib.algorithms.td import ModelBasedTDLearning


class MPCAgent(ModelBasedAgent):
    """Implementation of an agent that runs an MPC policy."""
    value_optimizer: Optional[Optimizer]
    num_gradient_steps: int
    value_learning: ModelBasedTDLearning

    def __init__(self,
                 env_name: str,
                 mpc_policy: MPCPolicy,
                 model_learn_num_iter: int = 0,
                 model_learn_batch_size: int = 64,
                 model_optimizer: Optimizer = None,
                 value_optimizer: Optimizer = None,
                 num_gradient_steps: int = 50,
                 num_steps_returns: int = 1,
                 max_memory: int = 1000,
                 value_opt_num_iter: int = 0,
                 value_opt_batch_size: int = None,
                 sim_num_steps: int = 0,
                 sim_initial_states_num_trajectories: int = 0,
                 sim_initial_dist_num_trajectories: int = 0,
                 sim_memory_num_trajectories: int = 0,
                 initial_distribution: Distribution = None,
                 gamma: float = 1.0,
                 exploration_steps: int = 0,
                 exploration_episodes: int = 0,
                 comment: str = ''
                 ) -> None: ...
