# Akari
arXivの論文で、前日に投稿されたものを探してきて、短く要約して日本語に直して毎日slackに投稿してくれるbotを作ろうプロジェクト

## 使い方
* 現状は以下の様にコマンドを打って、必要なものをダウンロードしてからakari.pyの動作確認をお願いします
```
git clone https://github.com/Masao-Someki/akari.git
cd akari

# optionally you can use virtual environment.
#
# python -m venv venv (for windows users)
# python3 -m venv venv (for mac or linux users)
#
# venv/Scripts/activate.bat (for windows users)
# venv/bin/activate (for mac or linux users)
#
# pip install -r requirements.txt (for all users)
#

pip install -r requirements.txt (for windows users, not required if you built virtual environment)
pip3 install -r requirements.txt (for mac or linux users, not required if you built virtual environment)

python akari.py (for windows users)
python3 akari.py (for mac or linux users)
```
今は、 `./tmp` ディレクトリ以下に、前日アップデートされたarxivの記事を、ファイルごとにまとめていくという作業が行われます。 `Akari.utils.url_utils:get_field` に規定されている `fields` の部分を変更することで、自分の読みたい分野の論文を解析することができるようになります。また、将来的には `Akari.utils.user:USER` クラスを定義することで、ユーザーによって要約する論文の分野を変更することができるようにしようと思っています。

