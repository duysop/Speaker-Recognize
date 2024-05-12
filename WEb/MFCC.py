import soundfile as sf
import numpy as np
from scipy.io import wavfile
import scipy.fftpack as fft
from scipy.signal import get_window
import IPython.display as idp
def MFCC(TRAIN_PATH,file):
    audio, sample_rate, = sf.read(TRAIN_PATH + file)
    def normalize_audio(audio):
        audio = audio / np.max(np.abs(audio))
        return audio
    audio = normalize_audio(audio)
    def frame_audio(audio, FFT_size=2048, hop_size=10, sample_rate=44100):
        # hop_size in ms
        
        audio = np.pad(audio, int(FFT_size / 2), mode='reflect')
        frame_len = np.round(sample_rate * hop_size / 1000).astype(int)
        frame_num = int((len(audio) - FFT_size) / frame_len) + 1
        frames = np.zeros((frame_num,FFT_size))
        
        for n in range(frame_num):
            frames[n] = audio[n*frame_len:n*frame_len+FFT_size]
        
        return frames
    hop_size = 15 #ms
    FFT_size = 2048
    audio_framed = frame_audio(audio, FFT_size=FFT_size, hop_size=hop_size, sample_rate=sample_rate)
    window = get_window("hann", FFT_size, fftbins=True)
    audio_win = audio_framed * window
    audio_winT = np.transpose(audio_win)
    audio_fft = np.empty((int(1 + FFT_size // 2), audio_winT.shape[1]), dtype=np.complex64, order='F')

    for n in range(audio_fft.shape[1]):
        audio_fft[:, n] = fft.fft(audio_winT[:, n], axis=0)[:audio_fft.shape[0]]

    audio_fft = np.transpose(audio_fft)
    audio_power = np.square(np.abs(audio_fft))
    freq_min = 0
    freq_high = sample_rate / 2
    mel_filter_num = 10
    def freq_to_mel(freq):
        return 2595.0 * np.log10(1.0 + freq / 700.0)

    def met_to_freq(mels):
        return 700.0 * (10.0**(mels / 2595.0) - 1.0)
    def get_filter_points(fmin, fmax, mel_filter_num, FFT_size, sample_rate=44100):
        fmin_mel = freq_to_mel(fmin)
        fmax_mel = freq_to_mel(fmax)
        
        mels = np.linspace(fmin_mel, fmax_mel, num=mel_filter_num+2)
        freqs = met_to_freq(mels)
        
        return np.floor((FFT_size + 1) / sample_rate * freqs).astype(int), freqs
    filter_points, mel_freqs = get_filter_points(freq_min, freq_high, mel_filter_num, FFT_size, sample_rate=44100)
    def get_filters(filter_points, FFT_size):
        filters = np.zeros((len(filter_points)-2,int(FFT_size/2+1)))
        
        for n in range(len(filter_points)-2):
            filters[n, filter_points[n] : filter_points[n + 1]] = np.linspace(0, 1, filter_points[n + 1] - filter_points[n])
            filters[n, filter_points[n + 1] : filter_points[n + 2]] = np.linspace(1, 0, filter_points[n + 2] - filter_points[n + 1])
        
        return filters
    filters = get_filters(filter_points, FFT_size)
    enorm = 2.0 / (mel_freqs[2:mel_filter_num+2] - mel_freqs[:mel_filter_num])
    filters *= enorm[:, np.newaxis]
    audio_filtered = np.dot(filters, np.transpose(audio_power))
    audio_log = 10.0 * np.log10(audio_filtered)
    def dct(dct_filter_num, filter_len):
        basis = np.empty((dct_filter_num,filter_len))
        basis[0, :] = 1.0 / np.sqrt(filter_len)
        
        samples = np.arange(1, 2 * filter_len, 2) * np.pi / (2.0 * filter_len)

        for i in range(1, dct_filter_num):
            basis[i, :] = np.cos(i * samples) * np.sqrt(2.0 / filter_len)
            
        return basis
    dct_filter_num = 40

    dct_filters = dct(dct_filter_num, mel_filter_num)
    audio_log=np.nan_to_num(audio_log,posinf=0,neginf=0)

    cepstral_coefficents = np.dot(dct_filters, audio_log)
    return cepstral_coefficents