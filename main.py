import streamlit as st
import math
import random
import plotly.express as px
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="다기능 웹 앱 (계산기 & 확률 시뮬레이터)", 
    page_icon="🛠️",
    layout="wide"
)

# --- 사이드바: 앱 선택 ---
st.sidebar.title("앱 선택")
app_mode = st.sidebar.selectbox(
    "사용할 앱을 선택하세요:",
    ("계산기", "확률 시뮬레이터")
)

st.sidebar.markdown("---")


# ==============================================================================
# 1. 계산기 앱 함수
# ==============================================================================

def calculator_app():
    """
    사칙연산, 모듈러, 지수, 로그, 다항함수 연산 기능을 제공하는 계산기 화면
    """
    st.title("🧮 다기능 웹 계산기")
    st.markdown("### 사칙연산, 공학 연산 및 다항함수 연산을 수행합니다.")
    st.write("---")

    # 1. 연산 종류 선택 (계산기 전용 사이드바)
    operation = st.selectbox(
        "연산 종류를 선택하세요",
        (
            "덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)", 
            "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (log)",
            "**다항함수 연산 (P(x))**"
        )
    )

    # 2. 연산 종류에 따른 입력 UI 조건부 렌더링
    num1 = 0.0
    num2 = 0.0
    coeffs_input = ""
    x_value = 0.0

    if "다항함수 연산" in operation:
        st.markdown("### 다항함수 입력")
        st.write("다항식 $P(x)$의 **계수**를 최고차항부터 상수항 순으로 쉼표(`,`)를 사용하여 입력하세요.")
        st.write("> 예시: $3x^2 - 2x + 1$ 의 경우: `3, -2, 1`")
        
        coeffs_input = st.text_input(
            "계수 입력 (쉼표로 구분)", 
            value="1, 0, 0"
        )
        
        x_value = st.number_input(
            "x 값 입력 (P(x)를 계산할 지점)",
            value=1.0,
            step=0.1,
            format="%.2f"
        )
        
    else:
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
            # --- 사칙연산 ---
            elif operation == "뺄셈 (-)":
                result = num1 - num2
                equation = f"{num1} - {num2}"

            elif operation == "곱셈 (*)":
                result = num1 * num2
                equation = f"{num1} \\times {num2}"

            elif operation == "나눗셈 (/)":
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    st.stop()
                else:
                    result = num1 / num2
                    equation = f"{num1} \\div {num2}"

            # --- 공학 연산 ---
            elif operation == "나머지 연산 (%)":
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    st.stop()
                else:
                    result = num1 % num2
                    equation = f"{num1} \\pmod{{{num2}}}"

            elif operation == "지수 연산 (^)":
                result = math.pow(num1, num2)
                equation = f"{num1}^{{{num2}}}"

            elif operation == "로그 연산 (log)":
                if num1 <= 0:
                    st.error("진수는 0보다 커야 합니다.")
                    st.stop()
                elif num2 <= 0 or num2 == 1:
                    st.error("밑은 0보다 크고 1이 아니어야 합니다.")
                    st.stop()
                else:
                    result = math.log(num1, num2)
                    equation = f"\\log_{{{num2}}} ({num1})"
            
            # --- 다항함수 연산 ---
            elif "**다항함수 연산 (P(x))**" in operation:
                try:
                    coeffs = [float(c.strip()) for c in coeffs_input.split(',') if c.strip()]
                except ValueError:
                    st.error("계수 입력 형식이 올바르지 않습니다. 숫자를 쉼표로 구분했는지 확인해주세요.")
                    st.stop()

                if not coeffs:
                    st.warning("계수를 입력해주세요.")
                    st.stop()
                
                result = 0
                for coeff in coeffs:
                    result = result * x_value + coeff
                
                # LaTeX 수식 구성 (이전 코드와 동일)
                poly_parts = []
                degree = len(coeffs) - 1
                for i, coeff in enumerate(coeffs):
                    current_degree = degree - i
                    if coeff == 0: continue
                    sign = "" if i == 0 or coeff < 0 else "+" 
                    abs_coeff = abs(coeff)
                    
                    if current_degree == 0: part = f"{sign} {abs_coeff}"
                    elif current_degree == 1:
                        coeff_str = "" if abs_coeff == 1 else abs_coeff
                        part = f"{sign} {coeff_str}x"
                    else:
                        coeff_str = "" if abs_coeff == 1 else abs_coeff
                        part = f"{sign} {coeff_str}x^{{{current_degree}}}"
                    poly_parts.append(part.strip())

                poly_str = "".join(poly_parts).strip().replace('+ -', '- ')
                if not poly_str: poly_str = "0"
                if poly_str.startswith('+ '): poly_str = poly_str[2:]
                
                equation = f"P({x_value}) = {poly_str}"

        except Exception as e:
            st.error(f"처리 중 예상치 못한 오류가 발생했습니다: {e}")
            
        
        if result is not None:
            st.success("계산 성공!")
            st.latex(f"{equation} \\approx {result:.4f}")

# ==============================================================================
# 2. 확률 시뮬레이터 앱 함수
# ==============================================================================

def probability_simulator_app():
    """
    주사위 또는 동전 던지기 시뮬레이션 및 Plotly 시각화 화면
    """
    st.title("🎲 확률 시뮬레이터")
    st.markdown("### 주사위나 동전 던지기를 시뮬레이션하고 결과를 시각화합니다.")
    st.write("---")

    # 시뮬레이션 설정
    sim_type = st.selectbox("시뮬레이션 대상 선택", ("주사위 던지기 🎲", "동전 던지기 🪙"))
    
    st.markdown("---")
    
    col_input, col_info = st.columns([1, 1])

    with col_input:
        n_trials = st.slider("시행 횟수 (N)", min_value=100, max_value=100000, value=1000, step=100)
        st.caption("시행 횟수가 많을수록 이론적 확률에 수렴합니다 (대수의 법칙).")
        
        if st.button("시뮬레이션 실행", type="primary"):
            
            results = []
            
            if sim_type == "주사위 던지기 🎲":
                # 주사위 시뮬레이션 (1~6)
                for _ in range(n_trials):
                    results.append(random.randint(1, 6))
                
                title = f"주사위 던지기 결과 (N={n_trials})"
                x_label = "주사위 눈"
                
                # 이론적 확률
                with col_info:
                    st.info("💡 **이론적 확률**")
                    st.markdown("각 눈이 나올 확률은 $1/6 \\approx 16.67\\%$ 입니다.")
                
            elif sim_type == "동전 던지기 🪙":
                # 동전 시뮬레이션 (0: 뒷면, 1: 앞면)
                for _ in range(n_trials):
                    results.append(random.choice(['앞면', '뒷면']))
                    
                title = f"동전 던지기 결과 (N={n_trials})"
                x_label = "결과"
                
                # 이론적 확률
                with col_info:
                    st.info("💡 **이론적 확률**")
                    st.markdown("앞면 또는 뒷면이 나올 확률은 $1/2 = 50\\%$ 입니다.")

            # 데이터프레임 생성 및 집계
            df = pd.DataFrame(results, columns=['결과'])
            
            # 빈도수를 계산하여 데이터프레임으로 변환
            counts_df = df['결과'].value_counts().reset_index()
            counts_df.columns = [x_label, '빈도수']
            
            # Plotly 시각화
            fig = px.bar(
                counts_df, 
                x=x_label, 
                y='빈도수', 
                title=title,
                labels={'빈도수': '관측 빈도'},
                color=x_label, # 막대 색상 구분
                template="streamlit"
            )
            
            # 그래프 출력
            st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# 3. 메인 실행 루프
# ==============================================================================

if app_mode == "계산기":
    calculator_app()
elif app_mode == "확률 시뮬레이터":
    probability_simulator_app()

st.write("---")
st.caption("Created with Python & Streamlit")
