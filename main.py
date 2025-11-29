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
# 1. 계산기 앱 함수 (변동 없음)
# ==============================================================================

def calculator_app():
    """
    사칙연산, 모듈러, 지수, 로그, 다항함수 연산 기능을 제공하는 계산기 화면
    """
    st.title("🧮 다기능 웹 계산기")
    st.markdown("### 사칙연산, 공학 연산 및 다항함수 연산을 수행합니다.")
    st.write("---")

    # 1. 연산 종류 선택 (계산기 전용 selectbox)
    operation = st.selectbox(
        "연산 종류를 선택하세요",
        (
            "덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)", 
            "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (log)",
            "**다항함수 연산 (P(x))**"
        )
    )

    # 2. 연산 종류에 따른 입력 UI 조건부 렌더링 (이전 코드와 동일)
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


    # 3. 계산 실행 버튼 및 로직 (이전 코드와 동일)
    if st.button("계산하기", type="primary"):
        result = None
        equation = ""

        try: 
            if operation == "덧셈 (+)":
                result = num1 + num2
                equation = f"{num1} + {num2}"
            
            # --- (나머지 사칙연산 및 공학 연산 로직은 생략) ---
            # ...

            elif operation == "뺄셈 (-)":
                result = num1 - num2
                equation = f"{num1} - {num2}"

            elif operation == "곱셈 (*)":
                result = num1 * num2
                equation = f"{num1} \times {num2}"

            elif operation == "나눗셈 (/)":
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    st.stop()
                else:
                    result = num1 / num2
                    equation = f"{num1} \div {num2}"

            elif operation == "나머지 연산 (%)":
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    st.stop()
                else:
                    result = num1 % num2
                    equation = f"{num1} \pmod{{{num2}}}"

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
                    equation = f"\log_{{{num2}}} ({num1})"
            
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
                
                # LaTeX 수식 구성 로직 (생략)
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
            st.latex(f"{equation} \approx {result:.4f}")

# ==============================================================================
# 2. 확률 시뮬레이터 앱 함수 (카드 뽑기 기능 추가)
# ==============================================================================

def probability_simulator_app():
    """
    주사위, 동전, 카드 뽑기 시뮬레이션 및 Plotly 시각화 화면
    """
    st.title("🎲 확률 시뮬레이터")
    st.markdown("### 주사위, 동전, 카드 뽑기를 시뮬레이션하고 결과를 시각화합니다.")
    st.write("---")

    # 시뮬레이션 설정
    sim_type = st.selectbox(
        "시뮬레이션 대상 선택", 
        ("주사위 던지기 🎲", "동전 던지기 🪙", "**카드 뽑기 🃏**") # 카드 뽑기 추가
    )
    
    st.markdown("---")
    
    col_input, col_info = st.columns([1, 1])

    with col_input:
        n_trials = st.slider("시행 횟수 (N)", min_value=100, max_value=100000, value=1000, step=100)
        st.caption("시행 횟수가 많을수록 이론적 확률에 수렴합니다 (대수의 법칙).")
        
        if sim_type == "**카드 뽑기 🃏**":
            n_draws = st.slider("한 번에 뽑을 카드 수", min_value=1, max_value=5, value=1, step=1)
            st.caption("52장 카드 덱에서 한 번의 시행마다 비복원 추출로 카드를 뽑습니다.")
        else:
            n_draws = 1 # 카드 뽑기가 아닌 경우 사용하지 않음
            
        if st.button("시뮬레이션 실행", type="primary"):
            
            results = []
            
            # --- 주사위 던지기 로직 ---
            if sim_type == "주사위 던지기 🎲":
                for _ in range(n_trials):
                    results.append(random.randint(1, 6))
                
                title = f"주사위 던지기 결과 (N={n_trials})"
                x_label = "주사위 눈"
                
                with col_info:
                    st.info("💡 **이론적 확률**")
                    st.markdown("각 눈이 나올 확률은 $1/6 \\approx 16.67\\%$ 입니다.")
                
            # --- 동전 던지기 로직 ---
            elif sim_type == "동전 던지기 🪙":
                for _ in range(n_trials):
                    results.append(random.choice(['앞면', '뒷면']))
                    
                title = f"동전 던지기 결과 (N={n_trials})"
                x_label = "결과"
                
                with col_info:
                    st.info("💡 **이론적 확률**")
                    st.markdown("앞면 또는 뒷면이 나올 확률은 $1/2 = 50\\%$ 입니다.")

            # --- 🌟 카드 뽑기 로직 (새로 추가) 🌟 ---
            elif sim_type == "**카드 뽑기 🃏**":
                # 카드 덱 초기화 (모양: S-스페이드, H-하트, D-다이아, C-클로버 / 숫자: A, 2-10, J, Q, K)
                suits = ['S', 'H', 'D', 'C']
                ranks = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
                deck = [f"{s}{r}" for s in suits for r in ranks] # 52장

                # 시행 횟수만큼 반복
                for _ in range(n_trials):
                    # 비복원 추출 (without replacement)
                    drawn_cards = random.sample(deck, n_draws) 
                    
                    # 뽑은 카드들을 문자열로 합쳐서 결과에 저장 (여러 장 뽑을 경우)
                    if n_draws == 1:
                        results.append(drawn_cards[0]) # 한 장만 뽑을 경우 카드 이름만 저장
                    else:
                        # 여러 장 뽑을 경우 (예: 'S2, HK'로 저장) -> 여기서는 첫 번째 카드만 시각화 대상으로 지정
                        # 시각화의 복잡성을 줄이기 위해 첫 번째 뽑은 카드의 Rank만 기록
                        first_card_rank = drawn_cards[0][1:] 
                        results.append(first_card_rank)

                title = f"카드 뽑기 결과 ({n_draws}장 뽑기, N={n_trials})"
                x_label = "결과 (주로 첫 번째 카드 Rank)"
                
                with col_info:
                    st.info("💡 **시뮬레이션 방식**")
                    if n_draws == 1:
                        st.markdown("매 시행마다 **1장**을 뽑고 다시 덱에 넣습니다 (복원 추출과 동일 효과).")
                        st.markdown(f"특정 카드(예: SA)가 나올 확률: $1/52 \\approx 1.92\\%$")
                    else:
                        st.markdown(f"매 시행마다 **{n_draws}장**을 뽑습니다 (비복원 추출). 시각화는 **첫 번째 뽑은 카드**의 Rank(A, 2~K)를 기준으로 합니다.")
                        st.markdown(f"특정 Rank(예: A)가 나올 확률: $4/52 \\approx 7.69\\%$")


            # 데이터프레임 생성 및 집계 (시각화 공통 로직)
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
