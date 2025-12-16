import React from 'react';
import './ResultDisplay.css';

// Списки возможных вариантов
const ALL_EQUIPMENT = ["Ноутбук", "Сервер", "СХД"];
const ALL_FAILURES = [
    "Аккумулятор", "Блок питания", "Вентилятор", "Динамики", "Диск",
    "Jack", "Камера", "Клавиатура", "Консультация", "Корпус",
    "Материнская плата", "Матрица", "Оперативная память", "Программное обеспечение",
    "Сервер", "SFP модуль", "Wi-fi антенна", "Wi-fi модуль"
];

const chunkArray = (array, size) => {
    const chunked_arr = [];
    for (let i = 0; i < array.length; i += size) {
        chunked_arr.push(array.slice(i, i + size));
    }
    return chunked_arr;
};

const failureChunks = chunkArray(ALL_FAILURES, Math.ceil(ALL_FAILURES.length / 3));

const GraphNode = ({ id, label, isActive }) => (
    <div id={id} className={`graph-node ${isActive ? 'active' : 'inactive'}`}>
        {label}
    </div>
);

const ResultDisplay = ({ result }) => {
    if (!result) return null;

    const { equipment, failure_point, serial_number } = result;
    const isUndefined = equipment === "Не определено" || failure_point === "Не определено";

    if (isUndefined) {
        return (
            <div className="result-container">
                 {serial_number && (
                    <div className="serial-number-badge">
                        S/N: {serial_number}
                    </div>
                )}
                <div className="undefined-result-message">
                    <strong>Недостаточно данных.</strong>
                    <p>Система не смогла с уверенностью определить проблему. Пожалуйста, уточните описание заявки.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="result-container">
            {}
            {serial_number && (
                <div className="serial-number-badge">
                    S/N: {serial_number}
                </div>
            )}
            {}
            
            <div className="graph-area-no-arrow">
                {}
                <div className="column-group">
                    <h3 className="column-title">Тип оборудования</h3>
                    <div className="node-column">
                        {ALL_EQUIPMENT.map(item => (
                            <GraphNode
                                key={item}
                                id={`eq-${item}`}
                                label={item}
                                isActive={item === equipment}
                            />
                        ))}
                    </div>
                </div>
                
                {}
                <div className="column-group failure-group">
                    <h3 className="column-title">Точки отказа</h3>
                    <div className="failure-columns-container">
                        {failureChunks.map((chunk, index) => (
                            <div className="node-column" key={index}>
                                {chunk.map(item => (
                                    <GraphNode
                                        key={item}
                                        id={`fail-${item}`}
                                        label={item}
                                        isActive={item === failure_point}
                                    />
                                ))}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultDisplay;