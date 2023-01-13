from mido import MidiFile, MetaMessage, tick2second
import midi_tab
import json

def number_to_letter(number: int):
    find_key = '';
    for key, val in midi_tab.midi_tab.items():
        if number == val:
            find_key = key
            break
    return find_key

def do_convert(file_to_convert: str):
    mid = MidiFile(file_to_convert)
    retrun_list = []
    tmp = mid.tracks[0][0].tempo
    tpb = mid.ticks_per_beat
    for t in mid.tracks[0]:
        time = tick2second(t.time, tpb, tmp)
        if type(t) != MetaMessage:
            if t.channel == 0:
                note = "NOTE_SILENT"
                if t.type == 'note_on':
                    note = "NOTE_{}".format(number_to_letter(t.note))
            dic = {
                'note': note,
                'time': time
            }
            retrun_list.append(dic)
    return json.dumps(retrun_list)
