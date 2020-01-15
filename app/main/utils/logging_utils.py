

class ApiLogger:

    def __init__(self, debug_id):
        self.debug_id = debug_id

    def log(self, msg):
        print('{} - {}'.format(self.debug_id, msg))
