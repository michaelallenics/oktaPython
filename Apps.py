import requests
import OktaError
import GeneralOktaException
import urllib

class AppsClient:

    """
    Functionality and documentation for the API calls comes from: https://developer.okta.com/docs/api/resources/apps.html

    Need to implement:
        -Everything
    """

    def __init__(self, orgUrl, apiKey):
        self.orgUrl = orgUrl
        self.apiKey = apiKey
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'SSWS ' + apiKey}
        self.endpointUrl = orgUrl + '/api/v1/apps'

    def delete_app(self, appId):
        """
        https://developer.okta.com/docs/api/resources/apps.html#delete-application
        :param appId: Unique ID of app to delete
        :return: None if it worked, raise error if failed
        """
        deleteUrl = self.endpointUrl + '/' + appId
        try:
            response = requests.delete(deleteUrl, headers=self.headers).json()
            code = response['errorCode']
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        except KeyError:
            raise GeneralOktaException.GeneralOktaException('delete_user', 'An unkown JSON Object has been returned')
        except ValueError:
            return None

    def list_apps(self, limit=20, filter=None):
        """
        https://developer.okta.com/docs/api/resources/apps.html#list-applications
        :param limit: Specifies the number of results for a page
        :param filter: Filters apps by status, user.id, group.id or credentials.signing.kid expression
        :return: List of app objects
        """
        if filter is None:
            getUrl = self.endpointUrl + '?limit=' + str(limit)
        else:
            getUrl = self.endpointUrl + '?filter=' + urllib.quote_plus(filter) + '&limit=' + str(limit)
        response = requests.get(getUrl, headers=self.headers).json()
        try:
            response['errorCode']
            raise OktaError.OktaError(response['errorCode'], response['errorSummary'])
        except TypeError:
            return response
        except KeyError:
            GeneralOktaException.GeneralOktaException('list_apps', 'Unknown JSON Object was returned')