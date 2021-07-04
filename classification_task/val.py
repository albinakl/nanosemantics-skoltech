from sklearn.metrics import accuracy_score
import torch
import numpy as np
import torch.nn as nn
from torch.utils.data import DataLoader
import librosa
import soundfile as sf

from CNN_BLSTM_SELF_ATTN import CNN_BLSTM_SELF_ATTN
from wav_to_mel import Wav_to_mel

path = '/mnt/ssd/skoltech/nada/logs_Nina/TTS1.pth'
pth_to_wav = 'albina_2.wav'

class Val():
    def __init__(self):

        self.model = CNN_BLSTM_SELF_ATTN(input_size=128, cnn_filter_size=3, num_layers_lstm=2,
                                         num_heads_self_attn=16, hidden_size_lstm=64, num_emotion_class=6,
                                         num_gender_class=2, num_age_class=3)
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def predict(self, path_to_wav = pth_to_wav):
        spectrogram = Wav_to_mel(path_to_wav).final_mels(scaling=True, padding=True, augmentation=False,
                                                         length_to_padd=1000)
        spectrogram = torch.Tensor(spectrogram)
        spectrogram = torch.unsqueeze(spectrogram, dim = 0)
        
        pred_gender, pred_age, pred_emotion = self.model(spectrogram)
        
        predictions_emotion = np.argmax(pred_emotion.detach().cpu().numpy(),axis=1)
        dict_emo = dict(np.load('dict_emo.npy',allow_pickle='TRUE').item())
        predictions_emotion = dict_emo[predictions_emotion[0]]
        
        
        predictions_gender = np.argmax(pred_gender.detach().cpu().numpy(),axis=1)
        print(predictions_gender)
        dict_gender = dict(np.load('dict_gender.npy',allow_pickle='TRUE').item())
        predictions_gender = dict_gender[predictions_gender[0]]
        
        predictions_age = np.argmax(pred_age.detach().cpu().numpy(),axis=1)
        dict_age = dict(np.load('dict_age.npy',allow_pickle='TRUE').item())
        predictions_age = dict_age[predictions_age[0]]
        
        return  predictions_gender, predictions_age, predictions_emotion