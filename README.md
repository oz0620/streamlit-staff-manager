# 職員管理システム

Googleスプレッドシートと連携した職員情報管理システムです。

## 機能

- 📊 **ダッシュボード**: 職員数や統計情報の表示
- 👥 **職員一覧**: スプレッドシートのデータを表形式で表示、検索機能付き
- 📂 **書類管理**: Googleドライブ上のPDFリンクを管理
- ⚙️ **設定**: システム設定（将来の拡張用）

## セットアップ

### 1. 必要なライブラリのインストール

```bash
pip install streamlit pandas gspread oauth2client
```

### 2. Google Cloud サービスアカウントの設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Google Sheets API と Google Drive API を有効化
3. サービスアカウントを作成し、JSON鍵をダウンロード
4. スプレッドシートとドライブフォルダをサービスアカウントに共有

### 3. secrets.toml の設定

`.streamlit/secrets.toml` ファイルを作成し、以下の形式で認証情報を設定してください：

```toml
[connections.gsheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"
```

**重要**: `secrets.toml` は `.gitignore` に含まれているため、GitHubにはアップロードされません。

### 4. アプリの起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

## スプレッドシートの設定

`app.py` の72行目にあるスプレッドシートIDを、ご自身のスプレッドシートIDに変更してください：

```python
spreadsheet_id = "your-spreadsheet-id-here"
```

スプレッドシートIDは、スプレッドシートのURLから取得できます：
```
https://docs.google.com/spreadsheets/d/[ここがスプレッドシートID]/edit
```

## 技術スタック

- **フレームワーク**: Streamlit
- **データ連携**: gspread, oauth2client
- **データ処理**: pandas
- **認証**: Google Service Account

## ライセンス

MIT License
