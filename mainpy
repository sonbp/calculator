import streamlit as st
import math

# 페이지 설정 (제목, 아이콘 등)
st.set_page_config(page_title="나만의 공학 계산기", page_icon="🧮")

# 타이틀 및 설명
st.title("🧮 다기능 웹 계산기")
st.markdown("### 깃허브와 스트림릿으로 만든 계산기입니다.")
st.write("---")

# 사이드바에서 연산 모드 선택
operation = st.sidebar.selectbox(
    "연산 종류를 선택하세요",
    ("덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)", 
     "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (log)")
)

# 입력값 받기 (2개의 숫자)
# 컬럼을 나누어 보기 좋게 배치
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("첫 번째 숫자 (또는 진수)", value=0.0, step=1.0, format="%.2f")

with col2:
    num2 = st.number_input("두 번째 숫자 (또는 지수/밑)", value=0.0, step=1.0, format="%.2f")

# 계산 실행 버튼
if st.button("계산하기"):
    result = None
    equation = ""

    # 연산 로직
    try:
        if operation == "덧셈 (+)":
            result = num1 + num2
            equation = f"{num1} + {num2}"

        elif operation == "뺄셈 (-)":
            result = num1 - num2
            equation = f"{num1} - {num2}"

        elif operation == "곱셈 (*)":
            result = num1 * num2
            equation = f"{num1} \times {num2}"

        elif operation == "나눗셈 (/)":
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                result = num1 / num2
                equation = f"{num1} \div {num2}"

        elif operation == "나머지 연산 (%)":
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                result = num1 % num2
                equation = f"{num1} \pmod{{{num2}}}"

        elif operation == "지수 연산 (^)":
            result = math.pow(num1, num2)
            equation = f"{num1}^{{{num2}}}"

        elif operation == "로그 연산 (log)":
            # num1: 진수, num2: 밑
            if num1 <= 0:
                st.error("진수는 0보다 커야 합니다.")
            elif num2 <= 0 or num2 == 1:
                st.error("밑은 0보다 크고 1이 아니어야 합니다.")
            else:
                result = math.log(num1, num2)
                equation = f"\log_{{{num2}}} ({num1})"

        # 결과 출력
        if result is not None:
            st.success("계산 성공!")
            # 수식은 LaTeX 형식으로 깔끔하게 표시
            st.latex(f"{equation} = {result:.4f}")
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# 바닥글
st.write("---")
st.caption("Created with Python & Streamlit")
