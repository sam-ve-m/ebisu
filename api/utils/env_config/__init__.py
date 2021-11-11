import os
import platform
from decouple import Config, RepositoryEnv

config = None
SYSTEM = platform.system()


def get_config(base_path: str) -> Config:
    path = os.path.join(base_path, "opt", "envs", "kami.customer.lionx.com.br", ".env")
    path = str(path)
    print(path)
    return Config(RepositoryEnv(path))


if SYSTEM == "Linux":
    config = get_config("/")
elif SYSTEM == "Windows":
    config = get_config("C:\\")
else:
    raise Exception("Unsupported system")

__all__ = ["config"]
