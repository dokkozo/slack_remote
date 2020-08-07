# slack remote: Remote Shell Control over Slack
Slack remote is a chatbot based remote control of machine on which the bot is working. The implementation is based on [slackbot](https://github.com/lins05/slackbot).
Please use this bot with great care about your security.

## installation
- Prepare two API tokens
    - Legacy API token for slackbot module to work. Detail: [slackbot](https://github.com/lins05/slackbot).
    - OAUTH Access token for file read/write. 
        - Add files:read and files:write to User Token Scopes. reference: https://qiita.com/ykhirao/items/3b19ee6a1458cfb4ba21 (Japanese)
- Set variables in slackbot_setting
- run run.py