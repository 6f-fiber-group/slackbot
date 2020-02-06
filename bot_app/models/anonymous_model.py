import json
import copy
from flask import current_app

from ..utils import \
  get_user_joined_channels,\
  get_channel_name_by_id,\
  get_users_in_channel

anonymous_post_info = {
  "channel_id": "",
  "text": "",
  "user_id": ""
}

def before_anonymous() -> dict:
  with open("bot_app/template/payloads/anonymous_befeore_entering_msg.json", "r") as f:
    tmpl = json.load(f)
  return tmpl

def do_anonymous(user_id: str) -> dict:
  with open("bot_app/template/payloads/anonymous_hide.json", "r") as f:
    tmpl = json.load(f)
  tmpl_set_params = set_params_for_anonymous_post(tmpl, user_id)
  return tmpl_set_params

def not_do_anonymous() -> dict:
  return {"text": "Bye! :wave:"}

def anonymous_post() -> dict:
  return anonymous_post_info

def anonymous_post_response() -> dict:
  channel_name = get_channel_name_by_id(anonymous_post_info["channel_id"])

  tmpl = copy.deepcopy(anonymous_post_info)
  tmpl["text"] = "Successfully posted to <#%s|%s>!"%(anonymous_post_info["channel_id"], channel_name)
  return tmpl

def ask_for_questionnaire() -> dict:
  with open("bot_app/template/payloads/anoymous_post_response.json", "r") as f:
    tmpl = json.load(f)
  return tmpl

def anonymous_form(user_id: str, display: str) -> dict:
  file_name = "anonymous_show.json" if display == "show_form" else "anonymous_hide.json"
  with open("bot_app/template/payloads/%s"%file_name, "r") as f:
    tmpl = json.load(f)
  tmpl_set_params = set_params_for_anonymous_post(tmpl, user_id)
  return tmpl_set_params

def do_anonymous_questionnaire():
  with open("bot_app/template/payloads/anonymous_questionnaire.json", "r") as f:
    tmpl = json.load(f)
  return tmpl

def not_do_anonymous_questionnaire():
  return {"text": "Have a nice day! :wave:"}

def after_submit_anonymous_questionnaire():
  return {"text": "Thank you! :smile:"}


def set_params_for_anonymous_post(tmpl: dict, user_id: str) -> dict:
  for idx, block in enumerate(tmpl["view"]["blocks"]):

    if "block_id" in block:

      # set the option of select channels fields
      # only cahnnels which user joined will be set in options
      if block["block_id"] == "select_channel":
        channels = get_user_joined_channels(user_id)
        for channel in channels:
          tmpl["view"]["blocks"][idx]["accessory"]["options"].append({
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
        members = get_users_in_channel(current_app.config["COMPLIANCE_CHANNEL_ID"])
        for member in members:
          if member["id"] != current_app.config["FIBERSLACKBOT_USER_ID"]:
            tmpl["view"]["blocks"][idx]["text"]["text"] += "%s\n"%(member["name"])
  
  return tmpl

def update_anonymous_post_info(act_type: str = "", channel_id: str = "" ,user_id: str = "", text: str = ""):
  if act_type == "view_submission":
    anonymous_post_info["text"] = text
    anonymous_post_info["user_id"] = user_id
  
  elif act_type == "block_actions":
    anonymous_post_info["channel_id"] = channel_id
    anonymous_post_info["user_id"] = user_id

  elif act_type == "initialize":
    anonymous_post_info["channel_id"] = ""
    anonymous_post_info["text"] = ""
    anonymous_post_info["user_id"] = ""

  return act_type