class GeneralOktaException(Exception):
    """
    This class is for errors that could occur in SDK methods that do not generate an Okta error code.
    For example, searching for a user by email, if no user exists it returns empty list, instead of having function
    return an empty list we raise an error, but we want to have a specific error class for this instead of just raising a
    general exception. Basically we want better try except statements
    """
    def __init__(self, method, message):
        self.errorMethod = method
        self.errorMessage = message

    def __str__(self):
        return 'Method Called: ' + self.errorMethod + '; Error Message: ' + self.errorMessage