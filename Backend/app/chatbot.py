from app.ollama_proxy import query_ollama

def get_response(message, user_type='guest', department=None, role=None):
    if user_type == 'guest':
        # Guest bot: limited info, uses Ollama with guest data
        return query_ollama(message, user_role='guest')
    elif user_type == 'student':
        # Institutional bot: department-specific, role-based, uses Ollama with context
        if department == 'BSC CSIT':
            return query_ollama(message, department=department, role=role)
        elif department == 'BIT':
            return query_ollama(message, department=department, role=role)
        else:
            return "Invalid department."
    else:
        return "Invalid user type."
