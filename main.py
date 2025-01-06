from argparse import ArgumentParser
import requests 
import json
import os

COOKIE_FILE = "cookie.txt"
COOKIE = None

def load_saved_cookie():
    try:
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r') as f:
                return f.read().strip()
    except Exception as e:
        print(f"Error loading saved cookie: {e}")
    return None

def save_cookie(cookie: str):
    try:
        with open(COOKIE_FILE, 'w') as f:
            f.write(cookie)
    except Exception as e:
        print(f"Error saving cookie: {e}")
    

def set_cookie(cookie: str):
    global COOKIE
    COOKIE = cookie
    save_cookie(cookie)
     


def get_cookie():
    global COOKIE
    
    if COOKIE is None:
        COOKIE = load_saved_cookie()
    return COOKIE
    

def get_bearer_token():
    return "AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw"


def get_user_id(username: str):
    cached: dict[str, str] = {}
    
    if username in cached:
        return cached[username]
    
    url = "https://api.twitter.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName"
    
    vars = {
        "screen_name": username,
        "withSafetyModeUserFields": True,
    }
    
    features = {
        "hidden_profile_subscriptions_enabled":                              True,
		"rweb_tipjar_consumption_enabled":                                   True,
		"responsive_web_graphql_exclude_directive_enabled":                  True,
		"verified_phone_label_enabled":                                      False,
		"subscriptions_verification_info_is_identity_verified_enabled":      True,
		"subscriptions_verification_info_verified_since_enabled":            True,
		"highlights_tweets_tab_ui_enabled":                                  True,
		"responsive_web_twitter_article_notes_tab_enabled":                  True,
		"subscriptions_feature_can_gift_premium":                            True,
		"creator_subscriptions_tweet_preview_api_enabled":                   True,
		"responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
		"responsive_web_graphql_timeline_navigation_enabled":                True,
    }
    
    params = {
        "variables": json.dumps(vars),
        "features": json.dumps(features)
    }
    
    res = requests.get(url, headers=get_headers(), params=params)
    
    res.raise_for_status()
    
    json_res = res.json()
    
    if "errors" in json_res and json_res['data']['user']['result']['rest_id'] == '':
        raise Exception("User not found")
    
    user_id = json_res['data']['user']['result']['rest_id']
    
    print(user_id)
    
    cached[username] = user_id
    
    return user_id
    
    




def get_guest_token():
    url = "https://api.twitter.com/1.1/guest/activate.json"
    
    headers = {
        "Authorization": f"Bearer {get_bearer_token()}",
    }
    
    res = requests.post(url, headers=headers)
    
    res.raise_for_status()
    
    
    json = res.json()
    print(json)
    
    guest_token = None
    
    if "guest_token" in json:
        guest_token = json["guest_token"]
    
    if guest_token is None:
        raise Exception("Guest token is None")
    else:
        return guest_token

def get_headers():
    cookie = get_cookie()

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {get_bearer_token()}",
        "cookie": cookie,
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "x-csrf-token": cookie.split('ct0=')[1].split(';')[0]
    }
    
    return headers
 
def getMedia(userid: str, count: int = 20):
    
    url = "https://x.com/i/api/graphql/2tLOJWwGuCTytDrGBg8VwQ/UserMedia"
    
    params = {
        "variables": json.dumps({
            "userId": userid,
            "count": count,
            "withClientEventToken": False,
            "withBirdwatchNotes": False,
            "includePromotedContent": False,
            "withVoice": True,
            "withV2Timeline": True
        }),
        "features": json.dumps({
           "responsive_web_graphql_exclude_directive_enabled":                        True,
		"verified_phone_label_enabled":                                            False,
		"creator_subscriptions_tweet_preview_api_enabled":                         True,
		"responsive_web_graphql_timeline_navigation_enabled":                      True,
		"responsive_web_graphql_skip_user_profile_image_extensions_enabled":       False,
		"c9s_tweet_anatomy_moderator_badge_enabled":                               True,
		"tweetypie_unmention_optimization_enabled":                                True,
		"responsive_web_edit_tweet_api_enabled":                                   True,
		"graphql_is_translatable_rweb_tweet_is_translatable_enabled":              True,
		"view_counts_everywhere_api_enabled":                                      True,
		"longform_notetweets_consumption_enabled":                                 True,
		"responsive_web_twitter_article_tweet_consumption_enabled":                True,
		"tweet_awards_web_tipping_enabled":                                        False,
		"freedom_of_speech_not_reach_fetch_enabled":                               True,
		"standardized_nudges_misinfo":                                             True,
		"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
		"rweb_video_timestamps_enabled":                                           True,
		"longform_notetweets_rich_text_read_enabled":                              True,
		"longform_notetweets_inline_media_enabled":                                True,
		"responsive_web_media_download_video_enabled":                             False,
		"responsive_web_enhance_cards_enabled":                                    False,
        })
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.text 
    
    
def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--cookie", help="Cookie", type=str, required=False)
    parser.add_argument("--user", help="Username", type=str, required=False)
    return parser.parse_args()



def main(args):
    
    saved_cookie = load_saved_cookie()
    
    if args.cookie:
        set_cookie(args.cookie)
        
    elif saved_cookie:
        set_cookie(saved_cookie)
        
    else:
        raise Exception("Cookie is required. Please provide it with --cookie or save it in cookie.txt")
    
    
    if args.cookie and not args.user:
        set_cookie(args.cookie)
        print("Cookie loaded. Please provide username with --user")
        return
    
    if not args.user:
        raise Exception("Username is required. Please provide it with --user")
    
    user_id = get_user_id(args.user)
    
    if not isinstance(user_id, str):
        raise Exception("User not found")
    
    print(getMedia(user_id))
   
    

if __name__ == "__main__":
    main(parse_args())
