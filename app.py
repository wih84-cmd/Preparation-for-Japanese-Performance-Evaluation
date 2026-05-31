import streamlit as st
import random
import time

# [데이터] 8143.jpg 프린트물 25개 전체 문항 데이터
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
    "잘 다녀오세요": ["이떼랏샤이", "이테랏샤이", "일떼랏샤이", "이떼라샤이", "이테라샤이"],
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

st.set_page_config(page_title="일본어 스톱워치 퀴즈", page_icon="⏱️", layout="centered")

st.title("⏱️ 일본어 수행평가 스톱워치 챌린지! ⏱️")
st.caption("25문제를 모두 완료하는 데 걸리는 최단 시간을 측정합니다. 손가락을 빠르게 움직이세요!")

# 학습 모드 선택
mode = st.radio(
    "원하는 학습 모드를 선택하세요:",
    ["드롭박스 고르기 (객관식)", "발음 직접 쓰기 (주관식)"],
    horizontal=True,
    key="quiz_mode"
)

# --- 🛠️ 안전한 세션 초기화 구조 ---
def reset_game_state():
    st.session_state.questions = list(QUIZ_DATA.keys())
    random.shuffle(st.session_state.questions)
    st.session_state.score = 0
    st.session_state.total = len(QUIZ_DATA)
    st.session_state.current_answered = False
    st.session_state.options = []
    st.session_state.start_time = time.time()
    st.session_state.final_time = None  # 최종 기록 저장용
    st.session_state.initialized = True

required_keys = ["questions", "score", "total", "current_answered", "options", "start_time", "final_time", "initialized"]
if not all(k in st.session_state for k in required_keys):
    reset_game_state()

if "prev_mode" not in st.session_state:
    st.session_state.prev_mode = mode

if st.session_state.prev_mode != mode:
    st.session_state.prev_mode = mode
    reset_game_state()
    st.rerun()

# --- 실시간 경과 시간 계산 ---
if st.session_state.final_time is None:
    elapsed_time = time.time() - st.session_state.start_time
else:
    elapsed_time = st.session_state.final_time

# --- 🏁 [게임 완료 화면] 25문제를 모두 마쳤을 때 ---
if not st.session_state.questions:
    if st.session_state.final_time is None:
        st.session_state.final_time = time.time() - st.session_state.start_time
        elapsed_time = st.session_state.final_time
        
    st.balloons()
    st.header("🏁 챌린지 완료!! 🏁")
    st.success(f"🎉 모든 문제를 풀고 스톱워치를 정지했습니다!")
    
    # 시간 가독성 포맷팅 (분/초 단위 분리)
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time - int(elapsed_time)) * 100)
    
    if minutes > 0:
        time_str = f"{minutes}분 {seconds}초 {milliseconds:02d}"
    else:
        time_str = f"{seconds}초 {milliseconds:02d}"
        
    st.metric(label="⏱️ 최종 소요 시간 (타임 레코드)", value=time_str)
    st.metric(label="최종 맞힌 개수", value=f"{st.session_state.score} / {st.session_state.total}")
    
    if st.button("내 기록 깨러 가기 (재도전) 🔄", type="primary"):
        reset_game_state()
        st.rerun()
    st.stop()

# --- 🕹️ 게임 진행 화면 구역 ---
current_q = st.session_state.questions[0]
correct_answers = QUIZ_DATA[current_q]
primary_answer = correct_answers[0]

# 현재 몇 번째 문제인지 계산
current_index = st.session_state.total - len(st.session_state.questions) + 1
st.info(f"**문제 {current_index}/{st.session_state.total}: {current_q}**")

# 상단 실시간 스톱워치 및 진행도 바가 들어갈 자리
timer_placeholder = st.empty()

# --- [모드 1] 드롭박스 객관식 ---
if mode == "드롭박스 고르기 (객관식)":
    if not st.session_state.options:
        wrong_pool = [ans_list[0] for q, ans_list in QUIZ_DATA.items() if q != current_q]
        selected_wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        options = selected_wrongs + [primary_answer]
        random.shuffle(options)
        st.session_state.options = options
        
    choices = ["-- 선택지를 골라주세요 --"] + st.session_state.options
    user_choice = st.selectbox("알맞은 발음을 선택하세요:", choices, key=f"select_{current_q}", disabled=st.session_state.current_answered)
    
    if st.button("정답 확인", type="primary", disabled=st.session_state.current_answered):
        if user_choice == "-- 선택지를 골라주세요 --":
            st.warning("⚠️ 보기를 먼저 선택해 주세요!")
        elif user_choice == primary_answer:
            st.success("⭕ 정답입니다!")
            st.session_state.score += 1
            st.session_state.current_answered = True
            st.rerun()
        else:
            st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
            st.session_state.current_answered = True
            st.rerun()
            
# --- [모드 2] 주관식 타이핑 ---
else:
    user_input = st.text_input("정답(발음)을 입력하세요:", key=f"text_{current_q}", disabled=st.session_state.current_answered).strip()
    
    if st.button("정답 확인", type="primary", disabled=st.session_state.current_answered):
        clean_user = user_input.replace(" ", "").replace("-", "")
        clean_correct_list = [ans.replace(" ", "").replace("-", "") for ans in correct_answers]
        
        if clean_user in clean_correct_list:
            st.success(f"⭕ 정답입니다! (인정된 정답 표기: {primary_answer})")
            st.session_state.score += 1
            st.session_state.current_answered = True
            st.rerun()
        else:
            st.error(f"❌ 틀렸습니다! 정답은 [{primary_answer}] 입니다.")
            st.session_state.current_answered = True
            st.rerun()

# --- 다음 문항 이동 처리 ---
if st.session_state.current_answered:
    if st.button("다음 문제로 👉"):
        st.session_state.questions.pop(0)
        st.session_state.options = []   
        st.session_state.current_answered = False 
        st.rerun()
        
st.write(f"현재 맞힌 개수: {st.session_state.score} / {st.session_state.total}")

# --- 🔥 [핵심] 실시간 스톱워치 업카운트 및 진행바 제어 루프 ---
progress_percent = (st.session_state.total - len(st.session_state.questions)) / st.session_state.total

if not st.session_state.current_answered:
    while True:
        elapsed_time = time.time() - st.session_state.start_time
        with timer_placeholder.container():
            st.progress(progress_percent) # 문제 진행도를 게이지바로 표시
            st.write(f"⏱️ **현재 경과 시간: {elapsed_time:.1f}초**")
        time.sleep(0.1) # 0.1초 단위로 빠르게 스톱워치를 갱신
else:
    # 정답을 확인하고 다음 버튼을 누르기 전 대기 시간 동안 화면 유지
    with timer_placeholder.container():
        st.progress(progress_percent)
        st.write(f"⏱️ **현재 경과 시간: {elapsed_time:.1f}초 (정답 확인 완료, 기록 단축을 위해 무브무브!)**")
