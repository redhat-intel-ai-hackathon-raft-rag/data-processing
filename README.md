### Web crawl for the web domains

Researching popular and trustable web sites and their quality of articles.

The factor of trustability:

- Review process of the web site

- PageRand or other algorithmically calculated scores

then write the domains within dataset/raw_dataset/spider_dataset_web.py

and run

````bash
python -m dataset.raw_dataset.spider_dataset_web
```

### Generating topics for each articles

```bash
python -m dataset.knowledge_graph.topic
````

### Saving the topics to text file

#### Notice: This is an application specific script

```bash
python -m dataset.knowledge_graph.medical_topic
```

### Collect Thesis or books for the topics

```bash
python -m dataset.raw_dataset.spider_dataset_book
```

then

```bash
python -m dataset.raw_dataset.pdf2xt
```

### Generating RAFT dataset

```bash
python -m dataset.raw_dataset.web_processing
```

```bash
python -m dataset.raw_dataset.pdftext2json
```

### Generating RAFT Dataset for training LLM

```bash
python -m dataset.upload_utility.processing2trainable_dataset
```

### Upload the datasets

./dataset/upload_utility/upload_dataset_book.sh

./dataset/upload_utility/upload_training_dataset_book.sh

./dataset/upload_utility/upload_dataset_web.sh

./dataset/upload_utility/upload_training_dataset_web.sh

### Budget

For feasible LLM application, at the minimum

5-50 $ when borrowing budgeted GPU to run vllm

-500$ when using Cohere or ChatGPT

more for other LLM provider's API
