# Embedding + FAISS

```bash
$ pip install -r requirements.txt
$ huggingface-cli login
$ python utils/save_model.py
$ streamlit run main.py
```

Blog: [한국어](https://denev6.github.io/projects/2025/03/24/retrieve-notice.html)

## Architecture

![overview](./utils/overview.png)

1. Crawl notices: [crawl.py](./utils/crawl.py)
2. Create database: [json2sqlite.py](./utils/json2sqlite.py)
3. Embed notices as vectors: [embed.py](./embed.py)
4. Test in the browser: [main.py](./main.py)
