## get raw dataset
python -m dataset.raw_dataset.get_dataset
## generate dataset with raft
python -m dataset.raw_dataset.raft.raft --config dataset/raw_dataset/raft/configs.yaml &&
## train with llamafactory-cli
llamafactory-cli train finetune/train_lora/llama3_lora.yaml
## raw inference without rag
llamafactory-cli chat finetune/inference/llama3_lora.yaml