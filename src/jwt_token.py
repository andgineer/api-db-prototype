"""JWT cryptography.

Checked with https://jwt.io/#debugger-io
"""

import datetime
from datetime import timezone
from typing import Any, Dict, Optional

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from jwt.exceptions import PyJWTError

import settings
from journaling import log

JWT_EXPIRATION = "exp"
JWT_CREATED = "iat"
JWT_MIN_LENGTH = 50


class JwtCrypto:
    """JWT encoder/decoder."""

    _public_key: Optional[bytes] = None
    _private_key: Optional[bytes] = None

    @property
    def public_key(self) -> bytes:
        """Facilitate lazy loading so we can set key's files beforehand."""
        assert settings.config
        assert hasattr(settings.config, "jwt_public_key_file") and isinstance(
            settings.config.jwt_public_key_file,
            str,
        )
        if not self._public_key:
            log.debug(f"Loading public key from {settings.config.jwt_public_key_file}")
            cert_str = open(settings.config.jwt_public_key_file, "rb").read()
            cert_obj = load_pem_x509_certificate(cert_str, default_backend())
            self._public_key = cert_obj.public_key()  # type: ignore
        return self._public_key  # type: ignore

    @property
    def private_key(self) -> bytes:
        """Facilitate lazy loading so we can set key's files beforehand."""
        assert settings.config
        assert hasattr(settings.config, "jwt_public_key_file") and isinstance(
            settings.config.jwt_secret_key_file,
            str,
        )
        if not self._private_key:
            log.debug(f"Loading private key from {settings.config.jwt_secret_key_file}")
            self._private_key = open(settings.config.jwt_secret_key_file, "rb").read()
        return self._private_key

    def encode(self, payload: Dict[str, Any]) -> str:
        """Encode payload into jwt string."""
        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def decode(self, encoded: str) -> Optional[Dict[str, Any]]:
        """Decode jwt string into payload."""
        try:
            decoded = jwt.decode(
                encoded,
                self.public_key,
                algorithms=["RS256"],
            )
        except PyJWTError as e:
            decoded = None
            log.debug(f'Decode error for jwt "{encoded}": {e}')
        return decoded  # type: ignore

    @staticmethod
    def datetime2jwt(utc_time: datetime.datetime) -> str:
        """Convert utc_time into POSIX (assuming that utc_time is in utc timezone)."""
        return str(utc_time.timestamp()).split(".", maxsplit=1)[0]

    @staticmethod
    def jwt2datetime(jwt_time: str) -> datetime.datetime:
        """Convert POSIX time into utc datetime."""
        return datetime.datetime.fromtimestamp(int(jwt_time), tz=timezone.utc)


token = JwtCrypto()
