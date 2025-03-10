from __future__ import annotations

import unittest

import gymnasium.utils.env_checker
from pettingzoo.test import parallel_api_test
from pettingzoo.test.seed_test import parallel_seed_test
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
import ray.rllib.utils

from sustaingym.envs.cogen import CogenEnv, MultiAgentCogenEnv


class TestSingleAgentEnv(unittest.TestCase):
    def setUp(self) -> None:
        self.env = CogenEnv()

    def tearDown(self) -> None:
        self.env.close()

    def test_check_env(self) -> None:
        gymnasium.utils.env_checker.check_env(self.env)

    def test_rllib_check_env(self) -> None:
        ray.rllib.utils.check_env(self.env)


class TestMultiAgentEnv(unittest.TestCase):
    def setUp(self) -> None:
        self.env = MultiAgentCogenEnv()

    def tearDown(self) -> None:
        self.env.close()

    def test_pettingzoo_parallel_api(self) -> None:
        parallel_api_test(self.env, num_cycles=1000)

    def test_pettingzoo_parallel_seed(self) -> None:
        parallel_seed_test(MultiAgentCogenEnv)

    def test_rllib_check_env(self) -> None:
        rllib_env = ParallelPettingZooEnv(self.env)
        ray.rllib.utils.check_env(rllib_env)


if __name__ == '__main__':
    unittest.main()
