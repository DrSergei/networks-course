import argparse
import email.message
import smtplib

LOGIN = "YOUR EMAIL"
PASSWORD = "YOUR PASSWORD"

def get_content(file):
    with open(file) as f:
        return f.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Email")
    parser.add_argument("--data")
    parser.add_argument("--to")
    parser.add_argument("--html", action="store_true")

    args = parser.parse_args()
    msg = email.message.EmailMessage()

    data = get_content(args.data)
    if args.html:
        msg.add_alternative(data, "html")
    else:
        msg.set_content(data)
    msg["Subject"] = "Test"
    msg["From"] = LOGIN
    msg["To"] = args.to

    # https://rushstudio.by/blog/razrabotchiku/reshenie_problemy_s_otpravkoy_pisem_cherez_yandeks_v_bitrixvm/
    # Нужно выполнить инструкцию чтобы можно было использовать самописный клиент
    smtp = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
    smtp.ehlo()
    smtp.login(LOGIN, PASSWORD)
    smtp.send_message(msg)
    smtp.quit()
