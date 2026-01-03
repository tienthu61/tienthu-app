import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Cấu hình trang
st.set_page_config(page_title="Tiến Thu - Báo cáo khách hàng", layout="wide")

# Đường dẫn file Excel
DB_FILE = "danh_sach_tiem_nang.xlsx"

# Hàm khởi tạo file Excel nếu chưa có
def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=[
            "Ngày tạo", "Họ và tên khách hàng", "Địa chỉ", "Phường", "Thành phố", 
            "Số điện thoại", "Giới tính", "Nhu cầu mua xe", "Thời gian mua xe", 
            "Xác suất", "Trạng thái", "Khoản tiền dự kiến", "Quá trình bán hàng",
            "NV Bán hàng", "Cách tiếp cận", "Ngày LH 1", "Nội dung LH 1",
            "Ngày LH 2", "Nội dung LH 2", "Ngày LH 3", "Nội dung LH 3",
            "Ngày mua xe", "Kết quả", "Ngày đóng phiếu"
        ])
        df.to_excel(DB_FILE, index=False)

init_db()

# Giao diện Tiêu đề
st.image("https://tienthu.com.vn/assets/images/logo.png", width=200) # Link logo minh họa
st.title("CÔNG TY TNHH TIẾN THU")
st.subheader("BỘ PHẬN: BÁN HÀNG")
st.write(f"📅 Ngày/Giờ hiện tại: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
st.write("📍 61 Đống Đa, Đà Nẵng")

# Menu điều hướng
menu = ["TẠO KHÁCH HÀNG TIỀM NĂNG", "CHI TIẾT LIÊN HỆ"]
choice = st.sidebar.selectbox("DANH MỤC", menu)

# --- CHỨC NĂNG 1: TẠO KHÁCH HÀNG ---
if choice == "TẠO KHÁCH HÀNG TIỀM NĂNG":
    st.header("📝 Nhập Thông Tin Khách Hàng")
    
    with st.form("form_khach_hang"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Họ và tên khách hàng").title()
            address = st.text_input("Địa chỉ").title()
            ward = st.selectbox("Phường", ["Hải Châu", "Thanh Khê", "Ngũ Hành Sơn", "Liên Chiểu", "Cẩm Lệ", "Sơn Trà", "Khác..."])
            city = st.selectbox("Thành phố", ["Đà Nẵng", "Quảng Nam", "Huế", "Khác..."])
            phone = st.text_input("Số điện thoại (VD: 0905.123.456)")
            gender = st.radio("Giới tính", ["Nam", "Nữ"], horizontal=True)
            demand = st.text_area("Nhu cầu mua xe")
            time_buy = st.selectbox("Thời gian mua xe", ["1 tuần", "2 tuần", "3 tuần", "Khác..."])
            
        with col2:
            prob = st.selectbox("Xác suất thành công", ["40%", "50%", "60%", "70%", "80%", "90%", "100%", "Khác..."])
            status = st.text_input("Trạng thái")
            budget = st.text_input("Khoản tiền dự kiến định mua")
            process = st.multiselect("Quá trình bán hàng", ["Đã mua", "Gửi báo giá", "Đã xem SP", "Đã trải nghiệm lái thử"])
            staff = st.selectbox("Nhân viên bán hàng", ["Khoa", "Chiến", "My", "Thuận", "Thêm mới..."])
            approach = st.selectbox("Cách tiếp cận", ["Điện thoại", "Quảng cáo", "Trực tiếp", "Khác..."])

        st.markdown("---")
        st.subheader("Lịch trình liên hệ")
        c1, c2, c3 = st.columns(3)
        with c1:
            d1 = st.date_input("Ngày liên hệ lần 1", value=None)
            n1 = st.text_input("Nội dung lần 1")
        with c2:
            d2 = st.date_input("Ngày liên hệ lần 2", value=None)
            n2 = st.text_input("Nội dung lần 2")
        with c3:
            d3 = st.date_input("Ngày liên hệ lần 3", value=None)
            n3 = st.text_input("Nội dung lần 3")

        st.markdown("---")
        c4, c5, c6 = st.columns(3)
        with c4:
            buy_date = st.date_input("Ngày mua xe", value=None)
        with c5:
            result = st.selectbox("Kết quả", ["Đang theo dõi", "Đã mua xe", "Không mua xe", "Mua nơi khác"])
        with c6:
            close_date = st.date_input("Ngày đóng phiếu", value=None)

        submitted = st.form_submit_button("LƯU THÔNG TIN")
        
        if submitted:
            new_data = {
                "Ngày tạo": datetime.now().strftime("%d/%m/%Y"),
                "Họ và tên khách hàng": name,
                "Địa chỉ": address,
                "Phường": ward,
                "Thành phố": city,
                "Số điện thoại": phone,
                "Giới tính": gender,
                "Nhu cầu mua xe": demand,
                "Thời gian mua xe": time_buy,
                "Xác suất": prob,
                "Trạng thái": status,
                "Khoản tiền dự kiến": budget,
                "Quá trình bán hàng": ", ".join(process),
                "NV Bán hàng": staff,
                "Cách tiếp cận": approach,
                "Ngày LH 1": d1, "Nội dung LH 1": n1,
                "Ngày LH 2": d2, "Nội dung LH 2": n2,
                "Ngày LH 3": d3, "Nội dung LH 3": n3,
                "Ngày mua xe": buy_date,
                "Kết quả": result,
                "Ngày đóng phiếu": close_date
            }
            df = pd.read_excel(DB_FILE)
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(DB_FILE, index=False)
            st.success("Đã lưu dữ liệu thành công!")

# --- CHỨC NĂNG 2: CHI TIẾT & CHỈNH SỬA ---
elif choice == "CHI TIẾT LIÊN HỆ":
    st.header("🔍 Danh sách & Cập nhật khách hàng")
    df = pd.read_excel(DB_FILE)
    
    if not df.empty:
        # Chọn khách hàng để sửa
        list_kh = df["Họ và tên khách hàng"].tolist()
        selected_kh = st.selectbox("Chọn khách hàng để xem/chỉnh sửa", list_kh)
        
        idx = df[df["Họ và tên khách hàng"] == selected_kh].index[0]
        row = df.iloc[idx]
        
        # Kiểm tra trạng thái khóa (Ngày đóng phiếu)
        is_locked = pd.notnull(row["Ngày đóng phiếu"])
        
        if is_locked:
            st.warning("⚠️ Phiếu này đã đóng. Không thể chỉnh sửa nội dung.")
            st.dataframe(df.iloc[[idx]])
        else:
            st.info("Chế độ: Chỉnh sửa thông tin")
            # Hiển thị các ô nhập dữ liệu có sẵn giá trị cũ (Sử dụng các widget tương tự phần nhập liệu)
            new_status = st.text_input("Cập nhật trạng thái", value=row["Trạng thái"])
            new_result = st.selectbox("Cập nhật kết quả", ["Đang theo dõi", "Đã mua xe", "Không mua xe", "Mua nơi khác"], 
                                      index=["Đang theo dõi", "Đã mua xe", "Không mua xe", "Mua nơi khác"].index(row["Kết quả"]))
            new_close_date = st.date_input("Cập nhật ngày đóng phiếu (Để khóa phiếu)", value=None)
            
            if st.button("CẬP NHẬT DỮ LIỆU"):
                df.at[idx, "Trạng thái"] = new_status
                df.at[idx, "Kết quả"] = new_result
                df.at[idx, "Ngày đóng phiếu"] = new_close_date
                df.to_excel(DB_FILE, index=False)
                st.success("Cập nhật thành công!")
                st.rerun()
                
        st.markdown("### Toàn bộ danh sách")
        st.dataframe(df)
    else:
        st.write("Chưa có dữ liệu.")