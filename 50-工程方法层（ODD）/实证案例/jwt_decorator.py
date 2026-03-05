import jwt
import functools
from datetime import datetime, timedelta
from typing import Optional, Callable, Any, Dict
from enum import Enum


class TokenError(Exception):
    pass


class TokenExpiredError(TokenError):
    pass


class TokenInvalidError(TokenError):
    pass


class TokenMissingError(TokenError):
    pass


class JWTAuthDecorator:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        token_expiration: int = 3600,
        refresh_expiration: int = 86400,
        token_prefix: str = "Bearer",
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiration = token_expiration
        self.refresh_expiration = refresh_expiration
        self.token_prefix = token_prefix

    def generate_token(
        self, payload: Dict[str, Any], expiration: Optional[int] = None
    ) -> str:
        try:
            exp_time = expiration or self.token_expiration
            token_payload = payload.copy()
            token_payload.update(
                {
                    "exp": datetime.utcnow() + timedelta(seconds=exp_time),
                    "iat": datetime.utcnow(),
                }
            )
            return jwt.encode(token_payload, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            raise TokenError(f"Token generation failed: {str(e)}")

    def generate_refresh_token(self, payload: Dict[str, Any]) -> str:
        return self.generate_token(payload, expiration=self.refresh_expiration)

    def decode_token(self, token: str, verify: bool = True) -> Dict[str, Any]:
        try:
            if verify:
                decoded = jwt.decode(
                    token, self.secret_key, algorithms=[self.algorithm]
                )
            else:
                decoded = jwt.decode(
                    token,
                    self.secret_key,
                    algorithms=[self.algorithm],
                    options={"verify_signature": False},
                )
            return decoded
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError:
            raise TokenInvalidError("Invalid token")
        except Exception as e:
            raise TokenError(f"Token decoding failed: {str(e)}")

    def verify_token(self, token: str) -> bool:
        try:
            self.decode_token(token, verify=True)
            return True
        except TokenError:
            return False

    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = self.decode_token(refresh_token, verify=True)
            payload.pop("exp", None)
            payload.pop("iat", None)
            return self.generate_token(payload)
        except TokenError as e:
            raise TokenError(f"Token refresh failed: {str(e)}")

    def extract_token_from_header(self, auth_header: Optional[str]) -> str:
        if not auth_header:
            raise TokenMissingError("Authorization header missing")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.token_prefix:
            raise TokenInvalidError(
                f"Invalid authorization header format. Expected: '{self.token_prefix} <token>'"
            )

        return parts[1]

    def __call__(
        self,
        token_getter: Optional[Callable] = None,
        required_claims: Optional[list] = None,
        optional: bool = False,
    ):
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    if token_getter:
                        token = token_getter(*args, **kwargs)
                    else:
                        token = kwargs.get("token") or (
                            args[0] if args else None
                        )

                    if not token:
                        if optional:
                            kwargs["jwt_payload"] = None
                            return func(*args, **kwargs)
                        raise TokenMissingError("Token not provided")

                    if isinstance(token, str) and token.startswith(self.token_prefix):
                        token = self.extract_token_from_header(token)

                    payload = self.decode_token(token, verify=True)

                    if required_claims:
                        missing_claims = [
                            claim for claim in required_claims if claim not in payload
                        ]
                        if missing_claims:
                            raise TokenInvalidError(
                                f"Missing required claims: {missing_claims}"
                            )

                    kwargs["jwt_payload"] = payload
                    return func(*args, **kwargs)

                except TokenExpiredError as e:
                    if optional:
                        kwargs["jwt_payload"] = None
                        kwargs["jwt_error"] = str(e)
                        return func(*args, **kwargs)
                    raise

                except (TokenInvalidError, TokenMissingError, TokenError) as e:
                    if optional:
                        kwargs["jwt_payload"] = None
                        kwargs["jwt_error"] = str(e)
                        return func(*args, **kwargs)
                    raise

            return wrapper

        return decorator

    def require_auth(
        self,
        token_getter: Optional[Callable] = None,
        required_claims: Optional[list] = None,
    ):
        return self(token_getter=token_getter, required_claims=required_claims)

    def optional_auth(
        self,
        token_getter: Optional[Callable] = None,
        required_claims: Optional[list] = None,
    ):
        return self(
            token_getter=token_getter, required_claims=required_claims, optional=True
        )


# 使用示例
if __name__ == "__main__":
    jwt_auth = JWTAuthDecorator(secret_key="your-secret-key-here")

    # 生成token
    token = jwt_auth.generate_token({"user_id": 123, "role": "admin"})
    print(f"Generated token: {token}")

    # 验证token
    @jwt_auth.require_auth(required_claims=["user_id"])
    def protected_function(token: str, jwt_payload: Dict[str, Any]):
        print(f"User ID: {jwt_payload['user_id']}")
        print(f"Role: {jwt_payload.get('role', 'N/A')}")
        return "Success"

    # 可选认证
    @jwt_auth.optional_auth()
    def optional_function(token: str = None, jwt_payload: Dict[str, Any] = None):
        if jwt_payload:
            print(f"Authenticated user: {jwt_payload.get('user_id')}")
        else:
            print("Anonymous user")

    try:
        result = protected_function(token=token)
        print(result)
    except TokenError as e:
        print(f"Error: {e}")

    # 刷新token
    refresh_token = jwt_auth.generate_refresh_token({"user_id": 123})
    new_token = jwt_auth.refresh_access_token(refresh_token)
    print(f"Refreshed token: {new_token}")