import streamlit as st
from datetime import datetime, timedelta
import time

# 페이지 설정
st.set_page_config(page_title="스마트 알람시계", layout="centered")

# --- 1. 세션 상태(Session State) 초기화 ---
if "page" not in st.session_state:
    st.session_state.page = "main"  # 'main' 또는 'add'
if "alarms" not in st.session_state:
    # 기본 샘플 알람 예시 데이터 구조
    st.session_state.alarms = [
        {
            "id": 1,
            "name": "출근 알람",
            "date": datetime.now().date(),
            "time": datetime.now().time(),
            "sound": "기본 벨소리",
            "vibrate": True,
            "snooze": True,
            "snooze_interval": 5,
            "snooze_count": 3,
            "active": True
        }
    ]
if "alarm_id_counter" not in st.session_state:
    st.session_state.alarm_id_counter = 2

# --- 2. 헬퍼 함수 (남은 시간 계산) ---
def get_time_remaining_str(alarm_date, alarm_time):
    """현재 시간으로부터 알람까지 남은 시간을 계산하여 문자열로 반환"""
    now = datetime.now()
    alarm_datetime = datetime.combine(alarm_date, alarm_time)
    
    if alarm_datetime <= now:
        return "이미 지나간 알람입니다."
    
    diff = alarm_datetime - now
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    days_str = f"{diff.days}일 " if diff.days > 0 else ""
    hours_str = f"{hours}시간 " if hours > 0 or diff.days > 0 else ""
    return f"{days_str}{hours_str}{minutes}분 뒤에 울립니다."

# --- 3. 실시간 알람 체크 기능 (상단 고정) ---
# 메인 화면이나 추가 화면 진입 시 현재 시간과 비교하여 켜져 있는 알람이 있으면 팝업을 띄웁니다.
now_dt = datetime.now()
for alarm in st.session_state.alarms:
    if alarm["active"]:
        alarm_dt = datetime.combine(alarm["date"], alarm["time"])
        # 현재 시간과 분 단위까지 일치할 때 알람 발동 (초 단위 오차 고려)
        if alarm_dt.date() == now_dt.date() and alarm_dt.hour == now_dt.hour and alarm_dt.minute == now_dt.minute:
            st.toast
