# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Configuration:
    def __init__(
        self,
        gateway_bot_banner: str,
        java_server_host: str,
        java_server_port: int,
        api_host: str,
        api_port: int,
        by_hand_minimal: int,
        by_hand_maximum: int,
    ) -> None:
        """
        Parameters
        ---------
        - `gateway_bot_banner` : `str`
        - `java_server_host` : `str`
        - `java_server_port` : `int`
        - `api_host` : `str`
        - `api_port` : `int`
        - `by_hand_minimal` : `int`
        - `by_hand_maximum` : `int`
        """
        self.gateway_bot_banner = gateway_bot_banner
        self.java_server_host = java_server_host
        self.java_server_port = java_server_port
        self.api_host = api_host
        self.api_port = api_port
        self.by_hand_minimal = by_hand_minimal
        self.by_hand_maximum = by_hand_maximum
