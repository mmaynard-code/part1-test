from otree.api import *
import random
import re
import math
c = Currency


doc = """
This is a multi-round prisoner's dilemma game between multiple participants simultaneously.
"""


class Constants(BaseConstants):
    # Setup information
    name_in_url = 'Game'
    players_per_group = 4
    num_rounds = 10
    timeout_time = 23
    random_names = tuple(
        ["Altair", "Birtum", "Ceres", "Deneb", "Enki", "Faumea", "Ganymede", "Hadar", "Indus", "Kuiper",
         "Lahar", "Meissa", "Nirah", "Oizys", "Phobos", "Rhapso", "Sedna", "Thesan", "Usil", "Vanth"])
    # Used to control the start of rating sharings
    round_share_start = 6

    # Payoff values
    betray_payoff = c(6)
    betrayed_payoff = c(0)
    both_cooperate_payoff = c(5)
    both_defect_payoff = c(2)

    # Reputation and rating
    min_reputation = 0
    max_reputation = 10
    base_reputation = 5

    # Grouping and Neighbours

    # Matrix for PD game group IDs
    matches = {1: [2, 4], 2: [1, 3], 3: [4, 2], 4: [3, 1]}
    # Group 1, groups odd participant IDs
    network1 = [1, 3, 5, 7, 9, 11, 13, 15]
    # Group 2, groups even participant IDs
    network2 = [2, 4, 6, 8, 10, 12, 14, 16]
    # Neighnour network used in Experiment
    treatment_id = [2, 3]
    control_id = [0, 0]
    # Neighbour network for Control
    treatment_c = {1: [2, 16], 2: [3, 1], 3: [4, 2], 4: [5, 3],
                   5: [6, 4], 6: [7, 5], 7: [8, 6], 8: [9, 7],
                   9: [10, 8], 10: [11, 9], 11: [12, 10], 12: [13, 11],
                   13: [14, 12], 14: [15, 13], 15: [16, 14], 16: [1, 15]}
    # Neighbour network for Testing
    treatment_t = {1: [3, 2], 2: [4, 1], 3: [1, 4], 4: [2, 3]}
    # Neighbour network for Treatment 2 Neighbours
    treatment_2 = {1: [3, 15], 2: [4, 16], 3: [5, 1], 4: [6, 2],
                   5: [7, 3], 6: [8, 4], 7: [9, 5], 8: [10, 6],
                   9: [11, 7], 10: [12, 8], 11: [13, 9], 12: [14, 10],
                   13: [15, 11], 14: [16, 12], 15: [1, 13], 16: [2, 14]}
    # Neighbour network for Treatment 3 Neighbours
    treatment_3 = {1: [3, 15, 9], 2: [4, 16, 10], 3: [5, 1, 11], 4: [6, 2, 12],
                   5: [7, 3, 13], 6: [8, 4, 14], 7: [9, 5, 15], 8: [10, 6, 16],
                   9: [11, 7, 1], 10: [12, 8, 2], 11: [13, 9, 3], 12: [14, 10, 4],
                   13: [15, 11, 5], 14: [16, 12, 6], 15: [1, 13, 7], 16: [2, 14, 8]}


class Subsession(BaseSubsession):
    treatment_id = models.IntegerField()
    control_id = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Setup variables
    timed_out = models.StringField(
        initial='a00')
    treatment_id = models.IntegerField()
    control_id = models.IntegerField()
    opponents = models.StringField()
    payoffs = models.StringField()

    # Decision values for both games
    decision1 = models.StringField(
        choices=[['X', 'X'], ['Y', 'Y']],
        doc="""This player's decision"""
    )
    decision2 = models.StringField(
        choices=[['X', 'X'], ['Y', 'Y']],
        doc="""This player's decision"""
    )

    # Rating variables
    my_ratings = models.StringField(
        initial='5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5')
    shared_ratings = models.StringField()
    received_ratings = models.StringField()


class PlayerBot(Bot):
    def play_round(self):
        pass


# FUNCTIONS


def creating_session(subsession):
    # Creates the session and allocates random names from the random names list in Constants
    labels = random.sample(Constants.random_names, 16)
    if subsession.round_number == 1:
        subsession.treatment_id = int(random.sample(Constants.treatment_id, 1)[0])
        subsession.control_id = int(random.sample(Constants.control_id, 1)[0])
    elif subsession.round_number > 1:
        subsession.treatment_id = subsession.in_round(subsession.round_number - 1).treatment_id
        subsession.control_id = subsession.in_round(subsession.round_number - 1).control_id
    if subsession.control_id == 0:
        network1 = Constants.network1.copy()
        network2 = Constants.network2.copy()
        group_matrix = []
        # pop elements from network1 until it's empty
        while network1:
            p1 = int(str(random.sample(network1, 1))[1:-1])
            p2 = int(str(random.sample(network1, 1))[1:-1])
            p3 = int(str(random.sample(network2, 1))[1:-1])
            p4 = int(str(random.sample(network2, 1))[1:-1])
            while p1 == p2:
                p2 = int(str(random.sample(network1, 1))[1:-1])
            while p3 == p4:
                p4 = int(str(random.sample(network2, 1))[1:-1])
            new_group = [
                p1,
                p2,
                p3,
                p4,
            ]
            network1.remove(p1)
            network1.remove(p2)
            network2.remove(p3)
            network2.remove(p4)
            group_matrix.append(new_group)
        subsession.set_group_matrix(group_matrix)
    else:
        subsession.group_randomly()
    for p, label in zip(subsession.get_players(), labels):
        p.participant.label = label
        if subsession.control_id == 0:
            p.treatment_id = subsession.treatment_id
            p.control_id = subsession.control_id
        else:
            p.treatment_id = 2
            p.control_id = 0


def set_payoffs(group: Group):
    # Sets the payoff by group for all the players in the group
    for p in group.get_players():
        set_payoff(p)


def set_ratings(group: Group):
    # Sets the received rating by group for all players in the group
    for p in group.get_players():
        tidy_ratings(p)
        set_received_rating(p)


def round_setup(group: Group):
    # Should fix Internal Error 500
    for p in group.get_players():
        get_my_ratings(p)
        get_opponents(p)


def set_payoff(player: Player):
    # Retrieve opponents for player
    opponent1 = get_opponents(player)[0]
    opponent2 = get_opponents(player)[1]
    # Payoff matrix based on constants
    payoff_matrix = dict(
        X=dict(
            X=Constants.both_cooperate_payoff, Y=Constants.betrayed_payoff
        ),
        Y=dict(
            X=Constants.betray_payoff, Y=Constants.both_defect_payoff
        ),
    )
    # Payoff calculations accounting for timeouts
    payoff1 = payoff_matrix[player.decision1][opponent1.decision1]
    payoff2 = payoff_matrix[player.decision2][opponent2.decision2]
    if opponent1.timed_out == 'd':
        # If both opponents time out on players decisions compensate $4
        payoff1 = 2
    elif opponent1.timed_out == 'b':
        # If both opponents time out on players decisions compensate $4
        payoff1 = 2
    if opponent2.timed_out == 'd':
        # If both opponents time out on players decisions compensate $4
        payoff2 = 2
    elif opponent2.timed_out == 'c':
        # If both opponents time out on players decisions compensate $4
        payoff2 = 2
    if player.timed_out == 'd':
        # If player times out with no decisions, no payoff
        payoff1 = 0
        payoff2 = 0
    elif player.timed_out == 'b':
        # If player timed out with only decision 1, partial payoff
        payoff1 = 0
    elif player.timed_out == 'c':
        # If player timed out with only decision 2, partial payoff
        payoff2 = 0
    player.payoff = payoff1 + payoff2
    player.payoffs = re.sub(r'[\[\]\' ]', '', str(list((payoff1, payoff2))))


def get_earnings(player: Player):
    # Establishes end of round earnings
    earnings = []
    if player.round_number == 10:
        for p in player.in_all_rounds():
            earnings.append(p.payoff)
        earnings = math.floor(sum(random.sample(earnings, 4))/4)
    else:
        earnings = [0]
    return earnings


def get_other_players(player: Player):
    # Builds a pair of variable lists we use to label participants on each page
    all_other_players = []
    for other_player in player.get_others_in_subsession():
        all_other_players.append(other_player)
    all_other_players_labels = []
    for other_player in player.get_others_in_subsession():
        all_other_players_labels.append(other_player.participant.label)
        # all_other_players_labels.sort()
    return dict(
        all_other_players=all_other_players,
        all_other_players_labels=all_other_players_labels
    )


def get_opponents(player: Player):
    # Uses the Constant.matches matrix to assign opponents for 2x PD games
    list_opponents = player.get_others_in_group()
    opponent = []
    for opponent_id in Constants.matches[player.id_in_group]:
        for other_player in list_opponents:
            if other_player.id_in_group == opponent_id:
                opponent.append(other_player)
    player.opponents = opponent[0].participant.label + "," + opponent[1].participant.label
    return opponent


def get_my_ratings(player: Player):
    if player.round_number == 1:
        player.my_ratings = '5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5'
    else:
        player.my_ratings = player.in_round(player.round_number - 1).my_ratings


# def get_ratings(player: Player):
    # Gets the default rating values for each round
    # round_ratings = []
    # round_ratings_avg = []
    # share_settings = []
    # For the first round, use the base reputation and set the share_settings to null to avoid an error
    # if player.round_number == 1:
        # share_settings = ['', '', '', '', '', '']
        # for other_player in player.get_others_in_subsession():
        #     round_ratings.append(Constants.base_reputation)
    # For rounds 7 and onwards we need to incorporate any shared ratings from neighbours, this works for both treatments
    # elif player.round_number > Constants.round_share_start:
    #    prev_ratings = player.in_round(player.round_number - 1).my_ratings.split(",")
    #    for i in prev_ratings:
    #        round_ratings.append(i)
    #    rr = player.in_round(player.round_number - 1).received_ratings.split(",")
    #    # We use the tracker to ensure the rr_sample variable starts at the correct index
    #    tracker = 0
    #    for i in prev_ratings:
    #        # Due to the way shared ratings are formatted they are sorted by neighbour and then by player, hence we need the tracker
    #        rr_sample = rr[tracker::len(player.get_others_in_subsession())]
    #        rr_list = []
    #        # Only stores values that are not our negative values
    #        for j in rr_sample:
    #            # '-1' is assigned for not sharing and '-2' is can't share (eg hasnt met that other participant yet)
    #            if j != '-1' and j != '-2':
    #                rr_list.append(int(j))
    #        tracker = tracker + 1
    #        # Rounds the new_rating down
    #        new_rating = math.floor((int(i) + sum(rr_list)) / (1 + len(rr_list)))
    #        round_ratings_avg.append(new_rating)
    #    round_ratings = round_ratings_avg
    #    # Converts values for whether player did share into 'checked' values for html display
    #    for i in player.in_round(player.round_number - 1).shared_ratings.split(","):
    #        if i != '-1' and i != '-2':
    #            share_settings.append("checked")
    #        else:
    #            share_settings.append("")
    # For all other rounds we just take the players my_ratings from the previous round
    # else:
    #     prev_ratings = player.in_round(player.round_number - 1).my_ratings.split(",")
    #     for i in prev_ratings:
    #         round_ratings.append(i)
    # Returns round_ratings for all rounds, the share_settings, and average aggregate ratings
    # return round_ratings


def get_neighbours(player: Player):
    # Depending on the treatment use a different neighbour matrix from Constants
    list_neighbours = player.get_others_in_subsession()
    treatment = {}
    if player.control_id == 1:
        treatment = Constants.treatment_c
    elif player.treatment_id == 1:
        treatment = Constants.treatment_t
    elif player.treatment_id == 2:
        treatment = Constants.treatment_2
    elif player.treatment_id == 3:
        treatment = Constants.treatment_3
    neighbours = []
    # Returns the neighbours as participant objects for future use
    for neighbour_id in treatment[player.participant.id_in_session]:
        for neighbour in list_neighbours:
            if neighbour.participant.id_in_session == neighbour_id:
                neighbours.append(neighbour)
    return neighbours


def get_known_opponents(player: Player):
    # Uses previous opponents to build a list of known opponents to limit allocation of player rating
    all_other_players_labels = get_other_players(player)['all_other_players_labels']
    opponent_list = []
    known_list = []
    for p in player.in_all_rounds():
        opponent_list.append(p.opponents.split(",")[0])
        opponent_list.append(p.opponents.split(",")[1])
    for i in all_other_players_labels:
        for j in opponent_list:
            if i == j:
                known_list.append(i)
    knowns = list(dict.fromkeys(known_list))
    known_list = []
    for i in all_other_players_labels:
        k = "disabled"
        for j in knowns:
            if j == i:
                k = ""
        known_list.append(k)
    return known_list


def get_base_ratings(player: Player):
    # Uses known opponents to build a list of unknown opponents to limit allocation of player rating
    base_rating_list = []
    for i in get_known_opponents(player):
        if player.round_number > Constants.round_share_start:
            if i == "disabled":
                base_rating_list.append("-2")
            else:
                base_rating_list.append("-1")
        else:
            base_rating_list.append("-2")
    return base_rating_list


def tidy_ratings(player: Player):
    # Tidies up the my_ratings and shared_ratings submitted on the page
    p_ratings = player.my_ratings[0:-1]
    p_shared_ratings = player.shared_ratings[0:-1]
    player.my_ratings = p_ratings
    player.shared_ratings = p_shared_ratings


def set_received_rating(player: Player):
    # Sets player.received_ratings after retrieving them from neighbours
    p_received_ratings = []
    neighbours = get_neighbours(player)
    all_other_players_labels = get_other_players(player)['all_other_players_labels']
    if player.round_number >= Constants.round_share_start:
        # For 2-neighbour treatment collects values from both neighbours
        if player.treatment_id <= 2:
            n1 = neighbours[0]
            n2 = neighbours[1]
            if n1.shared_ratings == '':
                n1.shared_ratings = '-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2'
            if n2.shared_ratings == '':
                n2.shared_ratings = '-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2'
            n1_shared = n1.shared_ratings.split(",")[0::2]
            n2_shared = n2.shared_ratings.split(",")[1::2]
            n1_others = get_other_players(n1)['all_other_players_labels']
            n2_others = get_other_players(n2)['all_other_players_labels']
            for i in all_other_players_labels:
                try:
                    j = n1_others.index(i)
                    p_received_ratings.append(n1_shared[j])
                except ValueError:
                    if i == n1.participant.label:
                        p_received_ratings.append('-2')
            for i in all_other_players_labels:
                try:
                    k = n2_others.index(i)
                    p_received_ratings.append(n2_shared[k])
                except ValueError:
                    if i == n2.participant.label:
                        p_received_ratings.append('-2')
            tracker = 0
            while tracker < 15:
                p_received_ratings.append('')
                tracker = tracker + 1
        # For 3-neighbour treatment collects values from all 3 neighbours
        elif player.treatment_id == 3:
            n1 = neighbours[0]
            n2 = neighbours[1]
            n3 = neighbours[2]
            if n1.shared_ratings == '':
                n1.shared_ratings = '-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2'
            if n2.shared_ratings == '':
                n2.shared_ratings = '-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2'
            if n3.shared_ratings == '':
                n3.shared_ratings = '-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2'
            n1_shared = n1.shared_ratings.split(",")[0::3]
            n2_shared = n2.shared_ratings.split(",")[1::3]
            n3_shared = n3.shared_ratings.split(",")[2::3]
            n1_others = get_other_players(n1)['all_other_players_labels']
            n2_others = get_other_players(n2)['all_other_players_labels']
            n3_others = get_other_players(n3)['all_other_players_labels']
            for i in all_other_players_labels:
                try:
                    j = n1_others.index(i)
                    p_received_ratings.append(n1_shared[j])
                except ValueError:
                    if i == n1.participant.label:
                        p_received_ratings.append('-2')
            for i in all_other_players_labels:
                try:
                    k = n2_others.index(i)
                    p_received_ratings.append(n2_shared[k])
                except ValueError:
                    if i == n2.participant.label:
                        p_received_ratings.append('-2')
            for i in all_other_players_labels:
                try:
                    l = n3_others.index(i)
                    p_received_ratings.append(n3_shared[l])
                except ValueError:
                    if i == n3.participant.label:
                        p_received_ratings.append('-2')
        p_received_ratings = re.sub(r'[\[\]\' ]', '', str(p_received_ratings))
        # Sets player.received_ratings at the end here
        player.received_ratings = p_received_ratings
    return p_received_ratings


# PAGES


class Introduction(Page):
    timeout_seconds = 120

    def is_displayed(self):
        return self.round_number == 1


class GroupWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'round_setup'


class Decision(Page):
    timeout_seconds = 30
    form_model = 'player'
    form_fields = ['decision1', 'decision2']

    def vars_for_template(player: Player):
        # Runs all the functions we need to get the vars we need for the template (includes debug atm)
        if player.treatment_id <= 2:
            neighbour1 = get_neighbours(player)[0].participant.label
            neighbour2 = get_neighbours(player)[1].participant.label
            neighbour3 = ''
        elif player.treatment_id == 3:
            neighbour1 = get_neighbours(player)[0].participant.label
            neighbour2 = get_neighbours(player)[1].participant.label
            neighbour3 = get_neighbours(player)[2].participant.label

        all_other_players_labels = get_other_players(player)['all_other_players_labels']
        disable_list = get_known_opponents(player)
        base_rating_list = get_base_ratings(player)

        if player.my_ratings == '' and player.round_number > 1:
            if player.in_round(player.round_number - 1).my_ratings == '':
                player.my_ratings = '5,5,5,5,5,5,5,5,5,5,5,5,5,5,5'
            else:
                player.my_ratings = player.in_round(player.round_number - 1).my_ratings

        vars_dict = dict(
            # neighbour information
            neighbour1=neighbour1,
            neighbour2=neighbour2,
            neighbour3=neighbour3,
            other_player01_disable=disable_list[0],
            other_player02_disable=disable_list[1],
            other_player03_disable=disable_list[2],
            other_player04_disable=disable_list[3],
            other_player05_disable=disable_list[4],
            other_player06_disable=disable_list[5],
            other_player07_disable=disable_list[6],
            other_player08_disable=disable_list[7],
            other_player09_disable=disable_list[8],
            other_player10_disable=disable_list[9],
            other_player12_disable=disable_list[11],
            other_player11_disable=disable_list[10],
            other_player13_disable=disable_list[12],
            other_player14_disable=disable_list[13],
            other_player15_disable=disable_list[14],
            other_player01_base=base_rating_list[0],
            other_player02_base=base_rating_list[1],
            other_player03_base=base_rating_list[2],
            other_player04_base=base_rating_list[3],
            other_player05_base=base_rating_list[4],
            other_player06_base=base_rating_list[5],
            other_player07_base=base_rating_list[6],
            other_player08_base=base_rating_list[7],
            other_player09_base=base_rating_list[8],
            other_player10_base=base_rating_list[9],
            other_player11_base=base_rating_list[10],
            other_player12_base=base_rating_list[11],
            other_player13_base=base_rating_list[12],
            other_player14_base=base_rating_list[13],
            other_player15_base=base_rating_list[14]
        )

        ratings_dict = dict(
            other_player01_rank=player.my_ratings.split(",")[0],
            other_player02_rank=player.my_ratings.split(",")[1],
            other_player03_rank=player.my_ratings.split(",")[2],
            other_player04_rank=player.my_ratings.split(",")[3],
            other_player05_rank=player.my_ratings.split(",")[4],
            other_player06_rank=player.my_ratings.split(",")[5],
            other_player07_rank=player.my_ratings.split(",")[6],
            other_player08_rank=player.my_ratings.split(",")[7],
            other_player09_rank=player.my_ratings.split(",")[8],
            other_player10_rank=player.my_ratings.split(",")[9],
            other_player11_rank=player.my_ratings.split(",")[10],
            other_player12_rank=player.my_ratings.split(",")[11],
            other_player13_rank=player.my_ratings.split(",")[12],
            other_player14_rank=player.my_ratings.split(",")[13],
            other_player15_rank=player.my_ratings.split(",")[14],
        )
        vars_dict.update(ratings_dict)

        labels_dict = dict(
            opponent1_label=player.opponents.split(",")[0],
            opponent2_label=player.opponents.split(",")[1],
            other_player01=all_other_players_labels[0],
            other_player02=all_other_players_labels[1],
            other_player03=all_other_players_labels[2],
            other_player04=all_other_players_labels[3],
            other_player05=all_other_players_labels[4],
            other_player06=all_other_players_labels[5],
            other_player07=all_other_players_labels[6],
            other_player08=all_other_players_labels[7],
            other_player09=all_other_players_labels[8],
            other_player10=all_other_players_labels[9],
            other_player11=all_other_players_labels[10],
            other_player12=all_other_players_labels[11],
            other_player13=all_other_players_labels[12],
            other_player14=all_other_players_labels[13],
            other_player15=all_other_players_labels[14],
        )
        vars_dict.update(labels_dict)

        return vars_dict

    def before_next_page(player: Player, timeout_happened):
        # Checks to see if a timeout occurred for the player before going to the next page
        if timeout_happened:
            # Checks if any decisions were made prior to timeout
            # If no decisions made, timeout code is d
            if player.decision1 == '' and player.decision2 == '':
                player.decision1 = 'Y'
                player.decision2 = 'Y'
                player.timed_out = 'd'
            # If one decision is made, timeout code is b or c
            elif player.decision1 == '':
                player.decision1 = 'Y'
                player.timed_out = 'b'
            elif player.decision2 == '':
                player.decision2 = 'Y'
                player.timed_out = 'c'
        else:
            # Otherwise ensures timeout value is a
            player.timed_out = 'a'


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    # Calculates payoff, uses timeout_happened check from previous page
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['my_ratings', 'shared_ratings']

    def vars_for_template(player: Player):
        # Runs all the functions we need to get the vars we need for the template (includes debug atm)
        if player.treatment_id <= 2:
            neighbour1 = get_neighbours(player)[0].participant.label
            neighbour2 = get_neighbours(player)[1].participant.label
            neighbour3 = ''
        elif player.treatment_id == 3:
            neighbour1 = get_neighbours(player)[0].participant.label
            neighbour2 = get_neighbours(player)[1].participant.label
            neighbour3 = get_neighbours(player)[2].participant.label

        all_other_players_labels = get_other_players(player)['all_other_players_labels']
        disable_list = get_known_opponents(player)
        base_rating_list = get_base_ratings(player)
        opponent1 = get_opponents(player)[0]
        opponent2 = get_opponents(player)[1]

        if player.my_ratings == '' and player.round_number > 1:
            if player.in_round(player.round_number - 1).my_ratings == '':
                player.my_ratings = '5,5,5,5,5,5,5,5,5,5,5,5,5,5,5'
            else:
                player.my_ratings = player.in_round(player.round_number - 1).my_ratings

        vars_dict = dict(
            # participant information
            neighbour1=neighbour1,
            neighbour2=neighbour2,
            neighbour3=neighbour3,
            other_player01_disable=disable_list[0],
            other_player02_disable=disable_list[1],
            other_player03_disable=disable_list[2],
            other_player04_disable=disable_list[3],
            other_player05_disable=disable_list[4],
            other_player06_disable=disable_list[5],
            other_player07_disable=disable_list[6],
            other_player08_disable=disable_list[7],
            other_player09_disable=disable_list[8],
            other_player10_disable=disable_list[9],
            other_player12_disable=disable_list[11],
            other_player11_disable=disable_list[10],
            other_player13_disable=disable_list[12],
            other_player14_disable=disable_list[13],
            other_player15_disable=disable_list[14],
            other_player01_base=base_rating_list[0],
            other_player02_base=base_rating_list[1],
            other_player03_base=base_rating_list[2],
            other_player04_base=base_rating_list[3],
            other_player05_base=base_rating_list[4],
            other_player06_base=base_rating_list[5],
            other_player07_base=base_rating_list[6],
            other_player08_base=base_rating_list[7],
            other_player09_base=base_rating_list[8],
            other_player10_base=base_rating_list[9],
            other_player11_base=base_rating_list[10],
            other_player12_base=base_rating_list[11],
            other_player13_base=base_rating_list[12],
            other_player14_base=base_rating_list[13],
            other_player15_base=base_rating_list[14]
        )

        ratings_dict = dict(
            other_player01_rank=player.my_ratings.split(",")[0],
            other_player02_rank=player.my_ratings.split(",")[1],
            other_player03_rank=player.my_ratings.split(",")[2],
            other_player04_rank=player.my_ratings.split(",")[3],
            other_player05_rank=player.my_ratings.split(",")[4],
            other_player06_rank=player.my_ratings.split(",")[5],
            other_player07_rank=player.my_ratings.split(",")[6],
            other_player08_rank=player.my_ratings.split(",")[7],
            other_player09_rank=player.my_ratings.split(",")[8],
            other_player10_rank=player.my_ratings.split(",")[9],
            other_player11_rank=player.my_ratings.split(",")[10],
            other_player12_rank=player.my_ratings.split(",")[11],
            other_player13_rank=player.my_ratings.split(",")[12],
            other_player14_rank=player.my_ratings.split(",")[13],
            other_player15_rank=player.my_ratings.split(",")[14],
        )
        vars_dict.update(ratings_dict)

        labels_dict = dict(
            opponent1_label=player.opponents.split(",")[0],
            opponent2_label=player.opponents.split(",")[1],
            other_player01=all_other_players_labels[0],
            other_player02=all_other_players_labels[1],
            other_player03=all_other_players_labels[2],
            other_player04=all_other_players_labels[3],
            other_player05=all_other_players_labels[4],
            other_player06=all_other_players_labels[5],
            other_player07=all_other_players_labels[6],
            other_player08=all_other_players_labels[7],
            other_player09=all_other_players_labels[8],
            other_player10=all_other_players_labels[9],
            other_player11=all_other_players_labels[10],
            other_player12=all_other_players_labels[11],
            other_player13=all_other_players_labels[12],
            other_player14=all_other_players_labels[13],
            other_player15=all_other_players_labels[14],
        )
        vars_dict.update(labels_dict)

        payoffs_dict = dict(
            payoff1=player.payoffs.split(",")[0].replace("cu", ""),
            payoff2=player.payoffs.split(",")[1].replace("cu", ""),
            # Decision values
            my_decision1=player.decision1,
            opponent1_decision=opponent1.decision1,
            same_choice1=player.decision1 == opponent1.decision1,
            my_decision2=player.decision2,
            opponent2_decision=opponent2.decision2,
            same_choice2=player.decision2 == opponent2.decision2,
            # Time out checks
            me_timed_out=player.timed_out,
            opponent1_timed_out=opponent1.timed_out,
            opponent2_timed_out=opponent2.timed_out,
        )
        vars_dict.update(payoffs_dict)

        return vars_dict

    def before_next_page(player: Player, timeout_happened):
        # Checks to see if a timeout occurred for the player before going to the next page
        if timeout_happened:
            player.timed_out = player.timed_out + '1'
        else:
            # Otherwise ensures timeout value is none
            player.timed_out = player.timed_out + '0'

class SharingWaitPage(WaitPage):
    wait_for_all_groups = True
    # Before the next round starts it sets the player.received_ratings for all players
    after_all_players_arrive = 'set_ratings'


class Sharing(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['my_ratings']
    def is_displayed(self):
        return self.round_number >= Constants.round_share_start
    def vars_for_template(player: Player):
        # Runs all the functions we need to get the vars we need for the template (includes debug atm)
        if player.treatment_id <= 2:
            neighbour1 = get_neighbours(player)[0].participant.label
            neighbour2 = get_neighbours(player)[1].participant.label
            neighbour3 = ''
        elif player.treatment_id == 3:
            neighbour1 = get_neighbours(player)[0].participant.label
            neighbour2 = get_neighbours(player)[1].participant.label
            neighbour3 = get_neighbours(player)[2].participant.label

        if player.round_number == 10:
            earnings = get_earnings(player)
            player.participant.payoff = earnings
            player.participant.vars['p1_earnings'] = earnings

        all_other_players_labels = get_other_players(player)['all_other_players_labels']
        opponent1 = get_opponents(player)[0]
        opponent2 = get_opponents(player)[1]

        shared_rating_list = []
        for i in player.received_ratings.split(","):
            if i == '-2' or i == '-1':
                shared_rating_list.append('-')
            else:
                shared_rating_list.append(i)

        if player.my_ratings == '' and player.round_number > 1:
            if player.in_round(player.round_number - 1).my_ratings == '':
                player.my_ratings = '5,5,5,5,5,5,5,5,5,5,5,5,5,5,5'
            else:
                player.my_ratings = player.in_round(player.round_number - 1).my_ratings

        vars_dict = dict(
            # participant information
            neighbour1=neighbour1,
            neighbour2=neighbour2,
            neighbour3=neighbour3,
        )

        ratings_dict = dict(
            other_player01_rank=player.my_ratings.split(",")[0],
            other_player02_rank=player.my_ratings.split(",")[1],
            other_player03_rank=player.my_ratings.split(",")[2],
            other_player04_rank=player.my_ratings.split(",")[3],
            other_player05_rank=player.my_ratings.split(",")[4],
            other_player06_rank=player.my_ratings.split(",")[5],
            other_player07_rank=player.my_ratings.split(",")[6],
            other_player08_rank=player.my_ratings.split(",")[7],
            other_player09_rank=player.my_ratings.split(",")[8],
            other_player10_rank=player.my_ratings.split(",")[9],
            other_player11_rank=player.my_ratings.split(",")[10],
            other_player12_rank=player.my_ratings.split(",")[11],
            other_player13_rank=player.my_ratings.split(",")[12],
            other_player14_rank=player.my_ratings.split(",")[13],
            other_player15_rank=player.my_ratings.split(",")[14],
            # Shared rating information
            other_player01_n1rating=shared_rating_list[0],
            other_player01_n2rating=shared_rating_list[15],
            other_player01_n3rating=shared_rating_list[30],
            other_player02_n1rating=shared_rating_list[1],
            other_player02_n2rating=shared_rating_list[16],
            other_player02_n3rating=shared_rating_list[31],
            other_player03_n1rating=shared_rating_list[2],
            other_player03_n2rating=shared_rating_list[17],
            other_player03_n3rating=shared_rating_list[32],
            other_player04_n1rating=shared_rating_list[3],
            other_player04_n2rating=shared_rating_list[18],
            other_player04_n3rating=shared_rating_list[33],
            other_player05_n1rating=shared_rating_list[4],
            other_player05_n2rating=shared_rating_list[19],
            other_player05_n3rating=shared_rating_list[34],
            other_player06_n1rating=shared_rating_list[5],
            other_player06_n2rating=shared_rating_list[20],
            other_player06_n3rating=shared_rating_list[35],
            other_player07_n1rating=shared_rating_list[6],
            other_player07_n2rating=shared_rating_list[21],
            other_player07_n3rating=shared_rating_list[36],
            other_player08_n1rating=shared_rating_list[7],
            other_player08_n2rating=shared_rating_list[22],
            other_player08_n3rating=shared_rating_list[37],
            other_player09_n1rating=shared_rating_list[8],
            other_player09_n2rating=shared_rating_list[23],
            other_player09_n3rating=shared_rating_list[38],
            other_player10_n1rating=shared_rating_list[9],
            other_player10_n2rating=shared_rating_list[24],
            other_player10_n3rating=shared_rating_list[39],
            other_player11_n1rating=shared_rating_list[10],
            other_player11_n2rating=shared_rating_list[25],
            other_player11_n3rating=shared_rating_list[40],
            other_player12_n1rating=shared_rating_list[11],
            other_player12_n2rating=shared_rating_list[26],
            other_player12_n3rating=shared_rating_list[41],
            other_player13_n1rating=shared_rating_list[12],
            other_player13_n2rating=shared_rating_list[27],
            other_player13_n3rating=shared_rating_list[42],
            other_player14_n1rating=shared_rating_list[13],
            other_player14_n2rating=shared_rating_list[28],
            other_player14_n3rating=shared_rating_list[43],
            other_player15_n1rating=shared_rating_list[14],
            other_player15_n2rating=shared_rating_list[29],
            other_player15_n3rating=shared_rating_list[44],
        )
        vars_dict.update(ratings_dict)

        labels_dict = dict(
            opponent1_label=player.opponents.split(",")[0],
            opponent2_label=player.opponents.split(",")[1],
            other_player01=all_other_players_labels[0],
            other_player02=all_other_players_labels[1],
            other_player03=all_other_players_labels[2],
            other_player04=all_other_players_labels[3],
            other_player05=all_other_players_labels[4],
            other_player06=all_other_players_labels[5],
            other_player07=all_other_players_labels[6],
            other_player08=all_other_players_labels[7],
            other_player09=all_other_players_labels[8],
            other_player10=all_other_players_labels[9],
            other_player11=all_other_players_labels[10],
            other_player12=all_other_players_labels[11],
            other_player13=all_other_players_labels[12],
            other_player14=all_other_players_labels[13],
            other_player15=all_other_players_labels[14],
        )
        vars_dict.update(labels_dict)

        payoffs_dict = dict(
            payoff1=player.payoffs.split(",")[0].replace("cu", ""),
            payoff2=player.payoffs.split(",")[1].replace("cu", ""),
            # Decision values
            my_decision1=player.decision1,
            opponent1_decision=opponent1.decision1,
            same_choice1=player.decision1 == opponent1.decision1,
            my_decision2=player.decision2,
            opponent2_decision=opponent2.decision2,
            same_choice2=player.decision2 == opponent2.decision2,
            # Time out checks
            me_timed_out=player.timed_out,
            opponent1_timed_out=opponent1.timed_out,
            opponent2_timed_out=opponent2.timed_out,
        )
        vars_dict.update(payoffs_dict)

        # Returns values for the template file
        return vars_dict

    def before_next_page(player: Player, timeout_happened):
        # Checks to see if a timeout occurred for the player before going to the next page
        if timeout_happened:
            player.timed_out = player.timed_out + '1'
        else:
            # Otherwise ensures timeout value is none
            player.timed_out = player.timed_out + '0'


class EndWaitPage(WaitPage):
    wait_for_all_groups = True


page_sequence = [Introduction, GroupWaitPage, Decision, ResultsWaitPage, Results, SharingWaitPage, Sharing, EndWaitPage]
