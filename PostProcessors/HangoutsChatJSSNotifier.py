#!/usr/local/autopkg/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Graham Pugh
# Copyright 2019 Matthew Warren / haircut
#
# Based on the 'Slacker' PostProcessor by Graham R Pugh
# https://grahamrpugh.com/2017/12/22/slack-for-autopkg-jssimporter.html
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import, print_function

import requests

from autopkglib import Processor, ProcessorError

# Set the webhook_url to the one provided by Hangouts Chat
# See https://developers.google.com/hangouts/chat/how-tos/webhooks
__all__ = ["HangoutsChatJSSNotifier"]

class HangoutsChatJSSNotifier(Processor):
    description = ("Posts a Card notification to a Hangouts Chat room"
                   "via webhook based on output of a JSSImporter run.")
    input_variables = {
        "JSS_URL": {
            "required": False,
            "description": ("JSS_URL.")
        },
        "policy_category": {
            "required": False,
            "description": ("Policy Category.")
        },
        "category": {
            "required": False,
            "description": ("Package Category.")
        },
        "prod_name": {
            "required": False,
            "description": ("Title (NAME)")
        },
        "jss_changed_objects": {
            "required": False,
            "description": ("Dictionary of added or changed values.")
        },
        "jss_importer_summary_result": {
            "required": False,
            "description": ("Description of interesting results.")
        },
        "hangoutschatjss_webhook_url": {
            "required": False,
            "description": ("Hangouts Chat webhook url.")
        }
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):
        JSS_URL = self.env.get("JSS_URL")
        policy_category = self.env.get("policy_category")
        category = self.env.get("category")
        prod_name = self.env.get("prod_name")
        jss_changed_objects = self.env.get("jss_changed_objects")
        jss_importer_summary_result = self.env.get("jss_importer_summary_result")
        webhook_url = self.env.get("hangoutschatjss_webhook_url")

        if jss_changed_objects:
            jss_policy_name = "%s" % jss_importer_summary_result["data"]["Policy"]
            jss_policy_version = "%s" % jss_importer_summary_result["data"]["Version"]
            jss_uploaded_package = "%s" % jss_importer_summary_result["data"]["Package"]
            print("JSS address: %s" % JSS_URL)
            print("Title: %s" % prod_name)
            print("Policy: %s" % jss_policy_name)
            print("Version: %s" % jss_policy_version)
            print("Category: %s" % category)
            print("Policy Category: %s" % policy_category)
            print("Package: %s" % jss_uploaded_package)

            hangoutschat_data = {
                "cards": [
                    {
                        "header": {
                            "title": "New item added to JSS",
                            "subtitle": JSS_URL
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "keyValue": {
                                            "topLabel": "Title",
                                            "content": prod_name
                                        }
                                    },
                                    {
                                        "keyValue": {
                                            "topLabel": "Version",
                                            "content": jss_policy_version
                                        }
                                    },
                                    {
                                        "keyValue": {
                                            "topLabel": "Category",
                                            "content": category
                                        }
                                    },
                                    {
                                        "keyValue": {
                                            "topLabel": "Policy",
                                            "content": jss_policy_name
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }


            response = requests.post(webhook_url, json=hangoutschat_data)
            if response.status_code != 200:
                raise ValueError(
                                'Request to Hangouts Chat returned an error %s, the response is:\n%s'
                                % (response.status_code, response.text)
                                )


if __name__ == "__main__":
    processor = HangoutsChatJSSNotifier()
    processor.execute_shell()
