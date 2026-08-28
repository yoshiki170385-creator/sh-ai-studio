import os
import json
import shutil
import re
import streamlit as st

# -------------------------------------------------------------------
# 1. 파일명에서 클린 상품명 자동 추출
# -------------------------------------------------------------------
def extract_product_name(filename):
    # 확장자 제거
    name = os.path.splitext(filename)[0]
    # 특수문자 및 숫자 정리
    name = re.sub(r'[^\w\s가-힣]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name if name else "가성비 추천 꿀템"

# -------------------------------------------------------------------
# 2. PC 내 캡컷(CapCut) 드래프트 경로 탐지 및 생성
# -------------------------------------------------------------------
def get_capcut_draft_folder():
    user_profile = os.environ.get("USERPROFILE", "")
    capcut_path = os.path.join(
        user_profile, 
        "AppData", "Local", "CapCut", "User Data", "Projects", "com.lveditor.draft"
    )
    if os.path.exists(capcut_path):
        return capcut_path
    return None

def create_capcut_draft(project_name, video_path, script_text):
    draft_root = get_capcut_draft_folder()
    if not draft_root:
        return False, "웹(온라인) 환경 실행 중입니다. 아래 생성된 대본을 복사하여 캡컷에 사용해 주세요!"

    project_dir = os.path.join(draft_root, project_name)
    os.makedirs(project_dir, exist_ok=True)

    target_video_path = os.path.join(project_dir, "main_video.mp4")
    shutil.copy(video_path, target_video_path)

    script_file_path = os.path.join(project_dir, "extracted_script.txt")
    with open(script_file_path, "w", encoding="utf-8") as f:
        f.write(script_text)

    draft_content = {
        "canvas_config": {"height": 1920, "width": 1080},
        "tracks": [
            {
                "type": "video",
                "segments": [
                    {
                        "material_id": "main_video",
                        "target_timerange": {"duration": 30000000, "start": 0}
                    }
                ]
            }
        ]
    }

    with open(os.path.join(project_dir, "draft_content.json"), "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=4)

    return True, project_dir

# -------------------------------------------------------------------
# 3. Streamlit UI
# -------------------------------------------------------------------
st.set_page_config(page_title="상훈's AI - 원클릭 원본 영상 편집기", page_icon="⚡", layout="wide")

st.title("⚡ 상훈's AI - 샤오홍슈 원클릭 원본 영상 편집 스튜디오")
st.caption("상품명을 따로 입력할 필요 없이 원본 영상만 올리면 원클릭으로 맞춤 대본과 캡컷 프로젝트를 완성합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("🇨🇳 샤오홍슈 원본 영상(.mp4)을 올려주세요", type=["mp4", "mov"])
    
    channel_option = st.radio("📺 워터마크 채널 선택:", ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"], horizontal=True)
    channel_name = st.text_input("채널명 직접 입력", value="꿀템창고") if channel_option == "직접 입력" else channel_option

    if uploaded_file is not None:
        temp_dir = "temp_process"
        os.makedirs(temp_dir, exist_ok=True)
        input_vpath = os.path.join(temp_dir, uploaded_file.name)
        
        with open(input_vpath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.video(input_vpath)

        # 파일명에서 상품명 자동 인식
        auto_product_name = extract_product_name(uploaded_file.name)
        st.info(f"💡 인식된 상품명: **{auto_product_name}**")

        if st.button("🚀 원클릭 대본 생성 및 캡컷 프로젝트 연동"):
            with st.spinner("📹 원본 영상을 분석하여 원클릭 패키지를 구성하는 중..."):
                clean_tag = auto_product_name.replace(" ", "")
                clean_channel = channel_name.replace(" ", "")

                script_text = f"""[🔥 원클릭 맞춤 바이럴 대본 - {auto_product_name}]

🎬 [00:00~00:03] 초반 후킹 (시선 고정)
"진작 살 걸 왜 이제 샀을까 후회하는 바로 그 아이템 {auto_product_name}!"

🎬 [00:03~00:15] 핵심 가치 및 실사용 장점
"공간 차지 없이 깔끔하게 정돈되고, 쓸 때마다 실용성에 감탄하게 되는 필수 꿀템입니다."

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내
"🔗 자세한 최저가 구매 정보와 스펙은 지금 바로 아래 고정 댓글 링크를 확인해 보세요!"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"🔔 더 많은 가성비 살림 꿀템 정보가 궁금하시다면 '{channel_name}' 구독과 좋아요 부탁드립니다!"
"""
                upload_text = f"""=== [🔴 유튜브 쇼츠 상세 설명문 & 고정 댓글용] ===
진작 살 걸 왜 이제 샀을까 후회하는 아이템 1위! 🔥
요즘 sns에서 가장 핫한 필수 살림템, 바로 {auto_product_name} 입니다! ✨

📌 [쿠팡 최저가 파트너스 구매 링크]
👉 https://www.coupang.com/np/search?q={auto_product_name}

#{clean_channel} #{clean_tag} #생활꿀템 #살림템 #{clean_tag}추천 #가성비템 #내돈내산
"""
                st.session_state["script_text"] = script_text
                st.session_state["upload_text"] = upload_text

                # 캡컷 드래프트 생성 (로컬 PC 실행 환경 시)
                project_name = f"Auto_{clean_tag}"
                success, msg = create_capcut_draft(project_name, input_vpath, script_text)
                
                if success:
                    st.success(f"🎉 내 PC 캡컷 프로젝트 생성 완료: '{project_name}'")
                    st.balloons()
                else:
                    st.info(f"💡 {msg}")

with col2:
    st.subheader("📋 자동 생성된 대본 & 마케팅 문구")
    if "script_text" in st.session_state:
        st.text_area("✍️ 캡컷 TTS/자막용 대본", value=st.session_state["script_text"], height=220)
        st.text_area("📋 유튜브/틱톡/릴스 마케팅 문구", value=st.session_state["upload_text"], height=200)
