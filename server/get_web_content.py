import logging
from tool.dotenv import get_firecrawl_bearer_token
import aiohttp

firecrawl_url = "https://api.firecrawl.dev/v1/scrape"


class GetWebContent:
    """
    Get web content from a given URL.
    """

    def __init__(self):
        pass

    async def get_content(self, url: str):
        timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=60000)

        headers = {
            "Authorization": f"Bearer {get_firecrawl_bearer_token()}",
            "Content-Type": "application/json",
        }

        payload = {"url": url, "formats": ["markdown"]}

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                firecrawl_url,
                headers=headers,
                json=payload,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data is not None and data.get("success"):
                        response_data = data.get("data", {})
                        return {
                            "title": response_data.get("metadata", {}).get("title", ""),
                            "markdown": response_data.get("markdown", ""),
                        }

                logging.error(f"Response data: {response.text()}")
                return {"status": response.status}
