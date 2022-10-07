from typing import Dict, List

MIN_INCREASE = 0.5


class Bid:
    def __init__(self, bidder_id: str, price: float):
        self.bidder_id = bidder_id
        self.price = price

    def __str__(self):
        return f"{self.bidder} bid {self.price}"


class Round:
    def __init__(self, item_count: int, auctioneer: int) -> None:
        self.item_count = item_count
        self.bids: Dict[int, List[Bid]] = dict(
            [(i, [Bid(auctioneer, 0)]) for i in range(item_count)])
        self.bidPlaced = False

    def place_bid(self, item_id: int, bid: Bid) -> None:
        self.bidPlaced = True
        if item_id in self.bids:
            self.bids[item_id] = list(filter(
                lambda b: bid.bidder_id != b.bidder_id, self.bids[item_id]))
            self.bids[item_id].append(bid)
        else:
            self.bids[item_id] = [bid]

    def get_highest_bid(self, item_id: int) -> Bid:
        if item_id in self.bids:
            max_bid = max(self.bids[item_id], key=lambda bid: bid.price)
            return max_bid
        else:
            print("item number", item_id, "not in bids")
            return None


class Auction:
    def __init__(self, item_count: int):
        self.auctioneer = "0"
        self.rounds: List[Round] = [Round(item_count, self.auctioneer)]
        self.item_count = item_count
        self.finish_round()

    def get_current_round(self) -> Round:
        return self.rounds[-1]

    # finish current round and return if there was any bid
    def finish_round(self) -> bool:
        self.rounds.append(Round(self.item_count, self.auctioneer))
        for i in range(self.item_count):
            self.rounds[-1].bids[i] += self.rounds[-2].bids[i][1:]
        return self.rounds[-2].bidPlaced

    def get_result(self) -> Dict[int, Bid]:
        result = {}
        for item_id in range(self.item_count):
            result[item_id] = self.get_current_round().get_highest_bid(item_id)
        return result

    def take_back_bid_cost(self, item_id: int):
        return self.get_current_round().get_highest_bid(item_id).price * 0.5 + 1

    def place_bid(self, item_id: int, bid: Bid):
        self.get_current_round().place_bid(item_id, bid)

    def takeback_bid(self, item_id: int, bid: Bid):
        self.get_current_round().bids[item_id].remove(bid)
        print("must pay fee of", self.take_back_bid_cost(
            item_id), "to take back bid on item", item_id)

    def bids_to_auction(bids:List[List[float]], bidder_ids:List[str]):
        auction = Auction(len(bids[0]))
        for i,bidder_id in enumerate(bidder_ids):
            for item_id in range(auction.item_count):
                auction.place_bid(item_id, Bid(bidder_id, bids[i][item_id]))
        auction.finish_round()
        return auction
