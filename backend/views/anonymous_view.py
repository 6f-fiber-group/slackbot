import os
from slack import WebClient
from slack.errors import SlackApiError
from flask import make_response

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def before_anonymous(tmpl: dict, channel_id: str):
  try:
    res = slack_client.chat_postMessage(
      channel = channel_id,
      attachments = tmpl["attachments"],
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def do_anonymous(tmpl: dict, trigger_id: str):
  try:
    res = slack_client.views_open(
      trigger_id = trigger_id,
      view = tmpl["view"],
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def not_do_anonymous(tmpl: dict, channel_id: str):
  try:
    res = slack_client.chat_postMessage(
      channel = channel_id,
      text = tmpl["text"],
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def anonymous_post(tmpl: dict):
  try:
    res = slack_client.chat_postMessage(
      channel = tmpl["channel_id"],
      text = tmpl["text"]
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def anonymous_post_response(tmpl: dict, user_id: str):
  try:
    res = slack_client.chat_postMessage(
      channel = user_id,
      text = tmpl["text"]
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def anonymous_form(tmpl: dict, view_id: str, view_hash: str):
  try:
    res = slack_client.views_update(
      view_id = view_id,
      hash = view_hash,
      view = tmpl["view"]
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def ask_for_questionnaire(tmpl: dict, user_id: str):
  try:
    res = slack_client.chat_postMessage(
      channel = user_id,
      attachments = tmpl["attachments"]
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def do_anonymous_questionnaire(tmpl: dict, trigger_id: str):
  try:
    res = slack_client.views_open(
      view = tmpl["view"],
      trigger_id = trigger_id
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def not_do_anonymous_questionnaire(tmpl: dict, user_id: str):
  try:
    res = slack_client.chat_postMessage(
      channel = user_id,
      text = tmpl["text"]
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)

def after_submit_anonymous_questionnaire(tmpl: dict, user_id: str):
  try:
    res = slack_client.chat_postMessage(
      channel = user_id,
      text = tmpl["text"]
    )
    return make_response("", res.status_code)
  except SlackApiError as e:
    return make_response(str(e.response), 200)