# **Finetuning Dia-1.6B version (https://github.com/stlohrey/dia-finetuning) for Indonesian Text to Speech**

This repository contains scripts and configurations to finetune a pretrained [Dia-1.6B](https://github.com/nari-labs/dia) model for Indonesian speech-to-text tasks.

## **Dataset Requirements**
You can use:

- Open-source datasets for the Indonesian language, such as [Common Voice](https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0), or explore more options via the [Hugging Face Audio Datasets (Bahasa Indonesia)](https://huggingface.co/datasets?modality=modality:audio&language=language:id&sort=downloads) and [SEACrowd (South East Asia Languages)](https://seacrowd.github.io/seacrowd-catalogue/#dataset).

- Your own custom dataset, as long as it is properly preprocessed.

All datasets must:

- Be in standard audio format (e.g., .wav, .mp3).

## **Prepare Dataset**

1. Prepare a dataset consisting of audio files (.wav / .mp3) along with their transcriptions.
2. Store all audio files in a well-structured folder.
3. Create a metadata file in CSV format with the following structure, use delimeter | :
    ```
    audio_path|transcription
    ```
4. Calculate text length and audio duration using the script `check_length.ipynb`.

    These values are important for estimating the `text_length` and `audio_length` parameters in config.json. Both parameters significantly affect VRAM consumption during training.

5. After obtaining the 95th percentile of text length and audio duration, update the corresponding parameters in config.json.

## **Finetuning**

Once the preprocessing and configuration steps are completed, you can start fine-tuning the model with the following command:
```bash
nohup python -m dia.finetune \
  --config ../config.json \
  --csv_path ../metadata.csv \
  --audio_root ..root/data \
  --hub_model nari-labs/Dia-1.6B \
  --run_name finetune-dia\
  --output_dir ../ft-combined-dataset-22072025 \
  > dia-finetuning.out &
```

## Convert result model .pth to .safetensors

Convert the fine-tuned model from .pth format to .safetensors format for stable and safer storage using the script `conversion.ipynb`.
