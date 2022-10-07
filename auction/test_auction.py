from auction.agent import *


# def run_test_auction():
#     setting = Setting([Task(10, Coordinate(46.74043084171534, 11.441287495316425)),
#                        Task(10, Coordinate(46.7432585363849, 11.444755132354194)),
#                        Task(10, Coordinate(46.742501843894296, 11.44760285662543)),
#                        Task(10, Coordinate(46.75238383331583, 11.446169308339897))])
#
#     auction = Auction(len(setting.tasks))
#     agents = [Bidder(str(i + 1), ) for i in range(5)]
#
#     for _ in range(10):
#         shuffle(agents)
#         for a in agents:
#             a.place_bids(auction)
#         print("round ", len(auction.rounds))
#         for i in range(auction.item_count):
#             print(auction.get_current_round().get_highest_bid(i).price, end=" | ")
#         print("----")
#         auction.finish_round()
#         # print(auction.get_current_round().bids)


def run_auction(previous_round):
    home_coordinate = Coordinate(46.73900067369887, 11.439390329077453)

    tasks = [Task(task['price'], Coordinate(task['position'][1], task['position'][0])) for task in
             previous_round['assets']]
    bidders = [Bidder(Coordinate(bidder['position'][1], bidder['position'][0]), bidder['budget'], tasks,
                      home_coordinate) for bidder in previous_round['bidders']]

    auction = Auction.bids_to_auction(
        previous_round['bids'], [b.id for b in bidders])

    if previous_round['to_the_end']:
        round_count = 0
        while round_count < 1000:
            round_count += 1
            for a in bidders:
                a.place_bids(auction, 3)

            for i in range(auction.item_count):
                print(auction.get_current_round(
                ).get_highest_bid(i).price, end=" | ")
            print("\n----\n")
            change = auction.finish_round()
            if not change:
                print("No change in assignment")
                break
        print("round count: ", round_count)
    else:
        for a in bidders:
            a.place_bids(auction, 3)

        for i in range(auction.item_count):
            print(auction.get_current_round().get_highest_bid(i).price, end=" | ")
        print("\n----\n")
        change = auction.finish_round()
        if not change:
            print("No change in assignment")

    bid_list = []
    print(auction)
    for bidder in bidders:
        bids_for_current_bidder = []
        for item_id in range(len(tasks)):
            bid_to_add = next((bid for bid in auction.get_current_round(
            ).bids[item_id] if bid.bidder_id == bidder.id), None)
            bids_for_current_bidder.append(
                bid_to_add.price if bid_to_add else 0)
        bid_list.append(bids_for_current_bidder)
    previous_round['bids'] = bid_list

    # pprint(previous_round)
    previous_round['routes'] = [
        [[bidder.coordinate.longitude, bidder.coordinate.latitude]] +
        [[tasks[t_id].coordinate.longitude, tasks[t_id].coordinate.latitude] for t_id in bidder.current_path] + [
            [home_coordinate.longitude, home_coordinate.latitude]] for bidder
        in bidders]

    previous_round['finished'] = not change

    return previous_round
