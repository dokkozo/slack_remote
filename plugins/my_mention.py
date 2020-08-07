# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import default_reply
import os
import subprocess as sp
import requests
import codecs
import slackbot_settings

# move to default dir
os.chdir(slackbot_settings.DEFAULT_DIR)

@respond_to(r'^cd\s*')
def change_dir(message):
    usrtext = message.body['text']
    to_dir = usrtext.split(' ', maxsplit=1)[1]
    print(f'cd {to_dir}')
    os.chdir(to_dir)
    retval = sp.check_output('pwd', shell=True)
    message.reply(retval)

@respond_to(r'^ls')
def list_dir(message):
    usrtext = message.body['text'].replace('*','')
    print(usrtext)
    flist = sp.check_output(usrtext, shell=True).decode('utf-8').strip('\n').split('\n')
    flist = '```' + '\n'.join([f'[{f}]' if os.path.isdir(f) else f'{f}' for f in flist]) + '```'
    print(flist)
    message.reply(flist)

@respond_to(r'^get\s*')
def get_file_from_remote(message):
    usrtext = message.body['text']
    target_file = usrtext.split(' ', maxsplit=1)[1]
    if not os.path.exists(target_file):
        message.reply(f'{target_file} does not exist')
        return
    
    print(f'get {target_file}')
    param = {
        'token':slackbot_settings.API_TOKEN_FIO,
        'filename':target_file.rsplit('/')[-1],
        'title':target_file.rsplit('/')[-1],
        'initial_comment':f'send {os.path.abspath(target_file)}',
        'channels':slackbot_settings.DEFAULT_CHANNEL,
    }
    with open(target_file, 'rb') as f:
        content = requests.post(
            url="https://slack.com/api/files.upload",
            params=param,
            files={'file': f}
        )
    print(content.json())

@respond_to(r'^send\s*')
def do_nothing(message):
    # This function is necessary to prevent a bot from replying to another bot uploading file
    # in response to get command
    pass

@default_reply()
def default_func(message):
    usrtext = message.body['text'].replace('*','')
    # in case of file receiving
    if 'files' in message._body:
        # receive files
        filesinfo = message._body['files']
        save_dir = ('./' if usrtext == '' else usrtext)
        # check savepath
        if not os.path.isdir(save_dir):
            message.reply(f'{save_dir} does not exist or is not directory')
        else:
            # save each file
            reply_msg = ''
            for finfo in filesinfo:
                save_path = f'{save_dir}/{finfo["name"]}'
                file_url = finfo['url_private_download']
                # get file from slack storage
                content = requests.get(file_url,
                        allow_redirects=True,
                        headers={'Authorization': 'Bearer %s' % slackbot_settings.API_TOKEN}, 
                        stream=True
                    ).content
                # savefile
                fp = codecs.open(save_path, 'wb')
                fp.write(content)
                fp.close()
                # reply
                reply_msg += f'{save_path}\n'
            message.reply(reply_msg.rstrip('\n')) 
        
        for finfo in filesinfo:
            requests.get('https://slack.com/api/files.delete',
                params={
                    'token':slackbot_settings.API_TOKEN_FIO,
                    'file':finfo['permalink'].split('/')[-2]
                },
            )

    # in case of normal command
    else:
        print(usrtext)
        execresult = sp.check_output(usrtext, shell=True).decode('utf-8') 
        if execresult == '':
            message.react('+1')
        else:
            rettext = '```' + execresult + '```'
            print(rettext)
            message.reply(rettext)
        
