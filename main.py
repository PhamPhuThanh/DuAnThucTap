import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
from tkinter import filedialog
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

####################################### Hàm #######################################

def delayed_action():
    if not window.winfo_exists():  # Kiểm tra xem window còn tồn tại hay không
        return

######################################################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

######################################################################################

def ghitg():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, ghitg)

#######################################################################

def clear():
    txt.delete(0, 'end')

def clear1():
    txt2.delete(0, 'end')

def clear2():
    txt3.delete(0, 'end')

def clear3():
    txt4.delete(0, 'end')

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Không tìm thấy file', message='Vui lòng tìm file')
        window.destroy()

################################# Mật khẩu ######################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Không tìm thấy mật khẩu cũ', 'Vui lòng nhập mật khẩu mới!', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Chưa cài đặt mật khẩu! Vui long thử lại')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Mật khẩu đã được đăng ký', message='Mật khẩu mới đã được đăng ký!')
            return
    password = tsd.askstring('Mật khẩu', 'Nhập mật khẩu', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Sai mật khẩu', message='Bạn đã nhập sai mật khẩu')

################################# Lấy ảnh nhận diện khuôn mặt ######################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', 'ID', 'NAME', 'PHONGBAN', 'CHUCVU']
    assure_path_exists("ThongTinNV/")
    assure_path_exists("TrainingImage/")
    serial = 0
    current_ids = set()  # Tập hợp để lưu trữ các ID hiện có

    # Kiểm tra và đọc dữ liệu từ CSV
    if os.path.isfile("ThongTinNV\ThongTinNV.csv"):
        with open("ThongTinNV\ThongTinNV.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            next(reader1)
            for row in reader1:
                if len(row) >= 2:
                    current_ids.add(row[1])
                    serial += 1
        serial += 1
        csvFile1.close()
    else:
        with open("ThongTinNV\ThongTinNV.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1

    Id = txt.get()
    name = txt2.get()
    phongban = txt3.get()
    chucvu = txt4.get()

    # Tạo danh sách lỗi
    errors = []
    if not name.replace(' ', '').isalpha():
        errors.append("Tên chỉ nên chứa chữ cái và khoảng trắng.")
    if Id in current_ids:
        errors.append("ID đã tồn tại.")
    if not phongban.replace(' ', '').isalpha():
        errors.append("Phòng ban chỉ nên chứa chữ cái và khoảng trắng.")
    if not chucvu.replace(' ', '').isalpha():
        errors.append("Chức vụ chỉ nên chứa chữ cái và khoảng trắng.")

    if errors:
        error_message = "\n".join(errors)
        mess.showerror("Lỗi nhập liệu", error_message)
        return  # Dừng hàm nếu có lỗi

    # Tiếp tục với quá trình ghi nhận hình ảnh
    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sampleNum += 1
            cv2.imwrite(f"TrainingImage\{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
            cv2.imshow('Lấy ảnh nhận diện', img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 50:
            break

    cam.release()
    cv2.destroyAllWindows()
    row = [serial, Id, name, phongban, chucvu]
    with open('ThongTinNV\ThongTinNV.csv', 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    current_ids.add(Id)

################################# Lấy ảnh nhận diện khuôn mặt ######################################

def TakeImagesVideo(video_path):
    check_haarcascadefile()
    columns = ['SERIAL NO.', 'ID', 'NAME', 'PHONGBAN', 'CHUCVU']
    assure_path_exists("ThongTinNV/")
    assure_path_exists("TrainingImage/")
    serial = 0
    current_ids = set()  # Tập hợp để lưu trữ các ID hiện có

    # Kiểm tra và đọc dữ liệu từ CSV
    if os.path.isfile("ThongTinNV\ThongTinNV.csv"):
        with open("ThongTinNV\ThongTinNV.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            next(reader1)  # Bỏ qua hàng tiêu đề
            for row in reader1:
                if len(row) >= 2:
                    current_ids.add(row[1])
                    serial += 1
        serial += 1
    else:
        with open("ThongTinNV\ThongTinNV.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1

    Id = txt.get()
    name = txt2.get()
    phongban = txt3.get()
    chucvu = txt4.get()

    # Tạo danh sách lỗi
    errors = []
    if not name.replace(' ', '').isalpha():
        errors.append("Tên chỉ nên chứa chữ cái và khoảng trắng.")
    if Id in current_ids:
        errors.append("ID đã tồn tại.")
    if not phongban.replace(' ', '').isalpha():
        errors.append("Phòng ban chỉ nên chứa chữ cái và khoảng trắng.")
    if not chucvu.replace(' ', '').isalpha():
        errors.append("Chức vụ chỉ nên chứa chữ cái và khoảng trắng.")

    if errors:
        error_message = "\n".join(errors)
        mess.showerror("Lỗi nhập liệu", error_message)
        return  # Dừng hàm nếu có lỗi

    # Tiếp tục với quá trình ghi nhận hình ảnh
    cam = cv2.VideoCapture(video_path)
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sampleNum += 1
            cv2.imwrite(f"TrainingImage\{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
            cv2.imshow('Lấy ảnh nhận diện', img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 200:
            break

    cam.release()
    cv2.destroyAllWindows()
    row = [serial, Id, name, phongban, chucvu]
    with open('ThongTinNV\ThongTinNV.csv', 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

##############################################################################

def select_video():
    root = tk.Tk()
    root.withdraw()  # Không hiển thị cửa sổ tkinter
    video_path = filedialog.askopenfilename(title="Chọn video", filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if video_path:
        TakeImagesVideo(video_path)
    else:
        mess.showerror("Lỗi", "Không chọn file video nào.")

################################# Training khuôn mặt ######################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='Chưa có công chức, viên chức được đăng ký', message='Vui lòng đăng ký!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    mess.showinfo(title="Lưu thành công", message='Thông tin được lưu thành công')
    message.configure(text='Số lượng công chức viên chức: ' + str(ID[0]))

##############################################################################

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

##############################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("ThongKeGhiNhan/")
    assure_path_exists("ThongTinNV/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Không tìm thấy dữ liệu', message='Vui lòng nhấn lưu thông tin!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Phongban', 'Chucvu', 'Date', 'Time']
    exists1 = os.path.isfile("ThongTinNV\ThongTinNV.csv")
    if exists1:
        df = pd.read_csv("ThongTinNV\ThongTinNV.csv")
    else:
        mess._show(title='Không tìm thấy thông tin', message='Thông tin công chức, viên chức không tìm thấy, vui lòng kiểm tra lại!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                cc = df.loc[df['SERIAL NO.'] == serial]['PHONGBAN'].values
                dd = df.loc[df['SERIAL NO.'] == serial]['CHUCVU'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                ee = str(cc)
                ee = ee[2:-2]
                ff = str(dd)
                ff = ff[2:-2]
                attendance = [str(ID), bb, ee, ff, str(date), str(timeStamp)]
                exists = os.path.isfile("ThongKeGhiNhan\ThongKeGhiNhan_" + date + ".csv")
                if exists:
                    with open("ThongKeGhiNhan\ThongKeGhiNhan_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(attendance)
                    csvFile1.close()
                else:
                    with open("ThongKeGhiNhan\ThongKeGhiNhan_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(col_names)
                        writer.writerow(attendance)
                    csvFile1.close()
                with open("ThongKeGhiNhan\ThongKeGhiNhan_" + date + ".csv", 'r') as csvFile1:
                    reader1 = csv.reader(csvFile1)
                    for lines in reader1:
                        i = i + 1
                        tam = ''
                        if (i > 1):
                            if (i % 2 != 0):
                                # iidd = str(lines[0])
                                # # tam = str(lines[0])
                                # if iidd != tam:
                                iidd = str(lines[0])
                                tv.insert('', 0, text=iidd, values=(
                                str(lines[1]), str(lines[2]), str(lines[3]), str(lines[4]), str(lines[5])))
                        # time.sleep(0.01)
                csvFile1.close()
            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x,  y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Nhan dien khuon mat', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    # ts = time.time()
    # date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    cam.release()
    cv2.destroyAllWindows()

##############################################################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
ngay,thang,nam=date.split("-")

mont={'01':'Tháng 1',
      '02':'Tháng 2',
      '03':'Tháng 3',
      '04':'Tháng 4',
      '05':'Tháng 5',
      '06':'Tháng 6',
      '07':'Tháng 7',
      '08':'Tháng 8',
      '09':'Tháng 9',
      '10':'Tháng 10',
      '11':'Tháng 11',
      '12':'Tháng 12'
      }


####################################### Giao Diện #######################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Recognize System")
window.configure(background='#ffffff')

frame1 = tk.Frame(window, bg="#dcdcdc")
frame1.place(relx=0.01, rely=0.17, relwidth=0.6, relheight=0.80)

frame2 = tk.Frame(window, bg="#dcdcdc")
frame2.place(relx=0.6, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Hệ thống nhận diện công chức, viên chức, người lao động Sở Thông Tin và Truyền Thông" ,fg="black",bg="#ffffff" ,width=75 ,height=1,font=('comic', 20, ' bold '))
message3.place(x=10, y=7)

frame3 = tk.Frame(window, bg="#ffffff")
frame3.place(relx=0.52, rely=0.09, relwidth=0.32, relheight=0.07)

frame4 = tk.Frame(window, bg="#ffffff")
frame4.place(relx=0.35, rely=0.09, relwidth=0.27, relheight=0.07)

datef = tk.Label(frame4, text = ngay+"-"+mont[thang]+"-"+nam+"  |  ", fg="black",bg="#ffffff" ,width=55 ,height=1,font=('comic', 17, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="black",bg="#ffffff" ,width=55 ,height=1,font=('comic', 17, ' bold '))
clock.pack(fill='both',expand=1)
ghitg()

head2 = tk.Label(frame2, text="                       Tạo khuôn mặt mới                       ", fg="black",bg="#dcdcdc" ,font=('comic', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       Nhận diện khuôn mặt                       ", fg="black",bg="#dcdcdc" ,font=('comic', 17, ' bold ') )
head1.place(x=40,y=0)

lbl = tk.Label(frame2, text="Nhập ID",width=20  ,height=1  ,fg="black"  ,bg="#dcdcdc" ,font=('comic', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Nhập Họ và Tên",width=20  ,fg="black"  ,bg="#dcdcdc" ,font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=30, y=173)

lbl3 = tk.Label(frame2, text="Nhập phòng ban", width=20  ,fg="black"  ,bg="#dcdcdc" ,font=('comic', 17, ' bold '))
lbl3.place(x=80, y=210)

txt3 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt3.place(x=30, y=240)

lbl4 = tk.Label(frame2, text="Nhập chức vụ", width=20  ,fg="black"  ,bg="#dcdcdc" ,font=('comic', 17, ' bold '))
lbl4.place(x=80, y=280)

txt4 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt4.place(x=30, y=310)

message = tk.Label(frame2, text="" ,bg="#dcdcdc" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Ghi nhận",width=20  ,fg="black"  ,bg="#dcdcdc"  ,height=1 ,font=('comic', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("ThongTinNV\ThongTinNV.csv")
if exists:
    with open("ThongTinNV\ThongTinNV.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        next(reader1)
        for l in reader1:
            res = res + 1
    res = (res // 2)
    csvFile1.close()
else:
    res = 0
message.configure(text='Số lượng công, viên chức: '+str(res))

################## Bảng Ghi Nhận ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name', 'phongban', 'chucvu','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('phongban',width=130)
tv.column('chucvu',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('phongban',text ='PHONGBAN')
tv.heading('chucvu',text ='CHUCVU')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

####################################### Btn #######################################

clearButton = tk.Button(frame2, text="Xóa", command=clear,fg="black"  ,bg="#ff7221"  ,width=10 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=335, y=88)
clearButton2 = tk.Button(frame2, text="Xóa", command=clear1,fg="black"  ,bg="#ff7221"  ,width=10 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=173)
clearButton3 = tk.Button(frame2, text="Xóa", command=clear2,fg="black"  ,bg="#ff7221"  ,width=10 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton3.place(x=335, y=240)
clearButton4 = tk.Button(frame2, text="Xóa", command=clear3,fg="black"  ,bg="#ff7221"  ,width=10 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton4.place(x=335, y=310)
takeImg = tk.Button(frame2, text="Lấy ảnh", command=TakeImages, fg="white"  ,bg="#6d00fc"  ,width=16  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=30, y=380)
takeImgVideo = tk.Button(frame2, text="Lấy ảnh qua video", command=select_video, fg="white"  ,bg="#6d00fc"  ,width=16  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImgVideo.place(x=240, y=380)
trainImg = tk.Button(frame2, text="Lưu thông tin", command=TrainImages,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=30, y=510)
trackImg = tk.Button(frame1, text="Nhận diện", command=TrackImages,fg="black"  ,bg="#3ffc00"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trackImg.place(x=90,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#eb4600"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=90, y=450)

####################################### Chạy Chương Trình #######################################


window.after(5000, delayed_action)  # Lên lịch hành động sau 5 giây
window.mainloop()