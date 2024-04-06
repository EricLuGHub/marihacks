# import matplotlib.pyplot as plt

# from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from enum import Enum
from csv import DictReader

from dataclasses import dataclass


# marked are solely contra brokers
BROKERS = {
      1: "Anonymous",
      2: "RBC Capital Markets",
      7: "TD Securities Inc.",
      9: "BMO Nesbitt Burns Inc.",
     14: "Virtu Canada Corp.",  #
     19: "Desjardins Securities Inc.",  #
     33: "Canaccord Genuity Corp.",
     39: "Merrill Lynch Canada Inc.",
     53: "Morgan Stanley Canada Ltd.",
     65: "Goldman Sachs Canada Inc.",  #
     70: "Manulife Securities Incorporated",  #
     72: "Credit Suisse Securities (Canada), Inc.",
     79: "CIBC World Markets Inc.",
     80: "National Bank Financial Inc.",
     84: "Independent Trading Group (ITG) Inc.",
     85: "Scotia Capital Inc.",
     88: "Aviso Financial Inc.",  #
    124: "Questrade Inc.",  #
}


class MessageType(Enum):
    ADD       = "A"
    CANCEL    = "X"
    EXECUTION = "E"


class OrderType(Enum):
    BUY  = "B"
    SELL = "S"


@dataclass
class Order:
    order_type: OrderType
    price_per_share: int
    share_count: int
    time: datetime
    order_id: int
    broker: int
    stock: str

    def __str__(self):
        return f"{self.time}  \x1b[32m{self.broker:03} {"bids" if self.order_type is OrderType.BUY else "asks"} for {self.share_count:5} {self.stock} shares @ ${self.price_per_share} (order {self.order_id})\x1b[m"


book: dict[int, Order] = {}

with open("chix.csv", newline='') as f:
    for row in DictReader(f, delimiter=';'):
        time = datetime.fromisoformat(row["time"])
        match MessageType(row["Message Type"]):
            case MessageType.ADD:
                order = Order(
                    order_type=OrderType(row["Buy/Sell Indicator"]),
                    price_per_share=Decimal(row["Price Decimal"]),
                    share_count=int(row["Shares"]),
                    time=time,
                    order_id=int(row["Order Reference"]),
                    broker=int(row["Broker"]),
                    stock=row["Stock"]
                )

                book[order.order_id] = order

                print(order)

            case MessageType.EXECUTION:
                trade_id = int(row["Trade Reference"])
                share_count = int(row["Executed Shares"])
                order_id = int(row["Order Reference"])
                broker = int(row["Broker"])
                contra_order_id = int(row["Contra Order Reference"])
                contra_broker = int(row["Contra Broker"])

                order = book[order_id]

                if order.order_type is OrderType.BUY:
                    operation = "bought"
                    direction = "from"
                else:
                    operation = "  sold"
                    direction = "to"

                print(f"{time}  \x1b[34m{broker:03} {operation} {share_count} {order.stock} shares {direction} {contra_broker:03} (orders {order_id} & {contra_order_id}) - (trade {trade_id})", end="\x1b[m\n")

                order.share_count -= share_count
                if order.share_count <= 0:
                    del book[order_id]

            case MessageType.CANCEL:
                order_id = int(row["Order Reference"])
                cancelled_count = int(row["Cancelled Shares"])

                order = book[order_id]

                if order.share_count == cancelled_count:
                    print(f"{time}  \x1b[31morder {order_id} fully cancelled", end="\x1b[m\n")
                    del book[order_id]
                else:
                    print(f"{time}  \x1b[31morder {order_id} cancelled {cancelled_count} {order.stock} shares out of {order.share_count}", end="\x1b[m\n")
                    order.share_count -= cancelled_count


# buys = defaultdict(int)
# sells = defaultdict(int)
# for order in book.values():
#     d = buys if order.order_type is OrderType.BUY else sells
#     d[order.price_per_share] += order.share_count

# plt.xlabel("price per share")
# plt.ylabel("share count")

# plt.bar(buys.keys(), buys.values(), alpha=.5, width=.01)
# plt.bar(sells.keys(), sells.values(), alpha=.5, width=.01)

# plt.show()
