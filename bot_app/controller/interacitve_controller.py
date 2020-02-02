import os
import json
from slack import WebClient
from flask import Blueprint, request, make_response
import pprint
from .anonymous_controller import\
  anonymous_post,\
  update_anonymous_post_info,\
  submit_anonymous_post,\
  form_display

bp = Blueprint('interactive-events', __name__, url_prefix='/interactive-events')

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

@bp.route("/", methods=["POST"])
def even_worker():
  req = json.loads(request.form["payload"])
  pprint.pprint(req)

  if req["type"] == "interactive_message":
    if req["callback_id"] == "anonymous_befeore_entering_msg":
      return anonymous_post(req)

  elif req["type"] == "block_actions":
    block_id = req["actions"][0]["block_id"]
    if block_id == "select_channel":
      res = update_anonymous_post_info(
        channel_id = req["actions"][0]["selected_option"]["value"],
        user_id = req["user"]["id"]
      )
      return res
    
    elif block_id == "form_display":
      return form_display(
        view_id = req["view"]["id"],
        view_hash = req["view"]["hash"],
        user_id = req["user"]["id"],
        display = req["actions"][0]["value"]
      )

  elif req["type"] == "view_submission":
    res = update_anonymous_post_info(
      text = req["view"]["state"]["values"]["content_block"]["content_action"]["value"],
      user_id = req["user"]["id"]
    )
    return submit_anonymous_post()

  else:
    return make_response("no function defiend", 500)
