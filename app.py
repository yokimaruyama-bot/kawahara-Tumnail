import streamlit as st
import pandas as pd
import altair as alt

st.title("YouTube動画分析ダッシュボード")

# 1. データの読み込み
DATA_SOURCE = 'youtube_data.csv' 

try:
    df = pd.read_csv(DATA_SOURCE, encoding='utf-8-sig')
    df.columns = df.columns.str.strip()

    # 2. 列名のチェック
    expected_cols = ['投稿日', 'サムネイル', '再生数', 'クリック率', '平均再生率']
    if any(c not in df.columns for c in expected_cols):
        st.error(f"CSVの列名を確認してください。必要列: {expected_cols}")
        st.stop()

    # 3. 指標の選択
    y_axis_choice = st.selectbox(
        "表示する指標（縦軸）を選んでください：",
        ["再生数", "クリック率", "平均再生率"]
    )

 # --- マウスオーバー時のみ表示する調整 ---

    # A. マウスが乗っている場所を特定する設定（empty=False にすることで、何も選んでいない時は「空」にする）
    selection = alt.selection_point(on='mouseover', nearest=True, fields=['サムネイルURL'], empty=False)

    # B. 共通の土台設定
    base = alt.Chart(df).encode(
        x=alt.X('投稿日:N', title='投稿日', sort='ascending'),
        y=alt.Y(f'{y_axis_choice}:Q', title=y_axis_choice),
        url='サムネイルURL:N',
        tooltip=['投稿日', '再生数', 'クリック率', '平均再生率']
    )

    # C. メインのグラフ
    main_chart = base.mark_image(
        width=100, 
        height=56
    ).add_params(
        selection
    ).properties(
        width=800,
        height=450
    )

    # D. 下に表示される拡大プレビュー
    # opacity（不透明度）を、selectionが有効な時は1（100%）、無効な時は0（透明）にします
    preview = base.mark_image(
        width=400, 
        height=225
    ).encode(
        opacity=alt.condition(selection, alt.value(1), alt.value(0))
    ).properties(
        title="選択中のサムネイル拡大（マウスを乗せると表示されます）"
    )

    # E. グラフを結合して表示
    st.altair_chart(alt.vconcat(main_chart, preview), use_container_width=True)


except Exception as e:
    st.error(f"予期せぬエラーが発生しました: {e}")

