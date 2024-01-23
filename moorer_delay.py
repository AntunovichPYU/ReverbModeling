import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from read_wav import read_wav, write_wav


def normalize(ys, amp=1.0):
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)


# all-pass filter
def allpass(input_signal, delay, gain):
    B = np.zeros(delay)
    B[0] = gain
    B[delay-1] = 1
    A = np.zeros(delay)
    A[0] = 1
    A[delay-1] = gain
    out = signal.lfilter(B, A, input_signal)
    return out


# low-pass comb filter
def comb_with_lp(input_signal, delay, g, g1):
    g2 = g*(1-g1)
    B = np.zeros(delay+1)
    B[delay-1] = 1
    B[delay] = -g1
    A = np.zeros(delay)
    A[0] = 1
    A[1] = -g1
    A[delay-1] = -g2
    out = signal.lfilter(B, A, input_signal)
    return out


# delay function
def delay(input_signal, delay, gain=1):
    out = np.concatenate((np.zeros(delay), input_signal))
    out = out * gain
    return out


if __name__ == '__main__':
    # read file

    sample_in = 'trumpet'
    N = 200000

    sample = read_wav('input/' + sample_in + '.wav')

    sample_data = sample['data'][0:N]
    if sample_data.ndim == 2:
        sample_data = sample_data[:, 0]
    sample_data = normalize(sample_data)
    sample_rate = sample['rate']

    # initial values

    delays = [2205, 2469, 2690, 2998, 3175, 3439]
    delays_early = [877, 1561, 1715, 1825, 3082, 3510]
    gains_early = [1.02, 0.818, 0.635, 0.719, 0.267, 0.242]
    g1_list = [0.41, 0.43, 0.45, 0.47, 0.48, 0.50]
    g = 0.9
    rev_to_er_delay = 1800
    allpass_delay = 286
    allpass_g = 0.7

    output_gain = 0.075
    dry = 1
    wet = 1

    early_reflections = np.zeros(sample_data.size)
    combs_out = np.zeros(sample_data.size)

    # algorythm

    for i in range(6):
        early_reflections = early_reflections + delay(sample_data, delays_early[i], gains_early[i])[:sample_data.size]

    for i in range(6):
        combs_out = combs_out + comb_with_lp(sample_data, delays[i], g, g1_list[i])

    reverb = allpass(combs_out, allpass_delay, allpass_g)

    early_reflections = np.concatenate((early_reflections, np.zeros(rev_to_er_delay)))

    reverb = delay(reverb, rev_to_er_delay)

    output_signal = (early_reflections + reverb)
    output_signal = output_gain * (output_signal * wet + np.concatenate((sample_data, np.zeros(rev_to_er_delay))) * dry)

    # write file

    write_wav('output/' + sample_in + '_moorer', output_signal, sample_rate)
    new_signal = read_wav('output/' + sample_in + '_moorer.wav')
    new_signal_data = normalize(new_signal['data'])
    new_signal_rate = new_signal['rate']

    # plot the results

    fig, axs = plt.subplots(nrows=2, ncols=1)
    fig.suptitle('Moorer algorythm reverb')
    axs[0].plot([i / sample_rate for i in range(len(sample_data))], sample_data)
    axs[0].set_ylabel('sample data')
    axs[1].plot([i / new_signal_rate for i in range(len(new_signal_data))], new_signal_data)
    axs[1].set_ylabel('reverb data')
    plt.xlabel('time (s)')
    plt.show()


