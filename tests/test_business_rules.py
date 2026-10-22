from business_rules import (
    calculate_order_total,
    calculate_shirt_cost,
    format_order_line,
    get_order_discount,
    largest_order,
    needs_approval,
    needs_sample,
    total_ordered,
)


# calculate_shirt_cost
def test_shirt_cost_for_an_ordinary_order():
    assert calculate_shirt_cost(11.00, 20) == 220.00


def test_shirt_cost_for_a_single_shirt():
    assert calculate_shirt_cost(10.00, 1) == 10.00


# get_order_discount: the 12 and the 48 limits
def test_no_discount_at_11_shirts():
    assert get_order_discount(11) == 0.0


def test_first_tier_starts_at_exactly_12_shirts():
    assert get_order_discount(12) == 0.05


def test_first_tier_still_applies_at_47_shirts():
    assert get_order_discount(47) == 0.05


def test_top_tier_starts_at_exactly_48_shirts():
    assert get_order_discount(48) == 0.10


# get_order_discount: the school extra
def test_school_extra_does_not_apply_at_11_shirts():
    assert get_order_discount(11, school=True) == 0.0


def test_school_extra_applies_at_exactly_12_shirts():
    assert round(get_order_discount(12, school=True), 2) == 0.08


def test_school_extra_applies_at_on_top_of_the_top_tier():
    assert round(get_order_discount(48, school=True), 2) == 0.13


def test_school_flag_changes_the_answer_at_20_shirts():
    assert get_order_discount(20) == 0.05
    assert round(get_order_discount(20, school=True), 2) == 0.08


# calculate_order_total: the $100 artwork fee limit
def test_artwork_fee_is_added_below_100():
    assert round(calculate_order_total(9.00, 8), 2) == 92.00


def test_no_artwork_fee_at_exactly_100():
    assert round(calculate_order_total(100.00, 1), 2) == 100.00


def test_artwork_fee_is_added_one_cent_below_100():
    assert round(calculate_order_total(99.99, 1), 2) == 119.99


def test_school_order_at_the_top_tier_has_no_fee():
    assert round(calculate_order_total(12.00, 80, school=True), 2) == 835.20


def test_school_below_12_shirts_gets_no_extra_and_pays_the_fee():
    assert round(calculate_order_total(8.50, 10, school=True), 2) == 105.00


# needs_approval: the $750 limit
def test_approval_needed_at_exactly_750():
    assert needs_approval(750.00) is True


def test_no_approval_one_cent_below_750():
    assert needs_approval(749.99) is False


# needs_sample: 30 shirts and over $400 (hold one condition True at a a time)
def test_sample_needed_at_Exactly_30_shirts():
    assert needs_sample(30, 800.00) is True


def test_no_sample_at_29_shirts():
    assert needs_sample(29, 800.00) is False


def test_no_sample_at_exactly_400_dollars():
    assert needs_sample(60, 400.00) is False


def test_sample_needed_one_cent_over_400():
    assert needs_sample(60, 400.00) is False


def test_no_sample_when_neither_condition_is_true():
    assert needs_sample(1, 200.00) is False


# total_ordered
def test_total_ordered_adds_every_order():
    orders = [
        {"team": "A", "shirt_price": 9.00, "shirts": 8, "school": False},
        {"team": "B", "shirt_price": 11.00, "shirts": 20, "school": False},
    ]
    assert round(total_ordered(orders), 2) == 301.00


def test_total_ordered_of_an_empty_list_is_zero():
    assert total_ordered([]) == 0


# largest_order
def test_largest_order_names_the_biggest_order():
    orders = [
        {"team": "A", "shirt_price": 9.00, "shirts": 8, "school": False},
        {"team": "B", "shirt_price": 12.00, "shirts": 80, "school": False},
        {"team": "C", "shirt_price": 11.00, "shirts": 20, "school": False},
    ]
    assert largest_order(orders) == "B"


def test_largest_order_tie_goes_to_the_first_one():
    orders = [
        {"team": "A", "shirt_price": 11.00, "shirts": 20, "school": False},
        {"team": "B", "shirt_price": 11.00, "shirts": 20, "school": False},
    ]
    assert largest_order(orders) == "A"


def test_largest_order_of_one_order_is_that_team():
    orders = [{"team": "A", "shirt_price": 9.00, "shirts": 8, "school": False}]
    assert largest_order(orders) == "A"


def test_largest_order_of_an_empty_list_is_an_empty_string():
    assert largest_order([]) == ""


# format_order_line
def test_order_line_shows_yes_and_no_with_two_decimals():
    line = format_order_line("Foundry Gym", 1234.5, True, False)
    assert line == "Foundry Gym: $1234.50 | approval: yes | sample: no"


def test_order_line_shows_the_other_way_around():
    line = format_order_line("Bayside Runners", 99.0, False, True)
    assert line == "Bayside Runners: $99.00 | approval: no | sample: yes"
