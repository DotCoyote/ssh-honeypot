username = "root"
password = "123456"
src_ip = "1.2.3.4"
port = 2222

print(f"{type(username)} {type(password)} {type(src_ip)} {type(port)}")

print(f"Login attempt: {username}/{password} from {src_ip}:{port}")