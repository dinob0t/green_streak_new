import github3 as gh
import time
import datetime
import getpass
from dateutil import rrule, tz


def utc_to_local(dt_in):
	from_zone = tz.gettz('UTC')
	#local_tz = datetime.datetime.now(tz.tzlocal()).tzinfo
	to_zone = tz.tzlocal()	
	dt_in = dt_in.replace(tzinfo=from_zone)
	dt_out = dt_in.astimezone(to_zone)
	return dt_out
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


def print_calender(now, prev_days):
	now_m_delta = now - datetime.timedelta(days=prev_days-1)
	for dt in rrule.rrule(rrule.DAILY, dtstart=now_m_delta, until=now):
		cur_date = dt.strftime("%Y-%m-%d")
		if cur_date in day_bins.keys():
			print cur_date, ': ', day_bins[cur_date]
		else:
			print cur_date, ': ', 0 

# Get username and password
login = raw_input('Enter login: ')
password = getpass.getpass('Enter password: ')



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
valid_commits = ['PushEvent', 'CreateEvent']

# Get today's date
now = datetime.datetime.now()

print 'Time now is now: '
today = get_time_string(now.isoformat().encode('utf-8'))
print 'Day now is (UTC): ', today


user = gh.user(login)
user = auth.user()
day_bins = {today:0}
# Go through each event
for event in user.iter_events():
	# If its a valid streak event
	if event.type in valid_commits:	
		# Only count public events
		if event.public:
			# Get the payload
			payload = event.payload
			# Get created datetime
			cur_dt = get_time_string(utc_to_local(event.created_at).isoformat())
			# If it's a push event
			if event.type == valid_commits[0]:
				# If the commit was to master
				if payload['ref'] == 'refs/heads/master':
					# Add all the commits to streak count
					update_day_bins(cur_dt,len(payload['commits']))
					
			# If it's a comment event
			elif payload['master_branch']==payload['ref']:
				update_day_bins(cur_dt,1)


print 'Recent activity: '
print_calender(now, 100)

print 'Auth calls remaining this hour: ', auth.ratelimit_remaining
print 'Public calls remaining this hour: ',gh.ratelimit_remaining()