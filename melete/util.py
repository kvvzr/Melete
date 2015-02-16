import string, random, re, requests, shutil

def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

def save_as_random_name(url, save_path):
    filetype = None
    pattern = re.compile(r'.+\.(?P<filetype>\w+)')
    match_obj = pattern.match(url)
    if not match_obj:
        return None

    filetype = match_obj.group('filetype')
    filename = random_string(16)

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        filepath = '%s/%s.%s' % (save_path, filename, filetype)
        with open(filepath, 'wb') as file:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, file)

    return filename + '.' + filetype

def save_twitter_icon(twitter, save_path, screen_name, user_id):
    res = twitter.request('users/show.json', data={
        'user_id': user_id,
        'screen_name': screen_name
    })
    if res.status == 200:
        icon_path = save_as_random_name(
            res.data['profile_image_url'],
            save_path
        )
        return icon_path
    return None
