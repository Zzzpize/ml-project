import React from 'react';
import Xarrow, { Xwrapper } from 'react-xarrows';
import './ResultDisplay.css';

const ALL_EQUIPMENT = ["Ноутбук", "Сервер", "СХД"];
const ALL_FAILURES = [
    "Аккумулятор", "Блок питания", "Вентилятор", "Динамики", "Диск",
    "Jack", "Камера", "Клавиатура", "Консультация", "Корпус",
    "Материнская плата", "Матрица", "Оперативная память", "Программное обеспечение",
    "Сервер", "SFP модуль", "Wi-fi антенна", "Wi-fi модуль"
];

const GraphNode = ({ id, label, isActive }) => (
    <div id={id} className={`graph-node ${isActive ? 'active' : 'inactive'}`}>
        {label}
    </div>
);

const ResultDisplay = ({ result }) => {
    if (!result) return null;

    const { equipment, failure_point, serial_number } = result;

    return (
        <div className="result-container">
            {serial_number && (
                <div className="serial-number-badge">
                    S/N: {serial_number}
                </div>
            )}
            <Xwrapper>
                <div className="graph-area">
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
                    <div className="node-column">
                        {ALL_FAILURES.map(item => (
                            <GraphNode
                                key={item}
                                id={`fail-${item}`}
                                label={item}
                                isActive={item === failure_point}
                            />
                        ))}
                    </div>
                </div>
                {}
                <Xarrow
                    start={`eq-${equipment}`}
                    end={`fail-${failure_point}`}
                    color="#00c853"
                    strokeWidth={3}
                    path="smooth"
                    curveness={0.8}
                    headSize={5}
                />
            </Xwrapper>
        </div>
    );
};

export default ResultDisplay;