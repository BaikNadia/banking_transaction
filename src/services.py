import json
import logging

def search_transactions(query, transactions):
    """
    Выполняет поиск транзакций по описанию или категории.

    Args:
        query (str): Строка поиска.
        transactions (List[Dict]): Список транзакций для поиска.

    Returns:
        str: JSON-строка с результатами поиска.
    """
    try:
        results = [t for t in transactions if query.lower() in t.get('Описание', '').lower()
                  or query.lower() in t.get('Категория', '').lower()]
        logging.info(f"Search completed for query: {query}")
        return json.dumps(results, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Search error: {e}")
        return json.dumps([])
