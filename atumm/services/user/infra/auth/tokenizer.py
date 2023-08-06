from datetime import datetime, timedelta
from typing import Any, Mapping

import jwt
from jwt import PyJWT

from atumm.services.user.domain.exceptions import (
    DecodeTokenException,
    ExpiredTokenException,
)

jwt_obj = PyJWT()
jwt_obj.options["verify_aud"] = False


class Tokenizer:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(self, payload: dict, expire_period: int = 43200) -> str:
        token = jwt_obj.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=self.secret_key,
            algorithm=self.algorithm,
        )
        return token

    def decode(self, token: str, verify=True) -> Mapping[str, Any]:
        try:
            return jwt_obj.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[self.algorithm],
                verify=verify,
            )
        except jwt.exceptions.DecodeError as e:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException
