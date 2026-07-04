import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Streamlit 계산기", layout="centered")

# --- 세션 상태(Session State) 초기화 ---
if "expression" not in st.session_state:
    st.session_state.expression = ""  # 현재 입력 중인 수식
if "result" not in st.session_state:
    st.session_state.result = ""      # 계산 결과
if "last_expression" not in st.session_state:
    st.session_state.last_expression = "" # 결과가 나온 직전 수식
if "history" not in st.session_state:
    st.session_state.history = []     # 계산 기록 저장 리스트
if "show_history" not in st.session_state:
    st.session_state.show_history = False # 기록 창 표시 여부

# --- 버튼 클릭 이벤트 함수 정의 ---
def press_key(key):
    if key == "C":
        st.session_state.expression = ""
        st.session_state.result = ""
        st.session_state.last_expression = ""
    elif key == "⌫":  # 하나씩 지우기
        st.session_state.expression = st.session_state.expression[:-1]
    elif key == "=":
        try:
            # 사용자가 보기 편하게 넣은 'x' 기호를 파이썬 연산자 '*'로 변경
            expr_to_eval = st.session_state.expression.replace("x", "*")
            
            # 수식이 비어있지 않은 경우에만 계산
            if expr_to_eval.strip():
                # eval 함수를 사용해 문자열 수식 계산 (소수점 유지)
                calc_result = eval(expr_to_eval)
                
                # 정수형태로 표현 가능하면 정수로, 아니면 소수점 그대로 표시
                if isinstance(calc_result, float) and calc_result.is_integer():
                    calc_result = int(calc_result)
                
                st.session_state.result = str(calc_result)
                st.session_state.last_expression = st.session_state.expression
                
                # 계산 기록에 추가
                record = f"{st.session_state.expression} = {st.session_state.result}"
                if record not in st.session_state.history:
                    st.session_state.history.append(record)
        except Exception:
            st.session_state.result = "Error"
            st.session_state.last_expression = st.session_state.expression
    else:
        # 일반 숫자 및 연산자 입력
        st.session_state.expression += str(key)

def toggle_history():
    st.session_state.show_history = not st.session_state.show_history

# --- UI 레이아웃 구성 ---
st.title("🧮 스마트 계산기")

# 1. 계산 결과창 및 수식 표시창 (큰 글씨 및 작은 글씨 상단 배치)
st.markdown("---")
if st.session_state.result:
    # '=' 버튼 클릭 시 작은 글씨로 직전 수식 표시, 큰 글씨로 결과 표시
    st.caption(f"수식: {st.session_state.last_expression}")
    st.markdown(f"## **{st.session_state.result}**")
else:
    # 평소에는 현재 입력 중인 수식을 큰 글씨로 표시
    st.caption("입력창")
    st.markdown(f"## **{st.session_state.expression if st.session_state.expression else '0'}**")
st.markdown("---")

# 2. 키
