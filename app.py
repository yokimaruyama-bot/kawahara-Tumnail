import streamlit as st
import pandas as pd
import altair as alt

st.title("YouTube動画分析ダッシュボード")

# 1. データの読み込み（文字コードの問題を回避する設定）
try:
    # encoding='utf-8-sig' を使うことでExcel特有のゴミ（BOM）を除去します
    df = pd.read_csv('youtube_data.csv', encoding='utf-8-sig')
    
    # 全ての列名の前後から余計なスペースを削除する
    df.columns = df.columns.str.strip()

    # 2. 列名のチェック（デバッグ用：エラー時に役立ちます）
    expected_cols = ['投稿日', 'サムネイル', '再生数', 'クリック率']
    missing_cols = [c for c in expected_cols if c not in df.columns]

    if missing_cols:
        st.error(f"CSVの中に以下の列が見つかりません: {missing_cols}")
        st.info(f"現在認識されている列名: {list(df.columns)}")
        st.stop()

    # 3. 指標の選択
    y_axis_choice = st.selectbox(
        "表示する指標（縦軸）を選んでください：",
        ["再生数", "クリック率","平均再生率"]
    )

    # 4. グラフの作成
    chart = alt.Chart(df).mark_image(
        width=160,
        height=90
    ).encode(
        # :N にすることで日付の形式がバラバラでもとりあえず表示させます
        x=alt.X('投稿日:N', title='投稿日', sort='ascending'),
        y=alt.Y(f'{y_axis_choice}:Q', title=y_axis_choice),
        url='サムネイル',
        tooltip=['投稿日', '再生数', 'クリック率','平均再生率']
    ).properties(
        width=800,
        height=700
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

　　# 1. マウス選択（セレクション）の設定を追加
selection = alt.selection_point(on='mouseover', nearest=True, fields=['サムネイルURL'])

# 2. メインのグラフ（画像は少し小さめ）
base = alt.Chart(df).encode(
    x=alt.X('投稿日:N', title='投稿日', sort='ascending'),
    y=alt.Y(f'{y_axis_choice}:Q', title=y_axis_choice),
    url='サムネイルURL:N',
    tooltip=['投稿日', '再生数', 'クリック率', '平均再生率']
)

chart = base.mark_image(width=60, height=34).add_params(selection)

# 3. マウスを乗せた画像だけを大きく表示する「プレビュー」を定義
# 透明度を調整して、選択したものだけ浮き出させることも可能
preview = base.mark_image(width=400, height=225).transform_filter(selection)

# 4. グラフを縦に並べて表示（メイングラフの下にデカい画像が出る）
st.altair_chart(alt.vconcat(chart, preview), use_container_width=True)

except FileNotFoundError:
    st.error("youtube_data.csv が見つかりません。app.pyと同じフォルダに置いてください。")
except Exception as e:

    st.error(f"予期せぬエラーが発生しました: {e}")







