import re
import json


def parse_receipt(file_path):
    # Читаем файл
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # ---------- ИЗВЛЕКАЕМ ЦЕНЫ ----------
    # Поддержка формата 12.34 и 12,34
    prices = re.findall(r"\d+[.,]\d{2}", text)
    prices = [float(price.replace(",", ".")) for price in prices]

    # ---------- ИЗВЛЕКАЕМ ТОВАРЫ ----------
    # Ищем строки типа: Название 12.34
    items = re.findall(r"([A-Za-zА-Яа-я\s]+)\s+(\d+[.,]\d{2})", text)

    formatted_items = []
    for name, price in items:
        formatted_items.append({
            "name": name.strip(),
            "price": float(price.replace(",", "."))
        })

    # ---------- ИЗВЛЕКАЕМ ДАТУ ----------
    date_match = re.search(r"\d{2}[./-]\d{2}[./-]\d{4}", text)
    date = date_match.group() if date_match else None

    # ---------- ИЗВЛЕКАЕМ ВРЕМЯ ----------
    time_match = re.search(r"\d{2}:\d{2}", text)
    time = time_match.group() if time_match else None

    # ---------- ИЩЕМ СПОСОБ ОПЛАТЫ ----------
    payment_match = re.search(
        r"(Card|Cash|Visa|Mastercard|Мир|Наличные|Карта)",
        text,
        re.IGNORECASE
    )
    payment_method = payment_match.group() if payment_match else None

    # ---------- ИЩЕМ TOTAL ----------
    total_match = re.search(r"(Total|Итого)[^\d]*(\d+[.,]\d{2})", text)
    if total_match:
        total = float(total_match.group(2).replace(",", "."))
    else:
        total = sum(prices)

    # ---------- СОБИРАЕМ JSON ----------
    result = {
        "items": formatted_items,
        "all_prices": prices,
        "total": total,
        "date": date,
        "time": time,
        "payment_method": payment_method
    }

    return result


if __name__ == "__main__":
    parsed_data = parse_receipt("raw.txt")

    # Красивый вывод
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))