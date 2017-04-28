#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import division
from RPiHTTPServer import RPiHTTPServer, RPiHTTPRequestHandler
#import Adafruit_PCA9685.PCA9685 as pca9685
from pca9685 import pca9685
import pystache
import os
import json

class WebHandler(RPiHTTPRequestHandler):

  # TODO: status should be set directly from interface to i2C
  status = {
    "freq": 50,
    "channels": [
      {"index":  0, "start": 0, "end": 0, "pulse": 0},
      {"index":  1, "start": 0, "end": 0, "pulse": 0},
      {"index":  2, "start": 0, "end": 0, "pulse": 0},
      {"index":  3, "start": 0, "end": 0, "pulse": 0},
      {"index":  4, "start": 0, "end": 0, "pulse": 0},
      {"index":  5, "start": 0, "end": 0, "pulse": 0},
      {"index":  6, "start": 0, "end": 0, "pulse": 0},
      {"index":  7, "start": 0, "end": 0, "pulse": 0},
      {"index":  8, "start": 0, "end": 0, "pulse": 0},
      {"index":  9, "start": 0, "end": 0, "pulse": 0},
      {"index": 10, "start": 0, "end": 0, "pulse": 0},
      {"index": 11, "start": 0, "end": 0, "pulse": 0},
      {"index": 12, "start": 0, "end": 0, "pulse": 0},
      {"index": 13, "start": 0, "end": 0, "pulse": 0},
      {"index": 14, "start": 0, "end": 0, "pulse": 0},
      {"index": 15, "start": 0, "end": 0, "pulse": 0}
    ]
  }

  def compute_pulses(self):
    for i in xrange(16):
      ch_start = self.status["channels"][i]["start"]
      ch_end = self.status["channels"][i]["end"]
      self.status["channels"][i]["pulse"] = round((ch_end - ch_start) / (4096 * self.status["freq"] ) * 1000, 2)
      print "Pulse %s length: %s" % (i, self.status["channels"][i]["pulse"])

  # GET /
  def default_response(self):
    self.compute_pulses()
    self.render_template()

  # POST /set
  def set_param(self):
    # TODO:
    # - handle errors / illegal params
    # - directly interface to i2C to have more control (set all, setup, off / on, etc..)

    # set freq
    if self.form.has_key('freq'):
      freq = int(self.form['freq'].value)
      if 10 <= freq <= 250:
        self.status["freq"] = freq
        self.server.pwm.set_pwm_freq(freq)

    # set start and end for pwm channels
    for i in xrange(16):
      ch_start = ch_end = 0

      if self.form.has_key("channel_%s_start" % i):
        ch_start = int(self.form["channel_%s_start" % i].value)
        if 0 <= ch_start <= 4095:
          self.status["channels"][i]["start"] = ch_start

      if self.form.has_key("channel_%s_end" % i):
        ch_end = int(self.form["channel_%s_end" % i].value)
        if 0 <= ch_end <= 4095:
          if ch_end < ch_start:
            ch_end = ch_start
          self.status["channels"][i]["end"] = ch_end

      self.server.pwm.set_pwm(i, self.status["channels"][i]["start"], self.status["channels"][i]["end"])

    self.compute_pulses()
    self.render_template()

  def render_template(self, template="home.html", tpl_vars={}):
    if not tpl_vars:
      tpl_vars = self.status

    if self.request_xhr:
      self.content_type = "application/json"
      self.content = json.dumps(tpl_vars)
    else:
      tpl = os.path.join(self.config.TEMPLATE_FOLDER, template)
      if os.path.isfile(tpl):
        tpl_content = open(tpl,"r").read()
        self.content = pystache.render(tpl_content, tpl_vars)
      else:
        self.give_404("Template %s missing" % template)


def main():

  # read configuration from json
  basedir = os.path.dirname(os.path.abspath(__file__))
  config_file = os.path.join(basedir,"config.json")

  # instantiate http server
  WebServer = RPiHTTPServer(config_file, WebHandler)

  # quick access to config params
  config = WebServer.server.config

  # instantiate and initialise pwm controller
  pwm = pca9685(address=int(config.I2C_ADDR,16))

  # assign variables to server
  WebServer.server.pwm = pwm
  WebServer.server.root_folder = basedir

  try:
    print "Server listening on http://%s:%s" % (config.SERVER_ADDRESS,config.SERVER_PORT)
    WebServer.serve_forever()
  except KeyboardInterrupt:
    pass
    # TODO: cleanup pwm status
    WebServer.server.server_close()


if __name__ == '__main__':

  main()
