import os
from slack import WebClient

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def get_user_joined_channels(user_id):
  all_channels = slack_client.channels_list().data["channels"]
  return list(map(
    lambda y: {"id": y["id"], "name": "#"+y["name"]}, filter(
      lambda x: user_id in x["members"], all_channels
    )
  ))

def get_channel_name_by_id(channel_id):
  return slack_client.channels_info(
    channel = channel_id
  )["channel"]["name"]

def get_users_in_channel(channel_id):
  users = slack_client.channels_info(
    channel = channel_id
  )["channel"]["members"]

  userinfos = []
  for user in users:
    userinfo = slack_client.users_info(
      user = user
    )["user"]
    userinfos.append({
      "id": userinfo["id"],
      "name": "@"+userinfo["name"]
    })
  
  return userinfos
