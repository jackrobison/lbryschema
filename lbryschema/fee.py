from collections import OrderedDict

from lbryschema.base import base_encode, base_decode
from lbryschema.schema import CURRENCY_NAMES, CURRENCY_MAP
from lbryschema.schema.fee import Fee as Fee_pb


def migrate(fee):
    if len(fee.keys()) > 1:
        raise Exception("Invalid fee")

    currency = fee.keys()[0]
    amount = fee[currency]['amount']
    address = fee[currency]['address']

    return Fee_pb.load({
        "version": "_0_0_1",
        "currency": currency,
        "amount": amount,
        "address": base_decode(address, 20, 58)
    })


class Fee(OrderedDict):
    def __init__(self, fee):
        if (len(fee) == 4 and "version" in fee and "currency" in fee
           and "amount" in fee and "address" in fee):
            OrderedDict.__init__(self, fee)
        else:
            OrderedDict.__init__(self, Fee.load_protobuf(migrate(fee)))

    @property
    def currency(self):
        return self['currency']

    @property
    def address(self):
        return self['address']

    @property
    def amount(self):
        return self['amount']

    @classmethod
    def load_protobuf(cls, pb):
        return cls({
                "version": pb.version,
                "currency": CURRENCY_NAMES[pb.currency],
                "address": base_encode(pb.address, 58),
                "amount": pb.amount
        })

    @property
    def protobuf(self):
        pb = {
                "version": self.version,
                "currency": CURRENCY_MAP[self.currency],
                "address": base_decode(self.address, 20, 58),
                "amount": self.amount
        }
        return Fee_pb.load(pb)