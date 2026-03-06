import httpx

from app.modules.agent_tools.base_tool import BaseTool


class CryptoPriceTool(BaseTool):
    name = "crypto_price"
    description = "Get live cryptocurrency prices from CoinGecko by coin id and fiat currency."

    async def execute(self, input_data: dict) -> dict:
        coin_id = input_data.get("coin_id", "bitcoin")
        vs_currency = input_data.get("vs_currency", "usd")
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin_id, "vs_currencies": vs_currency},
            )
            response.raise_for_status()
            return response.json()
