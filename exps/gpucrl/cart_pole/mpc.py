from dotmap import DotMap

from exps.gpucrl.cart_pole.util import get_agent_and_environment
from exps.gpucrl.mpc_arguments import parser
from exps.gpucrl.plotters import plot_last_trajectory
from exps.gpucrl.util import train_and_evaluate

parser.description = 'Run Swing-up Cart-Pole using Model-Based MPC.'
parser.set_defaults(action_cost=0.01, action_scale=3.,
                    mpc_horizon=25,  # default 20
                    mpc_num_iter=5,  # default 5
                    mpc_num_samples=400,  # default 400
                    mpc_num_elites=40,  # default 40
                    mpc_alpha=.1,  # default .1
                    environment_max_steps=200, train_episodes=15,
                    # exploration='expected',  # default optimistic
                    # exploration='thompson',
                    model_kind='DeterministicEnsemble', model_learn_num_iter=50,
                    model_opt_lr=1e-3, render_train=True)
args = parser.parse_args()
print(args)
params = DotMap(vars(args))

environment, agent = get_agent_and_environment(params, 'mpc')
train_and_evaluate(agent, environment, params, plot_callbacks=[plot_last_trajectory])
