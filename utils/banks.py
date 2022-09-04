from azbankgateways.banks import BaseBank

class MyBaseBank(BaseBank):
    def __init__(self, identifier: str, **kwargs):
        BaseBank.__init__(self, identifier, **kwargs)
        
    def set_orderId(self, orderId):
        self._order_id = orderId
        
    def get_orderId(self):
        return self._order_id