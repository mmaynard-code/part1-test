from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MatchingWaitPage(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.do_my_shuffle()

class Step1(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        
    timeout_seconds = 50
    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step1()
        if len(my_parterners_id) == 1:
            return ['likability_step1_1']
        else:
            return ['likability_step1_1','likability_step1_2']

    def vars_for_template(self):
        my_parterners_id = self.player.get_parternersid_step1()
        num_p = len(my_parterners_id)
        diff_answers_s2 = self.player.comp_survey2(1)
        diff_answers_s3_6 = self.player.get_survey3_6_diff(1)
        p_names = self.player.get_p_names(my_parterners_id)

        vars_dict = dict(
                my_id = self.player.id_in_group,
                num_p = num_p,
                p1_diff_answers_s2 = diff_answers_s2[0],
                l_p1_diff_answers_s2 = len(diff_answers_s2[0]),
                p1_diff_answers_s3_6 = diff_answers_s3_6[0],
                l_p1_diff_answers_s3_6 = len(diff_answers_s3_6[0]),
                p1_name = p_names[0]
                )
        
        if num_p != 1:
            vars_2p = dict(
                p2_diff_answers_s2 = diff_answers_s2[1],
                l_p2_diff_answers_s2 = len(diff_answers_s2[1]),
                p2_diff_answers_s3_6 = diff_answers_s3_6[1],
                l_p2_diff_answers_s3_6 = len(diff_answers_s3_6[1]),
                p2_name = p_names[1]
                )
            vars_dict.update(vars_2p)

        return vars_dict

    
    def before_next_page(self):
        my_parterners_id = self.player.get_parternersid_step1()
        num_p = len(my_parterners_id)
        p1 = my_parterners_id[0]
        self.player.participant.vars['likability'][p1] = self.player.likability_step1_1
        if num_p != 1:
            p2 = my_parterners_id[1]
            self.player.participant.vars['likability'][p2] = self.player.likability_step1_2
            if num_p == 3:
                p3 = my_parterners_id[2]
                self.player.participant.vars['likability'][p3] = self.player.likability_step1_3
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class Step2_1(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            all_answers = self.player.get_all_answers(2)
            my_answer = all_answers[0]
            self.player.re_issue_step2_1 = my_answer
    
    timeout_seconds = 50

    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step2()

        form_fields = ['re_issue_step2_1']

        form_list = ['likability_step2_1_1', 'likability_step2_1_2', 'likability_step2_1_3']
        if len(my_parterners_id) == 1:
            form_fields.append(form_list[0])
        else:
            if len(my_parterners_id) == 2:
                for f in form_list[0:2]:
                    form_fields.append(f)
            else:
                for f in form_list:
                    form_fields.append(f)
        
        return form_fields

    def vars_for_template(self):
        my_parterners_id_step1 = self.player.get_parternersid_step1()
        my_parterners_id_step2 = self.player.get_parternersid_step2()
        num_p = len(my_parterners_id_step2)
        same_p = []
        for p_id in my_parterners_id_step2:
            if p_id in my_parterners_id_step1:
                same_p.append("IS")
            else:
                same_p.append("IS NOT")
        
        all_answers = self.player.get_all_answers(2)
        my_answer = all_answers[0]
        p_answers = all_answers[1]

        p_names = self.player.get_p_names(my_parterners_id_step2)

        likability = self.player.get_likability(my_parterners_id_step2)

        vars_dict = dict(
            my_answer = my_answer,
            num_p = num_p,
            same_p1 = same_p[0],
            p1_answer = p_answers[0],
            p1_name = p_names[0],
            issue = Constants.issues_list[self.round_number-1],
            like1 = likability[0]
            )
        
        if num_p != 1:
            vars_2p = dict(
                same_p2 = same_p[1],
                p2_answer = p_answers[1],
                p2_name = p_names[1],
                like2 = likability[1]
                )
            vars_dict.update(vars_2p)       
            if num_p == 3:
                vars_3p = dict(
                    same_p3 = same_p[2],
                    p3_answer = p_answers[2],
                    p3_name = p_names[2],
                    like3 = likability[2]
                    )
                vars_dict.update(vars_3p)
        
        return vars_dict

    def before_next_page(self):
        my_parterners_id = self.player.get_parternersid_step2()
        num_p = len(my_parterners_id)
        p1 = my_parterners_id[0]
        self.player.participant.vars['likability'][p1] = self.player.likability_step2_1_1
        if num_p != 1:
            p2 = my_parterners_id[1]
            self.player.participant.vars['likability'][p2] = self.player.likability_step2_1_2
            if num_p == 3:
                p3 = my_parterners_id[2]
                self.player.participant.vars['likability'][p3] = self.player.likability_step2_1_3
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class PreMessageWait_step2_1(WaitPage):
    def after_all_players_arrive(self):
        self.group.save_update_answer("2_1")

class Step2_2(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            message = "You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine."
            self.player.message_step2_1_1 = message
            self.player.message_step2_1_2 = message
            self.player.message_step2_1_3 = message

    timeout_seconds = 30

    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step2()
        form_list = ['message_step2_1_1', 'message_step2_1_2', 'message_step2_1_3']
        if len(my_parterners_id) == 1:
            return [form_list[0]]
        else:
            if len(my_parterners_id) == 2:
                return form_list[0:2]
            else:
                return form_list
    
    def vars_for_template(self):
        my_parterners_id = self.player.get_parternersid_step2()
        num_p = len(my_parterners_id)
        all_answers = self.player.get_all_answers(2)
        my_answer = all_answers[0]
        p_answers = all_answers[1]
        p_names = self.player.get_p_names(my_parterners_id)

        vars_dict = dict(
            my_answer = my_answer,
            p1_answer = p_answers[0],
            p1_name = p_names[0],
            num_p = num_p,
            issue = Constants.issues_list[self.round_number-1]
        )

        if num_p != 1:
            vars_2p = dict(
                p2_answer = p_answers[1],
                p2_name = p_names[1],
            )
            vars_dict.update(vars_2p)
            if num_p == 3:
                vars_3p = dict(
                    p3_answer = p_answers[2],
                    p3_name = p_names[2],
                )
                vars_dict.update(vars_3p)
        
        return vars_dict


    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            message = "You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine."
            self.player.message_step2_1_1 = message
            self.player.message_step2_1_2 = message
            self.player.message_step2_1_3 = message

class MessageWait_step2_1(WaitPage):
    after_all_players_arrive = 'send_messages_step2_1'

class Step2_3(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            all_answers = self.player.get_all_answers(2)
            my_answer = all_answers[0]
            self.player.re_issue_step2_2 = my_answer
    
    timeout_seconds = 50
    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step2()

        form_fields = ['re_issue_step2_2']

        form_list = ['likability_step2_2_1', 'likability_step2_2_2', 'likability_step2_2_3']
        if len(my_parterners_id) == 1:
            form_fields.append(form_list[0])
        else:
            if len(my_parterners_id) == 2:
                for f in form_list[0:2]:
                    form_fields.append(f)
            else:
                for f in form_list:
                    form_fields.append(f)
        
        return form_fields

    def vars_for_template(self):
        my_answer = self.player.participant.vars['this_issue']
        my_parterners_id = self.player.get_parternersid_step2()
        p_names = self.player.get_p_names(my_parterners_id)
        num_p = len(my_parterners_id)
        my_id = self.player.id_in_group
        m_list = []
        for p_id in my_parterners_id:
            p = self.group.get_players()[p_id-1]
            p_message = p.participant.vars['message_step2_1']
            message = p_message[my_id]
            m_list.append(message)

        likability = self.player.get_likability(my_parterners_id)

        vars_dict = dict(
            num_p = num_p,
            issue = Constants.issues_list[self.round_number-1],
            message_got1 = m_list[0],
            my_answer = my_answer,
            p1_name = p_names[0],
            like1 = likability[0]
        )
        if num_p != 1:
            vars_2p = dict(
                message_got2 = m_list[1],
                p2_name = p_names[1],
                like2 = likability[1]
            )
            vars_dict.update(vars_2p)
            if num_p == 3:
                vars_3p = dict(
                message_got3 = m_list[2],
                p3_name = p_names[2],
                like3 = likability[2]
                )
                vars_dict.update(vars_3p)
        
        return vars_dict

    def before_next_page(self):
        my_parterners_id = self.player.get_parternersid_step2()
        num_p = len(my_parterners_id)
        p1 = my_parterners_id[0]
        self.player.participant.vars['likability'][p1] = self.player.likability_step2_2_1
        if num_p != 1:
            p2 = my_parterners_id[1]
            self.player.participant.vars['likability'][p2] = self.player.likability_step2_2_2
            if num_p == 3:
                p3 = my_parterners_id[2]
                self.player.participant.vars['likability'][p3] = self.player.likability_step2_2_3
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class PreMessageWait_step2_2(WaitPage):
    def after_all_players_arrive(self):
        self.group.save_update_answer("2_2")

class Step2_4(Page):    
    timeout_seconds = 30

    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            message = "You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine."
            self.player.message_step2_2_1 = message
            self.player.message_step2_2_2 = message
            self.player.message_step2_2_3 = message

    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step2()
        form_list = ['message_step2_2_1', 'message_step2_2_2', 'message_step2_2_3']
        if len(my_parterners_id) == 1:
            return [form_list[0]]
        else:
            if len(my_parterners_id) == 2:
                return form_list[0:2]
            else:
                return form_list
    
    def vars_for_template(self):
        my_parterners_id = self.player.get_parternersid_step2()
        p_names = self.player.get_p_names(my_parterners_id)
        num_p = len(my_parterners_id)
        all_answers = self.player.get_all_answers(2)
        my_answer = all_answers[0]
        p_answers = all_answers[1]

        vars_dict = dict(
            my_answer = my_answer,
            p1_answer = p_answers[0],
            num_p = num_p,
            issue = Constants.issues_list[self.round_number-1],
            p1_name = p_names[0],
        )

        if num_p != 1:
            vars_2p = dict(
                p2_answer = p_answers[1],
                p2_name = p_names[1],
            )
            vars_dict.update(vars_2p)
            if num_p == 3:
                vars_3p = dict(
                    p3_answer = p_answers[2],
                    p3_name = p_names[2],
                )
                vars_dict.update(vars_3p)
        
        return vars_dict

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            message = "You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine."
            self.player.message_step2_2_1 = message
            self.player.message_step2_2_2 = message
            self.player.message_step2_2_3 = message

class MessageWait_step2_2(WaitPage):
    after_all_players_arrive = 'send_messages_step2_2'

class Step2_5(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            all_answers = self.player.get_all_answers(2)
            my_answer = all_answers[0]
            self.player.re_issue_step2_3 = my_answer
    
    timeout_seconds = 50
    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step2()

        form_fields = ['re_issue_step2_3']

        form_list = ['likability_step2_3_1', 'likability_step2_3_2', 'likability_step2_3_3']

        if len(my_parterners_id) == 1:
            form_fields.append(form_list[0])
        else:
            if len(my_parterners_id) == 2:
                for f in form_list[0:2]:
                    form_fields.append(f)
            else:
                for f in form_list:
                    form_fields.append(f)
        
        return form_fields

    def vars_for_template(self):
        my_answer = self.player.participant.vars['this_issue']
        my_parterners_id = self.player.get_parternersid_step2()
        p_names = self.player.get_p_names(my_parterners_id)
        num_p = len(my_parterners_id)
        my_id = self.player.id_in_group
        m_list = []
        for p_id in my_parterners_id:
            p = self.group.get_players()[p_id-1]
            p_message = p.participant.vars['message_step2_2']
            message = p_message[my_id]
            m_list.append(message)

        likability = self.player.get_likability(my_parterners_id)

        vars_dict = dict(
            num_p = num_p,
            issue = Constants.issues_list[self.round_number-1],
            message_got1 = m_list[0],
            p1_name = p_names[0],
            my_answer = my_answer,
            like1 = likability[0]
        )
        if num_p != 1:
            vars_2p = dict(
                message_got2 = m_list[1],
                p2_name = p_names[1],
                like2 = likability[1]
            )
            vars_dict.update(vars_2p)
            if num_p == 3:
                vars_3p = dict(
                message_got3 = m_list[2],
                p3_name = p_names[2],
                like3 = likability[2]
                )
                vars_dict.update(vars_3p)
        
        return vars_dict

    def before_next_page(self):
        my_parterners_id = self.player.get_parternersid_step2()
        num_p = len(my_parterners_id)
        p1 = my_parterners_id[0]
        self.player.participant.vars['likability'][p1] = self.player.likability_step2_3_1
        if num_p != 1:
            p2 = my_parterners_id[1]
            self.player.participant.vars['likability'][p2] = self.player.likability_step2_3_2
            if num_p == 3:
                p3 = my_parterners_id[2]
                self.player.participant.vars['likability'][p3] = self.player.likability_step2_3_3
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class PreMessageWait_step2_3(WaitPage):
    def after_all_players_arrive(self):
        self.group.save_update_answer("2_3")

class Step3_1(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            all_answers = self.player.get_all_answers(2)
            my_answer = all_answers[0]
            self.player.re_issue_step3_1 = my_answer

    timeout_seconds = 50
    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step3()

        form_fields = ['re_issue_step3_1']

        form_list = ['likability_step3_1_1', 'likability_step3_1_2', 'likability_step3_1_3']

        if len(my_parterners_id) == 1:
            form_fields.append(form_list[0])
        else:
            if len(my_parterners_id) == 2:
                for f in form_list[0:2]:
                    form_fields.append(f)
            else:
                for f in form_list:
                    form_fields.append(f)
        
        return form_fields

    def vars_for_template(self):
        my_parterners_id_step1 = self.player.get_parternersid_step1()
        my_parterners_id_step2 = self.player.get_parternersid_step2()
        my_parterners_id_step3 = self.player.get_parternersid_step3()
        p_names = self.player.get_p_names(my_parterners_id_step3)
        num_p = len(my_parterners_id_step3)
        same_p = []
        for p_id in my_parterners_id_step3:
            if p_id in my_parterners_id_step2:
                same_p.append("IS")
            else:
                same_p.append("IS NOT")
        all_answers = self.player.get_all_answers(3)
        my_answer = all_answers[0]
        p_answers = all_answers[1]

        likability = self.player.get_likability(my_parterners_id_step3)

        return dict(
            num_p = num_p,
            same_p1 = same_p[0],
            same_p2 = same_p[1],
            same_p3 = same_p[2],
            p1_answer = p_answers[0],
            p1_name = p_names[0],
            p2_answer = p_answers[1],
            p2_name = p_names[1],
            p3_answer = p_answers[2],
            p3_name = p_names[2],
            my_answer = my_answer,
            issue = Constants.issues_list[self.round_number-1],
            like1 = likability[0],
            like2 = likability[1],
            like3 = likability[2]
        )
    
    def before_next_page(self):
        my_parterners_id = self.player.get_parternersid_step3()
        num_p = len(my_parterners_id)
        p1 = my_parterners_id[0]
        self.player.participant.vars['likability'][p1] = self.player.likability_step3_1_1
        if num_p != 1:
            p2 = my_parterners_id[1]
            self.player.participant.vars['likability'][p2] = self.player.likability_step3_1_2
            if num_p == 3:
                p3 = my_parterners_id[2]
                self.player.participant.vars['likability'][p3] = self.player.likability_step3_1_3
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class PreMessageWait_step3(WaitPage):
    def after_all_players_arrive(self):
        self.group.save_update_answer("3")

class Step3_2(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            message = "You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine."
            self.player.message_step3_1 = message
            self.player.message_step3_2 = message
            self.player.message_step3_3 = message

    timeout_seconds = 30

    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step3()
        form_list = ['message_step3_1', 'message_step3_2', 'message_step3_3']
        if len(my_parterners_id) == 1:
            return [form_list[0]]
        else:
            if len(my_parterners_id) == 2:
                return form_list[0:2]
            else:
                return form_list
    
    def vars_for_template(self):
        my_parterners_id = self.player.get_parternersid_step3()
        p_names = self.player.get_p_names(my_parterners_id)
        num_p = len(my_parterners_id)
        all_answers = self.player.get_all_answers(3)
        my_answer = all_answers[0]
        p_answers = all_answers[1]

        vars_dict = dict(
            my_answer = my_answer,
            p1_answer = p_answers[0],
            p1_name = p_names[0],
            num_p = num_p,
            issue = Constants.issues_list[self.round_number-1]
        )

        if num_p != 1:
            vars_2p = dict(
                p2_answer = p_answers[1],
                p2_name = p_names[1]
            )
            vars_dict.update(vars_2p)
            if num_p == 3:
                vars_3p = dict(
                    p3_answer = p_answers[2],
                    p3_name = p_names[2]
                )
                vars_dict.update(vars_3p)
        
        return vars_dict

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1
            message = "You are completely wrong with your opinion. Your opinion is absolutely not realistic. Rethink your position and change your mind so that is closer to mine."
            self.player.message_step3_1 = message
            self.player.message_step3_2 = message
            self.player.message_step3_3 = message

class MessageWait_step3(WaitPage):
    after_all_players_arrive = 'send_messages_step3'

class Step3_3(Page):
    def is_displayed(self):
        if self.player.participant.vars['is_dropout'] < 4:
            return True
        else:
            all_answers = self.player.get_all_answers(2)
            my_answer = all_answers[0]
            self.player.re_issue_step3_2 = my_answer
    
    timeout_seconds = 50
    form_model = 'player'
    def get_form_fields(self):
        my_parterners_id = self.player.get_parternersid_step3()

        form_fields = ['re_issue_step3_2']

        form_fields.append('likability_step3_2_1')
        form_fields.append('likability_step3_2_2')
        form_fields.append('likability_step3_2_3')
        
        return form_fields

    def vars_for_template(self):
        my_parterners_id = self.player.get_parternersid_step3()
        p_names = self.player.get_p_names(my_parterners_id)
        num_p = 3
        my_id = self.player.id_in_group
        m_list = []
        for p_id in my_parterners_id:
            p = self.group.get_players()[p_id-1]
            p_message = p.participant.vars['message_step3']
            message = p_message[my_id]
            m_list.append(message)
        
        my_answer = self.participant.vars['this_issue']

        likability = self.player.get_likability(my_parterners_id)

        return dict(
            num_p = num_p,
            issue = Constants.issues_list[self.round_number-1],
            my_answer = my_answer,
            p1_name = p_names[0],
            p2_name = p_names[1],
            p3_name = p_names[2],
            message_got1 = m_list[0],
            message_got2 = m_list[1],
            message_got3 = m_list[2],
            like1 = likability[0],
            like2 = likability[1],
            like3 = likability[2]
        )

    def before_next_page(self):
        my_parterners_id = self.player.get_parternersid_step3()
        num_p = len(my_parterners_id)
        p1 = my_parterners_id[0]
        self.player.participant.vars['likability'][p1] = self.player.likability_step3_2_1
        if num_p != 1:
            p2 = my_parterners_id[1]
            self.player.participant.vars['likability'][p2] = self.player.likability_step3_2_2
            if num_p == 3:
                p3 = my_parterners_id[2]
                self.player.participant.vars['likability'][p3] = self.player.likability_step3_2_3
        if self.timeout_happened:
            self.player.participant.vars['check_dropout'] = True
            prenum_timeout = self.player.participant.vars['num_timeout']
            self.player.participant.vars['num_timeout'] = prenum_timeout + 1

class Do_payoff(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    after_all_players_arrive ='do_payoff'

class Payoff(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        return dict(
            my_payoff = self.player.payoff,
            drop_out = self.player.participant.vars["is_dropout"]
        )

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



page_sequence = [MatchingWaitPage, Step1, Dropout_check, Step2_1, Dropout_check, PreMessageWait_step2_1, Step2_2, 
    Dropout_check, MessageWait_step2_1, Step2_3, Dropout_check, PreMessageWait_step2_2, Step2_4, Dropout_check, 
    MessageWait_step2_2, Step2_5, Dropout_check, PreMessageWait_step2_3, Step3_1, Dropout_check, PreMessageWait_step3, Step3_2, 
    Dropout_check, MessageWait_step3, Step3_3, Do_payoff, Payoff]
#MatchingWaitPage, 