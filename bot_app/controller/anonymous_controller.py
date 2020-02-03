import os
import json
from urllib.parse import parse_qs
from slack import WebClient
from flask import Blueprint, request, make_response, current_app

from ..utils import \
  get_user_joined_channels,\
  get_channel_name_by_id,\
  get_users_in_channel

from .questionnaire_controller import\
  ask_for_questionnaire

bp = Blueprint('anonymous', __name__, url_prefix='/anonymous')

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

anonymous_post_info = {
  "channel_id": "",
  "text": "",
  "user_id": ""
}

@bp.route("/", methods=["POST"])
def slash_anonymous():
  req = parse_qs(request.get_data(as_text=True))

  with open("bot_app/template/payloads/anonymous_befeore_entering_msg.json", "r") as f:
    res = json.load(f)
    res["channel"] = res["channel"].format(req["user_id"][0])

  slack_client.chat_postMessage(
    channel = res["channel"],
    attachments = res["attachments"],
  )

  return make_response("", 200)

def anonymous_post(req):
  action_val = req["actions"][0]["value"]

  if action_val == "do_annoymous_post":
    with open("bot_app/template/payloads/anonymous_hide.json", "r") as f:
      res = json.load(f)
      res["trigger_id"] = res["trigger_id"].format(req["trigger_id"])

    res = set_params_for_anonymous_post(res, req["user"]["id"])

    res = slack_client.views_open(
      view=res["view"],
      trigger_id=res["trigger_id"]
    )

  if action_val == "not_do_annoymous_post":
    slack_client.chat_postMessage(
      channel = req["user"]["id"],
      text = "Bye! :wave:"
    )

  return make_response("", 200)

def set_params_for_anonymous_post(res, user_id):
  for idx, block in enumerate(res["view"]["blocks"]):

    if "block_id" in block:

      # set the option of select channels fields
      # only cahnnels which user joined will be set in options
      if block["block_id"] == "select_channel":
        channels = get_user_joined_channels(slack_client, user_id)
        for channel in channels:
          res["view"]["blocks"][idx]["accessory"]["options"].append({
              "text": {
                "type": "plain_text",
                "text": channel["name"],
                "emoji": True
              },
              "value": channel["id"]
            })

      # set the text of compliance members fields
      # only members who joined in cmpliance channel
      if block["block_id"] == "compliance_members":
        members = get_users_in_channel(slack_client, current_app.config["COMPLIANCE_CHANNEL_ID"])
        for member in members:
          if member["id"] != current_app.config["FIBERSLACKBOT_USER_ID"]:
            res["view"]["blocks"][idx]["text"]["text"] += "%s\n"%(member["name"])

  return res

def update_anonymous_post_info(req):
  if req["type"] == "view_submission":
    anonymous_post_info["text"] = req["view"]["state"]["values"]["content_block"]["content_action"]["value"]
    anonymous_post_info["user_id"] = req["user"]["id"]
  
  elif req["type"] == "block_actions":
    anonymous_post_info["channel_id"] = req["actions"][0]["selected_option"]["value"]
    anonymous_post_info["user_id"] = req["user"]["id"]

  elif  req["type"] == "initialize":
    anonymous_post_info["channel_id"] = ""
    anonymous_post_info["text"] = ""
    anonymous_post_info["user_id"] = ""

  return make_response("update anonymous post info", 200)

def after_submit_anonymous_post(req):
  slack_client.chat_postMessage(
    channel = anonymous_post_info["channel_id"],
    text = anonymous_post_info["text"]
  )

  channel_name = get_channel_name_by_id(slack_client, anonymous_post_info["channel_id"])
  slack_client.chat_postMessage(
    channel = anonymous_post_info["user_id"],
    text = "Successfully posted to <#%s|%s>!"%(anonymous_post_info["channel_id"], channel_name)
  )

  update_anonymous_post_info({"type": "initialize"})

  ask_for_questionnaire(req)

  return make_response("", 200)

def form_display(req):
  user_id = req["user"]["id"]
  display = req["actions"][0]["value"]

  file_name = "anonymous_show.json" if display == "show_form" else "anonymous_hide.json"
  with open("bot_app/template/payloads/%s"%file_name, "r") as f:
    res = json.load(f)

  res = set_params_for_anonymous_post(res, user_id)
  slack_client.views_update(
    view_id = req["view"]["id"],
    hash = req["view"]["hash"],
    view = res["view"]
  )

  return make_response("", 200)

