from scipy.io import wavfile
import soundfile as sf


def read_wav(file_name):
    out_data = dict()
    samplerate, data = wavfile.read('data/' + file_name)
    out_data['rate'] = samplerate
    out_data['data'] = data
    out_data['N'] = len(data)
    return out_data


def write_wav(file_name, data, rate):
    sf.write('data/' + file_name + '.wav', data, rate)