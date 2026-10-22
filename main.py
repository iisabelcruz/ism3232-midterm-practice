from business_rules import (
    calculate_order_total,
    format_order_line,
    largest_order,
    needs_approval,
    needs_sample,
    total_ordered,
)

orders = [
    {"team": "Bayside Runners", "shirt_price": 9.00, "shirts": 8, "school": False},
    {"team": "Cedar Elemantary", "shirt_price": 8.50, "shirts": 10, "school": True},
    {"team": "Dockside Grill", "shirt_price": 11.00, "shirts": 20, "school": False},
    {"team": "Eastlake High", "shirt_price": 10.00, "shirts": 60, "school": True},
    {"team": "Foundary Gym", "shirt_price": 12.00, "shirts": 80, "school": False},
    {"team": "Granite Club", "shirt_price": 16.00, "shirts": 29, "school": False},
    {"team": "Harbor Swim", "shirt_price": 15.00, "shirts": 30, "school": True},
    {"team": "Ironwood FC", "shirt_price": 9.00, "shirts": 40, "school": False},
]

print("Stitchline Uniforms - Order Report")
count = 0
approval_count = 0
sample_count = 0
for order in orders:
    total = calculate_order_total(
        order["shirt_price"], order["shirts"], order["school"]
    )
    approval = needs_approval(total)
    sample = needs_sample(order["shirts"], total)
    count += 1
    if approval:
        approval_count += 1
    if sample:
        sample_count += 1
    print(format_order_line(order["team"], total, approval, sample))

grand_total = total_ordered(orders)
print(f"Orders: {count}")
print(f"Total ordered: ${grand_total:.2f}")
print(f"Average order total: ${grand_total / count:.2f}")
print(f"Largest order total: {largest_order(orders)}")
print(f"Approvals needed: {approval_count}")
print(f"Samples needed: {sample_count}")
