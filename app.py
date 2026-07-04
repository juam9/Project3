import streamlit as st
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(page_title="스마트 알람시계", layout="centered")

# --- 1. 세션 상태(Session State) 초기화 ---
if "page" not in st.session_state:
    st.session_state.page = "main"  # 'main' 또는 'add'
if "alarms" not in st.session_state:
    # 기본 샘플 알람 데이터 구조
    st.session_state.alarms = [
        {
            "id": 1,
            "name": "기상 알람",
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

# --- 2. 남은 시간 계산 함수 ---
def get_time_remaining_str(alarm_date, alarm_time):
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

# --- 3. 실시간 알람 체크 (화면 상단 알림) ---
now_dt = datetime.now()
for alarm in st.session_state.alarms:
    if alarm["active"]:
        alarm_dt = datetime.combine(alarm["date"], alarm["time"])
        if alarm_dt.date() == now_dt.date() and alarm_dt.hour == now_dt.hour and alarm_dt.minute == now_dt.minute:
            st.toast(f"⏰ [{alarm['name']}] 알람 시간이 되었습니다!", icon="🔔")
            st.error(f"🚨 **{alarm['name']}** 알람 작동 중! (음악: {alarm['sound']} / 진동: {'ON' if alarm['vibrate'] else 'OFF'})")

# --- 4. 화면 라우팅 (페이지 전환) ---

# ==================== [메인 화면] ====================
if st.session_state.page == "main":
    st.title("⏰ 스마트 알람시계")
    st.subheader("나의 알람 목록")
    st.write(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown("---")
    
    # 등록된 알람 목록 출력
    if not st.session_state.alarms:
        st.info("설정된 알람이 없습니다. 아래 + 버튼을 눌러 추가해 보세요!")
    else:
        for idx, alarm in enumerate(st.session_state.alarms):
            with st.container(border=True):
                col_info, col_toggle = st.columns([7, 2])
                
                with col_info:
                    st.markdown(f"### **{alarm['name']}**")
                    st.markdown(f"📅 **일시:** {alarm['date']}  |  🕒 **시간:** {alarm['time'].strftime('%H:%M')}")
                    
                    if alarm["active"]:
                        remaining_text = get_time_remaining_str(alarm["date"], alarm["time"])
                        st.caption(f"⏳ {remaining_text}")
                    else:
                        st.caption("⚪ 알람이 꺼져 있습니다.")
                        
                    st.caption(f"🎵 {alarm['sound']} | 📳 진동: {'ON' if alarm['vibrate'] else 'OFF'} | 🔄 다시울림: {'ON ('+str(alarm['snooze_interval'])+'분 간격)' if alarm['snooze'] else 'OFF'}")
                
                with col_toggle:
                    st.write("")  # 여백
                    is_active = st.toggle("켜기/끄기", value=alarm["active"], key=f"toggle_{alarm['id']}")
                    if is_active != alarm["active"]:
                        st.session_state.alarms[idx]["active"] = is_active
                        st.rerun()
                        
    st.markdown("---")
    
    # 알람 추가 버튼 (+ 버튼)
    col_btn, _ = st.columns([4, 5])
    with col_btn:
        if st.button("➕ 알람 추가하기", type="primary", use_container_width=True):
            st.session_state.page = "add"
            st.rerun()

# ==================== [알람 추가 화면] ====================
elif st.session_state.page == "add":
    st.title("➕ 새 알람 추가")
    st.write("알람 세부 설정을 입력하세요.")
    st.markdown("---")
    
    # 1. 시간 설정 (가장 위쪽 배치)
    st.markdown("### 🕒 1. 시간 설정")
    input_time = st.time_input("시간을 선택하세요", value=datetime.now().time())
    
    st.markdown("---")
    st.markdown("### ⚙️ 2. 상세 정보 입력")
    
    # 2. 알람 이름
    input_name = st.text_input("알람 이름", value="새 알람")
    
    # 3. 날짜
    input_date = st.date_input("날짜 설정", value=datetime.now().date())
    
    # 4. 알람음 설정
    input_sound = st.selectbox("알람음 선택", ["기본 벨소리", "새소리", "잔잔한 피아노", "사이렌"])
    
    # 5. 진동 설정
    input_vibrate = st.checkbox("진동 켜기", value=True)
    
    # 6. 다시울림 설정
    input_snooze = st.checkbox("다시울림(스누즈) 활성화", value=False)
    
    input_snooze_interval = 5
    input_snooze_count = 3
    if input_snooze:
        col_inv, col_cnt = st.columns(2)
        with col_inv:
            input_snooze_interval = st.number_input("다시울림 간격 (분)", min_value=1, max_value=60, value=5)
        with col_cnt:
            input_snooze_count = st.number_input("반복 횟수 (회)", min_value=1, max_value=10, value=3)

    st.markdown("---")
    
    # 저장 및 취소 버튼
    col_save, col_cancel = st.columns(2)
    
    with col_save:
        if st.button("💾 알람 등록", type="primary", use_container_width=True):
            new_alarm = {
                "id": st.session_state.alarm_id_counter,
                "name": input_name,
                "date": input_date,
                "time": input_time,
                "sound": input_sound,
                "vibrate": input_vibrate,
                "snooze": input_snooze,
                "snooze_interval": input_snooze_interval,
                "snooze_count": input_snooze_count,
                "active": True
            }
            st.session_state.alarms.append(new_alarm)
            st.session_state.alarm_id_counter += 1
            
            st.session_state.page = "main"
            st.success("알람이 등록되었습니다!")
            time.sleep(0.5)
            st.rerun()
            
    with col_cancel:
        if st.button("❌ 취소", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()
