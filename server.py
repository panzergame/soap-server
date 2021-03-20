import logging

from spyne import Application, rpc, ServiceBase, \
	Integer, Decimal, Unicode
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from money.money import Money
from money.currency import Currency

logging.basicConfig(level=logging.DEBUG)


class ShippingService(ServiceBase):
	@rpc(Decimal, Decimal, _returns=Decimal)
	def compute_shipping_cost(self, distance, total_weight):
		cost = Money('5', Currency.EUR) + \
			(Money('0.01', Currency.EUR) + Money('0.05', Currency.EUR) * total_weight) * \
			distance

		return cost.amount


application = Application(
	[ShippingService],
	tns='info802.soap.shipping',
	in_protocol=Soap11(validator='lxml'),
	out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)
