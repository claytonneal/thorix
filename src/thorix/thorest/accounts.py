from __future__ import annotations

import logging

from pydantic import ValidationError

from thorix.errors import ThorixHTTPInvalidJSON
from thorix.http.transport import AsyncTransport, SyncTransport
from thorix.schemas.account import AccountSchema
from thorix.schemas.mappers import map_account
from thorix.types.account import Account
from thorix.types.primitives import Address

logger = logging.getLogger(__name__)


class AccountsAPI:
    """
    Synchronous Accounts API
    """

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def get(self, address: Address) -> Account:
        """
        Retrieve account information

        Endpoint:
            GET /accounts/{address}
        """
        logger.debug("Fetching account %s", address)
        data = self._transport.get_json(f"/accounts/{address}")
        try:
            account_schema = AccountSchema.model_validate(data)
        except ValidationError as exc:
            logger.error("Account response validation failed for %s: %s", address, exc)
            raise ThorixHTTPInvalidJSON("Account response failed validation") from exc
        logger.debug("Account %s fetched successfully", address)
        return map_account(account_schema)


class AsyncAccountsAPI:
    """
    Asynchronous Accounts API
    """

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def get(self, address: Address) -> Account:
        """
        Retrieve account information

        Endpoint:
            GET /accounts/{address}
        """
        logger.debug("Fetching account %s", address)
        data = await self._transport.get_json(f"/accounts/{address}")
        try:
            account_schema = AccountSchema.model_validate(data)
        except ValidationError as exc:
            logger.error("Account response validation failed for %s: %s", address, exc)
            raise ThorixHTTPInvalidJSON("Account response failed validation") from exc
        logger.debug("Account %s fetched successfully", address)
        return map_account(account_schema)
