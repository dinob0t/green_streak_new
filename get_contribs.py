import github3 as gh
import time
import datetime


# Get username and password
login = raw_input('Enter login: ')
password = raw_input('Enter password: ')

# Need Auth to increase rate limit to 5000 an hour
auth = gh.login(login, password)


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
valid_commits = ['CommitCommentEvent', 'PushEvent' ]

todays_public_count = 0
weekly_public_count = 0

for event in auth.iter_events():
	print event.list_types()
	payload = event.payload
	if payload['public']:
		pass
	#print 'Event type: ', event.type, ', created at: ', type(event.created_at) 
