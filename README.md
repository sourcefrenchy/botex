# botex
 A slack bot to convert expressions into LaTeX images. Really **alpha**, code is not perfect nor optimal at all.
![](https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png | width=100)

# overview
- Received expressions via "tex <expression>" sent to the bot
- Convert into LaTeX
- Upload to s3 bucket protected by KMS
- Generate a pre-signed URL for the user
 
# todo
- Expire old pictures from the s3 bucket (30days?)
 
# configuration
- If using Docker, edit start.sh and insert your own SLACKTOKEN, AWS credentials information
- Edit botex.py and update your AWS information (Bucket, region, KMS key-id)

# editing/building new container
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
