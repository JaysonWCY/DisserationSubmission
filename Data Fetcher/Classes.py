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
