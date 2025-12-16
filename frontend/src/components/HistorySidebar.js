import React from 'react';
import './HistorySidebar.css';

const HistorySidebar = ({ history }) => {
    return (
        <aside className="sidebar">
            <h2 className="sidebar-title">История</h2>
            <ul className="history-list">
                {history.length > 0 ? (
                    history.map((item, index) => (
                        <li key={index} className="history-item" title={item.subject}>
                            {item.subject}
                        </li>
                    ))
                ) : (
                    <p>Здесь будет история ваших запросов.</p>
                )}
            </ul>
        </aside>
    );
};

export default HistorySidebar;