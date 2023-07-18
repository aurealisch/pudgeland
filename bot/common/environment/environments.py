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
from __future__ import annotations

__all__: typing.Sequence[str] = ("Environment",)

import typing


class Environment:
    __slots__: typing.Sequence[str] = (
        "gateway_bot_token",
        "gateway_bot_banner",
        "java_server_host",
        "java_server_port",
        "database_url",
        "api_host",
        "api_port",
        "by_hand_minimal",
        "by_hand_maximum",
        "default_mode_color",
        "error_mode_color",
        "success_mode_color",
    )

    def __init__(
        self,
        gateway_bot_token: str,
        gateway_bot_banner: str,
        java_server_host: str,
        java_server_port: int,
        database_url: str,
        api_host: str,
        api_port: int,
        by_hand_minimal: int,
        by_hand_maximum: int,
        default_mode_color: str,
        error_mode_color: str,
        success_mode_color: str,
    ) -> None:
        """
        Parameters
        ---------
        - `gateway_bot_token` : `str`
        - `gateway_bot_banner` : `str`
        - `java_server_host` : `str`
        - `java_server_port` : `int`
        - `database_url` : `str`
        - `api_host` : `str`
        - `api_port` : `int`
        - `by_hand_minimal` : `int`
        - `by_hand_maximum` : `int`
        - `default_mode_color` : `str`
        - `error_mode_color` : `str`
        - `success_mode_color` : `str`
        """
        self.gateway_bot_token = gateway_bot_token
        self.gateway_bot_banner = gateway_bot_banner
        self.java_server_host = java_server_host
        self.java_server_port = java_server_port
        self.database_url = database_url
        self.api_host = api_host
        self.api_port = api_port
        self.by_hand_minimal = by_hand_minimal
        self.by_hand_maximum = by_hand_maximum
        self.default_mode_color = default_mode_color
        self.error_mode_color = error_mode_color
        self.success_mode_color = success_mode_color
