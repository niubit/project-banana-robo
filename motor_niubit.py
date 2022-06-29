# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""GPIO Controller for L298"""
import RPi.GPIO as GPIO
import time


# Right (BCM)
RIGHT_IN1 = 27
RIGHT_IN2 = 22
# Left (BCM)
LEFT_IN3 = 24
LEFT_IN4 = 23

FRECUENCY = 20

PINS = {"L": {"IN1": LEFT_IN3, "IN2": LEFT_IN4},
        "R": {"IN1": RIGHT_IN1, "IN2": RIGHT_IN2}}


class MotorController(object):
    """GPIO Controller for L298."""

    def __init__(self):
        super(MotorController, self).__init__()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RIGHT_IN1, GPIO.OUT)
        GPIO.setup(RIGHT_IN2, GPIO.OUT)
        GPIO.setup(LEFT_IN3, GPIO.OUT)
        GPIO.setup(LEFT_IN4, GPIO.OUT)
        self.in1 = GPIO.PWM(RIGHT_IN1, FRECUENCY)
        self.in2 = GPIO.PWM(RIGHT_IN2, FRECUENCY)
        self.in3 = GPIO.PWM(LEFT_IN3, FRECUENCY)
        self.in4 = GPIO.PWM(LEFT_IN4, FRECUENCY)

    def __del__(self):
        self.stop()
        self.cleanup()

    def stop(self):
        self.in1.stop()
        self.in2.stop()
        self.in3.stop()
        self.in4.stop()

    def forward(self, duration=None):
        self.in1.start(100)
        self.in2.stop()
        self.in3.start(100)
        self.in4.stop()
        if duration:
            time.sleep(duration)

    def reverse(self, duration=None):
        self.in2.start(100)
        self.in1.stop()
        self.in4.start(100)
        self.in3.stop()
        if duration:
            time.sleep(duration)

    def turn_l(self, radius=0, duration=None):
        if radius > 0:
            self.in1.start(100)
            self.in2.stop()
            self.in3.start(radius)
            self.in4.stop()
        else:
            self.in1.start(100)
            self.in2.stop()
            self.in4.start(100)
            self.in3.stop()
        if duration:
            time.sleep(duration)

    def turn_r(self, radius=0, duration=None):
        if radius > 0:
            self.in1.start(radius)
            self.in2.stop()
            self.in3.start(100)
            self.in4.stop()
        else:
            self.in2.start(100)
            self.in1.stop()
            self.in3.start(100)
            self.in4.stop()
        if duration:
            time.sleep(duration)

    def cleanup(self):
        GPIO.cleanup()
