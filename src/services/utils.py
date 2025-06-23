def format_ticket_info(ticket: tuple) -> str:
    return (
        f"Тикет #{ticket[0]}\n"
        f"👤: {ticket[2]}\n"
        f"❓: {ticket[3]}\n"
        f"✅: {'Закрыт' if ticket[5] == 'closed' else 'Открыт'}"
    )