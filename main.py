import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="🧮 다기능 공학 계산기", page_icon="⚙️")

st.title("🧮 다기능 웹 계산기")
st.markdown("---")

# 1. 연산 종류 선택 (사이드바)
operation = st.sidebar.selectbox(
    "연산 종류를 선택하세요",
    (
        "덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)", 
        "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (log)",
        "**다항함수 연산 (P(x))**"
    )
)

st.header(f"선택된 연산: {operation}")

# 2. 연산 종류에 따른 입력 UI 조건부 렌더링
num1 = 0.0
num2 = 0.0
coeffs_input = ""
x_value = 0.0

if "다항함수 연산" in operation:
    # 다항함수 연산 입력
    st.markdown("### 다항함수 입력")
    st.write("다항식 $P(x)$의 **계수**를 최고차항부터 상수항 순으로 쉼표(`,`)를 사용하여 입력하세요.")
    st.write("> 예시: $3x^2 - 2x + 1$ 의 경우: `3, -2, 1`")
    
    coeffs_input = st.text_input(
        "계수 입력 (쉼표로 구분)", 
        value="1, 0, 0" # 기본값: x^2
    )
    
    x_value = st.number_input(
        "x 값 입력 (P(x)를 계산할 지점)",
        value=1.0,
        step=0.1,
        format="%.2f"
    )
    
else:
    # 2개의 숫자만 필요한 기본 연산 입력
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("첫 번째 숫자 (또는 진수)", value=0.0, step=1.0, format="%.2f")
    with col2:
        num2 = st.number_input("두 번째 숫자 (또는 지수/밑)", value=0.0, step=1.0, format="%.2f")


# 3. 계산 실행 버튼 및 로직
if st.button("계산하기", type="primary"):
    result = None
    equation = ""

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
                st.stop() # 👈 오류 수정: return 대신 st.stop()
            else:
                result = num1 / num2
                equation = f"{num1} \div {num2}"

        elif operation == "나머지 연산 (%)":
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
                st.stop() # 👈 오류 수정: return 대신 st.stop()
            else:
                result = num1 % num2
                equation = f"{num1} \pmod{{{num2}}}"

        elif operation == "지수 연산 (^)":
            result = math.pow(num1, num2)
            equation = f"{num1}^{{{num2}}}"

        elif operation == "로그 연산 (log)":
            if num1 <= 0:
                st.error("진수는 0보다 커야 합니다.")
                st.stop() # 👈 오류 수정: return 대신 st.stop()
            elif num2 <= 0 or num2 == 1:
                st.error("밑은 0보다 크고 1이 아니어야 합니다.")
                st.stop() # 👈 오류 수정: return 대신 st.stop()
            else:
                result = math.log(num1, num2)
                equation = f"\log_{{{num2}}} ({num1})"
        
        # 다항함수 연산 로직
        elif "**다항함수 연산 (P(x))**" in operation:
            
            # 1) 계수 파싱 및 정리
            try:
                coeffs = [float(c.strip()) for c in coeffs_input.split(',') if c.strip()]
            except ValueError:
                st.error("계수 입력 형식이 올바르지 않습니다. 숫자를 쉼표로 구분했는지 확인해주세요.")
                st.stop() # 👈 오류 수정: return 대신 st.stop()

            if not coeffs:
                st.warning("계수를 입력해주세요.")
                st.stop() # 👈 오류 수정: return 대신 st.stop()
            
            # 2) 다항식 평가 (Horner's Method)
            result = 0
            for coeff in coeffs:
                result = result * x_value + coeff
            
            # 3) 수식 구성 (LaTeX)
            poly_parts = []
            degree = len(coeffs) - 1
            
            for i, coeff in enumerate(coeffs):
                current_degree = degree - i
                
                if coeff == 0:
                    continue
                
                sign = "" if i == 0 or coeff < 0 else "+" 
                abs_coeff = abs(coeff)
                
                if current_degree == 0:
                    part = f"{sign} {abs_coeff}"
                elif current_degree == 1:
                    coeff_str = "" if abs_coeff == 1 else abs_coeff
                    part = f"{sign} {coeff_str}x"
                else:
                    coeff_str = "" if abs_coeff == 1 else abs_coeff
                    part = f"{sign} {coeff_str}x^{{{current_degree}}}"
                
                poly_parts.append(part.strip())

            poly_str = "".join(poly_parts).strip().replace('+ -', '- ')
            if not poly_str: poly_str = "0"
            
            if poly_str.startswith('+ '):
                poly_str = poly_str[2:]
            
            equation = f"P({x_value}) = {poly_str}"


        # 최종 결과 출력
        if result is not None:
            st.success("계산 성공!")
            # 수식은 LaTeX 형식으로 깔끔하게 표시
