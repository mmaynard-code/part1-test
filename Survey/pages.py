from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Survey1_1(Page):
    form_model = 'player'
    form_fields = ['survey_1_1a', 'survey_1_1b', 'survey_1_1c']
    timeout_seconds = 90
    timeout_submission = {'survey_1_1a': 50}

    def before_next_page(self):
        self.player.participant.vars['num_timeout'] = 0
        self.player.participant.vars['is_dropout'] = False
        self.player.participant.vars['check_dropout'] = False
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class Survey1_2(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_1_2a = 50

    form_model = 'player'
    form_fields = ['survey_1_2a', 'survey_1_2b', 'survey_1_2c']
    timeout_seconds = 90

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_1_2a = 50

class Survey1_3(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_1_3a = 50

    form_model = 'player'
    form_fields = ['survey_1_3a', 'survey_1_3b', 'survey_1_3c']
    timeout_seconds = 90

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_1_3a = 50

class Survey1_4(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_1_4a = 50

    form_model = 'player'
    form_fields = ['survey_1_4a', 'survey_1_4b', 'survey_1_4c']
    timeout_seconds = 90

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_1_4a = 50

class Survey1_5(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_1_5a = 50

    form_model = 'player'
    form_fields = ['survey_1_5a', 'survey_1_5b', 'survey_1_5c']
    timeout_seconds = 90

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_1_5a = 50   

class Survey2(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            choice1 = ["A. Problems around integration are mostly the fault of immigrants.", 
            "B. Problems around integration are mostly the fault of society."]
            choice2 = ["A. We have to limit the influence of Islam in the world.", 
            "B. We have to allow the free spreading of the influence of Islam in the world."]
            choice3 = ["A. The expression of your religion, such as wearing a headcover or burkah, is not appropriate in the public domain, just in the private domain.",
            "B. Everyone should be free to express their own religion through their clothing in the public domain."]
            choice4 = ["A. The regulations of the government of my country concerning the spread of COVID-19 were not strict enough.", 
            "B. The regulations of the government of my country concerning the spread of COVID-19 were too strict."]
            choice5 = ["A. It is perfectly appropriate to use books, notes, and online help for an exam that is taking place online.", 
            "B. One should not use any help from books, notes, or from the Internet for an exam that is taking place online."]
            self.player.survey_2_1 = random.choice(choice1)
            self.player.survey_2_2 = random.choice(choice2)
            self.player.survey_2_3 = random.choice(choice3)
            self.player.survey_2_4 = random.choice(choice4)
            self.player.survey_2_5 = random.choice(choice5)

    form_model = 'player'
    form_fields = ['survey_2_1', 'survey_2_2', 'survey_2_3', 'survey_2_4','survey_2_5']
    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            choice1 = ["A. Problems around integration are mostly the fault of immigrants.", 
            "B. Problems around integration are mostly the fault of society."]
            choice2 = ["A. We have to limit the influence of Islam in the world.", 
            "B. We have to allow the free spreading of the influence of Islam in the world."]
            choice3 = ["A. The expression of your religion, such as wearing a headcover or burkah, is not appropriate in the public domain, just in the private domain.",
            "B. Everyone should be free to express their own religion through their clothing in the public domain."]
            choice4 = ["A. The regulations of the government of my country concerning the spread of COVID-19 were not strict enough.", 
            "B. The regulations of the government of my country concerning the spread of COVID-19 were too strict."]
            choice5 = ["A. It is perfectly appropriate to use books, notes, and online help for an exam that is taking place online.", 
            "B. One should not use any help from books, notes, or from the Internet for an exam that is taking place online."]
            self.player.survey_2_1 = random.choice(choice1)
            self.player.survey_2_2 = random.choice(choice2)
            self.player.survey_2_3 = random.choice(choice3)
            self.player.survey_2_4 = random.choice(choice4)
            self.player.survey_2_5 = random.choice(choice5)

class Survey3(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            choices = ["E-sport", "Soccer (football)", "Car racing", "Figure skating", "Curling", "Darts", "I hate watching sports."]
            self.player.survey_3 = random.choice(choices)

    form_model = 'player'
    form_fields = ['survey_3']
    timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            choices = ["E-sport", "Soccer (football)", "Car racing", "Figure skating", "Curling", "Darts", "I hate watching sports."]
            self.player.survey_3 = random.choice(choices)


class Survey4(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            choices = ["Critical, quarrelsome", "Anxious, Easily upset", "Disorganized, careless", "Conventional, uncreative"]
            self.player.survey_4 = random.choice(choices)

    form_model = 'player'
    form_fields = ['survey_4']

    timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            choices = ["Critical, quarrelsome", "Anxious, Easily upset", "Disorganized, careless", "Conventional, uncreative"]
            self.player.survey_4 = random.choice(choices)

class Survey5(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_5 = "ON"

    form_model = 'player'
    form_fields = ['survey_5']
    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_5 = "ON"


class Survey6(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_6 = "B. I will do my best in this experiment to get the most for me, I do not care what you are going to receive."

    form_model = 'player'
    form_fields = ['survey_6']
    timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_6 = "B. I will do my best in this experiment to get the most for me, I do not care what you are going to receive."

class Survey7(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            self.player.survey_7 = 0

    form_model = 'player'
    form_fields = ['survey_7']
    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            self.player.survey_7 = 0

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'save_answers'
    body_text = "Another participant is making their decisions slower than you. You have to wait because they have not yet finished the previous task. You can only proceed after they finish the previous task. You are not allowed to do anything else; just wait until they are finished."

class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1 
    
    timeout_seconds = 90

class Dropout_check(Page):
    def is_displayed(self):
        if self.player.participant.vars["is_dropout"] < 4:
            return self.player.participant.vars["check_dropout"] 
        else:
            return False
    
    timeout_seconds = 30

    def vars_for_template(self):
        num_d = self.player.participant.vars["is_dropout"]
        return dict(
            num_d = num_d
        )

    def before_next_page(self):
        self.player.participant.vars["check_dropout"] = False
        if self.timeout_happened:
            prenum_dropout = self.player.participant.vars["is_dropout"]
            self.player.participant.vars["is_dropout"] = prenum_dropout + 1


page_sequence = [Welcome, Survey1_1, Dropout_check, 
    Survey1_2, Dropout_check, Survey1_3, Dropout_check, Survey1_4, 
    Dropout_check, Survey1_5, Dropout_check, Survey2, Dropout_check, Survey3, 
    Dropout_check, Survey4, Dropout_check, Survey5, Dropout_check, Survey6, 
    Dropout_check, Survey7, Dropout_check, ResultsWaitPage]
