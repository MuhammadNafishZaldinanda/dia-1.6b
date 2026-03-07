# **Finetuning Dia-1.6B version (https://github.com/mesolitica/malaya-speech/tree/master/session/dia-tts) for Indonesian Text to Speech**

This repository contains scripts and configurations to finetune a pretrained [Dia-1.6B](https://github.com/nari-labs/dia) model for Indonesian speech-to-text tasks.

## **Dataset Requirements**
You can use:

- Open-source datasets for the Indonesian language, such as [Common Voice](https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0), or explore more options via the [Hugging Face Audio Datasets (Bahasa Indonesia)](https://huggingface.co/datasets?modality=modality:audio&language=language:id&sort=downloads) and [SEACrowd (South East Asia Languages)](https://seacrowd.github.io/seacrowd-catalogue/#dataset)

    - indspeech_news_tts
    - sindodusc
    - titml-idn
    - indspeech_teldialog_lvscr
    - medisco

- Your own custom dataset, as long as it is properly preprocessed.

All datasets must:

- Be in standard audio format (e.g., .wav, .mp3).

## **Prepare Dataset**

1. Prepare raw data

    The raw dataset consists of a folder containing audio files and a transcript metadata file. The transcript can be provided in CSV or TXT format with a | delimiter:

    ```
    audio_path|transcription
    ```
    This metadata is then converted into JSON format with an additional speaker field.
    Example:
    ```json
    {
    "audio_path": "../SPK00_F_0000.wav",
    "text": "Selamat pagi.",
    "speaker": "indspeech_news_tts_0"
    }
    ```

2. Convert audio format
    
    Convert audio files from `.wav` / `.mp3` into `.dac`. The Dia model requires `.dac` format both for training and for the multipacking process. During multipacking, the decoder length is calculated using the `.dac` representation to determine the appropriate sequence length. For convert audio to `.dac` use the script `convert_dac.py`:
    ```bash
    CUDA_VISIBLE_DEVICES=0python convert_dac.py --path "../folder_audio_path/wavs/*.wav"
    ```

3. Permutation

    Apply permutation to the dataset `(audio_path, text, speaker)` and save the output in Hugging Face dataset format. Permutation is performed within the same speaker ID only.
    
    The purpose is to augment the dataset through random concatenation, preventing the model from memorizing dataset order. This improves robustness and generalization, similar to data augmentation.

    For permutation use the script `permutation.py`. Output: a Hugging Face dataset stored in Parquet format.

    Each sample in the permuted dataset will be stored as a pair of (reference, target) within the same speaker, where the reference provides speaker style/context and the target provides the actual training objective.

    ```json
    {
    "reference_audio": "Ind050_F_S_C_appl_1319.wav",
    "reference_text": "Nggak bener.",
    "target_audio": "Ind050_F_S_C_appl_1285.wav",
    "target_text": "Matikan AC selama satu setengah jam."
    }
   ```

   - reference_audio / reference_text → provide speaker identity and context.
   - target_audio / target_text → provide the supervised training target.

4. Multipacking

    Combine several short audio samples into one sequence, so that the total length is closer to the target `max_len`. This reduces wasted padding and optimizes `VRAM usage`.
    
    For multipacking use the script `permutation.py`. Output: a JSON file containing lists of batch instances.
    ```json
    [[28, 29, 7, 24, 19, 2, 18, 27, 21],
    [20, 17, 23, 12, 10, 5],
    [22, 0, 8, 14, 13, 6],
    [11, 1, 26, 25, 4]]]
    ```

5. Training input

    The training process uses:
    
    - The permutation output → Hugging Face dataset (pairs reference and taget) in Parquet format.
    - The multipacking output → JSON file containing batch instance lists.

## **Finetuning**

## **Finetuning**

Once the preprocessing and configuration steps are completed, you can start fine-tuning the model with the following command:
```bash
bash finetune_dia_multipacking_v2.sh
```

## Convert result model .pth to .safetensors

Convert the fine-tuned model from .pth format to .safetensors format for stable and safer storage using the script `conversion.ipynb`.