#!/Users/jma/.virtualenvs/botex/bin/python
import os
from slack import RTMClient
from slack.errors import SlackApiError
from pytexit import py2tex
import sympy

DEBUG = True

@RTMClient.run_on(event='message')
def say_hello(**payload):
	data = payload['data']
	web_client = payload['web_client']
	rtm_client = payload['rtm_client']
	if 'text' in data and 'tex' in data.get('text', []):
		channel_id = data['channel']
		thread_ts = data['ts']
		user = data['user']
		latexreq = data['text'].split("tex ",1)[1]
		if DEBUG:
			print("D> received text={} latexreq={}".format(data['text'], latexreq))
		try:
			latex = py2tex(latexreq)
			if DEBUG:
				print("D> computed={}".format(latex))
			computed = sympy.preview(latex, viewer='file', filename='output.png')
		except:
			computed = "Cannot transform this expression, invalid syntax?"
		try:
			response = web_client.chat_postMessage(
				channel=channel_id,
				text=f"Hi <@{user}>! " + computed,
				thread_ts=thread_ts
			)
		except SlackApiError as e:
			# You will get a SlackApiError if "ok" is False
			assert e.response["ok"] is False
			assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
			print(f"Got an error: {e.response['error']}")

rtm_client = RTMClient(token=os.environ["SLACKTOKEN"])
rtm_client.start()