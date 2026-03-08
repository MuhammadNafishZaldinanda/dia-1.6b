# Finetuning Dia-1.6B for Text-to-Speech

This repository provides scripts and configuration files for finetuning a pretrained Dia-1.6B model for Indonesian text-to-speech applications.

There are **two different finetuning approaches** available. You can choose the one that best suits your needs:

1. [`finetuning/dia-finetuning-mesolitica`](finetuning/dia-finetuning-mesolitica/)

    **Highlights:**
    - Advanced data pipeline with permutation and multipacking
    - Optimized GPU/VRAM utilization for large-scale training
    - Speaker-style conditioning via reference–target pairing
    - Suitable for large datasets and production-grade training

2. [`finetuning/dia-finetuning-stlohrey`](finetuning/dia-finetuning-stlohrey/)

    **Highlights:**
    - Simpler and more straightforward training workflow
    - Easier dataset preparation and configuration
    - Length-aware configuration using percentile statistics
    - Suitable for quick experimentation and smaller-scale finetuning

The repository also includes a production-ready API for deploying the finetuned Dia-1.6B TTS model, complete with voice cloning capabilities:

- [`deployment`](deployment/tts-api/)