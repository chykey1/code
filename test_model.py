from datetime import date, timedelta
import pytest

from model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def make_test_batch_and_line(sku: str, quantity_batch: int, quantity_line: int):
    return (
        Batch(
            reference="Batch-0001", sku=sku, quantity=quantity_batch, eta=date.today()
        ),
        OrderLine(order_id="my_reference", sku=sku, quantity=quantity_line),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    test_batch, test_line = make_test_batch_and_line("small_chair", 30, 7)
    test_batch.allocate(test_line)

    assert test_batch.available_units == 23


def test_can_allocate_if_available_greater_than_required():
    test_batch, small_line = make_test_batch_and_line("small_chair", 30, 7)

    assert test_batch.can_allocate(small_line) is True


def test_cannot_allocate_if_available_smaller_than_required():
    test_batch, large_line = make_test_batch_and_line("small_chair", 30, 35)

    assert test_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    test_batch, equal_line = make_test_batch_and_line("small_chair", 30, 30)

    assert test_batch.can_allocate(equal_line) is True


def test_cannot_allocate_if_skus_do_not_match():
    test_batch = Batch(
        reference="Batch-0001", sku="small_chair", quantity=30, eta=date.today()
    )
    different_sku_line = OrderLine(
        order_id="my_reference", sku="small_table", quantity=7
    )

    assert test_batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    test_batch, unallocated_line = make_test_batch_and_line("small_chair", 30, 7)
    test_batch.deallocate(unallocated_line)

    assert test_batch.available_units == 30


def test_allocation_idempotency():
    test_batch, test_line = make_test_batch_and_line("small_chair", 20, 2)
    test_batch.allocate(test_line)
    test_batch.allocate(test_line)

    assert test_batch.available_units == 18


def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")


if __name__ == "__main__":
    pytest.main()
