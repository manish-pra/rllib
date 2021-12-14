from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Type, TypeVar

import numpy as np
from torch import Tensor
from .datatypes import Array, Observation, Trajectory

T = TypeVar("T")

def map_observation(func: Callable[[Tensor], Tensor], observation: Observation) -> Observation: ...
def stack_list_of_tuples(iter_: List[T], dim: Optional[int] = ...) -> T: ...
def average_named_tuple(named_tuple_: T) -> T: ...
def average_dataclass(dataclass_: dataclass) -> dataclass: ...  # type: ignore
def map_and_cast(fun: Callable[[T], T], iter_: List[T]) -> T: ...
def bootstrap_trajectory(
    trajectory: Trajectory, bootstraps: int
) -> List[Trajectory]: ...
def batch_trajectory_to_single_trajectory(trajectory: Trajectory) -> Trajectory: ...
def concatenate_observations(
    observation: Observation, new_observation: Observation
) -> Observation: ...
def gather_trajectories(
    trajectories: List[Trajectory], gather_dim: int = ...
) -> Observation: ...
def unstack_observations(observation: Observation) -> Trajectory: ...
def chunk(array: Array, num_steps: int) -> Array: ...
def d4rl_to_observation(dataset: Dict[str, Array]) -> Observation: ...
def split_observations_by_done(observation: Observation) -> Trajectory: ...
def drop_last(observation: Observation, k:int) -> Observation: ...
def _observation_to_num_steps(observation: Observation, num_steps: int) -> Observation: ...
def observation_to_num_steps(observation: Observation, num_steps: int) -> Observation: ...
def trajectory_to_num_steps(trajectory: Trajectory, num_steps: int) -> Trajectory: ...
def merge_observations(trajectory: Trajectory, dim: int=...) -> Observation: ...
