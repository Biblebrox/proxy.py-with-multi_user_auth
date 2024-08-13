from proxy import Proxy
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    proxy_params = [
        "--hostname", "0.0.0.0",
        "--port", "8899",
        "--enable-dashboard",
        "--plugins", "multi_user_auth_plugin.MultiUserAuthPlugin"
    ]

    try:
        with Proxy(proxy_params) as p:
            print(f"Proxy запущен на {p.flags.hostname}:{p.flags.port}")
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("Proxy остановлен")
    except Exception as e:
        print(f"Error: {e}")
        
