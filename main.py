
# کتابخانه ها
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pygame 
import os
import threading
import textwrap  # اطمینان از وارد کردن ماژول textwrap
from pydub import AudioSegment, playback
import wave
from PIL import Image, ImageTk  # این خط برای وارد کردن کتابخانه Pillow است

# متغیرها
reading_window = []
listening_correct_answers = 0
listening_total_score = 0
reading_question_buttons = {}

# لاگین

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "" or password == "":
        messagebox.showwarning("خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید.")
        return

    users = load_users()
    
    if [username, password] in users:
        print("ورود موفق")
        navigate_to_main_page()
    else:
        messagebox.showerror("خطا", "نام کاربری یا رمز عبور نادرست.")

def navigate_to_main_page():
    tabs.pack_forget()  # پنهان کردن تب‌ها
    main_frame.pack(expand=1, fill='both')  # نمایش صفحه اصلی

def go_to_welcome():
    main_frame.pack_forget()  # پنهان کردن صفحه اصلی
    welcome_frame.pack()      # نمایش صفحه خوش آمدگویی

def register():
    username = entry_new_username.get()
    password = entry_new_password.get() 
    
    if username == "" or password == "":
        messagebox.showwarning("خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید.")
        return

    save_user_info(username, password)
    messagebox.showinfo("موفقیت", "ثبت نام با موفقیت انجام شد!")



def save_user_info(username, password):
    with open("users.txt", "a") as file:
        file.write(f"{username},{password}\n")

def load_users():
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    return []

def start_test():
    welcome_frame.pack_forget()  # پنهان کردن صفحه خوش آمدگویی
    tabs.pack(expand=1, fill='both')  # نمایش تب‌ها
    root.title("صفحه خوش آمدگویی")  # عنوان جدید

 # جمع امتیاز خواندن و شنیدار

def show_final_score():
    total_score = reading_score + listening_total_score  
    messagebox.showinfo(" نتیجه نهایی آزمون ", f"امتیاز نهایی شما: {total_score}  از 100 می باشد")

def create_test_tabs():

      # فریم برای توضیحات در بالای صفحه
    description_frame = tk.Frame(main_frame)
    description_frame.pack(side=tk.TOP, fill=tk.X, pady=20)  # فریم در بالای صفحه قرار می‌گیرد

# برچسب برای نمایش توضیحات
    description_label = tk.Label(description_frame, text="امتیاز آزمون شنیداری ۶۰ و امتیاز آزمون خواندن ۴۰ می‌باشد", 
                             font=("Arial", 12), wraplength=400, justify="center")
    description_label.pack(pady=10)

    # ایجاد فریم در پایین صفحه برای دکمه‌ها
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=100)  # فریم در پایین صفحه قرار می‌گیرد

    # دکمه شروع آزمون شنیداری
    start_listening_button = tk.Button(button_frame, text="شروع آزمون شنیداری", command=start_listening,bg="#90EE90",fg="black")
    start_listening_button.pack(pady=10, padx=20, fill=tk.X)  # افزودن padx برای فاصله از کناره‌ها

    # دکمه شروع آزمون خواندن
    start_reading_button = tk.Button(button_frame, text="شروع آزمون خواندن", command=start_reading,bg="#90EE90",fg="black")
    start_reading_button.pack(pady=10, padx=20, fill=tk.X)  # افزودن padx برای فاصله از کناره‌ها

    # دکمه نمایش امتیاز نهایی
    show_score_button = tk.Button(button_frame, text="امتیاز نهایی", command=show_final_score,bg="#90EE90",fg="black")
    show_score_button.pack(pady=20, padx=20, fill=tk.X)  # افزودن padx برای فاصله از کناره‌ها

    # تابع برای پایان آزمون و توقف پخش
def finish_test():
    pygame.mixer.music.stop()  # توقف پخش فایل صوتی
    display_listening_total_score()  # نمایش امتیاز کل آزمون

# شروع بخش  شنیداری 

def start_listening():
    global listening_window  # تعریف listening_window به عنوان متغیر سراسری
    listening_window = tk.Toplevel(root)
    listening_window.title("آزمون شنیداری")
    listening_window.geometry("600x600")
     
    # فریم برای محتوای توضیحات
    explanation_frame = tk.Frame(listening_window)
    explanation_frame.pack(side=tk.TOP, fill=tk.BOTH)  # توضیحات در بالای پنجره قرار می‌گیرد

# اضافه کردن توضیحات به فریم توضیحات
    explanation_label = tk.Label(
    explanation_frame, 
    text="پس از پاسخگویی به کلیه سوالات دکمه پایان آزمون را فشار دهید", 
    fg="#003366", 
    font=("Arial", 12),
    bg="#a1d6d6",  # رنگ پس‌زمینه
    highlightbackground="#003366",  # رنگ خط
    highlightthickness=2,  # ضخامت خط
    bd=0 ) # بدون حاشیه اصلی

    explanation_label.pack(pady=25, padx=20)

    # ایجاد یک فریم برای دکمه‌ها

    button_frame = tk.Frame(listening_window)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=50)
    
    global status_label
    status_label = tk.Label(listening_window, text="", font=("Arial", 12))
    status_label.pack(pady=100)  # وضعیت در بالای پنجره قرار می‌گیرد


    global play_buttons
    play_buttons = []

  # ایجاد دکمه‌های پخش
    play_buttons = []
    for i in range(1, 5):
        play_button = tk.Button(button_frame, text=f"فایل صوتی شماره {i}", command=lambda i=i: threading.Thread(target=play_audio, args=(i,)).start(), width=20,bg="#90EE90",fg="black")
        play_button.pack(pady=5, fill=tk.X)  # دکمه‌ها زیر هم و با فاصله مشخص قرار می‌گیرند
        play_buttons.append(play_button)

    # دکمه خروج از آزمون
    exit_button = tk.Button(button_frame, text="خروج از آزمون", command=lambda: [pygame.mixer.music.stop(), listening_window.destroy(), go_to_welcome()], width=20, bg="#FFFF00", fg="black")
    exit_button.pack(pady=10, fill=tk.X)
    
       
# ایجاد دکمه "پایان آزمون"
    finish_button = tk.Button(button_frame, text="پایان آزمون", command=lambda:[listening_window.destroy(), display_listening_total_score()] , width=20,bg="#FFFF00",fg="black")
    finish_button.pack(pady =10,fill=tk.X)

# متغیر برای ثبت نمره
readig_correct_answers = 0
score_label = None  # تعریف متغیر سراسری
play_buttons = []  # برای ذخیره دکمه‌های پخش فایل‌ها
reading_score = 0  # امتیاز کلی برای بخش خواندن

# تنظیمات pygame برای پخش فایل صوتی
pygame.mixer.init()

# تعیین پوشه فعلی که اسکریپت در آن اجرا می‌شود
current_directory = os.path.dirname(os.path.abspath(__file__))

# آدرس پوشه فایل‌های صوتی به صورت نسبی
audio_directory = os.path.join(current_directory)  # پوشه 'exam' در کنار فایل اسکریپت


def play_audio(audio_number):
    # فرمت‌های صوتی پشتیبانی شده
    supported_formats = ['mp3', 'ogg', 'flac', 'kmp','wave']  # شما می‌توانید فرمت‌های بیشتری اضافه کنید
    audio_file = None

    # بررسی هر یک از فرمت‌ها
    for audio_format in supported_formats:
        temp_file = os.path.join(audio_directory, f'conversation-{audio_number}.{audio_format}')
        if os.path.isfile(temp_file):
            audio_file = temp_file
            break

    # اگر فایل صوتی پیدا نشد
    if audio_file is None:
        messagebox.showerror("خطا", f"فایل صوتی با فرمت‌های {', '.join(supported_formats)} یافت نشد.")
        return
    
  # پخش فایل صوتی
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # غیر فعال کردن دکمه مربوط به فایل صوتی فعلی
    play_buttons[audio_number - 1].config(state=tk.DISABLED)

    # بررسی اتمام پخش فایل صوتی
    check_audio_status(audio_number)

# تابع برای بررسی وضعیت پخش
def check_audio_status(audio_number):
    if pygame.mixer.music.get_busy():  # اگر موسیقی در حال پخش است
        status_label.after(1500, check_audio_status, audio_number)  # بررسی مجدد بعد از 100 میلی‌ثانیه
    else:
        # وقتی پخش تمام شد، سوالات را نمایش می‌دهیم
        show_questions(audio_number)

    

def display_listening_total_score():
    # نمایش امتیاز در صورت وجود
   
        messagebox.showinfo(" امتیاز آزمون شنیداری", f"  امتیاز شما در آزمون شنیداری : {listening_total_score} از 60 می باشد " )  # استفاده از showinfo



def show_questions(audio_number):
    global correct_answers

    # سوالات مربوط به هر فایل صوتی
    questions = {
        1: [
            {"question": "why the student wants to transfer", 
             "options": ["difficult lessons", "due to costs", "missing hometown", "none of the answers"],
             "correct": 2},  # گزینه صحیح: A journey
        ],
        2: [
            {"question": "which subject Arthur is going to take this semester?", 
             "options": ["ecology", "biology", "anthropology", "maths"],
             "correct": 0},  # گزینه صحیح: A decision to try
        ],
        3: [
            {"question": "who is dissatisfied with the professor?", 
             "options": ["his student", "his colleague", "his wife", "his publisher"],
             "correct": 3},  # گزینه صحیح: Canvas
        ],
        4: [
            {"question": "which type of pass the student needs ?", 
             "options": ["he is not sure", "sport pass", "round trip pass", "one-way pass"],
             "correct": 0},  # گزینه صحیح: Self-confidence
        ]
    }

    # ایجاد پنجره سوالات
    questions_window = tk.Toplevel(root)
    questions_window.title(f"سوال فایل صوتی شماره {audio_number}")
    questions_window.geometry("400x200")

  
   # نمایش سوالات
    def check_answer(q, var):
        global listening_correct_answers ,listening_total_score
        if var.get() == q["correct"]:
            listening_correct_answers += 1
        listening_total_score = listening_correct_answers * 15

    for i, q in enumerate(questions[audio_number]):
        question_label = tk.Label(questions_window, text=f" {q['question']}")
        question_label.pack(pady=5)

        var = tk.IntVar(value=" " )  # متغیر برای ذخیره انتخاب کاربر
        for j, option in enumerate(q["options"]):
            radio_button = tk.Radiobutton(questions_window, text=option, variable=var, value=j)
            radio_button.pack(anchor="w")

    # دکمه ارسال پاسخ

    submit_button = tk.Button(questions_window, text="ارسال پاسخ", command=lambda: (check_answer(q, var), close_window()))
    submit_button.pack(pady=5)

      # پس از بستن پنجره سوالات، به صفحه آزمون برمی‌گردیم
    def on_close():
        questions_window.destroy()  # پنجره سوالات بسته می‌شود
        navigate_to_main_page()  # بازگشت به صفحه آزمون شنیداری


    questions_window.protocol("WM_DELETE_WINDOW", on_close)  # ا

    def close_window():
        questions_window.destroy()



# شروع بخش خواندن
def start_reading():
    global reading_window  # متغیر global برای دسترسی به reading_window
    reading_window = tk.Toplevel(root)
    reading_window.title("آزمون خواندن")
    reading_window.geometry("500x500")
    global score_label  # استفاده از متغیر global برای score_label
    global reading_question_buttons  # استفاده از دیکشنری global برای دکمه‌ها
    reading_question_buttons = {}  # تعریف دیکشنری برای دکمه‌ها

    # فریم برای محتوای توضیحات
    explanation_frame = tk.Frame(reading_window)
    explanation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # اضافه کردن توضیحات به فریم توضیحات
    explanation_label = tk.Label(
        explanation_frame, 
        text="پس از پاسخگویی به کلیه سوالات دکمه پایان آزمون را فشار دهید", 
        fg="#003366", 
        font=("Arial", 12),
        bg="#a1d6d6",  # رنگ پس‌زمینه
        highlightbackground="#003366",  # رنگ خط
        highlightthickness=2,  # ضخامت خط
        bd=0  # بدون حاشیه اصلی
    )
    explanation_label.pack(pady=25, padx=20)  # حاشیه برای قرار دادن در صفحه

    # ایجاد فریم برای دکمه‌ها
    button_frame = tk.Frame(reading_window)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20,padx=5)  # فریم در پایین پنجره قرار داده می‌شود و به طور کامل در عرض پنجره پخش می‌شود

    # ایجاد دکمه‌ها برای نمایش سوالات
    for i in range(1, len(reading_questions_dict) + 1):
        button = tk.Button(button_frame, text=f"نمایش سوالات {i}", command=lambda audio_number=i: show_reading_questions(audio_number), bg="#90EE90", fg="black")
        button.pack(fill=tk.X, pady=2)  # دکمه‌ها سراسر عرض صفحه را می‌پوشانند
        reading_question_buttons[i] = button  # ذخیره دکمه در دیکشنری

    # دکمه خروج از آزمون
    exit_button = tk.Button(button_frame, text="خروج از آزمون", command=exit_reading, bg="#FFFF00", fg="black")
    exit_button.pack(fill=tk.X, pady=5)  # دکمه خروج نیز تمام عرض صفحه را می‌پوشاند

    # دکمه اتمام آزمون
    finish_button = tk.Button(button_frame, text="پایان آزمون", command=end_reading_test, bg="#FFFF00", fg="black")
    finish_button.pack(fill=tk.X, pady=10, padx=5) 

# سوالات و پاسخ‌های اصلاح شده
reading_questions_dict = {
    1: {
        "text": textwrap.dedent("""\
            The Climb: Once upon a time, a young girl named Maya 
            dreamed of reaching the top of a tall mountain. Many warned 
            her it was too difficult, but she believed in herself. Day 
            by day, she trained, overcoming obstacles along the way. 
            Finally, after a long journey, she reached the summit, 
            feeling accomplished and proud.
        """),
        "questions": [
            {
                "question": "What did Maya dream of?",
                "options": ["Reaching the top of a mountain", "Flying", "Winning a race"],
                "correct_answer": "Reaching the top of a mountain"
            }
        ]
    },
    2: {
        "text": textwrap.dedent("""\
            The Art of Failure: In a small town, there lived a boy 
            named Sam who loved painting. His first few paintings 
            were not good at all. Instead of giving up, he took each 
            failure as a lesson. With practice, his skills improved, 
            and soon he created a beautiful masterpiece that won the 
            town's art contest.
        """),
        "questions": [
            {
                "question": "What did Sam do with his failures?",
                "options": ["Gave up", "Learned from them", "Ignored them"],
                "correct_answer": "Learned from them"
            }
        ]
    },
    3: {
        "text": textwrap.dedent("""\
            The Gift of Kindness: Once in a bustling city, an elderly 
            man named Mr. Thompson noticed a young boy sitting alone. 
            He decided to approach him and offered a kind smile. They 
            started talking, and soon the boy shared his struggles. 
            Mr. Thompson listened and encouraged him, reminding him 
            that kindness can change lives.
        """),
        "questions": [
            {
                "question": "What did Mr. Thompson do?",
                "options": ["Ignored the boy", "Offered a kind smile", "Yelled at him"],
                "correct_answer": "Offered a kind smile"
            }
        ]
    },
    4: {
        "text": textwrap.dedent("""\
            Lily loved her garden. Every morning, she watered the 
            flowers and talked to them. One day, a bright red rose 
            bloomed, more beautiful than any other flower. Lily smiled 
            and whispered, 'You’re special.' From that day on, the rose 
            became her favorite, standing tall among the rest.
        """),
        "questions": [
            {
                "question": "What made the rose special to Lily?",
                "options": ["It was taller than the others", "It bloomed beautifully", "It was the only flower in the garden"],
                "correct_answer": "It bloomed beautifully"
            }
        ]
    }
}

# متغیر جهانی برای امتیاز
reading_score = 0

def end_reading_test():
    global reading_score
    tk.messagebox.showinfo("پایان آزمون خواندن ", f"امتیاز شما در آزمون خواندن : {reading_score} از 40 می باشد")
    reading_window.destroy()  # بستن پنجره آزمون پس از پایان

def exit_reading():
    reading_window.destroy()  # بستن پنجره آزمون خواندن
    go_to_welcome()  # بازگشت به صفحه خوش آمد گویی

def show_reading_questions(story_number):
    questions_window = tk.Toplevel(root)
    questions_window.title(f"سوالات داستان {story_number}")
    questions_window.geometry("400x400")

    # دریافت متن داستان و سوالات
    story_data = reading_questions_dict[story_number]
    story_text = story_data["text"]
    questions = story_data["questions"]

    # نمایش متن داستان
    story_label = tk.Label(questions_window, text=story_text, wraplength=350, justify="center")
    story_label.pack(pady=10)

    # ایجاد متغیر برای ذخیره پاسخ انتخاب شده
    var = tk.StringVar(value=" ")

    for i, question_data in enumerate(questions):
        question = question_data["question"]
        options = question_data["options"]

        question_label = tk.Label(questions_window, text=f"سوال: {question}")
        question_label.pack(pady=5)
        
        # ایجاد گزینه‌ها برای سوال
        for option in options:
            # تغییر اندازه متن و دکمه‌های رادیویی
            radio_button = tk.Radiobutton(questions_window, text=option, variable=var, value=option, font=("Helvetica", 9))  # تغییر فونت
            radio_button.pack(anchor="w", padx=10, pady=5)  # افزودن padding برای فضاسازی بیشتر

    # دکمه ارسال پاسخ
    submit_button = tk.Button(questions_window, text="ارسال پاسخ", command=lambda: on_submit(questions_window, questions, var))
    submit_button.pack(pady=5)
    # غیرفعال کردن دکمه مربوط به سوال کلیک‌شده
    reading_question_buttons[story_number]['state'] = 'disabled'

def on_submit(questions_window, questions, var):
    global reading_score  # دسترسی به متغیر global امتیاز
    selected_answer = var.get()

    # بررسی پاسخ کاربر
    for question_data in questions:
        correct_answer = question_data["correct_answer"]
        if selected_answer == correct_answer:
            reading_score += 10  # به ازای هر پاسخ درست ۱۰ امتیاز اضافه می‌شود

    questions_window.destroy()  # بستن پنجره سوالات


# ایجاد پنجره اصلی
root = tk.Tk()
root.title("صفحه خوش آمدگویی  ")
root.geometry("400x500")
# تغییر رنگ پس‌زمینه کل پنجره اصلی
root.configure(bg="#a1d6d6")  # سبز یشمی کم رنگ

#لوگو 
base_dir = os.path.abspath(os.path.dirname(__file__))  # مسیر فعلی فایل برنامه
logo_path = os.path.join(base_dir,'logo.jpg')  # آدرس نسبی لوگو

# بررسی وجود فایل لوگو
if not os.path.isfile(logo_path):
    print("فایل لوگو یافت نشد.")
else:
    # بارگذاری و تنظیم لوگو
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((500, 500))  # تغییر اندازه لوگو به 500x500 پیکسل
    logo_photo = ImageTk.PhotoImage(logo_image)
    root.iconphoto(True, logo_photo)

# صفحه خوش آمدگویی
welcome_frame = tk.Frame(root, bg="#a1d6d6")  # سبز یشمی کم رنگ
welcome_label = tk.Label(welcome_frame, text="WELCOME TO  E_PY", font=("Arial", 14), bg="#a1d6d6", fg="black")
welcome_label.pack(pady=40)
start_button = tk.Button(welcome_frame, text="شروع آزمون", command=start_test,bg="green", fg="white")
start_button.pack(pady=40)
welcome_frame.pack()

# ایجاد تب‌ها
tabs = ttk.Notebook(root)

# تب ورود
login_tab = tk.Frame(tabs)
tabs.add(login_tab, text='ورود')
label_username = tk.Label(login_tab, text="نام کاربری:")
label_username.pack(pady=5)
entry_username = tk.Entry(login_tab)
entry_username.pack(pady=5)

label_password = tk.Label(login_tab, text="رمز عبور:")
label_password.pack(pady=5)
entry_password = tk
entry_password = tk.Entry(login_tab, show='*')
entry_password.pack(pady=5)

login_button = tk.Button(login_tab, text="ورود", command=login,bg="#ADD8E6", fg="black")
login_button.pack(pady=10)

# تب ثبت‌ نام
register_tab = tk.Frame(tabs)
tabs.add(register_tab, text='ثبت نام')
label_new_username = tk.Label(register_tab, text="نام کاربری:")
label_new_username.pack(pady=5)
entry_new_username = tk.Entry(register_tab)
entry_new_username.pack(pady=5)

label_new_password = tk.Label(register_tab, text="رمز عبور:")
label_new_password.pack(pady=5)
entry_new_password = tk.Entry(register_tab, show='*')
entry_new_password.pack(pady=5)

register_button = tk.Button(register_tab, text="ثبت نام", command=register,bg="#ADD8E6", fg="black")
register_button.pack(pady=10)

# صفحه اصلی
main_frame = tk.Frame(root)
# دکمه بازگشت به صفحه خوش آمدگویی
exit_button = tk.Button(main_frame, text="خروج از آزمون", command=go_to_welcome, bg="#ffff00", fg="black")
exit_button.pack(side=tk.BOTTOM, pady=10)

# ایجاد تب‌های آزمون
create_test_tabs()

# اجرای حلقه اصلی
root.mainloop()
