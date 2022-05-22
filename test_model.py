from datetime import date, timedelta
import pytest

from model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    test_batch = Batch(
        reference="Batch-0001", sku="small_chair", quantity=30, eta=date.today()
    )
    line = OrderLine(order_id="my_reference", sku="small_chair", quantity=7)

    test_batch.allocate(line)

    assert test_batch.available_units == 23


def test_can_allocate_if_available_greater_than_required():
    pytest.fail("todo")


def test_cannot_allocate_if_available_smaller_than_required():
    pytest.fail("todo")


def test_can_allocate_if_available_equal_to_required():
    pytest.fail("todo")


def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")
