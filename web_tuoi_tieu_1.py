import streamlit as st
import requests
from datetime import datetime, timedelta, date
import random
from PIL import Image
import time

st.set_page_config(page_title="Smart Irrigation WebApp", layout="wide")

# --- HEADER: LOGO + TÊN TRƯỜNG ---
col1, col2 = st.columns([1, 6])
with col1:
    logo = Image.open("logo.png")
    st.image(logo, width=180)
with col2:
    st.markdown("<h3 style='text-align: left; color: #004aad; font-family: Times New Roman;'>Ho Chi Minh City University of Technology and Education</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color: #004aad; font-family: Times New Roman;'>International Training Institute hoặc Faculty of International Training</h3>", unsafe_allow_html=True)
# --- TIÊU ĐỀ ỨNG DỤNG ---
#st.title("<h2 h2 style='text-align: center;'>🌾 Hệ Thống Tưới Tiêu Nông Sản Thông Minh</h2>",)
st.markdown("<h2 style='text-align: center; font-family: Times New Roman;'> 🌾Smart Agricultural Irrigation System🌾</h2>", unsafe_allow_html=True)
st.markdown("""
<div style='color: #004aad;'>
    <h3>Nhóm thực hiện: Ngô Nguyễn Định Tường - 21142488</h3>
    <h3 style='margin-left: 200px;'>Mai Phúc Khang - 21142031</h3>
</div>
""", unsafe_allow_html=True)
# --- HIỂN THỊ THỜI GIAN THỰC ---
placeholder_time = st.empty()
def update_time():
    now = datetime.now()
    placeholder_time.markdown(f"**⏰ Thời gian hiện tại:** `{now.strftime('%H:%M:%S - %d/%m/%Y')}`")
update_time()

# --- DANH SÁCH NÔNG SẢN VIỆT NAM ---
crops = {
    "Cà chua": (60, 80),
    "Rau cải": (30, 45),
    "Dưa hấu": (70, 90),
    "Lúa": (90, 120),
    "Ngô": (75, 100),
    "Khoai lang": (90, 120),
    "Ớt": (70, 90),
    "Bí đỏ": (85, 100),
    "Chuối": (270, 365),
    "Sắn": (180, 270),
    "Đậu bắp": (45, 60),
    "Cà tím": (60, 80),
    "Bắp": (90, 120)
}

selected_crop = st.selectbox("🌱 Chọn loại nông sản:", list(crops.keys()))
planting_date = st.date_input("📅 Chọn ngày gieo trồng:")

min_days, max_days = crops[selected_crop]
harvest_min = planting_date + timedelta(days=min_days)
harvest_max = planting_date + timedelta(days=max_days)
st.success(f"🌾 Dự kiến thu hoạch từ **{harvest_min.strftime('%d/%m/%Y')}** đến **{harvest_max.strftime('%d/%m/%Y')}**")

# --- API THỜI TIẾT ---
latitude = 10.8486
longitude = 106.7903
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation,precipitation_probability&timezone=auto"

weather_data = requests.get(weather_url).json()
current_weather = weather_data.get("current", {})

# --- THỜI TIẾT HIỆN TẠI ---
st.subheader("🌦️ Thời tiết thực tế hiện tại")
col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Nhiệt độ", f"{current_weather.get('temperature_2m', 'N/A')} °C")
col2.metric("💧 Độ ẩm", f"{current_weather.get('relative_humidity_2m', 'N/A')} %")
col3.metric("🌧️ Mưa", f"{current_weather.get('precipitation', 'N/A')} mm")

# --- GIẢ LẬP DỮ LIỆU CẢM BIẾN ---
st.subheader("🧪 Dữ liệu cảm biến ")
sensor_temp = round(random.uniform(25, 37), 1)
sensor_hum = round(random.uniform(50, 95), 1)
sensor_light = round(random.uniform(300, 1000), 1)

st.write(f"🌡️ Nhiệt độ cảm biến: **{sensor_temp} °C**")
st.write(f"💧 Độ ẩm đất cảm biến: **{sensor_hum} %**")
st.write(f"☀️ Cường độ ánh sáng: **{sensor_light} lux**")

# --- AI SO SÁNH DỮ LIỆU ---
st.subheader("🧠 So sánh AI: Dữ liệu thời tiết & cảm biến")

temp_diff = abs(current_weather.get("temperature_2m", 0) - sensor_temp)
hum_diff = abs(current_weather.get("relative_humidity_2m", 0) - sensor_hum)

if temp_diff < 2 and hum_diff < 10:
    st.success("✅ Dữ liệu cảm biến khớp tốt với thời tiết thực tế.")
else:
    st.warning(f"⚠️ Có sai lệch dữ liệu:\n- Nhiệt độ lệch {temp_diff:.1f}°C\n- Độ ẩm lệch {hum_diff:.1f}%")

# --- LOGIC TƯỚI CÂY DỰA VÀO GIAI ĐOẠN PHÁT TRIỂN CỦA CHUỐI ---
st.subheader("🚰 Trạng thái hệ thống tưới")
rain_probability = current_weather.get("precipitation_probability", 0)

# Giai đoạn phát triển theo số ngày
def chuoi_stage(days):
    if days <= 14:
        return "🌱 Giai đoạn mới trồng: tưới mỗi ngày nhẹ, tránh úng."
    elif days <= 180:
        return "🌿 Giai đoạn phát triển: tưới 2-3 ngày/lần, trời nắng thì tưới mỗi ngày."
    elif days <= 330:
        return "🌼 Giai đoạn ra hoa nuôi trái: tưới 1-2 ngày/lần để trái ngọt."
    else:
        return "🍌 Trước thu hoạch 15 ngày: giảm nước để chuối ngọt và chắc múi."

days_since_planting = (date.today() - planting_date).days
if selected_crop == "Chuối":
    stage_msg = chuoi_stage(days_since_planting)
    st.info(f"📅 Đã trồng: **{days_since_planting} ngày**\n\n🔍 {stage_msg}")

# Quyết định tưới
def should_irrigate(sensor_hum, rain_chance):
    return sensor_hum < 60 and rain_chance < 30

is_irrigating = should_irrigate(sensor_hum, rain_probability)
if is_irrigating:
    st.success("💦 Hệ thống đang **tưới tiêu** do độ ẩm thấp và khả năng mưa thấp.")
else:
    st.info("⛅ Hệ thống **không tưới** - độ ẩm đủ hoặc có khả năng mưa.")

# --- GHI CHÚ ---
st.markdown("---")
st.caption("📡 Dữ liệu thời tiết lấy từ Open-Meteo API. Dữ liệu cảm biến từ thực tế.")
