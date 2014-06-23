import github3 as gh
import time
import datetime
import pytz

# Return only year/month/day
def get_time_string(time_in):
	cur_str = list(time_in)
	cur_str = cur_str[0:10]
	cur_str = ''.join(cur_str)
	return cur_str

def update_day_bins(key, count):
	if key in day_bins.keys():
		day_bins[key] = day_bins[key] + count
	else:
		day_bins[key] = 1


# Get username and password
login = raw_input('Enter login: ')
password = raw_input('Enter password: ')

# Need Auth to increase rate limit to 5000 an hour
auth = gh.login(login, password)

# Green colour levels from Github
green_defs = {0: '#eee', 
			  1: '#d6e685', 
			  3: '#8cc665',
			  4: '#44a340',
  		      5: '#1e6823'}

###################################################
# # Below might be useful to get maximum commit num
# # Get all public repos for user
# for repo in auth.iter_repos(type='public'):

# 	# Start with empty dictionary
# 	repo_dict = {}	

# 	# When we request repo stats, the API takes a second
# 	# to calculate and respond. An empty dict is 
# 	# returned until we get a response
# 	# <Insert asynch implemntation here>

# 	while not repo_dict:
# 		repo_dict = repo.weekly_commit_count()
# 		if repo_dict:
# 			break
# 		time.sleep(0.25)
# 	print repo, repo_dict['owner']
###################################################

# Dump of all possible events
#['CommitCommentEvent', 'CreateEvent', 'DeleteEvent', 'FollowEvent', 'ForkApplyEvent', 'ForkEvent', 'GistEvent', 'GollumEvent', 'IssueCommentEvent', 'IssuesEvent', 'MemberEvent', 'PublicEvent', 'PullRequestEvent', 'PullRequestReviewCommentEvent', 'PushEvent', 'ReleaseEvent', 'StatusEvent', 'TeamAddEvent', 'WatchEvent']

# Valid commit types
valid_commits = ['PushEvent', 'CommitCommentEvent']

# Get today's date
now = datetime.datetime.now(pytz.utc)
today = get_time_string(now.isoformat())
print 'Day now is (UTC): ', today

day_bins = {today:0}
# Go through each event
for event in auth.iter_events():
	# If its a valid streak event
	if event.type in valid_commits:	
		# Only count public events
		if event.public:
			# Get the payload
			payload = event.payload
			# Get created datetime
			cur_dt = get_time_string((event.to_json())['created_at'])
			print event.to_json()
			# If it's a push event
			if event.type == valid_commits[0]:
				# If the commit was to master
				if payload['ref'] == 'refs/heads/master':
					# Add all the commits to streak count
					update_day_bins(cur_dt,len(payload['commits']))
					
			# If it's a comment event
			else:
				update_day_bins(cur_dt,1)

print day_bins