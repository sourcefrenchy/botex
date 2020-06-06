# botex
 A slack bot to convert expressions into LaTeX images. Really **alpha**, code is not perfect nor optimal at all.

# overview
- Received expressions via "tex <expression>" sent to the bot
- Convert into LaTeX
- Upload to s3 bucket protected by KMS
- Generate a pre-signed URL for the user
 
# configuration
- If using Docker, edit start.sh and insert your own SLACKTOKEN, AWS credentials information
- Edit botex.py and update your AWS information (Bucket, region, KMS key-id)
