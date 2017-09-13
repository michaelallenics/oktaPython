import requests
import OktaError
import GeneralOktaException
import urllib


class UserClient:

    """
    Functionality and documentation of API calls comes from: http://developer.okta.com/docs/api/resources/users.html

    Need To Implement:
        -Credential Operations (http://developer.okta.com/docs/api/resources/users.html#credential-operations)

    Have not tested list users functions
    """

    def __init__(self, orgUrl, apiKey):
        self.orgUrl = orgUrl
        self.apiKey = apiKey
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'SSWS ' + apiKey}
        self.endpointUrl = orgUrl + '/api/v1/users'

    # User Operations: https://developer.okta.com/docs/api/resources/users.html#user-operations

    def get_user(self, username):
        """
        http://developer.okta.com/docs/api/resources/users.html#get-user
        :param username: this can be the user ID, login, or login shortname
        :return: user object
        """
        getUrl = self.endpointUrl + '/' + username
        response = requests.get(getUrl, headers=self.headers).json()
        try:
            id = response['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def get_user_from_email(self, email):
        getUrl = self.endpointUrl + '?filter=profile.email+eq+"' + email + '"'
        response = requests.get(getUrl, headers=self.headers).json()
        """
        THIS CODE IS FOR PARSING ADS LOADING ERRORS IN LARGE FILES
        getUrl = self.endpointUrl + '?search=profile.email+sw+"' + email + '"'
        response = requests.get(getUrl, headers=self.headers).json()
        try:
            if len(response) == 0: return response
            id = response[0]['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        """
        if len(response) > 1:
            try:
                id = response[0]['id']
                raise GeneralOktaException.GeneralOktaException('get_user_from_email', 'There is more than one user with the email address ' + email)
            except KeyError:
                raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        elif len(response) == 0:
            raise GeneralOktaException.GeneralOktaException('get_user_from_email','Could not find a user with the email address ' + email)
        try:
            id = response[0]['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def create_user(self, profile, activate=True, provider=False, credentials=None, groupIds=None):
        """
        http://developer.okta.com/docs/api/resources/users.html#create-user
        :param profile: dict object with at lease firstName, lastName, username, and email
        :param activate: should you activate the user? Boolean
        :param provider: Indicates whether to create a user with a specified authentication provider. Boolean
        :param credentials: dict credential object, doc here: http://developer.okta.com/docs/api/resources/users.html#credentials-object
        :param groupIds: List of group IDs
        :return: created user object
        """
        postUrl = self.endpointUrl + '?activate=' + str(activate) + '&provider=' + str(provider)
        body = dict()
        body['profile'] = profile
        if credentials is not None:
            body['credentials'] = credentials
        if groupIds is not None:
            if len(groupIds) > 0:
                body['groupIds'] = groupIds
        response = requests.post(postUrl, json=body, headers=self.headers).json()
        try:
            response['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def update_user(self, userId, profile=None, credentials=None, replace=False):
        """
        http://developer.okta.com/docs/api/resources/users.html#update-user
        :param userId: id of user to update, String
        :param profile: Updated profile for user, Profile object, Dict
        :param credentials: Update credentials for user, Credentials object, Dict (http://developer.okta.com/docs/api/resources/users.html#credentials-object)
        :param replace: True if replacing profile/credentials with given input (complete update), False for partial updates
        :return: updated user object
        """
        requestUrl = self.endpointUrl + '/' + userId
        body = dict()
        if credentials is not None:
            body['credentials'] = credentials
        if profile is not None:
            body['profile'] = profile
            if replace:
                response = requests.put(requestUrl, json=body, headers=self.headers).json()
            else:
                response = requests.post(requestUrl, json=body, headers=self.headers).json()
        # if profile is None ignore the replace argument, credential updates are only POST
        else:
            response = requests.post(requestUrl, json=body, headers=self.headers).json()
        try:
            response['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def list_users(self, limit=200, find=None, filter=None, search=None):
        """
        List Users: https://developer.okta.com/docs/api/resources/users.html#list-users
        Find Users: https://developer.okta.com/docs/api/resources/users.html#find-users
        List With Filter: https://developer.okta.com/docs/api/resources/users.html#list-users-with-a-filter
        List with Search: https://developer.okta.com/docs/api/resources/users.html#list-users-with-search

        Only one of find, filter, and search can not be None
        Note: Search is currently in EA, will not be available for all orgs
        Note: Search data is not up to date, may have to wait to get recently changed info
        For examples of search and filter strings click on the links above, for more info about filtering look here:
        https://developer.okta.com/docs/api/getting_started/design_principles.html#filtering

        :param limit: Max number of users to return
        :param find: A string to look up users based on firstName, lastName, or email. Does not support pagination
        :param filter: A filter string to list users that meet the criteria. Input is non URL Encoded. supports: status, lastUpdated, id, profile.login, profile.email, profile.firstName, and profile.lastName. Does not include Deprovisioned users
        :param search: A search string to search for users based on profile values, all profile attributes are supported as well as the top level attributes: id, status, created, activated, statusChanged and lastUpdated
        :return: A list of user profile objects that meet the criteria
        """
        if find is not None and (filter is None and search is None):
            getUrl = self.endpointUrl + '?q=' + find + '&limit=' + str(limit)
        elif filter is not None and (find is None and search is None):
            getUrl = self.endpointUrl + '?filter=' + urllib.quote_plus(filter) + '&limit=' + str(limit)
        elif search is not None and (find is None and filter is None):
            getUrl = self.endpointUrl + '?search=' + urllib.quote_plus(search) + '&limit=' + str(limit)
        elif find is None and filter is None and search is None:
            getUrl = self.endpointUrl + '?limit=' + str(limit)
        else:
            raise GeneralOktaException.GeneralOktaException('list_users', 'Only one of the input parameters can be not None')
        response = requests.get(getUrl, headers=self.headers).json()
        try:
            response['errorCode']
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        except TypeError:
            size = len(response)
            # if pagination is required to iterate through all users
            if size == limit:
                result = []
                result.extend(response)
                while size == limit:
                    id = response[size - 1]['id']
                    newUrl = getUrl + '&after=' + id
                    response = requests.get(newUrl, headers=self.headers).json()
                    result.extend(response)
                    size = len(response)
                return result
            else:
                return response
        except KeyError:
            GeneralOktaException.GeneralOktaException('list_users', 'Unknown JSON Object was returned')

    # Related Resources: https://developer.okta.com/docs/api/resources/users.html#related-resources

    def get_user_app_links(self, userId):
        """
        http://developer.okta.com/docs/api/resources/users.html#get-assigned-app-links
        :param userId: unique id of user
        :return: Array of App Link objects
        """
        getUrl = self.endpointUrl + '/' + userId + '/appLinks'
        response = requests.get(getUrl, headers=self.headers).json()
        if len(response) == 0:
            return response
        try:
            id = response[0]['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def get_user_groups(self, userId):
        """
        http://developer.okta.com/docs/api/resources/users.html#get-member-groups
        :param userId: unique id of user
        :return: Array of group objects
        """
        getUrl = self.endpointUrl + '/' + userId + '/groups'
        response = requests.get(getUrl, headers=self.headers).json()
        if len(response) == 0:
            return response
        try:
            id = response[0]['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    # Lifecycle Operations: https://developer.okta.com/docs/api/resources/users.html#lifecycle-operations

    def activate_user(self, userId, sendEmail=True):
        """
        https://developer.okta.com/docs/api/resources/users.html#activate-user
        USE WHEN USER IN STAGED STATUS
        :param userId: unique ID of user
        :param sendEmail: Sends an activation email to the user if true
        :return: Returns an empty object unless sendEmail=false, then it returns an activation link
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/activate?sendEmail=' + str(sendEmail).lower()
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            response['activationToken']
            return response
        except KeyError:
            try:
                code = response['errorCode']
                raise OktaError.OktaError(code, response['errorSummary'])
            except KeyError:
                raise GeneralOktaException.GeneralOktaException('activate_user', 'An unkown JSON Object has been returned')

    def reactivate_user(self, userId, sendEmail=True):
        """
        https://developer.okta.com/docs/api/resources/users.html#reactivate-user
        USER WHEN USER IN PROVISIONED STATUS
        :param userId: Unique ID of user
        :param sendEmail: Sends an activation email to the user if true
        :return: Returns an empty object unless sendEmail=false, then it returns an activation link
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/reactivate?sendEmail=' + str(sendEmail).lower()
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            response['activationToken']
            return response
        except KeyError:
            try:
                code = response['errorCode']
                raise OktaError.OktaError(code, response['errorSummary'])
            except KeyError:
                raise GeneralOktaException.GeneralOktaException('reactivate_user', 'An unkown JSON Object has been returned')

    def deactivate_user(self, userId):
        """
        https://developer.okta.com/docs/api/resources/users.html#deactivate-user
        :param userId: Unique ID of user
        :return: returns an empty object
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/deactivate'
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('deactivate_user', 'An unkown JSON Object has been returned')

    def suspend_user(self, userId):
        """
        https://developer.okta.com/docs/api/resources/users.html#suspend-user
        :param userId: Unique ID of user
        :return: returns an empty object
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/suspend'
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('suspend_user', 'An unkown JSON Object has been returned')

    def unsuspend_user(self, userId):
        """
        https://developer.okta.com/docs/api/resources/users.html#unsuspend-user
        :param userId: Unique ID of user
        :return: returns an empty object
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/unsuspend'
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('unsuspend_user', 'An unkown JSON Object has been returned')

    def delete_user(self, userId):
        """
        https://developer.okta.com/docs/api/resources/users.html#delete-user
        :param userId: unique ID of user
        :return: empty object
        """
        deleteUrl = self.endpointUrl + "/" + userId
        try:
            response = requests.delete(deleteUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('delete_user', 'An unkown JSON Object has been returned')

    def unlock_user(self, userId):
        """
        https://developer.okta.com/docs/api/resources/users.html#unlock-user
        :param userId: unique ID of user
        :return: empty object
        """
        postUrl = self.endpointUrl + "/" + userId + '/lifecycle/unlock'
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('unlock_user', 'An unkown JSON Object has been returned')

    def reset_password(self, userId, sendEmail=True):
        """
        https://developer.okta.com/docs/api/resources/users.html#reset-password
        :param userId: unique ID of user
        :param sendEmail: Sends a reset password email to the user if true
        :return: Returns an empty object unless sendEmail=false, then it returns a password reset link
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/reset_password?sendEmail=' + str(sendEmail).lower()
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            response['resetPasswordUrl']
            return response
        except KeyError:
            try:
                code = response['errorCode']
                raise OktaError.OktaError(code, response['errorSummary'])
            except KeyError:
                raise GeneralOktaException.GeneralOktaException('reset_password', 'An unkown JSON Object has been returned')

    def expire_password(self, userId, tempPassword=False):
        """
        https://developer.okta.com/docs/api/resources/users.html#expire-password
        :param userId: unique ID of user
        :param sendEmail: Sends a reset password email to the user if true
        :return: Returns a user object unless tempPassword=true, then it returns a object with a temporary password
        """
        postUrl = self.endpointUrl + '/' + userId + '/lifecycle/expire_password?tempPassword=' + str(tempPassword).lower()
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            response['id']
            return response
        except KeyError:
            try:
                response['tempPassword']
                return response
            except KeyError:
                try:
                    code = response['errorCode']
                    raise OktaError.OktaError(code, response['errorSummary'])
                except KeyError:
                    raise GeneralOktaException.GeneralOktaException('expire_password', 'An unkown JSON Object has been returned')

    def reset_factors(self, userId):
        """
        https://developer.okta.com/docs/api/resources/users.html#reset-factors
        :param userId: unique ID of user
        :return: empty object
        """
        postUrl = self.endpointUrl + "/" + userId + '/lifecycle/reset_factors'
        try:
            response = requests.post(postUrl, headers=self.headers).json()
            if len(response) == 0:
                return response
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('reset_factors', 'An unkown JSON Object has been returned')

    # User Sessions: https://developer.okta.com/docs/api/resources/users.html#user-sessions

    def clear_user_sessions(self, userId, oauthTokens=False):
        """
        https://developer.okta.com/docs/api/resources/users.html#clear-user-sessions
        :param userId: Unique ID of the user
        :param oauthTokens: Revoke issued OpenID Connect and OAuth refresh and access tokens
        :return: None
        """
        deleteUrl = self.endpointUrl + '/' + userId + '/sessions?oauthTokens=' + str(oauthTokens).lower()
        try:
            response = requests.delete(deleteUrl, headers=self.headers).json()
            code = response['errorCode']
            raise OktaError.OktaError(code, response['errorSummary'])
        except ValueError:
            return None
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('clear_user_sessions', 'An unkown JSON Object has been returned')
