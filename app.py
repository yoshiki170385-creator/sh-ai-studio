import os
import json
import shutil
import re
import random
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
# 1. 파일명 기반 상품명 자동 추출
# -------------------------------------------------------------------
def extract_product_name(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[^\w\s가-힣]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name if name else "가성비 추천 꿀템"

# -------------------------------------------------------------------
# 2. 다양한 쇼츠 대본 랜덤 자동 생성기 (다양한 후킹 패턴)
# -------------------------------------------------------------------
def generate_dynamic_script(product_name, channel_name):
    # 1. 초반 3초 후킹 패턴 (다양화)
    hooking_list = [
        f"요즘 인스타랑 틱톡에서 난리 난 바로 그 {product_name}!",
        f"아니 이건 진짜 삶의 질이 달라집니다! {product_name} 직접 써봤는데요.",
        f"쿠팡에서 발견하자마자 장바구니 담아야 하는 {product_name}!",
        f"남들은 이미 몰래 편하게 쓰고 있었다는 {product_name} 숨은 꿀팁!",
        f"솔직히 이거 하나만 있어도 일상이 10배는 편해지는 {product_name}!"
    ]

    # 2. 중간 12초 상품 특징 강조 멘트 (다양화)
    body_list = [
        f"디자인도 깔끔한데 실용성까지 대박이라 쓸 때마다 감탄하게 됩니다. 진짜 돈값 제대로 하네요!",
        f"복잡하고 번거로웠던 과정들을 딱 1초 만에 해결해 줍니다. 써본 사람들이 입모아 극찬하는 이유가 있더라고요.",
        f"가성비는 기본이고 내구성까지 짱짱해서 사두면 무조건 뽕 뽑는 알짜배기 필수 아이템입니다.",
        f"공간 차지 없이 깔끔하게 어우러지면서 활용도가 너무 좋습니다. 지인한테 선물해 줘도 무조건 칭찬받을 꿀템이에요!"
    ]

    # 3. 고정댓글 유도 멘트 (다양화)
    comment_list = [
        "🔗 자세한 최저가 할인 정보와 스펙은 지금 바로 하단 고정 댓글 링크를 확인해 보세요!",
        "🔗 구매 정보가 궁금하신 분들은 아래 고정 댓글에 남겨둔 링크를 참고해 주세요!",
        "🔗 어디서 사는지 궁금하시다면 지금 바로 고정 댓글 링크를 터치해 보세요!"
    ]

    # 4. 구독 유도 CTA (다양화)
    cta_list = [
        f"🔔 매일 유용한 가성비 꿀템 정보가 궁금하다면 '{channel_name}' 구독과 좋아요 잊지 마세요!",
        f"🔔 도움이 되셨다면 '{channel_name}' 팔로우하시고 매일 핫한 살림 아이템 소식을 받아보세요!"
    ]

    script = f"""[🔥 5클립 통합 바이럴 쇼츠 대본 - {product_name}]

🎬 [00:00~00:03] 초반 시선 고정 (클립 1)
"{random.choice(hooking_list)}"

🎬 [00:03~00:15] 핵심 활용 장면 모음 (클립 2~4)
"{random.choice(body_list)}"

🎬 [00:15~00:22] 고정 댓글 구매 링크 안내 (클립 5)
"{random.choice(comment_list)}"

🎬 [00:22~00:28] 채널 구독 및 반응 유도 (CTA)
"{random.choice(cta_list)}"
"""
    return script

# -------------------------------------------------------------------
# 3. PC 내 캡컷(CapCut) 드래프트 경로 탐지 및 생성
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
# 4. Streamlit UI
# -------------------------------------------------------------------
st.set_page_config(page_title="상훈's AI - 5클립 자동 병합 스튜디오 Pro", page_icon="⚡", layout="wide")

st.title("⚡ 상훈's AI - 샤오홍슈 5개 영상 자동 병합 & 가변 대본 스튜디오")
st.caption("클립 영상 5개를 올리면, 다채로운 패턴의 대본과 1개의 합본 영상으로 캡컷 프로젝트를 완성합니다.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
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

        auto_product_name = extract_product_name(uploaded_files[0].name)
        st.info(f"💡 인식된 대표 상품명: **{auto_product_name}**")

        if st.button("🚀 5개 영상 하나로 병합 & 새로운 가변 대본 생성"):
            with st.spinner("🎬 5개 영상 클립 병합 및 새로운 대본을 조합하는 중..."):
                final_merged_path = os.path.join(temp_dir, "final_merged_video.mp4")
                
                if HAS_MOVIEPY and len(saved_file_paths) > 1:
                    try:
                        clips = [VideoFileClip(p) for p in saved_file_paths]
                        merged = concatenate_videoclips(clips, method="compose")
                        merged.write_videofile(final_merged_path, codec="libx264", audio_codec="aac")
                        for c in clips:
                            c.close()
                    except Exception:
                        shutil.copy(saved_file_paths[0], final_merged_path)
                else:
                    shutil.copy(saved_file_paths[0], final_merged_path)

                clean_tag = auto_product_name.replace(" ", "")
                clean_channel = channel_name.replace(" ", "")

                # 랜덤 가변 대본 생성
                script_text = generate_dynamic_script(auto_product_name, channel_name)
                
                upload_text = f"""=== [🔴 유튜브 쇼츠 상세 설명문 & 고정 댓글용] ===
요즘 sns에서 진짜 난리 난 필수 꿀템! 🔥
{auto_product_name} 솔직 후기 및 활용법 공개합니다! ✨

📌 [쿠팡 최저가 파트너스 구매 링크]
👉 https://www.coupang.com/np/search?q={auto_product_name}

#{clean_channel} #{clean_tag} #생활꿀템 #살림템 #{clean_tag}추천 #가성비템 #내돈내산
"""
                st.session_state["script_text"] = script_text
                st.session_state["upload_text"] = upload_text
                st.session_state["merged_video_path"] = final_merged_path

                project_name = f"Auto5_{clean_tag}"
                success, msg = create_capcut_draft(project_name, final_merged_path, script_text)
                
                if success:
                    st.success(f"🎉 캡컷 프로젝트 생성 완료: '{project_name}'")
                    st.balloons()
                else:
                    st.info(f"💡 {msg}")

with col2:
    st.subheader("📊 병합 영상 미리보기 & 신규 생성 대본")
    if "merged_video_path" in st.session_state and os.path.exists(st.session_state["merged_video_path"]):
        st.video(st.session_state["merged_video_path"])
        
    if "script_text" in st.session_state:
        st.text_area("✍️ 가변 조합된 신규 대본", value=st.session_state["script_text"], height=220)
        st.text_area("📋 마케팅 메타패키지 문구", value=st.session_state["upload_text"], height=160)
