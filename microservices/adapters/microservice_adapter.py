from core.interfaces.cart_interface import PurchasableInterface

class MicroserviceAdapter(PurchasableInterface):
    def __init__(self, microservice):
        self.microservice = microservice

    def get_price(self) -> float:
        return float(self.microservice.price)

    def get_title(self) -> str:
        return self.microservice.title

    def get_description(self) -> str:
        return self.microservice.description

    def get_type(self) -> str:
        return "microservice"