# Overview

Generative AI and RAG (Retrieval Augmented Generation) applications for https://redhat-intel.devpost.com.

## Problem

Solving problem of the specific domain, like knowledge of the organizations or industries, is hard.

## Solution

### Training time

RAG for generating dataset for fine tuning

### Inference time

RAG for generating answer

## Components

1. Docs

- requirement.txt
- spec.txt
- authors.txt
- branches.txt

2. Dataset(RAFT)

- raw_dataset
- raft
- generated_dataset

3. Training

- recipe
- training_script
- model
- finetuned-model
- openvivo

4. Inference(RAG)

- rag
- retrieval_optimization
- serve

5. Benchmarking

- efficinecy_raft
- efficiency_rag
- effectiveness_model

6. Infra

- deploy.sh

7. Deliverables

- demo_video
- test_run_all
- screen_shot_openvino
- screen_shot_amx

## Requirement

### Environment and technology

- Red Hat OpenShift AI environment

- Intel OpenVINO

- Intel Xeon Processor AMX feature

### Deliverables

- Include a demonstration video of the Project made publicly visible on YouTube, Vimeo, Facebook Video, or Youku

  Video should be around three minutes

  Video should include footage that shows the Project functioning on the device for which it was built

- Include at least one test script to demonstrate the Project functionality

- Include a screenshot capturing the results of the test script showcasing the use of the Intel OpenVINO model server for inference.

- Include a screenshot showcasing the underlying platform supporting the Intel Xeon Processor AMX feature.

## Legal

Apache-2.0 licensed, refer to the LICENSE file in the top level directory.
