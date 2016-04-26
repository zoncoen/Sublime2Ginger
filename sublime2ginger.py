#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple grammar checker

This grammar checker will fix grammar mistakes using Ginger.
"""

import sublime
import sublime_plugin
import urllib.request, urllib.parse, urllib.error
import urllib.parse
from urllib.error import HTTPError
from urllib.error import URLError
import json
import threading

# Sublime Ginger thread
sublime_ginger_thread = None


class GingerGrammarCheker:
    def __init__(self, command):
        """Called when the instance is created.
        @param command sublime_plugin.TextCommand
        """
        region = command.view.sel()[0]
        if region.size() == 0:
            region = command.view.line(region)
        self.original_text = command.view.substr(region).lstrip()
        self.sublime_ginger_settings = sublime.load_settings("Sublime2Ginger.sublime-settings")
        self.auto_replace = self.sublime_ginger_settings.get("auto_replace")

    def __call__(self, command, edit):
        """Called when the instance is called as a function.
        @param commnd sublime_plugin.TextCommand
        """
        sublime.set_timeout(lambda: sublime.status_message("Ginger grammar checker is running..."), 100)
        # Grammar check with Ginger
        result, status = self.parse_result()
        if status:
            output = self.original_text + " -- Original" + "\n" + result + " -- Fixed"
            sublime.set_timeout(lambda: self.show_result(command, output), 100)
            if self.auto_replace:
                sublime.set_timeout(lambda: self.replace_text(command, result), 100)
        else:
            sublime.set_timeout(lambda: self.show_result(command, result), 100)

    def get_url(self):
        """Get a Ginger URL for checking grammar.
        @return URL
        """
        API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
        scheme = "http"
        netloc = "services.gingersoftware.com"
        path = "/Ginger/correct/json/GingerTheText"
        params = ""
        query = urllib.parse.urlencode([
            ("lang", "US"),
            ("clientVersion", "2.0"),
            ("apiKey", API_KEY),
            ("text", self.original_text)])
        fragment = ""
        return(urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment)))

    def get_result(self):
        """Get a result of checking grammar.
        @return result of grammar check by Ginger as JSON
        """
        url = self.get_url()
        # HTTP request
        try:
            response = urllib.request.urlopen(url)
        except HTTPError:
                raise
        except URLError:
                raise
        except IOError:
                raise
        # Parse HTTP response
        try:
            result = json.loads(response.read().decode('utf-8'))
        except ValueError:
            raise
        return(result)

    def parse_result(self):
        """Grammar check by Ginger.
        @return result of grammar check by Ginger
        @return status 1(Success)/0(Failure)
        """
        if len(self.original_text) == 0:
            return("No text :(", 0)
        elif len(self.original_text) > 600:
            sublime.status_message("You can't check more than 600 characters at a time.")
            return("", 0)
        fixed_text = self.original_text

        # Get JSON as result of grammar check
        try:
            results = self.get_result()
        except HTTPError as e:
            return("HTTP Error: " + e.code, 0)
        except URLError as e:
            return("URL Error: " + e.reason, 0)
        except IOError as xxx_todo_changeme:
            (errno, strerror) = xxx_todo_changeme.args
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
                fixed_text = fixed_text[:from_index - fixed_gap] + suggest + fixed_text[to_index - fixed_gap:]
                fixed_gap += to_index - from_index - len(suggest)
        return(fixed_text, 1)

    def show_result(self, command, text):
        """Output result into output panel.
        @param window sublime_plugin.WindowCommand
        @param output Strings to output.
        """
        command.view.run_command("___sublime2_ginger_output", {"text": text})

    def replace_text(self, command, text):
        """Replace the selection with suggested text.
        @param command sublime_plugin.TextCommand
        @param result Suggensed text.
        """
        command.view.run_command("___sublime2_ginger_replace", {"text": text})


class Sublime2GingerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Function to run Sublime2Ginger plugin.
        @param edit sublime.Edit
        """
        global sublime_ginger_thread
        grammer_checker = GingerGrammarCheker(self)
        if sublime_ginger_thread is not None and sublime_ginger_thread.isAlive() is True:
            sublime.status_message("Already grammar checker is running. Please wait.")
            return
        sublime_ginger_thread = threading.Thread(target=grammer_checker, args=(self, edit))
        sublime_ginger_thread.setDaemon(True)
        sublime_ginger_thread.start()

class __Sublime2GingerOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        """Function to replace text for Sublime2Ginger plugin.
        @param edit sublime.Edit
        """
        window = self.view.window()
        output_view = window.get_output_panel("textarea")
        window.run_command("show_panel", {"panel": "output.textarea"})
        output_view.set_read_only(False)
        output_view.insert(edit, output_view.size(), text)
        output_view.set_read_only(True)

class __Sublime2GingerReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        """Function to replace text for Sublime2Ginger plugin.
        @param edit sublime.Edit
        """
        region = self.view.sel()[0]
        if region.size() == 0:
            region = self.view.line(region)
        self.view.replace(edit, region, text)
