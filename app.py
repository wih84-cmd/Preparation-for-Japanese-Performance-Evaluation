import streamlit as st
import random
import time

# [새 유인물 데이터 25개] 뜻을 보고 일본어 표현 또는 발음을 맞히는 구조
QUIZ_DATA = {
    "감사합니다": ["ありがとうございます", "아리가또~고자이마스", "아리가또고자이마스", "아리가또 고자이마스"],
    "축하합니다": ["おめでとうございます", "오매때또~고자이마스", "오매때또고자이마스", "오매때또 고자이마스"],
    "어떻습니까?": ["いかがですか", "이까가데스까", "이까가 데스까"],
    "미안합니다": ["ごめんなさい", "고멘나사이"],
    "오래간만입니다": ["おひさしぶりです", "오히사시부리데스", "오히사시부리 데스"],
    "야구를 좋아합니다": ["やきゅうがすきです", "야큐~가스끼데스", "야규가 스끼데스"],
    "잘하네요": ["じょうずですね", "죠~즈데스네", "죠즈 데스네"],
    "어디입니까?": ["どこですか", "도꼬데스까", "도꼬 데스까"],
    "언제입니까?": ["いつですか", "이쯔데스까", "이쯔 데스까"],
    "실례합니다 (방문할 때)": ["おじゃまします", "오자마시마스"],
    "괜찮습니다": ["だいじょうぶです", "다이죠~부데스", "다이조부데스"],
    "좋네요": ["いいですね", "이~~데스네", "이데스네"],
    "그렇군요": ["そうですね", "소~데스네", "소데스네"],
    "잠시만 기다려 주세요": ["ちょっとまってください", "춋또말떼쿠다사이", "춋또 말떼 쿠다사이"],
    "이쪽으로 오세요": ["こちらへどうぞ", "고찌라에도~조", "고찌라에 도조"],
    "저야말로": ["こちらこそ", "고찌라코소"],
    "조심하렴": ["きをつけてね", "키오쯔케떼네", "키오 쯔케떼네"],
    "한국에서 왔습니다": ["かんこくからきました", "강코꾸까라키마시따", "강코꾸까라 키마시따"],
    "그렇지 않아요": ["そんなことないですよ", "손나코또나이데스요", "손나 코또 나이데스요"],
    "같이 갈래": ["いっしょにいく", "잇쇼니이꾸", "잇쇼니 이꾸"],
    "힘내라": ["がんばって", "강발떼"],
    "비싸네요": ["たかいですね", "타까이데스네"],
    "싸네요": ["やすいですね", "야시이데스네"],
    "어디에 있습니까?": ["どこにありますか", "도꼬니아리마스까", "도꼬니 아리마스까"],
    "한국인입니다": ["かんこくじんです", "강코꾸진데스"]
}

# ⏱️ 문제당 제한 시간 (3초)
PER_QUESTION_TIME = 3.0

st.set_page_config(page_title="일본어 3초 스피드 퀴즈", page_icon="⚡", layout="centered")

st.title("⚡ 일본어 수행평가 3초 타임어택! ⚡")
st.caption(f"뜻을 보고 **3초 이내**에 알맞은 일본어 표현이나 발음을 맞혀 1점을 획득하세요!")

# 학습 모드 선택
mode = st.radio(
    "원하는 학습 모드를 선택하세요:",
    ["드롭박스 고르기 (객관식)", "발음 직접 쓰기 (주관식)"],
    horizontal=True,
    key="quiz_mode"
)

# --- 🛠️ 안전한 세션 초기화 함수 ---
def reset_game_state():
    st.session_state.questions = list(QUIZ_DATA.keys())
    random.shuffle(st.session_state.questions)
    st.session_state.score = 0
    st.session_state.total = len(QUIZ_DATA)
    st.session_state.current_answered = False
    st.session_state.options = []
    st.session_state.question_start_time = time.time()  # 문제별 3초 타이머 시작점
    st.session_state.initialized = True

required_keys = ["questions", "score", "total", "current_answered", "options", "question_start_time", "initialized"]
if not all(k in st.session_state for k in required_keys):
    reset_game_state()

if "prev_mode" not in st.session_state:
    st.session_state.prev_mode = mode

if st.session_state.prev_mode != mode:
    st.session_state.prev_mode = mode
    reset_game_state()
    st.rerun()

# --- 게임 종료 화면 ---
if not st.session_state.questions:
    st.balloons()
    st.header("🏁 3초 스피드 퀴즈 종료!! 🏁")
    st.success(f"🎉 25문제를 모두 풀었습니다!")
    st.metric(label="최종 획득 점수", value=f"{st.session_state.score} / {st.session_state.total}점")
    
    if st.button("다시 도전하기 🔄", type="primary"):
        reset_game_state()
        st.rerun()
    st.stop()

# --- 🕹️ 게임 진행 구역 ---
current_q = st.session_state.questions[0]
correct_answers = QUIZ_DATA[current_q]
primary_answer = correct_answers[1] if len(correct_answers) > 1 else correct_answers[0] # 가이드용 발음

# 현재 몇 번째 문제인지 계산
current_index = st.session_state.total - len(st.session_state.questions) + 1
st.info(f"**[문제 {current_index}/{st.session_state.total}] 뜻: {current_q}**")

# 타이머 및 진행도 바 위치
timer_placeholder = st.empty()

# --- 시간 경과 계산 및 3초 초과 검사 ---
elapsed_per_q = time.time() - st.session_state.question_start_time
remaining_q_time = max(0.0, PER_QUESTION_TIME - elapsed_per_q)

if remaining_q_time <= 0 and not st.session_state.current_answered:
    st.session_state.current_answered = "timeout"

# --- [모드 1] 드롭박스 객관식 ---
if mode == "드롭박스 고르기 (객관식)":
    if not st.session_state.options:
        wrong_pool = [ans_list[1] if len(ans_list) > 1 else ans_list[0] for q, ans_list in QUIZ_DATA.items() if q != current_q]
        selected_wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        options = selected_wrongs + [primary_answer]
        random.shuffle(options)
        st.session_state.options = options
        
    choices = ["-- 3초 안에 선택하세요! --"] + st.session_state.options
    user_choice = st.selectbox("알맞은 표현을 고르세요:", choices, key=f"select_{current_q}", disabled=st.session_state.current_answered)
    
    if st.button("정답 확인 (1점 도전)", type="primary", disabled=st.session_state.current_answered):
        if user_choice == "-- 3초 안에 선택하세요! --":
            st.warning("⚠️ 보기를 먼저 선택해 주세요!")
        elif user_choice in correct_answers:
            st.success("⭕ 정답! (+1점)")
            st.session_state.score += 1
            st.session_state.current_answered = True
            st.rerun()
        else:
            st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
            st.session_state.current_answered = True
            st.rerun()
            
# --- [모드 2] 주관식 타이핑 ---
else:
    user_input = st.text_input("정답(발음 또는 일본어)을 입력하세요:", key=f"text_{current_q}", disabled=st.session_state.current_answered).strip()
    
    if st.button("정답 확인 (1점 도전)", type="primary", disabled=st.session_state.current_answered):
        clean_user = user_input.replace(" ", "").replace("-", "")
        clean_correct_list = [ans.replace(" ", "").replace("-", "") for ans in correct_answers]
        
        if clean_user in clean_correct_list:
            st.success(f"⭕ 정답! (+1점)")
            st.session_state.score += 1
            st.session_state.current_answered = True
            st.rerun()
        else:
            st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
            st.session_state.current_answered = True
            st.rerun()

# --- 3초 초과되었을 때 처리 ---
if st.session_state.current_answered == "timeout":
    st.error(f"⏰ 3초 초과! (0점 처리) 정답은 [{primary_answer}] 입니다.")
    st.session_state.current_answered = True

# --- 다음 문항 이동 처리 ---
if st.session_state.current_answered is True or st.session_state.current_answered == "timeout":
    if st.button("다음 문제로 👉"):
        st.session_state.questions.pop(0)
        st.session_state.options = []   
        st.session_state.current_answered = False 
        st.session_state.question_start_time = time.time()  # 다음 문제 3초 타이머 재시작
        st.rerun()

st.write(f"현재 획득 점수: {st.session_state.score} / {st.session_state.total}점")

# --- 🔥 3초 실시간 타이머 바 루프 ---
if not st.session_state.current_answered:
    while remaining_q_time > 0:
        elapsed_per_q = time.time() - st.session_state.question_start_time
        remaining_q_time = max(0.0, PER_QUESTION_TIME - elapsed_per_q)
        
        with timer_placeholder.container():
            st.progress(remaining_q_time / PER_QUESTION_TIME)
            st.write(f"⏳ **이 문제 남은 시간: {remaining_q_time:.1f}초**")
            
        if remaining_q_time <= 0:
            st.session_state.current_answered = "timeout"
            st.rerun()
            
        time.sleep(0.1)
else:
    with timer_placeholder.container():
        st.progress(0.0)
        st.write("⏳ **시간 종료 또는 정답 확인 완료! 다음 문제로 넘어가세요.**")
