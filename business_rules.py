# business_rules.py
# Author: Isabel Cruz

# Rule 2: Discount tiers based on the number of shirts

MEDIUM_ORDER_MIN_SHIRTS = 12
LARGE_ORDER_MIN_SHIRTS = 48
NO_DISCOUNT = 0.0
MEDIUM_ORDER_DISCOUNT = 0.05
LARGE_ORDER_DISCOUNT = 0.10

# Rule 3: Schools get extra percentage, but only on orders of 12+ shirts
SCHOOL_BONUS_MIN_SHIRTS = 12
SCHOOL_BONUS_DISCOUNT = 0.03

# Rule 4: Artwork fee on discounted costs below $100
ARTWORK_FEE_THRESHOLD = 100.00
ARTWORK_FEE = 20.00

# Rule 5: Requires Owner Approval at $750 or more
APPROVAL_LIMIT = 750.00

# Rule #6: Provide a sample shirt to an order when it has 30 shirts or more and its order total is over $400.
SAMPLE_MIN_SHIRTS = 30
SAMPLE_TOTAL_OVER = 400.00


def calculate_shirt_cost(shirt_price: float, shirts: int) -> float:
    """Return the shirt cost before any discount"""
    return shirt_price * shirts


def get_order_discount(shirts: int, school: bool = False) -> float:
    """Return the discount rate as a decimal for this order"""
    if shirts >= LARGE_ORDER_MIN_SHIRTS:
        discount = LARGE_ORDER_DISCOUNT
    elif shirts >= MEDIUM_ORDER_MIN_SHIRTS:
        discount = MEDIUM_ORDER_DISCOUNT
    else:
        discount = NO_DISCOUNT

    if school and shirts >= SCHOOL_BONUS_MIN_SHIRTS:
        discount += SCHOOL_BONUS_DISCOUNT
    return discount


def calculate_order_total(
    shirt_price: float, shirts: int, school: bool = False
) -> float:
    """Return the total cost of the order after discounts and fees when it applies"""
    cost = calculate_shirt_cost(shirt_price, shirts)
    discount = get_order_discount(shirts, school)
    discounted_cost = cost * (1 - discount)

    if discounted_cost < ARTWORK_FEE_THRESHOLD:
        return discounted_cost + ARTWORK_FEE
    return discounted_cost


def needs_approval(total: float) -> bool:
    """Return True when the order toal needs the owener's approval, False otherwise"""
    return total >= APPROVAL_LIMIT


def needs_sample(shirts: int, total: float) -> bool:
    """Return True when the order qualifies for a sample shirt, False otherwise"""
    return shirts >= SAMPLE_MIN_SHIRTS and total > SAMPLE_TOTAL_OVER


def total_ordered(orders: list) -> float:
    """Return the sum of the order totals for every order in the list"""
    total = 0.0
    for order in orders:
        total += calculate_order_total(
            order["shirt_price"], order["shirts"], order.get("school", False)
        )
    return total


def largest_order(orders: list) -> str:
    """Return the team with the largest order total, or "" for an empty list"""
    largest_team = ""
    largest = 0.0
    for order in orders:
        total = calulate_order_total(
            order["shirt_price"], order["shirts"], order["school"]
        )
        if total > largest:
            largest = total
            largest_team = order["team"]
    return largest_team


def format_order_line(team: str, total: float, approval: bool, sample: bool) -> str:
    """Return one report line, with yes or no for each True/False value"""
    approval_text = "no"
    if approval:
        approval_text = "yes"
        sample_text = "no"
    if sample:
        sample_text = "yes"
    return f"{team}: ${total:.2f} | approval: {approval_text} | sample: {sample_text}"
