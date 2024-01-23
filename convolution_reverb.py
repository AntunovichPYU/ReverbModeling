import matplotlib.pyplot as plt
from scipy.signal import convolve
from in_out import read_wav, write_wav


# normalize signal to maximum amplitude
def normalize(ys, amp=1.0):
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)


if __name__ == '__main__':
    # reading files

    sample_in = 'phone'
    reverb_in = 'impulse'
    N = 200000

    sample = read_wav('input/' + sample_in + '.wav')
    reverb = read_wav('input/' + reverb_in + '.wav')

    sample_data = sample['data'][0:N]
    if sample_data.ndim == 2:
        sample_data = sample_data[:, 0]
    sample_data = normalize(sample_data)
    sample_rate = sample['rate']

    reverb_data = reverb['data'][0:N]
    if reverb_data.ndim == 2:
        reverb_data = reverb_data[:, 0]
    reverb_data = normalize(reverb_data)
    reverb_rate = reverb['rate']

    # values

    output_gain = 1
    dry = 1
    wet = 1

    # convolution

    output_signal = output_gain * normalize(convolve(sample_data * dry, reverb_data * wet, method='fft'))

    # write file

    write_wav('output/' + sample_in + '_conv', output_signal, sample_rate)
    new_signal = read_wav('output/' + sample_in + '_conv.wav')
    new_signal_data = normalize(new_signal['data'])
    new_signal_rate = new_signal['rate']

    # plot the results

    fig, axs = plt.subplots(nrows=3, ncols=1)
    fig.suptitle('Convolution reverb')
    axs[0].plot([i / sample_rate for i in range(len(sample_data))], sample_data)
    axs[0].set_ylabel('sample data')
    axs[1].plot([i / reverb_rate for i in range(len(reverb_data))], reverb_data)
    axs[1].set_ylabel('impulse')
    axs[2].plot([i / new_signal_rate for i in range(len(new_signal_data))], new_signal_data)
    axs[2].set_ylabel('reverb data')
    plt.xlabel('time (s)')
    plt.show()



