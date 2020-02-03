import os
import json
from slack import WebClient
from flask import Blueprint, request, make_response, current_app

bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def ask_for_questionnaire(req):
  with open("bot_app/template/payloads/anoymous_post_response.json", "r") as f:
    attachments = json.load(f)

  slack_client.chat_postMessage(
    channel = req["user"]["id"],
    attachments = attachments
  )

  return make_response("", 200)


def anonymous_questionnaire(req):
  action_val = req["actions"][0]["value"]

  if action_val == "do_questionnaire":
    with open("bot_app/template/payloads/anonymous_questionnaire.json", "r") as f:
      view = json.load(f)

    slack_client.views_open(
      view = view,
      trigger_id = req["trigger_id"]
    )

  if action_val == "not_do_questionnaire":
    slack_client.chat_postMessage(
      channel = req["user"]["id"],
      text = "Have a nice day! :wave:"
    )

  return make_response("", 200)

def after_submit_anonymous_questionnaire(req):
  slack_client.chat_postMessage(
    channel = req["user"]["id"],
    text = "Thank you! :smile:"
  )
  return make_response("", 200)