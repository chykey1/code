from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(self, reference: str, sku: str, quantity: int, eta: Optional[date]):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_units = quantity
        self._allocations = set()

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        else:
            return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_units(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_units(self) -> int:
        return self._purchased_units - self.allocated_units

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_units >= line.quantity and self.sku == line.sku


def allocate(line: OrderLine, batches: List[Batch]) -> str:

    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference
