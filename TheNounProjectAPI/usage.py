
from TheNounProjectAPI.core import Core
from TheNounProjectAPI.call import Call
from TheNounProjectAPI.models import UsageModel

class Usage(Core):
    @Call.usage
    def get_usage(self) -> UsageModel:
        """
        Fetches current oauth usage and limits.

        :returns: UsageModel object.
        :rtype: UsageModel
        """
        return self._prepare_url(f"{self._base_url}/oauth/usage")
