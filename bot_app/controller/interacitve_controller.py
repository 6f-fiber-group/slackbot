import os
import json
from slack import WebClient
from flask import Blueprint, request, make_response

from . import anonymous_controller as ac

bp = Blueprint('interactive-events', __name__, url_prefix='/interactive-events')

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

@bp.route("/", methods=["POST"])
def event_worker():
  req = json.loads(request.form["payload"])

  if req["type"] == "interactive_message":

    if req["callback_id"] == "anonymous_befeore_entering_msg":
      return ac.anonymous_post(req)

    elif req["callback_id"] == "anonymous_questionnaire":
      return ac.anonymous_questionnaire(req)

  elif req["type"] == "block_actions":
    block_id = req["actions"][0]["block_id"]

    if block_id == "select_channel":
      return ac.update_anonymous_post_info(req)
    
    elif block_id == "form_display":
      return ac.form_display(req)

  elif req["type"] == "view_submission":

    if req["view"]["callback_id"] == "anonymous":
      ac.update_anonymous_post_info(req)
      return ac.after_submit_anonymous_post(req)

    if req["view"]["callback_id"] == "anonymous_questionnaire":
      return ac.after_submit_anonymous_questionnaire(req)

  else:
    return ac.make_response("no function defiend", 200)
