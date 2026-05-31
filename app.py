import streamlit as st
import random

# 8143.jpg 이미지 데이터 기반 (여러 개의 정답 발음을 리스트로 지정)
quiz_data = {
    "안녕하세요 (아침 인사)": ["오하요-고자이마스", "오하요고자이마스"],
    "안녕하세요 (낮 인사)": ["곤니찌와"],
    "안녕하세요 (저녁 인사)": ["곤방와"],
    "안녕히 가세요 / 안녕히 계세요": ["사요-나라", "사요나라"],
    "내일 봐": ["마따 아시따", "마따아시따"],
    "다음에 또 만나": ["마따 콘도", "마따콘도"],
    "처음 뵙겠습니다": ["하지메마시떼"],
    "잘 부탁합니다": ["요로시쿠 오네가이시마스", "요로시쿠오네가이시마스"],
    "다녀오겠습니다": ["이떼키마스"],
    "잘 다녀오세요": ["이떼라っしゃ이", "이떼랏샤이", "이떼라샤이"], # 여러 발음 동시 적용
    "다녀왔습니다": ["다다이마"],
    "잘 다녀왔니?": ["오카에리나사이"],
    "잘 먹겠습니다": ["이따다키마스"],
    "잘 먹었습니다": ["고치소-사마데시따", "고치소사마데시따"],
    "안녕히 주무세요": ["오야스미나사이"],
    "미안합니다 (실례합니다)": ["스미마셍"],
    "모르겠습니다": ["와카리마셍"],
    "알았습니다": ["와카리마시따"],
    "여보세요": ["모시모시"],
    "맛있네요": ["오이시-데스네", "오이시데스네"],
    "얼마입니까": ["이쿠라데스까"],
    "몇 시 입니까": ["난지데스까"],
    "어서오세요 (가게에서)": ["이랏샤이마세"],
    "덥네요": ["아쯔이데스네"],
    "잘 지내십니까?": ["오겐끼데스까", "오겐키데스까"]
}

st.set_page_config(page_title="일본어 퀴즈 마스터", page_icon="🌸", layout="centered")

st.title("🌸 일본어 수행평가 완벽 대비 앱 🌸")
st.caption("뜻을 보고 프린트물(8143.jpg)의 발음을 맞혀보세요!")

# --- 모드 선택 구역 ---
mode = st.radio(
    "원하는 학습 모드를 선택하세요:",
    ["선택지 고르기 (객관식)", "발음 직접 쓰기 (주관식)"],
    horizontal=True,
    key="quiz_mode"
)

# 모드가 바뀌면 퀴즈를 리셋하기 위한 트리거
if "prev_mode" not in st.session_state:
    st.session_state.prev_mode = mode

if st.session_state.prev_mode != mode:
    st.session_state.questions = []  # 리셋 유도
    st.session_state.prev_mode = mode

# --- 세션 상태 초기화 ---
if "questions" not in st.session_state or not st.session_state.questions:
    st.session_state.questions = list(quiz_data.keys())
    random.shuffle(st.session_state.questions)
    st.session_state.score = 0
    st.session_state.total = len(quiz_data)
    st.session_state.answered = False
    st.session_state.options = []

if st.session_state.questions:
    current_q = st.session_state.questions[0]
    correct_answers = quiz_data[current_q]
    primary_answer = correct_answers[0]  # 화면 표시용 대표 정답
    
    st.info(f"**문제: {current_q}**")
    
    # --- [모드 1] 객관식 모드 제어 ---
    if mode == "선택지 고르기 (객관식)":
        # 문제를 처음 보거나 정답 확인 후 다음 단계로 가기 전, 보기 4개 생성
        if not st.session_state.options:
            wrong_pool = [ans_list[0] for q, ans_list in quiz_data.items() if q != current_q]
            options = random.sample(wrong_pool, min(3, len(wrong_pool)))
            options.append(primary_answer)
            random.shuffle(options)
            st.session_state.options = options
            
        user_choice = st.radio("알맞은 발음을 고르세요:", st.session_state.options, key="radio_choice")
        
        if st.button("정답 확인", type="primary"):
            if user_choice == primary_answer:
                st.success("⭕ 정답입니다!")
                if not st.session_state.answered:
                    st.session_state.score += 1
                    st.session_state.answered = True
            else:
                st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
                st.session_state.answered = True
                
    # --- [모드 2] 주관식 모드 제어 ---
    else:
        user_input = st.text_input("정답(발음)을 입력하세요:", key="text_input_ans").strip().replace(" ", "")
        
        if st.button("정답 확인", type="primary"):
            # 공백을 제거한 모든 허용 정답 리스트 생성
            clean_correct_list = [ans.replace(" ", "") for ans in correct_answers]
            
            if user_input in clean_correct_list:
                st.success(f"⭕ 정답입니다! (인정된 발음: {correct_answers})")
                if not st.session_state.answered:
                    st.session_state.score += 1
                    st.session_state.answered = True
            else:
                st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
                st.session_state.answered = True

    # --- 다음 문제 넘어가기 처리 ---
    if st.session_state.answered:
        if st.button("다음 문제로 👉"):
            st.session_state.questions.pop(0)
            st.session_state.options = []   # 다음 문제 보기 초기화
            st.session_state.answered = False # 답변 상태 초기화
            st.rerun()
            
    st.write(f"현재 진행률: {st.session_state.score} / {st.session_state.total}")

else:
    st.balloons()
    st.success("🎉 모든 문제를 다 풀었습니다! 수행평가 만점 달성! 🎉")
    if st.button("처음부터 다시 하기"):
        st.session_state.questions = []
        st.rerun()
