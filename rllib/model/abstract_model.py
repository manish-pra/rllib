"""Interface for dynamical models."""

from abc import ABCMeta

import torch
import torch.nn as nn


class AbstractModel(nn.Module, metaclass=ABCMeta):
    """Interface for Models of an Environment.

    A Model is an approximation of the environment.
    As such it has a step method that returns a `Distribution' over next states,
    instead of the next state.

    Parameters
    ----------
    dim_state: Tuple
        dimension of state.
    dim_action: Tuple
        dimension of action.
    dim_observation: Tuple
        dimension of observation.
    num_states: int, optional
        number of discrete states (None if state is continuous).
    num_actions: int, optional
        number of discrete actions (None if action is continuous).
    num_observations: int, optional
        number of discrete observations (None if observation is continuous).

    Methods
    -------
    __call__(state, action): torch.Distribution
        return the next state distribution given a state and an action.
    reward(state, action): float
        return the reward the model predicts.
    initial_state: torch.Distribution
        return the initial state distribution.

    discrete_state: bool
        Flag that indicates if state space is discrete.
    discrete_action: bool
        Flag that indicates if action space is discrete.
    discrete_observation: bool
        Flag that indicates if observation space is discrete.

    """

    def __init__(
        self,
        dim_state,
        dim_action,
        dim_observation=-1,
        num_states=-1,
        num_actions=-1,
        num_observations=-1,
    ):
        super().__init__()
        self.dim_state = dim_state
        self.dim_action = dim_action
        self.dim_observation = dim_observation if dim_observation else dim_state

        self.num_states = num_states if num_states is not None else -1
        self.num_actions = num_actions if num_actions is not None else -1
        self.num_observations = num_observations if num_observations is not None else -1

        self.discrete_state = self.num_states >= 0
        self.discrete_action = self.num_actions >= 0

    @property
    def name(self):
        """Get Model name."""
        return self.__class__.__name__

    def scale(self, state, action):
        """Get epistemic variance at a given state, action pair."""
        raise NotImplementedError

    def sample_posterior(self):
        """Sample a model from the (approximate) posterior."""
        raise NotImplementedError

    def set_prediction_strategy(self, val: str):
        """Set prediction strategy of model."""
        raise NotImplementedError

    def set_head(self, head_ptr: int):
        """Set ensemble head."""
        pass

    def get_head(self) -> int:
        """Get ensemble head."""
        return -1

    def set_head_idx(self, head_ptr):
        """Set ensemble head for particles."""
        pass

    def get_head_idx(self):
        """Get ensemble head index."""
        return torch.tensor(-1)

    def get_prediction_strategy(self) -> str:
        """Get ensemble head."""
        return ""
