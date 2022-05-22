from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(self, reference: str, sku: str, quantity: int, eta: Optional[date]):
        self.reference = reference
        self.sku = str
        self.eta = eta
        self.available_units = quantity
        self.allocations = set()

    def allocate(self, line: OrderLine):
        self.available_units -= line.quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_units >= line.quantity and self.sku == line.sku
