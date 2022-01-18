from redis import Redis


class RedisInfrastructure:
    @staticmethod
    def get_connection(**kwargs):
        return Redis(
            host=kwargs.get("host"),
            port=kwargs.get("port"),
            db=kwargs.get("db"),
            password=kwargs.get("password"),
        )
