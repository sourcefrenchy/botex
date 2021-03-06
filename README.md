# botex
 A slack bot to convert expressions into LaTeX images. Really **alpha**, code is ugly and not optimal at all.

# Overview
- Received expressions via "tex <expression>" sent to the bot
- Convert into LaTeX
- Upload to s3 bucket protected by KMS
- Generate a pre-signed URL for the user
 
 <img src="https://github.com/sourcefrenchy/botex/blob/master/s1.png?raw=true" width="300" /> <img src="https://github.com/sourcefrenchy/botex/blob/master/s2.png?raw=true" width="300" />
 
# Todo
- Expire old pictures from the s3 bucket (30days?)
- Delete old pictures from the docker container
 
# Configuration
- If using Docker, edit start.sh and insert your own SLACKTOKEN, AWS credentials information
- Edit botex.py and update your AWS information (Bucket, region, KMS key-id)

# Editing/building new container
- Git clone this project and edit Dockerfile based on your needs
- To create a new container:

```
botex on  master via 🐍 v3.7.7 (botex) on ☁️  us-east-1 
➜ docker build -t botex/botex:latest .
```

- To test your new container:
```
botex on  master via 🐍 v3.7.7 (botex) on ☁️  us-east-1 
➜ docker run --shm-size=256m botex/botex
```
***important*** Without editing (see Configuration above) and adding your SLACKTOKEN, running this the first time will result in "slack.errors.SlackApiError: The request to the Slack API failed. The server responded with: {'ok': False, 'error': 'invalid_auth'}"
