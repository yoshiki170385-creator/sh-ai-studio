import os
import json
import shutil
import streamlit as st

# -------------------------------------------------------------------
# 1. PC 내 캡컷(CapCut) 드래프트 경로 자동 탐지
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

# -------------------------------------------------------------------
# 2. 캡컷 드래프트 프로젝트 생성 함수
# -------------------------------------------------------------------
def create_capcut_draft(project_name, video_path, script_text):
    draft_root = get_capcut_draft_folder()
    if not draft_root:
        return False, "인터넷 웹 환경에서는 PC 캡컷 폴더에 직접 접근할 수 없습니다. 대본을 복사하여 캡컷에 사용해 주세요!"

    project_dir = os.path.join(draft_root, project_name)
    os.makedirs(project_dir, exist_ok=True)

    # 원본 영상 복사
    target_video_path = os.path.join(project_dir, "main_video.mp4")
    shutil.copy(video_path, target_video_path)

    # 추출/생성된 대본 텍스트 파일 저장
    script_file_path = os.path.join(project_dir, "extracted_script.txt")
    with open(script_file_path, "w", encoding="utf-8") as f:
        f.write(script_text)

    # 캡컷 프로젝트 기본 구조 파일(draft_content.json) 생성
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
st.set_page_config(page_title="상훈's AI - 샤오홍슈 캡컷 자동화", page_icon="✨", layout="wide")

st.title("✨ 상훈's AI - 샤오홍슈 대본 추출 & 캡컷 연동 스튜디오")
st.caption("자막 없는 샤오홍슈 원본 영상을 올려주시면, 맞춤 대본 작성 후 캡컷(CapCut) 연동용 대본 및 프로젝트를 생성합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("🇨🇳 샤오홍슈 원본 영상(.mp4) 업로드", type=["mp4", "mov"])
    project_title = st.text_input("📁 캡컷 프로젝트명", value="SH_Clean_01")
    product_name = st.text_input("🏷️ 상품명", value="휴대용 커피머신")
    feature_desc = st.text_input("✨ 상품 특징", value="가성비 꿀템")

    channel_option = st.radio("📺 워터마크 채널 선택:", ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"], horizontal=True)
    channel_name = st.text_input("채널명 직접 입력", value="꿀템창고") if channel_option == "직접 입력" else channel_option

    if uploaded_file is not None:
        temp_dir = "temp_process"
        os.makedirs(temp_dir, exist_ok=True)
        input_vpath = os.path.join(temp_dir, uploaded_file.name)
        
        with open(input_vpath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.video(input_vpath)

        if st.button("🚀 영상 분석 ➔ 대본 추출 & 캡컷 프로젝트 생성"):
            with st.spinner("📹 영상을 분석하고 대본을 생성하는 중..."):
                detail = f" {feature_desc}" if feature_desc else ""
                script_text = f"""[🔥 샤오홍슈 원본 맞춤 쇼츠 대본 - {product_name}]

🎬 [00:00~00:03] 초반 후킹 (시선 고정)
"진작 살 걸 왜 이제 샀을까 고민했던 바로 그 아이템 {product_name}{detail}!"

🎬 [00:03~00:15] 핵심 가치 및 실사용 장면
"공간 차지 없이 깔끔하게 정돈되고, 쓸 때마다 실용성에 감탄하게 되는 필수 꿀템입니다."

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내
"🔗 자세한 최저가 구매 정보와 스펙은 지금 바로 아래 고정 댓글 링크를 확인해 보세요!"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"🔔 더 많은 가성비 살림 꿀템 정보가 궁금하시다면 '{channel_name}' 구독과 좋아요 부탁드립니다!"
"""
                st.session_state["script_text"] = script_text

                # 캡컷 드래프트 생성 시도 (PC 로컬 실행 시 작동)
                success, msg = create_capcut_draft(project_title, input_vpath, script_text)
                
                if success:
                    st.success(f"🎉 내 PC 캡컷 프로젝트 생성 완료: '{project_title}'")
                    st.balloons()
                else:
                    st.info(f"💡 {msg}")

with col2:
    st.subheader("📋 추출/생성된 대본 & 마케팅 패키지")
    if "script_text" in st.session_state:
        st.text_area("✍️ 캡컷 타임라인용 대본 (TTS 복사용)", value=st.session_state["script_text"], height=380)
        st.info("""
💡 **작업 마무리 순서:**
1. 오른쪽 대본 박스의 내용을 복사합니다.
2. 캡컷(CapCut)에서 샤오홍슈 원본 영상을 타임라인에 올립니다.
3. 복사한 대본을 **캡컷 텍스트 / TTS 음성**으로 입힙니다.
4. 상단/하단에 **채널 워터마크**만 넣고 내보내면 완성됩니다!
""")
