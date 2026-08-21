def generate_viral_shopping_script(product_name, feature_desc, channel_name, viral_pattern, persona_type, coupang_url=""):
    detail = f" {feature_desc}" if feature_desc else ""
    
    # 1. 페르소나별 오프닝 수식어
    if "자취생" in persona_type:
        target_prefix = "좁은 자취방 공간 활용 극대화!"
        hook_questions = [
            f"원룸 사시는 분들 잠시만요! {product_name} 하나로 집 넓이가 달라집니다.",
            f"좁은 자취방에서 허덕이던 제 삶을 바꿔준 {product_name}{detail}!",
            f"자취 3년 차가 감탄한 역대급 가성비 꿀템, 바로 {product_name}입니다."
        ]
    elif "살림/주부" in persona_type:
        target_prefix = "주부 9단도 인정한 살림 필수템!"
        hook_questions = [
            f"살림 고수들 사이에서 입소문 난 {product_name}, 왜 다들 찾을까요?",
            f"매번 번거롭고 귀찮았던 집안일, {product_name}{detail} 하나로 끝냈습니다.",
            f"이거 모르고 살림했던 지난날이 억울할 정도인 {product_name}!"
        ]
    else: # 테크/직장인 및 일반
        target_prefix = "삶의 질 확 끌어올리는 가성비 템!"
        hook_questions = [
            f"돈 아끼고 시간 아껴주는 미친 가성비, {product_name} 솔직 후기입니다.",
            f"쓸 때마다 감탄 나오는 요즘 대세 아이템! 바로 {product_name}{detail}인데요.",
            f"아니 이 가격에 이 성능이 진짜 들어갔다고요?! {product_name} 직접 보여드립니다."
        ]

    # 2. 본문 문장 구조 다변화 (PAS 및 AIDA 혼합)
    bodys_problem = [
        f"매번 정리도 안 되고 불편하게 고생하셨던 경험 다들 있으시죠?",
        f"공간은 차지하고 쓸 때마다 번거로웠던 기존 제품들의 단점을 싹 잡았습니다.",
        f"반신반의하면서 사봤는데, 복잡했던 일상이 한결 가벼워지는 걸 바로 체감했어요."
    ]
    
    bodys_solution = [
        f"스마트한 구조와 세련된 디자인은 물론, {product_name}{detail} 특유의 실용성이 단연 돋보입니다.",
        f"내구성부터 디테일한 마감까지 완벽해서 써보면 바로 '돈값 제대로 한다'는 느낌이 딱 옵니다.",
        f"공간 효율성과 편리함을 한 번에 잡아내서 남녀노소 누구나 대만족할 수밖에 없는 필수템입니다."
    ]

    link_text = f" ({coupang_url})" if coupang_url else ""

    # 3. CTA 다변화
    link_mentions = [
        f"🔗 {target_prefix} 상세 스펙과 특가 구매 링크{link_text}는 지금 바로 아래 고정 댓글을 확인하세요!",
        f"🔗 고민은 배송만 늦출 뿐! 최저가 확인{link_text}은 하단 고정 댓글 상단 링크를 터치해 주세요!",
        f"🔗 제품 정보와 구매처{link_text}가 궁금하시다면 아래 고정 댓글을 확인해 보세요!"
    ]

    sub_mentions = [
        f"🔔 매일 업로드되는 가성비 살림 정보가 궁금하다면? '{channel_name}' 구독과 좋아요 클릭!",
        f"🔔 정보가 유용하셨다면 '{channel_name}' 구독 누르시고 매일 숨은 꿀템 소식을 챙겨가세요!",
        f"🔔 구독과 좋아요는 더 좋은 추천 콘텐츠 제작에 큰 힘이 됩니다! 💖"
    ]

    # 무작위 조합
    script = f"""[🔥 10만+ 뷰 바이럴 쇼츠 대본 - {product_name}]

(0~3초 초반 후킹 - 시선 고정)
{random.choice(hook_questions)}

(4~15초 핵심 문제 제기 및 해결)
{random.choice(bodys_problem)}
{random.choice(bodys_solution)}

(16~22초 고정 댓글 링크 클릭 유도)
{random.choice(link_mentions)}

(23~28초 구독 및 반응 유도 CTA)
{random.choice(sub_mentions)}
"""
    return script
