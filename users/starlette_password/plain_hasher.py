from starlette_password.hashers import BasePasswordHasher, constant_time_compare


class PlainPasswordHasher(BasePasswordHasher):
    """
    Used to have fast unit tests!

    Not for production use!
    """

    algorithm = "plain"

    def salt(self):
        return ""

    def encode(self, password, salt):
        return "%s$%s$%s" % (self.algorithm, "", password)

    def decode(self, encoded):
        algorithm, salt, password = encoded.split("$", 2)
        assert algorithm == self.algorithm
        return {"algorithm": algorithm, "password": password, "salt": salt}

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        return constant_time_compare(decoded["password"], password)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            "algorithm": decoded["algorithm"],
            "salt": decoded["salt"],
            "password": decoded["password"],
        }

    def harden_runtime(self, password, encoded):
        pass
