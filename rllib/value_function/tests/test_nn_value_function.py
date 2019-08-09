import pytest
import torch
import torch.testing
from rllib.value_function import NNValueFunction, NNQFunction


@pytest.fixture(params=[False, True])
def discrete_state(request):
    return request.param


@pytest.fixture(params=[False, True])
def discrete_action(request):
    return request.param


@pytest.fixture(params=[4, 2, 1])
def dim_state(request):
    return request.param


@pytest.fixture(params=[4, 2, 1])
def dim_action(request):
    return request.param


@pytest.fixture(params=[None, 1, 16])
def batch_size(request):
    return request.param


class TestNNValueFunction(object):
    def init(self, discrete_state, dim_state):
        if discrete_state:
            self.num_states = dim_state
            self.dim_state = 1
        else:
            self.num_states = None
            self.dim_state = dim_state

        layers = [32, 32]
        self.value_function = NNValueFunction(self.dim_state, self.num_states, layers)

    def test_num_states(self, discrete_state, dim_state):
        self.init(discrete_state, dim_state)
        assert self.num_states == self.value_function.num_states
        if not discrete_state:
            assert self.value_function.num_states is None
        assert discrete_state == self.value_function.discrete_state

    def test_dim_states(self, discrete_state, dim_state):
        self.init(discrete_state, dim_state)
        assert self.dim_state == self.value_function.dim_state

    def test_forward(self, discrete_state, dim_state, batch_size):
        self.init(discrete_state, dim_state)
        state = random_tensor(discrete_state, dim_state, batch_size)
        value = self.value_function(state)

        assert value.shape == torch.Size([batch_size] if batch_size else [])
        assert value.dtype is torch.float

    def test_parameters(self, discrete_state, dim_state):
        self.init(discrete_state, dim_state)
        old_parameter = self.value_function.parameters
        self.value_function.parameters = old_parameter


class TestNNQFunction(object):
    def init(self, discrete_state, discrete_action, dim_state, dim_action):
        if discrete_state:
            self.num_states = dim_state
            self.dim_state = 1
        else:
            self.num_states = None
            self.dim_state = dim_state

        if discrete_action:
            self.num_actions = dim_action
            self.dim_action = 1
        else:
            self.num_actions = None
            self.dim_action = dim_action

        layers = [32, 32]
        self.q_function = NNQFunction(self.dim_state, self.dim_action,
                                      self.num_states, self.num_actions, layers)

    def test_init(self, discrete_state, discrete_action, dim_state, dim_action):
        if discrete_state and not discrete_action:
            with pytest.raises(NotImplementedError):
                self.init(discrete_state, discrete_action, dim_state, dim_action)

    def test_num_states_actions(self, discrete_state, discrete_action, dim_state, dim_action):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            assert self.num_states == self.q_function.num_states
            assert self.num_actions == self.q_function.num_actions

            if not discrete_state:
                assert self.q_function.num_states is None
            if not discrete_action:
                assert self.q_function.num_actions is None

            assert discrete_state == self.q_function.discrete_state
            assert discrete_action == self.q_function.discrete_action

    def test_dim_state_actions(self, discrete_state, discrete_action, dim_state, dim_action):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            assert self.dim_state == self.q_function.dim_state
            assert self.dim_action == self.q_function.dim_action

    def test_forward(self, discrete_state, discrete_action, dim_state, dim_action, batch_size):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            state = random_tensor(discrete_state, dim_state, batch_size)
            action = random_tensor(discrete_action, dim_action, batch_size)

            value = self.q_function(state, action)
            assert value.shape == torch.Size([batch_size] if batch_size else [])
            assert value.dtype is torch.float

    def test_parameters(self, discrete_state, discrete_action, dim_state, dim_action):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            old_parameter = self.q_function.parameters
            self.q_function.parameters = old_parameter

    def test_partial_q_function(self, discrete_state, discrete_action, dim_state, dim_action, batch_size):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            state = random_tensor(discrete_state, dim_state, batch_size)

            if not discrete_action:
                with pytest.raises(NotImplementedError):
                    self.q_function(state)
            else:
                action_value = self.q_function(state)
                assert action_value.shape == torch.Size(
                    [batch_size, self.num_actions] if batch_size else [self.num_actions]
                )
                assert action_value.dtype is torch.float

    def test_max(self, discrete_state, discrete_action, dim_state, dim_action, batch_size):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            state = random_tensor(discrete_state, dim_state, batch_size)

            if not discrete_action:
                with pytest.raises(NotImplementedError):
                    self.q_function.max(state)
            else:
                q_max = self.q_function.max(state)
                assert q_max.dtype == torch.float
                assert q_max.shape == torch.Size([batch_size] if batch_size else [])

    def test_argmax(self, discrete_state, discrete_action, dim_state, dim_action, batch_size):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)
            state = random_tensor(discrete_state, dim_state, batch_size)

            if not discrete_action:
                with pytest.raises(NotImplementedError):
                    self.q_function.argmax(state)
            else:
                best_action = self.q_function.argmax(state)
                assert best_action.dtype == torch.long
                assert best_action.shape == torch.Size([batch_size] if batch_size else [])

    def test_extract_policy(self, discrete_state, discrete_action, dim_state, dim_action, batch_size):
        if not (discrete_state and not discrete_action):
            self.init(discrete_state, discrete_action, dim_state, dim_action)

            if not discrete_action:
                with pytest.raises(NotImplementedError):
                    self.q_function.extract_policy(temperature=10.)
            else:
                policy = self.q_function.extract_policy(temperature=10.)
                state = random_tensor(discrete_state, dim_state, batch_size)
                action = random_tensor(discrete_action, dim_state, batch_size)
                sample_action = policy(state).sample()
                assert sample_action.shape == torch.Size([batch_size] if batch_size else [])
                assert sample_action.dtype is torch.long


def random_tensor(discrete, dim, batch_size):
    if discrete:
        if batch_size:
            return torch.randint(dim, (batch_size, 1))
        else:
            return torch.randint(dim, ())
    else:
        if batch_size:
            return torch.randn(batch_size, dim)
        else:
            return torch.randn(dim)
