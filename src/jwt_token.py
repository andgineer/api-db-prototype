"""
JWT cryptography.

Checked with https://jwt.io/#debugger-io
"""
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import jwt
import settings
from journaling import log
from jwt.exceptions import PyJWTError
import datetime


JWT_EXPIRATION = 'exp'
JWT_CREATED = 'iat'


class JwtCrypto:
    """
    Jwt encoder/decoder
    """
    _public_key: bytes = None
    _private_key: bytes = None


    @property
    def public_key(self):
        """
        For lazy loading so we can set key's files beforehand
        """
        if not self._public_key:
            log.debug(f'Loading public key from {settings.config.jwt_public_key_file}')
            cert_str = open(settings.config.jwt_public_key_file, 'rb').read()
            cert_obj = load_pem_x509_certificate(cert_str, default_backend())
            self._public_key = cert_obj.public_key()
        return self._public_key

    @property
    def private_key(self):
        """
        For lazy loading so we can set key's files beforehand
        """
        if not self._private_key:
            log.debug(f'Loading private key from {settings.config.jwt_secret_key_file}')
            self._private_key = open(settings.config.jwt_secret_key_file, 'rb').read()
        return self._private_key

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.private_key, algorithm='RS256').decode()

    def decode(self, encoded: str) -> dict:
        try:
            decoded = jwt.decode(
                encoded,
                self.public_key,
                algorithms='RS256',
            )
        except PyJWTError as e:
            decoded = None
            log.debug(f'Decode error for jwt "{encoded}": {e}')
        return decoded

    @staticmethod
    def datetime2jwt(utc_time):
        """
        Converts utc_time into POSIX (assuming that utc_time is in utc timezone)
        """
        return str(utc_time.timestamp()).split('.')[0]

    @staticmethod
    def jwt2datetime(jwt_time):
        """
        Converts POSIX time into utc datetime
        """
        return datetime.datetime.fromtimestamp(int(jwt_time))


token = JwtCrypto()
