class OktaError(Exception):
    def __init__(self, code, summary):
        self.errorCode = code
        self.errorSummary = summary

    def __str__(self):
        return 'Error Code: ' + self.errorCode + '; Error Summary: ' + self.errorSummary