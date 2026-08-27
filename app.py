import os
import random
import streamlit as st
import numpy as np

# 쿠팡 파트너스 API 키 고정 (원하는 경우 아래 "" 안에 실제 키를 적어두세요)
DEFAULT_CP_ACCESS_KEY = "12145ccc-653f-4354-a41c-145a47a51982"
DEFAULT_CP_SECRET_KEY = "dc141c877f6cb4b179417fc2a012099abf1a0697"

# 쿠팡 API 불러오기
try:
    from coupang_api import get_coupang_product_info
except ImportError:
    def get_coupang_product_info(kw, ak, sk):
        return {
            "productName": kw,
            "productPrice": "가격 정보 없음",
            "productImage": "https://via.placeholder.com/300x300.png?text=No+Image",
            "shortenUrl": f"https://www.coupang.com/np/search?q={kw}"
        }

st.set_page_config(
    page_title="상훈's AI Studio",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FAFAFC 0%, #F0F4FF 50%, #FFF0F5 100%);
        color: #2D3748 !important;
    }
    h1 { color: #4A5568 !important; font-weight: 800; }
    h3, .stCaption, label, p, span { color: #2D3748 !important; }
    
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        color: #2D3748 !important;
        font-size: 16px !important;
    }

    div[data-testid="stRadio"] label span {
        color: #2D3748 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #A78BFA 0%, #F472B6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        box-shadow: 0 4px 14px 0 rgba(167, 139, 250, 0.35) !important;
        transition: all 0.3s ease !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 쿠팡 파트너스 API 설정")
    cp_access_key = st.text_input("Access Key", value=DEFAULT_CP_ACCESS_KEY, type="password", key="cp_ak")
    cp_secret_key = st.text_input("Secret Key", value=DEFAULT_CP_SECRET_KEY, type="password", key="cp_sk")
    st.caption("✅ 기본 API 키가 연동되어 있습니다.")

st.title("✨ 상훈's AI 콘텐츠 스튜디오 Pro")
st.caption("📱 상품 사진/영상 업로드 기반 맞춤 대본 및 쿠팡 수익 링크 자동 생성")
st.markdown("---")

def generate_viral_shopping_script(product_name, feature_desc, channel_name, viral_pattern, coupang_url="", upload_type=None):
    detail = f" {feature_desc}" if feature_desc else ""
    
    if "진작 살걸" in viral_pattern:
        openings = [
            f"진작 살 걸 왜 이제 샀을까 고민했던 바로 그 아이템!",
            f"쓰자마자 삶의 질 3배 상승해서 난리 난 {product_name}!",
            f"안 써본 사람은 있어도 한 번만 써본 사람은 없다는 {product_name}{detail}!"
        ]
        bodys = [
            f"공간 차지 없이 깔끔하게 정돈되는 건 기본이고, 쓸 때마다 실용성에 감탄하게 됩니다.",
            f"일상의 불편했던 순간들을 손쉽게 해결해 줘서 사용해 본 사람마다 극찬하는 이유를 알겠더라고요."
        ]
    elif "가성비" in viral_pattern or "돈 아끼는" in viral_pattern:
        openings = [
            f"잠시만요! 이거 모르고 {product_name} 비싸게 사면 무조건 손해입니다!",
            f"아니 이 가격에 이 퀄리티가 말이 되나요?! 가성비 미쳤다는 {product_name}!"
        ]
        bodys = [
            f"비싼 브랜드 제품 부럽지 않은 가성비에 내구성까지 짱짱해서 정말 만족스럽습니다.",
            f"가격 대비 성능이 기대 이상이라 고민할 시간에 빠르게 가져가시는 걸 추천합니다."
        ]
    else:
        openings = [
            f"살림 고수들만 몰래 쓴다는 숨은 꿀템, 오늘 싹 공개합니다!",
            f"알아두면 무조건 유용한 살림 꿀팁! 바로 이 {product_name} 하나면 종결입니다."
        ]
        bodys = [
            f"집안 어디에 놓아도 깔끔하게 어우러지면서 스마트하게 일상을 바꿔줍니다.",
            f"번거로웠던 과정들을 1초 만에 줄여주니 라이프스타일이 한결 가벼워지는 느낌이에요."
        ]

    link_text = f" ({coupang_url})" if coupang_url else ""
    
    if upload_type == "image":
        prefix = "[🖼️ 업로드 상품 이미지 기반 쇼츠 대본]"
    elif upload_type == "video":
        prefix = "[📹 업로드 영상 맞춤 타임라인 분석 대본]"
    else:
        prefix = "[🔥 10만+ 뷰 바이럴 쇼츠 대본]"

    script = f"""{prefix} - {product_name}

🎬 [00:00~00:03] 초반 후킹 (시선 고정)
"{random.choice(openings)}"

🎬 [00:03~00:15] 주요 특징 및 핵심 가치
"{random.choice(bodys)}"

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내
"🔗 자세한 제품 스펙과 구매 링크{link_text}는 지금 바로 아래 고정 댓글을 확인해 보세요!"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"🔔 더 유용한 가성비 꿀템 정보가 궁금하다면? '{channel_name}' 구독과 좋아요 부탁드려요!"
"""
    return script

tab1, tab2 = st.tabs(["🛍️ 쇼핑 리뷰 쇼츠", "🎧 수노 AI 롱폼 플레이리스트"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ 쇼핑 쇼츠 설정 및 대본 생성")
        
        # 📸 상품 이미지 또는 📹 영상 파일 통합 업로더
        uploaded_file = st.file_uploader("📸 상품 이미지 파일 또는 📹 영상 업로드 (선택)", type=["jpg", "jpeg", "png", "webp", "mp4", "mov"])
        
        product_name = st.text_input("🏷️ 상품명", value="휴대용커피머신", key="shop_pname")
        feature_desc = st.text_input("✨ 상품 특징", value="가성비 꿀템", key="shop_fdesc")
        
        channel_option = st.radio("📺 채널 선택:", ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"], horizontal=True, key="shop_ch_radio")
        channel_name = st.text_input("채널명 직접 입력", value="꿀템창고") if channel_option == "직접 입력" else channel_option

        viral_pattern = st.selectbox(
            "🔥 인기 쇼츠 바이럴 패턴 선택:",
            [
                "🔥 [10만뷰+] 진작 살걸 후회하는 살림/생활 꿀템",
                "😱 [10만뷰+] 쿠팡에서 사면 돈 아끼는 가성비 아이템",
                "🤫 [10만뷰+] 나만 알고 싶은 숨은 살림 꿀팁/아이템"
            ],
            key="shop_viral_select"
        )

        def update_script_and_product():
            info = get_coupang_product_info(product_name, cp_access_key, cp_secret_key)
            st.session_state["cp_info"] = info
            
            upload_type = None
            if uploaded_file is not None:
                if uploaded_file.type.startswith('image'):
                    upload_type = "image"
                elif uploaded_file.type.startswith('video'):
                    upload_type = "video"
                    
            st.session_state["shop_script_box"] = generate_viral_shopping_script(
                product_name, feature_desc, channel_name, viral_pattern, info["shortenUrl"], upload_type
            )

        if "shop_script_box" not in st.session_state:
            update_script_and_product()

        st.button("💡 이미지/영상 분석 & 대본 자동 생성", key="btn_script", on_click=update_script_and_product)

        cp_info = st.session_state.get("cp_info", {})
        if cp_info and cp_info.get("productImage"):
            st.markdown("---")
            st.write("🔍 **쿠팡 매칭 상품 미리보기**")
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                st.image(cp_info["productImage"], width=130)
            with p_col2:
                st.markdown(f"**상품명:** {cp_info['productName']}")
                st.markdown(f"**가격:** {cp_info['productPrice']}")
                st.markdown(f"**수익 링크:** [{cp_info['shortenUrl']}]({cp_info['shortenUrl']})")
            st.markdown("---")

        script_val = st.text_area("✍️ 맞춤 대본 (TTS로 복사해 사용하세요)", height=280, key="shop_script_box")
        start_btn = st.button("🚀 마케팅 패키지 생성", key="btn_shop")

    with col2:
        st.subheader("📊 파일 미리보기 및 마케팅 문구")
        if uploaded_file is not None:
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="업로드된 상품 이미지", use_column_width=True)
            elif uploaded_file.type.startswith('video'):
                st.video(uploaded_file)

    if start_btn:
        clean_tag = product_name.replace(" ", "")
        clean_channel = channel_name.replace(" ", "")
        desc_detail = f" {feature_desc}" if feature_desc else ""
        cp_info = st.session_state.get("cp_info", {})
        cp_link = cp_info.get("shortenUrl", f"https://www.coupang.com/np/search?q={product_name}")

        upload_text = f"""=== [🔴 유튜브 쇼츠 상세 설명문 & 고정 댓글용] ===
진작 살 걸 왜 이제 샀을까 후회하는 아이템 1위! 🔥
요즘 sns에서 가장 핫한 필수 살림템, 바로 {product_name}{desc_detail} 입니다! ✨

📌 [쿠팡 최저가 파트너스 구매 링크]
👉 {cp_link}

💡 이런 분들께 강력 추천해 드려요!
1️⃣ 편리함과 실용성을 한 번에 챙기고 싶으신 분 🏠
2️⃣ 가성비 넘치는 필수 꿀템을 찾고 계신 분 🛍️
3️⃣ 번거롭고 불편했던 일상을 스마트하게 바꾸고 싶으신 분 ⚡

#{clean_channel} #{clean_tag} #생활꿀템 #살림템 #{clean_tag}추천 #가성비템 #내돈내산

SEO 태그(10개)
{clean_channel}, {product_name}, {clean_tag}, 생활꿀템, 살림템, 가성비템, {clean_tag}추천, 꿀템추천, 필수템, 쇼핑추천
"""
        st.success("🎉 마케팅 문구 작성이 완료되었습니다!")
        with col2:
            st.text_area("📋 [마케팅 메타패키지]", value=upload_text, height=350)
