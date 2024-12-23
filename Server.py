import socket
import sys
import logging

def run_udp_chat_server(host='0.0.0.0', port=9999):
    """
    Запускает многопользовательский чат-сервер на базе UDP.
    Все полученные сообщения рассылаются всем подключённым клиентам.
    """
    # Настройка логирования
    logging.basicConfig(
        filename='udp_chat_server.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger()

    try:
        # Создаём UDP-сокет
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        logger.info(f"Сервер запущен на {host}:{port}")
        print(f"[СЕРВЕР] Запущен на {host}:{port}")
    except OSError as e:
        logger.error(f"Не удалось запустить сервер на {host}:{port}: {e}")
        print(f"[СЕРВЕР] Не удалось запустить сервер на {host}:{port}: {e}")
        sys.exit(1)

    # Храним адреса клиентов в set (чтобы не было дубликатов)
    clients = set()

    try:
        while True:
            try:
                # Получаем данные от клиента
                data, addr = sock.recvfrom(1024)
                message = data.decode('utf-8', errors='replace').strip()

                # Если новый клиент — добавляем в список
                if addr not in clients:
                    clients.add(addr)
                    logger.info(f"Новый клиент {addr}. Всего клиентов: {len(clients)}")
                    print(f"[СЕРВЕР] Новый клиент {addr}. Всего клиентов: {len(clients)}")

                # Логируем сообщение на сервере
                logger.info(f"[{addr}] {message}")
                print(f"[{addr}] {message}")

                # Формируем сообщение для рассылки
                broadcast_data = f"{addr} >> {message}".encode('utf-8')

                # Рассылаем полученное сообщение всем клиентам
                for client_addr in clients:
                    try:
                        sock.sendto(broadcast_data, client_addr)
                    except Exception as e:
                        logger.error(f"Ошибка при отправке клиенту {client_addr}: {e}")
                        print(f"[СЕРВЕР] Ошибка при отправке клиенту {client_addr}: {e}")
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения: {e}")
                print(f"[СЕРВЕР] Ошибка при обработке сообщения: {e}")
    except KeyboardInterrupt:
        logger.info("Остановка сервера по запросу пользователя (Ctrl+C)...")
        print("\n[СЕРВЕР] Остановка сервера по запросу пользователя (Ctrl+C)...")
    finally:
        sock.close()
        logger.info("Сокет закрыт. Сервер остановлен.")
        print("[СЕРВЕР] Сокет закрыт. Сервер остановлен.")

if __name__ == '__main__':
    # Ввод параметров сервера пользователем
    host_input = input("Введите адрес сервера (по умолчанию 0.0.0.0): ").strip()
    if not host_input:
        host_input = '0.0.0.0'
    port_input = input("Введите порт сервера (по умолчанию 9999): ").strip()
    if not port_input.isdigit():
        port_input = '9999'
    port_input = int(port_input)

    run_udp_chat_server(host_input, port_input)