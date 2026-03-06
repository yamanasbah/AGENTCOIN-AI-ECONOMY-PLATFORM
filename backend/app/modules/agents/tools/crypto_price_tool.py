import httpx

from app.modules.agents.tools.base import AgentTool


class CryptoPriceTool(AgentTool):
    name = "crypto_price"
    description = "Fetches live cryptocurrency prices via CoinGecko API."

    def run(self, input: dict) -> dict:
        symbol = ((input or {}).get("symbol") or "bitcoin").lower()
        vs_currency = ((input or {}).get("vs_currency") or "usd").lower()

        try:
            response = httpx.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": symbol, "vs_currencies": vs_currency},
                timeout=8.0,
            )
            response.raise_for_status()
            payload = response.json()
            price = payload.get(symbol, {}).get(vs_currency)
            if price is None:
                return {"error": f"Price not found for {symbol}/{vs_currency}"}
            return {"symbol": symbol, "vs_currency": vs_currency, "price": price}
        except Exception as exc:  # best-effort tool output for agent loop
            return {"error": str(exc), "symbol": symbol, "vs_currency": vs_currency}
