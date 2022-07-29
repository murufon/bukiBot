# bukiBot
splatoon2ブキルーレット用discord bot(むる太郎)

https://bukibot.ml

## デプロイ
Heroku側でGitHub連携の設定後、masterブランチにpushするとHerokuにデプロイされます

DiscordのBot Tokenを環境変数として渡しているので、HerokuのSettings/Config Varsに`DISCORDBOT_TOKEN`という名前でTokenを設定しておいてください

## ブランチ
- master
    - 作業用ブランチ
    - mkdocsの更新もこのブランチで作業する
- gh-pages
    - mkdocsコマンドで自動で更新される

## ローカルへの開発環境の構築

```
cp .env.sample .env
vim .env
docker-compose up -d
docker-compose exec bot bash
python manage.py migrate
python manage.py createsuperuser
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
ディレクトリ移動
```
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

## 開発
`bot.py`は本番で動いている
