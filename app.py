import os
import json
import shutil
import random
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
# 2. 다채로운 5가지 스타일 쇼츠 대본 자동 생성기
# -------------------------------------------------------------------
def generate_dynamic_script(product_name, feature_desc, channel_name, idx=1, file_name=""):
    detail = f" {feature_desc}" if feature_desc else ""
    
    # 다양화된 초반 후킹 멘트 묶음
    hooks = [
        f"다들 집에서 {product_name} 쓸 때 아직도 손으로 힘들게 하세요?",
        f"처음엔 속는 셈 치고 사봤는데... 와, {product_name} 이건 진짜 물건이네요!",
        f"모르고 지나쳤으면 계속 고생할 뻔했던 살림 꿀템 {product_name}{detail}!",
        f"요즘 쿠팡에서 후기 폭발하고 난리 난 {product_name}, 직접 써봤습니다.",
        f"비싼 브랜드 제품 다 필요 없고, {product_name} 하나면 완벽 해결입니다!",
        f"아직도 이거 없이 집안일 하시는 분 계신가요? 삶의 질이 달라집니다."
    ]

    # 본문 설득 멘트 묶음
    bodies = [
        f"공간 차지 없이 깔끔하게 정돈되는 건 기본이고, 쓸 때마다 편리해서 실용성에 감탄하게 됩니다.",
        f"일상의 불편했던 순간을 손쉽게 해결해 줘서 사용해 본 사람마다 극찬하는 이유가 있더라고요.",
        f"디자인도 깔끔한 데다 가성비까지 챙겨서 집안에 하나쯤 두면 무조건 돈값 하는 필수템입니다.",
        f"복잡한 조작 없이 1초 만에 깔끔하게 마무리되니까 라이프스타일이 한결 가벼워지는 느낌이에요."
    ]

    # 고정댓글 유도 멘트 묶음
    link_mentions = [
        "🔗 자세한 제품 스펙과 최저가 구매 링크는 지금 바로 고정 댓글을 확인해 보세요!",
        "🔗 어디서 사는지 궁금하신 분들은 아래 고정 댓글 링크를 터치해 주시면 됩니다!",
        "🔗 품절되기 전에 빠르게 확인해 보실 수 있도록 고정 댓글에 링크 남겨둘게요!"
    ]

    # 구독 유도 CTA 멘트 묶음
    sub_mentions = [
        f"🔔 더 유용한 가성비 꿀템 정보가 궁금하시다면 '{channel_name}' 구독과 좋아요 부탁드려요!",
        f"🔔 도움이 되셨다면 '{channel_name}' 팔로우하시고 매일 새로운 꿀템 정보를 가장 빠르게 받아보세요!",
        f"🔔 구독과 좋아요 눌러주시면 더 좋은 추천 영상 제작에 큰 힘이 됩니다! 💖"
    ]

    # 무작위 선택하여 조합
    hook = random.choice(hooks)
    body = random.choice(bodies)
    link = random.choice(link_mentions)
    sub = random.choice(sub_mentions)

    script_text = f"""[🔥 영상 #{idx} ({file_name}) 맞춤 쇼츠 대본 - {product_name}]

🎬 [00:00~00:03] 초반 후킹 (시선 고정)
"{hook}"

🎬 [00:03~00:15] 핵심 가치 및 실사용 장면
"{body}"

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내
"{link}"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"{sub}"
"""
    return script_text

# -------------------------------------------------------------------
# 3. 캡컷 드래프트 프로젝트 생성 함수
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

    # 캡컷 프로젝트 기본 구조 파일 생성
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
# 4. Streamlit UI
# -------------------------------------------------------------------
st.set_page_config(page_title="상훈's AI - 샤오홍슈 다채로운 대본 자동화", page_icon="✨", layout="wide")

st.title("✨ 상훈's AI - 샤오홍슈 맞춤 대본 & 캡컷 연동 스튜디오")
st.caption("어색한 멘트 없이 자연스럽고 다채로운 5가지 후킹 스타일 대본을 자동 조합합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_files = st.file_uploader(
        "🇨🇳 샤오홍슈 원본 영상(.mp4) 업로드 (최대 5개)", 
        type=["mp4", "mov"], 
        accept_multiple_files=True
    )
    
    if uploaded_files and len(uploaded_files) > 5:
        st.error("⚠️ 한 번에 최대 5개의 영상만 선택 가능합니다.")
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

        if st.button(f"🚀 영상 {len(uploaded_files)}개 일괄 분석 ➔ 자연스러운 대본 생성 & 캡컷 연동"):
            temp_dir = "temp_process"
            os.makedirs(temp_dir, exist_ok=True)
            
            all_scripts = []
            success_count = 0

            with st.spinner(f"📹 총 {len(uploaded_files)}개의 영상을 분석해 개별 맞춤 대본을 세팅 중..."):
                for idx, file in enumerate(uploaded_files, 1):
                    input_vpath = os.path.join(temp_dir, file.name)
                    with open(input_vpath, "wb") as f:
                        f.write(file.getbuffer())

                    current_proj_title = f"{project_base_title}_{idx:02d}_{file.name.split('.')[0]}"
                    
                    # 무작위 조합 다채로운 대본 생성
                    script_text = generate_dynamic_script(product_name, feature_desc, channel_name, idx, file.name)
                    all_scripts.append(script_text)

                    # 캡컷 드래프트 생성
                    success, msg = create_capcut_draft(current_proj_title, input_vpath, script_text)
                    if success:
                        success_count += 1

            st.session_state["combined_scripts"] = "\n\n" + ("="*50) + "\n\n".join(all_scripts)
            
            if success_count == len(uploaded_files):
                st.success(f"🎉 자연스러운 대본과 함께 {success_count}개 캡컷 프로젝트 생성이 완료되었습니다!")
                st.balloons()

with col2:
    st.subheader("📋 영상별 다채로운 대본 모음")
    if "combined_scripts" in st.session_state:
        st.text_area("✍️ 전체 영상 맞춤 타임라인 대본 (TTS 복사용)", value=st.session_state["combined_scripts"], height=480)
