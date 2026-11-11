import streamlit as st
import random

# [새 유인물 데이터 25개] 단어 카드용 데이터
CARD_DATA = {
    "감사합니다": {"jp": "ありがとうございます", "pron": "아리가또~고자이마스"},
    "축하합니다": {"jp": "おめでとうございます", "pron": "오매때또~고자이마스"},
    "어떻습니까?": {"jp": "いかがですか", "pron": "이까가데스까"},
    "미안합니다": {"jp": "ごめんなさい", "pron": "고멘나사이"},
    "오래간만입니다": {"jp": "おひさしぶりです", "pron": "오히사시부리데스"},
    "야구를 좋아합니다": {"jp": "やきゅうがすきです", "pron": "야큐~가스끼데스"},
    "잘하네요": {"jp": "じょうずですね", "pron": "죠~즈데스네"},
    "어디입니까?": {"jp": "どこですか", "pron": "도꼬데스까"},
    "언제입니까?": {"jp": "いつですか", "pron": "이쯔데스까"},
    "실례합니다 (방문할 때)": {"jp": "おじゃまします", "pron": "오자마시마스"},
    "괜찮습니다": {"jp": "だいじょうぶです", "pron": "다이죠~부데스"},
    "좋네요": {"jp": "いいですね", "pron": "이~~데스네"},
    "그렇군요": {"jp": "そうですね", "pron": "소~데스네"},
    "잠시만 기다려 주세요": {"jp": "ちょっとまってください", "pron": "춋또말떼쿠다사이"},
    "이쪽으로 오세요": {"jp": "こちらへどうぞ", "pron": "고찌라에도~조"},
    "저야말로": {"jp": "こちらこそ", "pron": "고찌라코소"},
    "조심하렴": {"jp": "きをつけてね", "pron": "키오쯔케떼네"},
    "한국에서 왔습니다": {"jp": "かんこくからきました", "pron": "강코꾸까라키마시따"},
    "그렇지 않아요": {"jp": "そんなことないですよ", "pron": "손나코또나이데스요"},
    "같이 갈래": {"jp": "いっしょにいく", "pron": "잇쇼니이꾸"},
    "힘내라": {"jp": "がんばって", "pron": "강발떼"},
    "비싸네요": {"jp": "たかいですね", "pron": "타까이데스네"},
    "싸네요": {"jp": "やすいですね", "pron": "야시이데스네"},
    "어디에 있습니까?": {"jp": "どこにありますか", "pron": "도꼬니아리마스까"},
    "한국인입니다": {"jp": "かんこくじんです", "pron": "강코꾸진데스"}
}

st.set_page_config(page_title="일본어 단어 카드", page_icon="📖", layout="centered")

st.title("📖 일본어 수행평가 단어 카드 📖")
st.caption("뜻을 보고 머릿속으로 일본어를 떠올린 뒤, 버튼을 눌러 발음과 원문을 확인하세요!")

# --- 세션 초기화 ---
if "card_keys" not in st.session_state:
    st.session_state.card_keys = list(CARD_DATA.keys())
    # 랜덤으로 보고 싶다면 아래 주석을 해제하세요 (순서대로 보려면 유지)
    # random.shuffle(st.session_state.card_keys)
    st.session_state.index = 0
    st.session_state.show_answer = False

# 카드 순서 제어 변수
total_cards = len(st.session_state.card_keys)
current_idx = st.session_state.index

# 모든 카드를 다 봤을 때
if current_idx >= total_cards:
    st.balloons()
    st.success("🎉 모든 단어 카드를 다 확인했습니다! 수고하셨습니다!")
    if st.button("처음부터 다시 보기 🔄", type="primary"):
        st.session_state.index = 0
        st.session_state.show_answer = False
        random.shuffle(st.session_state.card_keys)
        st.rerun()
    st.stop()

# 현재 카드 데이터 가져오기
current_korean = st.session_state.card_keys[current_idx]
card_info = CARD_DATA[current_korean]

# --- 상단 진행 상황 표시 ---
st.progress((current_idx) / total_cards)
st.write(f"카드 번호: **{current_idx + 1} / {total_cards}**")

# --- 🃏 단어 카드 UI 박스 ---
st.markdown("---")

# 뜻(한국어)을 커다랗게 먼저 보여줌
st.markdown(f"<h3 style='text-align: center; color: #555;'>🇰🇷 한국어 뜻</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: #1E88E5;'>{current_korean}</h1>", unsafe_allow_html=True)

st.markdown("---")

# 정답(일본어 원문 및 발음) 공개 영역
if st.session_state.show_answer:
    st.markdown(f"<h4 style='text-align: center; color: #2E7D32;'>🇯🇵 일본어 원문: <b>{card_info['jp']}</b></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: #6A1B9A;'>🔊 발음: <b>{card_info['pron']}</b></h4>", unsafe_allow_html=True)
else:
    st.info("💡 카드를 뒤집어서 정답을 확인해보세요!")

st.markdown("---")

# --- 조작 버튼 구역 ---
col1, col2 = st.columns(2)

with col1:
    if not st.session_state.show_answer:
        if st.button("👁️ 정답 보기", use_container_width=True, type="primary"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        if st.button("↩️ 가리기", use_container_width=True):
            st.session_state.show_answer = False
            st.rerun()

with col2:
    if st.button("다음 카드 👉", use_container_width=True):
        st.session_state.index += 1
        st.session_state.show_answer = False
        st.rerun()

# 이전 카드로 돌아가기 버튼 (원할 경우)
if current_idx > 0:
    if st.button("⬅️ 이전 카드"):
        st.session_state.index -= 1
        st.session_state.show_answer = False
        st.rerun()
