from typing import NamedTuple, Optional

SlackMessage = NamedTuple("SlackMessage",
                          [("text", Optional[str]),
                           ("channel", Optional[str])])
