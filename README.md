# **Finetuning Dia-1.6B Text to Speech**

This repository contains scripts and configurations to finetune a pretrained [Dia-1.6B](https://github.com/nari-labs/dia) model for Indonesian text-to-speech tasks.

This repository provides **two different finetuning approaches** for Dia-1.6B. Choose the one that best fits your use case.

[`finetuning/dia-finetuning-mesolitica`](finetuning/dia-finetuning-mesolitica/)

[`finetuning/dia-finetuning-stlohrey`](finetuning/dia-finetuning-stlohrey/)

This repository also includes a production-ready API implementation for serving the finetuned Dia-1.6B TTS model with voice cloning capabilities.

 [`deployment`](deployment/tts-api/)