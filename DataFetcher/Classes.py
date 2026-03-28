from datetime import datetime

class MarketData:
    def __init__(self, id=None, datadate=None, OpenVal=None, CloseVal=None, HighVal=None, LowVal=None, 
                 quantity=None, created_at=None, last_updated_at=None):
        self.id = id
        self.datadate = datadate
        self.OpenVal = OpenVal
        self.CloseVal = CloseVal
        self.HighVal = HighVal
        self.LowVal = LowVal
        self.quantity = quantity

class PriceChange:
    def __init__(self, market_data: MarketData):
        self.market_data = market_data

    def percentage_change(self):
        open_price = self.market_data.OpenVal
        close_price = self.market_data.CloseVal

        if open_price is None or close_price is None or open_price == 0:
            return None

        return ((close_price - open_price) / open_price) * 100