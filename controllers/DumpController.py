import pylvtmod as md
import pylvtmod.helpers.obj as mdpt


class DumpController(mdpt.LiveLiftController):
    def tick(self, time, ticks):
        while self.has_requests():
            request: md.Request = self.pop_request()
            for destination in request.destinations:
                self.lifts[0].push_command(md.Command(move_to_floor=destination, make_exchange=True))

        while self.has_calls():
            call: md.Call = self.pop_call()
            self.lifts[0].push_command(md.Command(move_to_floor=call.floor, make_exchange=True,
                                                  load_flag=call.flag, call_sender_id=call.sender_id))
