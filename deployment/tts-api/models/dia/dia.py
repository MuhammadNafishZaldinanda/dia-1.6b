from dia.model import Dia
import torch
import numpy as np
import config

class VoiceCloning:
    def __init__(self):
        compute_dtype = "float32" if config.HARDWARE == "cpu" else "float16"
        self.pipe = Dia.from_pretrained(config.MODEL_DIR, device=config.HARDWARE, compute_dtype=compute_dtype)

    def resampled_audio(self, output_waveform, speed_factor):
        sr = 44100
        speed_factor = float(speed_factor)
        if speed_factor != 1.0: 
            original_len = len(output_waveform)
            target_len = int(original_len / speed_factor)
            x_original = np.arange(original_len)
            x_resampled = np.linspace(0, original_len - 1, target_len)
            resampled_audio_np = np.interp(x_resampled, x_original, output_waveform)
            output_waveform = resampled_audio_np.astype(np.float32)
        return sr, output_waveform

    def predict(self, text):
        clone_from_text = "Mural kota Semarang. Sejarah kota Semarang dimulai sejak abad ke delapan masehi."
        clone_from_audio = config.AUD_REF
        speech = self.pipe.generate(clone_from_text + text, 
                                    audio_prompt=clone_from_audio, 
                                    use_torch_compile=True, 
                                    verbose=True, 
                                    cfg_scale=3.0,
                                    temperature=1.3,
                                    top_p=0.95,
                                    cfg_filter_top_k=35
                                    )
        sr, aud = self.resampled_audio(speech, speed_factor=config.SPEED_FACTOR)

        torch.cuda.empty_cache()

        return sr, aud