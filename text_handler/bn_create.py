import line
from models import User
from models.status_type import StatusType
import message as ms
import slack


def bn_create(line_bot_api, user, event):
    ss_type = user.get_session_type()
    user.set_answer_msg(event.message.text)

    if ss_type == StatusType.BN_CREATE:
        _bn_create(line_bot_api, user, event)
    else:
        bn_create_track(line_bot_api, user, event)


def _bn_create(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()

    if text == ms.default.KEY_NEXT:
        user.increment_session_stage()
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
        if ss_stage == 2:
            line.reply_msg(line_bot_api, event, ms.bn_create.M_2)
            user.set_question_msg(ms.bn_create.M_2)
        elif ss_stage == 3:
            line.reply_msg(line_bot_api, event, ms.bn_create.M_3)
            user.set_question_msg(ms.bn_create.M_3)
    elif text in (ms.bn_create.M_3_1, ms.bn_create.M_3_2, ms.bn_create.M_3_3, ms.bn_create.M_3_5):
        user.set_session_stage(1)
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
        if text == ms.bn_create.M_3_1:
            user.set_session_type(StatusType.BN_CREATE_TRACK1)
        elif text == ms.bn_create.M_3_2:
            user.set_session_type(StatusType.BN_CREATE_TRACK2)
        elif text == ms.bn_create.M_3_3:
            user.set_session_type(StatusType.BN_CREATE_TRACK3)
        elif text == ms.bn_create.M_3_5:
            user.set_session_type(StatusType.BN_CREATE_TRACK5)
        msg = _get_msg(user)
        line.reply_msg(line_bot_api, event, msg)
        user.set_question_msg(msg)


def bn_create_track(line_bot_api, user, event):
    text = event.message.text
    if text == ms.default.KEY_NEXT:
        user.increment_session_stage()
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
        msg = _get_msg(user)
        line.reply_msg(line_bot_api, event, msg)
        user.set_question_msg(msg)


def _get_msg(user: User):
    ss_stage = user.get_session_stage()
    ss_type = user.get_session_type()

    bn_dict = ms.bn_create.type_dict[ss_type]
    if ss_stage in bn_dict:
        if bn_dict[ss_stage] == ms.default.END:
            user.reset_answer_msg()
            user.set_question_msg(ms.default.END)
            slack.send_msg_to_other_thread(user)
            user.reset()
        return bn_dict[ss_stage]
