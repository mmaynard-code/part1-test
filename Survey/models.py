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



author = 'Your name here'

doc = """
Survey
"""


class Constants(BaseConstants):
    name_in_url = 'Survey'
    players_per_group = None
    num_rounds = 1
    num_participants = 8




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def save_answers(self):
        for p in self.get_players():
            my_issues = p.get_my_issues()
            my_survey2 = p.get_my_survey2()
            my_survey3_6 = p.get_my_survey3_6()
            p.participant.vars['issues_answers'] = my_issues
            p.participant.vars['survey2_answers'] = my_survey2
            p.participant.vars['surver3-6_answers'] = my_survey3_6
            p.participant.vars['meeting'] = my_survey3_6[2]
            p.participant.vars['give_money'] = p.survey_7

    


class Player(BasePlayer):

    def make_field1():
        return  models.IntegerField(
            label="1. Please give your opinion on this issue", 
            min=0, 
            max=100, 
            initial=0
            )
 
    def make_field2():
        return models.IntegerField(
            label="2. Please tell us also how important this issue is for you",
            choices=[[1, "Very unimportant"], [2, "Unimportant"], [3, "Important"], [4, "Very important"]], 
            widget=widgets.RadioSelectHorizontal,
            )

    def make_field3():
        return models.IntegerField(
            label="3. Please tell us also how sure are you about your opinion",
            choices=[[1, "Very unsure"], [2, "Unsure"], [3, "Sure"], [4, "Very sure"]], 
            widget=widgets.RadioSelectHorizontal,
            )

    survey_1_1a = make_field1()
    survey_1_1b = make_field2()
    survey_1_1c = make_field3()

    survey_1_2a = make_field1()
    survey_1_2b = make_field2()
    survey_1_2c = make_field3()

    survey_1_3a = make_field1()
    survey_1_3b = make_field2()
    survey_1_3c = make_field3()

    survey_1_4a = make_field1()
    survey_1_4b = make_field2()
    survey_1_4c = make_field3()

    survey_1_5a = make_field1()
    survey_1_5b = make_field2()
    survey_1_5c = make_field3()

    def get_my_issues(self):
        issues_answers = [self.survey_1_1a, self.survey_1_2a, self.survey_1_3a,self.survey_1_4a,self.survey_1_5a]
        # issues_answers = [self.survey_1_1a, self.survey_1_2a]
        return issues_answers

    survey_2_1 = models.StringField(
        choices=["Problems around integration are mostly the fault of immigrants.", 
        "Problems around integration are mostly the fault of society."],
        widget=widgets.RadioSelect
    )

    survey_2_2 = models.StringField(
        choices=["We have to limit the influence of Islam in the world.", 
        "We have to allow the free spreading of the influence of Islam in the world."],
        widget=widgets.RadioSelect
    )

    survey_2_3 = models.StringField(
        choices=["The expression of your religion, such as wearing a headcover or burkah, is not appropriate in the public domain, just in the private domain.",
        "Everyone should be free to express their own religion through their clothing in the public domain."],
        widget=widgets.RadioSelect
    )

    survey_2_4 = models.StringField(
        choices=["The regulations of the government of my country concerning the spread of COVID-19 were not strict enough.", 
        "The regulations of the government of my country concerning the spread of COVID-19 were too strict."],
        widget=widgets.RadioSelect
    )

    survey_2_5 = models.StringField(
        choices=["It is perfectly appropriate to use books, notes, and online help for an exam that is taking place online.", 
        "One should not use any help from books, notes, or from the Internet for an exam that is taking place online."],
        widget=widgets.RadioSelect
    )

    def get_my_survey2(self):
        survey2_answers = [self.survey_2_1, self.survey_2_2,self.survey_2_3,self.survey_2_4,self.survey_2_5]
        return survey2_answers

    survey_3 = models.StringField(
        choices=["E-sport", "Soccer (football)", "Car racing", "Figure skating", "Curling", "Darts", "I hate watching sports."],
        widget=widgets.RadioSelect
    )

    survey_4 = models.StringField(
        choices=["Critical, quarrelsome", "Anxious, Easily upset", "Disorganized, careless", "Conventional, uncreative"],
        widget=widgets.RadioSelect
    )

    survey_5 = models.StringField(
        choices=["OFF", "ON"],
        widget=widgets.RadioSelect
    )

    survey_6 = models.StringField(
        choices=["I am kind and will help you in this experiment as much as I can",
        "I will do my best in this experiment to get the most for me, I do not care what you are going to receive."],
        widget=widgets.RadioSelect
    )

    def get_my_survey3_6(self):
        survey3_6_answers = [self.survey_3, self.survey_4, self.survey_5, self.survey_6]
        return survey3_6_answers

    survey_7 = models.CurrencyField(label="Your decision", min=0, max=20)

