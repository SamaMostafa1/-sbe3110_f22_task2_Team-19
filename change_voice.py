
import librosa
import soundfile as sf 


y,sr = librosa.load('all_systems_go.wav')
f=librosa.effects.pitch_shift(y,sr=sr,n_steps=6)


sf.write('out.wav',f,sr)
