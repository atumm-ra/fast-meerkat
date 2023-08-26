from bcrypt import gensalt, hashpw


class PasswordHasher:
    def __init__(self, password_key: str) -> None:
        """
        Send a message to a recipient.
        :param str password_key: The password application key
        """
        self.password_key = password_key

    def hash_password(self, password: str, salt: str):
        pass_combination = password + self.password_key
        return hashpw(pass_combination, salt)

    def is_password_valid(self, password: str, salt: str) -> bool:
        input_pass_hashed = hashpw(password + self.password_key, salt)
        return self.password == input_pass_hashed

    def generate_salt(self) -> str:
        return gensalt()
