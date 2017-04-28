#!/usr/bin/python


class pca9685:

  def __init__(self, address):

    self.address = address
    self.freq = 0
    self.channels = [
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0},
      {"start":0, "end": 0}
      ]

    print "pca9685 initialized on address %s" % address

  def set_pwm_freq(self, freq):
    self.freq = freq
    print "PWM frequency set at %s" % freq

  def set_pwm(self, channel, start, end):
    self.channels[channel]["start"] = start
    self.channels[channel]["end"] = end
    print "PWM channel %s set to %s-%s" % (channel, start, end)
