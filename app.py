import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="YouTube分析ダッシュボード", layout="wide")

st.title("YouTube動画分析ダッシュボード")

# 1. データの読み込み
# CSVファイル名、またはウェブ公開したスプレッドシートのURLを入力してください
DATA_SOURCE = 'youtube_data.csv' 

try:
    # データの読み込み
    df = pd.read_csv(DATA_SOURCE, encoding='utf-8-sig')
    
    # 列名の前後にある余計なスペースを削除
    df.columns = df.columns.str.strip()

    # 2. 列名のチェック（「サムネイルURL」を「サムネイル」に変更済み）
    expected_cols = ['投稿日', 'サムネイル', '再生数', 'クリック率', '平均再生率']
    missing_cols = [c for c in expected_cols if c not in df.columns]

    if missing_cols:
        st.error(f"CSVの中に以下の列が見つかりません: {missing_cols}")
        st.info(f"現在認識されている列名: {list(df.columns)}")
        st.stop()

    # 3. 指標の選択（縦軸）
    y_axis_choice = st.selectbox(
        "表示する指標（縦軸）を選んでください：",
        ["再生数", "クリック率", "平均再生率"]
    )

    # --- グラフ作成：レイヤー方式（拡大画像が重なる設定） ---

    # A. マウスオーバーの判定設定
    # empty=Falseにすることで、マウスが乗っていない時は拡大画像を出さないようにします
    selection = alt.selection_point(
        on='mouseover', 
        nearest=True, 
        fields=['サムネイル'], 
        empty=False
    )

    # B. グラフの基本設定
    base = alt.Chart(df).encode(
        x=alt.X('投稿日:N', title='投稿日', sort='ascending'),
        

