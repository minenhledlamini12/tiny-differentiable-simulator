import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import pytinydiffsim 


class ReacherPyTinyDiffSim(gym.Env):
  metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 50}

  def __init__(self):
    
    self.tds_env = pytinydiffsim.ReacherEnv()

    self._render_width = 320
    self._render_height = 200

    self.force_mag = 1

    action_dim = 2
    action_high = np.array([self.force_mag] * action_dim, dtype=np.float32)
    self.action_space = spaces.Box(-action_high, action_high, dtype=np.float32)
    high = np.array([1,1,1,1, 4,4,200,200,4,4])
    self.observation_space = spaces.Box(-high, high, dtype=np.float32)

    self.seed()
    #    self.reset()
    self.viewer = None
    self._configure()

  def _configure(self, display=None):
    self.display = display

  

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    s = int(seed) & 0xffffffff
    self.tds_env.seed(s)
    return [seed]

  def rollout(self, max_steps, shift):
    res = self.tds_env.rollout(max_steps, shift)
    return res.total_reward, res.num_steps
  
  def policy(self, ob):
      ac = self.tds_env.policy(ob)
      return [ac]

  def step(self, action):
    force = action
    result = self.tds_env.step(force)
    self.state = result.obs
    #print("state=",self.state)
    done = result.done
    reward = result.reward
    return np.array(self.state), reward, done, {}

  def reset(self):
    self.state = self.tds_env.reset()
    #print("self.state=", self.state)
    return np.array(self.state)

  def update_weights(self, weights):
    #print("dir(self.tds_env=)", dir(self.tds_env))
    self.tds_env.update_weights(weights)
    
  def render(self, mode='human', close=False):
    #print("render mode=", mode)
    #if mode == "human":
    #  self._renders = True
    #if mode != "rgb_array":
    #  return np.array([])
    #px = np.array([[[255,255,255,255]]*self._render_width]*self._render_height, dtype=np.uint8)
    #rgb_array = np.array(px, dtype=np.uint8)
    #rgb_array = np.reshape(np.array(px), (self._render_height, self._render_width, -1))
    #rgb_array = rgb_array[:, :, :3]
    return []

  def configure(self, args):
    pass
    
  def close(self):
    del self.tds_env
    
