import socket
import threading

def listen_server(sock):
    """
    Поток/функция для постоянного прослушивания входящих UDP-сообщений от сервера
    и вывода их на экран.
    """
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8', errors='replace')
            print(message)
        except OSError:
            # Сокет закрыт или возникла ошибка
            break
        except Exception as e:
            print(f"[КЛИЕНТ] Ошибка при получении сообщения: {e}")
            break

def run_udp_chat_client(server_host='localhost', server_port=9999):
    """
    Запускает UDP-клиент для многопользовательского чата.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)  # Блокирующий режим при чтении

    # Запускаем поток прослушивания
    listener = threading.Thread(target=listen_server, args=(sock,), daemon=True)
    listener.start()

    print(f"[КЛИЕНТ] Подключаемся к серверу {server_host}:{server_port}")
    print("[КЛИЕНТ] Чтобы выйти, введите 'exit' и нажмите Enter.")

    try:
        while True:
            message = input()
            if not message:
                continue  # пустой ввод, продолжаем
            if message.strip().lower() == 'exit':
                print("[КЛИЕНТ] Завершение работы клиента.")
                break
            # Отправляем сообщение на сервер
            try:
                sock.sendto(message.encode('utf-8'), (server_host, server_port))
            except Exception as e:
                print(f"[КЛИЕНТ] Ошибка при отправке сообщения: {e}")
    except KeyboardInterrupt:
        print("\n[КЛИЕНТ] Завершение работы клиента по запросу пользователя (Ctrl+C)...")
    finally:
        sock.close()
        print("[КЛИЕНТ] Сокет закрыт. Клиент остановлен.")

if __name__ == '__main__':
    # Ввод параметров сервера пользователем
    host_input = input("Введите адрес сервера (по умолчанию localhost): ").strip()
    if not host_input:
        host_input = 'localhost'
    port_input = input("Введите порт сервера (по умолчанию 9999): ").strip()
    if not port_input.isdigit():
        port_input = '9999'
    port_input = int(port_input)

    run_udp_chat_client(host_input, port_input)