# bukiBot
splatoon2ブキルーレット用discord bot
https://bukibot.ml

## デプロイ
このリポジトリのmasterブランチにpushするとHerokuにデプロイされます

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
