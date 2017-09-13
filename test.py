import warnings
import requests
import Users
import OktaError
import Groups
import Apps
import GeneralOktaException
warnings.filterwarnings("ignore")


oktaUrl = ''
apiKey = ''

user_client = Users.UserClient(oktaUrl, apiKey)
group_client = Groups.GroupsClient(oktaUrl, apiKey)
apps_client = Apps.AppsClient(oktaUrl, apiKey)

try:
    response = user_client.clear_user_sessions('00u9vo78qxK9HrRBC0h7')
    print response
except OktaError.OktaError as e:
    print e.errorCode
    print e.errorSummary
except GeneralOktaException.GeneralOktaException as e:
    print e.errorMethod
    print e.errorMessage

