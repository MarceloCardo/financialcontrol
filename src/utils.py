from pathlib import Path
from config import DOWN_PATH


ROOT_PATH = Path(__file__).parent.parent
ROOT_DOWN_PATH = Path(ROOT_PATH, 'arc')

print(ROOT_PATH.resolve())
if not DOWN_PATH:
    DOWN_PATH = ROOT_DOWN_PATH


def require_env(value):
    if value is None:
        raise ValueError('Env variables not found')
    return value
