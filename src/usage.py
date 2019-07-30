
from src.core import Core
from src.call import Call
from src.models import UsageModel

class Usage(Core):
    @Call.usage
    def get_usage(self) -> UsageModel:
        """
        Fetches current oauth usage and limits.

        :returns: Usage object.
        :rtype: Usage
        """
        return self._prepare_url(f"{self._base_url}/oauth/usage")
