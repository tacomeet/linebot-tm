from linebot.models import TextSendMessage

import message as ms
import line
import slack


def self_ref_exp(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()
    if ss_stage == 3:
        if text in ['Yes', 'No']:
            slack.send_msg_to_other_thread(user)
            user.reset_answer_msg()
        if text == 'Yes':
            user.set_session_stage(5)
            line.reply_msg(line_bot_api, event, ms.self_ref.EXP_3_YES)
            user.set_question_msg(ms.self_ref.EXP_3_YES)
        elif text == 'No':
            user.set_session_stage(4)
            line.reply_msg(line_bot_api, event, ms.self_ref.EXP_3_NO)
            user.set_question_msg(ms.self_ref.EXP_3_NO)
    elif ss_stage == 11:
        if text in ['Yes', 'No']:
            slack.send_msg_to_other_thread(user)
            user.reset()
    elif text == ms.default.KEY_NEXT:
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
        msg = _route_next(user)
        if msg:
            line.reply_msg(line_bot_api, event, msg)


def _route_next(user):
    ss_stage = user.get_session_stage()
    msg = None
    if ss_stage == 2:
        msg = ms.self_ref.EXP_2
    elif ss_stage == 4:
        msg = ms.self_ref.EXP_4
    elif ss_stage == 5:
        msg = ms.self_ref.EXP_5
    elif ss_stage == 6:
        msg = ms.self_ref.EXP_6
    elif ss_stage == 7:
        msg = ms.self_ref.EXP_7
    elif ss_stage == 8:
        msg = ms.self_ref.EXP_8
    elif ss_stage == 9:
        msg = ms.self_ref.EXP_9
    elif ss_stage == 10:
        msg = ms.default.PERMISSION_FOR_FEEDBACK
    user.set_question_msg(msg)
    user.increment_session_stage()
    return msg
