from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from random import randrange
import numpy
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Interaction'
    players_per_group = 4
    num_rounds = 5
    num_participants = 16
    match_step1 = {1:[3,4], 2:[4], 3:[1], 4:[1,2]}
    match_step2 = {
        1: {1:[2], 2:[1,3], 3:[2,4], 4:[3]},
        2: {1:[3,4], 2:[4], 3:[1], 4:[1,2]},
        3: {1: [2,3,4], 2: [1,3,4], 3:[1,2,4], 4:[1,2,3]},
        4: {1:[2], 2:[1], 3:[4], 4:[3]},
        5: {1:[3], 2:[3], 3:[1], 4:[2]}
    }
    match_step3 = {1: [2,3,4], 2: [1,3,4], 3:[1,2,4], 4:[1,2,3]}
    num_issues = [3,1,4,2,5] 
    issues_list = ["The government of your country should subsidize public transport in [0…100] percent.",
    "The warning signs on cigarette boxes should cover [0…100] percent of the box total surface.",
    "The government of your country has to divide an available budget between two options: building new highways or new high-speed railway tracks. [0…100] percent of these resources should be used to build new high-speed railway tracks.",
    "[0…100] percent of immigrants who come to your country now for economic reasons should receive a residence permit.",
    "The military of your country has to divide its total budget between activities within the national borders, such as national defense and training, and peace-keeping (non-combative) missions outside the country. Foreign missions should receive [0…100] percent of the total budget."] 


class Subsession(BaseSubsession):

    def do_my_shuffle(self):
        name_list = ['Bestla','Chaldene','Daphnis','Elara','Farbauti','Galatea','Halimede','Iocaste','Jarnsaxa','Lysithea',
            'Metis','Nereid','Orthosie','Pasiphae','Sinope','Thyone']
        #name_list = ['Bestla','Chaldene','Daphnis','Elara','Farbauti','Galatea','Halimede','Iocaste']
        random.shuffle(name_list)
        for p in self.get_players():
                       
            if self.round_number == 1:                       
                p.participant.vars['num_timeout'] = 0
                p.participant.vars['is_dropout'] = False
                p.participant.vars['check_dropout'] = False

            all_issues = p.participant.vars['issues_answers']
            num_issue = Constants.num_issues[self.round_number-1]
            p.participant.vars['this_issue'] = all_issues[num_issue-1]
            p.participant.vars['last_this_issue'] = p.participant.vars['this_issue']
            p.participant.vars['name'] = name_list[p.id_in_subsession-1]
            p.participant.vars['likability'] = {1:0, 2:0, 3:0, 4:0}


        pl = sorted(
            self.get_players(), 
            key=lambda player: player.participant.vars['this_issue']
        )
        #matrix = [[0,1,6,7],[2,3,4,5]]
        matrix = [[0, 1, 14, 15], [2, 3, 12, 13], [4, 5, 10, 11], [6, 7, 8, 9]]
        group_matrix = []
        for row in matrix:
            r = []
            for i in row:
                p_id = pl[i].id_in_subsession
                r.append(p_id)
            group_matrix.append(r)

        self.set_group_matrix(group_matrix)

        for p in self.get_players():
            group_id = p.group.id_in_subsession
            name = p.participant.vars['name']
            opinion = p.participant.vars['this_issue']
            my_id = p.id_in_group
            p.participant.label = str(name)+","+str(group_id)+","+ str(my_id)+","+str(opinion)


class Group(BaseGroup):
    def save_update_answer(self, step):
        for p in self.get_players():
            p.participant.vars['last_this_issue'] = p.participant.vars['this_issue']
            if step == "2_1":
                p.participant.vars['this_issue'] = p.re_issue_step2_1
            if step == "2_2":
                p.participant.vars['this_issue'] = p.re_issue_step2_2
            if step == "2_3":
                p.participant.vars['this_issue'] = p.re_issue_step2_3
                p.participant.vars['last_this_issue'] = p.re_issue_step2_3
            if step == "3":
                p.participant.vars['this_issue'] = p.re_issue_step3_1

    
    def send_messages_step2_1(self):
        for p in self.get_players():
            parterner_id_step2 = p.get_parternersid_step2()
            num_p = len(parterner_id_step2)
            m_dict = {1:"", 2:"", 3:"", 4:""} 
            my_answer = "My opinion on this issue is " + str(p.participant.vars['this_issue']) + ". "
           
            p1_id = parterner_id_step2[0]
            m_dict[p1_id] = my_answer + p.message_step2_1_1
            if num_p != 1:
                p2_id = parterner_id_step2[1]
                m_dict[p2_id] = my_answer + p.message_step2_1_2
                if num_p == 3:
                    p3_id = parterner_id_step2[2]
                    m_dict[p3_id] = my_answer + p.message_step2_1_3
            
            p.participant.vars['message_step2_1'] = m_dict
                
    
    def send_messages_step2_2(self):
        for p in self.get_players():
            parterner_id_step2 = p.get_parternersid_step2()
            num_p = len(parterner_id_step2)
            m_dict = {1:"", 2:"", 3:"", 4:""} 
            my_answer = "My opinion on this issue is " + str(p.participant.vars['this_issue']) + ". "

            p1_id = parterner_id_step2[0]
            m_dict[p1_id] = my_answer + p.message_step2_2_1
            if num_p != 1:
                p2_id = parterner_id_step2[1]
                m_dict[p2_id] = my_answer + p.message_step2_2_2
                if num_p == 3:
                    p3_id = parterner_id_step2[2]
                    m_dict[p3_id] = my_answer + p.message_step2_2_3
            
            p.participant.vars['message_step2_2'] = m_dict

    def send_messages_step3(self):
        for p in self.get_players():
            parterner_id_step3 = p.get_parternersid_step3()
            m_dict = {1:"", 2:"", 3:"", 4:""}
            my_answer = "My opinion on this issue is " + str(p.participant.vars['this_issue']) + ". "
            
            p1_id = parterner_id_step3[0]
            p2_id = parterner_id_step3[1]
            p3_id = parterner_id_step3[2]
            m_dict[p1_id] = my_answer + p.message_step3_1
            m_dict[p2_id] = my_answer + p.message_step3_2
            m_dict[p3_id] = my_answer + p.message_step3_3
            p.participant.vars['message_step3'] = m_dict

    def do_payoff(self):
        num_on = 0
        players = self.get_players()
        for p in players:
            answer = p.participant.vars['meeting']
            if answer == "ON":
                num_on = num_on +1
        
        reward_rule = {0:[7,4], 1:[11,8], 2:[15,12], 3:[19,16]}

        for p in self.get_players():
            if p.participant.vars['meeting'] == "OFF":
                result = reward_rule[num_on]
                reward_meeting = result[0]
            else:
                result = reward_rule[num_on-1]
                reward_meeting = result[1]

            my_keep = 20 - p.participant.vars['give_money']
            p_id = 5-p.id_in_group
            par = players[p_id-1]
            p_give = par.participant.vars['give_money']
            if my_keep+p_give == 20:
                if random.randint(0,1) == 1:
                    reward_20MUs = my_keep
                else:
                    reward_20MUs = p_give
            else:
                if my_keep+p_give > 20:
                    reward_20MUs = my_keep
                else:
                    reward_20MUs = p_give

            p.payoff = reward_meeting + reward_20MUs
            
            num_timeout = p.participant.vars['num_timeout']
            if num_timeout > 5:
                if num_timeout < 11:
                    p.payoff = p.payoff*0.9
                else:
                    p.payoff = p.payoff*0.8
       

class Player(BasePlayer):

    def get_parternersid_step1(self):
        my_parterner = Constants.match_step1[self.id_in_group]
        return my_parterner

    def get_parternersid_step2(self):
        round_issues = Constants.match_step2[self.round_number]
        my_parterner = round_issues[self.id_in_group]
        return my_parterner

    def get_parternersid_step3(self):
        my_parterner = Constants.match_step3[self.id_in_group]
        return my_parterner

    def comp_survey2(self, step):
        if step == 1:
            my_parterner_id = self.get_parternersid_step1()
        if step == 2:
            my_parterner_id = self.get_parternersid_step2()
        if step == 3:
            my_parterner_id = self.get_parternersid_step3()
        players = self.group.get_players()
        my_answer = self.participant.vars['survey2_answers']
        different_answers = []
        for p_id in my_parterner_id:
            p = players[p_id-1]
            other_answers = p.participant.vars['survey2_answers']
            different_answer = [x for x in other_answers if x not in my_answer]
            different_answers.append(different_answer)
        return different_answers

    def get_survey3_6_diff(self,step):
        if step == 1:
            my_parterner_id = self.get_parternersid_step1()
        if step == 2:
            my_parterner_id = self.get_parternersid_step2()
        if step == 3:
            my_parterner_id = self.get_parternersid_step3()
        players = self.group.get_players()
        # ps_answers = []
        my_answer = self.participant.vars['surver3-6_answers']
        my_answer_7 = self.participant.vars['give_money']
        diff_answers_all = []
        for p_id in my_parterner_id:
            diff_answers = []
            p = players[p_id-1]
            p_answers = p.participant.vars['surver3-6_answers']
            p_answer_7 = p.participant.vars['give_money']
            n = 0
            for a in p_answers:
                m_ans = my_answer[n]
                if a != m_ans:
                    if n == 0:
                        diff_answers.append("Favorite sport to watch: "+ str.upper(a))
                    if n == 1:
                        diff_answers.append("This characteristics suits this person the best: "+ str.upper(a))
                    if n == 2:
                        diff_answers.append("This person had the camera and microphone: "+ str.upper(a))
                    if n == 3:
                        diff_answers.append("This person sent this message to another peroson: "+a)
                n = n+1
            answer_s7 = "This person kept MORE for him- or herself than you did in the task when you had to share 20 Monetary Units (MUs)."
            if p_answer_7 > my_answer_7:
                diff_answers.append(answer_s7)

            answer_s8 = "You had to wait, which was possibly very annoying. You and also other participants had to wait because this person was slower in completing the survey"
            diff_answers.append(answer_s8)

            diff_answers_all.append(diff_answers)
        return diff_answers_all

    def get_all_answers(self, step):
        players = self.group.get_players()
        p_answers = []
        if step == 2:
            my_parterners = self.get_parternersid_step2()
        else:
            my_parterners = self.get_parternersid_step3()
        for p_id in my_parterners:
            p = players[p_id-1]
            p_answers.append(p.participant.vars['last_this_issue'])

        my_answer = self.participant.vars['this_issue']

        return [my_answer, p_answers]

    def get_p_names(self, my_parterners_id):
        players = self.group.get_players()
        p_names = []
        for p_id in my_parterners_id:
            p = players[p_id-1]
            p_names.append(p.participant.vars['name'])
        return p_names

    def get_likability(self, my_parterners_id):
        likability = []
        last_likability = self.participant.vars['likability']
        for p_id in my_parterners_id:
            likability.append(last_likability[p_id])
        return likability
   
    def likability():
        return models.IntegerField(
            label="Please rate how likeable you find this person from -50 (not likable at all) to +50 (very much likable). A zero rating could be interpreted as a neutral position.",
            min=-50, 
            max=50
            )
    
    likability_step1_1 = likability()
    likability_step1_2 = likability()
    likability_step2_1_1 = likability()
    likability_step2_1_2 = likability()
    likability_step2_1_3 = likability()
    likability_step2_2_1 = likability()
    likability_step2_2_2 = likability()
    likability_step2_2_3 = likability()
    likability_step2_3_1 = likability()
    likability_step2_3_2 = likability()
    likability_step2_3_3 = likability()
    likability_step3_1_1 = likability()
    likability_step3_1_2 = likability()
    likability_step3_1_3 = likability()
    likability_step3_2_1 = likability()
    likability_step3_2_2 = likability()
    likability_step3_2_3 = likability()

    def re_issue_field():
        return models.IntegerField(
            min=0,
            max=100
        )
    
    re_issue_step2_1 = re_issue_field()
    re_issue_step2_2 = re_issue_field()
    re_issue_step2_3 = re_issue_field()
    re_issue_step3_1 = re_issue_field()
    re_issue_step3_2 = re_issue_field()

    def message():
        return models.StringField(
            choices=["You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine.",
                "I would appreciate it if you could move your opinion closer to mine", "I would be happy if you could move your opinion closer to mine.","Why don’t you move your opinion closer to mine?"],
            widget=widgets.RadioSelect
        )
    
    message_step2_1_1 = message()
    message_step2_1_2 = message()
    message_step2_1_3 = message()
    message_step2_2_1 = message()
    message_step2_2_2 = message()
    message_step2_2_3 = message()
    message_step3_1 = message()
    message_step3_2 = message()
    message_step3_3 = message()
