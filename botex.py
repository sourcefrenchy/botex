#!/Users/jma/.virtualenvs/botex/bin/python
# *** botex *** - render latex expressions into png and serve presigned url to it back to the user
# jeanmichel.amblat@gmail.com
#

import os, sys
import time
import logging
from slack import RTMClient
from slack.errors import SlackApiError
from pytexit import py2tex
import sympy
from pathlib import Path

import logging
import boto3
from botocore.client import Config
import botocore

DEBUG = False
AWS_S3_BUCKET = "botexjmatestingforfun"
AWS_S3_KEYID = "df05d3d3-c4a6-4d62-9f62-b540a3ca1150"
AWS_REGION = "us-east-1"

def file2s3_getlink(filename, bucket=AWS_S3_BUCKET, object_name=None):
	"""Upload a file to an S3 bucket

	:param file_name: File to upload
	:param bucket: Bucket to upload to
	:param object_name: S3 object name. If not specified then file_name is used
	:return: True if file was uploaded, else False
	"""

	if os.environ["AWS_ACCESS_KEY_ID"]:
		s3 = boto3.client('s3', AWS_REGION, config=Config(signature_version='s3v4'))
		try:
			f = open('/var/tmp/' + filename, 'rb')
			content = f.read()
			resp = s3.put_object(Bucket=AWS_S3_BUCKET,
              Key=filename,
              Body=content,
              ServerSideEncryption='aws:kms',
              SSEKMSKeyId=AWS_S3_KEYID)
			url = s3.generate_presigned_url(
					ClientMethod='get_object',
					Params={
						'Bucket': AWS_S3_BUCKET,
						'Key': filename
					}
				)
			return url
		except botocore.exceptions.ClientError as e:
			if DEBUG:
				print("[DEBUG] - {}".format(e))
			return False
		return True
	else:
		print("[FATAL] Missing AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY env. variables!")
		sys.exit(0)

@RTMClient.run_on(event='message')
def slack_loop_botex(**payload):
	data = payload['data']
	web_client = payload['web_client']
	rtm_client = payload['rtm_client']

	if DEBUG:
		print("[DEBUG] def slack_loop_botex()")

	if 'text' in data and 'tex' in data.get('text', []):
		channel_id = data['channel']
		thread_ts = data['ts']
		user = data['user']
		latexreq = data['text'].split("tex ",1)[1]

		filename = time.strftime("%Y%m%d-%H%M%S-{}-output.png".format(user))

		if DEBUG:
			print("[DEBUG] received text={} latexreq={}".format(data['text'], latexreq))

		try:
			latex = py2tex(latexreq)
			if DEBUG:
				print("[DEBUG] latex={}".format(latex))
			if DEBUG:
				print("[DEBUG] Generating png file")
			sympy.preview(latex, viewer='file', filename='/var/tmp/' + filename)
			if DEBUG:
				print("[DEBUG] Uploading to S3")
			reply = file2s3_getlink(filename)
		except:
			reply = "Cannot transform this expression, invalid syntax?"
		try:
			response = web_client.chat_postMessage(
				channel=channel_id,
				text=f"Hi <@{user}>! " + reply,
				thread_ts=thread_ts
			)
		except SlackApiError as e:
			# You will get a SlackApiError if "ok" is False
			assert e.response["ok"] is False
			assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
			print(f"Got an error: {e.response['error']}")

if os.environ["SLACKTOKEN"]:
	rtm_client = RTMClient(token=os.environ["SLACKTOKEN"])
	rtm_client.start()
else:
	print("[FATAL] No SLACKTOKEN env. variable set!")