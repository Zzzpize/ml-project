const API_URL = "http://localhost:8000/api/predict";

export const predictTicket = async (subject, description) => {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subject, description }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || 'Ошибка сети или сервера');
    }

    return response.json();
};