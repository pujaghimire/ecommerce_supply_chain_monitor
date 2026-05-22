"""Generate synthetic product movement CSV used by the demo pipeline."""
import csv
from pathlib import Path


def generate(path: str = "data/synthetic_products.csv", n: int = 200):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rows = []
    import random, datetime
    for i in range(n):
        pid = f"P{random.randint(1,20)}"
        sid = f"S{random.randint(1,5)}"
        qty = random.choice([0,1,2,3,5,10,50,100])
        price = round(random.uniform(1.0, 500.0), 2)
        ts = (datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0, 60*24))).isoformat() + "Z"
        rows.append({"product_id": pid, "seller_id": sid, "quantity": qty, "price": price, "timestamp": ts})

    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["product_id","seller_id","quantity","price","timestamp"])
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote", path)


if __name__ == "__main__":
    generate()
