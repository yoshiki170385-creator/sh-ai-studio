import time
import hmac
import hashlib
import requests
import json

def get_coupang_affiliate_link(keyword, access_key, secret_key):
    """
    키워드로 쿠팡 상품을 검색하여 첫 번째 상품의 쿠팡 파트너스 단축 링크(Deeplink)를 반환합니다.
    """
    if not access_key or not secret_key:
        return f"https://www.coupang.com/np/search?q={keyword}"

    # HMAC 서명 생성
    method = "POST"
    path = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    domain = "https://api-gateway.coupang.com"
    
    # 시간 설정
    datetime_gmt = time.strftime('%y%m%d', time.gmtime()) + 'T' + time.strftime('%H%M%S', time.gmtime()) + 'Z'
    message = datetime_gmt + method + path
    
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    authorization = f"CEA algorithm=HmacSHA256, access-key={access_key}, signed-date={datetime_gmt}, signature={signature}"
    
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }

    # 일반 검색 URL을 파트너스 수익 링크로 변환 요청
    target_url = f"https://www.coupang.com/np/search?q={keyword}"
    body = {
        "coupangUrls": [target_url]
    }

    try:
        response = requests.post(domain + path, headers=headers, data=json.dumps(body), timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("rCode") == "0" and result.get("data"):
                # 생성된 파트너스 단축 링크 반환
                short_url = result["data"][0].get("shortenUrl")
                return short_url
    except Exception as e:
        print(f"쿠팡 API 호출 실패: {e}")

    # API 호출 실패 시 일반 검색 링크 반환
    return target_url