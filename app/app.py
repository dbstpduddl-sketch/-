import streamlit as st
import pandas as pd

# Load product data
@st.cache_data
def load_products():
    return pd.read_csv("products.csv")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'start'
if 'budget' not in st.session_state:
    st.session_state.budget = None
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Move to another page
def go_to(page):
    st.session_state.page = page

# -------------------------
# 1. Start Page
# -------------------------
if st.session_state.page == 'start':
    st.title("🛒 미션 선택하기")
    st.write("세 가지 예산 중 하나를 선택하세요.")

    budget = st.radio("예산 선택", [5000, 10000, 20000])

    if st.button("다음으로 이동"):
        st.session_state.budget = budget
        go_to('shop')

# -------------------------
# 2. Shopping Page
# -------------------------
elif st.session_state.page == 'shop':
    st.title("🛍️ 쇼핑하기")
    st.write(f"선택한 예산: **{st.session_state.budget}원**")

    products = load_products()

    for i, row in products.iterrows():
        cols = st.columns([1, 2])

        with cols[0]:
            st.image(row["image_url"], width=120)

        with cols[1]:
            st.write(f"**{row['name']}**")
            st.write(f"가격: {row['price']}원")

            if st.button(f"장바구니 담기 {i}"):
                current_total = sum(item['price'] for item in st.session_state.cart)
                if current_total + row["price"] <= st.session_state.budget:
                    st.session_state.cart.append(row.to_dict())
                    st.success("장바구니에 담겼습니다!")
                else:
                    st.error("예산 초과! 다른 상품을 선택하세요.")

    st.subheader("🧺 장바구니")
    for item in st.session_state.cart:
        st.write(f"- {item['name']} ({item['price']}원)")

    if st.button("결제하기"):
        go_to("result")

# -------------------------
# 3. Result Page
# -------------------------
elif st.session_state.page == 'result':
    st.title("📄 구매 결과")
    st.write("예산 사용 목록:")

    total = sum(item['price'] for item in st.session_state.cart)
    st.write(f"총 사용 금액: **{total}원**")

    for item in st.session_state.cart:
        st.write(f"- {item['name']} ({item['price']}원)")

    st.write("## 구매 이유 작성")
    reason = st.text_area("구매 이유를 작성하세요:")

    if st.button("제출하기"):
        st.success("제출되었습니다! (추후 PNG 저장 기능 추가 가능)")
