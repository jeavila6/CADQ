import subprocess


class AudioPlayer:
    def __init__(self):
        self.process = None

    def play(self, filename):
        """Play audio file."""

        # open SoX in a new process
        command = 'sox "' + filename + '" -d'
        self.process = subprocess.Popen(command)

    def stop(self):
        """Stop playback."""
        if self.process is not None:
            self.process.kill()

    def is_playing(self):
        """Return True if audio is playing."""
        return (self.process is not None) and (self.process.poll() is None)
