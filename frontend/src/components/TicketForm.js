import React, { useState } from 'react';
import './TicketForm.css';

const TicketForm = ({ onSubmit, isLoading }) => {
    const [subject, setSubject] = useState('');
    const [description, setDescription] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!subject || !description) {
            alert('Пожалуйста, заполните оба поля');
            return;
        }
        onSubmit(subject, description);
    };

    return (
        <form onSubmit={handleSubmit} className="ticket-form-container">
            <input
                type="text"
                className="form-input"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Тема заявки (например, 'Не работает ноутбук')"
            />
            <textarea
                className="form-textarea"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Полное описание проблемы..."
            />
            <button type="submit" className="form-button" disabled={isLoading}>
                {isLoading ? 'Анализ...' : 'Отправить'}
            </button>
        </form>
    );
};

export default TicketForm;