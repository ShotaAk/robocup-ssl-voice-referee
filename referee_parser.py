

class RefereeParser:
    TEAM_LIST = ["blue", "yellow"]
    def __init__(self):
        self._current_msg = None
        self._prev_command = None
        self._prev_stage = None
        self._prev_team_info = {"blue": None, "yellow": None}

    def set_referee_msg(self, referee_msg):
        if self._current_msg is not None:
            self._prev_command = self._extract_command(self._current_msg)
            self._prev_stage = self._extract_stage(self._current_msg)
            for team in self.TEAM_LIST:
                self._prev_team_info[team] = self._extract_team_info(self._current_msg, team)

        self._current_msg = referee_msg

    def has_new_command(self):
        return self._has_new_something(self._extract_command, self._prev_command)

    def has_new_stage(self):
        return self._has_new_something(self._extract_stage, self._prev_stage)

    def has_new_team_info(self, team):
        return self._has_new_something(self._extract_team_info, self._prev_team_info[team], team)

    def _has_new_something(self, extract_func, prev_value, team=None):
        if self._current_msg is None:
            return False

        extracted_value = None
        if team is not None:
            extracted_value = extract_func(self._current_msg, team)
        else:
            extracted_value = extract_func(self._current_msg)

        if extracted_value is not None and extracted_value != prev_value:
            return True
        return False

    def get_command(self):
        return self._extract_command(self._current_msg)

    def get_stage(self):
        return self._extract_stage(self._current_msg)

    def get_team_info(self, team):
        return self._extract_team_info(self._current_msg, team)

    def _extract_command(self, msg):
        if msg is None:
            return -1
        return msg.command

    def _extract_stage(self, msg):
        if msg is None:
            return -1
        return msg.stage

    def _extract_team_info(self, msg, team="blue"):
        if msg is None or team not in self.TEAM_LIST:
            return -1
        return getattr(msg, team)

