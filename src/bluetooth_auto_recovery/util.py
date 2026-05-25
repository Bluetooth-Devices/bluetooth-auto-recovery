from __future__ import annotations

import sys

if sys.version_info[:2] < (3, 11):  # pragma: no cover - version-dependent import
    from async_timeout import timeout as asyncio_timeout
else:  # pragma: no cover - version-dependent import
    from asyncio import timeout as asyncio_timeout  # noqa: F401
