#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple grammar checker

This grammar checker will fix grammar mistakes using Ginger.
"""

import sublime
import sublime_plugin
import urllib
import urlparse
from urllib2 import HTTPError
from urllib2 import URLError
import json
import threading


class GingerGrammarCheker:
    thread = None

    def __call__(self, command, edit, original_text):
        """
        """
        sublime.set_timeout(lambda: sublime.status_message("Ginger Grammar Checker is running..."), 100)
        # Grammar check with Ginger
        result, flag = self.parse_result(original_text)
        if flag:
            output = "Original: " + original_text + "\n" + "Fixed    : " + result
            sublime.set_timeout(lambda: self.show_result(command.view.window(), output), 100)
        else:
            print result
            sublime.set_timeout(lambda: self.show_result(command.view.window(), result), 100)

    def get_url(self, text):
        """Get a Ginger URL for checking grammar.
        @param text English text
        @return URL
        """
        API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"

        scheme = "http"
        netloc = "services.gingersoftware.com"
        path = "/Ginger/correct/json/GingerTheText"
        params = ""
        query = urllib.urlencode([
            ("lang", "US"),
            ("clientVersion", "2.0"),
            ("apiKey", API_KEY),
            ("text", text)])
        fragment = ""

        return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))

    def get_result(self, text):
        """Get a result of checking grammar.
        @param text English text
        @return result of grammar check by Ginger as JSON
        """
        url = self.get_url(text)

        try:
            response = urllib.urlopen(url)
        except HTTPError:
                raise
        except URLError:
                raise
        except IOError:
                raise

        try:
            result = json.loads(response.read().decode('utf-8'))
        except ValueError:
            raise

        return(result)

    def parse_result(self, original_text):
        """Grammar check by Ginger.
        @param text Original English text
        @return result of grammar check by Ginger
        @return status 1(Success)/0(Failure)
        """
        if len(original_text) > 600:
            sublime.status_message("You can't check more than 600 characters at a time.")
            return("", 0)
        fixed_text = original_text

        # Get JSON as result of grammar check
        try:
            results = self.get_result(original_text)
        except HTTPError as e:
            return("HTTP Error: " + e.code, 0)
        except URLError as e:
            return("URL Error: " + e.reason, 0)
        except IOError, (errno, strerror):
            return("I/O error (%s): %s (You need to connect to the Internet)." % (errno, strerror), 0)
        except ValueError:
            return("Value Error: Invalid server response (not including result of grammar check).", 0)

        # Correct grammar
        if(not results["LightGingerTheTextResult"]):
            return("Good English :)", 0)

        # Incorrect grammar
        fixed_gap = 0
        for result in results["LightGingerTheTextResult"]:
            if(result["Suggestions"]):
                from_index = result["From"]
                to_index = result["To"] + 1
                suggest = result["Suggestions"][0]["Text"]

                original_text = original_text[:from_index] + original_text[from_index:to_index] + original_text[to_index:]
                fixed_text = fixed_text[:from_index - fixed_gap] + suggest + fixed_text[to_index - fixed_gap:]

                fixed_gap += to_index - from_index - len(suggest)

        return(fixed_text, 1)

    def show_result(self, window, output):
        output_view = window.get_output_panel("textarea")
        window.run_command("show_panel", {"panel": "output.textarea"})

        output_view.set_read_only(False)
        edit = output_view.begin_edit()
        output_view.insert(edit, output_view.size(), output)
        output_view.end_edit(edit)
        output_view.set_read_only(True)

    def grammer_check(self, command, edit):
        sublime.status_message("start translate...")
        # Set region
        for region in command.view.sel():
            region_of_line = command.view.line(region)
        # Grammar check with Ginger
        original_text = command.view.substr(region_of_line).lstrip()
        if len(original_text) == 0:
            sublime.status_message("No text.")
            return
        if self.thread is not None and self.thread.isAlive() is True:
            sublime.status_message("Already run grammar check now. Please wait.")
            return
        thread = threading.Thread(target=self, args=(command, edit, original_text))
        thread.setDaemon(True)
        thread.start()


class Sublime2GingerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        grammer_checker = GingerGrammarCheker()
        grammer_checker.grammer_check(self, edit)
