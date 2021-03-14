# bukiBot
splatoon2ブキルーレット用discord bot(むる太郎)

https://bukibot.ml

## デプロイ
Heroku側でGitHub連携の設定後、masterブランチにpushするとHerokuにデプロイされます

DiscordのBot Tokenを環境変数として渡しているので、HerokuのSettings/Config Varsに`BOT_TOKEN`という名前でTokenを設定しておいてください

## ブランチ
- master
    - 作業用ブランチ
    - mkdocsの更新もこのブランチで作業する
- gh-pages
    - mkdocsコマンドで自動で更新される

## ローカルへの開発環境の構築

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
vim .env
```

## ローカルでbotの実行

```
source venv/bin/activate
python bot.py
```

テスト
```
python -m unittest
```

## mkdocs
venvファイルの読み込みとディレクトリ移動
```
source venv/bin/activate
cd docs
```

ローカルで実行
```
mkdocs serve
```

ビルド
```
mkdocs build
```

デプロイ
```
mkdocs gh-deploy
```

heroku
```
heroku login
heroku logs -a bukibot
heroku ps -a bukibot
```

## 初期セットアップ(このリポジトリをcloneして使う場合には不要)
```
mkdocs new docs
```

## 開発
`bot.py`は本番で動いている

`main.py`は開発用。GoogleTTSなどの実験用
