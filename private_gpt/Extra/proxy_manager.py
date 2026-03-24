"""Lightweight proxy manager for streaming support and provider integration.

This module provides a simple, monkey-patchable proxy manager that rotates
through a pool of proxies. It works with both requests.Session and curl_cffi.

Usage:
    >>> from private_gpt.Extra.proxy_manager import ProxyManager
    >>> pm = ProxyManager(['http://proxy1:8080', 'http://proxy2:8080'])
    >>> pm.monkey_patch()  # Patch globally
    >>> # Now all providers use rotating proxies automatically
"""

import asyncio
import threading
import time
from itertools import cycle
from pathlib import Path
from typing import Iterator, Optional

import httpx
from curl_cffi import requests
from curl_cffi.requests import Session as CurlSession
from litprinter import ic


class ProxyManager:
    """Manages and rotates proxies with background Urban VPN fetching support."""

    def __init__(
        self,
        proxies: Optional[list[str]] = None,
        filepath: Optional[str] = None,
        auto_fetch: bool = False,
        debug: bool = False,
    ) -> None:
        self._proxies: list[str] = self._load_initial(proxies, filepath)
        self._pool: Iterator[str] = cycle(self._proxies) if self._proxies else iter([])
        self._lock = threading.Lock()
        self.debug = debug
        self._headers = {
            "origin": "chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        }
        if auto_fetch or not self._proxies:
            threading.Thread(target=self._background_refresh, daemon=True).start()

    def _load_initial(self, proxies: Optional[list[str]], filepath: Optional[str]) -> list[str]:
        loaded = []
        if proxies:
            loaded.extend([p.strip() for p in proxies if p.strip()])
        if filepath and (p := Path(filepath)).exists():
            loaded.extend([line.strip() for line in p.read_text().splitlines() if line.strip()])
        fb = Path("cached_proxies.txt")
        if fb.exists():
            loaded.extend([line.strip() for line in fb.read_text().splitlines() if line.strip()])
        return list(dict.fromkeys(loaded))

    async def _fetch_public_proxies(self) -> list[str]:
        """Fetch proxies from a reliable public list as a fallback."""
        try:
            url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=10)
                if resp.status_code == 200:
                    proxies = [f"http://{p.strip()}" for p in resp.text.splitlines() if p.strip()]
                    import random
                    random.shuffle(proxies)
                    return proxies[:30] # Return 30 random proxies for the pool
        except Exception as e:
            if self.debug:
                ic(f"Failed to fetch public proxies: {e}")
        return []

    async def _fetch_free_proxy_list(self) -> list[str]:
        """Fetch proxies from free-proxy-list.net and test them."""
        try:
            import random
            import re

            async with httpx.AsyncClient() as client:
                r = await client.get("https://free-proxy-list.net/", timeout=10)

                # Use regex to extract all IP:PORT combinations from the raw HTML
                proxies = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b', r.text)

                # Remove duplicates while preserving order
                proxies = list(dict.fromkeys(proxies))

                if not proxies:
                    return []

                # Test a random subset to save time
                random.shuffle(proxies)
                proxies = proxies[:50]

                async def test_proxy(p):
                    try:
                        async with httpx.AsyncClient(proxy=f"http://{p}", timeout=5) as test_client:
                            resp = await test_client.get("http://httpbin.org/ip")
                            if resp.status_code == 200:
                                return f"http://{p}"
                    except Exception:
                        pass
                    return None

                tasks = [test_proxy(p) for p in proxies]
                results = await asyncio.gather(*tasks)
                working = [p for p in results if p]

                if self.debug:
                    ic(f"Found {len(working)} working proxies from free-proxy-list.net")

                return working
        except Exception as e:
            if self.debug:
                ic(f"Failed to fetch free-proxy-list: {e}")
        return []

    async def _fetch_urban_proxies(self) -> list[str]:
        """Fetch proxies from Urban VPN API."""
        import random
        proxy_urls = [None]
        with self._lock:
            if self._proxies:
                proxy_urls = random.sample(self._proxies, min(3, len(self._proxies))) + [None]

        last_err = None
        for proxy_url in proxy_urls:
            client_kwargs = {"headers": self._headers, "timeout": 15}
            if proxy_url:
                client_kwargs["proxy"] = proxy_url
            try:
                async with httpx.AsyncClient(**client_kwargs) as client:
                    # 1. Anon Token
                    r = await client.post(
                        "https://api-pro.falais.com/rest/v1/registrations/clientApps/URBAN_VPN_BROWSER_EXTENSION/users/anonymous",
                        json={
                            "clientApp": {"name": "URBAN_VPN_BROWSER_EXTENSION", "browser": "CHROME"}
                        },
                    )

                    if r.status_code == 429:
                        if self.debug:
                            ic("Urban VPN rate limited. Falling back to public free proxy list...")
                        return await self._fetch_public_proxies()

                    r.raise_for_status()
                    anon_response = r.json()
                    if "value" not in anon_response:
                        if self.debug:
                            ic(f"Urban VPN anon response: {anon_response}")
                        return []
                    anon_token = anon_response["value"]

                    # 2. Access Token
                    r = await client.post(
                        "https://api-pro.falais.com/rest/v1/security/tokens/accs",
                        headers={"authorization": f"Bearer {anon_token}"},
                        json={"type": "accs", "clientApp": {"name": "URBAN_VPN_BROWSER_EXTENSION"}},
                    )
                    r.raise_for_status()
                    accs = r.json()
                    if "value" not in accs:
                        if self.debug:
                            ic(f"Urban VPN accs response: {accs}")
                        return []
                    token = accs["value"]

                    # 3. Countries
                    r = await client.get(
                        "https://stats.falais.com/api/rest/v2/entrypoints/countries",
                        headers={
                            "authorization": f"Bearer {token}",
                            "x-client-app": "URBAN_VPN_BROWSER_EXTENSION",
                        },
                    )
                    r.raise_for_status()
                    countries_response = r.json()
                    if (
                        "countries" not in countries_response
                        or "elements" not in countries_response["countries"]
                    ):
                        if self.debug:
                            ic(f"Urban VPN countries response: {countries_response}")
                        return []
                    countries = countries_response["countries"]["elements"]

                    # 4. Fetch credentials for a few random servers to keep it fast
                    new_proxies = []
                    for country in countries[:10]:  # Limit to 10 countries for speed
                        if "servers" not in country or not country["servers"]["elements"]:
                            continue
                        for server in country["servers"]["elements"][:1]:  # 1 server per country
                            if not server.get("signature"):
                                continue
                            r = await client.post(
                                "https://api-pro.falais.com/rest/v1/security/tokens/accs-proxy",
                                headers={"authorization": f"Bearer {token}"},
                                json={
                                    "type": "accs-proxy",
                                    "clientApp": {"name": "URBAN_VPN_BROWSER_EXTENSION"},
                                    "signature": server["signature"],
                                },
                            )
                            r.raise_for_status()
                            cred_response = r.json()
                            if "value" not in cred_response:
                                if self.debug:
                                    ic(f"Urban VPN cred response: {cred_response}")
                                continue
                            cred = cred_response["value"]
                            if "address" not in server or "primary" not in server["address"]:
                                continue
                            server_addr = server["address"]["primary"]
                            if "ip" not in server_addr or "port" not in server_addr:
                                continue
                            new_proxies.append(
                                f"http://{cred}:{cred}@{server_addr['ip']}:{server_addr['port']}"
                            )
                    return new_proxies
            except Exception as e:
                last_err = e
                continue
        if self.debug and last_err:
            ic(f"Proxy fetch failed all attempts: {last_err}")
        return []

    def _background_refresh(self) -> None:
        """Background loop to refresh proxies."""
        while True:
            # 1. First priority: free-proxy-list.net
            proxies = asyncio.run(self._fetch_free_proxy_list())

            # 2. Second priority: GitHub reliable list
            if not proxies:
                proxies = asyncio.run(self._fetch_public_proxies())

            # 3. Third priority: Urban VPN
            if not proxies:
                proxies = asyncio.run(self._fetch_urban_proxies())

            if proxies:
                with self._lock:
                    # Replace old proxies to avoid 407 Proxy Authentication errors
                    # from expired VPN session tokens hanging around in the pool.
                    self._proxies = list(dict.fromkeys(proxies))
                    self._pool = cycle(self._proxies)
                try:
                    Path("cached_proxies.txt").write_text("\n".join(self._proxies))
                except Exception:
                    pass
                if self.debug:
                    ic(f"Refreshed {len(proxies)} proxies background")
            time.sleep(300)  # Refresh every 5 mins

    def get(self) -> dict[str, str]:
        """Get next proxy in rotation."""
        with self._lock:
            if not self._proxies:
                return {}
            proxy = next(self._pool)
            return {"http": proxy, "https": proxy}

    def patch(self) -> None:
        """Patch requests and curl_cffi to use this manager."""
        original_req_init = requests.Session.__init__
        original_curl_init = CurlSession.__init__
        pm = self

        def patched_req(self: requests.Session, *a, **k) -> None:
            original_req_init(self, *a, **k)
            if p := pm.get():
                self.proxies.update(p)

        def patched_curl(self: CurlSession, *a, **k) -> None:
            k["proxies"] = k.get("proxies") or pm.get()
            original_curl_init(self, *a, **k)

        requests.Session.__init__ = patched_req  # type: ignore
        CurlSession.__init__ = patched_curl  # type: ignore

    def monkey_patch(self) -> None:
        """Alias for patch() for backward compatibility."""
        self.patch()


__all__ = ["ProxyManager"]
