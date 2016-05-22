import RPi.GPIO as GPIO
import subprocess
import os

from Adafruit_Video_Looper.omxplayer import OMXPlayer


class OMXPlayerGPIO(OMXPlayer):
    def __init__(self, *args, **kwargs):
        super(OMXPlayerGPIO, self).__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.setup_interrupts()

    def play(self, movie, loop=False, vol=0):
        """Play the provided movied file, optionally looping it repeatedly."""
        self.stop(3)  # Up to 3 second delay to let the old player stop.
        # Assemble list of arguments.
        args = ['omxplayer']
        args.extend(['-o', self._sound])  # Add sound arguments.
        args.extend(self._extra_args)     # Add extra arguments from config.
        if vol is not 0:
            args.extend(['--vol', str(vol)])
        if loop:
            args.append('--loop')         # Add loop parameter if necessary.
        args.append(movie)                # Add movie file path.
        # Run omxplayer process and direct standard output to /dev/null.
        self._process = subprocess.Popen(args,
                                         stdout=open(os.devnull,'wb'),
                                         stdin=subprocess.PIPE, # opens the stdinput to
                                         close_fds=True, bufsize=0)

    def pause_video(self, channel):
        print("a freaking interruption occured")
        p = self._process
        if p is not None:
            try:
                p.stdin.write('p') # writes the p character to stdin in order to toggle pause in omxplayer
            except EnvironmentError as e:
                """ Do something smart """
                print "no pause dude"

    def stop_for_next(self, channel):
        self.stop();

    def setup_interrupts(self):
        print("setup interruption")
        # GPIO.add_event_detect(11, GPIO.FALLING, callback=self.pause_video, bouncetime=200)
        GPIO.add_event_detect(11, GPIO.FALLING, callback=self.stop_for_next, bouncetime=200)


def create_player(config):
    return OMXPlayerGPIO(config)