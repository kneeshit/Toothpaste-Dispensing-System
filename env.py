# import detection.detectionUtils
# import gymnasium as gym
# import numpy as np
# from detection import detection, detectionUtils


# class ToothpasteEnv(gym.Env):
#     def __init__(self, model, camera_index=0):
#         super(ToothpasteEnv, self).__init__()
#         self.model = model
        
#         self.action_space = gym.spaces.Box(low=0, high=1000, shape=(1,), dtype=np.float32)
#         self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(2,), dtype=np.float32)
        
#         self.target_length = detectionUtils.find_target_length(self.model, camera_index=camera_index)
#         self.current_toothpaste_length = 0
#         self.current_rate = 0
        

#     def step(self, action):
#         current = self.action[0]
#         self.apply_force(current)
        
#         _, self.current_toothpaste_length, self.current_rate = detection.find_state(self.model, camera_index=0)

#         reward = self.calculate_reward()
        
#         done = self.current_length >= 0.9 * self.target_length  # Done when we are 90% close to the target length
#         return np.array([self.current_toothpaste_length, self.current_rate]), reward, done, {}

   
#     def reset(self):
#         # Reset the environment
#         _, self.current_toothpaste_length, self.current_rate = detection.find_state(self.model, camera_index=0)
#         return np.array([self.current_toothpaste_length, self.current_rate])


#     def apply_force(self, force):
#         # Apply the force to the motor (simulated or real)
#         pass
    
    
#     def calculate_reward(self):
#         # Calculate the reward based on the current state
#         pass
    


