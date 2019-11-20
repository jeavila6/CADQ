import threading
import time
import tempfile


def format_seconds(seconds):
    """Return formatted string hh:mm:ss.sss from seconds in float."""
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return '{:02.0f}:{:02.0f}:{:06.3f}'.format(hours, minutes, seconds)


def format_annotation(duration, start_time, end_time, rating):
    """Return tab-delimited: tier, duration, start_time, end_time, rating."""
    return f'rating\t{format_seconds(duration)}\t{format_seconds(start_time)}\t{format_seconds(end_time)}\t{rating}'


class SerialWriter(threading.Thread):

    def __init__(self, stream):
        super().__init__(daemon=True)
        self.stream = stream
        self.temp_file = tempfile.TemporaryFile(mode='w+')
        self.active = True

        # delay in seconds (50ms)
        self.delay = 0.05

    def run(self):
        """Write ratings to temporarily file until stopped."""
        start_time = 0.0
        base_time = time.time()
        rating = self.stream[0]

        while self.active:

            # write rating to file if it has changed, else sleep
            if rating != self.stream[0]:
                end_time = time.time() - base_time
                duration = end_time - start_time
                annotation = format_annotation(duration, start_time, end_time, rating)
                self.temp_file.write(annotation + '\n')
                start_time = end_time + self.delay
                rating = self.stream[0]
            else:
                time.sleep(self.delay)

        # write last rating to file before closing
        end_time = time.time() - base_time
        duration = end_time - start_time
        annotation = format_annotation(duration, start_time, end_time, rating)
        self.temp_file.write(annotation + '\n')

    def stop(self):
        """Stop writing ratings to temporary file and return its content."""
        self.active = False

        # wait for thread to stop writing to file
        while self.is_alive():
            pass

        self.temp_file.seek(0)
        return self.temp_file.read()
