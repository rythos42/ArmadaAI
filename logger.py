import time


class Logger:
    ai_log_file = None
    tabs = 0
    is_writing_log = False

    def set_writing_log(self, writing_log):
        self.is_writing_log = writing_log

    def increment_tabs(self):
        self.tabs = self.tabs + 1

    def decrement_tabs(self):
        self.tabs = self.tabs - 1

    def write(self, message):
        if(not self.is_writing_log):
            return

        if(self.ai_log_file == None):
            self.ai_log_file = open("ai.log", "w")
            self.start_time = time.time()

        current_tabs = "".rjust(self.tabs, "\t")
        self.ai_log_file.write(f"{current_tabs}[{time.asctime()}] {message}\n")
