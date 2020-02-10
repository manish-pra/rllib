"""Implementation of a random agent."""

from .abstract_agent import AbstractAgent
from rllib.dataset import TrajectoryDataset
from rllib.policy import RandomPolicy


class RandomAgent(AbstractAgent):
    """Agent that interacts randomly in an environment."""

    def __init__(self, dim_state, dim_action, num_states=None, num_actions=None,
                 gamma=None, episode_length=None):
        super().__init__(gamma=gamma, episode_length=episode_length)
        self.policy = RandomPolicy(dim_state, dim_action, num_states=num_states,
                                   num_actions=num_actions)
        self.trajectory = []
        self.dataset = TrajectoryDataset(sequence_length=1)

    def observe(self, observation):
        """See `AbstractAgent.observe'."""
        super().observe(observation)
        self.trajectory.append(observation)

    def start_episode(self):
        """See `AbstractAgent.start_episode'."""
        super().start_episode()
        self.trajectory = []

    def end_episode(self):
        """See `AbstractAgent.end_episode'."""
        self.dataset.append(self.trajectory)
