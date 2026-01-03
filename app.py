import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Tiến Thu CRM", layout="wide")

# Link Google Sheets của bạn (THAY LINK CỦA BẠN VÀO ĐÂY)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1UKatDsrpiNYryQDukxREKzh6uMQC8fHe?rtpof=true&usp=drive_fs"

# Kết nối với Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Hàm đọc dữ liệu từ Sheets
def load_data():
    return conn.read(spreadsheet=URL_SHEET, usecols=list(range(24)))

# Giao diện Tiêu đề
st.title("CÔNG TY TNHH TIẾN THU")
st.write(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Bộ phận Bán hàng")

menu = ["TẠO KHÁCH HÀNG TIỀM NĂNG", "CHI TIẾT LIÊN HỆ"]
choice = st.sidebar.selectbox("DANH MỤC", menu)

if choice == "TẠO KHÁCH HÀNG TIỀM NĂNG":
    st.header("📝 Nhập Thông Tin Khách Hàng")
    
    with st.form("form_khach_hang"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Họ và tên khách hàng").title()
            address = st.text_input("Địa chỉ").title()
            ward = st.selectbox("Phường", ["Hải Châu", "Thanh Khê", "Ngũ Hành Sơn", "Liên Chiểu", "Cẩm Lệ", "Sơn Trà", "Khác..."])
            city = st.selectbox("Thành phố", ["Đà Nẵng", "Quảng Nam", "Huế", "Khác..."])
            phone = st.text_input("Số điện thoại")
            gender = st.radio("Giới tính", ["Nam", "Nữ"], horizontal=True)
            demand = st.text_area("Nhu cầu mua xe")
            time_buy = st.selectbox("Thời gian mua xe", ["1 tuần", "2 tuần", "3 tuần", "Khác..."])
        with col2:
            prob = st.selectbox("Xác suất", ["40%", "50%", "60%", "70%", "80%", "90%", "100%"])
            status = st.text_input("Trạng thái")
            budget = st.text_input("Khoản tiền dự kiến")
            process = st.multiselect("Quá trình bán hàng", ["Đã mua", "Gửi báo giá", "Đã xem SP", "Đã trải nghiệm lái thử"])
            staff = st.selectbox("NV Bán hàng", ["Khoa", "Chiến", "My", "Thuận"])
            approach = st.selectbox("Cách tiếp cận", ["Điện thoại", "Quảng cáo", "Trực tiếp"])

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1: d1 = st.date_input("Ngày LH 1", value=None); n1 = st.text_input("Nội dung LH 1")
        with c2: d2 = st.date_input("Ngày LH 2", value=None); n2 = st.text_input("Nội dung LH 2")
        with c3: d3 = st.date_input("Ngày LH 3", value=None); n3 = st.text_input("Nội dung LH 3")

        st.markdown("---")
        buy_date = st.date_input("Ngày mua xe", value=None)
        result = st.selectbox("Kết quả", ["Đang theo dõi", "Đã mua xe", "Không mua xe", "Mua nơi khác"])
        close_date = st.date_input("Ngày đóng phiếu", value=None)

        submitted = st.form_submit_button("LƯU VÀO GOOGLE SHEETS")
        
        if submitted:
            # Tạo DataFrame mới từ dữ liệu nhập
            new_row = pd.DataFrame([{
                "Ngày tạo": datetime.now().strftime("%d/%m/%Y"),
                "Họ và tên khách hàng": name, "Địa chỉ": address, "Phường": ward, "Thành phố": city,
                "Số điện thoại": phone, "Giới tính": gender, "Nhu cầu mua xe": demand,
                "Thời gian mua xe": time_buy, "Xác suất": prob, "Trạng thái": status,
                "Khoản tiền dự kiến": budget, "Quá trình bán hàng": ", ".join(process),
                "NV Bán hàng": staff, "Cách tiếp cận": approach,
                "Ngày LH 1": str(d1), "Nội dung LH 1": n1, "Ngày LH 2": str(d2), "Nội dung LH 2": n2,
                "Ngày LH 3": str(d3), "Nội dung LH 3": n3, "Ngày mua xe": str(buy_date),
                "Kết quả": result, "Ngày đóng phiếu": str(close_date)
            }])
            
            # Đọc dữ liệu cũ, thêm dòng mới và ghi đè lên Sheets
            existing_data = load_data()
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("✅ Đã cập nhật dữ liệu lên Google Sheets thành công!")

elif choice == "CHI TIẾT LIÊN HỆ":
    st.header("🔍 Tra cứu dữ liệu từ Google Sheets")
    df = load_data()
    st.dataframe(df)
