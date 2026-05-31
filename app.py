import streamlit as st
import random

# [데이터 최적화] 8143.jpg 프린트물 25개 전체 문항 완벽 반영 및 복수 정답 지정
QUIZ_DATA = {
    "안녕하세요 (아침 인사)": ["오하요-고자이마스", "오하요고자이마스", "오하요 고자이마스"],
    "안녕하세요 (낮 인사)": ["곤니찌와", "곤니치와"],
    "안녕하세요 (저녁 인사)": ["곤방와"],
    "안녕히 가세요 / 안녕히 계세요": ["사요-나라", "사요나라"],
    "내일 봐": ["마따 아시따", "마따아시따", "마타아시타", "마타 아시타"],
    "다음에 또 만나": ["마따 콘도", "마따콘도", "마타콘도", "마타 콘도"],
    "처음 뵙겠습니다": ["하지메마시떼", "하지메마시테"],
    "잘 부탁합니다": ["요로시쿠 오네가이시마스", "요로시쿠오네가이시마스"],
    "다녀오겠습니다": ["이떼키마스", "이테키마스", "일떼키마스", "일떼키 마스"],
    "잘 다녀오세요": ["이떼라っしゃ이", "이떼랏샤이", "이떼라샤이", "이테랏샤이", "일떼랏샤이", "일 떼랏샤이"],
    "다녀왔습니다": ["다다이마", "타다이마"],
    "잘 다녀왔니?": ["오카에리나사이"],
    "잘 먹겠습니다": ["이따다키마스", "이타다키마스"],
    "잘 먹었습니다": ["고치소-사마데시따", "고치소사마데시따", "고치소사마데시타", "고치소-사마데시타"],
    "안녕히 주무세요": ["오야스미나사이"],
    "미안합니다 (실례합니다)": ["스미마셍", "스미마센"],
    "모르겠습니다": ["와카리마셍", "와카리마센"],
    "알았습니다": ["와카리마시따", "와카리마시타"],
    "여보세요": ["모시모시"],
    "맛있네요": ["오이시-데스네", "오이시데스네"],
    "얼마입니까": ["이쿠라데스까", "이쿠라데스카", "이쿠라 데스까"],
    "몇 시 입니까": ["난지데스까", "난지데스카", "난지 데스까"],
    "어서오세요 (가게에서)": ["이랏샤이마세", "이라샤이마세"],
    "덥네요": ["아쯔이데스네", "아츠이데스네"],
    "잘 지내십니까?": ["오겐끼데스까", "오겐키데스까", "오겐끼 데스까"]
}

st.set_page_config(page_title="일본어 퀴즈 마스터", page_icon="🌸", layout="centered")

st.title("🌸 일본어 수행평가 완벽 대비 앱 🌸")
st.caption("뜻을 보고 프린트물(8143.jpg)의 발음을 맞혀보세요!")

# 학습 모드 선택
mode = st.radio(
    "원하는 학습 모드를 선택하세요:",
    ["드롭박스 고르기 (객관식)", "발음 직접 쓰기 (주관식)"],
    horizontal=True,
    key="quiz_mode"
)

# --- [최적화] 세션 상태 초기화 구조 단일화 ---
if "initialized" not in st.session_state:
    st.session_state.questions = list(QUIZ_DATA.keys())
    random.shuffle(st.session_state.questions)
    st.session_state.score = 0
    st.session_state.total = len(QUIZ_DATA)
    st.session_state.answered = False
    st.session_state.options = []
    st.session_state.prev_mode = mode
    st.session_state.initialized = True

# 모드 변경 시 세션 안전 리셋 (충돌 방지)
if st.session_state.prev_mode != mode:
    st.session_state.questions = list(QUIZ_DATA.keys())
    random.shuffle(st.session_state.questions)
    st.session_state.score = 0
    st.session_state.options = []
    st.session_state.answered = False
    st.session_state.prev_mode = mode
    st.rerun()

# --- 퀴즈 로직 루프 ---
if st.session_state.questions:
    current_q = st.session_state.questions[0]
    correct_answers = QUIZ_DATA[current_q]
    primary_answer = correct_answers[0]  # 표준 정답 가이드용
    
    st.info(f"**문제: {current_q}**")
    
    # --- [모드 1] 드롭박스 객관식 모드 ---
    if mode == "드롭박스 고르기 (객관식)":
        # 현재 문제에 대한 보기 생성 (중복 차단 및 딱 한 번만 실행)
        if not st.session_state.options:
            wrong_pool = [ans_list[0] for q, ans_list in QUIZ_DATA.items() if q != current_q]
            selected_wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
            options = selected_wrongs + [primary_answer]
            random.shuffle(options)
            st.session_state.options = options
            
        # 드롭박스(selectbox) 구현
        choices = ["-- 선택지를 골라주세요 --"] + st.session_state.options
        user_choice = st.selectbox("알맞은 발음을 선택하세요:", choices, key=f"select_{current_q}")
        
        if st.button("정답 확인", type="primary"):
            if user_choice == "-- 선택지를 골라주세요 --":
                st.warning("⚠️ 보기를 먼저 선택해 주세요!")
            elif user_choice == primary_answer:
                st.success("⭕ 정답입니다!")
                if not st.session_state.answered:
                    st.session_state.score += 1
                    st.session_state.answered = True
            else:
                st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
                st.session_state.answered = True
                
    # --- [모드 2] 주관식 타이핑 모드 ---
    else:
        user_input = st.text_input("정답(발음)을 입력하세요:", key=f"text_{current_q}").strip()
        
        if st.button("정답 확인", type="primary"):
            # 입력값과 정답 데이터 전처리 기법 고도화 (공백, 하이픈 완전 제거 후 비교)
            clean_user = user_input.replace(" ", "").replace("-", "")
            clean_correct_list = [ans.replace(" ", "").replace("-", "") for ans in correct_answers]
            
            if clean_user in clean_correct_list:
                st.success(f"⭕ 정답입니다! (인정된 정답 표기: {primary_answer})")
                if not st.session_state.answered:
                    st.session_state.score += 1
                    st.session_state.answered = True
            else:
                st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
                st.session_state.answered = True

    # --- 공통 다음 문항 이동 처리 ---
    if st.session_state.answered:
        if st.button("다음 문제로 👉"):
            st.session_state.questions.pop(0)
            st.session_state.options = []   
            st.session_state.answered = False 
            st.rerun()
            
    st.write(f"현재 진행 상황: {st.session_state.score} / {st.session_state.total}")

else:
    st.balloons()
    st.success("🎉 25가지 모든 문제를 다 풀었습니다! 수행평가 만점입니다! 🎉")
    if st.button("처음부터 다시 도전하기"):
        del st.session_state.initialized
        st.rerun()
