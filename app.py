import streamlit as st
import random

# 8143.jpg 이미지 데이터
quiz_data = {
    "안녕하세요 (아침 인사)": "오하요-고자이마스",
    "안녕하세요 (낮 인사)": "곤니찌와",
    "안녕하세요 (저녁 인사)": "곤방와",
    "안녕히 가세요 / 안녕히 계세요": "사요-나라",
    "내일 봐": "마따 아시따",
    "다음에 또 만나": "마따 콘도",
    "처음 뵙겠습니다": "하지메마시떼",
    "잘 부탁합니다": "요로시쿠 오네가이시마스",
    "다녀오겠습니다": "이떼키마스",
    "잘 다녀오세요": "이떼라っしゃ이",
    "다녀왔습니다": "다다이마",
    "잘 다녀왔니?": "오카에리나사이",
    "잘 먹겠습니다": "이따다키마스",
    "잘 먹었습니다": "고치소-사마데시따",
    "안녕히 주무세요": "오야스미나사이",
    "미안합니다 (실례합니다)": "스미마셍",
    "모르겠습니다": "와카리마셍",
    "알았습니다": "와카리마시따",
    "여보세요": "모시모시",
    "맛있네요": "오이시-데스네",
    "얼마입니까": "이쿠라데스까",
    "몇 시 입니까": "난지데스까",
    "어서오세요 (가게에서)": "이랏샤이마세",
    "덥네요": "아쯔이데스네",
    "잘 지내십니까?": "오겐끼데스까"
}

st.set_page_config(page_title="일본어 퀴즈", page_icon="🌸", layout="centered")

st.title("🌸 일본어 수행평가 퀴즈 앱 🌸")
st.caption("뜻을 보고 프린트물(8143.jpg)에 적힌 발음을 맞혀보세요!")

# 세션 상태 초기화 (문제를 새로고침해도 유지되도록)
if "questions" not in st.session_state or not st.session_state.questions:
    st.session_state.questions = list(quiz_data.keys())
    random.shuffle(st.session_state.questions)
    st.session_state.score = 0
    st.session_state.total = len(quiz_data)

if st.session_state.questions:
    current_q = st.session_state.questions[0]
    correct_a = quiz_data[current_q]
    
    st.info(f"**문제: {current_q}**")
    
    # 사용자 입력 구역
    user_input = st.text_input("정답(발음)을 입력하세요:", key="user_answer").strip().replace(" ", "")
    
    if st.button("정답 확인", type="primary"):
        clean_correct = correct_a.replace(" ", "")
        
        if user_input == clean_correct:
            st.success("⭕ 정답입니다!")
            # 맞히면 다음 문제로 넘어가기 위해 리스트에서 제거
            st.session_state.questions.pop(0)
            st.session_state.score += 1
            st.button("다음 문제로 👉")
        else:
            st.error(f"❌ 틀렸습니다! 정답은 [{correct_a}] 입니다.")
            
    st.write(f"현재 점수: {st.session_state.score} / {st.session_state.total}")
else:
    st.balloons()
    st.success("🎉 모든 문제를 다 풀었습니다! 수행평가 만점 각! 🎉")
    if st.button("처음부터 다시 하기"):
        st.session_state.questions = []
        st.rerun()
