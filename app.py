import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="YouTube分析ダッシュボード", layout="wide")

st.title("YouTube動画分析ダッシュボード")

# 1. データの読み込み
DATA_SOURCE = 'youtube_data.csv' 

try:
    # データの読み込み
    df = pd.read_csv(DATA_SOURCE, encoding='utf-8-sig')
    
    # 列名の前後にある余計なスペースを削除
    df.columns = df.columns.str.strip()

    # 2. 列名のチェック
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
    selection = alt.selection_point(
        on='mouseover', 
        nearest=True, 
        fields=['サムネイル'], 
        empty=False
    )

    # B. グラフの基本設定（ここで途切れていました）
    base = alt.Chart(df).encode(
        x=alt.X('投稿日:N', title='投稿日', sort='ascending'),
        y=alt.Y(f'{y_axis_choice}:Q', title=y_axis_choice),
        url='サムネイル:N',
        tooltip=['投稿日', '再生数', 'クリック率', '平均再生率']
    )

    # C. メインのグラフ（通常のサムネイルサイズ）
    main_chart = base.mark_image(
        width=100, 
        height=56
    ).add_params(
        selection
    )

    # D. 拡大用のレイヤー（マウスが乗った時だけ大きく表示）
    upper_layer = base.mark_image(
        width=250, 
        height=140
    ).transform_filter(
        selection
    )

    # E. 2つのレイヤーを重ね合わせて表示
    final_chart = alt.layer(
        main_chart, 
        upper_layer
    ).properties(
        width=900,
        height=600,
        title="サムネイルにマウスを乗せると拡大表示されます"
    ).interactive()

    st.altair_chart(final_chart, use_container_width=True)

    st.info("💡 グラフ上でマウスホイールを動かすとズーム、ドラッグすると移動ができます。")

except FileNotFoundError:
    st.error(f"ファイル {DATA_SOURCE} が見つかりません。")
except Exception as e:
    st.error(f"予期せぬエラーが発生しました: {e}")
