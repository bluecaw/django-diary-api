import os
from functools import lru_cache

import jwt
from jwt import PyJWKClient
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from django.contrib.auth import get_user_model


@lru_cache(maxsize=1)
def get_jwks_client(tenant_id):
    jwks_url = (
        f"https://login.microsoftonline.com/{tenant_id}"
        "/discovery/v2.0/keys"
    )
    return PyJWKClient(jwks_url)


class EntraIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        # Authorizationヘッダーがない場合は、この認証方式では判定しない
        if not auth:
            return None

        if auth[0].lower() != b"bearer":
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed(
                "Invalid Authorization header."
            )

        token = auth[1].decode("utf-8")

        tenant_id = os.environ.get("ENTRA_TENANT_ID", "")
        api_client_id = os.environ.get("ENTRA_API_CLIENT_ID", "")
        required_scope = "Diary.ReadWrite"

        if not tenant_id or not api_client_id:
            raise exceptions.AuthenticationFailed(
                "Entra ID environment variables are not configured."
            )

        expected_issuer = (
            f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        )

        try:
            signing_key = get_jwks_client(
                tenant_id
            ).get_signing_key_from_jwt(token)

            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=api_client_id,
                issuer=expected_issuer,
                options={"require": ["exp", "iss", "aud", "tid"]},
            )

        except jwt.PyJWTError as exc:
            raise exceptions.AuthenticationFailed(
                "Invalid or expired Entra ID access token."
            ) from exc
        except Exception as exc:
            raise exceptions.AuthenticationFailed(
                "Unable to validate Entra ID access token."
            ) from exc

        if claims.get("tid") != tenant_id:
            raise exceptions.AuthenticationFailed(
                "Token tenant does not match."
            )

        scopes = claims.get("scp", "").split()
        if required_scope not in scopes:
            raise exceptions.AuthenticationFailed(
                "Required scope is missing."
            )

        entra_oid = claims.get("oid")
        if not entra_oid:
            raise exceptions.AuthenticationFailed(
                "Token does not contain an object ID."
            )

        User = get_user_model()
        username = f"entra_{entra_oid}"

        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                "email": claims.get("preferred_username", ""),
            },
        )

        return (user, claims)

    def authenticate_header(self, request):
        return "Bearer"
