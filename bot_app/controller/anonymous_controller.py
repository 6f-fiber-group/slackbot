import os
import json
from urllib.parse import parse_qs
from slack import WebClient
from flask import Blueprint, request, make_response

from ..views import anonymous_view as views
from ..models import anonymous_model as models

bp = Blueprint('anonymous', __name__, url_prefix='/anonymous')

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

@bp.route("/", methods=["POST"])
def slash_anonymous():
  req = parse_qs(request.get_data(as_text=True))
  tmpl = models.before_anonymous()
  return views.before_anonymous(tmpl, req["user_id"][0])

def anonymous_post(req):
  action_val = req["actions"][0]["value"]

  if action_val == "do_annoymous_post":
    tmpl = models.do_anonymous(req["user"]["id"])
    return views.do_anonymous(tmpl, req["trigger_id"])

  if action_val == "not_do_annoymous_post":
    tmpl = models.not_do_anonymous()
    return views.not_do_anonymous(tmpl, req["user"]["id"])

  return make_response("no action", 200)

def update_anonymous_post_info(req):
  models.update_anonymous_post_info(
    act_type = req["type"],
    channel_id = req["actions"][0]["selected_option"]["value"] if req["type"] == "block_actions" else "",
    user_id = req["user"]["id"],
    text = req["view"]["state"]["values"]["content_block"]["content_action"]["value"] if req["type"] == "view_submission" else ""
  )
  return make_response("update anonymous post info", 200)

def after_submit_anonymous_post(req):
  tmpl_1 = models.anonymous_post()
  views.anonymous_post(tmpl_1)

  tmpl_2 = models.anonymous_post_response()
  views.anonymous_post_response(tmpl_2, req["user"]["id"])

  models.update_anonymous_post_info("initialize")

  tmpl_3 = models.ask_for_questionnaire()
  views.ask_for_questionnaire(tmpl_3, req["user"]["id"])

  return make_response("", 200)

def form_display(req):
  tmpl = models.anonymous_form(req["user"]["id"], req["actions"][0]["value"])
  return views.anonymous_form(tmpl, req["view"]["id"], req["view"]["hash"])

def anonymous_questionnaire(req):
  action_val = req["actions"][0]["value"]

  if action_val == "do_questionnaire":
    tmpl = models.do_anonymous_questionnaire()
    return views.do_anonymous_questionnaire(tmpl, req["trigger_id"])

  if action_val == "not_do_questionnaire":
    tmpl = models.not_do_anonymous_questionnaire()
    return views.not_do_anonymous_questionnaire(tmpl, req["user"]["id"])

  return make_response("", 200)

def after_submit_anonymous_questionnaire(req):
  tmpl = models.after_submit_anonymous_questionnaire()
  return views.after_submit_anonymous_questionnaire(tmpl, req["user"]["id"])