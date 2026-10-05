passwords = ['pass', 'word', 'pass', 'password', '1234556', 'password123']

first_pass = passwords[0]
last_pass = passwords[-1]

print(first_pass)
print(last_pass)

passwords.append('newpassword')

print('admin' in passwords)

for password in passwords:
    if len(password) > 5:
        print(f"{password} ok")
    else:
        print(f"{password} WEAK")

LOGIN_SUCCESS_CODE = 'cowrie.login.success'
LOGIN_FAILED_CODE = 'cowrie.login.failed'

loginattempts = []
loginattempts.append(dict(eventid=LOGIN_FAILED_CODE, username='admin', password='123456', src_ip='1.2.3.4', src_port=2222))
loginattempts.append(dict(eventid=LOGIN_FAILED_CODE, username='admin1', password='78456', src_ip='1.2.3.4', src_port=2222))
loginattempts.append(dict(eventid=LOGIN_SUCCESS_CODE, username='admin2', password='237564', src_ip='1.2.3.4', src_port=2222))
loginattempts.append(dict(eventid=LOGIN_FAILED_CODE, username='admin3', password='pass', src_ip='1.2.3.4', src_port=2222))


for loginattempt in loginattempts:
    if (loginattempt.get('eventid') == LOGIN_SUCCESS_CODE):
        print(f"Successful Login attempt: {loginattempt.get('username')}/{loginattempt.get('password')} from {loginattempt.get('src_ip')}:{loginattempt.get('src_port')}")

password_counts = dict()

for password in passwords:
    password_counts[password] = password_counts.get(password, 0) + 1
print(f"Password counts: {password_counts}")