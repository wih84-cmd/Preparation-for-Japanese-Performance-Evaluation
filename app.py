import streamlit as st
import random

# [새 유인물 데이터 25개] 일본어 원문 중심 데이터
CARD_DATA = {
    "ありがとうございます": {"kr": "감사합니다", "pron": "아리가또~고자이마스"},
    "おめでとうございます": {"kr": "축하합니다", "pron": "오매때또~고자이마스"},
    "いかがですか": {"kr": "어떻습니까?", "pron": "이까가데스까"},
    "ごめんなさい": {"kr": "미안합니다", "pron": "고멘나사이"},
    "おひさしぶりです": {"kr": "오래간만입니다", "pron": "오히사시부리데스"},
    "やきゅうがすきです": {"kr": "야구를 좋아합니다", "pron": "야큐~가스끼데스"},
    "じょうずですね": {"kr": "잘하네요", "pron": "죠~즈데스네"},
    "どこですか": {"kr": "어디입니까?", "pron": "도꼬데스까"},
    "いつですか": {"kr": "언제입니까?", "pron": "이쯔데스까"},
    "おじゃまします": {"kr": "실례합니다 (방문할 때)", "pron": "오자마시마스"},
    "だいじょうぶです": {"kr": "괜찮습니다", "pron": "다이죠~부데스"},
    "いいですね": {"kr": "좋네요", "pron": "이~~데스네"},
    "そうですね": {"kr": "그렇군요", "pron": "소~데스네"},
    "ちょっとまってください": {"kr": "잠시만 기다려 주세요", "pron": "춋또말떼쿠다사이"},
    "こちらへどうぞ": {"kr": "이쪽으로 오세요", "pron": "고찌라에도~조"},
    "こちらこそ": {"kr": "저야말로", "pron": "고찌라코소"},
    "きをつけてね": {"kr": "조심하렴", "pron": "키오쯔케떼네"},
    "かんこくからきました": {"kr": "한국에서 왔습니다", "pron": "강코꾸까라키마시따"},
    "そんなことないですよ": {"kr": "그렇지 않아요", "pron": "손나코또나이데스요"},
    "いっしょにいく": {"kr": "같이 갈래", "pron": "잇쇼니이꾸"},
    "がんばって": {"kr": "힘내라", "pron": "강발떼"},
    "たかいですね": {"kr": "비싸네요", "pron": "타까이데스네"},
    "やすいですね": {"kr": "싸네요", "pron": "야시이데스네"},
    "どこにありますか": {"kr": "어디에 있습니까?", "pron": "도꼬니아리마스까"},
    "かんこくじんです": {"kr": "한국인입니다", "pron": "강코꾸진데스"}
}

st.set_page_config(page_title="일본어 우선 단어 카드", page_icon="🇯🇵", layout="centered")

st.title("🇯🇵 일본어 우선형 단어 카드 🇯🇵")
st.caption("일본어 표현을 먼저 보고 뜻과 발음을 머릿속으로 떠올린 뒤 확인해보세요!")

# --- 세션 초기화 ---
if "card_keys" not in st.session_state:
    st.session_state.card_keys = list(CARD_DATA.keys())
    st.session_state.index = 0
    st.session_state.show_answer = False

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
current_jp = st.session_state.card_keys[current_idx]
card_info = CARD_DATA[current_jp]

# --- 상단 진행 상황 표시 ---
st.progress((current_idx) / total_cards)
st.write(f"카드 번호: **{current_idx + 1} / {total_cards}**")

st.markdown("---")

# 🇯🇵 일본어 원문을 커다랗게 먼저 표시
st.markdown(f"<h3 style='text-align: center; color: #555;'>🇯🇵 일본어 표현</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: #1E88E5;'>{current_jp}</h1>", unsafe_allow_html=True)

st.markdown("---")

# 🇰🇷 한국어 뜻 및 발음 공개 영역
if st.session_state.show_answer:
    st.markdown(f"<h4 style='text-align: center; color: #2E7D32;'>🇰🇷 한국어 뜻: <b>{card_info['kr']}</b></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: #6A1B9A;'>🔊 발음: <b>{card_info['pron']}</b></h4>", unsafe_allow_html=True)
else:
    st.info("💡 카드를 뒤집어서 한국어 뜻과 발음을 확인해보세요!")

st.markdown("---")

# --- 조작 버튼 구역 ---
col1, col2 = st.columns(2)

with col1:
    if not st.session_state.show_answer:
        if st.button("👁️ 뜻·발음 보기", use_container_width=True, type="primary"):
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

# 이전 카드로 돌아가기 버튼
if current_idx > 0:
    if st.button("⬅️ 이전 카드"):
        st.session_state.index -= 1
        st.session_state.show_answer = False
        st.rerun()
