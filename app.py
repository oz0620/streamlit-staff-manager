# 職員管理システム - Streamlitアプリケーション
# バージョン: 1.0.0
# 最終更新: 2026-01-15

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ページ設定
st.set_page_config(
    page_title="職員管理システム",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# スタイル設定（総務系に相応しい落ち着いたプレミアムなデザイン）
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .header-container {
        padding: 2rem;
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Googleスプレッドシートへの接続
@st.cache_resource
def get_gspread_client():
    """Google Sheets APIクライアントを取得"""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    # secrets.tomlから認証情報を取得
    creds_dict = {
        "type": st.secrets["connections"]["gsheets"]["type"],
        "project_id": st.secrets["connections"]["gsheets"]["project_id"],
        "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
        "private_key": st.secrets["connections"]["gsheets"]["private_key"],
        "client_email": st.secrets["connections"]["gsheets"]["client_email"],
        "client_id": st.secrets["connections"]["gsheets"]["client_id"],
        "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
        "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
    }
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

@st.cache_data(ttl=600)
def load_data():
    """スプレッドシートからデータを読み込む"""
    try:
        client = get_gspread_client()
        # スプレッドシートIDを指定
        spreadsheet_id = "1s5sVs42ZsoTqM5AZsdsELnjtKVI27Sac7t_oGVxzbpQ"
        sheet = client.open_by_key(spreadsheet_id).sheet1  # 最初のシートを取得
        
        # データを取得してDataFrameに変換
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        st.error(f"データの読み込みに失敗しました: {e}")
        st.code(error_details, language="python")
        st.info("サービスアカウント: staff-manager-bot@myproject20260115.iam.gserviceaccount.com")
        st.info("このメールアドレスにスプレッドシートの編集権限を共有していますか？")
        return pd.DataFrame()

# データの読み込み
try:
    df = load_data()
    
    if df.empty:
        st.warning("データが空です。スプレッドシートの共有設定を確認してください。")
    else:
        # サイドバーメニュー
        st.sidebar.title("🏢 職員管理システム")
        menu = st.sidebar.radio("メニュー", ["🏠 ダッシュボード", "👥 職員一覧", "📂 書類管理", "⚙️ 設定"])

        if menu == "🏠 ダッシュボード":
            st.markdown('<div class="header-container"><h1>🏠 職員管理ダッシュボード</h1><p>組織の現状を一目で把握できます。</p></div>', unsafe_allow_html=True)
            
            # 統計メトリクス
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("総職員数", f"{len(df)} 名")
            with col2:
                # 職種別などの統計（データがある場合）
                if '役職' in df.columns:
                    unique_roles = df['役職'].nunique()
                    st.metric("役職種別", f"{unique_roles} 種")
                else:
                    st.metric("役職種別", "データなし")
            with col3:
                 st.metric("今月入職", "1 名") # サンプル
            with col4:
                 st.metric("書類更新が必要", "2 件") # サンプル

            # メインコンテンツ
            st.subheader("📊 職員構成")
            # ここにグラフなどを追加可能
            if '職種' in df.columns:
                role_counts = df['職種'].value_counts()
                st.bar_chart(role_counts)

        elif menu == "👥 職員一覧":
            st.markdown('<div class="header-container"><h1>👥 職員一覧</h1><p>全職員の情報を一元管理します。</p></div>', unsafe_allow_html=True)
            
            # 検索機能
            search_query = st.text_input("名前や職員IDで検索", "")
            
            if search_query:
                # 「氏名」列などがあることを想定してフィルター
                search_cols = ['氏名', 'フリガナ', '職員ＩＤ']
                available_cols = [c for c in search_cols if c in df.columns]
                if available_cols:
                    mask = df[available_cols].apply(lambda x: x.astype(str).str.contains(search_query, na=False)).any(axis=1)
                    filtered_df = df[mask]
                else:
                    filtered_df = df
            else:
                filtered_df = df

            # データテーブルの表示
            st.dataframe(filtered_df, use_container_width=True)

        elif menu == "📂 書類管理":
            st.markdown('<div class="header-container"><h1>📂 資格証・書類管理</h1><p>Googleドライブと連携した書類の写しを確認できます。</p></div>', unsafe_allow_html=True)
            
            # 職員を選択
            if '氏名' in df.columns:
                selected_staff = st.selectbox("職員を選択してください", df['氏名'].unique())
                staff_data = df[df['氏名'] == selected_staff].iloc[0]
                
                st.subheader(f"{selected_staff} さんの書類情報")
                
                # PDFリンクの表示（スプレッドシートの列名に合わせて調整）
                pdf_cols = [col for col in df.columns if 'PDF' in col or 'URL' in col]
                
                if pdf_cols:
                    cols = st.columns(len(pdf_cols))
                    for i, col_name in enumerate(pdf_cols):
                        with cols[i]:
                            url = staff_data[col_name]
                            if pd.notna(url) and str(url).startswith('http'):
                                st.markdown(f"**{col_name}**")
                                st.link_button("🔗 ファイルを開く", url)
                            else:
                                st.info(f"{col_name}: 未登録")
                else:
                    st.warning("書類リンクの列が見つかりません。")
            else:
                st.error("職員氏名の列が見つかりません。")

        elif menu == "⚙️ 設定":
            st.header("⚙️ システム設定")
            st.write("将来的な拡張（APIキーの変更、通知設定など）をここで行います。")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
    st.info("secrets.toml の設定や、スプレッドシートの共有設定を確認してください。")
    st.info("サービスアカウントのメールアドレス（staff-manager-bot@myproject20260115.iam.gserviceaccount.com）にスプレッドシートの編集権限を共有していますか？")
