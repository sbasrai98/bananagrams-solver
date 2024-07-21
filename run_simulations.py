from joblib import Parallel, delayed
from main import game_loop

Parallel(n_jobs=10)(delayed(game_loop)() for i in range(100))
