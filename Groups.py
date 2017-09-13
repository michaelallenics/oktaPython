import requests
import OktaError
import GeneralOktaException
import urllib


class GroupsClient:

    """
    Functionality and documentation of API calls comes from: http://developer.okta.com/docs/api/resources/groups.html

    Need To Implement:
        -Everything
    """

    def __init__(self, orgUrl, apiKey):
        self.orgUrl = orgUrl
        self.apiKey = apiKey
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'SSWS ' + apiKey}
        self.endpointUrl = orgUrl + '/api/v1/groups'

    def get_group(self, groupId):
        """
        http://developer.okta.com/docs/api/resources/groups.html#get-group
        :param groupId: unique id of a group
        :return: Group object
        """
        getUrl = self.endpointUrl + '/' + groupId
        response = requests.get(getUrl, headers=self.headers).json()
        try:
            id = response['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def get_group_from_name(self, groupName):
        """
        http://developer.okta.com/docs/api/resources/groups.html#search-groups
        :param groupName: name of group you want to get
        :return: array of group objects that meet search criteria, if no group is found returns empty list
        """
        parameters = dict()
        parameters['q'] = groupName
        response = requests.get(self.endpointUrl, params=parameters, headers=self.headers).json()
        if len(response) == 0:
            return response
        try:
            id = response[0]['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def add_group(self, profile):
        """
        http://developer.okta.com/docs/api/resources/groups.html#add-group
        :param profile: group profile object (https://developer.okta.com/docs/api/resources/groups.html#profile-object)
        :return: group object
        """
        body = dict()
        body['profile'] = profile
        response = requests.post(self.endpointUrl, headers=self.headers, json=body)
        try:
            response['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    # need to implement other parameters
    def list_group_membership(self, groupId, limit=1000):
        """
        http://developer.okta.com/docs/api/resources/groups.html#list-group-members
        :param groupId: unique ID of the group you want members for
        :return: a list of User objects
        """
        getUrl = self.endpointUrl + '/' + groupId + '/users?limit=' + str(limit)
        response = requests.get(getUrl, headers=self.headers).json()
        size = len(response)
        if size == 0:
            return response
        elif size == limit:
            result = []
            result.extend(response)
            while size == limit:
                id = response[size-1]['id']
                newUrl = getUrl + '&after=' + id
                response = requests.get(newUrl, headers=self.headers).json()
                result.extend(response)
                size = len(response)
            return result
        try:
            id = response[0]['id']
            return response
        except KeyError:
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])

    def add_user_to_group(self, userId, groupId):
        """
        http://developer.okta.com/docs/api/resources/groups.html#add-user-to-group
        :param userId: unique id of the user
        :param groupId: unique id of the group
        :return: return None if operation was successful, else raise error
        """
        putUrl = self.endpointUrl + '/' + groupId + '/users/' + userId
        try:
            response = requests.put(putUrl, headers=self.headers).json()
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        except ValueError:
            return None

    def delete_user_from_group(self, userId, groupId):
        """
        http://developer.okta.com/docs/api/resources/groups.html#remove-user-from-group
        :param userId: unique id of the user
        :param groupId: unique id of the group
        :return: return None if operation was successful, else raise error
        """
        deleteUrl = self.endpointUrl + '/' + groupId + '/users/' + userId
        try:
            response = requests.delete(deleteUrl, headers=self.headers).json()
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        except ValueError:
            return None