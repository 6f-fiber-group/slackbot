import os
import json
from slack import WebClient
from flask import Blueprint, request, make_response

from .anonymous_controller import\
  anonymous_post,\
  update_anonymous_post_info,\
  after_submit_anonymous_post,\
  form_display
from .questionnaire_controller import\
  anonymous_questionnaire,\
  after_submit_anonymous_questionnaire


bp = Blueprint('interactive-events', __name__, url_prefix='/interactive-events')

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

@bp.route("/", methods=["POST"])
def event_worker():
  req = json.loads(request.form["payload"])

  if req["type"] == "interactive_message":

    if req["callback_id"] == "anonymous_befeore_entering_msg":
      return anonymous_post(req)

    elif req["callback_id"] == "anonymous_questionnaire":
      return anonymous_questionnaire(req)

  elif req["type"] == "block_actions":
    block_id = req["actions"][0]["block_id"]

    if block_id == "select_channel":
      return update_anonymous_post_info(req)
    
    elif block_id == "form_display":
      return form_display(req)

  elif req["type"] == "view_submission":

    if req["view"]["callback_id"] == "anonymous":
      update_anonymous_post_info(req)
      return after_submit_anonymous_post(req)

    if req["view"]["callback_id"] == "anonymous_questionnaire":
      return after_submit_anonymous_questionnaire(req)

  else:
    return make_response("no function defiend", 500)
