import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter.messagebox as tkmb

root = tk.Tk()
root.configure(bg="#fff")
root.geometry("1520x780+0+0")

global puppyLarge_img, logo_img
import requests

def resizeImage(image_path, width, height):
    pil_image = Image.open(image_path)
    resized = pil_image.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized)

def on_convert():
    global ans

    amount = amount_entry.get()
    from_currency = combobox_var.get().split(" - ")[0]
    to_currency = combobox_var1.get().split(" - ")[0]

    try:
        amount = float(amount)
    except ValueError:
        ans.config(text="Error!!!", fg="red")
        return

    if from_currency == "Select Currency" or to_currency == "Select Currency":
        ans.config(text="Please select valid currencies!", fg="#0e0d0d",font=('Arial', 28))
        return

    try:
        api_url = f"https://v6.exchangerate-api.com/v6/cc6e98c26b00848bb144d603/latest/{from_currency}"
        response = requests.get(api_url)
        data = response.json()

        if data["result"] == "success":
            exchange_rate = data["conversion_rates"][to_currency]
            converted_amount = amount * exchange_rate

            ans.config(text=f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}", fg="#0e0d0d")

        else:
            ans.config(text="API error occurred! Please try again later.", fg="#e23030",font=('Arial', 28))

    except requests.exceptions.RequestException as e:
        ans.config(text=f"Network error: {e}", fg="#e23030",font=('Arial', 28))

def clear_screen():

    for widget in root.winfo_children():
        widget.destroy()


def technical():
    clear_screen()
    tech_frame = tk.Frame(root, bg="#fff")
    tech_frame.pack(fill="both", expand=True)

    def toggle():
        def close_toggle():
            toggle_menu.destroy()
            toggle_btn.config(text='☰')
            toggle_btn.config(command=toggle)

        toggle_menu = tk.Frame(root, bg='#fff')
        home_btn = tk.Button(toggle_menu, text='Home', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=home_page)
        home_btn.place(x=20, y=20)
        tech_btn = tk.Button(toggle_menu, text='Technical', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=technical)
        tech_btn.place(x=20, y=100)
        info_btn = tk.Button(toggle_menu, text='Tool', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2',command=tools)
        info_btn.place(x=20, y=180)

        window_height = root.winfo_height()
        toggle_menu.place(x=1300, y=50, height=window_height, width=250)
        toggle_btn.config(text='X')
        toggle_btn.config(command=close_toggle)

    toggle_btn = tk.Button(tech_frame, text='☰', bg='#00008B', fg='#fff', font=('Bold', 20), bd=0,
                           activebackground='#00008B', activeforeground='#fff',cursor='hand2', command=toggle)
    toggle_btn.place(x=1480, y=2)
    global logo_img
    logo_img = resizeImage("mainlogo2.jpg", 110, 80)
    logo_label = tk.Label(tech_frame, image=logo_img, borderwidth=0, bg="#00008B")
    logo_label.place(x=30, y=30)

    title = tk.Label(tech_frame, text='XE Live Exchange Rates', font=('Arial', 36), bg="#fff",fg='#00008B')
    title.place(x=480, y=100)

    API_KEY = 'cc6e98c26b00848bb144d603'

    def fetch_exchange_rates(base_currency):
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
        else:
            print("Error fetching data")
            return {}

    def create_table(parent, exchange_data, base_currency):

        for widget in parent.winfo_children():
            widget.destroy()

        columns = ("Currency", "Amount")
        tree = ttk.Treeview(parent, columns=columns, show="headings",height=20)

        tree.heading("Currency", text="Currency")
        tree.heading("Amount", text="Amount")

        tree.column("Currency", width=200)
        tree.column("Amount", width=200)

        currencies = ["USD", "EUR", "GBP", "AUD", "CAD", "JPY", "CNY", "CHF", "NZD", "SEK",
                      "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "ZAR", "BRL"]
        rates = {currency: exchange_data.get(currency, 0) for currency in currencies}

        for currency in currencies:
            if currency != base_currency:
                amount = rates[currency] * rates.get(base_currency, 1)  # Convert amount to base_currency
            else:
                amount = rates[currency]  # Base currency amount is just the rate itself
            tree.insert("", "end", values=(currency, f"{amount:.2f}"))

        tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    def update_data(event):
        selected_currency = currency_var.get()
        exchange_data = fetch_exchange_rates(selected_currency)
        create_table(table_frame, exchange_data, selected_currency)


    currency_var = tk.StringVar(value="INR")
    currency_label = tk.Label(root, text="Select Base Currency", font='Arial 16',bg="#fff")
    currency_label.place(x=480, y=200)
    currency_dropdown = ttk.Combobox(root, font='Arial 14', textvariable=currency_var, values=["USD", "EUR", "GBP", "AUD", "CAD",
                                                                              "JPY", "CNY", "CHF", "NZD", "SEK",
                                                                              "MXN", "SGD", "HKD", "NOK", "KRW",
                                                                              "TRY", "RUB", "INR", "ZAR", "BRL"],
                                     state="readonly")
    currency_dropdown.place(x=710, y=200)
    currency_dropdown.bind("<<ComboboxSelected>>", update_data)

    table_frame = tk.Frame(root)
    table_frame.place(x=550, y=300)

    exchange_data = fetch_exchange_rates("INR")
    create_table(table_frame, exchange_data, "INR")


def tools():
    clear_screen()
    tool_frame = tk.Frame(root, bg="#fff")
    tool_frame.pack(fill="both", expand=True)

    def toggle():
        def close_toggle():
            toggle_menu.destroy()
            toggle_btn.config(text='☰')
            toggle_btn.config(command=toggle)

        toggle_menu = tk.Frame(root, bg='#fff')
        home_btn = tk.Button(toggle_menu, text='Home', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=home_page)
        home_btn.place(x=20, y=20)
        tech_btn = tk.Button(toggle_menu, text='Technical', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=technical)
        tech_btn.place(x=20, y=100)
        info_btn = tk.Button(toggle_menu, text='Tool', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2',command=tools)
        info_btn.place(x=20, y=180)

        window_height = root.winfo_height()
        toggle_menu.place(x=1300, y=50, height=window_height, width=250)
        toggle_btn.config(text='X')
        toggle_btn.config(command=close_toggle)

    toggle_btn = tk.Button(tool_frame, text='☰', bg='#00008B', fg='#fff', font=('Bold', 20), bd=0,
                           activebackground='#00008B', activeforeground='#fff',cursor='hand2', command=toggle)
    toggle_btn.place(x=1480, y=2)

    global logo_img
    logo_img = resizeImage("mainlogo2.jpg", 110, 80)
    logo_label = tk.Label(tool_frame, image=logo_img, borderwidth=0, bg="#00008B")
    logo_label.place(x=30, y=30)

    title = tk.Label(tool_frame, text="The world's most popular currency tools", font=('Arial', 36), bg="#fff",fg="#00008B")
    title.place(x=350, y=100)
    img = tk.PhotoImage(file="freamm.png")
    image_label = tk.Label(tool_frame, image=img,bd=0)
    image_label.image = img
    image_label.place(x=350, y=200)

    global binance, mudrex, trust, bicoin, hotcoin,bitunix, coincheck, Kraken
    binance = resizeImage("binance.png", 60, 60)
    image_label = tk.Label(tool_frame, image=binance,bg="#fff")
    image_label.place(x=440,y=240)
    tex = tk.Label(tool_frame,text="Binance",font=('Arial', 20),bg="#fff")
    tex.place(x=520,y=250)

    mudrex = resizeImage("mudrex.png", 60, 60)
    image_label2 = tk.Label(tool_frame, image=mudrex, bg="#fff")
    image_label2.place(x=440, y=330)
    tex2 = tk.Label(tool_frame, text="Mudrex", font=('Arial', 20), bg="#fff")
    tex2.place(x=520, y=340)

    trust = resizeImage("trust.png", 60, 60)
    image_label3 = tk.Label(tool_frame, image=trust, bg="#fff")
    image_label3.place(x=440, y=420)
    tex3 = tk.Label(tool_frame, text="Trust", font=('Arial', 20), bg="#fff")
    tex3.place(x=520, y=430)

    bicoin = resizeImage("bicoinnomy.png", 60, 60)
    image_label4 = tk.Label(tool_frame, image=bicoin, bg="#fff")
    image_label4.place(x=440, y=510)
    tex4 = tk.Label(tool_frame, text="Biconomy", font=('Arial', 20), bg="#fff")
    tex4.place(x=520, y=520)

    hotcoin = resizeImage("hotcoin.png", 60, 60)
    image_label5 = tk.Label(tool_frame, image=hotcoin, bg="#fff")
    image_label5.place(x=780, y=240)
    tex5 = tk.Label(tool_frame, text="Hotcoin", font=('Arial', 20), bg="#fff")
    tex5.place(x=860, y=250)

    bitunix = resizeImage("bitunix.png", 60, 60)
    image_label6 = tk.Label(tool_frame, image=bitunix, bg="#fff")
    image_label6.place(x=780, y=330)
    tex6 = tk.Label(tool_frame, text="Bitunix", font=('Arial', 20), bg="#fff")
    tex6.place(x=860, y=340)

    coincheck = resizeImage("coincheck.png", 60, 60)
    image_label7 = tk.Label(tool_frame, image=coincheck, bg="#fff")
    image_label7.place(x=780, y=420)
    tex7 = tk.Label(tool_frame, text="Coincheck", font=('Arial', 20), bg="#fff")
    tex7.place(x=860, y=430)

    Kraken = resizeImage("Kraken.png", 60, 60)
    image_label8 = tk.Label(tool_frame, image=Kraken, bg="#fff")
    image_label8.place(x=780, y=510)
    tex8 = tk.Label(tool_frame, text="Kraken", font=('Arial', 20), bg="#fff")
    tex8.place(x=860, y=520)


def home_page():
    clear_screen()

    def toggle():
        def close_toggle():
            toggle_menu.destroy()
            toggle_btn.config(text='☰')
            toggle_btn.config(command=toggle)

        toggle_menu = tk.Frame(root, bg='#fff')
        home_btn = tk.Button(toggle_menu, text='Home', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=home_page)
        home_btn.place(x=20, y=20)
        tech_btn = tk.Button(toggle_menu, text='Technical', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=technical)
        tech_btn.place(x=20, y=100)
        info_btn = tk.Button(toggle_menu, text='Tool', font=('Bold', 20), bd=0, bg='#fff', fg='black',
                             activebackground='#fff', activeforeground='black',cursor='hand2', command=tools)
        info_btn.place(x=20, y=180)

        window_height = root.winfo_height()
        toggle_menu.place(x=1300, y=50, height=window_height, width=250)
        toggle_btn.config(text='X')
        toggle_btn.config(command=close_toggle)

    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    frame_canvas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

    global amount_entry, combobox_var, combobox_var1
    global puppyLarge_img, logo_img
    puppyLarge_img = resizeImage("logo.png", 1530, 410)
    image_label = tk.Label(frame_canvas, image=puppyLarge_img)
    image_label.pack(anchor="nw")

    logo_img = resizeImage("mainlogo.png", 110, 80)
    logo_label = tk.Label(frame_canvas, image=logo_img, borderwidth=0, bg="#00008B")
    logo_label.place(x=30, y=30)

    te = tk.Label(root, text="Currency Converter", font='Arial 26', fg="#fff", bg="#00008B")
    te.place(x=600, y=90)

    tex = tk.Label(root, text="Check live foreign currency exchange rates", font='Arial 16', fg="#fff", bg="#00008B")
    tex.place(x=570, y=150)

    toggle_btn = tk.Button(frame_canvas, text='☰', bg='#00008B', fg='#fff', font=('Bold', 20), bd=0,
                           activebackground='#00008B', activeforeground='#fff',cursor='hand2', command=toggle)
    toggle_btn.place(x=1480, y=2)

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    shadow_frame = tk.Frame(master=root, width=800, height=300, bg='#888')
    shadow_frame.place(x=385, y=225)

    form_frame = ctk.CTkFrame(master=root, width=800, height=300)
    form_frame.place(x=380, y=220)

    amount_label = tk.Label(master=form_frame, text="Amount", bg="#DCDCDC", font='Arial 16')
    amount_label.place(x=50, y=20)
    amount_entry = ctk.CTkEntry(master=form_frame, width=170, placeholder_text="Amount")
    amount_entry.place(x=20, y=86)

    from_label = tk.Label(master=form_frame, text="From", bg="#DCDCDC", font='Arial 16')
    from_label.place(x=340, y=20)

    currency_data1 = [
        {"code": "USD", "name": "US Dollar"},
        {"code": "EUR", "name": "Euro"},
        {"code": "GBP", "name": "British Pound"},
        {"code": "CAD", "name": "Canadian Dollar"},
        {"code": "AUD", "name": "Australian Dollar"},
        {"code": "JPY", "name": "Japanese Yen"},
        {"code": "INR", "name": "Indian Rupee"},
    ]

    combobox_var = tk.StringVar()
    combobox_var.set("Select Currency")
    combobox_from = ttk.Combobox(master=form_frame, textvariable=combobox_var, width=20, font=16, state="readonly",cursor='hand2')
    combobox_from.place(x=280, y=86)
    combobox_from['values'] = [f"{currency['code']} - {currency['name']}" for currency in currency_data1]

    to_label1 = tk.Label(master=form_frame, text="To", bg="#DCDCDC", font='Arial 16')
    to_label1.place(x=650, y=20)

    combobox_var1 = tk.StringVar()
    combobox_var1.set("Select Currency")
    combobox_to = ttk.Combobox(master=form_frame, textvariable=combobox_var1, width=20, font=16, state="readonly",cursor='hand2')
    combobox_to.place(x=570, y=86)
    combobox_to['values'] = [f"{currency['code']} - {currency['name']}" for currency in currency_data1]
    global ans
    ans = tk.Label(master=root,height=3,width=25,font='Arial 28',bg="#DCDCDC",fg="#0e0d0d")
    ans.place(x=400,y=370)

    button = ctk.CTkButton(master=root, text='Convert', height=50, font=("Helvetica", 24),cursor='hand2', command=on_convert)
    button.place(x=950, y=400)

home_page()
root.mainloop()
