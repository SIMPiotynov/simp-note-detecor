from mido import MidiFile, MetaMessage, tick2second, tempo2bpm
import midi_tab
import json

def number_to_letter(number: int):
    find_key = '';
    for key, val in midi_tab.midi_tab.items():
        if number == val:
            find_key = key
            break
    return find_key

def convert_and_save(file_to_convert: str):
    mid = MidiFile(file_to_convert)
    retrun_list = []
    tmp = mid.tracks[0][0].tempo
    tpb = mid.ticks_per_beat

    notes = []
    times = []

    for t in mid.tracks[0]:
        time = tick2second(t.time, tpb, tmp)
        if time == "":
            time = 0
        if type(t) != MetaMessage:
            if t.channel == 0:
                note = "NOTE_SILENT"
                if t.type == 'note_on':
                    note = "NOTE_{}".format(number_to_letter(t.note))
            dic = {
                'note': note,
                'time': time
            }
            notes.append(note)
            times.append(str(time))

            retrun_list.append(dic)
    
    with open('notes', 'w') as nf:
        notes_str = """
            {}    
----------------------------------------------
            {}
        """.format(
            ",".join(notes),
            ",".join(times)
        )
        nf.write(notes_str)
            
    return json.dumps(retrun_list)


def do_convert(file_to_convert: str, with_note: True):
    mid = MidiFile(file_to_convert)
    return_dic = {"bpm": 120, "data": []}
    tmp = mid.tracks[0][0].tempo
    tpb = mid.ticks_per_beat
    bpm = tempo2bpm(tmp)
    return_dic["bpm"] = int(bpm)

    notes = []
    times = []

    for t in mid.tracks[0]:
        time = tick2second(t.time, tpb, tmp)
        if time == "":
            time = 0
        if type(t) != MetaMessage:
            if t.channel == 0:
                if with_note:
                    note = "NOTE_SILENT"
                else:
                    note = 'p'
                if t.type == 'note_on':
                    if with_note:
                        note = "NOTE_{}".format(number_to_letter(t.note))
                    else:
                        note = number_to_letter(t.note)
            dic = {
                'note': note,
                'time': t.time
            }
            notes.append(note)
            times.append(str(time))

            return_dic['data'].append(dic)
            
    return json.dumps(return_dic)


def midi_to_rtttl(midi_file: str):
    notes_json = json.loads(do_convert(midi_tab, False))
    # d= durée d'une note par defaut
    # o= numéro d'octave par defaut
    # b= tempo (batement/minute bpm)
    song_str = 'Son: d=4,o=5,b={}:'.format(notes_json['bpm'])
    for i in notes_json['data']:
        note = i['note']
        time = i['time']
        if len(note) > 1 and note[1] == 'S':
            note_list = note.split('S')
            note = '{}#{}'.format(note_list[0], note_list[1])
        elif note == 'p':
            time = 4
        format_note = "{0}{1}".format(time, note.lower())
        song_str += ' {},'.format(format_note)
    song_str += ' 1p'
    print(song_str)