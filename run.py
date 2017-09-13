import warnings
import Users
import OktaError
import Groups
import Apps
import GeneralOktaException
import requests
warnings.filterwarnings("ignore")



oktaUrl = "https://alliancedata.okta.com"
apiKey = ""

user_client = Users.UserClient(oktaUrl, apiKey)
group_client = Groups.GroupsClient(oktaUrl, apiKey)


# print usernames of group
groupId = group_client.get_group_from_name("MyFin Users")[0]['id']
users = group_client.list_group_membership(groupId)
for user in users:
    print user['profile']['login']

"""
### SCRIPT IS ADDING USERS
path = 'C:\\Users\\Michael\\Google Drive\\Projects\\Alliance Data\\Phase 2\\PSHR\\HRTSTUsers2.txt'
groupId = group_client.get_group_from_name("HRTRN")[0]['id']



file = open(path, 'r')


for line in file:
    user = line.strip()
    userId = None
    #try to get the user id from either the username or the email address
    try:
        #from username
        userId = user_client.get_user(user)['id']
    except OktaError.OktaError:
        try:
            #from email address
            userSearch = user_client.get_user_from_email(user)
            if len(userSearch) > 1:
                print "Multiple users with email: " + user
            else:
                userId = userSearch[0]['id']
        except GeneralOktaException.GeneralOktaException as e:
            print e.errorMessage
    #make sure it worked
    if userId is not None:
        #attempt to add the user
        try:
            #delete_user = group_client.delete_user_from_group(userId, groupId)
            add_user = group_client.add_user_to_group(userId, groupId)
        #if the add failed, print the username
        except OktaError.OktaError:
            print user

file.close()


"""





"""
for line in file:
    user = line.strip().lower()
    userprefix = user.split('@')[0]
    userId = None
    #try to get the user id from either the username or the email address
    try:
        # from email address
        userSearch = user_client.get_user_from_email(userprefix)
        if len(userSearch) > 0:
            println = ""
            for i in range(len(userSearch)):
                println += userSearch[i]['profile']['login'] + ', '
            print user + " has the following matches: " + println
        else:
            print user + " has no prefix matches"
    except GeneralOktaException.GeneralOktaException as e:
        print e.errorMessage


file.close()
"""