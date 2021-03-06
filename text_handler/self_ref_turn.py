from linebot.models import TextSendMessage

import message as ms
import line
import slack


def self_ref_turn(line_bot_api, user, event):
    text = event.message.text
    if text == ms.default.KEY_NEXT:
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
        msg = _route_next(user)
        if msg:
            line.reply_msg(line_bot_api, event, msg)


def _route_next(user):
    ss_stage = user.get_session_stage()
    msg = None
    if ss_stage == 2:
        msg = ms.self_ref.TURN_2
    if ss_stage == 3:
        msg = ms.self_ref.TURN_3
    elif ss_stage == 4:
        msg = ms.self_ref.TURN_4
    elif ss_stage == 5:
        msg = ms.self_ref.TURN_5
    elif ss_stage == 6:
        msg = ms.self_ref.TURN_6
    if msg:
        user.set_question_msg(msg)
        user.increment_session_stage()
        return msg
    if ss_stage == 7:
        user.reset_answer_msg()
        user.set_question_msg(ms.default.PERMISSION_FOR_FEEDBACK)
        slack.send_msg_to_other_thread(user)
        user.reset()
        return ms.default.PERMISSION_FOR_FEEDBACK
