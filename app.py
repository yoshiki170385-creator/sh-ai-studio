import os
import json
import shutil
import random
import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips

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
# 2. 다중 영상 1개로 자동 결합(Concatenate) 함수
# -------------------------------------------------------------------
def merge_videos(video_paths, output_path):
    clips = []
    try:
        for path in video_paths:
            clip = VideoFileClip(path)
            clips.append(clip)
        
        # 클립들을 순서대로 연결
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # 메모리 해제
        for clip in clips:
            clip.close()
        final_clip.close()
        return True
    except Exception as e:
        print(f"영상 병합 중 오류 발생: {e}")
        return False

# -------------------------------------------------------------------
# 3. 통합 쇼츠 대본 자동 생성기
# -------------------------------------------------------------------
def generate_single_integrated_script(product_name, feature_desc, channel_name, video_count):
    detail = f" {feature_desc}" if feature_desc else ""
    
    hooks = [
        f"다들 집에서 {product_name} 쓸 때 아직도 손으로 힘들게 하세요?",
        f"처음엔 속는 셈 치고 사봤는데... 와, {product_name} 이건 진짜 물건이네요!",
        f"모르고 지나쳤으면 계속 고생할 뻔했던 살림 꿀템 {product_name}{detail}!",
        f"요즘 쿠팡에서 후기 폭발하고 난리 난 {product_name}, 직접 써봤습니다.",
        f"비싼 브랜드 제품 다 필요 없고, {product_name} 하나면 완벽 해결입니다!"
    ]

    bodies = [
        f"공간 차지 없이 깔끔하게 정돈되는 건 기본이고, 쓸 때마다 편리해서 실용성에 감탄하게 됩니다.",
        f"일상의 불편했던 순간을 손쉽게 해결해 줘서 사용해 본 사람마다 극찬하는 이유가 있더라고요.",
        f"디자인도 깔끔한 데다 가성비까지 챙겨서 집안에 하나쯤 두면 무조건 돈값 하는 필수템입니다.",
        f"복잡한 조작 없이 1초 만에 깔끔하게 마무리되니까 라이프스타일이 한결 가벼워지는 느낌이에요."
    ]

    link_mentions = [
        "🔗 자세한 제품 스펙과 최저가 구매 링크는 지금 바로 고정 댓글을 확인해 보세요!",
        "🔗 어디서 사는지 궁금하신 분들은 아래 고정 댓글 링크를 터치해 주시면 됩니다!",
        "🔗 품절되기 전에 빠르게 확인해 보실 수 있도록 고정 댓글에 링크 남겨둘게요!"
    ]

    sub_mentions = [
        f"🔔 더 유용한 가성비 꿀템 정보가 궁금하시다면 '{channel_name}' 구독과 좋아요 부탁드려요!",
        f"🔔 도움이 되셨다면 '{channel_name}' 팔로우하시고 매일 새로운 꿀템 정보를 가장 빠르게 받아보세요!",
        f"🔔 구독과 좋아요 눌러주시면 더 좋은 추천 영상 제작에 큰 힘이 됩니다! 💖"
    ]

    script_text = f"""[🔥 {video_count}개 영상 자동 결합 통합 쇼츠 대본 - {product_name}]

🎬 [00:00~00:03] 초반 후킹 (1번 영상 장면)
"{random.choice(hooks)}"

🎬 [00:03~00:15] 핵심 가치 및 실사용 장면 (2~{video_count}번 영상 교체 장면)
"{random.choice(bodies)}"

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내
"{random.choice(link_mentions)}"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"{random.choice(sub_mentions)}"
"""
    return script_text

# -------------------------------------------------------------------
# 4. 캡컷 드래프트 프로젝트 생성 함수
# -------------------------------------------------------------------
def create_capcut_draft(project_name, merged_video_path, script_text):
    draft_root = get_capcut_draft_folder()
    if not draft_root:
        return False, "컴퓨터에서 캡컷(CapCut) 설치 경로를 찾지 못했습니다."

    project_dir = os.path.join(draft_root, project_name)
    os.makedirs(project_dir, exist_ok=True)

    # 병합된 최종 영상 복사
    target_video_path = os.path.join(project_dir, "main_video.mp4")
    shutil.copy(merged_video_path, target_video_path)

    # 대본 텍스트 파일 저장
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
# 5. Streamlit UI
# -------------------------------------------------------------------
st.set_page_config(page_title="상훈's AI - 다중 영상 자동 합성", page_icon="🎬", layout="wide")

st.title("🎬 상훈's AI - 영상 자동 병합 & 통합 대본 캡컷 스튜디오")
st.caption("3~5개 샤오홍슈 원본 영상을 1개로 연결하고, 이에 맞춘 통합 대본과 캡컷 프로젝트를 완성합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_files = st.file_uploader(
        "🇨🇳 병합할 샤오홍슈 원본 영상들 업로드 (3~5개 권장)", 
        type=["mp4", "mov"], 
        accept_multiple_files=True
    )
    
    project_title = st.text_input("📁 생성할 캡컷 프로젝트명", value="SH_Merged_Shorts_01")
    product_name = st.text_input("🏷️ 대표 상품명", value="휴대용 커피머신")
    feature_desc = st.text_input("✨ 상품 특징", value="가성비 꿀템")

    channel_option = st.radio("📺 워터마크 채널 선택:", ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"], horizontal=True)
    channel_name = st.text_input("채널명 직접 입력", value="꿀템창고") if channel_option == "직접 입력" else channel_option

    if uploaded_files:
        st.write(f"📁 **업로드된 영상: 총 {len(uploaded_files)}개**")
        for idx, file in enumerate(uploaded_files, 1):
            st.caption(f"{idx}. {file.name}")

        if len(uploaded_files) < 2:
            st.warning("⚠️ 영상 자동 병합을 위해 2개 이상의 영상을 선택해 주세요.")
        else:
            if st.button("🚀 영상 1개로 자동 병합 ➔ 통합 대본 생성 & 캡컷 내보내기"):
                temp_dir = "temp_process"
                os.makedirs(temp_dir, exist_ok=True)
                
                saved_video_paths = []
                for file in uploaded_files:
                    input_vpath = os.path.join(temp_dir, file.name)
                    with open(input_vpath, "wb") as f:
                        f.write(file.getbuffer())
                    saved_video_paths.append(input_vpath)

                merged_output_path = os.path.join(temp_dir, "merged_final.mp4")

                with st.spinner("🎬 영상들을 1개로 자동 결합 중입니다. 잠시만 기다려 주세요..."):
                    # 1. 영상 하나로 합성
                    success_merge = merge_videos(saved_video_paths, merged_output_path)
                    
                    if success_merge:
                        # 2. 통합 대본 작성
                        script_text = generate_single_integrated_script(
                            product_name, feature_desc, channel_name, len(uploaded_files)
                        )
                        st.session_state["single_script"] = script_text
                        st.session_state["merged_video"] = merged_output_path

                        # 3. 캡컷 드래프트 프로젝트 생성
                        success_capcut, msg = create_capcut_draft(project_title, merged_output_path, script_text)
                        
                        if success_capcut:
                            st.success(f"🎉 성공! 병합된 1개 영상으로 캡컷 프로젝트 '{project_title}' 생성을 완료했습니다.")
                            st.balloons()
                        else:
                            st.error(msg)
                    else:
                        st.error("❌ 영상 병합 처리 도중 오류가 발생했습니다.")

with col2:
    st.subheader("📊 병합된 최종 영상 및 통합 대본")
    if "merged_video" in st.session_state and os.path.exists(st.session_state["merged_video"]):
        st.video(st.session_state["merged_video"])
        st.text_area("✍️ 1개로 연결된 영상에 입힐 통합 대본 (TTS 복사용)", value=st.session_state.get("single_script", ""), height=280)
        st.info("""
💡 **최종 마무리 작업 방법:**
1. PC에서 **캡컷(CapCut)**을 실행합니다.
2. [최근 프로젝트]에 생긴 **새 프로젝트**를 클릭합니다.
3. 3~5개 영상이 순서대로 이어 붙여진 1개의 메인 비디오 트랙을 확인합니다.
4. 오른쪽에 작성된 통합 대본으로 **TTS 음성 및 자막**을 넣고 수출하시면 끝납니다!
""")
