import os
import random
import streamlit as st
import numpy as np

# MoviePy import
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips

# 캡컷 exporter
try:
    from capcut_exporter import export_to_capcut_draft
except ImportError:
    try:
        from src.capcut_exporter import export_to_capcut_draft
    except ImportError:
        export_to_capcut_draft = None

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

# -------------------------------------------------------------------
# 페이지 기본 설정 및 모바일(반응형) UI 최적화
# -------------------------------------------------------------------
st.set_page_config(
    page_title="상훈's AI Studio",
    page_icon="✨",
    layout="wide"
)

# 모바일 화면 가독성 향상 반응형 CSS
st.markdown("""
    <style>
    /* 배경 파스텔 톤 및 글꼴 기본 설정 */
    .stApp {
        background: linear-gradient(135deg, #FAFAFC 0%, #F0F4FF 50%, #FFF0F5 100%);
        color: #2D3748;
    }
    h1 { color: #4A5568 !important; font-weight: 800; }
    h3, .stCaption { color: #718096 !important; }
    
    /* 입력 위젯 모바일 맞춤 디자인 */
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        color: #2D3748 !important;
        font-size: 16px !important; /* 모바일 터치 시 자동 확대 방지 */
    }
    
    /* 모바일 풀사이즈 터치 버튼 */
    .stButton > button {
        background: linear-gradient(90deg, #A78BFA 0%, #F472B6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important; /* 모바일 풀 너비 버튼 */
        box-shadow: 0 4px 14px 0 rgba(167, 139, 250, 0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(244, 114, 182, 0.45) !important;
    }

    /* 모바일 작은 화면 대응 여백 조절 */
    @media (max-width: 768px) {
        .stApp { padding: 10px !important; }
        h1 { font-size: 24px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 사이드바: 쿠팡 파트너스 API 키 설정
# -------------------------------------------------------------------
with st.sidebar:
    st.header("🔑 쿠팡 파트너스 API 설정")
    cp_access_key = st.text_input("Access Key", value="", type="password", key="cp_ak")
    cp_secret_key = st.text_input("Secret Key", value="", type="password", key="cp_sk")
    st.caption("API 키 입력 시 쿠팡 상품 이미지와 수익 링크가 자동 발급됩니다.")

# 메인 타이틀
st.title("✨ 상훈's AI 콘텐츠 스튜디오 Pro")
st.caption("📱 모바일 기기 완벽 지원: 10만+ 뷰 대본, 쿠팡 파트너스 연동, 캡컷 내보내기")
st.markdown("---")

# -------------------------------------------------------------------
# 10만+ 뷰 바이럴 대본 생성 함수
# -------------------------------------------------------------------
def generate_viral_shopping_script(product_name, feature_desc, channel_name, viral_pattern, coupang_url=""):
    detail = f" {feature_desc}" if feature_desc else ""
    
    if "진작 살걸" in viral_pattern:
        openings = [
            f"진작 살 걸 왜 이제 샀을까 고민했던 바로 그 아이템!",
            f"쓰자마자 삶의 질 3배 상승해서 난리 난 {product_name}!",
            f"안 써본 사람은 있어도 한 번만 써본 사람은 없다는 {product_name}{detail}!",
            f"요즘 인스타에서 반응 폭발한 살림 꿀템, {product_name} 솔직 사용 후기입니다!"
        ]
        bodys = [
            f"공간 차지 없이 깔끔하게 정돈되는 건 기본이고, 쓸 때마다 실용성에 감탄하게 됩니다.",
            f"일상의 불편했던 순간들을 손쉽게 해결해 줘서 사용해 본 사람마다 극찬하는 이유를 알겠더라고요.",
            f"실제 사용해 보니 디자인부터 성능까지 완벽해서 사두면 돈값 제대로 하는 필수템입니다."
        ]
    elif "가성비" in viral_pattern or "돈 아끼는" in viral_pattern:
        openings = [
            f"잠시만요! 이거 모르고 {product_name} 비싸게 사면 무조건 손해입니다!",
            f"아니 이 가격에 이 퀄리티가 말이 되나요?! 가성비 미쳤다는 {product_name}!",
            f"쿠팡에서 발견한 역대급 가성비 꿀템 {product_name}{detail} 직접 써봤습니다.",
            f"돈 아껴주는 살림 필수템 찾으셨나요? {product_name} 이거 진짜 물건이네요!"
        ]
        bodys = [
            f"비싼 브랜드 제품 부럽지 않은 가성비에 내구성까지 짱짱해서 정말 만족스럽습니다.",
            f"가격 대비 성능이 기대 이상이라 고민할 시간에 빠르게 가져가시는 걸 추천합니다.",
            f"일상에서 자주 쓰게 되니까 사두면 뽕을 뽑고도 남는 알짜배기 아이템이에요."
        ]
    else:
        openings = [
            f"살림 고수들만 몰래 쓴다는 숨은 꿀템, 오늘 싹 공개합니다!",
            f"아는 사람들만 입소문 타고 쓰던 {product_name}{detail} 드디어 가져왔습니다.",
            f"알아두면 무조건 유용한 살림 꿀팁! 바로 이 {product_name} 하나면 종결입니다.",
            f"남들은 이미 편하게 쓰고 있던 {product_name}, 왜 나만 몰랐을까요?"
        ]
        bodys = [
            f"집안 어디에 놓아도 깔끔하게 어우러지면서 스마트하게 일상을 바꿔줍니다.",
            f"번거로웠던 과정들을 1초 만에 줄여주니 라이프스타일이 한결 가벼워지는 느낌이에요.",
            f"지인들에게 추천하거나 선물해 줘도 무조건 칭찬받을 가성비 꿀템입니다."
        ]

    link_text = f" ({coupang_url})" if coupang_url else ""

    link_mentions = [
        f"🔗 자세한 제품 스펙과 구매 링크{link_text}는 지금 바로 아래 고정 댓글을 확인해 보세요!",
        f"🔗 최저가 구매 정보{link_text}는 하단 고정 댓글의 링크를 참고해 주시면 됩니다!",
        f"🔗 어디서 사는지 궁금하신 분들은 아래 고정 댓글 링크{link_text}를 터치해 주세요!"
    ]

    sub_mentions = [
        f"🔔 더 유용한 가성비 꿀템 정보가 궁금하다면? '{channel_name}' 구독과 좋아요 부탁드려요!",
        f"🔔 도움이 되셨다면 '{channel_name}' 구독하시고 매일 새로운 꿀템 정보를 가장 빠르게 받아보세요!",
        f"🔔 구독과 좋아요 눌러주시면 더 좋은 가성비 추천 영상 제작에 큰 힘이 됩니다! 💖"
    ]

    script = f"""[🔥 10만+ 뷰 바이럴 쇼츠 대본 - {product_name}]

(0~3초 초반 후킹 - 시선 고정)
{random.choice(openings)}

(4~15초 핵심 가치 및 문제 해결)
{random.choice(bodys)}

(16~22초 고정 댓글 링크 클릭 유도)
{random.choice(link_mentions)}

(23~28초 구독 및 반응 유도 CTA)
{random.choice(sub_mentions)}
"""
    return script

def generate_playlist_script(playlist_title, music_genre, channel_name):
    script = f"""[플레이리스트 대본 - {playlist_title}]
안녕하세요, {channel_name}에 오신 것을 환영합니다.
오늘 선곡한 음악은 {playlist_title} 입니다.
지친 일상 속 잠시 쉬어가고 싶을 때, 따뜻한 음료 한 잔과 함께 깊은 휴식을 누려보세요.
구독과 좋아요는 감성적인 음악 콘텐츠 제작에 큰 힘이 됩니다.
"""
    return script

# -------------------------------------------------------------------
# 메인 탭 구성
# -------------------------------------------------------------------
tab1, tab2 = st.tabs(["🛍️ 쇼핑 리뷰 쇼츠", "🎧 수노 AI 롱폼 플레이리스트"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ 쇼핑 쇼츠 설정 및 바이럴 대본")
        folder_path = st.text_input("📁 작업 폴더명", value="Coffee_", key="shop_folder")
        product_name = st.text_input("🏷️ 상품명", value="휴대용커피머신", key="shop_pname")
        feature_desc = st.text_input("✨ 상품 특징", value="가성비 꿀템", key="shop_fdesc")
        
        st.write("📺 **브랜딩 하단 워터마크 채널 선택**")
        channel_option = st.radio(
            "채널을 선택하세요:",
            ["템빨item빨", "굿템빨", "핫템리뷰", "직접 입력"],
            horizontal=True,
            key="shop_ch_radio"
        )
        if channel_option == "직접 입력":
            channel_name = st.text_input("채널명 직접 입력", value="꿀템창고", key="shop_custom_ch")
        else:
            channel_name = channel_option

        st.write("🔥 **10만+ 뷰 바이럴 영상 패턴 선택**")
        viral_pattern = st.selectbox(
            "인기 쇼츠의 대표 바이럴 패턴을 지정하세요:",
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
            st.session_state["shop_script_box"] = generate_viral_shopping_script(
                product_name, feature_desc, channel_name, viral_pattern, info["shortenUrl"]
            )

        if "shop_script_box" not in st.session_state:
            update_script_and_product()

        st.button("💡 상품 검색 & 10만뷰 대본 생성", key="btn_script", on_click=update_script_and_product)

        cp_info = st.session_state.get("cp_info", {})
        if cp_info and cp_info.get("productImage"):
            st.markdown("---")
            st.write("🔍 **쿠팡에서 찾은 매칭 상품 미리보기**")
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                st.image(cp_info["productImage"], width=150)
            with p_col2:
                st.markdown(f"**상품명:** {cp_info['productName']}")
                st.markdown(f"**가격:** {cp_info['productPrice']}")
                st.markdown(f"**수익 링크:** [{cp_info['shortenUrl']}]({cp_info['shortenUrl']})")
            st.markdown("---")

        script_val = st.text_area(
            "✍️ 초반 후킹 및 바이럴 대본 (복사하여 TTS에 사용하세요)",
            height=260,
            key="shop_script_box"
        )

        start_btn = st.button("🚀 캡컷 편집용 쇼츠 영상 생성", key="btn_shop")

    with col2:
        st.subheader("📊 미리보기 및 쿠팡 파트너스 마케팅 문구")

    if start_btn:
        if not os.path.exists(folder_path):
            st.error(f"❌ '{folder_path}' 폴더가 존재하지 않습니다. 폴더명을 다시 확인해 주세요.")
        else:
            with st.spinner("📹 캡컷 프로젝트 트랙용 영상을 구성 중입니다..."):
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                
                video_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mov'))])
                image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
                
                if not video_files and not image_files:
                    st.error(f"❌ '{folder_path}' 폴더 내에 영상(.mp4) 또는 이미지(.jpg, .png) 파일이 없습니다.")
                else:
                    audio_p = None
                    srt_p = os.path.join(folder_path, "subtitle.srt")
                    for f in os.listdir(folder_path):
                        if f.lower().endswith(('.mp3', '.wav')):
                            audio_p = os.path.join(folder_path, f)
                            break

                    video_clips = []
                    if video_files:
                        video_clips = [VideoFileClip(v_file) for v_file in video_files]
                    else:
                        for img_p in image_files:
                            img_clip = ImageClip(img_p)
                            img_clip = img_clip.set_duration(3.0) if hasattr(img_clip, "set_duration") else img_clip.with_duration(3.0)
                            video_clips.append(img_clip)

                    merged_video = concatenate_videoclips(video_clips, method="compose")

                    if audio_p and os.path.exists(audio_p):
                        audio = AudioFileClip(audio_p)
                        if merged_video.duration < audio.duration:
                            loop_cnt = int(audio.duration // merged_video.duration) + 1
                            merged_video = concatenate_videoclips([merged_video] * loop_cnt, method="compose")
                            merged_video = merged_video.subclip(0, audio.duration)
                            
                        merged_video = merged_video.set_audio(audio) if hasattr(merged_video, "set_audio") else merged_video.with_audio(audio)

                    out_video_p = os.path.join(output_dir, "final_shorts.mp4")
                    merged_video.write_videofile(out_video_p, codec="libx264", audio_codec="aac")

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

구독과 좋아요, 알림 설정 눌러주시면 더 좋은 꿀템 정보를 빠르게 받아보실 수 있습니다! 🔔💖

#{clean_channel} #{clean_tag} #생활꿀템 #살림템 #{clean_tag}추천 #가성비템 #꿀템추천 #내돈내산 #인기아이템

SEO 태그(10개)
{clean_channel}, {product_name}, {clean_tag}, 생활꿀템, 살림템, 가성비템, {clean_tag}추천, 꿀템추천, 필수템, 쇼핑추천


=== [🎵 틱톡 상세 설명] ===
직접 써보고 삶의 질 확 끌어올린 {product_name}🔥
{cp_link}

고민할 시간에 빠르게 가져가세요! ✨
팔로우하고 더 유용한 꿀템 정보 받아보기 💜


=== [📸 인스타 릴스 상세 캡션] ===
아 진짜 왜 이제야 알았지? 🫠
쓰면 쓸수록 만족도 최고인 {product_name}! ✨{desc_detail}

📌 구매 링크: {cp_link}
💜 '{clean_channel}' 팔로우 누르시고 댓글로 '{product_name}' 남겨주시면 링크를 DM으로도 빠르게 보내드릴게요! 💌
"""
                    info_p = os.path.join(output_dir, "upload_info.txt")
                    with open(info_p, "w", encoding="utf-8") as f:
                        f.write(upload_text)

                    if export_to_capcut_draft:
                        try:
                            export_to_capcut_draft(
                                video_path=out_video_p,
                                audio_path=audio_p,
                                srt_path=srt_p,
                                project_name=f"Check_{clean_tag}"
                            )
                        except Exception as e:
                            print(f"캡컷 드래프트 내보내기 중 참고: {e}")

                    st.success("🎉 상훈's AI 프로젝트 생성이 완료되었습니다!")
                    with col2:
                        st.video(out_video_p)
                        st.text_area("📋 [쿠팡 파트너스 링크가 포함된 마케팅 문구]", value=upload_text, height=350)

# ===================================================================
# TAB 2: 수노 AI 롱폼 플레이리스트 자동화
# ===================================================================
with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("🎵 수노 AI 롱폼 플레이리스트 설정")
        pl_folder = st.text_input("📁 음원/배경 폴더명", value="Music_01", key="pl_folder")
        playlist_title = st.text_input("📻 플레이리스트 주제", value="비 오는 날 카페에서 듣기 좋은 감성 로파이 모음", key="pl_title")
        song_title = st.text_input("🎶 메인 곡명 / 아티스트", value="Rainy Memory - Suno AI", key="pl_song")
        music_genre = st.text_input("🎸 대표 장르 / 분위기", value="Lofi / Chill / Cafe Music", key="pl_genre")
        
        st.write("📺 **플레이리스트 워터마크 채널 선택**")
        pl_ch_option = st.radio("채널 선택:", ["애니한 뮤직", "굿템빨", "템빨item빨", "직접 입력"], horizontal=True, key="pl_ch_radio")
        if pl_ch_option == "직접 입력":
            pl_channel = st.text_input("채널명 직접 입력", value="감성사운드", key="pl_custom_ch")
        else:
            pl_channel = pl_ch_option

        st.write("📝 **상훈's AI 플레이리스트 오프닝 대본 생성기**")

        def update_pl_script():
            st.session_state["pl_script_box"] = generate_playlist_script(playlist_title, music_genre, pl_channel)

        if "pl_script_box" not in st.session_state:
            st.session_state["pl_script_box"] = generate_playlist_script(playlist_title, music_genre, pl_channel)

        st.button("💡 감성 오프닝 대본 생성하기", key="btn_pl_script", on_click=update_pl_script)

        pl_script_val = st.text_area(
            "✍️ 생성된 오프닝 대본",
            height=140,
            key="pl_script_box"
        )

        start_pl_btn = st.button("🎧 캡컷 롱폼 플레이리스트 생성", key="btn_pl")

    with col2:
        st.subheader("📊 미리보기 및 캡컷 가이드")

    if start_pl_btn:
        if not os.path.exists(pl_folder):
            st.error(f"❌ '{pl_folder}' 폴더가 존재하지 않습니다.")
        else:
            with st.spinner("🎧 음원 길이에 맞춰 캡컷 롱폼 트랙을 생성 중입니다..."):
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                
                bg_files = sorted([os.path.join(pl_folder, f) for f in os.listdir(pl_folder) if f.lower().endswith(('.mp4', '.mov'))])
                bg_imgs = sorted([os.path.join(pl_folder, f) for f in os.listdir(pl_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
                
                audio_p = None
                for f in os.listdir(pl_folder):
                    if f.lower().endswith(('.mp3', '.wav')):
                        audio_p = os.path.join(pl_folder, f)
                        break

                if not audio_p:
                    st.error("❌ 폴더 내에 음원 파일(.mp3 또는 .wav)이 없습니다.")
                elif not bg_files and not bg_imgs:
                    st.error("❌ 폴더 내에 배경 영상(.mp4) 또는 배경 이미지(.jpg, .png)가 없습니다.")
                else:
                    audio = AudioFileClip(audio_p)
                    song_duration = audio.duration
                    
                    if bg_files:
                        bg_clips = [VideoFileClip(v) for v in bg_files]
                    else:
                        bg_clips = [ImageClip(img_p).set_duration(song_duration) for img_p in bg_imgs]
                        
                    merged_bg = concatenate_videoclips(bg_clips, method="compose")
                    
                    if merged_bg.duration < song_duration:
                        loop_count = int(song_duration // merged_bg.duration) + 1
                        merged_bg = concatenate_videoclips([merged_bg] * loop_count, method="compose")
                    
                    merged_bg = merged_bg.subclip(0, song_duration)
                    merged_bg = merged_bg.set_audio(audio) if hasattr(merged_bg, "set_audio") else merged_bg.with_audio(audio)

                    out_video_p = os.path.join(output_dir, "final_longform_playlist.mp4")
                    merged_bg.write_videofile(out_video_p, codec="libx264", audio_codec="aac")

                    clean_tag = playlist_title.replace(" ", "")
                    clean_channel = pl_channel.replace(" ", "")
                    
                    seo_package_text = f"""=== [📌 유튜브 롱폼 SEO 최적화 제목] ===
1. [Playlist] {playlist_title} ☕✨ | {music_genre}
2. 푹 쉬고 싶을 때 듣는 {playlist_title} 🎶 | {pl_channel}

=== [🔴 유튜브 롱폼 상세 설명문 & 타임스탬프] ===
안녕하세요, {pl_channel} 채널에 방문해 주셔서 감사합니다! ☕✨

오늘 선곡한 플레이리스트는 '{playlist_title}' 입니다.
복잡한 일상 속 집중이 필요하거나 편안한 휴식을 누리고 싶을 때 따뜻한 차 한 잔과 함께 감상해 보세요 🎶

[Tracklist & Timestamps]
00:00 {song_title}

📌 Notice:
- 구독과 좋아요, 알림 설정은 다음 감성 플레이리스트 제작에 큰 힘이 됩니다! ☕💖

=== [🏷️ 유튜브 SEO 해시태그] ===
#{clean_channel} #{clean_tag} #수노AI #SunoAI #플레이리스트 #Lofi #카페음악

=== [🔍 유튜브 알고리즘 노출용 키워드 태그 (10개)] ===
{pl_channel}, {playlist_title}, {music_genre}, 수노AI, SunoAI, 플레이리스트
"""
                    info_p = os.path.join(output_dir, "longform_seo_info.txt")
                    with open(info_p, "w", encoding="utf-8") as f:
                        f.write(seo_package_text)

                    srt_p = os.path.join(pl_folder, "subtitle.srt")

                    if export_to_capcut_draft:
                        try:
                            export_to_capcut_draft(
                                video_path=out_video_p,
                                audio_path=audio_p,
                                srt_path=srt_p,
                                project_name=f"Playlist_{clean_tag}"
                            )
                        except Exception as e:
                            print(f"캡컷 드래프트 내보내기 중 참고: {e}")

                    st.success("🎉 상훈's AI 롱폼 드래프트 프로젝트 생성이 완료되었습니다!")
                    with col2:
                        st.video(out_video_p)
                        st.text_area("📋 [SEO 상세 메타패키지]", value=seo_package_text, height=350)