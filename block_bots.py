import requests,platform,re,os,time,sys,json
from requests_oauthlib import OAuth1
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def login(u,p):
	try:
		t = str(getToken())
		return requests.post("https://api.twitter.com/auth/1/xauth_password.json",data={'x_auth_identifier':u,'x_auth_password':p,'send_error_codes':'true','x_auth_login_verification':'1','x_auth_login_challenge':'1','x_auth_country_code':'US'},headers={'X-Guest-Token': t,'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F'}, verify=False)
	except Exception as e:
		print("Login func",e)
		return "false"
		pass

def getToken():
	page = ''
	while page == '':
		try:
			return requests.post("https://api.twitter.com/1.1/guest/activate.json",headers={"Authorization":"Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F"}, verify=False).json()['guest_token']
		except Exception as e:
			time.sleep(5)
			continue

def getFollowers(xtoken,xsecret,cursor="-1"):
	try:
		#https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=xb4l1c&count=5000
		return requests.get("https://api.twitter.com/1.1/followers/list.json?cursor="+str(cursor)+"&screen_name=xb4l1c&skip_status=true&include_user_entities=false&count=200",headers={
		"User-Agent": "Twitter-iPhone/9.62 iOS/13.3.3 (Apple;iPhone9,1;;;;;1)",
		"Content-Type": "application/json"},auth=OAuth1('3nVuSoBZnx6U4vzUxf5w','Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys',xtoken,xsecret,decoding=None), verify=False).json()
	
	except Exception as e:
		print("getFollowers func", e)
		pass


def blockUser(xtoken,xsecret,username):
	try:
		return requests.post("https://api.twitter.com/1.1/blocks/create.json?screen_name="+str(username)+"&skip_status=true",headers={"User-Agent": "Twitter-iPhone/9.62 iOS/13.3.3 (Apple;iPhone9,1;;;;;1)","Content-Type": "application/json"},auth=OAuth1('3nVuSoBZnx6U4vzUxf5w','Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys',xtoken,xsecret,decoding=None), verify=False).json()
	except Exception as e:
		print("blockUser func", e)
		pass

def saveFile(f,j):
	try:
		with open(str(f), "w") as f:
			f.write(json.dumps(j))
	except Exception as e:
		print("saveCreds func", e)
		pass
		
username = sys.argv[1]
password = sys.argv[2]
limit = sys.argv[3]

if not len(sys.argv) == 4:
	print("usage :\npython block_bots.py username(str) password(str) limit(int)")
	os._exit(0);
	
	
attemp = login(str(username),str(password)).json()
saveFile(str(username) + "_creds.json", attemp)
X_Token,X_Secret = attemp['oauth_token'],attemp['oauth_token_secret']
followers = getFollowers(X_Token,X_Secret)
users = []
users = followers["users"]
print("fetch users from Twitter..")

while True:
	print(len(followers["users"]),"...")
	if followers["next_cursor"] == 0:
		break
	followers = getFollowers(X_Token,X_Secret,followers["next_cursor"])
	for user in followers["users"]:
		users.append(user)


saveFile(str(username) + "_followers.json",users)

print("Totally,",len(users),"users found.")
yesOrno = input("Are you sure to block users?(yes or no)\n")
if yesOrno == "yes":
	with open(str(username) + "_blockusers.json", "a") as f:
		for user in users:
			if user["followers_count"]<int(limit):
				blockUser(X_Token,X_Secret,str(user["screen_name"]))
				print(user["screen_name"],"blocked.")
				f.write(str(user["screen_name"]) + "\n")
