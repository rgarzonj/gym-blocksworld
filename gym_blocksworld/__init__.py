from gym.envs.registration import register

register(
    id='BlocksWorld-v0',
    entry_point='gym_blocksworld.envs:BlocksWorldEnv',
)
