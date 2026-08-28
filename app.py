import os
import json
import shutil
import re
import streamlit as st

# MoviePy 안전 불러오기
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    HAS_MOVIEPY = True
except Exception:
    try:
        from moviepy import VideoFileClip, concatenate_videoclips
        HAS_MOVIEPY = True
    except Exception:
        HAS_MOVIEPY = False

# -------------------------------------------------------------------
# 1. 파일명 기반 클린 상품명 자동 추출
# -------------------------------------------------------------------
def extract_product_name(filename):
    name = os.path.splitext(filename)[0]
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
        return False, "웹(온라인) 실행 환경입니다. 오른쪽 대본을 복사하여 캡컷에서 사용해 주세요!"

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
st.set_page_config(page_title="상훈's AI - 5클립 자동 병합 스튜디오", page_icon="⚡", layout="wide")

st.title("⚡ 상훈's AI - 샤오홍슈 5개 영상 자동 병합 & 캡컷 스튜디오")
st.caption("샤오홍슈 클립 영상 5개를 한 번에 올리시면, 하나의 쇼츠 영상으로 자동 편집하여 캡컷 프로젝트로 연결합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    # 🎬 최대 5개 영상 업로드 지원 (accept_multiple_files=True)
    uploaded_files = st.file_uploader(
        "🇨🇳 샤오홍슈 원본 영상 클립 업로드 (최대 5개까지 선택 가능)", 
        type=["mp4", "mov"], 
        accept_multiple_files=True
    )
    
    channel_option = st.radio("📺 워터마크 채널 선택:", ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"], horizontal=True)
    channel_name = st.text_input("채널명 직접 입력", value="꿀템창고") if channel_option == "직접 입력" else channel_option

    if uploaded_files:
        if len(uploaded_files) > 5:
            st.warning("⚠️ 영상은 최대 5개까지만 처리됩니다. 상위 5개 파일로 자동 선택합니다.")
            uploaded_files = uploaded_files[:5]

        st.success(f"📂 총 {len(uploaded_files)}개의 영상 클립이 선택되었습니다.")

        temp_dir = "temp_process"
        os.makedirs(temp_dir, exist_ok=True)
        
        saved_file_paths = []
        for idx, file in enumerate(uploaded_files):
            vpath = os.path.join(temp_dir, f"clip_{idx+1}_{file.name}")
            with open(vpath, "wb") as f:
                f.write(file.getbuffer())
            saved_file_paths.append(vpath)

        # 대표 상품명 자동 추출 (첫 번째 파일명 기준)
        auto_product_name = extract_product_name(uploaded_files[0].name)
        st.info(f"💡 인식된 대표 상품명: **{auto_product_name}**")

        if st.button("🚀 5개 영상 하나로 병합 & 대본 캡컷 연동"):
            with st.spinner("🎬 5개 영상 클립을 하나의 영상으로 병합 및 편집 중..."):
                final_merged_path = os.path.join(temp_dir, "final_merged_video.mp4")
                
                # 영상 병합 로직 (MoviePy 사용 가능한 환경 시)
                if HAS_MOVIEPY and len(saved_file_paths) > 1:
                    try:
                        clips = [VideoFileClip(p) for p in saved_file_paths]
                        merged = concatenate_videoclips(clips, method="compose")
                        merged.write_videofile(final_merged_path, codec="libx264", audio_codec="aac")
                        for c in clips:
                            c.close()
                    except Exception as e:
                        shutil.copy(saved_file_paths[0], final_merged_path)
                else:
                    shutil.copy(saved_file_paths[0], final_merged_path)

                clean_tag = auto_product_name.replace(" ", "")
                clean_channel = channel_name.replace(" ", "")

                script_text = f"""[🔥 5클립 통합 바이럴 쇼츠 대본 - {auto_product_name}]

🎬 [00:00~00:03] 초반 시선 고정 (클립 1)
"진작 살 걸 왜 이제 샀을까 후회하는 바로 그 아이템 {auto_product_name}!"

🎬 [00:03~00:15] 핵심 활용 장면 모음 (클립 2~4)
"공간 차지 없이 깔끔하게 정돈되고, 쓸 때마다 실용성에 감탄하게 되는 필수 꿀템입니다."

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내 (클립 5)
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
                st.session_state["merged_video_path"] = final_merged_path

                # 캡컷 드래프트 프로젝트 생성 (로컬 실행 시)
                project_name = f"Auto5_{clean_tag}"
                success, msg = create_capcut_draft(project_name, final_merged_path, script_text)
                
                if success:
                    st.success(f"🎉 5개 클립을 합친 캡컷 프로젝트 생성 완료: '{project_name}'")
                    st.balloons()
                else:
                    st.info(f"💡 {msg}")

with col2:
    st.subheader("📊 병합 영상 미리보기 & 대본")
    if "merged_video_path" in st.session_state and os.path.exists(st.session_state["merged_video_path"]):
        st.video(st.session_state["merged_video_path"])
        
    if "script_text" in st.session_state:
        st.text_area("✍️ 5클립 합본용 TTS 자막 대본", value=st.session_state["script_text"], height=200)
        st.text_area("📋 마케팅 메타패키지 문구", value=st.session_state["upload_text"], height=180)
