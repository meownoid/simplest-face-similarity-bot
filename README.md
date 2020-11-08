# Simplest Face Similarity Bot

This is a simple telegram bot which tells you what celebrity you are similar to.

## Usage

Clone the repository.

```shell script
git clone https://github.com/meownoid/simplest-face-similarity-bot.git
cd simplest-face-similarity-bot
```

Install requirements. This step may take a while because
dlib library will be compiled from sources.

```shell script
pip install -r requirements.txt
```

Optionally change paths in the `config.py` and place your own photos to the photos folder.
Then run `prepare.py` to download two pretrained models and create photos embeddings.

```shell script
python prepare.py
```

Place your bot token in the `config.py`.

```python
TOKEN = '<TOKEN>'
```

Start the bot.

```shell script
python bot.py
```
