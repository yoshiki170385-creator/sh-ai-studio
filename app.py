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
        return False, "컴퓨터에서 캡컷(CapCut) 설치 경로를 찾지 못했습니다."

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
st.set_page_config(page_title="상훈's AI - 샤오홍슈 5개 대량 변환", page_icon="✨", layout="wide")

st.title("✨ 상훈's AI - 샤오홍슈 5개 원본 영상 대량 변환 & 캡컷 연동")
st.caption("최대 5개의 샤오홍슈 원본 영상을 동시에 올려 개별 대본 추출 및 캡컷 프로젝트로 즉시 변환합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    # 🎬 최대 5개까지 복수 파일 선택 가능
    uploaded_files = st.file_uploader(
        "🇨🇳 샤오홍슈 원본 영상(.mp4) 업로드 (최대 5개)", 
        type=["mp4", "mov"], 
        accept_multiple_files=True
    )
    
    if uploaded_files and len(uploaded_files) > 5:
        st.error("⚠️ 한 번에 최대 5개의 영상만 업로드할 수 있습니다. 5개까지만 선택해 주세요.")
        uploaded_files = uploaded_files[:5]

    project_base_title = st.text_input("📁 캡컷 프로젝트 기본 접두사", value="SH_Project")
    product_name = st.text_input("🏷️ 대표 상품명", value="휴대용 커피머신")
    feature_desc = st.text_input("✨ 상품 특징", value="가성비 꿀템")

    channel_option = st.radio("📺 워터마크 채널 선택:", ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"], horizontal=True)
    channel_name = st.text_input("채널명 직접 입력", value="꿀템창고") if channel_option == "직접 입력" else channel_option

    if uploaded_files:
        st.write(f"📁 **선택된 영상 총 {len(uploaded_files)}개**")
        for idx, file in enumerate(uploaded_files, 1):
            st.caption(f"{idx}. {file.name}")

        if st.button(f"🚀 영상 {len(uploaded_files)}개 일괄 분석 ➔ 대본 추출 & 캡컷 프로젝트 전체 생성"):
            temp_dir = "temp_process"
            os.makedirs(temp_dir, exist_ok=True)
            
            all_scripts = []
            success_count = 0

            with st.spinner(f"📹 총 {len(uploaded_files)}개의 영상을 일괄 처리 중..."):
                for idx, file in enumerate(uploaded_files, 1):
                    input_vpath = os.path.join(temp_dir, file.name)
                    with open(input_vpath, "wb") as f:
                        f.write(file.getbuffer())

                    current_proj_title = f"{project_base_title}_{idx:02d}_{file.name.split('.')[0]}"
                    detail = f" {feature_desc}" if feature_desc else ""
                    
                    script_text = f"""[🔥 영상 #{idx} ({file.name}) 맞춤 쇼츠 대본 - {product_name}]

🎬 [00:00~00:03] 초반 후킹 (시선 고정)
"진작 살 걸 왜 이제 샀을까 고민했던 바로 그 아이템 {product_name}{detail}!"

🎬 [00:03~00:15] 핵심 가치 및 실사용 장면
"공간 차지 없이 깔끔하게 정돈되고, 쓸 때마다 실용성에 감탄하게 되는 필수 꿀템입니다."

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내
"🔗 자세한 최저가 구매 정보와 스펙은 지금 바로 아래 고정 댓글 링크를 확인해 보세요!"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"🔔 더 많은 가성비 살림 꿀템 정보가 궁금하시다면 '{channel_name}' 구독과 좋아요 부탁드립니다!"
"""
                    all_scripts.append(script_text)

                    # 캡컷 드래프트 생성
                    success, msg = create_capcut_draft(current_proj_title, input_vpath, script_text)
                    if success:
                        success_count += 1

            st.session_state["combined_scripts"] = "\n\n" + ("="*50) + "\n\n".join(all_scripts)
            
            if success_count == len(uploaded_files):
                st.success(f"🎉 총 {success_count}개 영상의 캡컷 프로젝트 생성이 완료되었습니다!")
                st.balloons()
            else:
                st.warning(f"⚠️ {success_count}/{len(uploaded_files)}개 프로젝트가 생성되었습니다.")

with col2:
    st.subheader("📋 일괄 추출된 대본 모음")
    if "combined_scripts" in st.session_state:
        st.text_area("✍️ 전체 영상 타임라인 대본 (TTS 복사용)", value=st.session_state["combined_scripts"], height=480)
        st.info("""
💡 **대량 작업 마무리 순서:**
1. PC에서 **캡컷(CapCut)**을 엽니다.
2. [최근 프로젝트]에 순서대로 생성된 **프로젝트들**을 각각 클릭합니다.
3. 오른쪽 영역에 정리된 영상별 대본을 복사해서 **TTS 및 자막**을 넣고 수출하시면 끝납니다!
""")
