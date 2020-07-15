import mercadopago as mp_base


class MP(mp_base.MP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search_order(self, filters, offset=0, limit=0):
        filters["access_token"] = self.get_access_token()
        filters["offset"] = offset
        filters["limit"] = limit

        # get name of base
        bases = self.__class__.__bases__
        atr = f'_{bases[0].__name__}__rest_client'
        endpoit = "/merchant_orders/search"

        order_result = getattr(self, atr).get(endpoit, filters)
        return order_result

